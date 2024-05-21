# Standard Library
import shutil
import warnings
from collections import defaultdict
from pathlib import Path

# Django
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Third party
import pandas as pd

# Project
from insee_sirene.shortcuts import camel_to_snake

warnings.filterwarnings("ignore")

MODEL_CODE = """
class {model_name}(models.Model):
    {fields}

    class __Meta__:
        verbose_name = "{vb}"
        verbose_name_plural = "{vbp}"

    def __str__(self):
        return {model_str}
"""

MODELS_ORDER = [
    "UniteLegale",
    "UniteLegaleHistorique",
    "Etablissement",
    "EtablissementHistorique",
    "EtablissementLiensSuccession",
]

MODELS_PRIMARY_KEYS = {
    "UniteLegale": "siren",
    "Etablissement": "siret",
}

MODELS_DB_INDEX = {
    "UniteLegale": {
        "statut_diffusion_unite_legale",
        "unite_purgee_unite_legale",
        "date_creation_unite_legale",
        "date_debut",
        "etat_administratif_unite_legale",
        "denomination_unite_legale",
        "denomination_usuelle1_unite_legale",
        "denomination_usuelle2_unite_legale",
        "denomination_usuelle3_unite_legale",
        "activite_principale_unite_legale",
        "nomenclature_activite_principale_unite_legale",
        "nic_siege_unite_legale",
        "economie_sociale_solidaire_unite_legale",
    },
    "UniteLegaleHistorique": {
        "date_fin",
        "date_debut",
        "etat_administratif_unite_legale",
        "changement_etat_administratif_unite_legale",
        "changement_nom_unite_legale",
        "changement_nom_usage_unite_legale",
        "changement_denomination_unite_legale",
        "changement_denomination_usuelle_unite_legale",
        "changement_categorie_juridique_unite_legale",
        "changement_activite_principale_unite_legale",
        "changement_nic_siege_unite_legale",
        "changement_economie_sociale_solidaire_unite_legale",
        "changement_societe_mission_unite_legale",
        "changement_caractere_employeur_unite_legale",
    },
    "Etablissement": {
        "nic",
        "statut_diffusion_etablissement",
        "libelle_commune_etablissement",
        "code_commune_etablissement",
        "etat_administratif_etablissement",
        "enseigne1_etablissement",
        "enseigne2_etablissement",
        "enseigne3_etablissement",
        "denomination_usuelle_etablissement",
        "activite_principale_etablissement",
        "nomenclature_activite_principale_etablissement",
        "caractere_employeur_etablissement",
    },
    "EtablissementHistorique": {
        "nic",
        "date_fin",
        "date_debut",
        "etat_administratif_etablissement",
        "changement_etat_administratif_etablissement",
        "changement_enseigne_etablissement",
        "changement_denomination_usuelle_etablissement",
        "changement_activite_principale_etablissement",
        "changement_caractere_employeur_etablissement",
    },
    "EtablissementLiensSuccession": {
        "date_lien_succession",
        "transfert_siege",
        "continuite_economique",
        "date_dernier_traitement_lien_succession",
    },
}

MODELS_BOOLEANS_FIELDS = {
    "UniteLegale": {
        "unite_purgee_unite_legale",
    },
    "UniteLegaleHistorique": {
        "changement_etat_administratif_unite_legale",
        "changement_nom_unite_legale",
        "changement_nom_usage_unite_legale",
        "changement_denomination_unite_legale",
        "changement_denomination_usuelle_unite_legale",
        "changement_categorie_juridique_unite_legale",
        "changement_activite_principale_unite_legale",
        "changement_nic_siege_unite_legale",
        "changement_economie_sociale_solidaire_unite_legale",
        "changement_societe_mission_unite_legale",
        "changement_caractere_employeur_unite_legale",
    },
    "Etablissement": {
        "etablissement_siege",
    },
    "EtablissementHistorique": {
        "changement_etat_administratif_etablissement",
        "changement_enseigne_etablissement",
        "changement_denomination_usuelle_etablissement",
        "changement_activite_principale_etablissement",
        "changement_caractere_employeur_etablissement",
    },
    "EtablissementLiensSuccession": {
        "transfert_siege",
        "continuite_economique",
    },
}

