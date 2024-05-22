import asyncio

from arcGisFeatureCash import ArcGisFeatureService
from shapely import Point


async def get_feature_service_km_async():
    url = "https://mapservices.prorail.nl/arcgis/rest/services/Referentiesysteem_004/FeatureServer"
    return await ArcGisFeatureService.factory(url)


async def get_feature_service_tekeningen_async():
    url = "https://maps.prorail.nl/arcgis/rest/services/Tekeningen_schematisch/FeatureServer"
    return await ArcGisFeatureService.factory(url)


async def get_all_gis_features_async():
    # todo: make jobs list and await that one to gain some speed
    km_features = await get_feature_service_km_async()
    tekening_features = await get_feature_service_tekeningen_async()
    return km_features, tekening_features


class GisRailDataLayer:
    def __init__(self, feature_cash_km, feature_cash_schema_tek):
        self._feature_cash_km: ArcGisFeatureService = feature_cash_km
        self._feature_cash_schema_tek: ArcGisFeatureService = feature_cash_schema_tek

        self.km_vlak = [_ for _ in self._feature_cash_km.feature_service_layers if _.dataset == "Kilometerlintvlak"][0]
        self.km_lint = [_ for _ in self._feature_cash_km.feature_service_layers if _.dataset == "Kilometerlint"][0]
        self.OBE_contour = [_ for _ in self._feature_cash_schema_tek.feature_service_layers if _.dataset == "OBE blad"][0]

    def get_km_linear_referencing(self, x: float, y: float) -> str:
        def round_floor_to_3_decimals(num):
            return (num * 1000) // 1 / 1000.0

        point = Point(x, y)
        vlak_matches = [item for item in self.km_vlak.features if point.within(item.geometry)]
        response = []
        for item in vlak_matches:
            lint_name = item.attributes.get_value("KMLINT")
            lint_match = [item for item in self.km_lint.features if item.attributes.get_value("NAAM") == lint_name][0]
            projected_point = lint_match.measure_geometry.interpolate(lint_match.measure_geometry.project(point))
            response.append(f"{lint_name}: km {round_floor_to_3_decimals(projected_point.z)}")

        return "".join(response) if len(response) == 1 else "\n".join(response)

    def get_obe_contours(self):
        pass


def get_gis_rail_data_layer() -> GisRailDataLayer:
    km_features, schema_tek_features = asyncio.run(get_all_gis_features_async())
    return GisRailDataLayer(km_features, schema_tek_features)
