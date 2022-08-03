import logging
from datetime import datetime

from ..metabase_api import MetabaseApi


def download_native_queries(using: MetabaseApi, save_path: str | None = None) -> None:
    """Downloads all native queries on the connected server into a JSON file formatted for input into the upload_native_queries function

    Parameters
    ----------
    save_path : str | None, optional
        Name of the file to save results to, by default None
    """
    # Determine save path
    dt = datetime.now().strftime('%y%m%dT%H%M%S')
    save_path = save_path or f'./mapping_{dt}.json'

    # Download list of cards from Metabase API
    cards = []

    # Filter list of cards to only those with native queries
    cards = [card for card in cards if card.query_type == 'native']

    # Format filtered list
    formatted_list = {
        "root": "./metabase",
        "file extension": ".sql",
        "folders": {}
    }

    for card in cards:
        pass

    # Save formatted + filtered list


def upload_native_queries(using: MetabaseApi, mapping_path: str | None = None, dry_run: bool = True) -> None:
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
