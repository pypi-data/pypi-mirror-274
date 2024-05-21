# Django
from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# Local application / specific library imports
from .models import (
    Etablissement,
    EtablissementHistorique,
    EtablissementLiensSuccession,
    UniteLegale,
    UniteLegaleHistorique,
)


class AdminReadOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AdminReadOnlyInlineMixin(AdminReadOnlyMixin):
    extra = 0
    details_url_reverse = None

    @admin.display(
        description=_("Détails"),
    )
    def see_details(self, obj):
        details_url = reverse(f"admin:{self.details_url_reverse}", args=[obj.pk])
        return mark_safe(f"<a href='{details_url}'>Voir le détail</a>")


class EtablissementInlineAdmin(AdminReadOnlyInlineMixin, admin.TabularInline):
    model = Etablissement
    extra = 0

    details_url_reverse = "insee_sirene_etablissement_change"
    readonly_fields = (
        "siren_display",
        "see_details",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "siret",
                    "nic",
                    "siren_display",
                    "enseigne1_etablissement",
                    "activite_principale_etablissement",
                    "nomenclature_activite_principale_etablissement",
                    "numero_voie_etablissement",
                    "type_voie_etablissement",
                    "libelle_voie_etablissement",
                    "code_postal_etablissement",
                    "libelle_commune_etablissement",
                    "code_commune_etablissement",
                    "see_details",
                ),
            },
        ),
    )

    @admin.display(
        description=_("SIREN"),
    )
    def siren_display(self, obj):
        return obj.siren_id

    verbose_name = _("Établissement")


class UniteLegaleHistoriqueInlineAdmin(AdminReadOnlyInlineMixin, admin.TabularInline):
    model = UniteLegaleHistorique
    extra = 0

    details_url_reverse = "insee_sirene_unitelegalehistorique_change"
    readonly_fields = ("see_details",)

    verbose_name = _("Historique")
    verbose_name_plural = _("Historique")


@admin.register(UniteLegale)
class UniteLegaleAdmin(AdminReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "siren",
        "statut_diffusion_unite_legale",
        "unite_purgee_unite_legale",
        "date_creation_unite_legale",
        "sigle_unite_legale",
        "sexe_unite_legale",
        "prenom1_unite_legale",
        "prenom2_unite_legale",
        "prenom3_unite_legale",
        "prenom4_unite_legale",
        "prenom_usuel_unite_legale",
        "pseudonyme_unite_legale",
        "identifiant_association_unite_legale",
        "tranche_effectifs_unite_legale",
        "annee_effectifs_unite_legale",
        "date_dernier_traitement_unite_legale",
        "nombre_periodes_unite_legale",
        "categorie_entreprise",
        "annee_categorie_entreprise",
        "date_debut",
        "etat_administratif_unite_legale",
        "nom_unite_legale",
        "nom_usage_unite_legale",
        "denomination_unite_legale",
        "denomination_usuelle1_unite_legale",
        "denomination_usuelle2_unite_legale",
        "denomination_usuelle3_unite_legale",
        "categorie_juridique_unite_legale",
        "activite_principale_unite_legale",
        "nomenclature_activite_principale_unite_legale",
        "nic_siege_unite_legale",
        "economie_sociale_solidaire_unite_legale",
        "societe_mission_unite_legale",
        "caractere_employeur_unite_legale",
    )

    search_fields = (
        "siren",
        "nom_unite_legale",
        "denomination_unite_legale",
    )

    inlines = [EtablissementInlineAdmin, UniteLegaleHistoriqueInlineAdmin]


@admin.register(UniteLegaleHistorique)
class UniteLegaleHistoriqueAdmin(AdminReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "siren",
        "date_fin",
        "date_debut",
        "etat_administratif_unite_legale",
        "changement_etat_administratif_unite_legale",
        "nom_unite_legale",
        "changement_nom_unite_legale",
        "nom_usage_unite_legale",
        "changement_nom_usage_unite_legale",
        "denomination_unite_legale",
        "changement_denomination_unite_legale",
        "denomination_usuelle1_unite_legale",
        "denomination_usuelle2_unite_legale",
        "denomination_usuelle3_unite_legale",
        "changement_denomination_usuelle_unite_legale",
        "categorie_juridique_unite_legale",
        "changement_categorie_juridique_unite_legale",
        "activite_principale_unite_legale",
        "nomenclature_activite_principale_unite_legale",
        "changement_activite_principale_unite_legale",
        "nic_siege_unite_legale",
        "changement_nic_siege_unite_legale",
        "economie_sociale_solidaire_unite_legale",
        "changement_economie_sociale_solidaire_unite_legale",
        "societe_mission_unite_legale",
        "changement_societe_mission_unite_legale",
        "caractere_employeur_unite_legale",
        "changement_caractere_employeur_unite_legale",
    )

    search_fields = (
        "siren__siren",
        "nom_unite_legale",
        "denomination_unite_legale",
    )


