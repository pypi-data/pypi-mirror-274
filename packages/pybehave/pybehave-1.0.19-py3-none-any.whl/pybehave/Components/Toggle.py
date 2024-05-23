from __future__ import annotations
from typing import TYPE_CHECKING

from pybehave.Components.Output import Output

if TYPE_CHECKING:
    from pybehave.Tasks.Task import Task

from pybehave.Components.Component import Component


class Toggle(Output):
    """
        Class defining a Toggle component in the operant chamber.

        Parameters
        ----------
        source : Source
            The Source related to this Component
        component_id : str
            The ID of this Component
        component_address : str
            The location of this Component for its Source
        metadata : str
            String containing any metadata associated with this Component

        Attributes
        ----------
        state : boolean
            Boolean indicating if the Component is currently toggled

        Methods
        -------
        get_state()
            Returns state
        toggle(on)
            Sets the Toggle state with the Source
        get_type()
            Returns Component.Type.DIGITAL_OUTPUT
    """

    def __init__(self, task: Task, component_id: str, component_address: str):
        super().__init__(task, component_id, component_address)
        self.state = False

    def toggle(self, on: bool) -> None:
        if on != self.state:
            self.write(on)
            self.state = on

    @staticmethod
    def get_type() -> Component.Type:
        return Component.Type.DIGITAL_OUTPUT
