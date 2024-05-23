from typing import Optional
from bflower.field_typing import Text
from bflower.interface.custom.custom_component import CustomComponent


class MyCustomComponent(CustomComponent):
    display_name = "My Burak Custom Component"
    description = "Use as a template to create your own component."
    documentation: str = "http://docs.bflower.org/components/custom"
    icon = "custom_components"

    def build_config(self):
        return {
            "input_value": {
                "display_name": "Value",
                "input_types": ["Record", "Text"],
                "info": "Text or Record to be passed as output.",
            }
        }

    def build(self, input_value: Optional[Text] = "") -> Text:
        return Text(input_value)
