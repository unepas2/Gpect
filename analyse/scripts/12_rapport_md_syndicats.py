#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapport Markdown depuis resultats_syndicats.json (lecture seule)."""
import json
R=json.load(open("/home/user/Gpect/analyse/resultats/resultats_syndicats.json",encoding="utf-8"))
q=R["questions"]; L=[]; w=L.append; m=R["_meta"]
w("# GPECT Issoudun — Résultats collège SYNDICATS / ORGANISATIONS PROFESSIONNELLES\n")
w(f"*Source : {m['source']} — {m['source_date']} · n={m['n_repondants']} · généré {m['genere_le']}*\n")
w(f"> ⚠️ {m['avertissement']}\n> Composition interne : {m['composition_interne']}. {m['note_option_1']}\n")
w("*Chiffres : `analyse/scripts/11_analyse_syndicats.py`. Anonyme (SY01–SY07).*\n")
def cat(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · choix unique · n={d['n_repondants']}\n\n| Modalité | n | % |\n|---|--:|--:|")
    for x in d["modalites"]: w(f"| {x['modalite']} | {x['n']} | {x['pct']} |")
def multi(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · multi-select · n={d['n_repondants']}\n\n| Modalité | n | % |\n|---|--:|--:|")
    for x in d["modalites"]:
        if x['n']>0: w(f"| {x['modalite']} | {x['n']} | {x['pct_repondants']} |")
def scale(d):
    w(f"\n**{d['qid']} — {d['item']}** · échelle 1-5 · n={d['n']} · moy {d['moyenne']} · méd {d['mediane']} · éc-type {d['ecart_type']} · [{d['min']}-{d['max']}]\n")
def tcode(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · texte libre codé · n={d['n_repondants']}\n\n| Thème | n | % |\n|---|--:|--:|")
    for t in d["themes"]:
        if t['n']>0: w(f"| {t['theme']} | {t['n']} | {t['pct']} |")
    w("\n*Verbatims (anonymisés) :*")
    for v in d["verbatims_anonymises"]: w(f"- « {v} »")
def verb(d):
    w(f"\n**{d['qid']} — {d['intitule']}** · texte libre · n={d['n_repondants']}\n\n*Verbatims (anonymisés) :*")
    for v in d["verbatims_anonymises"]: w(f"- « {v} »")
disp={"choix_unique":cat,"multi_select":multi,"echelle_1_5":scale,"texte_libre_code":tcode,"texte_libre":verb}
order=list(q.keys())
w("\n## Résultats question par question")
for k in order:
    disp[q[k]["type"]](q[k])
w("\n\n## Récapitulatif — échelles 1-5")
w("\n| Q | Item | moy | méd | éc-type | n |\n|---|---|--:|--:|--:|--:|")
for x in R["recap_echelles"]:
    w(f"| {x['qid']} | {x['item']} | {x['moyenne']} | {x['mediane']} | {x['ecart_type']} | {x['n']} |")
open("/home/user/Gpect/analyse/resultats/resultats_syndicats_rapport.md","w",encoding="utf-8").write("\n".join(L))
print("OK ->",len(L),"lignes")
