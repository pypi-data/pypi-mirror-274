from ursactl.core._base import Base
from ursactl.core.services import client

from .running_agent import RunningAgent


class AgentSwarm(Base):
    """
    Provides access to agent swarms.
    """

    @property
    def client(self):
        if self._client is None:
            self._client = client("planning", self.app)
        return self._client

    @property
    def name(self):
        return self._data["name"]

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {"name": None, "project_uuid": None}
            else:
                self._cached_data = self.client.get_agent_swarm(self.uuid)
        return self._cached_data

    def send_event(self, domain, name, params, group=None):
        result = self.client.send_event_to_agent_swarm(
            self.uuid,
            {"domain": domain, "name": name, "params": params, "group": group},
        )
        return result["result"]

    def send_events(self, events):
        actions = []
        for event in events:
            result = self.client.send_event_to_agent_swarm(self.uuid, event)
            if result["result"]:
                actions.extend(result["result"])
        return actions

    def add_agents(self, agent_name, configs, groups=[]):
        result = self.client.run_agents_in_swarm(self.uuid, agent_name, configs, groups)
        if result["errors"]:
            return None
        return [
            RunningAgent(
                uuid=running_agent_id,
                app=self.app,
                client=self.client,
                project=self.project,
            )
            for running_agent_id in result["result"]
        ]

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.client.delete_agent_swarm(self.uuid)

    @classmethod
    def create_anonymous(klass, project=None, app=None, **_kwargs):
        c = client("planning", app)
        swarm = c.create_agent_swarm(project_uuid=project.uuid)
        return klass(uuid=swarm["result"]["id"], project=project, app=app, client=c)