class EtablissementHistoriqueInlineAdmin(AdminReadOnlyInlineMixin, admin.TabularInline):
    model = EtablissementHistorique
    extra = 0

    details_url_reverse = "insee_sirene_etablissementhistorique_change"
    readonly_fields = ("see_details",)

    verbose_name = _("Historique")
    verbose_name_plural = _("Historique")


class EtablissementLiensSuccessionInlineAdmin(
    AdminReadOnlyInlineMixin, admin.TabularInline
):
    model = EtablissementLiensSuccession
    extra = 0
    fk_name = "siret_etablissement_predecesseur"

    details_url_reverse = "insee_sirene_etablissementlienssuccession_change"
    readonly_fields = ("see_details",)

    verbose_name = _("Lien de succession")
    verbose_name_plural = _("Liens de succession")


@admin.register(Etablissement)
class EtablissementAdmin(AdminReadOnlyMixin, gis_admin.OSMGeoAdmin):
    list_display = (
        "siret",
        "nic",
        "siren_display",
        "enseigne1_etablissement",
        "denomination_usuelle_etablissement",
        "statut_diffusion_etablissement",
        "date_creation_etablissement",
        "tranche_effectifs_etablissement",
        "annee_effectifs_etablissement",
        "activite_principale_registre_metiers_etablissement",
        "date_dernier_traitement_etablissement",
        "etablissement_siege",
        "nombre_periodes_etablissement",
        "complement_adresse_etablissement",
        "numero_voie_etablissement",
        "indice_repetition_etablissement",
        "dernier_numero_voie_etablissement",
        "indice_repetition_dernier_numero_voie_etablissement",
        "type_voie_etablissement",
        "libelle_voie_etablissement",
        "code_postal_etablissement",
        "libelle_commune_etablissement",
        "libelle_commune_etranger_etablissement",
        "distribution_speciale_etablissement",
        "code_commune_etablissement",
        "code_cedex_etablissement",
        "libelle_cedex_etablissement",
        "code_pays_etranger_etablissement",
        "libelle_pays_etranger_etablissement",
        "identifiant_adresse_etablissement",
        "coordonnees_etablissement",
        "complement_adresse2_etablissement",
        "numero_voie2_etablissement",
        "indice_repetition2_etablissement",
        "type_voie2_etablissement",
        "libelle_voie2_etablissement",
        "code_postal2_etablissement",
        "libelle_commune2_etablissement",
        "libelle_commune_etranger2_etablissement",
        "distribution_speciale2_etablissement",
        "code_commune2_etablissement",
        "code_cedex2_etablissement",
        "libelle_cedex2_etablissement",
        "code_pays_etranger2_etablissement",
        "libelle_pays_etranger2_etablissement",
        "date_debut",
        "etat_administratif_etablissement",
        "enseigne2_etablissement",
        "enseigne3_etablissement",
        "activite_principale_etablissement",
        "nomenclature_activite_principale_etablissement",
        "caractere_employeur_etablissement",
    )

    readonly_fields = (
        "siret",
        "nic",
        "siren_display",
        "enseigne1_etablissement",
        "denomination_usuelle_etablissement",
        "statut_diffusion_etablissement",
        "date_creation_etablissement",
        "tranche_effectifs_etablissement",
        "annee_effectifs_etablissement",
        "activite_principale_registre_metiers_etablissement",
        "date_dernier_traitement_etablissement",
        "etablissement_siege",
        "nombre_periodes_etablissement",
        "complement_adresse_etablissement",
        "numero_voie_etablissement",
        "indice_repetition_etablissement",
        "dernier_numero_voie_etablissement",
        "indice_repetition_dernier_numero_voie_etablissement",
        "type_voie_etablissement",
        "libelle_voie_etablissement",
        "code_postal_etablissement",
        "libelle_commune_etablissement",
        "libelle_commune_etranger_etablissement",
        "distribution_speciale_etablissement",
        "code_commune_etablissement",
        "code_cedex_etablissement",
        "libelle_cedex_etablissement",
        "code_pays_etranger_etablissement",
        "libelle_pays_etranger_etablissement",
        "identifiant_adresse_etablissement",
        "complement_adresse2_etablissement",
        "numero_voie2_etablissement",
        "indice_repetition2_etablissement",
        "type_voie2_etablissement",
        "libelle_voie2_etablissement",
        "code_postal2_etablissement",
        "libelle_commune2_etablissement",
        "libelle_commune_etranger2_etablissement",
        "distribution_speciale2_etablissement",
        "code_commune2_etablissement",
        "code_cedex2_etablissement",
        "libelle_cedex2_etablissement",
        "code_pays_etranger2_etablissement",
        "libelle_pays_etranger2_etablissement",
        "date_debut",
        "etat_administratif_etablissement",
        "enseigne2_etablissement",
        "enseigne3_etablissement",
        "activite_principale_etablissement",
        "nomenclature_activite_principale_etablissement",
        "caractere_employeur_etablissement",
    )

    # Special case for OSMGeoAdmin to display a map on field "coordonnees_etablissement"
    modifiable = False

    def has_change_permission(self, request, obj=None):
        return True

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "siret",
                    "nic",
                    "siren_display",
                    "enseigne1_etablissement",
                    "denomination_usuelle_etablissement",
                    "statut_diffusion_etablissement",
                    "date_creation_etablissement",
                    "tranche_effectifs_etablissement",
                    "annee_effectifs_etablissement",
                    "activite_principale_registre_metiers_etablissement",
                    "date_dernier_traitement_etablissement",
                    "etablissement_siege",
                    "nombre_periodes_etablissement",
                    "complement_adresse_etablissement",
                    "numero_voie_etablissement",
                    "indice_repetition_etablissement",
                    "dernier_numero_voie_etablissement",
                    "indice_repetition_dernier_numero_voie_etablissement",
                    "type_voie_etablissement",
                    "libelle_voie_etablissement",
                    "code_postal_etablissement",
                    "libelle_commune_etablissement",
                    "libelle_commune_etranger_etablissement",
                    "distribution_speciale_etablissement",
                    "code_commune_etablissement",
                    "code_cedex_etablissement",
                    "libelle_cedex_etablissement",
                    "code_pays_etranger_etablissement",
                    "libelle_pays_etranger_etablissement",
                    "identifiant_adresse_etablissement",
                    "coordonnees_etablissement",
                    "complement_adresse2_etablissement",
                    "numero_voie2_etablissement",
                    "indice_repetition2_etablissement",
                    "type_voie2_etablissement",
                    "libelle_voie2_etablissement",
                    "code_postal2_etablissement",
                    "libelle_commune2_etablissement",
                    "libelle_commune_etranger2_etablissement",
                    "distribution_speciale2_etablissement",
                    "code_commune2_etablissement",
                    "code_cedex2_etablissement",
                    "libelle_cedex2_etablissement",
                    "code_pays_etranger2_etablissement",
                    "libelle_pays_etranger2_etablissement",
                    "date_debut",
                    "etat_administratif_etablissement",
                    "enseigne2_etablissement",
                    "enseigne3_etablissement",
                    "activite_principale_etablissement",
                    "nomenclature_activite_principale_etablissement",
                    "caractere_employeur_etablissement",
                ),
            },
        ),
    )

    @admin.display(description="SIREN", ordering="siren_id")
    def siren_display(self, obj):
        return obj.siren_id

    search_fields = (
        "siret",
        "siren__siren",
        "enseigne1_etablissement",
        "denomination_usuelle_etablissement",
    )

    inlines = [
        EtablissementHistoriqueInlineAdmin,
        EtablissementLiensSuccessionInlineAdmin,
    ]


