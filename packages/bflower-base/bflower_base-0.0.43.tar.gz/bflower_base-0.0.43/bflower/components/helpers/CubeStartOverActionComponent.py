import json
import nats

# from bflower.schema import Record
from bflower.interface.custom.custom_component import CustomComponent


class CubeStartOverActionComponent(CustomComponent):
    display_name = "Cube StartOver Action Component"
    description = "START_OVER_CUBE"
    documentation: str = "http://docs.bflower.org/components/custom"
    icon = "custom_components"

    def build_config(self):
        return {
            "workflowId": {
                "display_name": "Workflow ID",
                "info": "Input text to pass to the agent.",
            },
        }

    async def build(self, workflowId: str) -> str:
        nc = await nats.connect("nats://192.168.2.115:4222")
        js = nc.jetstream()
        action = {
            "workflowId": workflowId,
            "event": {"type": "START_OVER_CUBE", "id": workflowId},
        }
        res = await js.publish(f"machines.{workflowId}.action", json.dumps(action).encode("utf-8"))
        print(f"Published [{res}] : '{action}'")
        # Terminate connection to NATS.
        await nc.drain()
        return workflowId
