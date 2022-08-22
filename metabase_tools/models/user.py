"""User class for user objects from Metabase
"""

from datetime import datetime
from typing import Optional

from pydantic.fields import Field
from typing_extensions import Self

from metabase_tools.exceptions import RequestFailure
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import MetabaseGeneric


class User(MetabaseGeneric):
    """Class for user objects from Metabase"""

    name: str = Field(alias="common_name")
    email: str
    first_name: str
    last_name: str
    date_joined: datetime
    last_login: Optional[datetime]
    updated_at: Optional[datetime]
    is_qbnewb: bool
    is_superuser: bool
    ldap_auth: Optional[bool]
    google_auth: Optional[bool]
    is_active: Optional[bool]
    locale: Optional[str]
    group_ids: Optional[list[int]]
    login_attributes: Optional[list]
    personal_collection_id: Optional[int]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        """Fetch a list of users using the provided MetabaseAPI

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        targets : list[int], optional
            List of targets to fetch. Returns all users if not provided.

        Returns
        -------
        list[Self]
            List of users
        """
        return super(User, cls).get(adapter=adapter, endpoint="/user", targets=targets)

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Create new user(s)

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        payloads : list[dict]
            List of dicts with details for new user(s)

        Returns
        -------
        list[Self]
            List of created users
        """
        return super(User, cls).post(
            adapter=adapter, endpoint="/user", payloads=payloads
        )

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Update existing user(s)

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        payloads : list[dict]
            List of dicts with details for user update(s)

        Returns
        -------
        list[Self]
            List of user(s) updated
        """
        return super(User, cls).put(
            adapter=adapter, endpoint="/user/{id}", payloads=payloads
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        """Search for users based on provided criteria

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        search_params : list[dict]
            List of dicts, each containing search criteria. 1 result returned per dict.
        search_list : Optional[list[Self]], optional
            Provide to search against an existing list, by default pulls from API

        Returns
        -------
        list[Self]
            List of users from results
        """
        return super(User, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )

    @classmethod
    def current(cls, adapter: MetabaseApi) -> list[Self]:
        """Fetch the current user

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API

        Returns
        -------
        list[Self]
            Current user details
        """
        response = adapter.get(endpoint="/user/current")
        if response.data:
            return [cls(**record) for record in [response.data]]  # type: ignore
        raise RequestFailure

    @classmethod
    def disable(cls, adapter: MetabaseApi, targets: list[int]) -> dict:
        """Disables user(s) provided

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        targets : list[int]
            List of users to disable

        Returns
        -------
        dict
            Dict of users that were disabled with results
        """
        return super(User, cls).delete(
            adapter=adapter, endpoint="/user/{id}", targets=targets
        )

    @classmethod
    def enable(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        """Re-enable user(s) provided

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        targets : list[int]
            List of users to re-enabled

        Returns
        -------
        list[Self]
            List of users that were re-enabled
        """
        return super(User, cls).put(
            adapter=adapter,
            endpoint="/user/{id}/reactivate",
            payloads=[{"id": target} for target in targets],
        )

    @classmethod
    def resend_invite(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        """Resend the user invite email

        :param adapter: Connection to Metabase API
        :type adapter: MetabaseApi
        :param targets: List of users to resend invites
        :type targets: list[int]
        :return: Users with resent invites
        :rtype: list[Self]
        """
        return super(User, cls).post(
            adapter=adapter,
            endpoint="/user/{id}/send_invite",
            payloads=[{"id": target} for target in targets],
        )

    @classmethod
    def update_password(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Updates passwords for users

        :param adapter: Connection to Metabase API
        :type adapter: MetabaseApi
        :param payloads: List of dicts with user ids and new passwords
        :type payloads: list[dict]
        :return: Users with password changed
        :rtype: list[Self]
        """
        return super(User, cls).put(
            adapter=adapter, endpoint="/user/{id}/password", payloads=payloads
        )

    @classmethod
    def qbnewb(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        """Indicate that a user has been informed about Query Builder.

        :param adapter: Connection to Metabase API
        :type adapter: MetabaseApi
        :param targets: List of users to toggle
        :type targets: list[int]
        :return: Users that were toggled
        :rtype: list[Self]
        """
        return super(User, cls).put(
            adapter=adapter,
            endpoint="/user/{id}/qbnewb",
            payloads=[{"id": target} for target in targets],
        )
