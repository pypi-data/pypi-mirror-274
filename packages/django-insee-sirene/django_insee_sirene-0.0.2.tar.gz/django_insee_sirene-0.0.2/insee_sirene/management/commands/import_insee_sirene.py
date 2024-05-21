# Standard Library
import logging
import shutil
import time
from pathlib import Path

# Django
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management import call_command

# from django import db
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Model
from django.utils.timezone import make_aware

# Third party
import dateutil.parser
import pandas as pd

# Project
from insee_sirene.models import (
    Etablissement,
    EtablissementHistorique,
    EtablissementLiensSuccession,
    UniteLegale,
    UniteLegaleHistorique,
)
from insee_sirene.shortcuts import camel_to_snake

FK_FIXES = {
    UniteLegale: [],
    UniteLegaleHistorique: ["siren"],
    Etablissement: ["siren"],
    EtablissementHistorique: ["siren", "siret"],
    EtablissementLiensSuccession: [
        "siret_etablissement_predecesseur",
        "siret_etablissement_successeur",
    ],
}

IMPORT_MODELS_ORDER = [
    UniteLegale,
    UniteLegaleHistorique,
    Etablissement,
    EtablissementHistorique,
    EtablissementLiensSuccession,
]

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import INSEE Sirene data from CSV files"

    def __init__(self, *args, **kwargs):
        self.siren_set = set()
        self.siret_set = set()
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--force-download",
            dest="force_download",
            action="store_true",
            help="Force download of the source files",
        )
        parser.add_argument(
            "-k",
            "--keep-sources-folder",
            dest="keep_sources_folder",
            action="store_true",
            help="Keep downloaded sources folder after import",
        )
        parser.add_argument(
            "--chunk",
            dest="chunk_size",
            type=int,
            help="Amount of lines to read at once and objects bulk created (1000 by default)",
            default=1000,
        )

    def handle(self, *args, **options):
        import_files_path = Path(__file__).parent / "data/"
        import_files_path.mkdir(parents=True, exist_ok=True)

        files_to_download = []
        for model_class in IMPORT_MODELS_ORDER:
            csv_file_name = f"Stock{model_class.__name__}_utf8.csv"
            zip_file_name = csv_file_name.replace(".csv", ".zip")

            csv_file_path = import_files_path / csv_file_name

            if not csv_file_path.exists() or options["force_download"]:
                files_to_download.append(zip_file_name)

        if files_to_download:
            call_command(
                "download_insee_sirene_csv_files", download_only=files_to_download
            )

        start_time = time.time()

        with transaction.atomic():
            for model_class in IMPORT_MODELS_ORDER:
                logger.info(f"Importing {model_class._meta.object_name}")
                csv_file_name = f"Stock{model_class.__name__}_utf8.csv"
                csv_file_path = import_files_path / csv_file_name

                CSVImporter(
                    file_path=csv_file_path,
                    model_class=model_class,
                    chunk_size=options["chunk_size"],
                    siren_set=self.siren_set,
                    siret_set=self.siret_set,
                    start_time=start_time,
                ).run()

        end_time = time.time()
        logger.info(f"Import done in {end_time - start_time:.2f}s")

        if not options["keep_sources_folder"]:
            shutil.rmtree(import_files_path)


class CSVImporter:
    def __init__(
        self,
        file_path: Path,
        model_class: Model,
        chunk_size: int,
        siren_set: set[str],
        siret_set: set[str],
        start_time: float,
    ):
        self.file_path = file_path
        self.model_class = model_class
        self.chunk_size = chunk_size
        self.start_time = start_time

        self.siren_set = siren_set
        self.siret_set = siret_set

        with file_path.open() as f:
            self.line_amount = 0
            for line in f:
                self.line_amount += 1

    def run(self):
        skipped = 0
        total = 0

        chunks = pd.read_csv(
            self.file_path,
            chunksize=self.chunk_size,
            header=0,
            sep=",",
            dtype=str,
        )
        for chunk in chunks:
            amount = self.import_chunk(chunk)

            total += chunk.shape[0]
            skipped += chunk.shape[0] - amount

            log_message = f"[{time.time() - self.start_time:.2f}s][{self.model_class._meta.object_name}]  {total}/{self.line_amount} ({(total / self.line_amount * 100):.2f}%)"
            log_message += f", {skipped} skipped." if skipped else "."
            logger.info(log_message)

            if total > self.line_amount:
                break

        return self.siren_set, self.siret_set

    def import_chunk(self, chunk: pd.DataFrame):
        # Replace NaN values with None
        chunk = chunk.astype(object).where(pd.notnull(chunk), None)
        # Replace trash values with None
        chunk = chunk.replace(["[ND]", "-"], None)  # noqa
        # Convert the Dataframe to a list of dictionaries
        data = chunk.to_dict("records")  # noqa

        objects = []
        for row in data:
            try:
                obj = self.create_object_from_row(row)
                objects.append(obj)
            except ValueError:
                continue

        self.model_class.objects.bulk_create(objects)

        return len(objects)

    def create_object_from_row(self, row: dict):
        row = {camel_to_snake(k): v for k, v in row.items()}

        # Fix & ignore not existing FK
        for fk_field in FK_FIXES.get(self.model_class):
            value = row.pop(fk_field, None)
            if ("siren" in fk_field and value not in self.siren_set) or (
                "siret" in fk_field and value not in self.siret_set
            ):
                raise ValueError(f"FK {fk_field} not found: {value}")

            row[fk_field + "_id"] = value

        # Cast model values
        for field_name in row.keys():
            if field_name in (
                "coordonnee_lambert_abscisse_etablissement",
                "coordonnee_lambert_ordonnee_etablissement",
            ):
                continue

            field = self.model_class._meta.get_field(field_name)
            if field.get_internal_type() == "BooleanField":
                row[field_name] = row[field_name] == "true"
            elif field.get_internal_type() == "IntegerField":
                try:
                    row[field_name] = int(row[field_name])
                except (ValueError, TypeError):
                    row[field_name] = None
            elif field.get_internal_type() == "DateField":
                try:
                    row[field_name] = dateutil.parser.parse(row[field_name]).date()
                except (ValueError, TypeError):
                    row[field_name] = None
            elif field.get_internal_type() == "DateTimeField":
                try:
                    row[field_name] = dateutil.parser.parse(row[field_name])

                    if settings.USE_TZ:
                        row[field_name] = make_aware(row[field_name])

                except (ValueError, TypeError):
                    row[field_name] = None

        # Very specific case for PointField
        x_coordinate = row.pop("coordonnee_lambert_abscisse_etablissement", None)
        y_coordinate = row.pop("coordonnee_lambert_ordonnee_etablissement", None)

        if x_coordinate and y_coordinate:
            x_coordinate = float(x_coordinate)
            y_coordinate = float(y_coordinate)
            # breakpoint()
            row["coordonnees_etablissement"] = Point(
                y_coordinate,
                x_coordinate,
                # srid=2154,
            )

        # Save siren and siret for future FK constraints check
        if self.model_class is UniteLegale:
            self.siren_set.add(row["siren"])
        if self.model_class is Etablissement:
            self.siret_set.add(row["siret"])

        obj = self.model_class(**row)
        return obj
