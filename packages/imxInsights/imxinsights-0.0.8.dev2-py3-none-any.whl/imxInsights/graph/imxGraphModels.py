from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar

from lxml.etree import Element
from shapely import LineString, Point

from imxInsights.domain.models.imxRelation import ImxRelation
from imxInsights.graph.imxGraphJunction import ImxGraphJunction, ImxGraphSwitchPosition
from imxInsights.repo.tree.objectTreeProtocol import ImxObjectProtocol
from imxInsights.utils.log import logger
from imxInsights.utils.shapely_geojson import GeoJsonFeature, GeoJsonFeatureCollection
from imxInsights.utils.shapely_helpers import ShapelyTransform

T = TypeVar("T")


def parse_to_bool_if_unknown_true(string):
    string_lower = string.lower()
    if string_lower == "true":
        return True
    elif string_lower == "false":
        return False
    elif string_lower == "unknown":
        return True
    else:
        raise ValueError("Invalid boolean string: {}".format(string))


@dataclass
class ImxRailConnection:
    imx_object: ImxObjectProtocol
    puic: str = field(init=False)
    passage_refs: List[ImxRelation] = field(init=False)

    def __post_init__(self):
        self.puic = self.imx_object.puic
        try:
            self.passage_refs = [_ for _ in self.imx_object.reffed_objects.objects if _.type in ["passageRefs", "PassageRefs"]]
        except Exception as e:
            print(e)


@dataclass
class ImxMicroNodeJumper:
    _element: Element
    from_idx: str = field(init=False)
    to_idx: str = field(init=False)
    is_traversible: bool = field(init=False)
    is_two_way: bool = field(init=False)
    passage_refs: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.from_idx = self._element.attrib.get("fromIndex")
        self.to_idx = self._element.attrib.get("toIndex")
        self.is_traversible = parse_to_bool_if_unknown_true(self._element.attrib.get("isTraversible"))
        self.is_two_way = parse_to_bool_if_unknown_true(self._element.attrib.get("isTwoWay"))

        # todo: make explicit check what to use
        try:
            self.passage_refs = self._element.attrib.get("passageRefs").split(" ")
        except Exception as e:
            try:
                self.passage_refs = self._element.find(".//{*}PassageRefs").text.split(" ")
            except Exception as e_2:
                print(e, e_2)


@dataclass
class ImxMicroNode:
    _imx_obj: ImxObjectProtocol
    puic: str = field(init=False)
    junctionRef: str = field(init=False)
    jumpers: List[ImxMicroNodeJumper] = field(default_factory=list)

    def __post_init__(self):
        self.puic = self._imx_obj.puic
        self.junctionRef = self._imx_obj.puic.split("_")[0]
        self.jumpers = [ImxMicroNodeJumper(_) for _ in self._imx_obj.element.findall(".//{http://www.prorail.nl/IMSpoor}Jumper")]


@dataclass
class ImxMicroLinkFromOrToNode:
    _element: Element
    ref: str = field(init=False)
    idx: int = field(init=False)
    micro_node: ImxMicroNode | None = None
    tag: str = field(init=False)

    def __post_init__(self):
        self.ref = self._element.attrib.get("nodeRef")
        self.idx = self._element.attrib.get("portIndex")
        self.tag = self._element.tag.split("}")[1]