MODELS_INTEGER_FIELDS = {
    "UniteLegale": {
        "annee_effectifs_unite_legale",
        "nombre_periodes_unite_legale",
        "annee_categorie_entreprise",
    },
    "Etablissement": {
        "annee_effectifs_etablissement",
        "nombre_periodes_etablissement",
    },
}

MODELS_POINT_FIELDS = {
    "Etablissement": {
        "coordonnees_etablissement": {
            "x": "coordonnee_lambert_abscisse_etablissement",
            "y": "coordonnee_lambert_ordonnee_etablissement",
        }
    },
}

MODELS_DATE_FIELDS = {
    "UniteLegale": {
        "date_creation_unite_legale",
        "date_debut",
    },
    "UniteLegaleHistorique": {
        "date_fin",
        "date_debut",
    },
    "Etablissement": {
        "date_creation_etablissement",
        "date_debut",
    },
    "EtablissementHistorique": {
        "date_fin",
        "date_debut",
    },
    "EtablissementLiensSuccession": {
        "date_lien_succession",
    },
}

MODELS_DATETIME_FIELDS = {
    "UniteLegale": {"date_dernier_traitement_unite_legale"},
    "Etablissement": {
        "date_dernier_traitement_etablissement",
    },
    "EtablissementLiensSuccession": {
        "date_dernier_traitement_lien_succession",
    },
}

MODELS_FOREIGN_KEYS = {
    "UniteLegaleHistorique": {"siren": "UniteLegale"},
    "Etablissement": {"siren": "UniteLegale"},
    "EtablissementHistorique": {
        "siren": "UniteLegale",
        "siret": "Etablissement",
    },
    "EtablissementLiensSuccession": {
        "siret_etablissement_predecesseur": "Etablissement",
        "siret_etablissement_successeur": "Etablissement",
    },
}

MODELS_STR_FIELDS = {
    "UniteLegale": "f'{self.siren} ({self.denomination_unite_legale})' if self.denomination_unite_legale else str(self.siren)",
    "UniteLegaleHistorique": 'f\'{self.siren}  ({self.date_debut or ""} -> {self.date_fin or ""})\'',
    "Etablissement": "f'{self.siret}  ({self.enseigne1_etablissement})' if self.enseigne1_etablissement else str(self.siret)",
    "EtablissementHistorique": 'f\'{self.siret}  ({self.date_debut or ""} -> {self.date_fin or ""})\'',
    "EtablissementLiensSuccession": "f'{self.siret_etablissement_predecesseur} -> {self.siret_etablissement_successeur} ({self.date_lien_succession})' if self.date_lien_succession else f'{self.siret_etablissement_predecesseur} -> {self.siret_etablissement_successeur}'",
}


