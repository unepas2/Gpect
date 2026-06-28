# -*- coding: utf-8 -*-
"""
ETAPE 1 — Lecture STRUCTURELLE + controle qualite du fichier Entreprises.
Aucun calcul d'analyse. On annonce dimensions + colonnes + anomalies, on attend validation.
"""
import pandas as pd

SRC = "/root/.claude/uploads/c81e9d0c-8492-5a42-b5cc-973534e42748/8ffdf5f0-01_entreprises.xlsx.xlsx"

xl = pd.ExcelFile(SRC, engine="openpyxl")
print("FEUILLES :", xl.sheet_names)
print("=" * 78)

df = pd.read_excel(SRC, sheet_name=xl.sheet_names[0], engine="openpyxl")
print(f"DIMENSIONS BRUTES : {df.shape[0]} lignes x {df.shape[1]} colonnes")

n_vides = df.isna().all(axis=1).sum()
print(f"Lignes entierement vides : {n_vides}")
print(f"Lignes non vides (repondants potentiels) : {df.shape[0] - n_vides}")
# doublons stricts
print(f"Lignes dupliquees strictes : {df.duplicated().sum()}")
print("=" * 78)
print("COLONNES (index | intitule) | dtype | remplis | vides | n_uniques")
print("-" * 78)
for i, c in enumerate(df.columns):
    nn = int(df[c].notna().sum()); nv = int(df[c].isna().sum()); nu = int(df[c].nunique(dropna=True))
    label = str(c).replace("\n", " ").strip()
    print(f"[{i:02d}] {label}")
    print(f"      dtype={df[c].dtype} | remplis={nn} | vides={nv} | uniques={nu}")