@dataclass
class ImxMicroLink:
    _imx_obj: ImxObjectProtocol
    from_node: ImxMicroLinkFromOrToNode = field(init=False)
    to_node: ImxMicroLinkFromOrToNode = field(init=False)
    _rail_connection: ImxObjectProtocol = field(init=False)
    puic: str = field(init=False)
    track_ref: str = field(init=False)
    passage_refs: List[str] = field(init=False)

    def __post_init__(self):
        self.puic = self._imx_obj.puic.split("_")[0]
        self.from_node = ImxMicroLinkFromOrToNode(self._imx_obj.element.find(".//{http://www.prorail.nl/IMSpoor}FromMicroNode"))
        self.to_node = ImxMicroLinkFromOrToNode(self._imx_obj.element.find(".//{http://www.prorail.nl/IMSpoor}ToMicroNode"))
        self._rail_connection = self._imx_obj.reffed_objects.objects[0].reffed_object
        if self._rail_connection is not None:
            self.track_ref = self._rail_connection.properties["@trackRef"] if "@trackRef" in self._rail_connection.properties.keys() else ""
            self.passage_refs = [_.key for _ in self._rail_connection.reffed_objects.objects if _.type in ["passageRefs", "PassageRefs"]]
        else:
            logger.critical(f"MicroLink {self.puic} object does not have a railConnection counterpart, the app will crash: fix issue and try again!")
            self.track_ref = ""
            self.passage_refs = []

    def link_micro_nodes(self, micro_nodes: dict[str, ImxMicroNode]):
        self.from_node.micro_node = micro_nodes[self.from_node.ref]
        self.to_node.micro_node = micro_nodes[self.to_node.ref]

    def get_centroid_as_xy(self) -> tuple[float, float]:
        x = self._rail_connection.shapely.centroid.x
        y = self._rail_connection.shapely.centroid.y
        return x, y

    def get_shapely(self):
        return self._rail_connection.shapely


class DirectionEnum(Enum):
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"
    UNKNOWN = "unknown"


@dataclass
class GraphMicroLink:
    imx_micro_link: ImxMicroLink
    from_direction: DirectionEnum
    to_direction: DirectionEnum
    junction: ImxMicroNode
    graph_junction: ImxGraphJunction
    jumper: ImxMicroNodeJumper


class Repo:
    @staticmethod
    def _check_and_return(list_of_things: List[T]) -> T:
        if len(list_of_things) == 1:
            return list_of_things[0]
        if len(list_of_things) > 1:
            raise ValueError("Multiple instances found in repo")
        raise ValueError("Not Found")


@dataclass
class RailConnectionRepo(Repo):
    rail_connections: List[ImxRailConnection] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> ImxRailConnection:
        _ = [item for item in self.rail_connections if item.puic == puic]
        return self._check_and_return(_)


@dataclass
class MicroNodeRepo(Repo):
    micro_nodes: List[ImxMicroNode] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> ImxMicroNode:
        _ = [item for item in self.micro_nodes if item.junctionRef == puic]
        return self._check_and_return(_)


@dataclass
class MicroLinkRepo(Repo):
    micro_links: List[ImxMicroLink] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> ImxMicroLink:
        _ = [item for item in self.micro_links if item.puic == puic]
        return self._check_and_return(_)


class MicroLinkConnectionTypeEnum(Enum):
    POINT = "point"
    LINE_START = "line_start"
    LINE_END = "line_end"


@dataclass
class MicroLinkConnection:
    measure: float
    ref: str
    direction: str
    connection_type: MicroLinkConnectionTypeEnum
    item: any  # Assuming 'item' can be of any type for now

    @staticmethod
    def create_from_rail_info(rail_con_info, imx_object):
        """Creates MicroLinkConnection instances from rail connection information.

        Args:
            rail_con_info: The rail connection information object.
            imx_object: The IMX object associated with the rail connection.

        Returns:
            List[MicroLinkConnection]: A list containing one or more MicroLinkConnection instances.
        """
        connections = []
        if hasattr(rail_con_info, "at_measure"):
            # Handle point-type rail connections.
            connections.append(
                MicroLinkConnection(
                    rail_con_info.at_measure, rail_con_info.ref, rail_con_info.direction, MicroLinkConnectionTypeEnum.POINT, imx_object
                )
            )
        else:
            # Handle line-type rail connections, assuming they have 'from_measure' and 'to_measure'.
            # todo: check if present, else give error warning.
            if not hasattr(rail_con_info, "from_measure") or not hasattr(rail_con_info, "to_measure"):
                pass
            else:
                connections.extend(
                    [
                        MicroLinkConnection(
                            rail_con_info.from_measure,
                            rail_con_info.ref,
                            rail_con_info.direction,
                            MicroLinkConnectionTypeEnum.LINE_START,
                            imx_object,
                        ),
                        MicroLinkConnection(
                            rail_con_info.to_measure,
                            rail_con_info.ref,
                            rail_con_info.direction,
                            MicroLinkConnectionTypeEnum.LINE_END,
                            imx_object,
                        ),
                    ]
                )
        return connections