@admin.register(EtablissementHistorique)
class EtablissementHistoriqueAdmin(AdminReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "siren",
        "nic",
        "siret",
        "date_fin",
        "date_debut",
        "etat_administratif_etablissement",
        "changement_etat_administratif_etablissement",
        "enseigne1_etablissement",
        "enseigne2_etablissement",
        "enseigne3_etablissement",
        "changement_enseigne_etablissement",
        "denomination_usuelle_etablissement",
        "changement_denomination_usuelle_etablissement",
        "activite_principale_etablissement",
        "nomenclature_activite_principale_etablissement",
        "changement_activite_principale_etablissement",
        "caractere_employeur_etablissement",
        "changement_caractere_employeur_etablissement",
    )

    search_fields = (
        "siret__siret",
        "siren__siren",
        "enseigne1_etablissement",
        "denomination_usuelle_etablissement",
    )


@admin.register(EtablissementLiensSuccession)
class EtablissementLiensSuccessionAdmin(AdminReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "siret_etablissement_predecesseur",
        "siret_etablissement_successeur",
        "date_lien_succession",
        "transfert_siege",
        "continuite_economique",
        "date_dernier_traitement_lien_succession",
    )

    search_fields = (
        "siret_etablissement_predecesseur__siret",
        "siret_etablissement_successeur__siret",
    )
