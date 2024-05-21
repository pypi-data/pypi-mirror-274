from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class UniteLegale(models.Model):
    siren = models.CharField(primary_key=True, verbose_name=_("SIREN"))
    statut_diffusion_unite_legale = models.CharField(verbose_name=_("Statut diffusion unite legale"), null=True, blank=True, db_index=True)
    unite_purgee_unite_legale = models.BooleanField(verbose_name=_("Unite purgee unite legale"), null=True, blank=True, db_index=True)
    date_creation_unite_legale = models.DateField(verbose_name=_("Date creation unite legale"), null=True, blank=True, db_index=True)
    sigle_unite_legale = models.CharField(verbose_name=_("Sigle unite legale"), null=True, blank=True)
    sexe_unite_legale = models.CharField(verbose_name=_("Sexe unite legale"), null=True, blank=True)
    prenom1_unite_legale = models.CharField(verbose_name=_("Prenom1 unite legale"), null=True, blank=True)
    prenom2_unite_legale = models.CharField(verbose_name=_("Prenom2 unite legale"), null=True, blank=True)
    prenom3_unite_legale = models.CharField(verbose_name=_("Prenom3 unite legale"), null=True, blank=True)
    prenom4_unite_legale = models.CharField(verbose_name=_("Prenom4 unite legale"), null=True, blank=True)
    prenom_usuel_unite_legale = models.CharField(verbose_name=_("Prenom usuel unite legale"), null=True, blank=True)
    pseudonyme_unite_legale = models.CharField(verbose_name=_("Pseudonyme unite legale"), null=True, blank=True)
    identifiant_association_unite_legale = models.CharField(verbose_name=_("Identifiant association unite legale"), null=True, blank=True)
    tranche_effectifs_unite_legale = models.CharField(verbose_name=_("Tranche effectifs unite legale"), null=True, blank=True)
    annee_effectifs_unite_legale = models.IntegerField(verbose_name=_("Annee effectifs unite legale"), null=True, blank=True)
    date_dernier_traitement_unite_legale = models.DateTimeField(verbose_name=_("Date dernier traitement unite legale"), null=True, blank=True)
    nombre_periodes_unite_legale = models.IntegerField(verbose_name=_("Nombre periodes unite legale"), null=True, blank=True)
    categorie_entreprise = models.CharField(verbose_name=_("Categorie entreprise"), null=True, blank=True)
    annee_categorie_entreprise = models.IntegerField(verbose_name=_("Annee categorie entreprise"), null=True, blank=True)
    date_debut = models.DateField(verbose_name=_("Date debut"), null=True, blank=True, db_index=True)
    etat_administratif_unite_legale = models.CharField(verbose_name=_("Etat administratif unite legale"), null=True, blank=True, db_index=True)
    nom_unite_legale = models.CharField(verbose_name=_("Nom unite legale"), null=True, blank=True)
    nom_usage_unite_legale = models.CharField(verbose_name=_("Nom usage unite legale"), null=True, blank=True)
    denomination_unite_legale = models.CharField(verbose_name=_("Denomination unite legale"), null=True, blank=True, db_index=True)
    denomination_usuelle1_unite_legale = models.CharField(verbose_name=_("Denomination usuelle1 unite legale"), null=True, blank=True, db_index=True)
    denomination_usuelle2_unite_legale = models.CharField(verbose_name=_("Denomination usuelle2 unite legale"), null=True, blank=True, db_index=True)
    denomination_usuelle3_unite_legale = models.CharField(verbose_name=_("Denomination usuelle3 unite legale"), null=True, blank=True, db_index=True)
    categorie_juridique_unite_legale = models.CharField(verbose_name=_("Categorie juridique unite legale"), null=True, blank=True)
    activite_principale_unite_legale = models.CharField(verbose_name=_("Activite principale unite legale"), null=True, blank=True, db_index=True)
    nomenclature_activite_principale_unite_legale = models.CharField(verbose_name=_("Nomenclature activite principale unite legale"), null=True, blank=True, db_index=True)
    nic_siege_unite_legale = models.CharField(verbose_name=_("NIC siege unite legale"), null=True, blank=True, db_index=True)
    economie_sociale_solidaire_unite_legale = models.CharField(verbose_name=_("Economie sociale solidaire unite legale"), null=True, blank=True, db_index=True)
    societe_mission_unite_legale = models.CharField(verbose_name=_("Societe mission unite legale"), null=True, blank=True)
    caractere_employeur_unite_legale = models.CharField(verbose_name=_("Caractere employeur unite legale"), null=True, blank=True)

    class __Meta__:
        verbose_name = "Unite legale"
        verbose_name_plural = "Unites legales"

    def __str__(self):
        return f'{self.siren} ({self.denomination_unite_legale})' if self.denomination_unite_legale else str(self.siren)


