#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 2 — SCRIPT MAÎTRE collège ACTEURS DE L'EMPLOI (GPECT Issoudun). n=7.
Quasi 100% échelles 1-5. Pour chaque échelle : stats globales + éclairage
intérim (n=3) vs opérateurs publics (n=4). Multi-select via contains.
Écrit resultats_acteurs.json + rapport markdown."""
import json, re
import numpy as np, pandas as pd
from datetime import datetime, timezone

PATH="/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/eb78e3b2-03_acteurs_emploi.xlsx.xlsx"
OUT_JSON="/home/user/Gpect/analyse/resultats/resultats_acteurs.json"
OUT_MD="/home/user/Gpect/analyse/resultats/resultats_acteurs_rapport.md"

df=pd.read_excel(PATH,engine="openpyxl",dtype=object); cols=list(df.columns); N=len(df)
assert N==7, f"PÉRIMÈTRE INVALIDE {N}!=7"
interim=df.index[df[cols[4]].astype(str).str.contains("ntérim",case=False,na=False)].tolist()
public=[i for i in df.index if i not in interim]

def r1(x): return None if x is None or (isinstance(x,float) and np.isnan(x)) else round(float(x),1)
def grp_mean(idx, idx_list):
    s=pd.to_numeric(df.loc[idx_list,cols[idx]],errors="coerce").dropna()
    return r1(s.mean()) if len(s) else None
def scale_one(idx, qid, label):
    s=pd.to_numeric(df[cols[idx]],errors="coerce").dropna()
    return {"qid":qid,"item":label,"type":"echelle_1_5","intitule":str(cols[idx]),
            "n":int(s.shape[0]),"moyenne":r1(s.mean()),"mediane":r1(s.median()),
            "min":(int(s.min()) if len(s) else None),"max":(int(s.max()) if len(s) else None),
            "ecart_type":r1(s.std(ddof=1)) if s.shape[0]>1 else None,
            "moy_interim":grp_mean(idx,interim),"moy_public":grp_mean(idx,public)}
def battery(rng,qid,base):
    items=[]
    for i in rng:
        sub=re.search(r"\[(.+)\]",str(cols[i])); lab=sub.group(1) if sub else str(cols[i])
        items.append(scale_one(i,qid,lab))
    classt=sorted(items,key=lambda x:x["moyenne"] if x["moyenne"] is not None else -1,reverse=True)
    return {"qid":qid,"type":"batterie_echelle_1_5","intitule":base,"n_items":len(items),
            "items":items,"classement_par_moyenne":classt}
def cat_counts(idx,qid):
    s=df[cols[idx]].dropna(); n=int(s.shape[0]); vc=s.value_counts()
    return {"qid":qid,"type":"choix_unique","intitule":str(cols[idx]),"n_repondants":n,
            "modalites":[{"modalite":str(k),"n":int(v),"pct":r1(100*v/n)} for k,v in vc.items()]}
def multi_counts(idx,qid,mods):
    s=df[cols[idx]].dropna().astype(str); n=int(s.shape[0]); out=[]
    for lab,kw in mods:
        c=int(s.str.contains(re.escape(kw),case=False,na=False).sum())
        out.append({"modalite":lab,"n":c,"pct_repondants":r1(100*c/n)})
    return {"qid":qid,"type":"multi_select","intitule":str(cols[idx]),"n_repondants":n,
            "modalites":sorted(out,key=lambda x:x["n"],reverse=True)}

R={"_meta":{"college":"Acteurs de l'emploi","n_repondants":N,"source":PATH.split("/")[-1],
    "source_date":"2026-03 (collecte) / export 2026-06-28",
    "genere_le":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "composition":"3 agences d'intérim, 4 opérateurs publics (France Travail, Mission Locale, Cap Emploi, APEC)",
    "lignes_interim_internes":interim,"lignes_public_internes":public,
    "avertissement":"n=7 : aucune généralisation. Effectifs bruts + dispersion prioritaires."},
   "questions":{}}
q=R["questions"]
# Q0
q["Q0.1_type"]=cat_counts(4,"Q0.1")
q["Q0.2_conseillers"]=cat_counts(5,"Q0.2")
q["Q0.3_volume_accompagnes"]=cat_counts(6,"Q0.3")
# Q1
q["Q1.1_publics"]=multi_counts(7,"Q1.1",[
    ("Jeunes <26 ans","Jeunes de moins de 26"),("Seniors 50+","Seniors de 50"),
    ("Publics issus des QPV","QPV"),("Travailleurs handicapés","handicapés"),
    ("Personnes en reconversion","reconversion"),("Demandeurs d'emploi longue durée","longue durée"),
    ("Réfugiés / primo-arrivants","primo-arrivants")])
q["Q1.2_importance_publics"]=battery(range(8,15),"Q1.2","Importance des publics (1 faible→5 fort)")
q["Q1.3_qualif_dominante"]=cat_counts(15,"Q1.3")
# Q2
q["Q2.1_adequation_profils"]=scale_one(16,"Q2.1","Adéquation profils/besoins (1 faible→5 forte)")
q["Q2.2_facteurs_inadequation"]=battery(range(17,24),"Q2.2","Facteurs d'inadéquation candidats/besoins (1→5)")
# Q3
q["Q3.1_difficulte_competences"]=battery(range(24,36),"Q3.1","Difficulté des entreprises à trouver la compétence (1→5)")
# Q4
q["Q4.1_freins_acces_emploi"]=battery(range(36,44),"Q4.1","Freins à l'accès à l'emploi industriel (1→5)")
# Q5
q["Q5.1_usage_dispositifs"]=battery(range(44,48),"Q5.1","Usage des dispositifs (1 jamais→5 systématique)")
q["Q5.2_efficacite_dispositifs"]=battery(range(48,52),"Q5.2","Efficacité perçue des dispositifs (1→5)")
q["Q5.3_duree_emplois"]=scale_one(52,"Q5.3","Durée/stabilité des emplois obtenus (1 courte→5 durable)")
# Q6
q["Q6.1_offre_locale"]=scale_one(53,"Q6.1","Offre de formation locale répond aux besoins (1 faible→5 forte)")
q["Q6.2_manque_formation"]=battery(range(54,65),"Q6.2","Manque de formation par domaine (1 faible→5 fort manque)")
# Q7
q["Q7.1_cooperation"]=battery(range(65,70),"Q7.1","Coopération avec les entreprises (1→5)")
# Q8
q["Q8.1_importance_actions"]=battery(range(70,76),"Q8.1","Importance des actions territoriales (1→5)")
q["Q8.2_participation"]=battery(range(76,83),"Q8.2","Disposition à participer aux actions collectives (1→5)")
q["Q8.3_interet_ateliers"]=battery(range(83,88),"Q8.3","Intérêt pour les ateliers GPECT (1→5)")

# récap
recap=[]
for k,v in q.items():
    if v.get("type")=="echelle_1_5":
        recap.append({"qid":v["qid"],"item":v["item"],"moyenne":v["moyenne"],"mediane":v["mediane"],
                      "ecart_type":v["ecart_type"],"n":v["n"],"moy_interim":v["moy_interim"],"moy_public":v["moy_public"]})
    elif v.get("type")=="batterie_echelle_1_5":
        for it in v["items"]:
            recap.append({"qid":v["qid"],"item":it["item"],"moyenne":it["moyenne"],"mediane":it["mediane"],
                          "ecart_type":it["ecart_type"],"n":it["n"],"moy_interim":it["moy_interim"],"moy_public":it["moy_public"]})
R["recap_echelles"]=recap
json.dump(R,open(OUT_JSON,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("OK -> resultats_acteurs.json | n=",N,"| intérim",interim,"| public",public,"| échelles récap",len(recap))
