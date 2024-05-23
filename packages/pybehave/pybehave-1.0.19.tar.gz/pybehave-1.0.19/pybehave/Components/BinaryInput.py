from __future__ import annotations
from typing import TYPE_CHECKING

from pybehave.Components.Input import Input

if TYPE_CHECKING:
    from pybehave.Tasks.Task import Task

from pybehave.Components.Component import Component


class BinaryInput(Input):

    def __init__(self, task: Task, component_id: str, component_address: str):
        super().__init__(task, component_id, component_address)
        self.state = False

    @staticmethod
    def get_type() -> Component.Type:
        return Component.Type.DIGITAL_INPUT
