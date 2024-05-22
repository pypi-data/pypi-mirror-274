import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import matplotlib.pyplot as plt
from shapely import Point
from shapely.geometry import LineString
from shapely.ops import linemerge, unary_union

from imxInsights.utils.shapely_helpers import (
    extend_line,
    point_relative_to_linestring,
    reproject_point_to_line,
)

IMX_NS = {"": "http://www.prorail.nl/IMSpoor", "gml": "http://www.opengis.net/gml"}  # Global namespace dict


@dataclass
class ImxGraphPassage:
    puic: str
    name: str
    side_tag: str
    geometry: LineString
    speed: float | None = None


@dataclass(unsafe_hash=True)
class ImxGraphSwitchMechanism:
    puic: str
    name: str
    geometry: Point
    geometry_reprojected: Optional[Point] = None
    left_or_right_line: Optional[LineString] = None


class ImxGraphSwitchPositionEnum(Enum):
    LEFT = "left"
    RIGHT = "right"


@dataclass(unsafe_hash=True)
class ImxGraphSwitchPosition:
    switch_mechanism: ImxGraphSwitchMechanism
    position: ImxGraphSwitchPositionEnum


@dataclass
class ImxGraphJunctionPath:
    passages: list[ImxGraphPassage]
    geometry: LineString
    speed: float
    start: ImxGraphPassage
    end: ImxGraphPassage
    switches_in_path: list[ImxGraphSwitchPosition]


@dataclass
class ImxGraphPassageSwitchMechanismDistance:
    passage: str
    switch_mechanism: str
    distance: float


