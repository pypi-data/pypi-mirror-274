from typing import Protocol, TypeVar

from imxInsights.graph.imxGraphModels import GraphRoute
from imxInsights.graph.imxGraphSituationProtocol import ImxSituationRepoMinimalProtocol

T = TypeVar("T")


class ImxGraphProtocol(Protocol):
    # fmt: off
    @property
    def imx_situation(self) -> ImxSituationRepoMinimalProtocol: ...  # noqa E704

    def get_paths_between_imx_objects(self, from_object: T, to_object: T) -> list[GraphRoute]: ...  # noqa E704
    # fmt: on
