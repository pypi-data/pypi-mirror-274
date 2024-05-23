import json
import nats

# from bflower.schema import Record
from bflower.interface.custom.custom_component import CustomComponent


class CubeMoveActionComponent(CustomComponent):
    display_name = "Cube Move Action Component"
    description = "MOVE_CUBE"
    documentation: str = "http://docs.bflower.org/components/custom"
    icon = "custom_components"

    def build_config(self):
        return {
            "workflowId": {
                "display_name": "Workflow ID",
                "info": "Input text to pass to the agent.",
            },
            "x": {
                "display_name": "Position X",
            },
            "y": {
                "display_name": "Position Y",
            },
        }

    async def build(self, workflowId: str, x: int, y: int) -> str:
        nc = await nats.connect("nats://192.168.2.115:4222")
        js = nc.jetstream()
        action = {
            "workflowId": workflowId,
            "event": {"type": "MOVE_CUBE", "position": {"x": x, "y": y}, "id": workflowId},
        }
        res = await js.publish(f"machines.{workflowId}.action", json.dumps(action).encode("utf-8"))
        print(f"Published [{res}] : '{action}'")
        # Terminate connection to NATS.
        await nc.drain()
        return workflowId