class UniteLegaleHistorique(models.Model):
    siren = models.ForeignKey(UniteLegale, on_delete=models.CASCADE, verbose_name=_("SIREN"), related_name="unite_legale_historiques")
    date_fin = models.DateField(verbose_name=_("Date fin"), null=True, blank=True, db_index=True)
    date_debut = models.DateField(verbose_name=_("Date debut"), null=True, blank=True, db_index=True)
    etat_administratif_unite_legale = models.CharField(verbose_name=_("Etat administratif unite legale"), null=True, blank=True, db_index=True)
    changement_etat_administratif_unite_legale = models.BooleanField(verbose_name=_("Changement etat administratif unite legale"), null=True, blank=True, db_index=True)
    nom_unite_legale = models.CharField(verbose_name=_("Nom unite legale"), null=True, blank=True)
    changement_nom_unite_legale = models.BooleanField(verbose_name=_("Changement nom unite legale"), null=True, blank=True, db_index=True)
    nom_usage_unite_legale = models.CharField(verbose_name=_("Nom usage unite legale"), null=True, blank=True)
    changement_nom_usage_unite_legale = models.BooleanField(verbose_name=_("Changement nom usage unite legale"), null=True, blank=True, db_index=True)
    denomination_unite_legale = models.CharField(verbose_name=_("Denomination unite legale"), null=True, blank=True)
    changement_denomination_unite_legale = models.BooleanField(verbose_name=_("Changement denomination unite legale"), null=True, blank=True, db_index=True)
    denomination_usuelle1_unite_legale = models.CharField(verbose_name=_("Denomination usuelle1 unite legale"), null=True, blank=True)
    denomination_usuelle2_unite_legale = models.CharField(verbose_name=_("Denomination usuelle2 unite legale"), null=True, blank=True)
    denomination_usuelle3_unite_legale = models.CharField(verbose_name=_("Denomination usuelle3 unite legale"), null=True, blank=True)
    changement_denomination_usuelle_unite_legale = models.BooleanField(verbose_name=_("Changement denomination usuelle unite legale"), null=True, blank=True, db_index=True)
    categorie_juridique_unite_legale = models.CharField(verbose_name=_("Categorie juridique unite legale"), null=True, blank=True)
    changement_categorie_juridique_unite_legale = models.BooleanField(verbose_name=_("Changement categorie juridique unite legale"), null=True, blank=True, db_index=True)
    activite_principale_unite_legale = models.CharField(verbose_name=_("Activite principale unite legale"), null=True, blank=True)
    nomenclature_activite_principale_unite_legale = models.CharField(verbose_name=_("Nomenclature activite principale unite legale"), null=True, blank=True)
    changement_activite_principale_unite_legale = models.BooleanField(verbose_name=_("Changement activite principale unite legale"), null=True, blank=True, db_index=True)
    nic_siege_unite_legale = models.CharField(verbose_name=_("NIC siege unite legale"), null=True, blank=True)
    changement_nic_siege_unite_legale = models.BooleanField(verbose_name=_("Changement nic siege unite legale"), null=True, blank=True, db_index=True)
    economie_sociale_solidaire_unite_legale = models.CharField(verbose_name=_("Economie sociale solidaire unite legale"), null=True, blank=True)
    changement_economie_sociale_solidaire_unite_legale = models.BooleanField(verbose_name=_("Changement economie sociale solidaire unite legale"), null=True, blank=True, db_index=True)
    societe_mission_unite_legale = models.CharField(verbose_name=_("Societe mission unite legale"), null=True, blank=True)
    changement_societe_mission_unite_legale = models.BooleanField(verbose_name=_("Changement societe mission unite legale"), null=True, blank=True, db_index=True)
    caractere_employeur_unite_legale = models.CharField(verbose_name=_("Caractere employeur unite legale"), null=True, blank=True)
    changement_caractere_employeur_unite_legale = models.BooleanField(verbose_name=_("Changement caractere employeur unite legale"), null=True, blank=True, db_index=True)

    class __Meta__:
        verbose_name = "Unite legale historique"
        verbose_name_plural = "Unites legales historiques"

    def __str__(self):
        return f'{self.siren}  ({self.date_debut or ""} -> {self.date_fin or ""})'


