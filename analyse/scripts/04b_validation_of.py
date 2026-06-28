#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 1 (suite) — contrôle valeurs collège OF. Pas d'indicateur."""
import pandas as pd
PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/677aa4a6-02_organismes_formation.xlsx.xlsx"
df = pd.read_excel(PATH, engine="openpyxl", dtype=object)
cols = list(df.columns)

scale_idx = list(range(23, 43)) + [44] + list(range(46, 54)) + [55, 56, 61, 67, 76] + list(range(81, 89)) + [91]
print("CONTRÔLE ÉCHELLES 1-5 (", len(scale_idx), "colonnes )")
oob = False
for i in scale_idx:
    s = df[cols[i]].dropna()
    num = pd.to_numeric(s, errors="coerce")
    nn = s[num.isna()]
    bad = num[(num < 1) | (num > 5)]
    if len(nn) or len(bad):
        oob = True
        print(f"  [!] [{i}] {str(cols[i])[:50]} non_num={list(nn.astype(str))} hors={sorted(bad.unique().tolist())}")
print("  OK bornes 1-5" if not oob else "  -> anomalies ci-dessus")

print("\nNUMÉRIQUES (7 valeurs) :")
for i in [19, 20]:
    print(f"  [{i}] {str(cols[i])[:45]} : {df[cols[i]].astype(str).tolist()}")

print("\nTYPE D'ORGANISME (Q0.7) — 7 valeurs :")
for v in df[cols[9]].astype(str).tolist():
    print("   -", v[:90])
print("\nQ0.7 autre / Q0.8 Qualiopi / Q0.9 CPF / Q1.4 capacité :")
for lab, i in [("Qualiopi",11),("CPF",12),("Capacité",18)]:
    print(f"  {lab}: {df[cols[i]].astype(str).tolist()}")
