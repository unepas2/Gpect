#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÉTAPE 2 (exploration préalable) — Collège Entreprises.
Objectif : disposer de tout le matériau pour
  1) trancher l'anomalie A1 (décimales pyramide des âges),
  2) construire les listes de modalités des questions à choix MULTIPLE
     (comptage par str.contains, jamais par split virgule),
  3) coder par thèmes les champs texte libre.
Aucune décision d'indicateur figée ici : on imprime, on lit, on décidera
dans le script maître 02_analyse.
"""
import pandas as pd

PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/126d3b2d-01_entreprises.xlsx.xlsx"
df = pd.read_excel(PATH, engine="openpyxl", dtype=object)
cols = list(df.columns)
N = len(df)

def line(t=""):
    print(t)

# ------------------------------------------------------------------ A1
line("#" * 80)
line("# A1 — INVESTIGATION PYRAMIDE DES ÂGES (Q4.1.1 -> Q4.1.8)")
line("#" * 80)
pyr_idx = list(range(42, 50))  # 8 colonnes
eff_inscrit = pd.to_numeric(df[cols[14]], errors="coerce")  # Q1.4
band = df[cols[13]]  # Q1.3
line("Légende colonnes pyramide :")
for i in pyr_idx:
    line(f"   [{i}] {cols[i]}")
line("")
line(f"{'lig':>3} | {'H<30':>5} {'F<30':>5} {'H31-44':>6} {'F31-44':>6} {'H45-59':>6} {'F45-59':>6} {'H60+':>5} {'F60+':>5} | {'somme_pyr':>9} | {'Q1.4_inscrit':>11} | decimal?")
for r in range(N):
    vals = [pd.to_numeric(df.iloc[r, i], errors="coerce") for i in pyr_idx]
    somme = sum(v for v in vals if pd.notna(v))
    has_dec = any(pd.notna(v) and float(v) != int(v) for v in vals)
    vv = " ".join(f"{(v if pd.notna(v) else 0):>5.2f}" if has_dec else f"{int(v) if pd.notna(v) else 0:>5d}" for v in vals)
    # alignement simple
    cells = []
    for v in vals:
        if pd.isna(v):
            cells.append("   .")
        elif has_dec:
            cells.append(f"{float(v):.2f}")
        else:
            cells.append(str(int(v)))
    flag = "  <-- DÉCIMAUX" if has_dec else ""
    e = eff_inscrit.iloc[r]
    line(f"{r:>3} | " + " ".join(f"{c:>6}" for c in cells) +
         f" | somme={somme:>8.2f} | Q1.4={'' if pd.isna(e) else int(e):>6} | band={band.iloc[r]}{flag}")

# ------------------------------------------------------------------ choix unique
line("")
line("#" * 80)
line("# VALEURS & EFFECTIFS — COLONNES À CHOIX UNIQUE / CATÉGORIELLES")
line("#" * 80)
choix_unique = {
    10: "Q0.8 Statut juridique (brut)",
    11: "Q1.1 Secteur",
    13: "Q1.3 Effectif total (tranche)",
    15: "Q1.5 Recours ressources externes",
    18: "Q1.8 Tranche âge dirigeant",
    20: "Q2.2 Transmission/cession",
    21: "Q2.3 Évolution effectifs 3 ans",
    22: "Q2.4 Investissements prévus",
    23: "Q2.5 Investissements -> compétences",
    25: "Q3.2 Tension recrutement",
    36: "Q3.4 Métiers sensibles",
    53: "Q4.5 Turnover",
    70: "Q4.8b Besoin transmission",
    71: "Q5.1 Recrutements 2024-2025",
    84: "Q6.1 Compétences techniques adaptées",
    86: "Q6.3 Savoir-être adaptés",
    89: "Q7.1 Formations organisées",
    90: "Q7.2 Connaissance OPCO",
    92: "Q7.4 Alternance",
    93: "Q7.5 Alternants du territoire",
    101: "Q7.8 Coopération acteurs emploi",
}
for i, lab in choix_unique.items():
    line(f"\n--- [{i}] {lab} | n_rempli={df[cols[i]].notna().sum()}")
    vc = df[cols[i]].astype(str).where(df[cols[i]].notna()).value_counts(dropna=True)
    for val, cnt in vc.items():
        line(f"     {cnt:>3}  | {val}")

# ------------------------------------------------------------------ multi-select RAW
line("")
line("#" * 80)
line("# VALEURS BRUTES UNIQUES — COLONNES À CHOIX MULTIPLE (pour bâtir modalités)")
line("#" * 80)
multi = {
    19: "Q2.1 3 préoccupations",
    52: "Q4.4 Services/métiers départs retraite",
    82: "Q5.5 Motivation recrutements",
    83: "Q5.6 Actions attractivité",
    85: "Q6.2 Compétences techniques manquantes",
    87: "Q6.4 Savoir-être à renforcer",
    88: "Q6.5 Compétences à développer 3-5 ans",
    91: "Q7.3 Freins formation",
    110: "Q8.1 Facteurs territoire",
    112: "Q8.3 Actions collectives (prêt à s'engager)",
    121: "Q9.2 Ateliers co-construction",
}
for i, lab in multi.items():
    line(f"\n--- [{i}] {lab} | n_rempli={df[cols[i]].notna().sum()}")
    for v in df[cols[i]].dropna().astype(str).tolist():
        line(f"     • {v}")

# ------------------------------------------------------------------ texte libre
line("")
line("#" * 80)
line("# CHAMPS TEXTE LIBRE (verbatims — pour codage thématique, à anonymiser)")
line("#" * 80)
freetext = {
    12: "Q1.2 Autre secteur",
    24: "Q3.1 Métiers clés/en tension",
    52: "Q4.4 (déjà multi mais texte libre mixte)",
    54: "Q4.6 Postes turnover",
    122: "Q9.3 Action concrète la plus utile",
    123: "Q9.4 Remarques",
}
for i, lab in freetext.items():
    line(f"\n--- [{i}] {lab} | n_rempli={df[cols[i]].notna().sum()}")
    for v in df[cols[i]].dropna().astype(str).tolist():
        line(f"     » {v}")

# numeric raw (volumes) for cleaning decisions
line("")
line("#" * 80)
line("# NUMÉRIQUES — VALEURS BRUTES (nettoyage volumes intérim/prestation)")
line("#" * 80)
for i, lab in {16: "Q1.6 intérim", 17: "Q1.7 prestation",
               50: "Q4.2 retraite 2 ans", 51: "Q4.3 retraite 5 ans",
               81: "Q5.4 recrut. prévus 3 ans", 14: "Q1.4 effectif inscrit"}.items():
    vals = df[cols[i]].dropna().astype(str).tolist()
    line(f"--- [{i}] {lab} (n={len(vals)}) : {vals}")
