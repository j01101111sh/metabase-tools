from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, Field, PrivateAttr

from metabase_tools.exceptions import MetabaseApiException

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi


def replace_hyphens(s: str) -> str:
    return s.replace("_", "-")


class Setting(BaseModel):
    """Individual setting on the server"""

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    key: str
    value: Optional[Any]
    is_env_setting: bool
    env_name: str
    description: str
    default: Optional[Any]

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        self._adapter = adapter

    def update(self, new_value: Any) -> dict[str, Any]:
        if not self._value_type_compatible(new_value):
            raise TypeError
        if self._adapter:
            result = self._adapter.put(
                endpoint=f"/setting/{self.key}", params={"value": new_value}
            )
            if isinstance(result, dict):
                return result
        raise MetabaseApiException

    def _value_type_compatible(self, new_value: Any) -> bool:
        if self.value is None or new_value is None:
            return True
        if isinstance(new_value, type(self.value)):
            return True
        return False


class ServerSettings(BaseModel):
    """Settings for a Metabase server"""

    _adapter: MetabaseApi = PrivateAttr(None)

    admin_email: Setting
    anon_tracking_enabled: Setting
    application_colors: Setting
    application_favicon_url: Setting
    application_logo_url: Setting
    application_name: Setting
    available_locales: Setting
    available_timezones: Setting
    breakout_bin_width: Setting
    breakout_bins_num: Setting
    check_for_updates: Setting
    custom_formatting: Setting
    custom_geojson: Setting
    email_configured: Setting = Field(..., alias="email-configured?")
    email_from_address: Setting
    email_smtp_host: Setting
    email_smtp_password: Setting
    email_smtp_port: Setting
    email_smtp_security: Setting
    email_smtp_username: Setting
    embedding_app_origin: Setting
    embedding_secret_key: Setting
    enable_audit_app: Setting = Field(..., alias="enable-audit-app?")
    enable_embedding: Setting
    enable_enhancements: Setting = Field(..., alias="enable-enhancements?")
    enable_nested_queries: Setting
    enable_password_login: Setting
    enable_public_sharing: Setting
    enable_query_caching: Setting
    enable_sandboxes: Setting = Field(..., alias="enable-sandboxes?")
    enable_sso: Setting = Field(..., alias="enable-sso?")
    enable_whitelabeling: Setting = Field(..., alias="enable-whitelabeling?")
    enable_xrays: Setting
    engines: Setting
    field_filter_operators_enabled: Setting = Field(
        ..., alias="field-filter-operators-enabled?"
    )
    ga_code: Setting
    google_auth_auto_create_accounts_domain: Setting
    google_auth_client_id: Setting
    has_sample_dataset: Setting = Field(..., alias="has-sample-dataset?")
    hide_embed_branding: Setting = Field(..., alias="hide-embed-branding?")
    humanization_strategy: Setting
    landing_page: Setting
    ldap_attribute_email: Setting
    ldap_attribute_firstname: Setting
    ldap_attribute_lastname: Setting
    ldap_bind_dn: Setting
    ldap_configured: Setting = Field(..., alias="ldap-configured?")
    ldap_enabled: Setting
    ldap_group_base: Setting
    ldap_group_mappings: Setting
    ldap_group_sync: Setting
    ldap_host: Setting
    ldap_password: Setting
    ldap_port: Setting
    ldap_security: Setting
    ldap_user_base: Setting
    ldap_user_filter: Setting
    map_tile_server_url: Setting
    metabot_enabled: Setting
    password_complexity: Setting
    premium_embedding_token: Setting
    premium_features: Setting
    query_caching_max_kb: Setting
    query_caching_max_ttl: Setting
    query_caching_min_ttl: Setting
    query_caching_ttl_ratio: Setting
    redirect_all_requests_to_https: Setting
    redshift_fetch_size: Setting
    report_timezone: Setting
    report_timezone_short: Setting
    search_typeahead_enabled: Setting
    setup_token: Setting
    show_homepage_data: Setting
    show_homepage_xrays: Setting
    site_locale: Setting
    site_name: Setting
    site_url: Setting
    slack_token: Setting
    source_address_header: Setting
    ssh_heartbeat_interval_sec: Setting
    ssl_certificate_public_key: Setting
    start_of_week: Setting
    version: Setting
    version_info: Setting
    version_info_last_checked: Setting

    class Config:
        alias_generator = replace_hyphens
        extra = "ignore"

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        self._adapter = adapter

        self.admin_email.set_adapter(self._adapter)
        self.anon_tracking_enabled.set_adapter(self._adapter)
        # application_colors.set_adapter(self._adapter)
        # application_favicon_url.set_adapter(self._adapter)
        # application_logo_url.set_adapter(self._adapter)
        # application_name.set_adapter(self._adapter)
        # available_locales.set_adapter(self._adapter)
        # available_timezones.set_adapter(self._adapter)
        # breakout_bin_width.set_adapter(self._adapter)
        # breakout_bins_num.set_adapter(self._adapter)
        # check_for_updates.set_adapter(self._adapter)
        # custom_formatting.set_adapter(self._adapter)
        # custom_geojson.set_adapter(self._adapter)
        # email_configured.set_adapter(self._adapter)
        # email_from_address.set_adapter(self._adapter)
        # email_smtp_host.set_adapter(self._adapter)
        # email_smtp_password.set_adapter(self._adapter)
        # email_smtp_port.set_adapter(self._adapter)
        # email_smtp_security.set_adapter(self._adapter)
        # email_smtp_username.set_adapter(self._adapter)
        # embedding_app_origin.set_adapter(self._adapter)
        # embedding_secret_key.set_adapter(self._adapter)
        # enable_audit_app.set_adapter(self._adapter)
        # enable_embedding.set_adapter(self._adapter)
        # enable_enhancements.set_adapter(self._adapter)
        # enable_nested_queries.set_adapter(self._adapter)
        # enable_password_login.set_adapter(self._adapter)
        # enable_public_sharing.set_adapter(self._adapter)
        # enable_query_caching.set_adapter(self._adapter)
        # enable_sandboxes.set_adapter(self._adapter)
        # enable_sso.set_adapter(self._adapter)
        # enable_whitelabeling.set_adapter(self._adapter)
        # enable_xrays.set_adapter(self._adapter)
        # engines.set_adapter(self._adapter)
        # field_filter_operators_enabled.set_adapter(self._adapter)
        # ga_code.set_adapter(self._adapter)
        # google_auth_auto_create_accounts_domain.set_adapter(self._adapter)
        # google_auth_client_id.set_adapter(self._adapter)
        # has_sample_dataset.set_adapter(self._adapter)
        # hide_embed_branding.set_adapter(self._adapter)
        # humanization_strategy.set_adapter(self._adapter)
        # landing_page.set_adapter(self._adapter)
        # ldap_attribute_email.set_adapter(self._adapter)
        # ldap_attribute_firstname.set_adapter(self._adapter)
        # ldap_attribute_lastname.set_adapter(self._adapter)
        # ldap_bind_dn.set_adapter(self._adapter)
        # ldap_configured.set_adapter(self._adapter)
        # ldap_enabled.set_adapter(self._adapter)
        # ldap_group_base.set_adapter(self._adapter)
        # ldap_group_mappings.set_adapter(self._adapter)
        # ldap_group_sync.set_adapter(self._adapter)
        # ldap_host.set_adapter(self._adapter)
        # ldap_password.set_adapter(self._adapter)
        # ldap_port.set_adapter(self._adapter)
        # ldap_security.set_adapter(self._adapter)
        # ldap_user_base.set_adapter(self._adapter)
        # ldap_user_filter.set_adapter(self._adapter)
        # map_tile_server_url.set_adapter(self._adapter)
        # metabot_enabled.set_adapter(self._adapter)
        # password_complexity.set_adapter(self._adapter)
        # premium_embedding_token.set_adapter(self._adapter)
        # premium_features.set_adapter(self._adapter)
        # query_caching_max_kb.set_adapter(self._adapter)
        # query_caching_max_ttl.set_adapter(self._adapter)
        # query_caching_min_ttl.set_adapter(self._adapter)
        # query_caching_ttl_ratio.set_adapter(self._adapter)
        # redirect_all_requests_to_https.set_adapter(self._adapter)
        # redshift_fetch_size.set_adapter(self._adapter)
        # report_timezone.set_adapter(self._adapter)
        # report_timezone_short.set_adapter(self._adapter)
        # search_typeahead_enabled.set_adapter(self._adapter)
        # setup_token.set_adapter(self._adapter)
        # show_homepage_data.set_adapter(self._adapter)
        # show_homepage_xrays.set_adapter(self._adapter)
        # site_locale.set_adapter(self._adapter)
        # site_name.set_adapter(self._adapter)
        # site_url.set_adapter(self._adapter)
        # slack_token.set_adapter(self._adapter)
        # source_address_header.set_adapter(self._adapter)
        # ssh_heartbeat_interval_sec.set_adapter(self._adapter)
        # ssl_certificate_public_key.set_adapter(self._adapter)
        # start_of_week.set_adapter(self._adapter)
        # version.set_adapter(self._adapter)
        # version_info.set_adapter(self._adapter)
        # version_info_last_checked.set_adapter(self._adapter)
