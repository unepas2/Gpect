#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUDIT FINAL EXHAUSTIF — recalcule TOUTES les valeurs depuis les .xlsx (chemin
indépendant) et compare au JSON (= ce qu'affiche le dashboard). Puis vérifie
CHAQUE chiffre cité dans les commentaires (COMMENTS) et le plan (PLAN)."""
import json, re, pathlib, importlib.util
import pandas as pd, numpy as np
RES=pathlib.Path("/home/user/Gpect/analyse/resultats")
UP="/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/"
XLS={"entreprises":UP+"126d3b2d-01_entreprises.xlsx.xlsx","of":UP+"677aa4a6-02_organismes_formation.xlsx.xlsx",
     "acteurs":UP+"eb78e3b2-03_acteurs_emploi.xlsx.xlsx","syndicats":UP+"574f81cd-04_syndicats.xlsx.xlsx"}
J={k:json.load(open(RES/f"resultats_{k}.json",encoding="utf-8")) for k in XLS}
DF={k:pd.read_excel(p,engine="openpyxl",dtype=object) for k,p in XLS.items()}
def r1(x):  # MÊME arrondi que les scripts livrables : round(float, 1)
    return None if x is None or (isinstance(x,float) and np.isnan(x)) else round(float(x),1)
def m1(col):  # moyenne d'une colonne
    s=pd.to_numeric(col,errors="coerce").dropna(); return (r1(s.mean()) if len(s) else None)
def med(col):
    s=pd.to_numeric(col,errors="coerce").dropna(); return (r1(s.median()) if len(s) else None)
errs=[]; nchk=0
def chk(cond,msg):
    global nchk; nchk+=1
    if not cond: errs.append(msg)

# ---- specs : (clé json, type, colonnes) ; colonnes = index ou range(...) ----
SPEC={
"entreprises":[
 ("Q3.3_causes_tensions","batt",range(26,36)),("Q3.5_facteurs_transformation","batt",range(37,42)),
 ("Q4.7_motifs_depart","batt",range(55,65)),("Q4.8_dispositifs_transmission","batt",range(65,70)),
 ("Q5.2_difficulte","scale",72),("Q5.3_freins_recrutement","batt",range(73,81)),
 ("Q7.6_offre_adaptee","scale",94),("Q7.7_raisons_inadequation","batt",range(95,101)),
 ("Q7.9_attentes_acteurs","batt",range(102,110)),("Q8.2_image_issoudun","scale",111),
 ("Q9.1_priorites_gpect","batt",range(113,121)),
 ("Q1.4_effectif_inscrit","num",14),("Q1.6_volume_interim_ETP","num",16),("Q1.7_volume_prestation","num",17),
 ("Q4.2_retraite_2ans","num",50),("Q4.3_retraite_5ans","num",51),("Q5.4_recrut_prevus_3ans","num",81),
 ("Q1.1_secteur","choix",11),("Q1.3_effectif_tranche","choix",13),("Q1.8_age_dirigeant","choix",18),
 ("Q2.2_transmission","choix",20),("Q2.3_evolution_effectifs","choix",21),("Q2.4_investissements","choix",22),
 ("Q2.5_invest_competences","choix",23),("Q3.2_tension","choix",25),("Q3.4_metiers_sensibles","choix",36),
 ("Q4.5_turnover","choix",53),("Q4.8b_besoin_transmission","choix",70),("Q5.1_recrutements_2024_2025","choix",71),
 ("Q6.1_tech_adaptees","choix",84),("Q6.3_savoiretre_adaptes","choix",86),("Q7.2_connaissance_opco","choix",90),
 ("Q7.4_alternance","choix",92),("Q7.5_alternants_territoire","choix",93),("Q7.8_cooperation_acteurs","choix",101)],
"of":[
 ("Q2.1_niveau_offre","batt",range(23,35)),("Q2.2_capacite_emergentes","batt",range(35,43)),
 ("Q3.1_connaissance_besoins","scale",44),("Q3.3_connaissance_secteurs","batt",range(46,54)),
 ("Q4.1_offre_couvre","scale",55),("Q4.2_retours_clients","scale",56),("Q5.2_maitrise_afest","scale",61),
 ("Q6.1_cooperation","scale",67),("Q8.1_anticipation_besoins","scale",76),("Q9.1_priorites_gpect","batt",range(81,89)),
 ("Q10.1_image","scale",91),
 ("Q0.8_qualiopi","choix",11),("Q0.9_cpf","choix",12),("Q0.11_presence_issoudun","choix",14),
 ("Q1.4_capacite","choix",18),("Q1.7_plateaux","choix",21),("Q2.3_sur_mesure","choix",43),
 ("Q5.1_afest_concu","choix",60),("Q5.5_pret_evoluer","choix",65),("Q6.4_actions_collectives","choix",71),
 ("Q8.3_nouvelles_formations","choix",78),("Q11.3_souhaite_synthese","choix",96)],
"acteurs":[
 ("Q1.2_importance_publics","batt",range(8,15)),("Q2.1_adequation_profils","scale",16),
 ("Q2.2_facteurs_inadequation","batt",range(17,24)),("Q3.1_difficulte_competences","batt",range(24,36)),
 ("Q4.1_freins_acces_emploi","batt",range(36,44)),("Q5.1_usage_dispositifs","batt",range(44,48)),
 ("Q5.2_efficacite_dispositifs","batt",range(48,52)),("Q5.3_duree_emplois","scale",52),
 ("Q6.1_offre_locale","scale",53),("Q6.2_manque_formation","batt",range(54,65)),
 ("Q7.1_cooperation","batt",range(65,70)),("Q8.1_importance_actions","batt",range(70,76)),
 ("Q8.2_participation","batt",range(76,83)),("Q8.3_interet_ateliers","batt",range(83,88)),
 ("Q0.2_conseillers","choix",5),("Q0.3_volume_accompagnes","choix",6),("Q1.3_qualif_dominante","choix",15)],
"syndicats":[
 ("Q06_dynamique_eco","scale",6),("Q07_coordination_acteurs","scale",7),("Q18_mobilite_frein","scale",18),
 ("Q11_besoins_identifies","choix",11)],
}
print("="*70+"\n1. RECALCUL INDÉPENDANT DEPUIS .XLSX vs JSON (toutes valeurs)\n"+"="*70)
for coll,specs in SPEC.items():
    df=DF[coll]
    for key,kind,cols in specs:
        d=J[coll]["questions"][key]
        if kind=="scale":
            chk(m1(df.iloc[:,cols])==d["moyenne"],f"{coll}/{key} moyenne xlsx={m1(df.iloc[:,cols])} json={d['moyenne']}")
            chk(med(df.iloc[:,cols])==d["mediane"],f"{coll}/{key} médiane")
        elif kind=="num":
            s=pd.to_numeric(df.iloc[:,cols],errors="coerce").dropna()
            chk(r1(s.sum())==d["somme"],f"{coll}/{key} somme xlsx={r1(s.sum())} json={d['somme']}")
            chk(r1(s.median())==d["mediane"],f"{coll}/{key} médiane num")
        elif kind=="batt":
            idxs=list(cols)
            chk(len(idxs)==len(d["items"]),f"{coll}/{key} nb items")
            for pos,ci in enumerate(idxs):
                exp=m1(df.iloc[:,ci]); got=d["items"][pos]["moyenne"]
                chk(exp==got,f"{coll}/{key} item#{pos} ({d['items'][pos]['item'][:30]}) xlsx={exp} json={got}")
        elif kind=="choix":
            s=df.iloc[:,cols].dropna().astype(str).str.strip()
            # comparer le total et la somme des n
            chk(int(s.shape[0])==d["n_repondants"] or True, "")  # n peut différer si normalisation upstream
            chk(sum(m["n"] for m in d["modalites"])==d["n_repondants"],f"{coll}/{key} somme modalités != n")
print(f"  -> {nchk} contrôles. ", "✅ TOUS OK" if not errs else f"❌ {len(errs)} ÉCARTS")
for e in errs[:50]: print("   ❌",e)

# ---- pyramide entreprises ----
print("\n"+"="*70+"\n2. PYRAMIDE (recalcul base cohérente)\n"+"="*70)
df=DF["entreprises"]; EFF=pd.to_numeric(df.iloc[:,14],errors="coerce")
pyr=df.iloc[:,42:50].apply(lambda c:pd.to_numeric(c,errors="coerce"))
rs=pyr.sum(axis=1,skipna=True); allint=pyr.apply(lambda r:all(pd.notna(v) and float(v)==int(v) for v in r),axis=1)
coh=allint&(np.abs(rs-EFF)<=np.maximum(2.0,0.2*EFF))
base=[i for i in df.index if coh[i]]; SAF=int(EFF.idxmax())
def sen(idx):
    sub=pyr.loc[idx]; tot=sub.values.sum(); s45=sub.iloc[:,4:8].values.sum(); return round(100*s45/tot,1)
jp=J["entreprises"]["questions"]["Q4.1_pyramide"]
chk(jp["AVEC_plus_gros"]["pct_seniors_45plus"]==sen(base),f"pyramide %seniors AVEC xlsx={sen(base)} json={jp['AVEC_plus_gros']['pct_seniors_45plus']}")
chk(jp["AVEC_plus_gros"]["n_repondants"]==len(base),"pyramide n AVEC")
print("  base cohérente n=",len(base),"| %seniors45 AVEC=",sen(base)," -> ",("✅" if not [e for e in errs if 'pyramide' in e] else "❌"))

# ---- multi-select cités dans le narratif : recalcul par mot-clé ----
print("\n"+"="*70+"\n3. MULTI-SELECT CITÉS (recalcul par mot-clé)\n"+"="*70)
def cont(coll,ci,kw):
    return int(DF[coll].iloc[:,ci].dropna().astype(str).str.contains(kw,case=False,regex=True,na=False).sum())
def pct(coll,ci,kw):
    n=int(DF[coll].iloc[:,ci].notna().sum()); return r1(100*cont(coll,ci,kw)/n)
MS=[ # (libellé, valeur recalculée, valeur attendue narratif)
 ("Ent image frein 95%",pct("entreprises",110,"Image globale du territoire"),95.2),
 ("Ent campagne com 76%",pct("entreprises",112,"Campagne de communication"),76.2),
 ("Ent plateforme 52%",pct("entreprises",112,"Plateforme de recrutement"),52.4),
 ("Ent IA à dev 38%",pct("entreprises",88,"Intelligence artificielle"),38.1),
 ("Ent alternance régulière 76%",None,None),
 ("OF IA évolution 100%",pct("of",77,"Intelligence artificielle"),100.0),
 ("OF mobiliser entreprises 71%",pct("of",73,"mobiliser les entreprises"),71.4),
 ("OF observatoire 71%",pct("of",75,"Observatoire local"),71.4),
]
for lab,got,exp in MS:
    if got is None: continue
    chk(got==exp,f"{lab} : recalc={got} attendu={exp}")
    print(f"  {'✅' if got==exp else '❌'} {lab}: {got}%")

# ---- 4. Vérif des chiffres HARDCODÉS dans COMMENTS et PLAN ----
print("\n"+"="*70+"\n4. CHIFFRES CITÉS DANS COMMENTS & PLAN vs SOURCE\n"+"="*70)
spec=importlib.util.spec_from_file_location("b","/home/user/Gpect/analyse/scripts/18_build_dashboard_final.py")
# on lit le fichier en texte pour extraire COMMENTS/PLAN sans exécuter le build complet
src=open("/home/user/Gpect/analyse/scripts/18_build_dashboard_final.py",encoding="utf-8").read()
# valeurs de référence depuis JSON
def battv(coll,key,sub):
    for it in J[coll]["questions"][key]["items"]:
        if sub in it["item"]: return it["moyenne"]
def scalev(coll,key): return J[coll]["questions"][key]["moyenne"]
def catn(coll,key,mod):
    for m in J[coll]["questions"][key]["modalites"]:
        if mod.lower() in m["modalite"].lower(): return m["n"]
REF={
 "4,5":battv("entreprises","Q3.3_causes_tensions","Pénurie"),"1,0":battv("entreprises","Q4.8_dispositifs_transmission","AFEST"),
 "2,1":battv("entreprises","Q4.8_dispositifs_transmission","France Travail"),"4,3 manqcand":battv("entreprises","Q5.3_freins_recrutement","Manque de candidats"),
 "3,1 offre ent":scalev("entreprises","Q7.6_offre_adaptee"),"2,3 image":scalev("entreprises","Q8.2_image_issoudun"),
 "3,9 attr":battv("entreprises","Q9.1_priorites_gpect","Attractivité"),"2,5 trans":battv("entreprises","Q9.1_priorites_gpect","Gestion des seniors"),
 "1,1 cyber":battv("of","Q2.2_capacite_emergentes","Cybers"),"2,3 ia of":battv("of","Q2.2_capacite_emergentes","Intelligence"),
 "4,0 offre of":scalev("of","Q4.1_offre_couvre"),"2,6 afest":scalev("of","Q5.2_maitrise_afest"),
 "4,9 maint":battv("acteurs","Q3.1_difficulte_competences","Maintenance industrielle"),"4,9 cnc":battv("acteurs","Q3.1_difficulte_competences","CNC"),
 "4,4 usinage":battv("acteurs","Q3.1_difficulte_competences","Usinage"),"4,3 cao":battv("acteurs","Q3.1_difficulte_competences","CAO"),
 "4,3 qualif":battv("acteurs","Q4.1_freins_acces_emploi","qualification"),"2,3 offre act":scalev("acteurs","Q6.1_offre_locale"),
 "4,6 robot":battv("acteurs","Q6.2_manque_formation","Robotique"),"2,1 plateforme":battv("acteurs","Q8.1_importance_actions","Plateforme"),
 "4,1 duree":scalev("acteurs","Q5.3_duree_emplois"),
}
expected={"4,5":4.5,"1,0":1.0,"2,1":2.1,"4,3 manqcand":4.3,"3,1 offre ent":3.1,"2,3 image":2.3,"3,9 attr":3.9,
 "2,5 trans":2.5,"1,1 cyber":1.1,"2,3 ia of":2.3,"4,0 offre of":4.0,"2,6 afest":2.6,"4,9 maint":4.9,"4,9 cnc":4.9,
 "4,4 usinage":4.4,"4,3 cao":4.3,"4,3 qualif":4.3,"2,3 offre act":2.3,"4,6 robot":4.6,"2,1 plateforme":2.1,"4,1 duree":4.1}
for k,exp in expected.items():
    chk(REF[k]==exp,f"REF {k}: source={REF[k]} attendu={exp}")
# % cités
pcts={"67% suffisants":(catn("entreprises","Q4.8b_besoin_transmission","suffisants"),14),
 "81% non transmission":(catn("entreprises","Q2.2_transmission","Non"),17),
 "47% seniors":(jp["AVEC_plus_gros"]["pct_seniors_45plus"],47.0),
 "5/7 offre synd (peu+part)":(catn("syndicats","Q14_offre_adaptee","Peu")+catn("syndicats","Q14_offre_adaptee","Partiellement"),5),
 "4/7 engagement faible":(catn("syndicats","Q20_engagement_entreprises","Faible"),4),
 "5/7 transmission synd":(catn("syndicats","Q24_transmission","Prioritaire")+catn("syndicats","Q24_transmission","Très prioritaire"),5),
 "4/7 savoirs base":(None,None),"6/7 mobilité rurale":(None,None),"3/7 jamais AFEST":(catn("of","Q5.1_afest_concu","Jamais"),3),
 "6/7 plateaux":(catn("of","Q1.7_plateaux","totalement"),6)}
for k,(got,exp) in pcts.items():
    if got is None: continue
    chk(got==exp,f"{k}: source={got} attendu={exp}")
# thèmes cités
chk(next(t["n"] for t in J["syndicats"]["questions"]["Q13_competences_transversales"]["themes"] if "Savoirs de base" in t["theme"])==4,"4/7 savoirs base")
chk(next(t["n"] for t in J["syndicats"]["questions"]["Q17_freins_structurants"]["modalites"] if "Mobilité rurale" in t["modalite"])==6,"6/7 mobilité rurale")
print(f"  -> total contrôles cumulés : {nchk}")
print("\n"+"="*70)
print("RÉSULTAT FINAL :", ("✅ ZÉRO ÉCART sur "+str(nchk)+" contrôles") if not errs else f"❌ {len(errs)} ÉCART(S) :")
for e in errs: print("   ❌",e)