class Etablissement(models.Model):
    siren = models.ForeignKey(UniteLegale, on_delete=models.CASCADE, verbose_name=_("SIREN"), related_name="etablissements")
    nic = models.CharField(verbose_name=_("NIC"), null=True, blank=True, db_index=True)
    siret = models.CharField(primary_key=True, verbose_name=_("SIRET"))
    statut_diffusion_etablissement = models.CharField(verbose_name=_("Statut diffusion etablissement"), null=True, blank=True, db_index=True)
    date_creation_etablissement = models.DateField(verbose_name=_("Date creation etablissement"), null=True, blank=True)
    tranche_effectifs_etablissement = models.CharField(verbose_name=_("Tranche effectifs etablissement"), null=True, blank=True)
    annee_effectifs_etablissement = models.IntegerField(verbose_name=_("Annee effectifs etablissement"), null=True, blank=True)
    activite_principale_registre_metiers_etablissement = models.CharField(verbose_name=_("Activite principale registre metiers etablissement"), null=True, blank=True)
    date_dernier_traitement_etablissement = models.DateTimeField(verbose_name=_("Date dernier traitement etablissement"), null=True, blank=True)
    etablissement_siege = models.BooleanField(verbose_name=_("Etablissement siege"), null=True, blank=True)
    nombre_periodes_etablissement = models.IntegerField(verbose_name=_("Nombre periodes etablissement"), null=True, blank=True)
    complement_adresse_etablissement = models.CharField(verbose_name=_("Complement adresse etablissement"), null=True, blank=True)
    numero_voie_etablissement = models.CharField(verbose_name=_("Numero voie etablissement"), null=True, blank=True)
    indice_repetition_etablissement = models.CharField(verbose_name=_("Indice repetition etablissement"), null=True, blank=True)
    dernier_numero_voie_etablissement = models.CharField(verbose_name=_("Dernier numero voie etablissement"), null=True, blank=True)
    indice_repetition_dernier_numero_voie_etablissement = models.CharField(verbose_name=_("Indice repetition dernier numero voie etablissement"), null=True, blank=True)
    type_voie_etablissement = models.CharField(verbose_name=_("Type voie etablissement"), null=True, blank=True)
    libelle_voie_etablissement = models.CharField(verbose_name=_("Libelle voie etablissement"), null=True, blank=True)
    code_postal_etablissement = models.CharField(verbose_name=_("Code postal etablissement"), null=True, blank=True)
    libelle_commune_etablissement = models.CharField(verbose_name=_("Libelle commune etablissement"), null=True, blank=True, db_index=True)
    libelle_commune_etranger_etablissement = models.CharField(verbose_name=_("Libelle commune etranger etablissement"), null=True, blank=True)
    distribution_speciale_etablissement = models.CharField(verbose_name=_("Distribution speciale etablissement"), null=True, blank=True)
    code_commune_etablissement = models.CharField(verbose_name=_("Code commune etablissement"), null=True, blank=True, db_index=True)
    code_cedex_etablissement = models.CharField(verbose_name=_("Code cedex etablissement"), null=True, blank=True)
    libelle_cedex_etablissement = models.CharField(verbose_name=_("Libelle cedex etablissement"), null=True, blank=True)
    code_pays_etranger_etablissement = models.CharField(verbose_name=_("Code pays etranger etablissement"), null=True, blank=True)
    libelle_pays_etranger_etablissement = models.CharField(verbose_name=_("Libelle pays etranger etablissement"), null=True, blank=True)
    identifiant_adresse_etablissement = models.CharField(verbose_name=_("Identifiant adresse etablissement"), null=True, blank=True)
    coordonnees_etablissement = models.PointField(verbose_name=_("Coordonnees etablissement"), null=True, blank=True)
    coordonnee_lambert_ordonnee_etablissement = models.CharField(verbose_name=_("Coordonnee lambert ordonnee etablissement"), null=True, blank=True)
    complement_adresse2_etablissement = models.CharField(verbose_name=_("Complement adresse2 etablissement"), null=True, blank=True)
    numero_voie2_etablissement = models.CharField(verbose_name=_("Numero voie2 etablissement"), null=True, blank=True)
    indice_repetition2_etablissement = models.CharField(verbose_name=_("Indice repetition2 etablissement"), null=True, blank=True)
    type_voie2_etablissement = models.CharField(verbose_name=_("Type voie2 etablissement"), null=True, blank=True)
    libelle_voie2_etablissement = models.CharField(verbose_name=_("Libelle voie2 etablissement"), null=True, blank=True)
    code_postal2_etablissement = models.CharField(verbose_name=_("Code postal2 etablissement"), null=True, blank=True)
    libelle_commune2_etablissement = models.CharField(verbose_name=_("Libelle commune2 etablissement"), null=True, blank=True)
    libelle_commune_etranger2_etablissement = models.CharField(verbose_name=_("Libelle commune etranger2 etablissement"), null=True, blank=True)
    distribution_speciale2_etablissement = models.CharField(verbose_name=_("Distribution speciale2 etablissement"), null=True, blank=True)
    code_commune2_etablissement = models.CharField(verbose_name=_("Code commune2 etablissement"), null=True, blank=True)
    code_cedex2_etablissement = models.CharField(verbose_name=_("Code cedex2 etablissement"), null=True, blank=True)
    libelle_cedex2_etablissement = models.CharField(verbose_name=_("Libelle cedex2 etablissement"), null=True, blank=True)
    code_pays_etranger2_etablissement = models.CharField(verbose_name=_("Code pays etranger2 etablissement"), null=True, blank=True)
    libelle_pays_etranger2_etablissement = models.CharField(verbose_name=_("Libelle pays etranger2 etablissement"), null=True, blank=True)
    date_debut = models.DateField(verbose_name=_("Date debut"), null=True, blank=True)
    etat_administratif_etablissement = models.CharField(verbose_name=_("Etat administratif etablissement"), null=True, blank=True, db_index=True)
    enseigne1_etablissement = models.CharField(verbose_name=_("Enseigne1 etablissement"), null=True, blank=True, db_index=True)
    enseigne2_etablissement = models.CharField(verbose_name=_("Enseigne2 etablissement"), null=True, blank=True, db_index=True)
    enseigne3_etablissement = models.CharField(verbose_name=_("Enseigne3 etablissement"), null=True, blank=True, db_index=True)
    denomination_usuelle_etablissement = models.CharField(verbose_name=_("Denomination usuelle etablissement"), null=True, blank=True, db_index=True)
    activite_principale_etablissement = models.CharField(verbose_name=_("Activite principale etablissement"), null=True, blank=True, db_index=True)
    nomenclature_activite_principale_etablissement = models.CharField(verbose_name=_("Nomenclature activite principale etablissement"), null=True, blank=True, db_index=True)
    caractere_employeur_etablissement = models.CharField(verbose_name=_("Caractere employeur etablissement"), null=True, blank=True, db_index=True)

    class __Meta__:
        verbose_name = "Etablissement"
        verbose_name_plural = "Etablissements"

    def __str__(self):
        return f'{self.siret}  ({self.enseigne1_etablissement})' if self.enseigne1_etablissement else str(self.siret)


