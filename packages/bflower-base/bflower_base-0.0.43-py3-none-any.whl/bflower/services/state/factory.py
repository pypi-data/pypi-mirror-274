from bflower.services.factory import ServiceFactory
from bflower.services.settings.service import SettingsService
from bflower.services.state.service import InMemoryStateService


class StateServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(InMemoryStateService)

    def create(self, settings_service: SettingsService):
        return InMemoryStateService(
            settings_service,
        )
