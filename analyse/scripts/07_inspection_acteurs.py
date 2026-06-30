#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 1 — Lecture & contrôle, collège ACTEURS DE L'EMPLOI. Aucun calcul. n attendu=7."""
import pandas as pd
pd.set_option("display.max_colwidth",120); pd.set_option("display.width",200)
PATH="/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/eb78e3b2-03_acteurs_emploi.xlsx.xlsx"
xls=pd.ExcelFile(PATH,engine="openpyxl"); print("FEUILLES :",xls.sheet_names)
df=pd.read_excel(PATH,sheet_name=xls.sheet_names[0],engine="openpyxl",dtype=object)
print(f"\nDIMENSIONS BRUTES : {df.shape[0]} lignes x {df.shape[1]} colonnes")
empty=df.isna().all(axis=1); print("Lignes 100% vides :",int(empty.sum()),list(df.index[empty]) if empty.any() else "")
df=df[~empty].copy()
print(f"APRÈS retrait vides : {df.shape[0]} x {df.shape[1]} | doublons stricts : {int(df.duplicated().sum())}")
print("\n=== COLONNES (index | remplissage | intitulé) ===")
for i,c in enumerate(df.columns):
    print(f"[{i:02d}] {int(df[c].notna().sum()):>2}/{df.shape[0]} | {str(c).replace(chr(10),' ').strip()}")
print("\n=== APERÇU valeurs (contrôle décalage) ===")
for i,c in enumerate(df.columns):
    vals=[v.replace('\n',' ')[:70] for v in df[c].dropna().astype(str).head(4).tolist()]
    print(f"[{i:02d}] {str(c).replace(chr(10),' ').strip()[:55]!r}")
    for v in vals: print("       -",v)
