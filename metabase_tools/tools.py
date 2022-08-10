from datetime import datetime
from json import dumps
from pathlib import Path

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card import Card
from metabase_tools.models.collection import Collection


class MetabaseTools(MetabaseApi):
    def download_native_queries(self, save_path: str | None = None, save_file: str | None = None, root_folder: str = './', file_extension: str = '.sql') -> Path:
        # TODO make method generic to include other filters
        """Downloads all native queries on the connected server into a JSON file formatted for input into the upload_native_queries function

        Parameters
        ----------
        save_path : str | None, optional
            Name of the file to save results to, by default None
        """
        # Determine save path
        dt = datetime.now().strftime('%y%m%dT%H%M%S')
        save_path = save_path or f'.'
        save_file = save_file or f'mapping_{dt}.json'

        # Download list of cards from Metabase API
        cards = Card.get(adapter=self)

        # Filter list of cards to only those with native queries
        cards = [card for card in cards
                 if card.query_type == 'native']

        # Create dictionary of collections for file paths
        collections = {}
        for item in Collection.get_flat_list(adapter=self):
            collections[item['id']] = {
                'name': item['name'],
                'path': item['path']
            }

        # Format filtered list
        formatted_list = {
            'root': root_folder,
            'file_extension': file_extension,
            'cards': []
        }

        for card in cards:
            path = collections[card.collection_id]['path']
            new_card = {
                'name': card.name,
                'id': card.id,
                'path': path
            }
            formatted_list['cards'].append(new_card)

        # Save formatted + filtered list
        p = Path(f'{save_path}')
        p.mkdir(parents=True, exist_ok=True)
        p /= save_file
        with open(p, 'w', newline='', encoding='utf-8') as f:
            f.write(dumps(formatted_list, indent=2))

        # Returns path to file saved
        return p

    def upload_native_queries(self, mapping_path: str | None = None, dry_run: bool = True) -> None:
        """Uploads files 

        Parameters
        ----------
        mapping_path : str | None, optional
            Path to the mapping configuration file, by default None
        dry_run : bool, optional
            Execute task as a dry run (i.e. do not make any changes), by default True
        """
        # Determine mapping path

        # Open mapping configuration file

        # Initialize common settings (e.g. root folder, file extension, etc.)

        # Iterate through mapping file

        # Get Card object from Metabase API

        # Validate that the data from Metabase API matches mapping file

        # Merge existing dataset_query from API with query defintion from file

        # Loop exit before pushing changes to Metabase in case errors are encountered
        # Push changes back to Metabase API
        if not dry_run:
            pass
