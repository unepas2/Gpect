# -*- coding: utf-8 -*-
"""ETAPE 1 — Lecture structurelle collège Organismes de formation (OF). Aucun calcul d'analyse."""
import pandas as pd
SRC = "/root/.claude/uploads/c81e9d0c-8492-5a42-b5cc-973534e42748/fa1196a1-02_organismes_formation.xlsx.xlsx"
xl = pd.ExcelFile(SRC, engine="openpyxl")
print("FEUILLES :", xl.sheet_names)
print("=" * 78)
df = pd.read_excel(SRC, sheet_name=xl.sheet_names[0], engine="openpyxl")
print(f"DIMENSIONS BRUTES : {df.shape[0]} lignes x {df.shape[1]} colonnes")
n_vides = df.isna().all(axis=1).sum()
print(f"Lignes entierement vides : {n_vides} | repondants potentiels : {df.shape[0]-n_vides} | doublons stricts : {df.duplicated().sum()}")
print("=" * 78)
for i, c in enumerate(df.columns):
    nn = int(df[c].notna().sum()); nu = int(df[c].nunique(dropna=True))
    print(f"[{i:02d}] {str(c).replace(chr(10),' ').strip()}")
    print(f"      dtype={df[c].dtype} | remplis={nn}/{len(df)} | uniques={nu}")