class Command(BaseCommand):
    help = "Generates Django models from a CSV file"

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

    def handle(self, *args, **options):
        import_files_path = Path(__file__).parent / "data/"
        import_files_path.mkdir(parents=True, exist_ok=True)

        files_to_download = []
        for model_name in MODELS_ORDER:
            csv_file_name = f"Stock{model_name}_utf8.csv"
            zip_file_name = csv_file_name.replace(".csv", ".zip")

            csv_file_path = import_files_path / csv_file_name

            if not csv_file_path.exists() or options["force_download"]:
                files_to_download.append(zip_file_name)

        if files_to_download:
            call_command(
                "download_insee_sirene_csv_files", download_only=files_to_download
            )

        models = {}

        for model_name in MODELS_ORDER:
            csv_file_name = f"Stock{model_name}_utf8.csv"
            csv_file_path = import_files_path / csv_file_name

            df = pd.read_csv(
                csv_file_path,
                nrows=1,
                sep=",",
            )

            model_vb = self.to_verbose_name(model_name)
            model_vbp = " ".join(
                word + "s" if word[-1] != "s" else word for word in model_vb.split()
            )
            fields = []

            model_foreign_keys = MODELS_FOREIGN_KEYS.get(model_name, {})
            model_primary_key = MODELS_PRIMARY_KEYS.get(model_name)
            models_db_index = MODELS_DB_INDEX.get(model_name, set())
            models_booleans_fields = MODELS_BOOLEANS_FIELDS.get(model_name, set())
            models_date_fields = MODELS_DATE_FIELDS.get(model_name, set())
            models_datetime_fields = MODELS_DATETIME_FIELDS.get(model_name, set())
            models_integer_fields = MODELS_INTEGER_FIELDS.get(model_name, set())
            models_point_fields = []
            models_point_fields_mapping = {}
            for p_field_name, p_field in MODELS_POINT_FIELDS.get(
                model_name, {}
            ).items():
                for index, p_field_value in enumerate(p_field.values(), start=1):
                    models_point_fields_mapping[p_field_value] = p_field_name
                    models_point_fields.append(p_field_value)
                    if index == 1:
                        break

            related_models_count = defaultdict(int)
            for mfk_model_name in model_foreign_keys.values():
                related_models_count[mfk_model_name] += 1

            for column in df.columns:
                column = column.strip()
                verbose_name = self.to_verbose_name(column)
                field_name = camel_to_snake(column)

                foreign_key = model_foreign_keys.get(field_name)
                primary_key = field_name == model_primary_key
                db_index = field_name in models_db_index
                is_boolean = field_name in models_booleans_fields
                is_date_field = field_name in models_date_fields
                is_datetime_field = field_name in models_datetime_fields
                is_integer_field = field_name in models_integer_fields
                is_point_field = field_name in models_point_fields

                if foreign_key:
                    model_name_snake = camel_to_snake(model_name)
                    if related_models_count[foreign_key] > 1:
                        related_name = f"{model_name_snake}_{field_name}s"
                    else:
                        related_name = f"{model_name_snake}s"

                    fields.append(
                        f'{field_name} = models.ForeignKey({foreign_key}, on_delete=models.CASCADE, verbose_name=_("{verbose_name}"), related_name="{related_name}")'
                    )
                elif primary_key:
                    fields.append(
                        f'{field_name} = models.CharField(primary_key=True, verbose_name=_("{verbose_name}"))'
                    )
                else:

                    if is_boolean is True:
                        field_kind = "BooleanField"
                    elif is_date_field is True:
                        field_kind = "DateField"
                    elif is_datetime_field is True:
                        field_kind = "DateTimeField"
                    elif is_integer_field is True:
                        field_kind = "IntegerField"
                    elif is_point_field is True:
                        field_kind = "PointField"

                        if field_name not in models_point_fields_mapping:
                            continue
                        else:
                            field_name = models_point_fields_mapping[field_name]
                            verbose_name = field_name.replace("_", " ").capitalize()

                    else:
                        field_kind = "CharField"

                    field = f'{field_name} = models.{field_kind}(verbose_name=_("{verbose_name}"), null=True, blank=True'

                    if db_index:
                        field += ", db_index=True"

                    field += ")"

                    fields.append(field)

            model_str = MODELS_STR_FIELDS.get(model_name, "self.pk")

            models[model_name] = MODEL_CODE.format(
                model_name=model_name,
                fields="\n    ".join(fields),
                vb=model_vb,
                vbp=model_vbp,
                model_str=model_str,
            )

        raw_generated_models_file = "raw_generated_models.py"
        raw_generated_models_file_path = (
            Path(__file__).parent / "../../history" / raw_generated_models_file
        )
        models_file_path = Path(__file__).parent / "../../models.py"

        with open(raw_generated_models_file_path, "w") as f:
            f.write("from django.contrib.gis.db import models\n")
            f.write("from django.utils.translation import gettext as _\n\n")
            f.write("\n".join(models.values()))

        shutil.copyfile(raw_generated_models_file_path, models_file_path)

        print(
            "Done! Please see changes in raw_generated_models.py and models.py file to see if you need to manually adjust the generated models."
        )

    def to_verbose_name(self, camelCase: str):
        verbose_name = (
            "".join([" " + char if char.isupper() else char for char in camelCase])
            .strip()
            .capitalize()
        )

        verbose_name = verbose_name.replace("Siren", "SIREN")  # noqa
        verbose_name = verbose_name.replace("Nic", "NIC")  # noqa
        verbose_name = verbose_name.replace("Siret", "SIRET")  # noqa

        return verbose_name
