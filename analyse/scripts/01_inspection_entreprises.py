#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÉTAPE 1 — Lecture & contrôle du fichier Entreprises (collège Entreprises).
AUCUN calcul d'indicateur ici : on lit, on décrit, on contrôle le périmètre,
on cherche les anomalies (lignes vides, doublons, décalages de colonnes,
encodage, valeurs hors échelle évidentes). On s'arrête ensuite.

Périmètre attendu : 21 répondants.
"""
import sys
import pandas as pd

PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/126d3b2d-01_entreprises.xlsx.xlsx"

pd.set_option("display.max_colwidth", 120)
pd.set_option("display.width", 200)

# --- 1. Lister les feuilles du classeur -------------------------------------
xls = pd.ExcelFile(PATH, engine="openpyxl")
print("=" * 78)
print("FEUILLES DU CLASSEUR :", xls.sheet_names)
print("=" * 78)

# Charger la première feuille telle quelle (en-tête = ligne 0 par défaut)
df = pd.read_excel(PATH, sheet_name=xls.sheet_names[0], engine="openpyxl", dtype=object)

print("\nDIMENSIONS BRUTES (avant nettoyage) : %d lignes x %d colonnes"
      % (df.shape[0], df.shape[1]))

# --- 2. Lignes entièrement vides --------------------------------------------
all_empty = df.isna().all(axis=1)
n_empty = int(all_empty.sum())
print("Lignes entièrement vides :", n_empty)
if n_empty:
    print("  -> indices (0-based) des lignes vides :", list(df.index[all_empty]))

df_clean = df[~all_empty].copy()
print("\nDIMENSIONS APRÈS retrait des lignes 100%% vides : %d lignes x %d colonnes"
      % (df_clean.shape[0], df_clean.shape[1]))

# --- 3. Liste complète des colonnes -----------------------------------------
print("\n" + "=" * 78)
print("LISTE COMPLÈTE DES COLONNES (index : intitulé)")
print("=" * 78)
for i, c in enumerate(df.columns):
    label = str(c).replace("\n", " ").strip()
    print(f"[{i:02d}] {label}")

# --- 4. Taux de remplissage par colonne -------------------------------------
print("\n" + "=" * 78)
print("TAUX DE REMPLISSAGE PAR COLONNE (sur lignes non vides, n=%d)" % df_clean.shape[0])
print("=" * 78)
for i, c in enumerate(df_clean.columns):
    non_null = int(df_clean[c].notna().sum())
    pct = 100.0 * non_null / df_clean.shape[0] if df_clean.shape[0] else 0
    label = str(c).replace("\n", " ").strip()
    print(f"[{i:02d}] {non_null:>3d}/{df_clean.shape[0]} ({pct:5.1f}%)  {label[:80]}")

# --- 5. Aperçu des premières cellules de chaque colonne (contrôle décalage) --
print("\n" + "=" * 78)
print("APERÇU : 3 premières valeurs non nulles de chaque colonne (contrôle décalage)")
print("=" * 78)
for i, c in enumerate(df_clean.columns):
    vals = df_clean[c].dropna().astype(str).head(3).tolist()
    vals = [v.replace("\n", " ")[:60] for v in vals]
    label = str(c).replace("\n", " ").strip()[:55]
    print(f"[{i:02d}] {label!r}")
    for v in vals:
        print(f"       - {v}")

# --- 6. Doublons potentiels --------------------------------------------------
print("\n" + "=" * 78)
print("CONTRÔLE DOUBLONS")
print("=" * 78)
dup_full = int(df_clean.duplicated().sum())
print("Lignes strictement identiques (toutes colonnes) :", dup_full)

# --- 7. Types de données détectés -------------------------------------------
print("\n" + "=" * 78)
print("TYPES INFÉRÉS PAR COLONNE (échantillon de valeurs uniques)")
print("=" * 78)
for i, c in enumerate(df_clean.columns):
    uniq = df_clean[c].dropna().unique()
    nuniq = len(uniq)
    sample = [str(u).replace("\n", " ")[:40] for u in uniq[:6]]
    label = str(c).replace("\n", " ").strip()[:50]
    print(f"[{i:02d}] {label!r:55s} | valeurs uniques={nuniq:>3d} | ex: {sample}")
