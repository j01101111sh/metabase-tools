from datetime import datetime
from json import dumps
from pathlib import Path

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card import Card
from metabase_tools.models.collection import Collection


class MetabaseTools(MetabaseApi):
    def download_native_queries(
        self,
        save_path: str | None = None,
        save_file: str | None = None,
        root_folder: str = "./",
        file_extension: str = ".sql",
    ) -> Path:
        # TODO make method generic to include other filters
        """Downloads all native queries into a JSON file

        Parameters
        ----------
        save_path : str | None, optional
            Name of the file to save results to, by default None
        """
        # Determine save path
        timestamp = datetime.now().strftime("%y%m%dT%H%M%S")
        save_path = save_path or "."
        save_file = save_file or f"mapping_{timestamp}.json"

        # Download list of cards from Metabase API
        cards = Card.get(adapter=self)

        # Filter list of cards to only those with native queries
        cards = [card for card in cards if card.query_type == "native"]

        # Create dictionary of collections for file paths
        collections = {}
        for item in Collection.get_flat_list(adapter=self):
            collections[item["id"]] = {"name": item["name"], "path": item["path"]}

        # Format filtered list
        formatted_list = {
            "root": root_folder,
            "file_extension": file_extension,
            "cards": [],
        }

        for card in cards:
            path = collections[card.collection_id]["path"]
            new_card = {"name": card.name, "id": card.id, "path": path}
            formatted_list["cards"].append(new_card)

        # Save formatted + filtered list
        path = Path(f"{save_path}")
        path.mkdir(parents=True, exist_ok=True)
        path /= save_file
        with open(path, "w", newline="", encoding="utf-8") as file:
            file.write(dumps(formatted_list, indent=2))

        # Returns path to file saved
        return path
