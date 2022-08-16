from datetime import datetime
from json import dumps, loads
from pathlib import Path

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card import Card
from metabase_tools.models.collection import Collection


class MetabaseTools(MetabaseApi):
    def download_native_queries(
        self,
        save_path: str | None = None,
        save_file: str | None = None,
        root_folder: str = ".",
        file_extension: str = "sql",
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
            try:
                new_card = {
                    "id": card.id,
                    "name": card.name,
                    "path": collections[card.collection_id]["path"],
                }
            except KeyError as error:
                # Raised if collection_id is not in collections which will happen for personal colls
                continue
            formatted_list["cards"].append(new_card)
            sql_code = card.dataset_query["native"]["query"]

            sql_path = Path(f"{save_path}/{new_card['path']}")
            sql_path.mkdir(parents=True, exist_ok=True)
            sql_path /= f"{new_card['name']}.{file_extension}"
            with open(sql_path, "w", newline="", encoding="utf-8") as file:
                file.write(sql_code)

        # Save formatted + filtered list
        mapping_path = Path(f"{save_path}")
        mapping_path.mkdir(parents=True, exist_ok=True)
        mapping_path /= save_file
        with open(mapping_path, "w", newline="", encoding="utf-8") as file:
            file.write(dumps(formatted_list, indent=2))

        # Returns path to file saved
        return mapping_path

    def upload_native_queries(
        self,
        mapping_path: Path | str,
        dry_run: bool = True,
        error_on_failure: bool = False,
    ) -> list[dict]:
        """Uploads files

        Parameters
        ----------
        mapping_path : Path | str
            Path to the mapping configuration file, by default None
        dry_run : bool, optional
            Execute task as a dry run (i.e. do not make any changes), by default True

        Returns
        -------
        list[dict]
            list of dicts with results of upload
        """
        # Determine mapping path
        mapping_path = Path(mapping_path or "./mapping.json")

        # Open mapping configuration file
        with open(mapping_path, "r") as file:
            mapping = loads(file.read())

        # Initialize common settings (e.g. root folder, file extension, etc.)
        root_folder = mapping.get("root", ".")
        extension = mapping.get("file_extension", ".sql")
        cards = mapping["cards"]

        # Iterate through mapping file
        updates = []
        for card in cards:
            card_path = Path(f"{root_folder}/{card['path']}/{card['name']}.{extension}")
            if card_path.exists():
                if "id" in card:
                    card_obj = Card.get(adapter=self, targets=[card["id"]])[0]
                    # Verify query definition
                    with open(card_path, "r", newline="", encoding="utf-8") as file:
                        dev_code = file.read()
                    prod_code = card_obj.dataset_query["native"]["query"]
                    code_update = dev_code != prod_code
                    # Verify location of card
                    collections = Collection.get_flat_list(adapter=self)
                    dev_loc = card["path"][1:]
                    prod_loc = None
                    for coll in collections:
                        if card_obj.collection_id == coll["id"]:
                            prod_loc = coll["name"]
                            break
                    loc_update = dev_loc != prod_loc
                    new_coll_id = card_obj.collection_id
                    if loc_update:
                        for coll in collections:
                            if coll["path"] == card["path"]:
                                new_coll_id = coll["id"]
                                break
                    # Generate update
                    if code_update or loc_update:
                        new_query = card_obj.dataset_query
                        new_query["native"]["query"] = dev_code
                        new_def = {
                            "id": card["id"],
                            "dataset_query": new_query,
                            "collection_id": new_coll_id,
                        }
                        updates.append(new_def)
                else:
                    # Check if a card with the same name exists in the listed location
                    # If exists, update card
                    # Elif does not exist, create card
                    pass
            else:
                raise FileNotFoundError(f"{card_path} not found")

        # Loop exit before pushing changes to Metabase in case errors are encountered
        # Push changes back to Metabase API
        results = []
        if not dry_run:
            update_results = Card.put(adapter=self, payloads=updates)
            if isinstance(update_results, list):
                for result in update_results:
                    results.append(
                        {"id": result.id, "name": result.name, "is_success": True}
                    )

        return results
