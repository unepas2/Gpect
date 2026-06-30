#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 1 — Lecture & contrôle, collège ORGANISMES DE FORMATION.
Aucun calcul d'indicateur. Périmètre attendu : 7 répondants."""
import pandas as pd
pd.set_option("display.max_colwidth", 120); pd.set_option("display.width", 200)

PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/677aa4a6-02_organismes_formation.xlsx.xlsx"
xls = pd.ExcelFile(PATH, engine="openpyxl")
print("FEUILLES :", xls.sheet_names)
df = pd.read_excel(PATH, sheet_name=xls.sheet_names[0], engine="openpyxl", dtype=object)
print(f"\nDIMENSIONS BRUTES : {df.shape[0]} lignes x {df.shape[1]} colonnes")
empty = df.isna().all(axis=1)
print("Lignes 100% vides :", int(empty.sum()), list(df.index[empty]) if empty.any() else "")
df = df[~empty].copy()
print(f"DIMENSIONS APRÈS retrait vides : {df.shape[0]} lignes x {df.shape[1]} colonnes")
print("Doublons stricts :", int(df.duplicated().sum()))

print("\n=== COLONNES (index | remplissage | intitulé) ===")
for i, c in enumerate(df.columns):
    nn = int(df[c].notna().sum())
    print(f"[{i:02d}] {nn:>2}/{df.shape[0]} | {str(c).replace(chr(10),' ').strip()}")

print("\n=== APERÇU : valeurs non nulles de chaque colonne (contrôle décalage) ===")
for i, c in enumerate(df.columns):
    vals = df[c].dropna().astype(str).head(4).tolist()
    vals = [v.replace("\n"," ")[:70] for v in vals]
    print(f"[{i:02d}] {str(c).replace(chr(10),' ').strip()[:55]!r}")
    for v in vals: print(f"       - {v}")
