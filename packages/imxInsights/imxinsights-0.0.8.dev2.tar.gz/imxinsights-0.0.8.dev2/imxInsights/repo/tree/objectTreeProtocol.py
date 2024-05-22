from typing import Iterable, List, Optional, Protocol

from lxml import etree as ET
from shapely.geometry.base import BaseGeometry

from imxInsights.domain.area.areaClassifiedTypeEnum import AreaClassifiedTypeEnum
from imxInsights.domain.area.imxProjectArea import ImxProjectArea
from imxInsights.domain.models.imxGeometry import ImxGeometry
from imxInsights.domain.models.imxMetadata import ImxObjectMetadata
from imxInsights.domain.models.ImxRailConnectionInfo import RailConnectionInfos
from imxInsights.domain.models.imxRelation import ImxReffedObjects
from imxInsights.repo.tree.imxTopoTreeObject import ImxTopoObject


class ImxObjectProtocol(Protocol):
    @property
    def properties(self) -> dict[str, str]:
        raise NotImplementedError

    @property
    def metadata(self) -> ImxObjectMetadata:
        raise NotImplementedError

    @property
    def geometry(self) -> Optional[ImxGeometry]:
        raise NotImplementedError

    @property
    def rail_connection_infos(self) -> Optional[RailConnectionInfos]:
        raise NotImplementedError

    @property
    def track_fragments(self) -> Optional[RailConnectionInfos]:
        raise NotImplementedError

    @property
    def demarcation_markers(self) -> Optional[RailConnectionInfos]:
        raise NotImplementedError

    @property
    def reffed_objects(self) -> ImxReffedObjects:
        raise NotImplementedError

    @property
    def topo_object(self) -> Optional[ImxTopoObject]:
        raise NotImplementedError

    @property
    def area(self) -> Optional[ImxProjectArea]:
        raise NotImplementedError

    @property
    def area_classify_type(self) -> Optional[AreaClassifiedTypeEnum]:
        raise NotImplementedError

    @property
    def parent(self) -> Optional["ImxObjectProtocol"]:
        raise NotImplementedError

    @property
    def children(self) -> List["ImxObjectProtocol"]:
        raise NotImplementedError

    @property
    def element(self) -> ET.Element:
        raise NotImplementedError

    @property
    def tag(self) -> str:
        raise NotImplementedError

    @property
    def path(self) -> str:
        raise NotImplementedError

    @property
    def puic(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def shapely(self) -> BaseGeometry:
        raise NotImplementedError

    # fmt: off
    def _parents_generator(self) -> Iterable["ImxObjectProtocol"]: ...  # noqa E704

    def register_topo_object(self, topo_object: ImxTopoObject): ...  # noqa E704

    def can_compare(self, other: Optional["ImxObjectProtocol"]) -> bool: ...  # noqa E704

    @staticmethod
    def lookup_tree_from_root_element(start: ET.Element) -> list["ImxObjectProtocol"]: ...  # noqa E704
    # fmt: on
