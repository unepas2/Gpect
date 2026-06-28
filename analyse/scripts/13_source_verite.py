#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ANALYSE TERRITORIALE CROISÉE — construit source_verite.json (+ .md).
Lit UNIQUEMENT les 4 resultats_*.json déjà figés. Aucun recalcul des données
sources ; les seuls calculs sont des JUXTAPOSITIONS et des ÉCARTS (max-min)
entre indicateurs déjà produits. Chaque valeur référence sa source (collège+qid).
"""
import json
from datetime import datetime, timezone
RES="/home/user/Gpect/analyse/resultats/"
E=json.load(open(RES+"resultats_entreprises.json",encoding="utf-8"))
O=json.load(open(RES+"resultats_of.json",encoding="utf-8"))
A=json.load(open(RES+"resultats_acteurs.json",encoding="utf-8"))
S=json.load(open(RES+"resultats_syndicats.json",encoding="utf-8"))
COL={"entreprises":E,"of":O,"acteurs":A,"syndicats":S}

# ---------- fetchers (lecture seule dans les JSON) ----------
def scale(j,qk):
    d=j["questions"][qk]; assert d["type"]=="echelle_1_5",qk
    return d
def batt_item(j,qk,sub):
    d=j["questions"][qk]
    for it in d["items"]:
        if sub.lower() in it["item"].lower(): return it
    raise KeyError(f"{qk} / {sub}")
def cat_mod(j,qk,sub):
    d=j["questions"][qk]
    for m in d["modalites"]:
        if sub.lower() in m["modalite"].lower(): return m
    raise KeyError(f"{qk} / {sub}")
def multi_mod(j,qk,sub): return cat_mod(j,qk,sub)
def theme(j,qk,sub):
    d=j["questions"][qk]
    for t in d["themes"]:
        if sub.lower() in t["theme"].lower(): return t
    raise KeyError(f"{qk} / {sub}")

def ecart(vals):
    nums=[v for v in vals.values() if isinstance(v,(int,float))]
    return round(max(nums)-min(nums),1) if len(nums)>=2 else None

SV={"_meta":{
    "titre":"GPECT Issoudun — Source de vérité (analyse territoriale croisée)",
    "genere_le":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "regle":"Construit uniquement à partir des 4 resultats_*.json. Écarts = max-min d'indicateurs déjà calculés. Agrégé, anonyme.",
    "colleges":{"entreprises":{"n":E["_meta"]["n_repondants"],"libelle":"Entreprises"},
                "of":{"n":O["_meta"]["n_repondants"],"libelle":"Organismes de formation"},
                "acteurs":{"n":A["_meta"]["n_repondants"],"libelle":"Acteurs de l'emploi"},
                "syndicats":{"n":S["_meta"]["n_repondants"],"libelle":"Syndicats / orga pro"}},
    "total_repondants":E["_meta"]["n_repondants"]+O["_meta"]["n_repondants"]+A["_meta"]["n_repondants"]+S["_meta"]["n_repondants"],
    "avertissement":"3 collèges à n=7 : lecture en tendances et convergences, pas de généralisation."
}}

# =================================================================
# 1) DICTIONNAIRE DES QUESTIONS PARTAGÉES + 2) ÉCARTS DE PERCEPTION
# =================================================================
dims=[]

# --- Offre de formation locale : adéquation perçue (échelle 1-5 + catégoriel)
of_offre = round((scale(O,"Q4.1_offre_couvre")["moyenne"]+O["questions"]["Q4.1_offre_couvre"]["sans_financeur"]["moyenne"])/1,1)
dims.append({
 "dimension":"Adéquation de l'offre de formation locale",
 "echelle":"1-5 (5=très adaptée) ; Syndicats = catégoriel",
 "valeurs":{
   "of":scale(O,"Q4.1_offre_couvre")["moyenne"],
   "entreprises":scale(E,"Q7.6_offre_adaptee")["moyenne"],
   "acteurs":scale(A,"Q6.1_offre_locale")["moyenne"],
   "syndicats":None},
 "detail":{"of_sans_financeur":O["questions"]["Q4.1_offre_couvre"]["sans_financeur"]["moyenne"],
           "of_retours_clients":scale(O,"Q4.2_retours_clients")["moyenne"],
           "syndicats_peu_ou_partiellement_adaptee_n":cat_mod(S,"Q14_offre_adaptee","Peu")["n"]+cat_mod(S,"Q14_offre_adaptee","Partiellement")["n"],
           "syndicats_globalement_adaptee_n":cat_mod(S,"Q14_offre_adaptee","Globalement")["n"]},
 "sources":{"of":"Q4.1","entreprises":"Q7.6","acteurs":"Q6.1","syndicats":"Q14"},
 "lecture":"Les producteurs de formation (OF) s'auto-évaluent nettement mieux (4.0, 4.3 hors financeur) que leurs 'clients' : entreprises 3.1, acteurs 2.3 ; 5/7 syndicats jugent l'offre peu/partiellement adaptée."})
dims[-1]["ecart"]=ecart(dims[-1]["valeurs"])

# --- Image / attractivité du territoire (échelle 1-5)
dims.append({
 "dimension":"Image / attractivité perçue du territoire",
 "echelle":"1-5 (5=très attractive)",
 "valeurs":{"entreprises":scale(E,"Q8.2_image_issoudun")["moyenne"],
            "of":scale(O,"Q10.1_image")["moyenne"],
            "acteurs":None,"syndicats":None},
 "detail":{"entreprises_image_citee_comme_frein_pct":multi_mod(E,"Q8.1_facteurs_territoire","Image du territoire")["pct_repondants"],
           "of_image_frein_pct":multi_mod(O,"Q10.2_freins_territoire","Image du territoire")["pct_repondants"],
           "syndicats_dynamique_eco":scale(S,"Q06_dynamique_eco")["moyenne"]},
 "sources":{"entreprises":"Q8.2","of":"Q10.1"},
 "lecture":"Image jugée basse par les entreprises (2.3, jamais >3) et un peu moins par les OF côté stagiaires (3.1). Frein 'image' cité par 95% des entreprises, 71% des OF."})
dims[-1]["ecart"]=ecart(dims[-1]["valeurs"])

# --- Mobilité comme frein (échelle 1-5)
dims.append({
 "dimension":"Mobilité / transport comme frein à l'emploi",
 "echelle":"1-5 (5=frein majeur)",
 "valeurs":{"entreprises":batt_item(E,"Q5.3_freins_recrutement","Problèmes de mobilité")["moyenne"],
            "acteurs":batt_item(A,"Q4.1_freins_acces_emploi","Mobilité et accès")["moyenne"],
            "syndicats":scale(S,"Q18_mobilite_frein")["moyenne"],"of":None},
 "detail":{"syndicats_mobilite_rurale_n":multi_mod(S,"Q17_freins_structurants","Mobilité rurale")["n"],
           "of_transports_frein_pct":multi_mod(O,"Q10.2_freins_territoire","Transports")["pct_repondants"],
           "acteurs_inadequation_mobilite":batt_item(A,"Q2.2_facteurs_inadequation","mobilité ou de transport")["moyenne"]},
 "sources":{"entreprises":"Q5.3","acteurs":"Q4.1","syndicats":"Q18"},
 "lecture":"Écart de perception net : les entreprises minimisent la mobilité comme frein au recrutement (2.1) alors que les acteurs (3.7) et les syndicats (3.3 ; mobilité rurale 6/7) la placent au premier plan."})
dims[-1]["ecart"]=ecart(dims[-1]["valeurs"])

# --- Engagement des entreprises dans le collectif (perçu)
dims.append({
 "dimension":"Engagement des entreprises dans les démarches collectives",
 "echelle":"mixte (déclaratif entreprises vs perception syndicats)",
 "valeurs":{"entreprises":None,"syndicats":None,"of":None,"acteurs":None},
 "detail":{"entreprises_pret_campagne_com_pct":multi_mod(E,"Q8.3_actions_collectives","Campagne de communication")["pct_repondants"],
           "entreprises_pret_plateforme_pct":multi_mod(E,"Q8.3_actions_collectives","Plateforme de recrutement")["pct_repondants"],
           "entreprises_ne_souhaite_pas_atelier_pct":multi_mod(E,"Q9.2_ateliers","Ne souhaite pas")["pct_repondants"],
           "syndicats_engagement_faible_n":cat_mod(S,"Q20_engagement_entreprises","Faible")["n"],
           "acteurs_anticipation_besoins_public":batt_item(A,"Q7.1_cooperation","Anticipation des besoins")["moy_public"]},
 "sources":{"entreprises":"Q8.3/Q9.2","syndicats":"Q20","acteurs":"Q7.1"},
 "lecture":"Paradoxe : les entreprises se disent prêtes à s'engager (com commune 76%, plateforme 52%) mais 33% refusent les ateliers ; les syndicats jugent l'engagement des entreprises faible (4/7) et les opérateurs publics notent l'anticipation des besoins très bas (2.0)."})

# --- Plateforme de recrutement mutualisée (désaccord)
dims.append({
 "dimension":"Plateforme de recrutement mutualisée (intérêt)",
 "echelle":"entreprises % prêts vs acteurs importance 1-5",
 "valeurs":{"acteurs":batt_item(A,"Q8.1_importance_actions","Plateforme de recrutement")["moyenne"]},
 "detail":{"entreprises_pret_pct":multi_mod(E,"Q8.3_actions_collectives","Plateforme de recrutement")["pct_repondants"],
           "acteurs_importance":batt_item(A,"Q8.1_importance_actions","Plateforme de recrutement")["moyenne"],
           "acteurs_participation":batt_item(A,"Q8.2_participation","Plateforme de recrutement")["moyenne"]},
 "sources":{"entreprises":"Q8.3","acteurs":"Q8.1/Q8.2"},
 "lecture":"Désaccord : 52% des entreprises sont prêtes à une plateforme mutualisée, alors que les acteurs de l'emploi la jugent peu importante (2.1) et y participeraient peu (2.7) — ils s'estiment déjà ce maillon."})

# --- Transmission des savoir-faire / seniors (priorité)
dims.append({
 "dimension":"Transmission des savoir-faire & gestion des seniors (priorité)",
 "echelle":"1-5 (priorité GPECT) ; Syndicats = catégoriel",
 "valeurs":{"entreprises":batt_item(E,"Q9.1_priorites_gpect","Gestion des seniors")["moyenne"],
            "of":batt_item(O,"Q9.1_priorites_gpect","Gestion des seniors")["moyenne"],
            "acteurs":batt_item(A,"Q8.3_interet_ateliers","transmission")["moyenne"],
            "syndicats":None},
 "detail":{"entreprises_rang":"dernier des 8 items Q9.1",
           "entreprises_dispositifs_suffisants_pct":cat_mod(E,"Q4.8b_besoin_transmission","suffisants")["pct"],
           "entreprises_afest":batt_item(E,"Q4.8_dispositifs_transmission","AFEST")["moyenne"],
           "entreprises_seniors_45plus_pct":E["questions"]["Q4.1_pyramide"]["AVEC_plus_gros"]["pct_seniors_45plus"],
           "syndicats_transmission_prioritaire_ou_tres_n":cat_mod(S,"Q24_transmission","Prioritaire")["n"]+cat_mod(S,"Q24_transmission","Très prioritaire")["n"]},
 "sources":{"entreprises":"Q9.1/Q4.8b/Q4.8/Q4.1","of":"Q9.1","acteurs":"Q8.3","syndicats":"Q24"},
 "lecture":"Paradoxe central : la transmission est classée DERNIÈRE priorité par les entreprises (2.5) — qui s'estiment couvertes (67%) malgré 47% de seniors 45+ et un AFEST inexistant (1.0) — alors qu'elle est priorité haute pour 5/7 syndicats et un atelier plébiscité par les acteurs (4.0)."})
dims[-1]["ecart"]=ecart(dims[-1]["valeurs"])

# --- AFEST (panne partagée)
dims.append({
 "dimension":"AFEST — maîtrise / déploiement",
 "echelle":"1-5",
 "valeurs":{"entreprises":batt_item(E,"Q4.8_dispositifs_transmission","AFEST")["moyenne"],
            "of":scale(O,"Q5.2_maitrise_afest")["moyenne"],"acteurs":None,"syndicats":None},
 "detail":{"of_jamais_concu_pct":cat_mod(O,"Q5.1_afest_concu","Jamais")["pct"],
           "of_sans_financeur":O["questions"]["Q5.2_maitrise_afest"]["sans_financeur"]["moyenne"],
           "acteurs_afest":"non listé dans les dispositifs mobilisés (POEI/PMSMP/formation qualifiante/parcours)"},
 "sources":{"entreprises":"Q4.8","of":"Q5.2/Q5.1"},
 "lecture":"AFEST en panne des deux côtés : inexistante chez les entreprises (1.0), faiblement maîtrisée par les OF (2.6 ; 3/7 jamais conçu), absente de la boîte à outils des acteurs de l'emploi."})
dims[-1]["ecart"]=ecart(dims[-1]["valeurs"])

# --- Compétences en tension (convergence)
dims.append({
 "dimension":"Compétences industrielles en tension (convergence)",
 "echelle":"références par collège",
 "valeurs":{},
 "detail":{
   "acteurs_maintenance":batt_item(A,"Q3.1_difficulte_competences","Maintenance industrielle")["moyenne"],
   "acteurs_cnc_robots":batt_item(A,"Q3.1_difficulte_competences","CNC ou robots")["moyenne"],
   "acteurs_usinage":batt_item(A,"Q3.1_difficulte_competences","Usinage et mécanique")["moyenne"],
   "acteurs_cao":batt_item(A,"Q3.1_difficulte_competences","CAO")["moyenne"],
   "entreprises_usinage_theme_pct":theme(E,"Q3.1_metiers_cles_themes","Usinage")["pct"],
   "entreprises_qualite_manquante_pct":multi_mod(E,"Q6.2_tech_manquantes","Qualité")["pct_repondants"],
   "syndicats_usinage_theme_n":theme(S,"Q10_metiers_tension","Usinage")["n"],
   "syndicats_qualite_theme_n":theme(S,"Q10_metiers_tension","Qualité")["n"]},
 "sources":{"acteurs":"Q3.1","entreprises":"Q3.1/Q6.2","syndicats":"Q10","of":"Q3.4(verbatims)"},
 "lecture":"Convergence des 4 collèges : usinage/CN, maintenance, qualité/métrologie-méthodes, CAO. Les acteurs de l'emploi confirment quantitativement (maintenance 4.9, CNC 4.9, usinage 4.4, CAO 4.3)."})

# --- Compétences de demain (IA/cyber/robotique) : besoin vs capacité
dims.append({
 "dimension":"Compétences de demain (IA, cybersécurité, robotique) : besoin vs capacité à former",
 "echelle":"1-5 / %",
 "valeurs":{},
 "detail":{
   "of_capacite_IA":batt_item(O,"Q2.2_capacite_emergentes","Intelligence artificielle")["moyenne"],
   "of_capacite_cyber":batt_item(O,"Q2.2_capacite_emergentes","Cybersécurité")["moyenne"],
   "of_evolution_IA_pct":multi_mod(O,"Q8.2_domaines_evolutions","Intelligence artificielle")["pct_repondants"],
   "entreprises_IA_a_developper_pct":multi_mod(E,"Q6.5_competences_3_5ans","Intelligence artificielle")["pct_repondants"],
   "entreprises_cyber_pct":multi_mod(E,"Q6.5_competences_3_5ans","Cybersécurité")["pct_repondants"],
   "acteurs_manque_robotique":batt_item(A,"Q6.2_manque_formation","Robotique")["moyenne"],
   "acteurs_manque_i40_ia":batt_item(A,"Q6.2_manque_formation","Industrie 4.0")["moyenne"]},
 "sources":{"of":"Q2.2/Q8.2","entreprises":"Q6.5","acteurs":"Q6.2"},
 "lecture":"Gap offre/futur : 100% des OF anticipent l'IA comme évolution majeure mais leur capacité à la former est faible (IA 2.3, cybersécurité 1.1). Les acteurs pointent un manque de formation en robotique (4.6) et I4.0/IA (4.1). Demande entreprises : IA 38%, cyber 24%."})

# --- Nature du blocage (candidats vs qualification)
dims.append({
 "dimension":"Nature du blocage emploi (manque de candidats vs manque de qualification)",
 "echelle":"1-5 / catégoriel",
 "valeurs":{},
 "detail":{
   "entreprises_penurie_candidats":batt_item(E,"Q3.3_causes_tensions","Pénurie de candidats")["moyenne"],
   "entreprises_frein_manque_candidats":batt_item(E,"Q5.3_freins_recrutement","Manque de candidats")["moyenne"],
   "acteurs_qualification_insuffisante":batt_item(A,"Q4.1_freins_acces_emploi","qualification insuffisant")["moyenne"],
   "acteurs_manque_competences_tech":batt_item(A,"Q2.2_facteurs_inadequation","compétences techniques")["moyenne"],
   "syndicats_savoirs_de_base_n":theme(S,"Q13_competences_transversales","Savoirs de base")["n"],
   "acteurs_qualif_dominante_capbep_pct":cat_mod(A,"Q1.3_qualif_dominante","CAP / BEP")["pct"]},
 "sources":{"entreprises":"Q3.3/Q5.3","acteurs":"Q4.1/Q2.2/Q1.3","syndicats":"Q13"},
 "lecture":"Lecture complémentaire : les entreprises vivent une 'pénurie de candidats' (4.5/4.3) ; acteurs et syndicats y répondent par un déficit de QUALIFICATION (4.3), de compétences techniques (4.3) et même de savoirs de base (4/7), sur un public dominé par le CAP/BEP."})

# --- Coopération entreprises <-> acteurs/OF
dims.append({
 "dimension":"Coopération entreprises ↔ acteurs emploi / OF",
 "echelle":"1-5 / catégoriel",
 "valeurs":{"of":scale(O,"Q6.1_cooperation")["moyenne"]},
 "detail":{
   "entreprises_coop_faible_ou_nulle_pct":cat_mod(E,"Q7.8_cooperation_acteurs","faible et ponctuelle")["pct"]+cat_mod(E,"Q7.8_cooperation_acteurs","Aucune")["pct"],
   "acteurs_coop_anticipation":batt_item(A,"Q7.1_cooperation","Anticipation des besoins")["moyenne"],
   "acteurs_coop_sur_mesure":batt_item(A,"Q7.1_cooperation","parcours sur mesure")["moyenne"],
   "of_frein_mobiliser_entreprises_pct":multi_mod(O,"Q7.1_freins_offre","mobiliser les entreprises")["pct_repondants"]},
 "sources":{"entreprises":"Q7.8","acteurs":"Q7.1","of":"Q6.1/Q7.1"},
 "lecture":"Coopération jugée surtout opérationnelle mais peu anticipatrice : 62% des entreprises la disent faible/nulle avec les acteurs ; côté acteurs, anticipation 3.1 et sur-mesure 2.4 ; 71% des OF citent 'difficulté à mobiliser les entreprises' comme frein."})

SV["dimensions_partagees"]=dims

# =================================================================
# 3) CONVERGENCES / 4) PARADOXES / 5) HYPOTHÈSES / 6) AXES (interprétation, chiffres sourcés ci-dessus)
# =================================================================
SV["convergences"]=[
 "Tension de recrutement sur un socle industriel commun : usinage/CN, maintenance, qualité/méthodes, CAO (4 collèges).",
 "Offre de formation locale jugée insuffisante par tous les 'clients' (entreprises 3.1, acteurs 2.3, 5/7 syndicats).",
 "Mobilité/transport = frein structurant reconnu (acteurs 3.7, syndicats mobilité rurale 6/7, OF 57%).",
 "Besoin de compétences de demain (IA, robotique, cyber) reconnu partout, mais non couvert par l'offre.",
 "AFEST en panne (entreprises 1.0, OF 2.6 dont 3/7 jamais, absente chez les acteurs).",
 "Forte appétence déclarée pour des actions collectives (campagne com, ateliers courts, promotion des métiers)."]
SV["paradoxes"]=[
 {"titre":"Angle mort transmission","detail":"47% de seniors 45+ et AFEST=1.0 chez les entreprises, mais transmission classée DERNIÈRE priorité (2.5) et 67% se disent couvertes — alors que 5/7 syndicats la jugent prioritaire."},
 {"titre":"Auto-évaluation de l'offre (OF) vs perception clients","detail":"OF 4.0-4.3 vs entreprises 3.1 vs acteurs 2.3 vs 5/7 syndicats peu/partiellement : écart d'environ 2 points."},
 {"titre":"Engagement des entreprises","detail":"Entreprises déclarées prêtes (com 76%, plateforme 52%) mais 33% refusent les ateliers ; syndicats jugent l'engagement faible (4/7) ; acteurs publics notent l'anticipation des besoins à 2.0."},
 {"titre":"Plateforme mutualisée","detail":"Voulue par 52% des entreprises, jugée peu utile par les acteurs (2.1) qui y participeraient peu (2.7)."},
 {"titre":"Mobilité minimisée par les entreprises","detail":"Frein mobilité à 2.1 pour les entreprises vs 3.7 acteurs / 3.3 syndicats / mobilité rurale 6/7."},
 {"titre":"Candidats vs qualification","detail":"'Manque de candidats' (entreprises 4.5) vs 'manque de qualification et de savoirs de base' (acteurs 4.3 ; syndicats 4/7)."}]
SV["hypotheses_a_verifier"]=[
 "HYPOTHÈSE (à vérifier) : l'écart d'auto-évaluation de l'offre pourrait refléter un défaut de mise en relation/connaissance mutuelle plutôt qu'un déficit réel de capacité (OF : plateaux 'totalement équipés' 6/7) — à confirmer par un appariement offre/besoins.",
 "HYPOTHÈSE : la sous-priorisation de la transmission par les entreprises pourrait venir d'une non-perception du risque démographique (47% de 45+ mais seulement 5-6% de 60+ → départ différé) — à vérifier par une projection des départs par métier.",
 "HYPOTHÈSE : la divergence sur la mobilité pourrait tenir à des publics différents (entreprises = salariés déjà en poste ; acteurs/syndicats = demandeurs d'emploi non motorisés) — à vérifier.",
 "HYPOTHÈSE : le faible engagement perçu des entreprises pourrait être un problème de FORMAT (temps, utilité) plus que de volonté (ateliers courts 2h plébiscités) — à tester via un pilote.",
 "Limite transversale : 3 collèges à n=7 et écarts-types souvent élevés (1.5-2.0) → toute corrélation reste indicative, à confirmer sur un échantillon élargi."]
SV["axes_strategiques"]=[
 {"axe":"A1 — Attractivité & image du territoire","fondé_sur":"image 2.3 (ent.)/3.1 (OF) ; priorité #1 entreprises (3.9) ; frein image 95%","pistes":["campagne de communication territoriale commune (entreprises 76%, acteurs 4.7)","promotion des métiers industriels auprès des scolaires (66-67%)"]},
 {"axe":"A2 — Appariement offre de formation ↔ besoins","fondé_sur":"écart d'auto-évaluation (~2 pts) ; observatoire = levier #1 des OF (71%)","pistes":["observatoire local des métiers/compétences","cartographie partagée de l'offre","parcours sur mesure (CQP, blocs)"]},
 {"axe":"A3 — Compétences de demain","fondé_sur":"IA 100% anticipée par OF mais capacité 2.3 ; cyber 1.1 ; manque robotique 4.6 (acteurs)","pistes":["montée en compétences des formateurs (IA, robotique, cyber)","mutualisation de plateaux techniques"]},
 {"axe":"A4 — Transmission & seniors","fondé_sur":"47% seniors 45+ ; AFEST 1.0 ; priorité syndicats 5/7","pistes":["sensibilisation au risque démographique","relance AFEST/tutorat","viviers de repreneurs (artisanat)"]},
 {"axe":"A5 — Mobilité & freins périphériques","fondé_sur":"mobilité rurale 6/7 ; acteurs 3.7 ; solutions transport/hébergement","pistes":["navettes gare-zones, adaptation horaires","hébergement apprentis/stagiaires (colocation/habitat partagé)"]},
 {"axe":"A6 — Qualification & compétences socles","fondé_sur":"qualification insuffisante 4.3 (acteurs) ; savoirs de base 4/7 (syndicats) ; public CAP/BEP","pistes":["parcours de pré-qualification industrielle (acteurs 4.3)","remise à niveau des savoirs de base"]},
 {"axe":"A7 — Animation & mobilisation des entreprises","fondé_sur":"engagement faible perçu 4/7 ; ateliers courts 2h plébiscités","pistes":["ateliers courts thématiques avec résultats concrets","aller-vers en entreprise (\"bâton de pèlerin\")"]}]

# =================================================================
# 7) DONNÉES COMPLÈTES PAR COLLÈGE (le dashboard puise ici)
# =================================================================
SV["donnees_colleges"]={
 "entreprises":{"meta":E["_meta"],"questions":E["questions"],"recap_echelles":E.get("recap_echelles")},
 "of":{"meta":O["_meta"],"questions":O["questions"],"recap_echelles":O.get("recap_echelles")},
 "acteurs":{"meta":A["_meta"],"questions":A["questions"],"recap_echelles":A.get("recap_echelles")},
 "syndicats":{"meta":S["_meta"],"questions":S["questions"],"recap_echelles":S.get("recap_echelles")}}

json.dump(SV,open(RES+"source_verite.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("OK -> source_verite.json")
print("dimensions partagées :",len(dims))
for d in dims:
    print(f"  - {d['dimension'][:55]:55s} écart={d.get('ecart')}")
