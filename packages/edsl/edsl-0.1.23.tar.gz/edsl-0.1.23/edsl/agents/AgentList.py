"""A list of Agent objects.

Example usage:

.. code-block:: python

    al = AgentList([Agent.example(), Agent.example()])
    len(al)
    2
    
"""
from __future__ import annotations
from collections import UserList
from typing import Optional, Union
from rich import print_json
from rich.table import Table
import json

from edsl.Base import Base
from edsl.agents import Agent
from edsl.utilities.decorators import (
    add_edsl_version,
    remove_edsl_version,
)


class AgentList(UserList, Base):
    """A list of Agents."""

    def __init__(self, data: Optional[list[Agent]] = None):
        """Initialize a new AgentList.

        :param data: A list of Agents.
        """
        if data is not None:
            super().__init__(data)
        else:
            super().__init__()

    @add_edsl_version
    def to_dict(self):
        """Return dictionary of AgentList to serialization."""
        return {"agent_list": [agent.to_dict() for agent in self.data]}

    def __repr__(self):
        return f"AgentList({self.data})"

    def print(self, format: Optional[str] = None):
        """Print the AgentList."""
        print_json(json.dumps(self.to_dict()))

    def _repr_html_(self):
        """Return an HTML representation of the AgentList."""
        from edsl.utilities.utilities import data_to_html

        return data_to_html(self.to_dict()["agent_list"])

    @classmethod
    @remove_edsl_version
    def from_dict(cls, data: dict) -> "AgentList":
        """Deserialize the dictionary back to an AgentList object.

        :param: data: A dictionary representing an AgentList.
        """
        agents = [Agent.from_dict(agent_dict) for agent_dict in data["agent_list"]]
        return cls(agents)

    @classmethod
    def example(cls) -> "AgentList":
        """Return an example AgentList."""
        return cls([Agent.example(), Agent.example()])

    def code(self) -> list[str]:
        """Return code to construct an AgentList."""
        lines = [
            "from edsl.agents.Agent import Agent",
            "from edsl.agents.AgentList import AgentList",
        ]
        lines.append(f"agent_list = AgentList({self.data})")
        return lines

    def rich_print(self) -> Table:
        """Display an object as a rich table."""
        table = Table(title="AgentList")
        table.add_column("Agents", style="bold")
        for agent in self.data:
            table.add_row(agent.rich_print())
        return table


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
