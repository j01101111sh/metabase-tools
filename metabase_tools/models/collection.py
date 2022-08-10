from typing import Optional

from typing_extensions import Self

from ..exceptions import EmptyDataReceived
from ..metabase import MetabaseApi
from .generic import MetabaseGeneric


class Collection(MetabaseGeneric):
    description: Optional[str]
    archived: Optional[bool]
    slug: Optional[str]
    color: Optional[str]
    name: str
    personal_owner_id: Optional[int]
    id: str | int
    location: Optional[str]
    namespace: Optional[int]
    effective_location: Optional[str]
    effective_ancestors: Optional[list[str]]
    can_write: Optional[bool]

    @classmethod
    def get(cls, adapter: MetabaseApi, targets: Optional[int | list[int]] = None) -> Self | list[Self]:
        return super(Collection, cls).get(adapter=adapter, endpoint='/collection', targets=targets)

    @classmethod
    def get_tree(cls, adapter: MetabaseApi) -> dict | list[dict]:
        response = adapter.get(endpoint='/collection/tree')
        if response.data:
            return response.data
        else:
            raise EmptyDataReceived

    @staticmethod
    def flatten_tree(parent: dict, path: str = '/') -> list:
        children = []
        for child in parent['children']:
            children.append(
                {'id': child['id'], 'path': f'{path}/{parent["name"]}/{child["name"]}'.replace('//', '/')})
            if 'children' in child and len(child['children']) > 0:
                grandchildren = Collection.flatten_tree(
                    child, f'{path}/{parent["name"]}'.replace('//', '/'))
                if isinstance(grandchildren, list):
                    children.extend(grandchildren)
                else:
                    children.append(grandchildren)
        return children

    @classmethod
    def get_flat_list(cls, adapter: MetabaseApi) -> list:
        tree = cls.get_tree(adapter=adapter)
        folders = []
        for root_folder in tree:
            if root_folder['personal_owner_id'] is not None:  # Skips personal folders
                continue
            folders.append(
                {'id': root_folder['id'], 'path': f'/{root_folder["name"]}'})
            folders.extend(Collection.flatten_tree(root_folder))
        return folders

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: dict | list[dict]) -> Self | list[Self]:
        return super(Collection, cls).post(adapter=adapter, endpoint='/collection', payloads=payloads)

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: dict | list[dict]) -> Self | list[Self]:
        return super(Collection, cls).put(adapter=adapter, endpoint='/collection', payloads=payloads)

    @classmethod
    def archive(cls, adapter: MetabaseApi, targets: int | list[int], unarchive=False) -> Self | list[Self]:
        return super(Collection, cls).archive(adapter=adapter, endpoint='/collection', targets=targets, unarchive=unarchive)