class EtablissementHistorique(models.Model):
    siren = models.ForeignKey(UniteLegale, on_delete=models.CASCADE, verbose_name=_("SIREN"), related_name="etablissement_historiques")
    nic = models.CharField(verbose_name=_("NIC"), null=True, blank=True, db_index=True)
    siret = models.ForeignKey(Etablissement, on_delete=models.CASCADE, verbose_name=_("SIRET"), related_name="etablissement_historiques")
    date_fin = models.DateField(verbose_name=_("Date fin"), null=True, blank=True, db_index=True)
    date_debut = models.DateField(verbose_name=_("Date debut"), null=True, blank=True, db_index=True)
    etat_administratif_etablissement = models.CharField(verbose_name=_("Etat administratif etablissement"), null=True, blank=True, db_index=True)
    changement_etat_administratif_etablissement = models.BooleanField(verbose_name=_("Changement etat administratif etablissement"), null=True, blank=True, db_index=True)
    enseigne1_etablissement = models.CharField(verbose_name=_("Enseigne1 etablissement"), null=True, blank=True)
    enseigne2_etablissement = models.CharField(verbose_name=_("Enseigne2 etablissement"), null=True, blank=True)
    enseigne3_etablissement = models.CharField(verbose_name=_("Enseigne3 etablissement"), null=True, blank=True)
    changement_enseigne_etablissement = models.BooleanField(verbose_name=_("Changement enseigne etablissement"), null=True, blank=True, db_index=True)
    denomination_usuelle_etablissement = models.CharField(verbose_name=_("Denomination usuelle etablissement"), null=True, blank=True)
    changement_denomination_usuelle_etablissement = models.BooleanField(verbose_name=_("Changement denomination usuelle etablissement"), null=True, blank=True, db_index=True)
    activite_principale_etablissement = models.CharField(verbose_name=_("Activite principale etablissement"), null=True, blank=True)
    nomenclature_activite_principale_etablissement = models.CharField(verbose_name=_("Nomenclature activite principale etablissement"), null=True, blank=True)
    changement_activite_principale_etablissement = models.BooleanField(verbose_name=_("Changement activite principale etablissement"), null=True, blank=True, db_index=True)
    caractere_employeur_etablissement = models.CharField(verbose_name=_("Caractere employeur etablissement"), null=True, blank=True)
    changement_caractere_employeur_etablissement = models.BooleanField(verbose_name=_("Changement caractere employeur etablissement"), null=True, blank=True, db_index=True)

    class __Meta__:
        verbose_name = "Etablissement historique"
        verbose_name_plural = "Etablissements historiques"

    def __str__(self):
        return f'{self.siret}  ({self.date_debut or ""} -> {self.date_fin or ""})'


