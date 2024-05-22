import asyncio
from dataclasses import dataclass
from typing import List, TypeVar, cast

import nest_asyncio
from loguru import logger
from shapely import LineString
from shapely.ops import linemerge

from imxInsights.graph.queries.imxGraphProtocol import ImxGraphProtocol
from imxInsights.repo.tree.objectTreeProtocol import ImxObjectProtocol
from imxInsights.utils.shapely_geojson import (
    GeoJsonFeature,
    GeoJsonFeatureCollection,
    dump,
)
from imxInsights.utils.shapely_helpers import ShapelyTransform

T = TypeVar("T")

nest_asyncio.apply()


@dataclass
class ImxGraphSectionQueryResult:
    section: ImxObjectProtocol
    geometry: LineString


class SectionGeometryGraphQuery:
    def __init__(self, imx_graph: ImxGraphProtocol):
        self.g: ImxGraphProtocol = imx_graph

    async def _get_section_geometry(self, refs: List[str]) -> LineString:
        refs_mapping = {uuid: [other_uuid for other_uuid in refs if other_uuid != uuid] for uuid in refs}
        line_strings = []

        # todo: make task for every mapping item so we can process them async
        for key, values in refs_mapping.items():
            from_obj = self.g.imx_situation.get_by_puic(key)
            if from_obj is None:
                logger.warning(f"Object {key} not found in situation")
                continue

            # todo: make task for every to item so we can process them async
            for item in values:
                to_obj = self.g.imx_situation.get_by_puic(item)
                if to_obj is None:
                    logger.warning(f"Object {item} not found in situation")
                    continue

                paths = self.g.get_paths_between_imx_objects(from_obj, to_obj)
                for path in paths:
                    line_strings.append(path.geometry)

        return linemerge(line_strings).buffer(0.01)

    async def _get_section_async(self, section: T, ref_type: List[str]) -> ImxGraphSectionQueryResult:
        refs = [_.key for _ in section.reffed_objects.objects if _.type in ref_type]
        line_string = await self._get_section_geometry(refs)
        return ImxGraphSectionQueryResult(section, line_string)

    async def _get_all_sections_async(self, section_type: str, ref_type: List[str]) -> List[ImxGraphSectionQueryResult]:
        sections = self.g.imx_situation.get_by_types([section_type])
        tasks = [self._get_section_async(section, ref_type) for section in sections]
        result = await asyncio.gather(*tasks)
        return cast(List[ImxGraphSectionQueryResult], result)

    def get_section(self, section: T, ref_type: List[str]) -> ImxGraphSectionQueryResult:
        return asyncio.run(self._get_section_async(section, ref_type))

    def get_all_section(self, section_type: str, ref_type: List[str]) -> List[ImxGraphSectionQueryResult]:
        return asyncio.run(self._get_all_sections_async(section_type, ref_type))

    @staticmethod
    def _create_geojson_features(query_results: List[ImxGraphSectionQueryResult]):
        features = []
        for result in query_results:
            features.append(GeoJsonFeature([ShapelyTransform.rd_to_wgs(result.geometry)], result.section.properties | {"type": result.section.tag}))
        return features

    @staticmethod
    def _save_as_geojson(fc, file_name):
        with open(file_name, "w") as file:
            dump(fc, file)

    def create_geojson_files(self):
        try:
            features = self.get_all_section("AxleCounterSection", ["AxleCounterDetectionPointRefs"])
            tester = self._create_geojson_features(features)
            self._save_as_geojson(GeoJsonFeatureCollection(tester), "AxleCounterSection.geojson")

            features = self.get_all_section("TrackCircuit", ["InsulatedJointRefs"])
            tester = self._create_geojson_features(features)
            self._save_as_geojson(GeoJsonFeatureCollection(tester), "TrackCircuit.geojson")

        except RuntimeError as e:
            print(f"Error running async function: {e}")
