# Standard Library
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zipfile import ZipFile

# Django
from django.core.management.base import BaseCommand

# Third party
import requests

IMPORT_FILES_URLS = {
    "StockEtablissementHistorique_utf8.zip": "https://www.data.gouv.fr/fr/datasets/r/88fbb6b4-0320-443e-b739-b4376a012c32",
    "StockEtablissement_utf8.zip": "https://www.data.gouv.fr/fr/datasets/r/0651fb76-bcf3-4f6a-a38d-bc04fa708576",
    "StockUniteLegaleHistorique_utf8.zip": "https://www.data.gouv.fr/fr/datasets/r/0835cd60-2c2a-497b-bc64-404de704ce89",
    "StockEtablissementLiensSuccession_utf8.zip": "https://www.data.gouv.fr/fr/datasets/r/9c4d5d9c-4bbb-4b9c-837a-6155cb589e26",
    "StockUniteLegale_utf8.zip": "https://www.data.gouv.fr/fr/datasets/r/825f4199-cadd-486c-ac46-a65a8ea1a047",
}

logger = logging.getLogger(__name__)


def download_extract_file(file_to_download):
    zip_file_path, url, keep_archive = file_to_download

    logger.info(f"Downloading file from {url}")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(zip_file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(zip_file_path.parent)

    if keep_archive is False:
        zip_file_path.unlink()

    logger.info(f"✓ File download {url} complete")


class Command(BaseCommand):
    help = "Download INSEE Sirene CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--force-download",
            dest="force_download",
            action="store_true",
            help="Force download of the source files even if they already exist",
        )

        parser.add_argument(
            "-o",
            "--only",
            dest="download_only",
            help="Download only the given files names. Ex: python manage.py download_insee_sirene_csv_files -o StockEtablissement_utf8.zip StockUniteLegale_utf8.zip",
            nargs="+",
        )

        parser.add_argument(
            "-k",
            "--keep-archives",
            dest="keep_archives",
            action="store_true",
            help="Keep the downloaded archives after extraction",
        )

    def handle(self, *args, **options):
        import_files_path = Path(__file__).parent / "data/"
        import_files_path.mkdir(parents=True, exist_ok=True)
        start_time = time.time()
        files_to_download = []

        for zip_file_name, url in IMPORT_FILES_URLS.items():
            if (
                options["download_only"]
                and zip_file_name not in options["download_only"]
            ):
                continue

            csv_file_name = zip_file_name.replace(".zip", ".csv")
            csv_file_path = import_files_path / csv_file_name
            zip_file_path = import_files_path / zip_file_name

            if (
                not (csv_file_path.exists() or zip_file_path.exists())
                or options["force_download"]
            ):
                files_to_download.append((zip_file_path, url, options["keep_archives"]))

        if files_to_download:
            with ThreadPoolExecutor() as executor:
                executor.map(download_extract_file, files_to_download)

        end_time = time.time()
        logger.info(f"Files download done in {end_time - start_time:.2f}s")
