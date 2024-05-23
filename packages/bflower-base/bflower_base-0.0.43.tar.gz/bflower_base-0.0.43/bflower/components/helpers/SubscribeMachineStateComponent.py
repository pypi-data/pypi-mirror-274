import json
import time
import nats
from bflower.field_typing import Text
# from typing import TypedDict

# from bflower.schema import Record
from bflower.interface.custom.custom_component import CustomComponent

# class NatsMessageResponse(TypedDict):
#   workflowId: str
#   oldStateValue: str
#   newStateValue: str


class SubscribeMachineStateComponent(CustomComponent):
    display_name = "Subscribe Machine State Component"
    description = "I's subscibe to the target state of the machine."
    documentation: str = "http://docs.bflower.org/components/custom"
    icon = "custom_components"

    async def runMyCode(self, targetState: str, workflowId: str) -> Text:
        nc = await nats.connect("nats://192.168.2.115:4222")
        js = nc.jetstream()
        sub = await js.subscribe(f"machines.{workflowId}.stateChanged")
        msg = await sub.next_msg(50)
        await msg.ack()
        print(targetState)
        response = json.loads(msg.data.decode())
        print(f"Received: {response['newStateValue']}")
        # Terminate connection to NATS.
        await nc.drain()
        return response

    def build_config(self):
        return {
            "workflowId": {
                "display_name": "Workflow ID",
                "info": "Input text to pass to the agent.",
            },
            "targetState": {
                "display_name": "Target State",
            },
        }

    async def build(self, workflowId: str, targetState: str) -> str:
        # nc = await nats.connect("nats://192.168.2.115:4222")
        # js = nc.jetstream()
        # sub = await js.subscribe(f"machines.{workflowId}.stateChanged")
        # msg = await sub.next_msg()
        # await msg.ack()
        s = time.perf_counter()
        # asyncio.run(self.runMyCode(targetState, workflowId))
        res = await self.runMyCode(targetState, workflowId)
        elapsed = time.perf_counter() - s
        print(f"executed in {elapsed:0.2f} seconds.")
        # print(f"Received: {msg.data.decode()}")
        # Terminate connection to NATS.
        # await nc.drain()
        return res
