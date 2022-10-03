from datetime import datetime
from json import dumps, loads
from pathlib import Path

import pytest
from packaging.version import Version

from metabase_tools import MetabaseApi
from tests.helpers import random_string


class TestDownload:
    def test_download_native_queries(self, api: MetabaseApi, result_path):
        file = api.tools.download_native_queries(root_folder=f"{result_path}/data/")
        assert file.stat().st_size > 0  # File size greater than 0
        assert (
            file.stat().st_ctime - datetime.now().timestamp() < 2
        )  # file was created in the last 2 seconds


class TestUpload:
    def test_upload_existing(self, api: MetabaseApi):
        mapping_path = Path("./tests/data/mapping.json")
        test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
        with open(test_card_path, "r", newline="", encoding="utf-8") as file:
            current = file.read()
        with open(test_card_path, "a", newline="", encoding="utf-8") as file:
            file.write("\n-- " + random_string(6))
        try:
            results = api.tools.upload_native_queries(
                mapping_path=mapping_path,
                file_extension="sql",
                dry_run=False,
                stop_on_error=False,
            )
        except:
            assert False
        finally:
            with open(test_card_path, "w", newline="", encoding="utf-8") as file:
                file.write(current)
        assert isinstance(results, list)
        assert all(isinstance(result, dict) for result in results)
        assert all(result["is_success"] for result in results)

    def test_upload_existing_dry(self, api: MetabaseApi):
        mapping_path = Path("./tests/data/mapping.json")
        test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
        with open(test_card_path, "r", newline="", encoding="utf-8") as file:
            current = file.read()
        with open(test_card_path, "a", newline="", encoding="utf-8") as file:
            file.write("\n-- " + random_string(6))
        try:
            results = api.tools.upload_native_queries(
                mapping_path=mapping_path,
                file_extension="sql",
                dry_run=True,
                stop_on_error=False,
            )
        except:
            assert False
        finally:
            with open(test_card_path, "w", newline="", encoding="utf-8") as file:
                file.write(current)
        assert isinstance(results, dict)
        assert "updates" in results and len(results["updates"]) > 0
        assert "creates" in results
        assert "errors" in results

    def test_upload_existing_stop(self, api: MetabaseApi):
        mapping_path = Path("./tests/data/mapping.json")
        test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
        with open(test_card_path, "r", newline="", encoding="utf-8") as file:
            current = file.read()
        with open(test_card_path, "a", newline="", encoding="utf-8") as file:
            file.write("\n-- " + random_string(6))
        with pytest.raises(FileNotFoundError):
            _ = api.tools.upload_native_queries(
                mapping_path=mapping_path,
                file_extension="sql",
                dry_run=False,
                stop_on_error=True,
            )
        with open(test_card_path, "w", newline="", encoding="utf-8") as file:
            file.write(current)

    def test_upload_existing_dry_stop(self, api: MetabaseApi):
        mapping_path = Path("./tests/data/mapping.json")
        test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
        with open(test_card_path, "r", newline="", encoding="utf-8") as file:
            current = file.read()
        with open(test_card_path, "a", newline="", encoding="utf-8") as file:
            file.write("\n-- " + random_string(6))
        with pytest.raises(FileNotFoundError):
            _ = api.tools.upload_native_queries(
                mapping_path=mapping_path,
                file_extension="sql",
                dry_run=True,
                stop_on_error=True,
            )
        with open(test_card_path, "w", newline="", encoding="utf-8") as file:
            file.write(current)

    def test_upload_new(self, api: MetabaseApi, server_version: Version):
        # Set parameters
        mapping_path = Path("./tests/data/mapping.json")
        test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
        # Read contents of test card
        with open(test_card_path, "r", newline="", encoding="utf-8") as file:
            test_card = file.read()
        # Create new .sql file with same contents
        rdm_str = random_string(6)
        new_card_path = Path(
            f"{test_card_path} - {rdm_str}".replace(".sql", "") + ".sql"
        )
        with open(new_card_path, "w", encoding="utf-8") as file:
            file.write(test_card)
        # Update mapping file with new file
        with open(mapping_path, "r", encoding="utf-8") as file:
            o_map: list = loads(file.read())
        n_map = o_map.copy()
        new_card_map = {
            "name": f"Test Card - {rdm_str}",
            "collection_id": 5,
            "path": "/Development/Accounting",
            "database_id": 1,
            "database_name": "Sample Dataset",
        }
        if server_version >= Version("v0.42"):
            new_card_map["database_name"] = new_card_map["database_name"].replace(
                "Sample Dataset", "Sample Database"
            )
        n_map.append(new_card_map)
        with open(mapping_path, "w", encoding="utf-8") as file:
            file.write(dumps(n_map, indent=2))
        # Run upload
        try:
            results = api.tools.upload_native_queries(
                mapping_path=mapping_path,
                file_extension="sql",
                dry_run=False,
                stop_on_error=False,
            )
        except:
            assert False
        finally:
            # Undo changes
            if new_card_path.exists():
                new_card_path.unlink()
            with open(mapping_path, "w", encoding="utf-8") as file:
                file.write(dumps(o_map, indent=2))
                file.write("\n")
        # Tests
        assert isinstance(results, list)
        assert all(isinstance(result, dict) for result in results)
        assert all(result["is_success"] for result in results)
