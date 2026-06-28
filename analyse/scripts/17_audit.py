#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUDIT pré-livraison. Vérifie : noms/PII dans les livrables, périmètre,
traçabilité (recalcul depuis xlsx), exhaustivité colonnes, anomalies, cohérence."""
import json, re, glob, pathlib
import pandas as pd, numpy as np
RES=pathlib.Path("/home/user/Gpect/analyse/resultats")
UP="/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/"
XLS={"entreprises":UP+"126d3b2d-01_entreprises.xlsx.xlsx","of":UP+"677aa4a6-02_organismes_formation.xlsx.xlsx",
     "acteurs":UP+"eb78e3b2-03_acteurs_emploi.xlsx.xlsx","syndicats":UP+"574f81cd-04_syndicats.xlsx.xlsx"}
J={k:json.load(open(RES/f"resultats_{k}.json",encoding="utf-8")) for k in XLS}
SV=json.load(open(RES/"source_verite.json",encoding="utf-8"))
DASH=(pathlib.Path("/home/user/Gpect/analyse/dashboard/dashboard_gpect_issoudun.html")).read_text(encoding="utf-8")
MDS={p.name:p.read_text(encoding="utf-8") for p in RES.glob("*.md")}

def H(t): print("\n"+"="*70+"\n"+t+"\n"+"="*70)

# ---------- 1. NOMS / PII ----------
H("1. RECHERCHE DE NOMS / PII DANS LES LIVRABLES")
# colonnes identité par fichier
idcols={"entreprises":[3,4],"of":[3,4],"acteurs":[3],"syndicats":[1,2,3]}
names=set()
for k,path in XLS.items():
    df=pd.read_excel(path,engine="openpyxl",dtype=object)
    for i in idcols[k]:
        for v in df.iloc[:,i].dropna().astype(str):
            names.add(v.strip())
# tokens significatifs
stop={"de","la","le","et","des","du","les","centre","val","loire","indre","france","travail",
      "mission","locale","cap","emploi","organisation","professionnelle","syndicale","agence",
      "interim","intérim","groupe","site","responsable","conseillère","conseiller","délégué",
      "déléguée","directrice","directeur","générale","général","emploi","formation","bureau",
      "entreprises","ressources","humaines","coordinateur","central","départemental","représente"}
toks=set()
for n in names:
    for t in re.split(r"[\s/\-,]+",n):
        t=t.strip()
        if len(t)>=4 and t.lower() not in stop and not t.isdigit():
            toks.add(t)
deliverables={"resultats_entreprises.json":json.dumps(J["entreprises"],ensure_ascii=False),
 "resultats_of.json":json.dumps(J["of"],ensure_ascii=False),
 "resultats_acteurs.json":json.dumps(J["acteurs"],ensure_ascii=False),
 "resultats_syndicats.json":json.dumps(J["syndicats"],ensure_ascii=False),
 "source_verite.json":json.dumps(SV,ensure_ascii=False),
 "dashboard.html(zone visible)":re.sub(r"const SV =.*?;</script>","",DASH,flags=re.S)}
print("Noms/tokens identité recherchés :",len(toks))
hits={}
for fname,txt in deliverables.items():
    found=sorted({t for t in toks if re.search(r"\b"+re.escape(t)+r"\b",txt,re.I)})
    if found: hits[fname]=found
if not hits: print("  ✅ AUCUN nom/token d'identité de répondant trouvé dans les livrables.")
else:
    for f,v in hits.items(): print(f"  ⚠️ {f} -> {v}")

# noms propres tiers dans verbatims (heuristique majuscules)
H("1b. NOMS PROPRES TIERS DANS LES VERBATIMS (à anonymiser ?)")
def collect_verbatims(jj):
    out=[]
    for qk,d in jj["questions"].items():
        for v in (d.get("verbatims_anonymises") or []):
            out.append((qk,v))
    return out
propnoun=re.compile(r"\b([A-ZÉÈÀ][A-Za-zÉÈÀ]{2,}(?:\s+[A-ZÉÈÀ][A-Za-zÉÈÀ]{2,})?)\b")
WL={"RAS","RSE","DUERP","AFEST","OPCO","POEI","PMSMP","CAO","DAO","CNC","CFA","VAE","IA","CCI","CMA",
    "UIMM","SPL","CACES","GPECT","Industrie","Production","Maintenance","Usinage","Soudure","Logistique",
    "Mécanique","Qualité","Conduite","Formation","Technicien","Maroquinerie","Chaudronnier","Monteur",
    "Métiers","Education","Nationale","Région","Département","Difficulté","Manque","Travailler","Avoir",
    "Bien","Donner","Adaptation","Navette","Hébergement","Financement","Création","Révision","Accompagnement",
    "Communication","Attractivité","Valorisation","Rencontre","Société","Groupe","Ateliers","Atelier",
    "Anglais","Programma","Réapprendre","Connaissance","Refonte","Mobiliser","Pas","Non","Que","Dans","Le","La"}
for k in ("of","syndicats"):
    print(f"-- {k} --")
    for qk,v in collect_verbatims(J[k]):
        cands=[m for m in propnoun.findall(v) if m.split()[0] not in WL and not all(w in WL for w in m.split())]
        # garder mots avec majuscule interne ou connus comme entités
        flag=[c for c in cands if re.search(r"(Safran|Vuitton|Trigano|Tech Demi|Lizaine|Fouchon|Manpower|Adecco|Triangle|Leclerc|Afpa|Afpi|SAFRAN)",v,re.I)]
        if flag:
            print(f"   [{qk}] !! {sorted(set(flag))}  ::  {v[:120]}")

# ---------- 2. PERIMETRE ----------
H("2. PÉRIMÈTRE")
exp={"entreprises":21,"of":7,"acteurs":7,"syndicats":7}
okp=True
for k in XLS:
    df=pd.read_excel(XLS[k],engine="openpyxl",dtype=object); n=len(df.dropna(how="all"))
    jn=J[k]["_meta"]["n_repondants"]
    s="✅" if (n==exp[k]==jn) else "❌"; okp&= (n==exp[k]==jn)
    print(f"  {s} {k}: xlsx={n} | json={jn} | attendu={exp[k]}")
tot=sum(J[k]["_meta"]["n_repondants"] for k in XLS)
print(f"  TOTAL json = {tot} (attendu 42) ", "✅" if tot==42 else "❌")

# ---------- 3. TRACABILITE : recalcul direct depuis xlsx ----------
H("3. TRAÇABILITÉ — 15 chiffres recalculés depuis le .xlsx et comparés au JSON (= ce que lit le dashboard)")
def col(df,i): return df.iloc[:,i]
def mean15(s): s=pd.to_numeric(s,errors="coerce").dropna(); return round(s.mean(),1)
E=pd.read_excel(XLS["entreprises"],engine="openpyxl",dtype=object)
O=pd.read_excel(XLS["of"],engine="openpyxl",dtype=object)
A=pd.read_excel(XLS["acteurs"],engine="openpyxl",dtype=object)
S=pd.read_excel(XLS["syndicats"],engine="openpyxl",dtype=object)
checks=[]
def getbatt(jj,qk,sub):
    for it in jj["questions"][qk]["items"]:
        if sub in it["item"]: return it["moyenne"]
def getscale(jj,qk): return jj["questions"][qk]["moyenne"]
def getcat(jj,qk,sub):
    for m in jj["questions"][qk]["modalites"]:
        if sub in m["modalite"]: return (m["n"],m.get("pct"))
def getmulti(jj,qk,sub):
    for m in jj["questions"][qk]["modalites"]:
        if sub in m["modalite"]: return (m["n"],m.get("pct_repondants"))
# 1 Ent Q3.3 pénurie (col 26)
checks.append(("Ent Q3.3 Pénurie candidats (col26)",mean15(col(E,26)),getbatt(J["entreprises"],"Q3.3_causes_tensions","Pénurie")))
# 2 Ent Q8.2 image (col111)
checks.append(("Ent Q8.2 image (col111)",mean15(col(E,111)),getscale(J["entreprises"],"Q8.2_image_issoudun")))
# 3 Ent Q4.8 AFEST (col66)
checks.append(("Ent Q4.8 AFEST (col66)",mean15(col(E,66)),getbatt(J["entreprises"],"Q4.8_dispositifs_transmission","AFEST")))
# 4 Ent Q1.4 somme (col14)
checks.append(("Ent Q1.4 somme effectif (col14)",round(pd.to_numeric(col(E,14),errors="coerce").sum(),1),J["entreprises"]["questions"]["Q1.4_effectif_inscrit"]["somme"]))
# 5 Ent Q5.4 somme recrut (col81)
checks.append(("Ent Q5.4 somme recrut (col81)",round(pd.to_numeric(col(E,81),errors="coerce").sum(),1),J["entreprises"]["questions"]["Q5.4_recrut_prevus_3ans"]["somme"]))
# 6 Ent Q3.2 majeures n (col25)
nmaj=int((col(E,25).astype(str).str.contains("majeures")).sum())
checks.append(("Ent Q3.2 'difficultés majeures' n (col25)",nmaj,getcat(J["entreprises"],"Q3.2_tension","majeures")[0]))
# 7 Ent Q8.1 image frein contains % (col110)
nimg=int(col(E,110).dropna().astype(str).str.contains("Image globale du territoire",case=False).sum())
checks.append(("Ent Q8.1 image frein n (col110)",nimg,getmulti(J["entreprises"],"Q8.1_facteurs_territoire","Image du territoire")[0]))
# 8 OF Q2.2 IA (col35)
checks.append(("OF Q2.2 capacité IA (col35)",mean15(col(O,35)),getbatt(J["of"],"Q2.2_capacite_emergentes","Intelligence")))
# 9 OF Q2.2 cyber (col39)
checks.append(("OF Q2.2 capacité cyber (col39)",mean15(col(O,39)),getbatt(J["of"],"Q2.2_capacite_emergentes","Cybers")))
# 10 OF Q4.1 offre (col55)
checks.append(("OF Q4.1 offre couvre (col55)",mean15(col(O,55)),getscale(J["of"],"Q4.1_offre_couvre")))
# 11 Acteurs Q3.1 maintenance (col25)
checks.append(("Act Q3.1 maintenance (col25)",mean15(col(A,25)),getbatt(J["acteurs"],"Q3.1_difficulte_competences","Maintenance industrielle")))
# 12 Acteurs Q6.1 offre (col53)
checks.append(("Act Q6.1 offre locale (col53)",mean15(col(A,53)),getscale(J["acteurs"],"Q6.1_offre_locale")))
# 13 Acteurs Q8.1 plateforme (col70)
checks.append(("Act Q8.1 plateforme mutualisée (col70)",mean15(col(A,70)),getbatt(J["acteurs"],"Q8.1_importance_actions","Plateforme")))
# 14 Synd Q24 transmission 'Prioritaire' n (col24)  -> n exact
npr=int((col(S,24).astype(str).str.strip()=="Prioritaire").sum())
checks.append(("Synd Q24 'Prioritaire' n (col24)",npr,getcat(J["syndicats"],"Q24_transmission","Prioritaire")[0] if False else next(m["n"] for m in J["syndicats"]["questions"]["Q24_transmission"]["modalites"] if m["modalite"]=="Prioritaire")))
# 15 Synd Q18 mobilité (col18)
checks.append(("Synd Q18 mobilité frein (col18)",mean15(col(S,18)),getscale(J["syndicats"],"Q18_mobilite_frein")))
allok=True
for lab,src,jv in checks:
    ok=(src==jv); allok&=ok
    print(f"  {'✅' if ok else '❌'} {lab}: xlsx={src} | json/dashboard={jv}")
print("  -> Traçabilité 15/15 :", "✅ OK" if allok else "❌ ÉCART")

# ---------- 4. EXHAUSTIVITE ----------
H("4. EXHAUSTIVITÉ — colonnes existantes vs traitées")
# qids présents par fichier (extraits des intitulés sources)
def treated_qids(jj):
    s=set()
    for d in jj["questions"].values():
        intit=d.get("intitule","")
        m=re.match(r"\s*(Q[0-9]+(?:\.[0-9]+[a-z]?)*)",str(intit))
        if m: s.add(m.group(1))
        # batterie : ajouter qid
        if d.get("qid"): s.add(d["qid"])
    return s
for k in XLS:
    df=pd.read_excel(XLS[k],engine="openpyxl",dtype=object)
    qcols=[c for c in df.columns if re.match(r"\s*Q[0-9]",str(c))]
    # qid de base par colonne
    base=set()
    for c in qcols:
        m=re.match(r"\s*(Q[0-9]+(?:\.[0-9]+[a-z]?)*)",str(c));
        if m: base.add(m.group(1))
    tr=treated_qids(J[k])
    miss=sorted(base-tr)
    print(f"  {k}: {df.shape[1]} colonnes ; {len(qcols)} colonnes 'Q*' ; {len(base)} questions distinctes ; traitées {len(base& tr)}/{len(base)}")
    if miss: print(f"     non couvertes : {miss}")

# ---------- 6. ANOMALIES ----------
H("6. ANOMALIES (pct>100, moyenne hors 1-5, n incohérent)")
anom=[]
for k in XLS:
    for qk,d in J[k]["questions"].items():
        t=d.get("type")
        if t=="echelle_1_5":
            if d["moyenne"] is not None and not(1<=d["moyenne"]<=5): anom.append(f"{k}/{qk} moyenne {d['moyenne']} hors 1-5")
        if t=="batterie_echelle_1_5":
            for it in d["items"]:
                if it["moyenne"] is not None and not(1<=it["moyenne"]<=5): anom.append(f"{k}/{qk}/{it['item']} {it['moyenne']} hors 1-5")
        if t=="multi_select":
            for m in d["modalites"]:
                if m["pct_repondants"] is not None and m["pct_repondants"]>100: anom.append(f"{k}/{qk}/{m['modalite']} pct {m['pct_repondants']}>100")
        if t=="choix_unique":
            ssum=sum(m["n"] for m in d["modalites"])
            if ssum>d["n_repondants"]: anom.append(f"{k}/{qk} somme n {ssum} > n_repondants {d['n_repondants']}")
print("  "+("✅ aucune anomalie" if not anom else "❌ "+str(len(anom))+" anomalies :"))
for a in anom: print("   -",a)

# ---------- 5. COHERENCE source_verite vs college ----------
H("5. COHÉRENCE source_verite (dimensions) vs JSON collège d'origine")
def offre(): return getscale(J["of"],"Q4.1_offre_couvre"),getscale(J["entreprises"],"Q7.6_offre_adaptee"),getscale(J["acteurs"],"Q6.1_offre_locale")
d0=SV["dimensions_partagees"][0]["valeurs"]
o_of,o_ent,o_act=offre()
for lab,sv,src in [("offre.of",d0["of"],o_of),("offre.ent",d0["entreprises"],o_ent),("offre.act",d0["acteurs"],o_act)]:
    print(f"  {'✅' if sv==src else '❌'} {lab}: source_verite={sv} | collège={src}")
afd=next(d for d in SV["dimensions_partagees"] if "AFEST" in d["dimension"])["valeurs"]
print(f"  {'✅' if afd['entreprises']==getbatt(J['entreprises'],'Q4.8_dispositifs_transmission','AFEST') else '❌'} AFEST.ent: sv={afd['entreprises']} | collège={getbatt(J['entreprises'],'Q4.8_dispositifs_transmission','AFEST')}")
print("\nAUDIT TERMINÉ.")