class ImxGraphJunction:
    def __init__(self, xml_data):
        self._r = ET.fromstring(xml_data)

        self.passages = self._parse_passages()
        self._st_passage = self._find_passage_by_name("S-T")
        self._pq_passage = self._find_passage_by_name("P-Q")
        self._center_line = self._calculate_center_line()

        self.switch_mechanisms = self._parse_switch_mechanisms()
        self._reproject_switch_mechanisms()
        self._passage_switch_distance_map = self._map_passages_to_switch_mechanisms()
        self._assign_switch_lines()

    @staticmethod
    def from_element(junction_element: ET.Element) -> "ImxGraphJunction":
        return ImxGraphJunction(ET.tostring(junction_element))

    @staticmethod
    def _parse_coordinates_linestring(coordinates_str: str) -> list[tuple[float, ...]]:
        return [tuple(map(float, coord.split(",")[:2])) for coord in coordinates_str.split()]

    def _parse_coordinates_point(self, coordinate_str: str) -> Point:
        return Point(self._parse_coordinates_linestring(coordinate_str)[0])

    def _parse_passages(self) -> dict[str, ImxGraphPassage]:
        return {
            passage.get("puic"): ImxGraphPassage(
                puic=passage.get("puic"),
                name=passage.get("name"),
                side_tag=passage.get("sideTag"),
                geometry=LineString(self._parse_coordinates_linestring(passage.find(".//gml:coordinates", IMX_NS).text)),
                speed=passage.get("passageSpeed", None),
            )
            for passage in self._r.findall(".//Passage", IMX_NS)
        }

    def _find_passage_by_name(self, name: str) -> Optional[str]:
        return next((puic for puic, passage in self.passages.items() if passage.name == name), None)

    def _parse_switch_mechanisms(self) -> dict[str, ImxGraphSwitchMechanism]:
        return {
            switch.get("puic"): ImxGraphSwitchMechanism(
                puic=switch.get("puic"),
                name=switch.get("name"),
                geometry=self._parse_coordinates_point(switch.find(".//gml:coordinates", IMX_NS).text),
            )
            for switch in self._r.findall(".//SwitchMechanism", IMX_NS)
        }

    def _calculate_center_line(self) -> LineString:
        passages_of_interest = {_.name: _ for puic, _ in self.passages.items() if _.name in ["R", "L", "V"]}
        if len(passages_of_interest.keys()) == 3:
            midpoints = {name: passage.geometry.centroid for name, passage in passages_of_interest.items()}
            left_midpoint = midpoints["V"].centroid
            right_midpoint = LineString([midpoints["L"], midpoints["R"]]).centroid

        elif len(self.passages.keys()) != 0:
            passages_of_interest = {_.name: _ for puic, _ in self.passages.items() if _.name in ["P", "T", "Q", "S"]}

            midpoints = {name: passage.geometry.centroid for name, passage in passages_of_interest.items()}
            left_midpoint = LineString([midpoints["P"], midpoints["T"]]).centroid
            right_midpoint = LineString([midpoints["Q"], midpoints["S"]]).centroid

        else:
            return LineString()

        center_point = LineString([left_midpoint, right_midpoint]).centroid
        center_line = LineString([left_midpoint, center_point, right_midpoint])

        return center_line

    def _reproject_switch_mechanisms(self) -> None:
        for switch in self.switch_mechanisms.values():
            switch.geometry_reprojected = reproject_point_to_line(switch.geometry, self._center_line)

    def _map_passages_to_switch_mechanisms(self) -> dict[str, Optional[ImxGraphPassageSwitchMechanismDistance]]:
        passage_switch_distance_map = {}

        for passage_id, passage_geom in self.passages.items():
            closest_switch = None
            min_distance = 0.0

            # the controlled switch mech is the one with the most distance to the passage
            for switch_id, switch_geom in self.switch_mechanisms.items():
                distance = passage_geom.geometry.distance(switch_geom.geometry_reprojected)
                if distance > min_distance:
                    min_distance = distance
                    closest_switch = (switch_id, distance)
            if len(self.switch_mechanisms.keys()) != 0:
                passage_switch_distance_map[passage_id] = ImxGraphPassageSwitchMechanismDistance(passage_id, *closest_switch)

        all_mapped = all(mapping is not None for mapping in passage_switch_distance_map.values())
        all_mapped_reversed = all(mapping is None for mapping in passage_switch_distance_map.values())
        if not all_mapped and not all_mapped_reversed:
            raise ValueError("Some passages could not be mapped to a switch mechanism.")

        return passage_switch_distance_map

    def _assign_switch_lines(self):
        for passage_id, switch_info in self._passage_switch_distance_map.items():
            if switch_info is None or switch_info.switch_mechanism is None:
                continue

            switch_mech_id = switch_info.switch_mechanism
            switch_mech = self.switch_mechanisms[switch_mech_id]
            passage = self.passages[passage_id]

            if not switch_mech.left_or_right_line:
                projected_passage_point = self._center_line.interpolate(self._center_line.project(passage.geometry.centroid))

                switch_mech_line = extend_line(switch_mech.geometry_reprojected, projected_passage_point, extension_meters=25, extend_from="end")

                switch_mech.left_or_right_line = switch_mech_line

    def _passage_left_or_right_of_switch(self, switch_mech: ImxGraphSwitchMechanism, passage: ImxGraphPassage) -> str:
        projected_passage_point = self._center_line.interpolate(self._center_line.project(passage.geometry.centroid))
        extended_line_from_switch = extend_line(switch_mech.geometry_reprojected, projected_passage_point, extension_meters=10, extend_from="end")
        is_passage_right_of_switch = point_relative_to_linestring(extended_line_from_switch, passage.geometry.centroid)
        return is_passage_right_of_switch

    @staticmethod
    def _get_speed_in_path(passages: list[ImxGraphPassage]) -> float:
        return float("inf") if all(value.speed is None for value in passages) else min([_.speed for _ in passages])

    @staticmethod
    def _validate_path(passages: list[ImxGraphPassage]) -> bool:
        if any(passage is None for passage in passages):
            return False

        geometries = [passage.geometry for passage in passages if passage]
        merged = linemerge(unary_union(geometries))
        return merged.is_valid and merged.geom_type == "LineString"

    def _get_path_geometry(self, path_puics: list[str]) -> LineString:
        start_passage = self.passages.get(path_puics[0])
        end_passage = self.passages.get(path_puics[-1])

        side_tag_insertions = {
            ("T", "S"): self._st_passage,
            ("S", "T"): self._st_passage,
            ("P", "Q"): self._pq_passage,
            ("Q", "P"): self._pq_passage,
        }
        side_tag_pair = (start_passage.side_tag, end_passage.side_tag)
        if side_tag_pair in side_tag_insertions and side_tag_insertions[side_tag_pair] is not None:
            path_puics = [path_puics[0], side_tag_insertions[side_tag_pair], path_puics[-1]]

        return linemerge([self.passages[puic].geometry for puic in path_puics if puic in self.passages])

    def get_path(self, path_puics: list[str]) -> ImxGraphJunctionPath:
        passages = [self.passages.get(puic) for puic in path_puics]
        if not self._validate_path(passages):
            raise ValueError("path is not valid")

        min_speed = self._get_speed_in_path(passages)
        geometry = self._get_path_geometry(path_puics)
        start = self.passages.get(path_puics[0])
        end = self.passages.get(path_puics[-1])

        switches_positions_in_path = []
        if len(self._passage_switch_distance_map.keys()) == 0:
            switches_positions_in_path = []
        else:
            for puic in path_puics:
                passage_switch_distance_map = self._passage_switch_distance_map[puic]

                switch_mech = self.switch_mechanisms[passage_switch_distance_map.switch_mechanism]

                passage = self.passages[puic]

                if passage.side_tag != "V":
                    left_or_right = self._passage_left_or_right_of_switch(switch_mech, passage)
                    switches_positions_in_path.append(ImxGraphSwitchPosition(switch_mech, ImxGraphSwitchPositionEnum[left_or_right.upper()]))

            switches_positions_in_path = list(set(switches_positions_in_path))

        return ImxGraphJunctionPath(
            passages=passages, speed=min_speed, geometry=geometry, start=start, end=end, switches_in_path=switches_positions_in_path
        )

    ####################################################################################################

    def plot_path_with_elements(self, path_geometries=None, path_title=""):
        fig, ax = plt.subplots()

        def plot_line(x, y, label, style_dict, with_markers=True):
            # Use the label only for the first call to this function
            ax.plot(x, y, label=label, **style_dict)
            if with_markers:
                ax.text((x[0] + x[-1]) / 2, (y[0] + y[-1]) / 2, label, fontsize=9, ha="center")

        # Plot passages
        passage_style = {"marker": "o", "linestyle": "-", "markersize": 5, "linewidth": 3}
        for passage in self.passages.values():
            x, y = passage.geometry.xy
            plot_line(x, y, passage.name, passage_style)

        # Plot switch mechanisms and reprojected switch mechanisms
        switch_colors = ["red", "orange"]
        for idx, switch in enumerate(self.switch_mechanisms.values()):
            # Plot left or right line for switch mechanism
            if switch.left_or_right_line:
                x, y = switch.left_or_right_line.xy

                switch_mechanism_line_style = {
                    "marker": "o",
                    "linestyle": "--",
                    "markersize": 5,
                    "linewidth": 5,
                    "color": switch_colors[idx % len(switch_colors)],
                }
                plot_line(x, y, f"{switch.name} switch mechanism line", switch_mechanism_line_style)
                ax.plot(x, y, linestyle="--", linewidth=5, color=switch_colors[idx % len(switch_colors)])

            # Original and reprojected switch positions with unique labels
            for geom, geom_label in zip([switch.geometry, switch.geometry_reprojected], ["", "\n(reprojected)"]):
                ax.plot(geom.x, geom.y, "^", markersize=10, color=switch_colors[idx % len(switch_colors)])
                ax.text(geom.x, geom.y, f"{switch.name}{geom_label}", fontsize=9, color="red", ha="center")

        # Plot center line

        ax.plot(*self._center_line.xy, label="Center Line", marker="", linestyle="--", linewidth=5, color="green")

        # Plot path
        path_style = {"marker": ">", "linestyle": "--", "linewidth": 6, "color": "magenta"}

        if path_geometries:
            x, y = path_geometries.xy

            for i in range(len(x) - 1):
                dx = x[i + 1] - x[i]
                dy = y[i + 1] - y[i]
                plt.arrow(x[i], y[i], dx, dy, head_width=1, head_length=1, fc="magenta", ec="magenta")

            plot_line(x, y, "Path", path_style)

        # Final plot adjustments
        ax.set_aspect("equal", adjustable="datalim")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.title(f"Graph junction {path_title}")
        plt.legend(loc="upper left", fontsize="small")
        plt.show()
