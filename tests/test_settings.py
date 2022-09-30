import pytest

from metabase_tools import MetabaseApi
from metabase_tools.models import ServerSettings, Setting


class TestSettingsPass:
    def test_update_site_name(self, api: MetabaseApi):
        new_site_name = "testing-site-test"
        result = api.settings.site_name.update(new_site_name)
        assert result["success"] is True
        assert isinstance(api.settings, ServerSettings)
        assert isinstance(api.settings.site_name, Setting)
        assert api.settings.site_name.value == new_site_name


class TestSettingsFail:
    def test_update_wrong_type(self, api: MetabaseApi):
        with pytest.raises(TypeError):
            _ = api.settings.site_name.update(4)
