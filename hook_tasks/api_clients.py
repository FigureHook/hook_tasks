from figure_hook_client.client import AuthenticatedClient

from hook_tasks.configs import HookApiSettings

hook_api_settings = HookApiSettings()  # type: ignore
hook_api_client = AuthenticatedClient(
    base_url=hook_api_settings.URL,
    token=hook_api_settings.TOKEN,
    prefix="",
    auth_header_name="x-api-token",
)  # type: ignore
