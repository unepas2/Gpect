#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 2 — SCRIPT MAÎTRE collège SYNDICATS / ORGA PRO (GPECT Issoudun). n=7.
Dominante qualitative : codage thématique + verbatims anonymisés.
Option 1 : agrégé sur 7 ; familles (patronal/salarié/consulaire) = grille de
lecture interne uniquement (pas de chiffrage par famille). Anonyme (SY01-SY07).
Écrit resultats_syndicats.json + rapport markdown."""
import json, re
import numpy as np, pandas as pd
from datetime import datetime, timezone

PATH="/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/574f81cd-04_syndicats.xlsx.xlsx"
OUT_JSON="/home/user/Gpect/analyse/resultats/resultats_syndicats.json"
OUT_MD="/home/user/Gpect/analyse/resultats/resultats_syndicats_rapport.md"
df=pd.read_excel(PATH,engine="openpyxl",dtype=object); c=list(df.columns); N=len(df)
assert N==7, f"PÉRIMÈTRE {N}!=7"

# --- Anonymisation des verbatims : aucun nom de tiers/personne dans les livrables ---
_ANON=[
 (re.compile(r"ecole\s+safran\s+universit[eé]",re.I),"l'école interne d'un grand groupe"),
 (re.compile(r"interne\s+à\s+safran",re.I),"interne à un grand groupe"),
 (re.compile(r"safran\s*/\s*vuitton",re.I),"deux grands donneurs d'ordre"),
 (re.compile(r"\b(safran|vuitton)\b",re.I),"un grand groupe industriel"),
 (re.compile(r"\b(trigano|tech\s*demi|st\s*lizaine)\b",re.I),"une entreprise locale"),
 (re.compile(r"\bleclerc\b",re.I),"une enseigne de distribution"),
 (re.compile(r"\b(manpower|adecco|triangle)\b",re.I),"une agence d'intérim"),
 (re.compile(r"\bafpa\b",re.I),"un organisme de formation national"),
 (re.compile(r"\bafpi\b",re.I),"un organisme de formation de branche"),
 (re.compile(r"\buimm\b",re.I),"une branche professionnelle"),
 (re.compile(r"\b(cpme|medef)\b",re.I),"une organisation patronale"),
 (re.compile(r"\bcpe\b\s*\(branche m[eé]tallurgie\)",re.I),"une branche professionnelle"),
 (re.compile(r"des\s+restos\s+du\s+c[oœ]ur",re.I),"d'une association caritative"),
 (re.compile(r"restos\s+du\s+c[oœ]ur",re.I),"une association caritative"),
 (re.compile(r"\s*\(alix\s+fouchon\)",re.I),""),
]
def anon(t):
    t=str(t)
    for p,r in _ANON: t=p.sub(r,t)
    return t

def r1(x): return None if x is None or (isinstance(x,float) and np.isnan(x)) else round(float(x),1)
def scale(idx,qid,lab):
    s=pd.to_numeric(df[c[idx]],errors="coerce").dropna()
    return {"qid":qid,"item":lab,"type":"echelle_1_5","intitule":str(c[idx]),"n":int(s.shape[0]),
            "moyenne":r1(s.mean()),"mediane":r1(s.median()),"min":int(s.min()),"max":int(s.max()),
            "ecart_type":r1(s.std(ddof=1)) if s.shape[0]>1 else None}
def cat(idx,qid,norm=None):
    s=df[c[idx]].dropna()
    if norm: s=s.map(norm)
    n=int(s.shape[0]); vc=s.value_counts()
    return {"qid":qid,"type":"choix_unique","intitule":str(c[idx]),"n_repondants":n,
            "modalites":[{"modalite":str(k),"n":int(v),"pct":r1(100*v/n)} for k,v in vc.items()]}
def multi(idx,qid,mods):
    s=df[c[idx]].dropna().astype(str); n=int(s.shape[0]); out=[]
    for lab,kw in mods:
        cnt=int(s.str.contains(kw,case=False,regex=True,na=False).sum())
        out.append({"modalite":lab,"n":cnt,"pct_repondants":r1(100*cnt/n)})
    return {"qid":qid,"type":"multi_select","intitule":str(c[idx]),"n_repondants":n,
            "modalites":sorted(out,key=lambda x:x["n"],reverse=True)}
def theme(idx,qid,themes):
    s=df[c[idx]].dropna().astype(str); n=int(s.shape[0]); out=[]
    for lab,pats in themes.items():
        mask=s.str.contains("|".join(pats),case=False,regex=True,na=False)
        out.append({"theme":lab,"n":int(mask.sum()),"pct":r1(100*mask.sum()/n)})
    out=sorted(out,key=lambda x:x["n"],reverse=True)
    return {"qid":qid,"type":"texte_libre_code","intitule":str(c[idx]),"n_repondants":n,
            "themes":out,"verbatims_anonymises":[anon(str(v).strip()) for v in df[c[idx]].dropna().tolist()]}
def verb(idx,qid):
    return {"qid":qid,"type":"texte_libre","intitule":str(c[idx]),
            "n_repondants":int(df[c[idx]].notna().sum()),
            "verbatims_anonymises":[anon(str(v).strip()) for v in df[c[idx]].dropna().tolist()]}

R={"_meta":{"college":"Syndicats / organisations professionnelles","n_repondants":N,
    "source":PATH.split("/")[-1],"source_date":"2026-04/05 (collecte) / export 2026-06-28",
    "genere_le":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "composition_interne":"3 organisations patronales, 2 syndicats de salariés, 2 organismes consulaires (chambres)",
    "note_option_1":"Agrégé sur 7. Familles = grille de lecture qualitative interne, sans chiffrage par famille (anonymat à n=2-3).",
    "avertissement":"n=7, dominante qualitative : thèmes + verbatims, aucune généralisation."},
   "questions":{}}
q=R["questions"]
_norm04=lambda x:("Organisation consulaire" if ("cci" in str(x).lower() or "consulaire" in str(x).lower())
                  else ("Organisation professionnelle / syndicale" if "professionnelle" in str(x).lower() else str(x)))
_norm05=lambda x:("Intercommunalité" if "commun" in str(x).lower() else str(x))
q["Q04_type_acteur"]=cat(4,"Q04",norm=_norm04)
q["Q05_territoire"]=cat(5,"Q05",norm=_norm05)
q["Q06_dynamique_eco"]=scale(6,"Q06","Dynamique économique du bassin (1 faible→5 forte)")
q["Q07_coordination_acteurs"]=scale(7,"Q07","Coordination entre acteurs économiques (1→5)")
q["Q08_atouts"]=theme(8,"Q08",{
    "Foncier disponible / prix": [r"foncier"],
    "Axes routiers / logistique / accessibilité": [r"routi", r"autorout", r"logisti", r"a[eé]roport", r"axe"],
    "Qualité de vie": [r"qualit[eé] de vie"],
    "Tissu industriel implanté / diversifié": [r"tissu", r"industr", r"diversifi", r"safran", r"trigano"],
    "Proximité pouvoirs publics / coordination": [r"pouvoirs publics", r"coordination", r"r[eé]seau"],
    "Atouts numériques (data center)": [r"data center"],
})
q["Q09_freins"]=theme(9,"Q09",{
    "Transport / accessibilité / réseau routier": [r"transport", r"routi", r"accessibilit", r"train", r"voiture"],
    "Logement": [r"logement"],
    "Qualification / main d'œuvre / compétences absentes": [r"qualification", r"main d", r"comp[eé]tences non", r"comp[eé]tences non pr", r"candidat"],
    "Démographie / vieillissement": [r"d[eé]mograph", r"vieilliss"],
    "Désertification médicale / santé": [r"m[eé]dical", r"sant[eé]"],
    "Mobilisation / accès aux entreprises": [r"mobiliser", r"rencontrer les entreprises"],
    "Fiscalité / financement / banques": [r"fiscalit", r"banque", r"financ"],
    "Énergie (puissance électrique)": [r"[eé]lectric", r"puissance"],
    "Orientation scolaire / image des métiers": [r"orientation", r"[eé]ducation nationale", r"d[eé]valoris", r"m[eé]tiers manuels"],
})
q["Q10_metiers_tension"]=theme(10,"Q10",{
    "Usinage / fraiseur / tourneur / ajusteur": [r"usinage", r"fraiseur", r"tourneur", r"ajusteur", r"chaudron"],
    "Maintenance": [r"maintenance"],
    "Qualité / méthodes / contrôle": [r"qualit", r"m[eé]thode", r"contr[oô]leur"],
    "Encadrement / management": [r"encadrement", r"manager", r"management"],
    "Métiers manuels (génériques)": [r"m[eé]tiers manuels", r"manuel"],
    "Aéronautique / défense / CATIA": [r"a[eé]ronaut", r"d[eé]fense", r"catia", r"conception"],
    "Automobile": [r"automobile"],
    "Bâtiment / BTP": [r"batiment", r"b[aâ]timent"],
    "Restauration / services": [r"restauration", r"services", r"propret[eé]"],
    "Production / opérateurs / monteurs": [r"op[eé]rateur", r"monteur", r"production"],
})
q["Q11_besoins_identifies"]=cat(11,"Q11")
q["Q12_competences_techniques"]=theme(12,"Q12",{
    "Mécanique / usinage / productique": [r"m[eé]canique", r"usinage", r"productique", r"g[eé]nie m[eé]ca"],
    "Qualité / méthodes": [r"qualit", r"m[eé]thode"],
    "Robotique / automatisation": [r"robot", r"automat"],
    "IA / digitalisation / numérique": [r"intelligence artificielle", r"\bIA\b", r"digital", r"num[eé]rique"],
    "Conception assistée (CATIA)": [r"catia", r"conception assist"],
    "Maintenance": [r"maintenance"],
    "Métiers manuels": [r"manuel"],
})
q["Q13_competences_transversales"]=theme(13,"Q13",{
    "Savoirs de base (lire/écrire/compter)": [r"lire", r"[eé]crire", r"compter", r"savoir de base", r"comp[eé]tences [eé]l[eé]mentaires", r"niveau scolaire", r"calcul"],
    "Savoir-être": [r"savoir.?[eê]tre"],
    "Motivation / valeur travail / engagement": [r"motivation", r"valeur travail", r"engagement", r"effort"],
    "Anglais / langues": [r"anglais", r"langue"],
    "Mobilité (permis, véhicule)": [r"mobilit", r"permis", r"v[eé]hicule"],
    "Communication écoles / experts métiers": [r"communication entre", r"experts m[eé]tiers"],
})
q["Q14_offre_adaptee"]=cat(14,"Q14")
q["Q15_freins_formation"]=theme(15,"Q15",{
    "Éducation nationale / orientation / présentation métiers": [r"[eé]ducation nationale", r"pr[eé]sente pas", r"orientation"],
    "Méconnaissance des OF": [r"connaissance.*OF", r"pas de connaissances sur les OF"],
    "Disparition d'organismes (réseau national → branches)": [r"afpa", r"afpi"],
    "Lenteur administrative / financement / valeur des diplômes": [r"administ", r"financ", r"valeur des dipl"],
    "Tutorat / concertation amont entreprises-OF": [r"tutorat", r"concertation", r"amont"],
    "Intégration / maintien en formation / effectifs": [r"int[eé]gration", r"effectifs", r"promotion", r"cursus", r"stagiaires"],
    "Débouchés / concurrence CFA": [r"d[eé]bouche", r"concurrence"],
})
q["Q16_evolutions_offre"]=theme(16,"Q16",{
    "Apprentissage / alternance / contrat pro": [r"apprentissage", r"alternance", r"professionnalisation"],
    "Formation interne / écoles d'entreprise / tuteurs": [r"interne", r"tuteur", r"[eé]cole"],
    "Renforcement des compétences de base / niveau": [r"comp[eé]tences de base", r"niveau", r"intensiv"],
    "Formations courtes": [r"courte"],
    "Orientation collège / découverte métiers": [r"orientation", r"coll[eè]ge", r"r[eé]alit[eé] augment", r"portrait"],
    "Adapter aux besoins du terrain": [r"adapter", r"besoins d[eé]tect", r"terrain"],
})
q["Q17_freins_structurants"]=multi(17,"Q17",[
    ("Mobilité rurale","Mobilit[eé] rurale"),("Logement cher / mauvais état","Logement cher"),
    ("Compétences de base","Comp[eé]tences de base"),("Motivation des personnes","Motivation"),
    ("Orientation","Orientation"),("Freins sociaux","Freins sociaux"),
    ("Niveau scolaire faible (jeunes)","niveau scolaire")])
q["Q18_mobilite_frein"]=scale(18,"Q18","Mobilité comme frein à l'emploi (1 faible→5 majeur)")
q["Q19_solutions_mobilite"]=theme(19,"Q19",{
    "Transport adapté / navette / bus gare-zones": [r"transport", r"navette", r"bus", r"desserte", r"gare"],
    "Hébergement / colocation / habitat partagé": [r"h[eé]bergement", r"coloc", r"appart", r"habitat", r"auberge"],
    "Aides financières à la mobilité": [r"aide", r"financement"],
    "Réapprendre à se déplacer": [r"r[eé]apprendre", r"se d[eé]placer"],
})
q["Q20_engagement_entreprises"]=cat(20,"Q20")
q["Q21_freins_mobilisation"]=theme(21,"Q21",{
    "Manque de temps / sursollicitation": [r"temps", r"sollicitation", r"saturation"],
    "Réunions sans résultat concret": [r"m[eè]nent à rien", r"r[eé]sultat"],
    "Concurrence / manque de collaboration inter-entreprises": [r"concurrence", r"collaboration"],
    "Manque de ressources internes": [r"ressources internes", r"ressources"],
    "Anxiété économique / carnet de commandes": [r"anxi[eé]t", r"commande"],
    "Autarcie / méfiance historique du tissu": [r"autarcie", r"mainmise", r"historique"],
})
q["Q22_formats_animation"]=theme(22,"Q22",{
    "Ateliers courts / par thème": [r"atelier", r"court", r"th[eè]me", r"th[eé]matique"],
    "Avec représentants institutionnels / élus": [r"institutionnel", r"pr[eé]fet", r"[eé]lus", r"CMA"],
    "Conditionné à un résultat concret": [r"r[eé]sultat concret", r"r[eé]sultat"],
    "Mobiliser les branches": [r"branche"],
    "Réserve / ne sait pas": [r"ne sait pas", r"\bRAS\b"],
})
q["Q23_themes_engagement"]=theme(23,"Q23",{
    "Attractivité du territoire": [r"attractivit"],
    "Transmission": [r"transmission"],
    "Logement": [r"logement"],
    "Compétences / RH": [r"comp[eé]tences", r"\bRH\b", r"ardan"],
    "RSE / DUERP / santé-sécurité": [r"rse", r"duerp"],
    "Innovation / diversification": [r"innovation", r"diversif"],
    "Motivation des salariés": [r"motivation", r"envie"],
})
q["Q24_transmission"]=cat(24,"Q24")
q["Q25_besoins_transmission"]=theme(25,"Q25",{
    "Accompagnement (générique)": [r"accompagn"],
    "Viviers de repreneurs / détection": [r"vivier", r"repreneur", r"d[eé]tection", r"urssaf"],
    "Aides aux petites entreprises": [r"aide", r"petite"],
    "Formation gestion / RH pour reprise": [r"gestion", r"\bRH\b", r"montée en comp", r"banque"],
})
q["Q26_action_prioritaire"]=verb(26,"Q26")
q["Q27_actions_rapides"]=verb(27,"Q27")
q["Q28_resultats_attendus"]=verb(28,"Q28")
q["Q29_remarques"]=verb(29,"Q29")

recap=[{"qid":v["qid"],"item":v["item"],"moyenne":v["moyenne"],"mediane":v["mediane"],
        "ecart_type":v["ecart_type"],"n":v["n"]} for v in q.values() if v.get("type")=="echelle_1_5"]
R["recap_echelles"]=recap
json.dump(R,open(OUT_JSON,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("OK -> resultats_syndicats.json | n=",N,"| échelles",len(recap),"| questions",len(q))
