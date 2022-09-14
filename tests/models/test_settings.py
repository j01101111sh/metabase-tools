from metabase_tools import MetabaseApi
from metabase_tools.server_settings import ServerSettings, Setting


def test_update_admin_email(api: MetabaseApi):
    result = api.settings.admin_email.update("jim.test@dundermifflin.com")
    assert result["success"] is True
    assert isinstance(api.settings, ServerSettings)
    assert isinstance(api.settings.admin_email, Setting)