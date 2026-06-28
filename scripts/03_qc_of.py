# -*- coding: utf-8 -*-
"""ETAPE 1 (suite) — QC collège Organismes de formation. Aucune donnee nominative affichee."""
import pandas as pd, re, unicodedata
SRC = "/root/.claude/uploads/c81e9d0c-8492-5a42-b5cc-973534e42748/fa1196a1-02_organismes_formation.xlsx.xlsx"
df = pd.read_excel(SRC, sheet_name="Réponses au formulaire 1", engine="openpyxl")
C = list(df.columns)

print("### A. ANTI-DECALAGE — consentement [01][02] doivent contenir du consentement, pas des noms")
for idx in [1,2]:
    print(f" [{idx:02d}] -> {list(df.iloc[:,idx].astype(str).str.strip().unique())}")
print(" Categoriels surs (non nominatifs) :")
for idx in [9,11,18,21,43,65,78]:
    vals = sorted(df.iloc[:,idx].astype(str).str.strip().unique())
    print(f"  [{idx:02d}] {str(C[idx])[:38]:40s} -> {vals}")

print("\n### B. DOUBLONS DEGUISES sur nom organisme (normalise, noms NON affiches)")
def norm(s):
    s = unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]','',s)
nn = df.iloc[:,3].map(norm)
print(f"  noms uniques brut={df.iloc[:,3].nunique()} | normalises={nn.nunique()} | doublons={nn.duplicated().sum()}")

print("\n### C. VALIDATION ECHELLES — toutes colonnes numeriques int64 : verifier bornes 1-5")
int_cols = [i for i,c in enumerate(C) if str(df[c].dtype)=='int64']
hors=0
for i in int_cols:
    s = pd.to_numeric(df.iloc[:,i],errors='coerce')
    mn,mx = s.min(),s.max()
    flag = "" if (mn>=1 and mx<=5) else "  <-- HORS 1-5 !!"
    if flag: hors+=1
    print(f"  [{i:02d}] min={mn} max={mx} {str(C[i])[:50]}{flag}")
print(f"  => colonnes int64={len(int_cols)} | hors 1-5 = {hors}")

print("\n### D. COLONNES NUMERIQUES 'object' a typer (formateurs Q1.5/Q1.6)")
for idx in [19,20]:
    print(f"  [{idx:02d}] {str(C[idx])[:45]} -> valeurs brutes : {list(df.iloc[:,idx].astype(str).str.strip())}")

print("\n### E. HORODATEUR (datation source)")
h = pd.to_datetime(df.iloc[:,0])
print(f"  collecte du {h.min().strftime('%d/%m/%Y')} au {h.max().strftime('%d/%m/%Y')}")

print("\n### F. TAUX DE REPONSE FAIBLES = filtres conditionnels (normal) — colonnes <7 remplis")
for i,c in enumerate(C):
    n = df[c].notna().sum()
    if n < 7:
        print(f"  [{i:02d}] remplis={n}/7  {str(c)[:55]}")