@dataclass
class MicroLinkConnectionRepo:
    micro_links: Dict[str, list[MicroLinkConnection]] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> List[MicroLinkConnection]:
        return self.micro_links[puic]

    def get_keys(self):
        return [_ for _ in self.micro_links.keys()]


@dataclass
class PathEdgeData:
    source_direction: DirectionEnum
    target_direction: DirectionEnum
    junction_ref: str
    graph_junction: ImxGraphJunction
    jumper: ImxMicroNodeJumper

    def as_string(self):
        return f"source: {self.source_direction}, target:{self.target_direction} true_node:{self.junction_ref}"


@dataclass
class PathEdge:
    source: str
    target: str
    data: Optional[PathEdgeData] = None

    @property
    def edge_geometry(self) -> LineString:
        return self.data.graph_junction.get_path(self.data.jumper.passage_refs).geometry

    @property
    def switches_on_edge(self) -> list[ImxGraphSwitchPosition]:
        return self.data.graph_junction.get_path(self.data.jumper.passage_refs).switches_in_path


@dataclass
class PathEdgeSwitchMechanismDisplay:
    ref: str
    name: str
    geometry: Point
    position: str
    path_geometry: LineString


@dataclass
class GraphRoute:
    path: List[PathEdge] = field(default_factory=list)
    geometry: LineString = None
    objects_on_route: List[Any] = field(default_factory=list)
    # todo: get switches in route by pathEdges
    #  switches_on_route: List[Any] = field(default_factory=list)

    @property
    def switches_on_route(self) -> list[PathEdgeSwitchMechanismDisplay]:
        output = []
        for path_edge in self.path:
            for switch_on_edge in path_edge.switches_on_edge:
                output.append(
                    PathEdgeSwitchMechanismDisplay(
                        switch_on_edge.switch_mechanism.puic,
                        switch_on_edge.switch_mechanism.name,
                        switch_on_edge.switch_mechanism.geometry_reprojected,
                        switch_on_edge.position.value,
                        path_edge.edge_geometry,
                    )
                )

        return output

    @property
    def lr_string(self) -> str:
        return "-".join([f"{_.name}_{_.position[0].upper()}" for _ in self.switches_on_route])

    def as_shapely(self) -> LineString:
        return self.geometry

    def as_feature_collection(self):
        route_feature = GeoJsonFeature([ShapelyTransform.rd_to_wgs(self.geometry)], {"path": self.lr_string, "stroke-width": 20.0, "color": "yellow"})

        switch_jumper_features = [
            GeoJsonFeature(
                [ShapelyTransform.rd_to_wgs(item.path_geometry)],
                {"switch_name": item.name, "position": item.position, "stroke-width": 25.0, "color": "orange"},
            )
            for item in self.switches_on_route
        ]

        switch_mech_features = [
            GeoJsonFeature(
                [ShapelyTransform.rd_to_wgs(item.geometry)], {"switch_name": item.name, "position": item.position, "imx_type": "SwitchMechanism"}
            )
            for item in self.switches_on_route
        ]

        # 	"featureTags": ["tag"]
        # 	an array of string tags that are used for hierarchical filtering;
        # 	featureTags values can have a pipe (|) inside thus making groups on different levels;
        # 	for example, "group_1|group_2|group_3" will result in a three-level deep tree.

        # # todo: make sure it's only in direction of travel or none
        features = [
            GeoJsonFeature([ShapelyTransform.rd_to_wgs(item.item.shapely)], item.item.properties | {"imx_type": item.item.path})
            for item in self.objects_on_route
        ]

        # features = []
        features.extend(switch_jumper_features)
        features.extend(switch_mech_features)
        features.append(route_feature)
        return GeoJsonFeatureCollection(features)
