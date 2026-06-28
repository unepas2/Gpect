#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 2 (exploration) collège OF : valeurs complètes multi-select + texte libre."""
import pandas as pd
PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/677aa4a6-02_organismes_formation.xlsx.xlsx"
df = pd.read_excel(PATH, engine="openpyxl", dtype=object)
cols = list(df.columns)

# repérage du financeur (non-dispensateur)
fin = df[cols[9]].astype(str).str.contains("Collectivit|financeur", case=False, na=False)
print("Ligne(s) financeur/non-dispensateur :", list(df.index[fin]), "\n")

multi = {13:"Q0.10 intervient sur",15:"Q1.1 publics",16:"Q1.2 type formations",17:"Q1.3 niveaux",
         45:"Q3.2 sources besoins",57:"Q4.3 points inadaptés",62:"Q5.3 freins AFEST",
         64:"Q5.4 formes adaptation",68:"Q6.2 acteurs",70:"Q6.3 formes coop",73:"Q7.1 freins offre",
         75:"Q7.2 leviers",77:"Q8.2 domaines évolutions",80:"Q8.5 transfo internes",
         89:"Q9.2 rôles GPECT",90:"Q9.3 ateliers",92:"Q10.2 freins territoire",93:"Q10.3 actions attractivité"}
print("="*70,"\nMULTI-SELECT — valeurs complètes (7 lignes)\n","="*70)
for i,lab in multi.items():
    print(f"\n--- [{i}] {lab}")
    for v in df[cols[i]].dropna().astype(str).tolist():
        print("   •", v)

freetext = {22:"Q1.8 équipements",54:"Q3.4 métiers tension",59:"Q4.4 métiers à adapter",
            72:"Q6.5 actions collectives rôle",94:"Q11.1 action utile",95:"Q11.2 acteur à associer",
            97:"Q11.4 observations"}
print("\n",  "="*70,"\nTEXTE LIBRE\n","="*70)
for i,lab in freetext.items():
    print(f"\n--- [{i}] {lab} (n={df[cols[i]].notna().sum()})")
    for v in df[cols[i]].dropna().astype(str).tolist():
        print("   »", v)
