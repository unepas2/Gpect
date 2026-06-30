#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÉTAPE 1 (suite) — Contrôle des valeurs : bornes des échelles 1-5 et
cohérence des colonnes numériques. AUCUN indicateur calculé.
"""
import pandas as pd

PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/126d3b2d-01_entreprises.xlsx.xlsx"
df = pd.read_excel(PATH, engine="openpyxl", dtype=object)

cols = list(df.columns)

# Colonnes "échelle 1-5" = celles dont l'intitulé contient un barème explicite
likert_idx = [i for i, c in enumerate(cols) if any(
    k in str(c) for k in ["1 = Faible", "1 = Pas du tout", "1 = Très faible",
                           "= Fort impact", "Faible impact", "Très haute priorité",
                           "Très forte attente", "Très bien mis en place"])]
# On ajoute aussi les échelles isolées repérées par leur intitulé
extra_scale = [72, 94, 111]  # Q5.2 difficulté, Q7.6 adéquation offre, Q8.2 image
likert_idx = sorted(set(likert_idx + extra_scale))

print("=" * 78)
print("CONTRÔLE ÉCHELLES 1-5  (valeurs hors bornes ?)")
print("=" * 78)
print("Nb de colonnes-échelle détectées :", len(likert_idx))
any_oob = False
for i in likert_idx:
    s = df[cols[i]].dropna()
    num = pd.to_numeric(s, errors="coerce")
    non_num = s[num.isna()]
    oob = num[(num < 1) | (num > 5)]
    flags = []
    if len(non_num):
        flags.append(f"NON-NUM={list(non_num.astype(str).unique())}")
    if len(oob):
        flags.append(f"HORS 1-5={sorted(oob.unique().tolist())}")
    if flags:
        any_oob = True
        print(f"  [!] [{i:03d}] {str(cols[i])[:55]!r:57s} -> " + " ; ".join(flags))
if not any_oob:
    print("  OK : toutes les colonnes-échelle ne contiennent que des entiers 1..5 (hors vides).")

print("\n" + "=" * 78)
print("CONTRÔLE COLONNES NUMÉRIQUES (effectifs, départs, volumes)")
print("=" * 78)
num_idx = [14, 16, 17, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 81]
for i in num_idx:
    s = df[cols[i]].dropna()
    num = pd.to_numeric(s, errors="coerce")
    non_num = s[num.isna()]
    numd = num.dropna()
    dec_mask = numd.apply(lambda x: float(x) != int(x))
    dec_vals = sorted(numd[dec_mask].unique().tolist()) if dec_mask.any() else []
    info = f"n_rempli={len(s):>2d}"
    if len(non_num):
        info += f" | NON-NUM={list(non_num.astype(str).unique())}"
    if dec_vals:
        info += f" | DÉCIMAUX={dec_vals}"
    print(f"  [{i:03d}] {str(cols[i])[:48]!r:50s} {info}")

print("\n" + "=" * 78)
print("IDENTIFICATION DU PLUS GROS EMPLOYEUR (contrôle effet de poids)")
print("=" * 78)
eff = pd.to_numeric(df[cols[14]], errors="coerce")
top = eff.sort_values(ascending=False).head(3)
for idx, v in top.items():
    # rang neutre, on n'affiche pas le nom dans les résultats finaux ;
    # ici contrôle interne uniquement
    print(f"  ligne {idx} -> effectif inscrit (Q1.4) = {v}")
print("  Somme effectif inscrit (Q1.4), toutes lignes :", int(eff.sum()))
print("  Part du plus gros dans la somme : %.1f%%" % (100*top.iloc[0]/eff.sum()))
