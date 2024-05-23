import json
import nats

# from bflower.schema import Record
from bflower.interface.custom.custom_component import CustomComponent


class CubeChangeColorActionComponent(CustomComponent):
    display_name = "Cube ChangeColor Action Component"
    description = "CHANGE_CUBE_COLOR"
    documentation: str = "http://docs.bflower.org/components/custom"
    icon = "custom_components"

    def build_config(self):
        return {
            "workflowId": {
                "display_name": "Workflow ID",
                "info": "Input text to pass to the agent.",
            },
            "color": {
                "display_name": "Color",
            },
        }

    async def build(self, workflowId: str, color: str) -> str:
        nc = await nats.connect("nats://192.168.2.115:4222")
        js = nc.jetstream()
        action = {
            "workflowId": workflowId,
            "event": {"type": "CHANGE_CUBE_COLOR", "color": color, "id": workflowId},
        }
        res = await js.publish(f"machines.{workflowId}.action", json.dumps(action).encode("utf-8"))
        print(f"Published [{res}] : '{action}'")
        # Terminate connection to NATS.
        await nc.drain()
        return workflowId
