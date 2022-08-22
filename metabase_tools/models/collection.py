from typing import Optional

from typing_extensions import Self

from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import MetabaseGeneric


class Collection(MetabaseGeneric):
    id: int | str  # root is a valid id for a collection
    description: Optional[str]
    archived: Optional[bool]
    slug: Optional[str]
    color: Optional[str]
    personal_owner_id: Optional[int]
    location: Optional[str]
    namespace: Optional[int]
    effective_location: Optional[str]
    effective_ancestors: Optional[list[dict]]
    can_write: Optional[bool]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        return super(Collection, cls).get(
            adapter=adapter, endpoint="/collection", targets=targets
        )

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(Collection, cls).post(
            adapter=adapter, endpoint="/collection", payloads=payloads
        )

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(Collection, cls).put(
            adapter=adapter, endpoint="/collection/{id}", payloads=payloads
        )

    @classmethod
    def archive(
        cls, adapter: MetabaseApi, targets: list[int], unarchive=False
    ) -> list[Self]:
        return super(Collection, cls).archive(
            adapter=adapter,
            endpoint="/collection/{id}",
            targets=targets,
            unarchive=unarchive,
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        return super(Collection, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )

    @classmethod
    def get_tree(cls, adapter: MetabaseApi) -> list[dict]:
        response = adapter.get(endpoint="/collection/tree")
        if response.data:
            return response.data
        raise EmptyDataReceived

    @staticmethod
    def flatten_tree(parent: dict, path: str = "/") -> list[dict]:
        children = []
        for child in parent["children"]:
            children.append(
                {
                    "id": child["id"],
                    "name": child["name"],
                    "path": f'{path}/{parent["name"]}/{child["name"]}'.replace(
                        "//", "/"
                    ),
                }
            )
            if "children" in child and len(child["children"]) > 0:
                grandchildren = Collection.flatten_tree(
                    child, f'{path}/{parent["name"]}'.replace("//", "/")
                )
                if isinstance(grandchildren, list):
                    children.extend(grandchildren)
                else:
                    children.append(grandchildren)
        return children

    @classmethod
    def get_flat_list(cls, adapter: MetabaseApi) -> list[dict]:
        tree = cls.get_tree(adapter=adapter)
        folders = []
        for root_folder in tree:
            if root_folder["personal_owner_id"] is not None:  # Skips personal folders
                continue
            folders.append(
                {
                    "id": root_folder["id"],
                    "name": root_folder["name"],
                    "path": f'/{root_folder["name"]}',
                }
            )
            folders.extend(Collection.flatten_tree(root_folder))
        return folders

    @classmethod
    def get_contents(
        cls,
        adapter: MetabaseApi,
        collection_id: int,
        model_type: Optional[str] = None,
        archived: bool = False,
    ) -> list:
        params = {}
        if archived:
            params["archived"] = archived
        if model_type:
            params["model"] = model_type
        items = adapter.get(
            endpoint=f"/collection/{collection_id}/items",
            params=params,
        ).data
        if items:
            return items
        raise EmptyDataReceived

    @classmethod
    def graph(cls, adapter: MetabaseApi):
        return adapter.get(endpoint="/collection/graph").data
