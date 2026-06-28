#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉTAPE 2 — SCRIPT MAÎTRE collège ORGANISMES DE FORMATION (GPECT Issoudun).
n=7. Questions OF-spécifiques (capacité à former / offre / AFEST) calculées
AVEC les 7 ET SANS le financeur non-dispensateur (option B validée).
Écrit resultats_of.json + rapport markdown. Multi-select via contains. n= partout.
"""
import json, re
import numpy as np, pandas as pd
from datetime import datetime, timezone

PATH = "/root/.claude/uploads/1447a9c7-2762-5c18-91a7-363f75a8a110/677aa4a6-02_organismes_formation.xlsx.xlsx"
OUT_JSON = "/home/user/Gpect/analyse/resultats/resultats_of.json"
OUT_MD = "/home/user/Gpect/analyse/resultats/resultats_of_rapport.md"

df = pd.read_excel(PATH, engine="openpyxl", dtype=object)
cols = list(df.columns); N = len(df)
assert N == 7, f"PÉRIMÈTRE INVALIDE : {N} != 7"
FIN = list(df.index[df[cols[9]].astype(str).str.contains("Collectivit|financeur", case=False, na=False)])
FIN_IDX = FIN[0] if FIN else None
disp_idx = [i for i in df.index if i != FIN_IDX]  # dispensateurs

def r1(x): return None if x is None or (isinstance(x,float) and np.isnan(x)) else round(float(x),1)

def scale_one(idx, idx_list):
    s = pd.to_numeric(df.loc[idx_list, cols[idx]], errors="coerce").dropna()
    if s.empty: return {"n":0,"moyenne":None,"mediane":None,"min":None,"max":None,"ecart_type":None}
    return {"n":int(s.shape[0]),"moyenne":r1(s.mean()),"mediane":r1(s.median()),
            "min":int(s.min()),"max":int(s.max()),
            "ecart_type":r1(s.std(ddof=1)) if s.shape[0]>1 else None}

def scale_stats(idx, qid, with_without=False):
    d={"qid":qid,"type":"echelle_1_5","intitule":str(cols[idx]),**scale_one(idx,list(df.index))}
    if with_without and FIN_IDX is not None:
        d["sans_financeur"]=scale_one(idx,disp_idx)
    return d

def battery(idx_range, qid, base, with_without=False):
    items=[]
    for i in idx_range:
        sub=re.search(r"\[(.+)\]",str(cols[i])); lab=sub.group(1) if sub else str(cols[i])
        it={"item":lab, **scale_one(i,list(df.index))}
        if with_without and FIN_IDX is not None:
            it["sans_financeur"]=scale_one(i,disp_idx)
        items.append(it)
    classt=sorted(items,key=lambda x:x["moyenne"] if x["moyenne"] is not None else -1,reverse=True)
    return {"qid":qid,"type":"batterie_echelle_1_5","intitule":base,"n_items":len(items),
            "items":items,"classement_par_moyenne":classt}

def cat_counts(idx, qid, normalize=None):
    s=df[cols[idx]].dropna()
    if normalize: s=s.map(normalize)
    n=int(s.shape[0]); vc=s.value_counts()
    return {"qid":qid,"type":"choix_unique","intitule":str(cols[idx]),"n_repondants":n,
            "modalites":[{"modalite":str(k),"n":int(v),"pct":r1(100*v/n)} for k,v in vc.items()]}

def multi_counts(idx, qid, modalites):
    s=df[cols[idx]].dropna().astype(str); n=int(s.shape[0]); out=[]
    for lab,kw in modalites:
        c=int(s.str.contains(re.escape(kw),case=False,na=False).sum())
        out.append({"modalite":lab,"n":c,"pct_repondants":r1(100*c/n)})
    out=sorted(out,key=lambda x:x["n"],reverse=True)
    return {"qid":qid,"type":"multi_select","intitule":str(cols[idx]),"n_repondants":n,"modalites":out}

def numeric_text(idx, qid):
    raw=df[cols[idx]]; num=pd.to_numeric(raw,errors="coerce")
    nn=raw[raw.notna()&num.isna()]; s=num.dropna()
    return {"qid":qid,"type":"numerique","intitule":str(cols[idx]),"n_numerique":int(s.shape[0]),
            "valeurs_non_numeriques":[str(x) for x in nn.tolist()],
            "valeurs_numeriques":sorted([int(x) if float(x).is_integer() else float(x) for x in s.tolist()]),
            "mediane":r1(s.median()),"min":r1(s.min()),"max":r1(s.max()),"somme":r1(s.sum())}

def verbatims(idx, qid):
    return {"qid":qid,"type":"texte_libre","intitule":str(cols[idx]),
            "n_repondants":int(df[cols[idx]].notna().sum()),
            "verbatims_anonymises":[str(v).strip() for v in df[cols[idx]].dropna().tolist()]}

R={"_meta":{"college":"Organismes de formation","n_repondants":N,
    "source":PATH.split("/")[-1],"source_date":"2026-04/05 (collecte) / export 2026-06-28",
    "genere_le":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "financeur_non_dispensateur_ligne_interne":FIN_IDX,
    "note_option_B":"Questions OF-spécifiques calculées AVEC 7 et SANS financeur (n=6).",
    "avertissement":"n=7 : aucune généralisation. Effectifs bruts prioritaires sur les %."},
   "questions":{}}
q=R["questions"]

# Q0
q["Q0.7_type"]=cat_counts(9,"Q0.7")
q["Q0.8_qualiopi"]=cat_counts(11,"Q0.8")
q["Q0.9_cpf"]=cat_counts(12,"Q0.9")
q["Q0.10_perimetre"]=multi_counts(13,"Q0.10",[
    ("Issoudun et agglomération","Issoudun et son agglom"),("Indre hors Issoudun","hors Issoudun"),
    ("Région Centre-Val de Loire","Centre-Val de Loire"),("National","National")])
q["Q0.11_presence_issoudun"]=cat_counts(14,"Q0.11")
# Q1
q["Q1.1_publics"]=multi_counts(15,"Q1.1",[
    ("Scolaires / lycéens","Scolaires"),("Demandeurs d'emploi","Demandeurs d'emploi"),
    ("Salariés en poste (continue)","Salariés en poste"),("Jeunes en alternance","alternance"),
    ("Reconversion professionnelle","reconversion"),("Indépendants / dirigeants","indépendants"),
    ("Situation de handicap","situation de handicap"),("Allophones / sous main de justice","allophones")])
q["Q1.2_type_formations"]=multi_counts(16,"Q1.2",[
    ("Initiales (scolaires)","Initiales"),("Continues (adultes)","Continues"),("En alternance","alternance"),
    ("Certifiantes / diplômantes","Certifiantes"),("Courtes / modulaires","Courtes"),
    ("Sur mesure / intra","Sur mesure"),("Blocs de compétences","Blocs de comp"),("VAE","VAE")])
q["Q1.3_niveaux"]=multi_counts(17,"Q1.3",[
    ("Infra-bac","Infra-bac"),("CAP / BEP","CAP / BEP"),("Baccalauréat","Baccalauréat"),
    ("BTS / BUT","BTS / BUT"),("Licence / Bachelor","Licence")])
q["Q1.4_capacite"]=cat_counts(18,"Q1.4")
q["Q1.5_formateurs_internes"]=numeric_text(19,"Q1.5")
q["Q1.6_formateurs_externes"]=numeric_text(20,"Q1.6")
q["Q1.7_plateaux"]=cat_counts(21,"Q1.7")
q["Q1.8_equipements"]=verbatims(22,"Q1.8")
# Q2 — OF-spécifique with/without
q["Q2.1_niveau_offre"]=battery(range(23,35),"Q2.1","Niveau de l'offre actuelle par domaine (1 faible→5 fort)",with_without=True)
q["Q2.2_capacite_emergentes"]=battery(range(35,43),"Q2.2","Capacité à former aux compétences émergentes (1→5)",with_without=True)
q["Q2.3_sur_mesure"]=cat_counts(43,"Q2.3")
# Q3
q["Q3.1_connaissance_besoins"]=scale_stats(44,"Q3.1",with_without=True)
q["Q3.2_sources"]=multi_counts(45,"Q3.2",[
    ("Contacts directs entreprises","Contacts directs"),("Instances locales (clubs, syndicats)","instances locales"),
    ("Données France Travail / observatoires","France Travail / observatoires"),
    ("Veille sectorielle (OPCO, branches)","Veille sectorielle"),
    ("Retours d'alternants / stagiaires","Retours d'alternants"),("Études sectorielles / CCI","Études sectorielles")])
q["Q3.3_connaissance_secteurs"]=battery(range(46,54),"Q3.3","Connaissance par secteur du bassin (1→5)",with_without=True)
q["Q3.4_metiers_tension"]=verbatims(54,"Q3.4")
# Q4
q["Q4.1_offre_couvre"]=scale_stats(55,"Q4.1",with_without=True)
q["Q4.2_retours_clients"]=scale_stats(56,"Q4.2",with_without=True)
q["Q4.3_points_inadaptes"]=multi_counts(57,"Q4.3",[
    ("Éloignement géographique","Éloignement"),("Coût pédagogique trop élevé PME","Coût pédagogique"),
    ("Niveaux de qualification non adaptés","Niveaux de qualification"),
    ("Durée des parcours trop rigide","Durée des parcours"),("Volume de sessions insuffisant","Volume de sessions"),
    ("Aucune lacune identifiée","Aucune lacune")])
q["Q4.4_metiers_a_adapter"]=verbatims(59,"Q4.4")
# Q5 — AFEST
q["Q5.1_afest_concu"]=cat_counts(60,"Q5.1")
q["Q5.2_maitrise_afest"]=scale_stats(61,"Q5.2",with_without=True)
q["Q5.3_freins_afest"]=multi_counts(62,"Q5.3",[
    ("Résistance / méconnaissance des entreprises","Résistance ou méconnaissance"),
    ("Complexité du référentiel et traçabilité","Complexité du référentiel"),
    ("Absence de modèle économique viable","modèle économique"),
    ("Difficulté à identifier les situations apprenantes","situations apprenantes"),
    ("Méconnaissance par les OPCO locaux","OPCO locaux"),
    ("Pas de demandes / manque de personnel","Pas de demandes")])
q["Q5.4_formes_adaptation"]=multi_counts(64,"Q5.4",[
    ("Création de nouveaux modules","Création de nouveaux modules"),("Révision de contenus","Révision de contenus"),
    ("Modularisation / blocs","Modularisation"),("Formation sur mesure intra","sur mesure intra"),
    ("Renforcement de l'alternance","Renforcement de l'alternance"),
    ("Intervention en entreprise","Intervention directement"),("Co-animation avec professionnels","Co-animation"),
    ("Aucune adaptation réalisée","Aucune adaptation")])
q["Q5.5_pret_evoluer"]=cat_counts(65,"Q5.5")
# Q6
q["Q6.1_cooperation"]=scale_stats(67,"Q6.1",with_without=True)
q["Q6.2_acteurs"]=multi_counts(68,"Q6.2",[
    ("France Travail","France Travail"),("Mission Locale de l'Indre","Mission Locale"),
    ("Cap Emploi","Cap Emploi"),("OPCO","OPCO"),("Autres OF","Autres organismes de formation"),
    ("Collectivités (CC/Dép./Région)","Collectivités"),("Chambres consulaires (CCI/CMA)","Chambres consulaires"),
    ("Entreprises locales (directement)","Entreprises locales")])
q["Q6.3_formes_coop"]=multi_counts(70,"Q6.3",[
    ("Co-construction de contenus","Co-construction"),("Accueil d'alternants","Accueil d'alternants"),
    ("Visites / immersions","Visites / immersions"),("Intervention de professionnels","Intervention de professionnels"),
    ("Recrutement direct en sortie","Recrutement direct"),("Suivi de cohortes / insertion","Suivi de cohortes"),
    ("Comités de pilotage / instances","Comités de pilotage")])
q["Q6.4_actions_collectives"]=cat_counts(71,"Q6.4")
# Q7
q["Q7.1_freins_offre"]=multi_counts(73,"Q7.1",[
    ("Manque de financements ingénierie","financements pour l'ingénierie"),
    ("Plateaux techniques absents/vétustes","plateaux techniques"),
    ("Difficulté à mobiliser les entreprises","mobiliser les entreprises"),
    ("Faible attractivité de certains métiers","Faible attractivité"),
    ("Manque de RH internes","ressources humaines internes"),
    ("Contraintes réglementaires / certif","Contraintes réglementaires"),
    ("Concurrence entre OF","Concurrence entre organismes"),
    ("Faible volume de demande","Faible volume de demande")])
q["Q7.2_leviers"]=multi_counts(75,"Q7.2",[
    ("Plateforme mutualisée de plateaux techniques","Plateforme mutualisée"),
    ("Parcours communs entre OF","parcours communs entre OF"),
    ("Ingénierie partagée avec entreprises","Ingénierie partagée"),
    ("Réseau structuré d'acteurs locaux","Réseau structuré"),
    ("Financement dédié adaptation pédago","Financement dédié"),
    ("Outil de repérage/orientation publics","repérage et d'orientation"),
    ("Cartographie partagée de l'offre","Cartographie partagée"),
    ("Observatoire local des métiers","Observatoire local")])
# Q8
q["Q8.1_anticipation_besoins"]=scale_stats(76,"Q8.1")
q["Q8.2_domaines_evolutions"]=multi_counts(77,"Q8.2",[
    ("Intelligence artificielle","Intelligence artificielle"),
    ("Automatisation / cobotique / robotique","Automatisation"),
    ("Maintenance avancée et prédictive","Maintenance avancée"),
    ("Transition énergétique et décarbonation","Transition énergétique"),
    ("Cybersécurité industrielle","Cybersécurité"),("Management de la performance","Management de la performance"),
    ("Conduite du changement / projet","Conduite du changement"),
    ("Transmission des savoir-faire / tutorat","Transmission des savoir-faire"),
    ("Anglais / compétences transversales","Anglais")])
q["Q8.3_nouvelles_formations"]=cat_counts(78,"Q8.3")
q["Q8.5_transfo_internes"]=multi_counts(80,"Q8.5",[
    ("Offre digitale / e-learning","digitale / e-learning"),
    ("Nouvelles filières / certifications","nouvelles filières"),
    ("Extension géographique","Extension géographique"),
    ("Renforcement partenariats entreprises","partenariats entreprises"),
    ("Mutualisation avec d'autres OF","Mutualisation avec d'autres"),
    ("Embauche de formateurs","Embauche de nouveaux formateurs"),
    ("Investissement plateaux techniques","Investissement plateaux"),
    ("Aucune transformation prévue","Aucune transformation")])
# Q9
q["Q9.1_priorites_gpect"]=battery(range(81,89),"Q9.1","Priorités GPECT (1 faible→5 très haute)")
q["Q9.2_roles"]=multi_counts(89,"Q9.2",[
    ("Informer sur l'offre existante","Informer sur l'offre"),
    ("Adapter l'offre aux besoins","Adapter l'offre"),
    ("Co-construire des parcours","Co-construire des parcours"),
    ("Accueillir alternance / VAE","alternance ou en VAE"),
    ("Participer à des groupes de travail","groupes de travail"),
    ("Contribuer à l'attractivité (lycées)","attractivité des métiers"),
    ("Animer des ateliers de sensibilisation","ateliers de sensibilisation"),
    ("Déployer des parcours AFEST","parcours AFEST")])
q["Q9.3_ateliers"]=multi_counts(90,"Q9.3",[
    ("Métiers sensibles & compétences clés","Métiers sensibles"),
    ("Attractivité et recrutement territorial","Attractivité et recrutement"),
    ("Formation & ingénierie pédagogique mutualisée","ingénierie pédagogique"),
    ("Transmission savoir-faire & seniors","Transmission des savoir-faire et gestion"),
    ("Industrie 4.0 et compétences de demain","Industrie 4.0"),("Ne souhaite pas participer","ne souhaite pas")])
# Q10
q["Q10.1_image"]=scale_stats(91,"Q10.1")
q["Q10.2_freins_territoire"]=multi_counts(92,"Q10.2",[
    ("Logement insuffisant/cher","logement"),("Soins et santé insuffisants","soins et de santé"),
    ("Transports / mobilité","transports en commun"),("Emploi du conjoint difficile","emploi pour le conjoint"),
    ("Services à la personne (crèches/gardes)","services à la personne"),
    ("Image du territoire peu attractive","Image globale"),("Animation culturelle/sportive","animation culturelle"),
    ("Aucun frein territorial","Aucun frein territorial")])
q["Q10.3_actions_attractivite"]=multi_counts(93,"Q10.3",[
    ("Promotion métiers industriels (scolaires)","Promotion des métiers"),
    ("Visites / portes ouvertes coordonnées","Visites d'entreprises"),
    ("Campagne de communication commune","Campagne de communication"),
    ("Participation à un groupement d'employeurs","groupement d'employeurs"),
    ("Ateliers inter-entreprises RH","Ateliers inter-entreprises"),
    ("Pas d'intérêt","pas d'intérêt")])
# Q11
q["Q11.1_action_utile"]=verbatims(94,"Q11.1")
q["Q11.3_souhaite_synthese"]=cat_counts(96,"Q11.3")
q["Q11.4_observations"]=verbatims(97,"Q11.4")

# récap échelles
recap=[]
for k,v in q.items():
    if v.get("type")=="echelle_1_5":
        recap.append({"qid":v["qid"],"item":"—","moyenne":v["moyenne"],"mediane":v["mediane"],
                      "ecart_type":v["ecart_type"],"n":v["n"],
                      "moy_sans_financeur":v.get("sans_financeur",{}).get("moyenne")})
    elif v.get("type")=="batterie_echelle_1_5":
        for it in v["items"]:
            recap.append({"qid":v["qid"],"item":it["item"],"moyenne":it["moyenne"],"mediane":it["mediane"],
                          "ecart_type":it["ecart_type"],"n":it["n"],
                          "moy_sans_financeur":it.get("sans_financeur",{}).get("moyenne")})
R["recap_echelles"]=recap

json.dump(R,open(OUT_JSON,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("OK -> resultats_of.json")
print("n=",N,"| financeur ligne interne =",FIN_IDX,"| dispensateurs n=",len(disp_idx))
print("nb échelles récap =",len(recap))
