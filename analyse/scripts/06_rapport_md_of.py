#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapport Markdown lisible depuis resultats_of.json (lecture seule)."""
import json
R=json.load(open("/home/user/Gpect/analyse/resultats/resultats_of.json",encoding="utf-8"))
q=R["questions"]; L=[]; w=L.append
m=R["_meta"]
w(f"# GPECT Issoudun — Résultats collège ORGANISMES DE FORMATION\n")
w(f"*Source : {m['source']} — {m['source_date']} · n={m['n_repondants']} · généré {m['genere_le']}*\n")
w(f"> ⚠️ {m['avertissement']}  \n> {m['note_option_B']} Le financeur n'est jamais nommé.\n")
w("*Tous les chiffres : `analyse/scripts/05_analyse_of.py`. Anonyme (ID OF01–OF07).*\n")

def cat(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · choix unique · n={d['n_repondants']}\n")
    w("| Modalité | n | % |\n|---|--:|--:|")
    for x in d["modalites"]: w(f"| {x['modalite']} | {x['n']} | {x['pct']} |")
def multi(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · multi-select (contains) · n={d['n_repondants']}\n")
    w("| Modalité | n | % rép. |\n|---|--:|--:|")
    for x in d["modalites"]:
        if x['n']>0: w(f"| {x['modalite']} | {x['n']} | {x['pct_repondants']} |")
def scale(d):
    sf=f" · **sans financeur : {d['sans_financeur']['moyenne']}** (n={d['sans_financeur']['n']})" if 'sans_financeur' in d else ""
    w(f"\n**{d['qid']} — {d['intitule']}** · échelle 1-5 · n={d['n']}{sf}\n")
    w("| moyenne | médiane | écart-type | min | max |\n|--:|--:|--:|--:|--:|")
    w(f"| {d['moyenne']} | {d['mediane']} | {d['ecart_type']} | {d['min']} | {d['max']} |")
def batt(d):
    ww='sans_financeur' in d['items'][0]
    w(f"\n**{d['qid']} — {d['intitule']}** · batterie 1-5 · {d['n_items']} items\n")
    head="| Item | moy | méd | éc-type | n |"+(" moy sans fin. |" if ww else "")
    w(head); w("|---|--:|--:|--:|--:|"+("--:|" if ww else ""))
    for it in d["classement_par_moyenne"]:
        extra=f" {it['sans_financeur']['moyenne']} |" if ww else ""
        w(f"| {it['item']} | {it['moyenne']} | {it['mediane']} | {it['ecart_type']} | {it['n']} |{extra}")
def num(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · numérique · valeurs={d['valeurs_numeriques']}"
      f" · médiane {d['mediane']} · [{d['min']}–{d['max']}]"
      + (f" · non num. : {d['valeurs_non_numeriques']}" if d['valeurs_non_numeriques'] else "")+"\n")
def txt(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · texte libre (verbatims anonymisés) · n={d['n_repondants']}\n")
    for v in d["verbatims_anonymises"]: w(f"- « {v} »")

disp={"choix_unique":cat,"multi_select":multi,"echelle_1_5":scale,"batterie_echelle_1_5":batt,
      "numerique":num,"texte_libre":txt}
sections={
 "Q0 — Identité de l'organisme":["Q0.7_type","Q0.8_qualiopi","Q0.9_cpf","Q0.10_perimetre","Q0.11_presence_issoudun"],
 "Q1 — Offre, capacité, moyens":["Q1.1_publics","Q1.2_type_formations","Q1.3_niveaux","Q1.4_capacite",
    "Q1.5_formateurs_internes","Q1.6_formateurs_externes","Q1.7_plateaux","Q1.8_equipements"],
 "Q2 — Niveau de l'offre & compétences émergentes":["Q2.1_niveau_offre","Q2.2_capacite_emergentes","Q2.3_sur_mesure"],
 "Q3 — Connaissance des besoins":["Q3.1_connaissance_besoins","Q3.2_sources","Q3.3_connaissance_secteurs","Q3.4_metiers_tension"],
 "Q4 — Adéquation de l'offre":["Q4.1_offre_couvre","Q4.2_retours_clients","Q4.3_points_inadaptes","Q4.4_metiers_a_adapter"],
 "Q5 — AFEST & adaptation":["Q5.1_afest_concu","Q5.2_maitrise_afest","Q5.3_freins_afest","Q5.4_formes_adaptation","Q5.5_pret_evoluer"],
 "Q6 — Coopération":["Q6.1_cooperation","Q6.2_acteurs","Q6.3_formes_coop","Q6.4_actions_collectives"],
 "Q7 — Freins & leviers":["Q7.1_freins_offre","Q7.2_leviers"],
 "Q8 — Prospective":["Q8.1_anticipation_besoins","Q8.2_domaines_evolutions","Q8.3_nouvelles_formations","Q8.5_transfo_internes"],
 "Q9 — Priorités & rôles GPECT":["Q9.1_priorites_gpect","Q9.2_roles","Q9.3_ateliers"],
 "Q10 — Territoire & attractivité":["Q10.1_image","Q10.2_freins_territoire","Q10.3_actions_attractivite"],
 "Q11 — Ouverture":["Q11.1_action_utile","Q11.3_souhaite_synthese","Q11.4_observations"],
}
for sec,keys in sections.items():
    w(f"\n\n## {sec}")
    for k in keys:
        d=q[k]; disp[d["type"]](d)

w("\n\n## Récapitulatif — échelles 1-5")
w("\n| Q | Item | moy | méd | éc-type | n | moy sans financeur |\n|---|---|--:|--:|--:|--:|--:|")
for x in sorted(R["recap_echelles"],key=lambda z:(z["qid"],-(z["moyenne"] or 0))):
    w(f"| {x['qid']} | {x['item']} | {x['moyenne']} | {x['mediane']} | {x['ecart_type']} | {x['n']} | {x.get('moy_sans_financeur','—')} |")

open("/home/user/Gpect/analyse/resultats/resultats_of_rapport.md","w",encoding="utf-8").write("\n".join(L))
print("OK ->",len(L),"lignes")
