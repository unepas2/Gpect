#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère un rapport Markdown lisible à partir de resultats_entreprises.json.
Aucun recalcul : lecture seule du JSON figé."""
import json

J = "/home/user/Gpect/analyse/resultats/resultats_entreprises.json"
MD = "/home/user/Gpect/analyse/resultats/resultats_entreprises_rapport.md"
R = json.load(open(J, encoding="utf-8"))
q = R["questions"]
L = []
def w(s=""): L.append(s)

m = R["_meta"]
w(f"# GPECT Issoudun — Résultats collège ENTREPRISES")
w(f"\n*Source : {m['source']} — {m['source_date']} · n={m['n_repondants']} répondants · "
  f"généré le {m['genere_le']}*")
w(f"\n*Méthode : {m['regles']}. Tous les chiffres sont produits par script "
  f"(`analyse/scripts/02_analyse_entreprises.py`) — aucun calcul manuel.*")
w("\n> **Anonymat** : aucun nom n'apparaît. Le « plus gros employeur » (≈1550 sal.) "
  "est traité en interne pour l'effet de poids et n'est jamais nommé.")

def fmt_cat(d):
    w(f"\n**{d['qid']} — {d['intitule']}**  · *choix unique* · n={d['n_repondants']}\n")
    w("| Modalité | n | % |")
    w("|---|--:|--:|")
    for x in d["modalites"]:
        w(f"| {x['modalite']} | {x['n']} | {x['pct']} |")

def fmt_multi(d):
    w(f"\n**{d['qid']} — {d['intitule']}**  · *choix multiple (comptage par mot-clé)* · n={d['n_repondants']}\n")
    w("| Modalité | n | % des répondants |")
    w("|---|--:|--:|")
    for x in d["modalites"]:
        w(f"| {x['modalite']} | {x['n']} | {x['pct_repondants']} |")

def fmt_num(d):
    w(f"\n**{d['qid']} — {d['intitule']}**  · *numérique* · n={d['n']}"
      + (f" (exclus non num. : {d['valeurs_non_numeriques']})" if d['n_non_numerique_exclus'] else "") + "\n")
    w("| | somme | moyenne | médiane | min | max |")
    w("|---|--:|--:|--:|--:|--:|")
    w(f"| Tous (n={d['n']}) | {d['somme']} | {d['moyenne']} | {d['mediane']} | {d['min']} | {d['max']} |")
    if "sans_plus_gros" in d:
        s = d["sans_plus_gros"]
        w(f"| Sans plus gros employeur (n={s['n']}) | {s['somme']} | {s['moyenne']} | {s['mediane']} | — | {s['max']} |")

def fmt_scale(d):
    w(f"\n**{d['qid']} — {d['intitule']}**  · *échelle 1-5* · n={d['n']}\n")
    w("| moyenne | médiane | écart-type | min | max |")
    w("|--:|--:|--:|--:|--:|")
    w(f"| {d['moyenne']} | {d['mediane']} | {d['ecart_type']} | {d['min']} | {d['max']} |")

def fmt_batt(d):
    w(f"\n**{d['qid']} — {d['intitule']}**  · *batterie échelle 1-5* · {d['n_items']} items "
      f"(classés par moyenne décroissante)\n")
    w("| Item | moyenne | médiane | écart-type | n |")
    w("|---|--:|--:|--:|--:|")
    for it in d["classement_par_moyenne"]:
        w(f"| {it['item']} | {it['moyenne']} | {it['mediane']} | {it['ecart_type']} | {it['n']} |")

def fmt_txt(d):
    w(f"\n**{d['qid']} — champ texte libre (codage thématique, verbatims anonymisés)** · n={d['n_repondants']}\n")
    w("| Thème | n | % |")
    w("|---|--:|--:|")
    for t in d["themes"]:
        if t["n"] > 0:
            w(f"| {t['theme']} | {t['n']} | {t['pct']} |")

sections = {
    "Q0 — Identité & profil juridique": ["Q0.8_statut"],
    "Q1 — Profil de l'entreprise": ["Q1.1_secteur","Q1.3_effectif_tranche","Q1.4_effectif_inscrit",
        "Q1.5_recours_externes","Q1.6_volume_interim_ETP","Q1.7_volume_prestation","Q1.8_age_dirigeant"],
    "Q2 — Stratégie & anticipation": ["Q2.1_preoccupations","Q2.2_transmission","Q2.3_evolution_effectifs",
        "Q2.4_investissements","Q2.5_invest_competences"],
    "Q3 — Métiers clés & tensions": ["Q3.1_metiers_cles_themes","Q3.2_tension","Q3.3_causes_tensions",
        "Q3.4_metiers_sensibles","Q3.5_facteurs_transformation"],
    "Q4 — Démographie, turnover & transmission": ["Q4.2_retraite_2ans","Q4.3_retraite_5ans",
        "Q4.4_services_retraite","Q4.5_turnover","Q4.6_postes_turnover_themes","Q4.7_motifs_depart",
        "Q4.8_dispositifs_transmission","Q4.8b_besoin_transmission"],
    "Q5 — Recrutement": ["Q5.1_recrutements_2024_2025","Q5.2_difficulte","Q5.3_freins_recrutement",
        "Q5.4_recrut_prevus_3ans","Q5.5_motivation_recrut","Q5.6_actions_attractivite"],
    "Q6 — Compétences": ["Q6.1_tech_adaptees","Q6.2_tech_manquantes","Q6.3_savoiretre_adaptes",
        "Q6.4_savoiretre_renforcer","Q6.5_competences_3_5ans"],
    "Q7 — Formation & coopération": ["Q7.1_formations_organisees","Q7.2_connaissance_opco",
        "Q7.3_freins_formation","Q7.4_alternance","Q7.5_alternants_territoire","Q7.6_offre_adaptee",
        "Q7.7_raisons_inadequation","Q7.8_cooperation_acteurs","Q7.9_attentes_acteurs"],
    "Q8 — Territoire & attractivité": ["Q8.1_facteurs_territoire","Q8.2_image_issoudun","Q8.3_actions_collectives"],
    "Q9 — Priorités GPECT": ["Q9.1_priorites_gpect","Q9.2_ateliers","Q9.3_action_utile_themes","Q9.4_remarques_themes"],
}
disp = {"choix_unique": fmt_cat, "multi_select": fmt_multi, "numerique": fmt_num,
        "echelle_1_5": fmt_scale, "batterie_echelle_1_5": fmt_batt, "texte_libre_code": fmt_txt}

for sec, keys in sections.items():
    w(f"\n\n## {sec}")
    for k in keys:
        d = q[k]
        disp[d["type"]](d)

# pyramide
p = q["Q4.1_pyramide"]
w("\n\n## Q4.1 — Pyramide des âges (effet de poids)")
w(f"\n*{p['note']}*\n")
w("| Base | n | Total têtes | <30 | 31-44 | 45-59 | 60+ | Seniors 45+ | % femmes |")
w("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
for tag, lab in [("AVEC_plus_gros","AVEC plus gros employeur"),("SANS_plus_gros","SANS plus gros employeur")]:
    a = p[tag]
    w(f"| {lab} | {a['n_repondants']} | {a['total_tetes']} | "
      f"{a['tranche_moins30']} ({a['pct_moins30']}%) | {a['tranche_31_44']} ({a['pct_31_44']}%) | "
      f"{a['tranche_45_59']} ({a['pct_45_59']}%) | {a['tranche_60plus']} ({a['pct_60plus']}%) | "
      f"{a['seniors_45plus']} ({a['pct_seniors_45plus']}%) | {a['pct_femmes']} |")

# récap échelles
w("\n\n## Tableau récapitulatif — toutes les échelles 1-5")
w("\n| Q | Item | moy | méd | éc.-type | n |")
w("|---|---|--:|--:|--:|--:|")
for x in sorted(R["recap_echelles"], key=lambda z: (z["qid"], -(z["moyenne"] or 0))):
    w(f"| {x['qid']} | {x['item']} | {x['moyenne']} | {x['mediane']} | {x['ecart_type']} | {x['n']} |")

open(MD, "w", encoding="utf-8").write("\n".join(L))
print("OK ->", MD, "(", len(L), "lignes )")