class EtablissementLiensSuccession(models.Model):
    siret_etablissement_predecesseur = models.ForeignKey(Etablissement, on_delete=models.CASCADE, verbose_name=_("SIRET etablissement predecesseur"), related_name="etablissement_liens_succession_siret_etablissement_predecesseurs")
    siret_etablissement_successeur = models.ForeignKey(Etablissement, on_delete=models.CASCADE, verbose_name=_("SIRET etablissement successeur"), related_name="etablissement_liens_succession_siret_etablissement_successeurs")
    date_lien_succession = models.DateField(verbose_name=_("Date lien succession"), null=True, blank=True, db_index=True)
    transfert_siege = models.BooleanField(verbose_name=_("Transfert siege"), null=True, blank=True, db_index=True)
    continuite_economique = models.BooleanField(verbose_name=_("Continuite economique"), null=True, blank=True, db_index=True)
    date_dernier_traitement_lien_succession = models.DateTimeField(verbose_name=_("Date dernier traitement lien succession"), null=True, blank=True, db_index=True)

    class __Meta__:
        verbose_name = "Etablissement liens succession"
        verbose_name_plural = "Etablissements liens successions"

    def __str__(self):
        return f'{self.siret_etablissement_predecesseur} -> {self.siret_etablissement_successeur} ({self.date_lien_succession})' if self.date_lien_succession else f'{self.siret_etablissement_predecesseur} -> {self.siret_etablissement_successeur}'
