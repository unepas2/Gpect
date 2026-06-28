#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÉTAPE 2 — SCRIPT MAÎTRE d'analyse, collège ENTREPRISES (GPECT Issoudun).
Tous les indicateurs sont calculés ici et écrits dans resultats_entreprises.json
+ un rapport lisible resultats_entreprises_rapport.md.
Règles : agrégé / question par question ; multi-select via str.contains ;
n= partout ; effet de poids (Safran) traité avec ET sans.
Rejouable à l'identique d'une vague à l'autre.
"""
import json
import re
import numpy as np
import pandas as pd
from datetime import datetime, timezone

PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/126d3b2d-01_entreprises.xlsx.xlsx"
OUT_JSON = "/home/user/Gpect/analyse/resultats/resultats_entreprises.json"
OUT_MD = "/home/user/Gpect/analyse/resultats/resultats_entreprises_rapport.md"
SOURCE_DATE = "2026-03 (collecte) / export reçu 2026-06-28"

df = pd.read_excel(PATH, engine="openpyxl", dtype=object)
cols = list(df.columns)
N = len(df)
assert N == 21, f"PÉRIMÈTRE INVALIDE : {N} lignes au lieu de 21"

# index Safran (plus gros employeur) repéré en contrôle interne via Q1.4 = 1550
EFF = pd.to_numeric(df[cols[14]], errors="coerce")
SAFRAN_IDX = int(EFF.idxmax())  # ligne du plus gros employeur

R = {"_meta": {
        "college": "Entreprises",
        "n_repondants": N,
        "source": PATH.split("/")[-1],
        "source_date": SOURCE_DATE,
        "genere_le": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "plus_gros_employeur_ligne_interne": SAFRAN_IDX,
        "regles": "agrégé, question par question, anonyme ; multi-select via contains ; n= explicite",
    }, "questions": {}}

def r1(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 1)

def scale_stats(idx, label, qid):
    s = pd.to_numeric(df[cols[idx]], errors="coerce").dropna()
    d = {"qid": qid, "type": "echelle_1_5", "intitule": str(cols[idx]),
         "n": int(s.shape[0]),
         "moyenne": r1(s.mean()), "mediane": r1(s.median()),
         "min": (None if s.empty else int(s.min())),
         "max": (None if s.empty else int(s.max())),
         "ecart_type": r1(s.std(ddof=1)) if s.shape[0] > 1 else None}
    return d

def battery(idx_range, qid, intitule_base):
    items = []
    for i in idx_range:
        sub = re.search(r"\[(.+)\]", str(cols[i]))
        sublabel = sub.group(1) if sub else str(cols[i])
        st = scale_stats(i, sublabel, qid)
        st["item"] = sublabel
        items.append(st)
    items_sorted = sorted(items, key=lambda x: (x["moyenne"] if x["moyenne"] is not None else -1), reverse=True)
    return {"qid": qid, "type": "batterie_echelle_1_5", "intitule": intitule_base,
            "n_items": len(items), "items": items, "classement_par_moyenne": items_sorted}

def cat_counts(idx, qid, normalize=None):
    s = df[cols[idx]].dropna()
    if normalize:
        s = s.map(normalize)
    n = int(s.shape[0])
    vc = s.value_counts()
    out = [{"modalite": str(k), "n": int(v), "pct": r1(100*v/n)} for k, v in vc.items()]
    return {"qid": qid, "type": "choix_unique", "intitule": str(cols[idx]),
            "n_repondants": n, "modalites": out}

def multi_counts(idx, qid, modalites, intitule=None):
    s = df[cols[idx]].dropna().astype(str)
    n = int(s.shape[0])
    out = []
    for lab, kw in modalites:
        cnt = int(s.str.contains(re.escape(kw), case=False, na=False).sum())
        out.append({"modalite": lab, "mot_cle": kw, "n": cnt, "pct_repondants": r1(100*cnt/n)})
    out = sorted(out, key=lambda x: x["n"], reverse=True)
    return {"qid": qid, "type": "multi_select", "intitule": str(cols[idx]),
            "n_repondants": n, "note": "% = part des répondants ayant cité la modalité (contains)",
            "modalites": out}

def numeric_stats(idx, qid, with_without_top=False, top_idx=None, treat_nonnum_as_missing=True):
    raw = df[cols[idx]]
    num = pd.to_numeric(raw, errors="coerce")
    non_num = raw[raw.notna() & num.isna()]
    s = num.dropna()
    d = {"qid": qid, "type": "numerique", "intitule": str(cols[idx]),
         "n": int(s.shape[0]),
         "n_non_numerique_exclus": int(non_num.shape[0]),
         "valeurs_non_numeriques": [str(x) for x in non_num.unique().tolist()],
         "somme": r1(s.sum()), "moyenne": r1(s.mean()), "mediane": r1(s.median()),
         "min": r1(s.min()), "max": r1(s.max())}
    if with_without_top and top_idx is not None and top_idx in s.index:
        s2 = s.drop(index=top_idx)
        d["sans_plus_gros"] = {"n": int(s2.shape[0]), "somme": r1(s2.sum()),
                               "moyenne": r1(s2.mean()), "mediane": r1(s2.median()),
                               "max": r1(s2.max())}
    return d

# ===================== Q0 — IDENTITÉ (PII exclues) =====================
R["questions"]["Q0"] = {"type": "identite", "note":
    "Champs nominatifs (nom, interlocuteur, e-mail, tél., NAF, convention) EXCLUS des résultats (anonymat). "
    "Consentement : 21/21 (Q : prise de connaissance + consentement)."}
R["questions"]["Q0.8_statut"] = cat_counts(10, "Q0.8",
    normalize=lambda x: str(x).strip().upper())

# ===================== Q1 — PROFIL =====================
R["questions"]["Q1.1_secteur"] = cat_counts(11, "Q1.1")
R["questions"]["Q1.3_effectif_tranche"] = cat_counts(13, "Q1.3")
R["questions"]["Q1.4_effectif_inscrit"] = numeric_stats(14, "Q1.4",
    with_without_top=True, top_idx=SAFRAN_IDX)
R["questions"]["Q1.5_recours_externes"] = multi_counts(15, "Q1.5", [
    ("Intérim", "Intérim"),
    ("Prestation de services industriels/logistiques", "Prestation de services"),
    ("Aucun recours externe", "Aucun recours")])
R["questions"]["Q1.6_volume_interim_ETP"] = numeric_stats(16, "Q1.6",
    with_without_top=True, top_idx=SAFRAN_IDX)
R["questions"]["Q1.7_volume_prestation"] = numeric_stats(17, "Q1.7")
R["questions"]["Q1.8_age_dirigeant"] = cat_counts(18, "Q1.8")

# ===================== Q2 — STRATÉGIE / ANTICIPATION =====================
R["questions"]["Q2.1_preoccupations"] = multi_counts(19, "Q2.1", [
    ("Maintenir activité/compétitivité (hausse des coûts)", "Maintenir l'activité"),
    ("Recruter des collaborateurs qualifiés", "Recruter des collaborateurs"),
    ("Fidéliser les collaborateurs en poste", "Fidéliser les collaborateurs"),
    ("Investir / moderniser l'outil de production", "Investir pour moderniser"),
    ("Développer de nouveaux marchés ou clients", "Développer de nouveaux marchés"),
    ("Diversifier l'activité / nouveaux produits", "Diversifier l'activité"),
    ("Transition écologique et énergétique", "transition écologique"),
    ("Évolutions technologiques (Industrie 4.0, IA)", "évolutions technologiques"),
    ("Préparer la transmission / reprise", "transmission ou la reprise")])
R["questions"]["Q2.2_transmission"] = cat_counts(20, "Q2.2")
R["questions"]["Q2.3_evolution_effectifs"] = cat_counts(21, "Q2.3")
R["questions"]["Q2.4_investissements"] = cat_counts(22, "Q2.4")
R["questions"]["Q2.5_invest_competences"] = cat_counts(23, "Q2.5")

# ===================== Q3 — MÉTIERS / TENSIONS =====================
R["questions"]["Q3.2_tension"] = cat_counts(25, "Q3.2")
R["questions"]["Q3.3_causes_tensions"] = battery(range(26, 36), "Q3.3",
    "Causes des tensions (1 faible → 5 fort impact)")
R["questions"]["Q3.4_metiers_sensibles"] = cat_counts(36, "Q3.4")
R["questions"]["Q3.5_facteurs_transformation"] = battery(range(37, 42), "Q3.5",
    "Facteurs de transformation (1→5)")

# ===================== Q4 — DÉMOGRAPHIE / TURNOVER / TRANSMISSION =====================
# Pyramide : base cohérente (8 cellules entières & somme ≈ effectif déclaré)
pyr_idx = list(range(42, 50))
pyr_labels = ["H<30", "F<30", "H31-44", "F31-44", "H45-59", "F45-59", "H60+", "F60+"]
pyr_num = df.iloc[:, pyr_idx].apply(lambda c: pd.to_numeric(c, errors="coerce"))
row_sum = pyr_num.sum(axis=1, skipna=True)
all_int = pyr_num.apply(lambda row: all((pd.notna(v) and float(v) == int(v)) for v in row), axis=1)
tol = np.maximum(2.0, 0.20 * EFF)
coherent = all_int & (np.abs(row_sum - EFF) <= tol)
excl = [int(i) for i in df.index[~coherent]]
base_idx = [int(i) for i in df.index[coherent]]

def pyramide(idx_list):
    sub = pyr_num.loc[idx_list]
    totals = {lab: int(sub.iloc[:, k].sum()) for k, lab in enumerate(pyr_labels)}
    total = sum(totals.values())
    H = totals["H<30"]+totals["H31-44"]+totals["H45-59"]+totals["H60+"]
    Fm = totals["F<30"]+totals["F31-44"]+totals["F45-59"]+totals["F60+"]
    moins30 = totals["H<30"]+totals["F<30"]
    t31_44 = totals["H31-44"]+totals["F31-44"]
    t45_59 = totals["H45-59"]+totals["F45-59"]
    t60 = totals["H60+"]+totals["F60+"]
    seniors45 = t45_59 + t60
    return {"n_repondants": len(idx_list), "total_tetes": total,
            "par_cellule": totals,
            "hommes": H, "femmes": Fm,
            "pct_femmes": r1(100*Fm/total) if total else None,
            "tranche_moins30": moins30, "tranche_31_44": t31_44,
            "tranche_45_59": t45_59, "tranche_60plus": t60,
            "pct_moins30": r1(100*moins30/total) if total else None,
            "pct_31_44": r1(100*t31_44/total) if total else None,
            "pct_45_59": r1(100*t45_59/total) if total else None,
            "pct_60plus": r1(100*t60/total) if total else None,
            "seniors_45plus": seniors45,
            "pct_seniors_45plus": r1(100*seniors45/total) if total else None}

base_sans_safran = [i for i in base_idx if i != SAFRAN_IDX]
R["questions"]["Q4.1_pyramide"] = {
    "qid": "Q4.1", "type": "pyramide_effectifs",
    "note": ("Pyramide sur base COHÉRENTE = pyramide entière ET somme ≈ effectif déclaré (±20%, min 2). "
             f"Exclus : {len(excl)} répondants (décimaux/incohérents/non renseignés). "
             "Calcul sensible au poids → présenté AVEC et SANS le plus gros employeur."),
    "lignes_exclues_internes": excl,
    "AVEC_plus_gros": pyramide(base_idx),
    "SANS_plus_gros": pyramide(base_sans_safran)}
R["questions"]["Q4.2_retraite_2ans"] = numeric_stats(50, "Q4.2", with_without_top=True, top_idx=SAFRAN_IDX)
R["questions"]["Q4.3_retraite_5ans"] = numeric_stats(51, "Q4.3", with_without_top=True, top_idx=SAFRAN_IDX)
R["questions"]["Q4.4_services_retraite"] = multi_counts(52, "Q4.4", [
    ("Production / Fabrication", "Production / Fabrication"),
    ("Qualité", "Qualité"),
    ("Maintenance", "Maintenance"),
    ("Logistique", "Logistique"),
    ("Bureau d'études", "Bureau d'études"),
    ("Management de proximité", "Management de proximité"),
    ("Comptabilité / contrôle de gestion", "Comptabilité et contrôle"),
    ("Commerce / ADV", "Commerce / ADV"),
    ("Achat / Approvisionnement", "Achat / Approvisionnement"),
    ("Chefs de projets / chargés d'affaires", "Chefs de projets"),
    ("Conduite / transport (verbatims)", "ondu")])  # CONDUITE/CONDUCTEUR/conducteurs
R["questions"]["Q4.5_turnover"] = cat_counts(53, "Q4.5")
R["questions"]["Q4.7_motifs_depart"] = battery(range(55, 65), "Q4.7",
    "Motifs de départ (1→5)")
R["questions"]["Q4.8_dispositifs_transmission"] = battery(range(65, 70), "Q4.8",
    "Dispositifs de transmission en place (1 pas du tout → 5 très bien)")
R["questions"]["Q4.8b_besoin_transmission"] = cat_counts(70, "Q4.8b")

# ===================== Q5 — RECRUTEMENT =====================
R["questions"]["Q5.1_recrutements_2024_2025"] = cat_counts(71, "Q5.1")
R["questions"]["Q5.2_difficulte"] = scale_stats(72, "difficulté", "Q5.2")
R["questions"]["Q5.3_freins_recrutement"] = battery(range(73, 81), "Q5.3",
    "Freins au recrutement (1→5)")
R["questions"]["Q5.4_recrut_prevus_3ans"] = numeric_stats(81, "Q5.4", with_without_top=True, top_idx=SAFRAN_IDX)
R["questions"]["Q5.5_motivation_recrut"] = multi_counts(82, "Q5.5", [
    ("Remplacement départs à la retraite", "départs à la retraite"),
    ("Remplacement départs volontaires", "départs volontaires"),
    ("Accroissement de l'activité actuelle", "Accroissement de l'activité"),
    ("Lancement nouvelle activité/marché", "Lancement d'une nouvelle"),
    ("Création postes liés à la transformation techno", "Création de nouveaux postes")])
R["questions"]["Q5.6_actions_attractivite"] = multi_counts(83, "Q5.6", [
    ("Relations écoles / CFA / lycées", "Relations avec les écoles"),
    ("Portes ouvertes / visites / journées découverte", "Portes ouvertes"),
    ("Communication réseaux sociaux", "réseaux sociaux"),
    ("Programme d'ambassadeurs métiers", "ambassadeurs métiers"),
    ("Partenariat France Travail / Mission Locale / Cap Emploi", "France Travail, Mission Locale"),
    ("Aucune action spécifique", "Aucune action")])

# ===================== Q6 — COMPÉTENCES =====================
R["questions"]["Q6.1_tech_adaptees"] = cat_counts(84, "Q6.1")
R["questions"]["Q6.2_tech_manquantes"] = multi_counts(85, "Q6.2", [
    ("Usinage, mécanique, travail des métaux", "Usinage, mécanique"),
    ("Maintenance industrielle et automatismes", "Maintenance industrielle"),
    ("Programmation machines (robots, automates, CNC)", "Programmation de machines"),
    ("Qualité, contrôle et métrologie", "Qualité, contrôle et métrologie"),
    ("CAO / DAO / lecture de plans", "CAO / DAO"),
    ("Numérique industriel, data, traçabilité (ERP/GPAO)", "Numérique industriel"),
    ("Logistique, supply chain, flux", "Logistique, supply chain"),
    ("Conduite de véhicules / engins (SPL, CACES)", "Conduite de véhicules"),
    ("Sécurité et prévention des risques", "Sécurité et prévention"),
    ("Compétences commerciales / relation client", "Compétences commerciales"),
    ("Management et gestion d'équipe", "Management et gestion d'équipe"),
    ("Transition écologique et énergétique", "Transition écologique"),
    ("Aucun manque identifié", "Aucun manque")])
R["questions"]["Q6.3_savoiretre_adaptes"] = cat_counts(86, "Q6.3")
R["questions"]["Q6.4_savoiretre_renforcer"] = multi_counts(87, "Q6.4", [
    ("Autonomie et prise d'initiative", "Autonomie et prise"),
    ("Rigueur et respect des procédures", "Rigueur et respect"),
    ("Travail en équipe et coopération", "Travail en équipe"),
    ("Gestion du stress et résilience", "Gestion du stress"),
    ("Culture sécurité et vigilance", "Culture sécurité"),
    ("Engagement et sens des responsabilités", "Engagement et sens"),
    ("Adaptabilité au changement technologique", "Adaptabilité au changement")])
R["questions"]["Q6.5_competences_3_5ans"] = multi_counts(88, "Q6.5", [
    ("Automatisation, cobotique, robotique avancée", "Automatisation, cobotique"),
    ("Intelligence artificielle", "Intelligence artificielle"),
    ("Maintenance avancée", "Maintenance avancée"),
    ("Transition énergétique et décarbonation", "Transition énergétique"),
    ("Cybersécurité industrielle", "Cybersécurité industrielle"),
    ("Management de la performance / pilotage indicateurs", "Management de la performance"),
    ("Conduite du changement et gestion de projet", "Conduite du changement"),
    ("Animation d'équipes (agile/projet)", "Animation d'équipes"),
    ("Transmission des savoir-faire et tutorat", "Transmission des savoir-faire"),
    ("Outils numériques collaboratifs", "outils numériques collaboratifs"),
    ("Communication professionnelle écrite/orale", "Communication professionnelle"),
    ("Anglais", "Anglais")])

# ===================== Q7 — FORMATION =====================
R["questions"]["Q7.1_formations_organisees"] = multi_counts(89, "Q7.1", [
    ("Développement des compétences métiers", "développement des compétences métiers"),
    ("Management et développement personnel", "management et développement personnel"),
    ("Obligatoires uniquement (sécurité, habilitations)", "obligatoires uniquement")])
R["questions"]["Q7.2_connaissance_opco"] = cat_counts(90, "Q7.2")
R["questions"]["Q7.3_freins_formation"] = multi_counts(91, "Q7.3", [
    ("Absence de formation adaptée localement", "Absence de formation adaptée"),
    ("Coût pédagogique trop élevé", "Coût pédagogique"),
    ("Coût déplacements / hébergements", "Coût des déplacements"),
    ("Difficulté à libérer les salariés", "Difficulté à libérer"),
    ("Manque de temps pour organiser", "Manque de temps"),
    ("Faible appétence des salariés", "Faible appétence"),
    ("Complexité administrative des financements", "Complexité administrative"),
    ("Aucun frein particulier", "Aucun frein")])
R["questions"]["Q7.4_alternance"] = cat_counts(92, "Q7.4")
R["questions"]["Q7.5_alternants_territoire"] = cat_counts(93, "Q7.5")
R["questions"]["Q7.6_offre_adaptee"] = scale_stats(94, "adéquation offre", "Q7.6")
R["questions"]["Q7.7_raisons_inadequation"] = battery(range(95, 101), "Q7.7",
    "Raisons d'inadéquation de l'offre (1→5)")
R["questions"]["Q7.8_cooperation_acteurs"] = cat_counts(101, "Q7.8")
R["questions"]["Q7.9_attentes_acteurs"] = battery(range(102, 110), "Q7.9",
    "Attentes vis-à-vis des acteurs de l'emploi (1→5)")

# ===================== Q8 — TERRITOIRE =====================
R["questions"]["Q8.1_facteurs_territoire"] = multi_counts(110, "Q8.1", [
    ("Offre de logement insuffisante/chère", "Offre de logement"),
    ("Offre de soins et de santé insuffisante", "Offre de soins"),
    ("Transports en commun / mobilité", "transports en commun"),
    ("Emploi du conjoint difficile", "emploi pour le conjoint"),
    ("Services à la personne (crèches, gardes)", "services à la personne"),
    ("Image du territoire peu attractive", "Image globale du territoire"),
    ("Animation culturelle/sportive/loisirs", "animation culturelle"),
    ("Aucun frein territorial", "Aucun frein territorial")])
R["questions"]["Q8.2_image_issoudun"] = scale_stats(111, "image Issoudun", "Q8.2")
R["questions"]["Q8.3_actions_collectives"] = multi_counts(112, "Q8.3", [
    ("Plateforme de recrutement mutualisée", "Plateforme de recrutement"),
    ("Promotion des métiers industriels (scolaires)", "promotion des métiers industriels"),
    ("Visites d'entreprises / portes ouvertes coordonnées", "Visites d'entreprises"),
    ("Campagne de communication territoriale commune", "Campagne de communication"),
    ("Groupement d'employeurs (temps partagé)", "Groupement d'employeurs"),
    ("Ateliers inter-entreprises bonnes pratiques RH", "Ateliers inter-entreprises"),
    ("Pas d'intérêt actuellement", "pas d'intérêt")])

# ===================== Q9 — PRIORITÉS GPECT =====================
R["questions"]["Q9.1_priorites_gpect"] = battery(range(113, 121), "Q9.1",
    "Priorités GPECT (1 faible → 5 très haute)")
R["questions"]["Q9.2_ateliers"] = multi_counts(121, "Q9.2", [
    ("Métiers sensibles & compétences clés", "Métiers sensibles et compétences"),
    ("Attractivité et recrutement territorial", "Attractivité et recrutement"),
    ("Formation & ingénierie pédagogique mutualisée", "Formation et ingénierie"),
    ("Transmission savoir-faire & seniors", "Transmission des savoir-faire et gestion"),
    ("Industrie 4.0 et compétences de demain", "Industrie 4.0"),
    ("Ne souhaite pas participer", "ne souhaite pas")])

# ===================== Champs texte libre : codage thématique =====================
def theme_count(idx, themes):
    s = df[cols[idx]].dropna().astype(str)
    n = int(s.shape[0])
    out = []
    for lab, pats in themes.items():
        mask = s.str.contains("|".join(pats), case=False, regex=True, na=False)
        out.append({"theme": lab, "n": int(mask.sum()), "pct": r1(100*mask.sum()/n)})
    out = sorted(out, key=lambda x: x["n"], reverse=True)
    return {"n_repondants": n, "themes": out}

R["questions"]["Q3.1_metiers_cles_themes"] = {"qid": "Q3.1", "type": "texte_libre_code",
    **theme_count(24, {
        "Soudure / chaudronnerie": [r"soud", r"chaudron"],
        "Usinage / réglage CN / mécanique": [r"usinage", r"r[eè]gleur", r"\bCN\b", r"m[eé]canic", r"forge", r"tour"],
        "Bureau d'études / méthodes / dessin / dévis": [r"bureau d.?[eé]tudes", r"m[eé]thode", r"dessin", r"deviseur", r"\bCAO\b", r"programmeur", r"industrialisation", r"ing[eé]nieur"],
        "Qualité / contrôle / HSE": [r"qualit", r"contr[oô]l", r"QHSE", r"\bHSE\b", r"certificat"],
        "Maintenance": [r"maintenance", r"[eé]lectrom[eé]ca"],
        "Conduite / transport / chauffeurs": [r"conducteur", r"chauffeur", r"\bcar\b", r"\bSPL\b", r"exploitant", r"routier"],
        "Logistique / magasinier / cariste": [r"logistique", r"magasin", r"cariste", r"approvision", r"supply"],
        "Encadrement / management": [r"chef d.?[eé]quipe", r"responsable", r"management", r"chef de projet", r"charg[eé] d.?affaire"],
        "R&D / ingénierie": [r"R&D", r"recherche", r"ing[eé]nieur"],
        "RH / support / gestion": [r"ressources humaines", r"\bRH\b", r"contr[oô]le de gestion", r"comptab", r"facturation", r"s[eé]dentaire"],
        "Maroquinerie / imprimerie (métiers spécifiques)": [r"maroquinier", r"imprimeur", r"graphiste", r"massicotier", r"plieur", r"viseur"],
        "Aucun métier en tension": [r"pas de m[eé]tier en tension"],
    })}
R["questions"]["Q4.6_postes_turnover_themes"] = {"qid": "Q4.6", "type": "texte_libre_code",
    **theme_count(54, {
        "Production / opérateurs": [r"production", r"op[eé]rateur"],
        "Conduite / transport": [r"conducteur", r"chauffeur", r"\bcar\b"],
        "Maintenance": [r"maintenance"],
        "Qualité / contrôle": [r"qualit", r"contr[oô]l"],
        "Bureau d'études / techniciens": [r"bureau d.?[eé]tudes", r"technicien", r"ing[eé]nieur"],
        "Réglage / usinage": [r"r[eé]gleur", r"usinage", r"plieur"],
        "Services supports": [r"support", r"services support"],
        "Logistique": [r"logistique"],
        "Métiers spécifiques (maroquinier, apprentissage)": [r"maroquinier", r"apprentis"],
        "Pas de turnover / RAS": [r"pas de turn", r"\bRAS\b", r"pas de secteur"],
    })}
R["questions"]["Q9.3_action_utile_themes"] = {"qid": "Q9.3", "type": "texte_libre_code",
    **theme_count(122, {
        "Attractivité / image / communication du territoire": [r"attractivit", r"image", r"visibilit", r"communication", r"atouts"],
        "Formation locale (ouverture, génie méca, jeunes)": [r"formation", r"g[eé]nie m[eé]canique", r"jeunes"],
        "Observatoire / identification des métiers en tension": [r"observatoire", r"m[eé]tiers", r"tension", r"identification"],
        "Forum / job dating / recrutement": [r"forum", r"job dating", r"recrutement"],
        "Lien acteurs emploi-formation-entreprises": [r"lien", r"acteurs", r"mutualisation"],
        "Stages / découverte scolaires": [r"stage", r"3[eè]me", r"2nde"],
        "Santé / sécurité / transport": [r"sant[eé]", r"m[eé]decin", r"s[eé]curit", r"transport"],
    })}
R["questions"]["Q9.4_remarques_themes"] = {"qid": "Q9.4", "type": "texte_libre_code",
    **theme_count(123, {
        "RAS / pas de remarque": [r"\bRAS\b", r"ras", r"pas de partage", r"concis"],
        "Constat : sujets connus mais pas d'action concrète": [r"pas d.?action concr", r"connues depuis"],
        "Vieillissement / attractivité des jeunes": [r"pyramide", r"attractivit[eé] des jeunes", r"jeunes"],
        "Disposition à coopérer / mutualiser (formations, jeunes)": [r"accompagner les jeunes", r"partag[eé]es", r"mobiliser les entreprises", r"partenariat"],
        "Faire connaître les métiers (écoles)": [r"se faire connaitre", r"[eé]coles"],
    })}

# ===================== Tableau récap des échelles =====================
recap = []
def push_scale(d, fam=None):
    if d.get("type") == "echelle_1_5":
        recap.append({"qid": d["qid"], "libelle": d.get("intitule", "")[:60],
                      "item": d.get("item", "—"), "moyenne": d["moyenne"],
                      "mediane": d["mediane"], "ecart_type": d["ecart_type"], "n": d["n"]})
    elif d.get("type") == "batterie_echelle_1_5":
        for it in d["items"]:
            recap.append({"qid": d["qid"], "libelle": d["intitule"][:60],
                          "item": it["item"], "moyenne": it["moyenne"],
                          "mediane": it["mediane"], "ecart_type": it["ecart_type"], "n": it["n"]})
for k, v in R["questions"].items():
    if isinstance(v, dict):
        push_scale(v)
R["recap_echelles"] = recap

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)

print("OK -> resultats_entreprises.json écrit.")
print("Périmètre :", N, "répondants | plus gros employeur = ligne interne", SAFRAN_IDX,
      "(effectif inscrit =", int(EFF.max()), ")")
print("Pyramide : base cohérente =", len(base_idx), "répondants | exclus =", excl)
print("Nb échelles dans le récap :", len(recap))
