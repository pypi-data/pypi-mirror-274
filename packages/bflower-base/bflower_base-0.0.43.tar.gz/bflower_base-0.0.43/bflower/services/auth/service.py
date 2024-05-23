from typing import TYPE_CHECKING

from bflower.services.base import Service

if TYPE_CHECKING:
    from bflower.services.settings.service import SettingsService


class AuthService(Service):
    name = "auth_service"

    def __init__(self, settings_service: "SettingsService"):
        self.settings_service = settings_service
