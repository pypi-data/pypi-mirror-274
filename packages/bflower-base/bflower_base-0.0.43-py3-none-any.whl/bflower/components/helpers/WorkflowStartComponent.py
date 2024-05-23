import json
import nats

# from bflower.schema import Record
from bflower.interface.custom.custom_component import CustomComponent


class WorkflowStartComponent(CustomComponent):
    display_name = "WorkflowStartComponent"
    description = "It's start a workflow with given workflowId."
    documentation: str = "http://docs.bflower.org/components/custom"
    icon = "custom_components"

    def build_config(self):
        return {
            "workflowId": {
                "display_name": "Workflow ID",
                "info": "Input text to pass to the agent.",
            },
            "machineType": {
                "display_name": "Machine Type",
                "advanced": False,
                "options": [
                    "cubeMachine",
                    "userDataMachine",
                    "counterMachine",
                    "openAiJokeMachine",
                    "mistralAiJokeMachine",
                    "openAiFriendJokeMachine",
                    "mistralAiFriendRatingMachine",
                ],
            },
        }

    async def build(self, workflowId: str, machineType: str = "cubeMachine") -> str:
        nc = await nats.connect("nats://192.168.2.115:4222")
        js = nc.jetstream()
        action = {
            "type": "WORKFLOWS_START",
            "workflowId": workflowId,
            "temporalTaskQueue": "taskQueue3",
            "machineType": machineType,
        }
        res = await js.publish("workflows.start", json.dumps(action).encode("utf-8"))
        print(f"Published [{res}] : '{action}'")
        # Terminate connection to NATS.
        await nc.drain()
        return workflowId
