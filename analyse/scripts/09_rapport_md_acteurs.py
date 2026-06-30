#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapport Markdown depuis resultats_acteurs.json (lecture seule)."""
import json
R=json.load(open("/home/user/Gpect/analyse/resultats/resultats_acteurs.json",encoding="utf-8"))
q=R["questions"]; L=[]; w=L.append; m=R["_meta"]
w(f"# GPECT Issoudun — Résultats collège ACTEURS DE L'EMPLOI\n")
w(f"*Source : {m['source']} — {m['source_date']} · n={m['n_repondants']} · généré {m['genere_le']}*\n")
w(f"> ⚠️ {m['avertissement']}\n> Composition : {m['composition']}. Colonnes « i » = moyenne intérim (n=3), « p » = moyenne opérateurs publics (n=4) — **à n si faible, purement indicatif**.\n")
w("*Chiffres : `analyse/scripts/08_analyse_acteurs.py`. Anonyme (AC01–AC07).*\n")
def cat(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · choix unique · n={d['n_repondants']}\n\n| Modalité | n | % |\n|---|--:|--:|")
    for x in d["modalites"]: w(f"| {x['modalite']} | {x['n']} | {x['pct']} |")
def multi(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · multi-select · n={d['n_repondants']}\n\n| Modalité | n | % rép. |\n|---|--:|--:|")
    for x in d["modalites"]: w(f"| {x['modalite']} | {x['n']} | {x['pct_repondants']} |")
def scale(d):
    w(f"\n**{d['qid']} — {d['item']}** · échelle 1-5 · n={d['n']}\n\n| moy | méd | éc-type | min | max | i | p |\n|--:|--:|--:|--:|--:|--:|--:|")
    w(f"| {d['moyenne']} | {d['mediane']} | {d['ecart_type']} | {d['min']} | {d['max']} | {d['moy_interim']} | {d['moy_public']} |")
def batt(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · batterie 1-5 ({d['n_items']} items)\n\n| Item | moy | méd | éc-type | i | p |\n|---|--:|--:|--:|--:|--:|")
    for it in d["classement_par_moyenne"]:
        w(f"| {it['item']} | {it['moyenne']} | {it['mediane']} | {it['ecart_type']} | {it['moy_interim']} | {it['moy_public']} |")
disp={"choix_unique":cat,"multi_select":multi,"echelle_1_5":scale,"batterie_echelle_1_5":batt}
order=["Q0.1_type","Q0.2_conseillers","Q0.3_volume_accompagnes","Q1.1_publics","Q1.2_importance_publics",
 "Q1.3_qualif_dominante","Q2.1_adequation_profils","Q2.2_facteurs_inadequation","Q3.1_difficulte_competences",
 "Q4.1_freins_acces_emploi","Q5.1_usage_dispositifs","Q5.2_efficacite_dispositifs","Q5.3_duree_emplois",
 "Q6.1_offre_locale","Q6.2_manque_formation","Q7.1_cooperation","Q8.1_importance_actions",
 "Q8.2_participation","Q8.3_interet_ateliers"]
w("\n## Résultats question par question")
for k in order:
    d=q[k]; disp[d["type"]](d)
w("\n\n## Récapitulatif — toutes les échelles (avec éclairage intérim/public)")
w("\n| Q | Item | moy | méd | éc-type | n | intérim | public |\n|---|---|--:|--:|--:|--:|--:|--:|")
for x in sorted(R["recap_echelles"],key=lambda z:(z["qid"],-(z["moyenne"] or 0))):
    w(f"| {x['qid']} | {x['item']} | {x['moyenne']} | {x['mediane']} | {x['ecart_type']} | {x['n']} | {x['moy_interim']} | {x['moy_public']} |")
open("/home/user/Gpect/analyse/resultats/resultats_acteurs_rapport.md","w",encoding="utf-8").write("\n".join(L))
print("OK ->",len(L),"lignes")
