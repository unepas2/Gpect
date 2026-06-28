# -*- coding: utf-8 -*-
"""
ETAPE 1 (suite) — Controle qualite anti-decalage / hors-echelle / doublons.
Aucune donnee nominative affichee (noms/emails/tel masques).
"""
import pandas as pd, re, unicodedata

SRC = "/root/.claude/uploads/c81e9d0c-8492-5a42-b5cc-973534e42748/8ffdf5f0-01_entreprises.xlsx.xlsx"
df = pd.read_excel(SRC, sheet_name="Réponses au formulaire 1", engine="openpyxl")
C = list(df.columns)

print("### A. COLONNES SENSIBLES — verif anti-decalage (le contenu colle-t-il a l'intitule ?)")
# Consentement [01],[02] : doivent contenir du consentement, PAS des noms
for idx in [1, 2]:
    vals = df.iloc[:, idx].astype(str).str.strip().unique()
    print(f" [{idx:02d}] valeurs uniques = {list(vals)[:3]}")
# Statut juridique [10], secteur [11], tranche dirigeant [18] : categoriels surs
for idx in [10, 11, 18]:
    vals = sorted(df.iloc[:, idx].astype(str).str.strip().unique())
    print(f" [{idx:02d}] {str(C[idx])[:45]}... -> {len(vals)} modalites : {vals}")

print("\n### B. DOUBLONS DEGUISES sur le nom d'entreprise (normalise) — noms NON affiches")
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)
names_norm = df.iloc[:, 3].map(norm)
dup = names_norm[names_norm.duplicated(keep=False)]
print(f" Noms uniques (brut) : {df.iloc[:,3].nunique()} / Noms uniques (normalises) : {names_norm.nunique()}")
print(f" Doublons normalises detectes : {len(dup)}  (0 = aucun doublon cache)")

print("\n### C. VALIDATION DES ECHELLES 1-5 (toute valeur hors {1..5} = ALERTE)")
echelle_cols = [i for i,c in enumerate(C) if ("1 = " in str(c)) or ("[" in str(c) and "impact" in str(c).lower())]
alertes = 0
for i in echelle_cols:
    s = pd.to_numeric(df.iloc[:, i], errors="coerce").dropna()
    hors = s[(s < 1) | (s > 5)]
    if len(hors) > 0:
        print(f"  !! [{i:02d}] hors-echelle : {sorted(hors.unique())}"); alertes += 1
print(f"  Colonnes echelle testees : {len(echelle_cols)} | alertes hors-echelle : {alertes}")

print("\n### D. BORNES DES VARIABLES NUMERIQUES (effectifs, pyramide, retraites, recrut.)")
num_idx = [13,14,16,50,51,81] + list(range(42,50))
for i in num_idx:
    s = pd.to_numeric(df.iloc[:, i], errors="coerce")
    lab = str(C[i])[:48]
    print(f"  [{i:02d}] {lab:50s} min={s.min()} max={s.max()} remplis={s.notna().sum()} <0:{(s<0).sum()}")

print("\n### E. EFFET DE POIDS — plus gros employeur (effectif inscrit Q1.4)")
eff = pd.to_numeric(df.iloc[:, 14], errors="coerce")
print(f"  Effectif inscrit Q1.4 : total={int(eff.sum())} | max={int(eff.max())} | 2e max={int(eff.sort_values(ascending=False).iloc[1])}")
print(f"  Part du plus gros dans le total : {eff.max()/eff.sum()*100:.1f}%  (effet de poids a surveiller)")

print("\n### F. COLONNES AMBIGUES / a typer manuellement plus tard")
print("  [13] Q1.3 effectif = TRANCHE texte (uniques=4), [14] Q1.4 effectif = NUMERIQUE -> deux logiques differentes")
for idx in [13]:
    print(f"   [{idx}] modalites Q1.3 : {sorted(df.iloc[:,idx].astype(str).str.strip().unique())}")
print(f"  [17] Q1.7 prestation = object (texte+num melanges?) remplis={df.iloc[:,17].notna().sum()}")
print(f"  [09] Q0.7 NAF/APE = object remplis={df.iloc[:,9].notna().sum()}/21")
