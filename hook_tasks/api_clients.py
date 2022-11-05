from figure_hook_client.client import AuthenticatedClient
from plurk_oauth import PlurkAPI

from hook_tasks.configs import HookApiSettings, PlurkApiSettings

hook_api_settings = HookApiSettings()  # type: ignore
hook_api_client = AuthenticatedClient(
    base_url=hook_api_settings.URL,
    token=hook_api_settings.TOKEN,
    prefix="",
    auth_header_name="x-api-token",
)  # type: ignore


plurk_api_settings = PlurkApiSettings()  # type: ignore
plurk_api = PlurkAPI(
    key=plurk_api_settings.app_key,
    secret=plurk_api_settings.app_secret,
    access_token=plurk_api_settings.access_token,
    access_secret=plurk_api_settings.access_token_secret,
)
