from typing import Protocol

from imxInsights.domain.models.imxEnums import AreaNameEnum
from imxInsights.repo.tree.objectTree import ImxObject


class ImxSituationRepoMinimalProtocol(Protocol):
    # fmt: off
    def get_by_types(self, object_types: list[str]) -> list[ImxObject]: ...  # noqa E704

    def get_by_puic(self, puic: str) -> ImxObject | None: ...  # noqa E704


    def get_all(self, areas: list[AreaNameEnum] | None) -> list[ImxObject]: ...  # noqa E704
    # fmt: on
