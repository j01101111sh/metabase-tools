"""
MetabaseTools extends MetabaseApi with additional complex functions
"""
from datetime import datetime
from json import dumps, loads
from pathlib import Path
from typing import Optional

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card import Card
from metabase_tools.models.collection import Collection
from metabase_tools.models.database import Database


class MetabaseTools(MetabaseApi):
    """Extends MetabaseApi with additional complex functions"""

    def download_native_queries(
        self,
        save_file: Optional[Path | str] = None,
        root_folder: Path | str = ".",
        file_extension: str = "sql",
    ) -> Path:
        # TODO make method generic to include other filters
        """Downloads all native queries into a JSON file

        Parameters
        ----------
        save_file : Optional[Path | str], optional
            Path to save mapping file, defaults to mapping_{timestamp}.json
        root_folder : Path | str, optional
            Root folder to save queries, by default "."
        file_extension : str, optional
            File extension to save the queries, by default "sql"

        Returns
        -------
        Path
            Path to save file
        """
        # Determine save path
        timestamp = datetime.now().strftime("%y%m%dT%H%M%S")
        root_folder = Path(root_folder)  # Convert root folder to a path object
        save_file = Path(save_file or f"mapping_{timestamp}.json")

        # Download list of cards from Metabase API and filter to only native queries
        cards = [card for card in Card.get(adapter=self) if card.query_type == "native"]
        self._logger.debug("Found %s cards with native queries", len(cards))

        # Create dictionary of collections for file paths
        collections = {
            item["id"]: {"name": item["name"], "path": item["path"]}
            for item in Collection.get_flat_list(adapter=self)
        }
        self._logger.debug("Generated flat list of %s collections", len(collections))

        # Format filtered list
        formatted_list = {
            "root": str(root_folder),
            "file_extension": file_extension,
            "cards": [],
        }

        for card in cards:
            # Mapping dict append
            try:
                new_card = {
                    "id": card.id,
                    "name": card.name,
                    "path": collections[card.collection_id]["path"],
                    "database": Database.search(
                        adapter=self, search_params=[{"id": card.database_id}]
                    )[0].name,
                }
            except KeyError as error_raised:
                self._logger.warning(
                    "Skipping %s (personal collection)\n%s", card.name, card
                )
                continue
            formatted_list["cards"].append(new_card)

            # SQL file creation
            sql_code = card.dataset_query["native"]["query"]
            sql_path = Path(f"{root_folder}/{new_card['path']}")
            sql_path.mkdir(parents=True, exist_ok=True)
            sql_path /= f"{new_card['name']}.{file_extension}"
            try:
                with open(sql_path, "w", newline="", encoding="utf-8") as file:
                    file.write(sql_code)
                self._logger.debug(f"{card.name} saved to {sql_path}\n{card}")
            except OSError as error_raised:
                self._logger.warning(
                    "Skipping %s (name error): %s\n%s",
                    card.name,
                    str(error_raised),
                    card,
                )
                continue

        # Save mapping file
        mapping_path = Path(f"{root_folder}")
        mapping_path.mkdir(parents=True, exist_ok=True)
        mapping_path /= save_file
        self._logger.debug(
            "Completed iterating through list, saving file: %s", mapping_path
        )
        with open(mapping_path, "w", newline="", encoding="utf-8") as file:
            file.write(dumps(formatted_list, indent=2))

        # Returns path to file saved
        return mapping_path

    def upload_native_queries(
        self,
        mapping_path: Path | str,
        dry_run: bool = True,
        stop_on_error: bool = False,
    ) -> list[dict] | dict:
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
        root_folder = Path(mapping.get("root", "."))
        extension = mapping.get("file_extension", ".sql")
        cards = mapping["cards"]

        # Iterate through mapping file
        changes = {"updates": [], "creates": [], "errors": []}
        collections = Collection.get_flat_list(adapter=self)
        for card in cards:
            card_path = Path(f"{root_folder}/{card['path']}/{card['name']}.{extension}")
            if card_path.exists():  # Ensures file exists
                if "id" in card:  # If ID is in mapping, use that, else use location
                    prod_card = Card.get(adapter=self, targets=[card["id"]])[0]
                    # Verify query definition
                    with open(card_path, "r", newline="", encoding="utf-8") as file:
                        dev_code = file.read()
                    # Verify location of card
                    prod_loc = [
                        coll["path"]
                        for coll in collections
                        if prod_card.collection_id == coll["id"]
                    ][0]
                    dev_coll_id = prod_card.collection_id  # Sets to prod loc as default
                    if card["path"] != prod_loc:
                        # find coll_id of new path
                        dev_coll_id = [
                            coll["id"]
                            for coll in collections
                            if coll["path"] == card["path"]
                        ][0]
                    # Generate update
                    if (
                        dev_code != prod_card.dataset_query["native"]["query"]
                        or card["path"] != prod_loc
                    ):
                        dev_query = prod_card.dataset_query.copy()
                        dev_query["native"]["query"] = dev_code
                        dev_def = {
                            "id": card["id"],
                            "dataset_query": dev_query,
                            "collection_id": dev_coll_id,
                        }
                        changes["updates"].append(dev_def.copy())
                else:
                    # Check if a card with the same name exists in the listed location
                    dev_coll_id = [
                        coll["id"]
                        for coll in collections
                        if card["path"] == coll["path"]
                    ][0]
                    try:
                        card_id = [
                            item["id"]
                            for item in self.get(
                                endpoint=f"/collection/{dev_coll_id}/items"
                            ).data  # type: ignore
                            if item["model"] == "card" and item["name"] == card["name"]
                        ][0]
                    except IndexError as error_raised:
                        self._logger.debug(
                            "Card not found in listed location, creating: %s", card
                        )
                        card_id = None
                    except TypeError as error_raised:
                        # No items in collection
                        card_id = None

                    if card_id:  # update card
                        prod_card = Card.get(adapter=self, targets=[card_id])[0]
                        with open(card_path, "r", newline="", encoding="utf-8") as file:
                            dev_code = file.read()
                        if dev_code != prod_card.dataset_query["native"]["query"]:
                            dev_query = prod_card.dataset_query.copy()
                            dev_query["native"]["query"] = dev_code
                            dev_def = {"id": card_id, "dataset_query": dev_query}
                            changes["updates"].append(dev_def)
                    else:  # create card
                        with open(card_path, "r", newline="", encoding="utf-8") as file:
                            dev_query = file.read()
                        db_id = [
                            database.id
                            for database in Database.get(adapter=self)
                            if card["database"] == database.name
                        ][0]

                        new_card_def = {
                            "visualization_settings": {},
                            "collection_id": dev_coll_id,
                            "name": card["name"],
                            "dataset_query": {
                                "type": "native",
                                "native": {"query": dev_query},
                                "database": db_id,
                            },
                            "display": "table",
                        }
                        changes["creates"].append(new_card_def.copy())
            else:
                self._logger.error(
                    "Skipping %s (file not found):\n%s", card["name"], card
                )
                if stop_on_error:
                    raise FileNotFoundError(f"{card_path} not found")
                else:
                    changes["errors"].append(card)

        # Loop exit before pushing changes to Metabase in case errors are encountered
        # Push changes back to Metabase API
        if not dry_run:
            results = []
            if len(changes["updates"]) > 0:
                update_results = Card.put(adapter=self, payloads=changes["updates"])
                if isinstance(update_results, list):
                    for result in update_results:
                        results.append(
                            {"id": result.id, "name": result.name, "is_success": True}
                        )

            if len(changes["creates"]) > 0:
                create_results = Card.post(adapter=self, payloads=changes["creates"])
                if isinstance(create_results, list):
                    for result in create_results:
                        results.append(
                            {"id": result.id, "name": result.name, "is_success": True}
                        )

            return results
        else:
            return changes
