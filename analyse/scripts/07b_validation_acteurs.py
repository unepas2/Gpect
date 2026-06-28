#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 1 (suite) — contrôle valeurs collège Acteurs de l'emploi. Pas d'indicateur."""
import pandas as pd
PATH="/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/eb78e3b2-03_acteurs_emploi.xlsx.xlsx"
df=pd.read_excel(PATH,engine="openpyxl",dtype=object); cols=list(df.columns)

# toutes les colonnes d'échelle/single 1-5 : 8..14, 16, 17..23, 24..35, 36..43, 44..51, 52, 53, 54..64, 65..69, 70..75, 76..82, 83..87
scale_idx=list(range(8,15))+[16]+list(range(17,24))+list(range(24,36))+list(range(36,44))+\
          list(range(44,52))+[52,53]+list(range(54,65))+list(range(65,70))+list(range(70,76))+\
          list(range(76,83))+list(range(83,88))
print("CONTRÔLE ÉCHELLES 1-5 (",len(scale_idx),"colonnes )")
oob=False
for i in scale_idx:
    s=df[cols[i]].dropna(); num=pd.to_numeric(s,errors="coerce")
    nn=s[num.isna()]; bad=num[(num<1)|(num>5)]
    if len(nn) or len(bad):
        oob=True; print(f"  [!] [{i}] {str(cols[i])[:45]} non_num={list(nn.astype(str))} hors={sorted(bad.unique().tolist())}")
print("  OK bornes 1-5" if not oob else "")

print("\nCATÉGORIELLES (7 valeurs) :")
for i,lab in {4:"Q0.1 type structure",5:"Q0.2 nb conseillers",6:"Q0.3 nb accompagnés/an",15:"Q1.3 qualif dominante"}.items():
    print(f"\n--- [{i}] {lab}")
    for v in df[cols[i]].astype(str).tolist(): print("   •",v)

print("\nMULTI-SELECT Q1.1 publics (7 lignes) :")
for v in df[cols[7]].dropna().astype(str).tolist(): print("   •",v)
