#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard FINAL enrichi (un seul .html autoporté) à partir de source_verite.json.
- Surface TOUS les indicateurs déjà calculés (aucun recalcul, aucun doublon).
- Encadrés d'explication sur chaque stat critique.
- Plan d'action GPECT multi-pages très détaillé (7 fiches + pilotage).
"""
import json, pathlib
RES=pathlib.Path("/home/user/Gpect/analyse/resultats")
DASH=pathlib.Path("/home/user/Gpect/analyse/dashboard")
SV=json.load(open(RES/"source_verite.json",encoding="utf-8"))
CX=json.load(open(RES/"contexte_insee.json",encoding="utf-8"))
CHARTJS=(DASH/"chartjs.min.js").read_text(encoding="utf-8")
SVDATA=json.dumps(SV,ensure_ascii=False)
CXDATA=json.dumps(CX,ensure_ascii=False)

# ---- Encadrés "ce que ça dit" pour les stats critiques (coll|qid) ----
COMMENTS={
"entreprises|Q1.4_effectif_inscrit":"Un seul employeur (~1 550 salariés) pèse 48,6 % du total : d'où la lecture « avec / sans » sur tous les agrégats d'effectifs.",
"entreprises|Q1.8_age_dirigeant":"Près d'un dirigeant sur trois a 55 ans ou plus : enjeu de transmission des entreprises elles-mêmes (à relier au faible nombre de projets de cession).",
"entreprises|Q2.2_transmission":"Malgré des dirigeants âgés, 81 % n'envisagent aucune cession à 5 ans : transmission peu anticipée (signal faible).",
"entreprises|Q3.3_causes_tensions":"La pénurie de candidats locaux domine très nettement (4,5/5, consensus). Les freins « vie quotidienne » (logement, garde d'enfant) sont jugés faibles.",
"entreprises|Q4.7_motifs_depart":"Tous les motifs de départ sont faibles (<2,8) : cohérent avec un turnover maîtrisé — le problème est d'attirer, pas de retenir.",
"entreprises|Q4.8_dispositifs_transmission":"Transmission gérée « maison » (documentation, tutorat). L'AFEST est inexistante (1,0/5) et les dispositifs publics peu mobilisés (2,1).",
"entreprises|Q4.8b_besoin_transmission":"67 % se disent couvertes — alors que 47 % des salariés ont 45 ans et + : possible sous-estimation du risque démographique.",
"entreprises|Q5.3_freins_recrutement":"Le frein n°1 est le manque de candidats (4,3/5), loin devant les conditions internes ou le salaire.",
"entreprises|Q6.5_competences_3_5ans":"Les compétences de demain selon les entreprises : IA (38 %), transition énergétique et transmission des savoir-faire (33 %).",
"entreprises|Q7.6_offre_adaptee":"Offre de formation locale jugée moyenne (3,1/5) — à comparer aux OF qui s'auto-évaluent à 4,0-4,3.",
"entreprises|Q7.8_cooperation_acteurs":"62 % jugent la coopération avec les acteurs de l'emploi faible ou nulle : marge de progression forte.",
"entreprises|Q8.2_image_issoudun":"Image faible et homogène (2,3/5, jamais notée au-dessus de 3) : aucun répondant optimiste.",
"entreprises|Q8.3_actions_collectives":"Forte appétence collective : campagne de communication commune (76 %), plateforme de recrutement mutualisée (52 %).",
"entreprises|Q9.1_priorites_gpect":"L'attractivité écrase tout (3,9). La transmission des seniors est classée DERNIÈRE (2,5) — paradoxe avec la démographie.",
"of|Q2.2_capacite_emergentes":"Capacité quasi nulle en cybersécurité (1,1) et faible en IA (2,3), même en écartant l'organisme acheteur — alors que 100 % des OF anticipent l'IA comme évolution majeure.",
"of|Q4.1_offre_couvre":"Auto-évaluation élevée (4,0 ; 4,3 sans l'organisme acheteur) — à confronter aux entreprises (3,1) et aux acteurs de l'emploi (2,3) : ~2 points d'écart.",
"of|Q5.2_maitrise_afest":"AFEST faiblement maîtrisée (2,6/5) ; 3 OF sur 7 n'en ont jamais conçu. Frein principal : la méconnaissance des entreprises.",
"of|Q7.1_freins_offre":"Frein n°1 déclaré par les OF : la difficulté à mobiliser les entreprises (71 %).",
"of|Q7.2_leviers":"Levier le plus demandé : un observatoire local des métiers et des compétences (71 %).",
"of|Q1.7_plateaux":"L'infrastructure existe : 6 OF sur 7 disposent de plateaux techniques « totalement équipés ».",
"acteurs|Q2.1_adequation_profils":"Adéquation candidats / besoins jugée moyenne (2,9/5) : les profils ne collent qu'à moitié.",
"acteurs|Q3.1_difficulte_competences":"Confirmation externe des tensions : maintenance 4,9, programmation CNC/robots 4,9, usinage 4,4, CAO 4,3 — diagnostic identique à celui des entreprises.",
"acteurs|Q4.1_freins_acces_emploi":"Vu des prescripteurs, le frein n°1 est le niveau de qualification insuffisant (4,3), puis la mobilité (3,7).",
"acteurs|Q5.2_efficacite_dispositifs":"Formation qualifiante et parcours individualisés sont jugés les plus efficaces (4,3) ; la POEI l'est moins.",
"acteurs|Q6.1_offre_locale":"Note la plus sévère des 4 collèges sur l'offre de formation locale (2,3/5).",
"acteurs|Q6.2_manque_formation":"Manques de formation : robotique/cobotique (4,6), maintenance (4,4), Industrie 4.0 / IA (4,1).",
"acteurs|Q8.1_importance_actions":"Réserve nette sur la plateforme de recrutement mutualisée (2,1/5) — alors que 52 % des entreprises la veulent : désaccord à arbitrer.",
"syndicats|Q06_dynamique_eco":"Dynamique économique et coordination des acteurs jugées « moyennes » (2,9/5) : un territoire en attente.",
"syndicats|Q13_competences_transversales":"Alerte propre à ce collège : un déficit de compétences socles (lire / écrire / compter) cité par 4 répondants sur 7.",
"syndicats|Q14_offre_adaptee":"5 répondants sur 7 jugent l'offre de formation peu ou partiellement adaptée.",
"syndicats|Q17_freins_structurants":"Mobilité rurale citée par 6 répondants sur 7 (quasi unanime).",
"syndicats|Q20_engagement_entreprises":"Engagement des entreprises jugé faible par 4 répondants sur 7.",
"syndicats|Q24_transmission":"Transmission-reprise prioritaire ou très prioritaire pour 5 répondants sur 7 — à l'opposé des entreprises (dernière priorité).",
}

# ---- Ordre d'affichage par collège : [#Section|desc] ou qid (ou 'PYR') ----
ORDER={
"entreprises":[
 "#Profil de l'entreprise|Qui sont les 21 entreprises répondantes.",
 "Q0.8_statut","Q1.1_secteur","Q1.3_effectif_tranche","Q1.4_effectif_inscrit",
 "Q1.5_recours_externes","Q1.6_volume_interim_ETP","Q1.7_volume_prestation","Q1.8_age_dirigeant",
 "#Stratégie & anticipation|Ce que les entreprises préparent pour les 3 ans à venir.",
 "Q2.1_preoccupations","Q2.2_transmission","Q2.3_evolution_effectifs","Q2.4_investissements","Q2.5_invest_competences",
 "#Métiers clés & tensions|Les métiers en tension et leurs causes.",
 "Q3.1_metiers_cles_themes","Q3.2_tension","Q3.3_causes_tensions","Q3.4_metiers_sensibles","Q3.5_facteurs_transformation",
 "#Démographie, turnover & transmission|Pyramide des âges, départs en retraite, transmission des savoir-faire.",
 "PYR","Q4.2_retraite_2ans","Q4.3_retraite_5ans","Q4.4_services_retraite","Q4.5_turnover","Q4.6_postes_turnover_themes",
 "Q4.7_motifs_depart","Q4.8_dispositifs_transmission","Q4.8b_besoin_transmission",
 "#Recrutement|Difficultés, freins et intentions d'embauche.",
 "Q5.1_recrutements_2024_2025","Q5.2_difficulte","Q5.3_freins_recrutement","Q5.4_recrut_prevus_3ans","Q5.5_motivation_recrut","Q5.6_actions_attractivite",
 "#Compétences|Compétences techniques et comportementales, aujourd'hui et demain.",
 "Q6.1_tech_adaptees","Q6.2_tech_manquantes","Q6.3_savoiretre_adaptes","Q6.4_savoiretre_renforcer","Q6.5_competences_3_5ans",
 "#Formation & coopération|Pratiques de formation, alternance, lien avec les acteurs.",
 "Q7.1_formations_organisees","Q7.2_connaissance_opco","Q7.3_freins_formation","Q7.4_alternance","Q7.5_alternants_territoire",
 "Q7.6_offre_adaptee","Q7.7_raisons_inadequation","Q7.8_cooperation_acteurs","Q7.9_attentes_acteurs",
 "#Territoire & attractivité|Freins territoriaux et envie d'agir ensemble.",
 "Q8.1_facteurs_territoire","Q8.2_image_issoudun","Q8.3_actions_collectives",
 "#Priorités GPECT|Ce que les entreprises attendent de la démarche.",
 "Q9.1_priorites_gpect","Q9.2_ateliers","Q9.3_action_utile_themes","Q9.4_remarques_themes"],
"of":[
 "#Identité de l'organisme|Profil des 7 organismes de formation (OF).",
 "Q0.7_type","Q0.8_qualiopi","Q0.9_cpf","Q0.10_perimetre","Q0.11_presence_issoudun",
 "#Offre, publics & moyens|Ce que les OF proposent et avec quels moyens.",
 "Q1.1_publics","Q1.2_type_formations","Q1.3_niveaux","Q1.4_capacite","Q1.5_formateurs_internes","Q1.6_formateurs_externes","Q1.7_plateaux","Q1.8_equipements",
 "#Niveau de l'offre & compétences de demain|Auto-évaluation par domaine et capacité à former aux compétences émergentes.",
 "Q2.1_niveau_offre","Q2.2_capacite_emergentes","Q2.3_sur_mesure",
 "#Connaissance des besoins|Comment les OF identifient les besoins des entreprises.",
 "Q3.1_connaissance_besoins","Q3.2_sources","Q3.3_connaissance_secteurs","Q3.4_metiers_tension",
 "#Adéquation de l'offre|Ce qui colle et ce qui manque.",
 "Q4.1_offre_couvre","Q4.2_retours_clients","Q4.3_points_inadaptes","Q4.4_metiers_a_adapter",
 "#AFEST & adaptation|Formation en situation de travail et capacité d'adaptation.",
 "Q5.1_afest_concu","Q5.2_maitrise_afest","Q5.3_freins_afest","Q5.4_formes_adaptation","Q5.5_pret_evoluer",
 "#Coopération|Avec qui et sous quelles formes.",
 "Q6.1_cooperation","Q6.2_acteurs","Q6.3_formes_coop","Q6.4_actions_collectives",
 "#Freins & leviers|Ce qui bloque et ce qui aiderait.","Q7.1_freins_offre","Q7.2_leviers",
 "#Prospective|Évolutions anticipées et transformations internes.",
 "Q8.1_anticipation_besoins","Q8.2_domaines_evolutions","Q8.3_nouvelles_formations","Q8.5_transfo_internes",
 "#Priorités & rôles GPECT|Place que les OF veulent prendre dans la démarche.",
 "Q9.1_priorites_gpect","Q9.2_roles","Q9.3_ateliers",
 "#Territoire|Image et freins vus côté stagiaires/alternants.",
 "Q10.1_image","Q10.2_freins_territoire","Q10.3_actions_attractivite",
 "#Ouverture|Action la plus utile et observations.","Q11.1_action_utile","Q11.4_observations"],
"acteurs":[
 "#Profil & publics|Qui sont les 7 acteurs de l'emploi et qui ils accompagnent.",
 "Q0.1_type","Q0.2_conseillers","Q0.3_volume_accompagnes","Q1.1_publics","Q1.2_importance_publics","Q1.3_qualif_dominante",
 "#Adéquation candidats / besoins|Pourquoi l'offre et la demande ne se rencontrent pas toujours.",
 "Q2.1_adequation_profils","Q2.2_facteurs_inadequation",
 "#Compétences difficiles à trouver|Le diagnostic des prescripteurs.","Q3.1_difficulte_competences",
 "#Freins à l'accès à l'emploi|Ce qui empêche d'accéder à l'emploi industriel.","Q4.1_freins_acces_emploi",
 "#Dispositifs|Usage, efficacité et durée des emplois obtenus.","Q5.1_usage_dispositifs","Q5.2_efficacite_dispositifs","Q5.3_duree_emplois",
 "#Offre de formation|Adéquation et manques.","Q6.1_offre_locale","Q6.2_manque_formation",
 "#Coopération avec les entreprises|Relations et anticipation.","Q7.1_cooperation",
 "#Actions territoriales|Importance, engagement et ateliers.","Q8.1_importance_actions","Q8.2_participation","Q8.3_interet_ateliers"],
"syndicats":[
 "#Profil & diagnostic territorial|Qui répond et comment ils voient le territoire.",
 "Q04_type_acteur","Q05_territoire","Q06_dynamique_eco","Q07_coordination_acteurs","Q08_atouts","Q09_freins",
 "#Métiers & compétences|Tensions et compétences à renforcer.",
 "Q10_metiers_tension","Q11_besoins_identifies","Q12_competences_techniques","Q13_competences_transversales",
 "#Formation|Adéquation, freins et évolutions souhaitées.","Q14_offre_adaptee","Q15_freins_formation","Q16_evolutions_offre",
 "#Accès à l'emploi & mobilité|Freins structurants et solutions.","Q17_freins_structurants","Q18_mobilite_frein","Q19_solutions_mobilite",
 "#Engagement des entreprises|Niveau, freins et formats d'animation.","Q20_engagement_entreprises","Q21_freins_mobilisation","Q22_formats_animation","Q23_themes_engagement",
 "#Transmission-reprise|Un enjeu jugé prioritaire.","Q24_transmission","Q25_besoins_transmission",
 "#Propositions|Actions prioritaires et attentes.","Q26_action_prioritaire","Q27_actions_rapides","Q28_resultats_attendus","Q29_remarques"],
}

# ---- PLAN D'ACTION : 7 fiches détaillées ----
PLAN=[
{"code":"A1","titre":"Attractivité & image du territoire","prio":"Priorité haute","prioCls":"hi","impact":4,"effort":3,"phase":"Court terme",
 "horizon":"Court à moyen terme (0-18 mois)",
 "constat":"Image notée 2,3/5 par les entreprises (jamais >3) et citée comme frein par 95 % d'entre elles ; 3,1/5 côté OF. C'est la priorité n°1 des entreprises (3,9/5).",
 "objectif":"Inverser la perception du bassin auprès des candidats, salariés et jeunes, et faire connaître un tissu industriel riche.",
 "cibles":["Candidats hors territoire","Jeunes, scolaires & familles","Salariés en poste (fidélisation)"],
 "porteur":"Intercommunalité / démarche d'attractivité territoriale, en binôme avec les entreprises volontaires",
 "partenaires":["Chambres consulaires","France Travail","Région Centre-Val de Loire","Branches professionnelles","Éducation nationale"],
 "actions":["Campagne de communication territoriale commune (76 % des entreprises prêtes ; 4,7/5 côté acteurs)",
   "Promotion des métiers industriels auprès des lycéens/collégiens (66-67 %)",
   "Portes ouvertes et visites d'entreprises coordonnées (57 %)",
   "Valorisation des atouts objectifs du territoire (foncier, axes logistiques) relevés par les syndicats"],
 "jalons":[{"q":"0-6 mois","t":"Constituer le collectif d'entreprises ambassadrices + premier forum/job dating « résultat rapide »"},
   {"q":"6-12 mois","t":"Lancer la campagne et le kit « métiers » pour les collèges"},
   {"q":"12-18 mois","t":"Cycle annuel d'événements + première mesure d'impact"}],
 "livrables":["Identité/marque territoriale partagée","Kit de découverte des métiers pour les établissements","Calendrier annuel d'événements"],
 "kpi":[{"i":"Note d'image (ré-enquête)","c":"de 2,3 à ≥ 3,0 à 24 mois"},{"i":"Événements métiers / an","c":"≥ 6"},{"i":"Entreprises engagées","c":"≥ 15"}],
 "moyens":"Région CVL (attractivité), programme Territoires d'industrie, budget mutualisé des entreprises, forums France Travail.",
 "risques":"Dispersion des messages ; essoufflement si les résultats tardent → prévoir des actions à effet rapide (forums, job datings)."},
{"code":"A2","titre":"Appariement offre de formation ↔ besoins","prio":"Priorité haute","prioCls":"hi","impact":5,"effort":3,"phase":"Court terme",
 "horizon":"Court à moyen terme (0-24 mois)",
 "constat":"Écart d'auto-évaluation de l'offre d'environ 2 points : OF 4,0-4,3 vs entreprises 3,1 vs acteurs 2,3 (et 5/7 syndicats « peu/partiellement adaptée »). Pourtant 6 OF sur 7 ont des plateaux « totalement équipés » : le problème semble être la mise en relation plus que la capacité.",
 "objectif":"Rapprocher concrètement l'offre des besoins réels et rendre l'offre lisible pour tous.",
 "cibles":["Entreprises (donneurs d'ordre ET sous-traitants/artisans)","Organismes de formation","Prescripteurs emploi"],
 "porteur":"Animateur GPECT territorial + organismes de formation",
 "partenaires":["OPCO","France Travail","Région CVL","Chambres consulaires","Branches"],
 "actions":["Créer un observatoire local des métiers et compétences (levier n°1 des OF : 71 %)",
   "Cartographie partagée de l'offre de formation du bassin",
   "Construction de parcours sur mesure (blocs de compétences, CQP, titres pro)",
   "Rendez-vous réguliers OF–entreprises pour formaliser les besoins (besoins « partiellement identifiés » pour 4/7 syndicats)"],
 "jalons":[{"q":"0-6 mois","t":"Cahier des charges de l'observatoire + recensement de l'offre existante"},
   {"q":"6-12 mois","t":"Première cartographie diffusée + 2-3 parcours sur mesure pilotes"},
   {"q":"12-24 mois","t":"Observatoire opérationnel et actualisé annuellement"}],
 "livrables":["Observatoire local des métiers","Cartographie de l'offre","Catalogue de parcours sur mesure"],
 "kpi":[{"i":"Note d'adéquation de l'offre (entreprises)","c":"de 3,1 à ≥ 3,7"},{"i":"Parcours sur mesure créés","c":"≥ 5 / an"},{"i":"Entreprises consultées / an","c":"≥ 30"}],
 "moyens":"OPCO (ingénierie), Région CVL (carte des formations), France Travail (données marché), Plan d'investissement compétences.",
 "risques":"Observatoire « gadget » s'il n'est pas alimenté/animé ; veiller à inclure les artisans sous-traitants, pas seulement les grands comptes."},
{"code":"A3","titre":"Compétences de demain (IA, robotique, cybersécurité)","prio":"Priorité haute","prioCls":"hi","impact":4.2,"effort":4.3,"phase":"Moyen terme",
 "horizon":"Moyen à long terme (12-36 mois)",
 "constat":"100 % des OF anticipent l'IA comme évolution majeure, mais leur capacité à former est faible : IA 2,3/5, cybersécurité 1,1/5. Les acteurs pointent un manque de formation en robotique (4,6) et Industrie 4.0/IA (4,1). Demande des entreprises : IA 38 %, cyber 24 %.",
 "objectif":"Doter le territoire d'une capacité de formation aux technologies clés de l'industrie 4.0.",
 "cibles":["Formateurs des OF","Salariés en poste","Demandeurs d'emploi en reconversion"],
 "porteur":"Réseau des OF + branche métallurgie",
 "partenaires":["OPCO 2i","Région CVL","Pôles techniques / écoles d'ingénieurs","Entreprises pilotes"],
 "actions":["Plan de montée en compétences des formateurs (IA, robotique, cybersécurité)",
   "Mutualisation de plateaux techniques (cobotique/robotique) entre OF",
   "Modules courts « Industrie 4.0 » co-construits avec les entreprises",
   "Veille technologique partagée"],
 "jalons":[{"q":"0-12 mois","t":"Diagnostic des équipements + formation de formateurs « starter »"},
   {"q":"12-24 mois","t":"Plateau mutualisé + premiers modules cyber/IA"},
   {"q":"24-36 mois","t":"Offre régulière sur les 3 domaines"}],
 "livrables":["Plan de formation des formateurs","Plateau technique mutualisé","Catalogue Industrie 4.0"],
 "kpi":[{"i":"Capacité OF à former à l'IA","c":"de 2,3 à ≥ 3,5"},{"i":"Capacité cybersécurité","c":"de 1,1 à ≥ 2,5"},{"i":"Salariés formés / an","c":"cible à fixer avec les OPCO"}],
 "moyens":"OPCO 2i, FNE-Formation, Région CVL, Territoires d'industrie (investissement plateaux).",
 "risques":"Coût des équipements ; risque de doublons entre OF → la mutualisation est la clé."},
{"code":"A4","titre":"Transmission des savoir-faire & gestion des seniors","prio":"Priorité haute (angle mort)","prioCls":"hi","impact":4.3,"effort":2.7,"phase":"Court terme",
 "horizon":"Court à moyen terme (0-24 mois)",
 "constat":"47 % des salariés ont 45 ans et + ; l'AFEST est inexistante (1,0/5) et les dispositifs publics peu mobilisés (2,1). Pourtant 67 % des entreprises se disent « couvertes » et classent la transmission DERNIÈRE priorité (2,5) — alors qu'elle est prioritaire pour 5/7 syndicats. C'est l'angle mort du diagnostic.",
 "objectif":"Faire prendre conscience du risque démographique et outiller la transmission avant les départs.",
 "cibles":["Entreprises à pyramide vieillissante","Seniors détenteurs de savoir-faire","Tuteurs/juniors","Artisans en fin de carrière"],
 "porteur":"Animateur GPECT + OPCO + chambres consulaires (volet reprise artisanale)",
 "partenaires":["France Travail","Branches","Experts AFEST","Réseaux de cédants/repreneurs"],
 "actions":["Sensibilisation chiffrée au risque démographique (pyramide des âges par entreprise)",
   "Relance de l'AFEST et du tutorat (formation de tuteurs)",
   "Cartographie des savoir-faire critiques à transmettre",
   "Constitution d'un vivier de repreneurs (volet artisanat — détection cédants)"],
 "jalons":[{"q":"0-6 mois","t":"Ateliers « pyramide des âges & compétences clés » en entreprise (outil simple, aller-vers)"},
   {"q":"6-18 mois","t":"Parcours tutorat/AFEST pilotes + vivier de repreneurs amorcé"},
   {"q":"18-24 mois","t":"Démarche transmission intégrée à la GPE des entreprises volontaires"}],
 "livrables":["Outil pyramide des âges/compétences clés","Parcours tutorat-AFEST","Dispositif cédants-repreneurs"],
 "kpi":[{"i":"Entreprises ayant cartographié leurs savoir-faire","c":"≥ 10"},{"i":"Maîtrise AFEST (OF)","c":"de 2,6 à ≥ 3,5"},{"i":"Reprises accompagnées","c":"cible avec les chambres"}],
 "moyens":"OPCO (tutorat/AFEST), France Travail, chambres consulaires (transmission), dispositifs régionaux.",
 "risques":"Déni du risque (« on est couverts ») → la sensibilisation chiffrée et l'aller-vers sont déterminants."},
{"code":"A5","titre":"Mobilité & freins périphériques","prio":"Priorité moyenne","prioCls":"mid","impact":3.8,"effort":4,"phase":"Moyen terme",
 "horizon":"Moyen terme (6-24 mois)",
 "constat":"Frein vu très différemment : mobilité notée 2,1/5 par les entreprises mais 3,7 par les acteurs et 3,3 par les syndicats (mobilité rurale citée par 6/7). Les solutions proposées sont concrètes : transport adapté, hébergement des apprentis.",
 "objectif":"Lever les freins d'accès physique à l'emploi et à la formation (transport, hébergement).",
 "cibles":["Demandeurs d'emploi non motorisés","Apprentis & stagiaires","Salariés en horaires décalés"],
 "porteur":"Intercommunalité (mobilité) + acteurs de l'emploi",
 "partenaires":["Région (transports)","Entreprises (horaires)","Bailleurs / communes (hébergement)","France Travail"],
 "actions":["Navettes gare ↔ zones d'activité et adaptation des horaires de transport aux entreprises",
   "Solutions d'hébergement pour apprentis/stagiaires (colocation, habitat partagé dans des bâtiments vacants)",
   "Aides à la mobilité pendant la formation/alternance",
   "Accompagnement « savoir se déplacer » (permis, véhicule)"],
 "jalons":[{"q":"0-6 mois","t":"Diagnostic mobilité fin (origine des candidats, horaires)"},
   {"q":"6-18 mois","t":"Expérimentation navette + 1 solution d'hébergement"},
   {"q":"18-24 mois","t":"Généralisation des dispositifs qui marchent"}],
 "livrables":["Plan mobilité emploi-formation","Offre d'hébergement apprentis","Fonds d'aide à la mobilité"],
 "kpi":[{"i":"Candidats levant un frein mobilité","c":"à mesurer (base zéro)"},{"i":"Places d'hébergement créées","c":"cible locale"},{"i":"Lignes/horaires adaptés","c":"≥ 1 axe"}],
 "moyens":"Région (mobilité), intercommunalités, France Travail (aides à la mobilité), bailleurs sociaux.",
 "risques":"Coûts récurrents des transports ; veiller à des solutions soutenables (mutualisation employeurs)."},
{"code":"A6","titre":"Qualification & compétences socles","prio":"Priorité haute","prioCls":"hi","impact":5,"effort":4,"phase":"Moyen terme",
 "horizon":"Moyen à long terme (6-36 mois)",
 "constat":"Vu des prescripteurs, le frein n°1 est le niveau de qualification insuffisant (4,3) et le manque de compétences techniques (4,3), sur un public dominé par le CAP/BEP. Les syndicats alertent sur les savoirs de base (lire/écrire/compter : 4/7). Côté entreprises, c'est « le manque de candidats » — deux lectures complémentaires.",
 "objectif":"Élever le niveau de qualification et sécuriser les compétences socles pour rendre les candidats « employables ».",
 "cibles":["Demandeurs d'emploi infra-CAP","Jeunes sans qualification","Personnes en reconversion"],
 "porteur":"France Travail + organismes de formation",
 "partenaires":["Région CVL","OPCO","Entreprises (immersions)","Branches"],
 "actions":["Parcours de pré-qualification industrielle (jugés importants : 4,3/5 par les acteurs)",
   "Remise à niveau des savoirs de base intégrée aux parcours",
   "Articulation immersion (PMSMP) → formation qualifiante → embauche (dispositifs jugés les plus efficaces : 4,3/5)",
   "Mobilisation de l'alternance (76 % des entreprises y recourent déjà)"],
 "jalons":[{"q":"0-12 mois","t":"Concevoir 1-2 parcours de pré-qualification sur les métiers en tension"},
   {"q":"12-24 mois","t":"Premières promotions + suivi d'insertion"},
   {"q":"24-36 mois","t":"Offre pérenne ajustée aux tensions"}],
 "livrables":["Parcours de pré-qualification","Module savoirs de base","Tableau de bord d'insertion"],
 "kpi":[{"i":"Adéquation candidats/besoins (acteurs)","c":"de 2,9 à ≥ 3,5"},{"i":"Sortants en emploi durable","c":"à suivre (emplois jugés plutôt durables : 4,1/5)"},{"i":"Entrées en pré-qualification / an","c":"cible à fixer"}],
 "moyens":"Plan d'investissement dans les compétences, Région CVL, France Travail, OPCO.",
 "risques":"Décrochage en cours de parcours ; importance de l'accompagnement et de l'immersion entreprise."},
{"code":"A7","titre":"Animation & mobilisation des entreprises","prio":"Quick win","prioCls":"qw","impact":3,"effort":2,"phase":"Court terme",
 "horizon":"Immédiat & continu (0-6 mois puis permanent)",
 "constat":"Engagement des entreprises jugé faible par 4/7 syndicats ; freins = manque de temps, sur-sollicitation, scepticisme (« réunions qui ne mènent à rien »). Les acteurs de l'emploi notent l'anticipation des besoins à 2,0/5. Format plébiscité : ateliers courts (2h) à résultats concrets.",
 "objectif":"Mobiliser durablement les entreprises avec des formats utiles, courts et orientés résultats.",
 "cibles":["Dirigeants & RH des PME/PMI","Donneurs d'ordre et sous-traitants"],
 "porteur":"Animateur GPECT territorial",
 "partenaires":["Branches & organisations professionnelles","Chambres consulaires","France Travail","Élus locaux"],
 "actions":["Ateliers courts (2h) par thématique ciblée, avec un livrable concret à chaque séance",
   "« Aller-vers » : l'animateur se rend en entreprise (le « bâton de pèlerin »)",
   "Présence impérative d'entreprises industrielles « ressortissantes » pour légitimer la démarche",
   "Communication régulière sur les résultats obtenus"],
 "jalons":[{"q":"0-3 mois","t":"Calendrier d'ateliers courts + premières visites en entreprise"},
   {"q":"3-6 mois","t":"Premiers livrables concrets diffusés"},
   {"q":"continu","t":"Animation permanente et restitutions régulières"}],
 "livrables":["Programme d'ateliers thématiques","Compte-rendu/livrable par atelier","Tableau de bord de mobilisation"],
 "kpi":[{"i":"Entreprises participantes / atelier","c":"≥ 8"},{"i":"Ateliers organisés / an","c":"≥ 6"},{"i":"Taux de satisfaction « utile »","c":"≥ 80 %"}],
 "moyens":"Animation GPECT (financement Région/État/intercommunalité), appui des branches.",
 "risques":"Lassitude si pas de résultats visibles → la règle est « un atelier = un livrable »."},
]

HTML = r"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet"><meta name="googlebot" content="noindex,nofollow">
<title>GPECT Issoudun — Diagnostic & Plan d'action</title>
<style>
:root{--ent:#1f4e79;--of:#2e8b57;--act:#c55a11;--syn:#7030a0;--ink:#16263d;--mut:#64748b;--bg:#eef3f8;--card:#fff;--line:#e6edf4;--accent:#0b6e99;--accent2:#1f4e79;--navh:54px;
 --sh-sm:0 1px 2px rgba(16,41,63,.05);--sh-md:0 2px 10px rgba(16,41,63,.06);--sh-lg:0 16px 40px rgba(16,41,63,.14);--r:16px;}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;scroll-padding-top:calc(var(--navh) + 14px)}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
 background:radial-gradient(1200px 600px at 80% -120px,#e2ecf6 0,rgba(226,236,246,0) 60%),linear-gradient(180deg,#eef3f8,#e9eff6 40%,#eaf0f6);background-attachment:fixed;
 line-height:1.58;overflow-x:hidden;font-feature-settings:"kern","liga","tnum"}
::selection{background:rgba(11,110,153,.18)}
header.top{position:relative;overflow:hidden;background:linear-gradient(120deg,#0c2236 0,#0b6e99 62%,#2e8b57 120%);color:#fff;padding:clamp(20px,4vw,30px) clamp(16px,4vw,34px)}
header.top::after{content:"";position:absolute;inset:0;background:radial-gradient(700px 240px at 88% -60px,rgba(255,255,255,.18),transparent 70%);pointer-events:none}
header.top h1{margin:0;font-size:clamp(18px,2.7vw,25px);font-weight:800;letter-spacing:-.2px;line-height:1.2;position:relative}
header.top p{margin:7px 0 0;font-size:clamp(11px,1.6vw,13.5px);opacity:.9;font-weight:500;position:relative}
nav{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.82);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid var(--line);
 display:flex;gap:3px;padding:8px clamp(8px,2vw,14px);box-shadow:0 4px 18px rgba(16,41,63,.06);overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
nav::-webkit-scrollbar{height:5px}nav::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:4px}
nav button{flex:0 0 auto;border:0;background:transparent;color:var(--mut);font-size:13px;font-weight:650;padding:9px 14px;border-radius:11px;cursor:pointer;white-space:nowrap;min-height:40px;letter-spacing:.1px;transition:background .2s,color .2s,box-shadow .2s,transform .12s}
nav button:hover{background:#eef4f9;color:var(--ink)}
nav button:active{transform:translateY(1px)}
nav button.active{background:linear-gradient(135deg,#0b6e99,#1f4e79);color:#fff;box-shadow:0 4px 12px rgba(11,110,153,.38)}
nav button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
nav .grp{align-self:center;color:#94a3b8;font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.7px;padding:0 8px 0 12px;border-left:1px solid var(--line);margin-left:5px}
main{max-width:1220px;margin:0 auto;padding:clamp(16px,3vw,26px) clamp(12px,3vw,20px) 90px}
.page{display:none}.page.active{display:block;animation:fade .34s cubic-bezier(.2,.7,.2,1)}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.banner{background:linear-gradient(115deg,#ffffff,#f1f7fb 90%);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:14px;padding:15px 19px;margin:0 0 20px;box-shadow:var(--sh-md);font-size:clamp(13px,1.7vw,15px)}
.banner b{color:var(--accent)}
h2.pt{font-size:clamp(20px,2.8vw,26px);margin:0 0 4px;font-weight:800;letter-spacing:-.4px}
.sub{color:var(--mut);font-size:13.5px;margin:0 0 18px}
h3.sec{position:relative;font-size:16.5px;font-weight:750;margin:30px 0 6px;padding-left:14px;color:#0e2740}
h3.sec::before{content:"";position:absolute;left:0;top:2px;bottom:2px;width:4px;border-radius:4px;background:linear-gradient(180deg,#0b6e99,#2e8b57)}
h3.sec span{display:block;font-weight:450;font-size:12.5px;color:var(--mut);margin-top:3px;padding-left:0}
.gauto{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px;margin-top:14px}
.grid{display:grid;gap:18px}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
@media(max-width:1024px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:760px){.g4,.g3,.g2{grid-template-columns:1fr}}
.card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:17px;box-shadow:var(--sh-sm);display:flex;flex-direction:column;transition:transform .2s cubic-bezier(.2,.7,.2,1),box-shadow .2s ease,border-color .2s}
.card:hover{transform:translateY(-4px);box-shadow:var(--sh-lg);border-color:#d4e2ee}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.gauto .card{animation:rise .55s cubic-bezier(.2,.7,.2,1) both}
.gauto .card:nth-child(2){animation-delay:.05s}.gauto .card:nth-child(3){animation-delay:.1s}.gauto .card:nth-child(4){animation-delay:.15s}.gauto .card:nth-child(5){animation-delay:.2s}.gauto .card:nth-child(6){animation-delay:.25s}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
.gauge{height:10px;background:#e9eef3;border-radius:8px;overflow:hidden;margin-top:11px;box-shadow:inset 0 1px 2px rgba(16,41,63,.08)}
.gauge>span{display:block;height:100%;background:linear-gradient(90deg,#0b6e99,#2e8b57);border-radius:8px;width:0;transition:width 1s cubic-bezier(.2,.8,.2,1)}
.gscale{display:flex;justify-content:space-between;font-size:10px;color:#9aa7b4;margin-top:4px}
.card h3{margin:0 0 2px;font-size:14.5px;line-height:1.32;font-weight:700;letter-spacing:-.1px}
.card .note{color:var(--mut);font-size:11.5px;margin:0 0 9px}
.metric{text-align:center;justify-content:center;background:linear-gradient(180deg,#ffffff,#fbfdff)}
.metric .num,.big{background:linear-gradient(135deg,#0b6e99,#16263d);-webkit-background-clip:text;background-clip:text;color:#10293f;-webkit-text-fill-color:transparent}
.metric .num{font-size:clamp(27px,5vw,36px);font-weight:850;line-height:1;letter-spacing:-1px}
.metric .lab{font-size:12px;color:var(--mut);margin-top:7px;font-weight:550}.metric small{display:block;color:var(--mut);font-size:11px;margin-top:5px;-webkit-text-fill-color:currentColor}
.chartbox{position:relative;width:100%;height:clamp(250px,40vh,320px)}.chartbox.tall{height:clamp(320px,52vh,440px)}
.bigrow{display:flex;align-items:center;gap:14px;padding:6px 2px}
.big{font-size:42px;font-weight:850;line-height:1;letter-spacing:-1px}.big span{font-size:16px;color:var(--mut);font-weight:650;-webkit-text-fill-color:var(--mut)}
.bigmeta{font-size:12px;color:var(--mut)}
.lec{background:linear-gradient(120deg,#f1f8ed,#eef6f0);border:1px solid #dceed0;border-left:4px solid var(--of);border-radius:10px;padding:10px 13px;margin-top:11px;font-size:12.5px;color:#27412e}
.lec b{color:#1e5b34}
.verb{background:#f7f9fc;border-left:3px solid var(--syn);padding:8px 12px;border-radius:8px;font-style:italic;font-size:12.5px;margin:7px 0;color:#33414f}
table.mx{width:100%;border-collapse:separate;border-spacing:0;font-size:13px;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--sh-sm)}
table.mx th,table.mx td{border-bottom:1px solid var(--line);border-right:1px solid var(--line);padding:10px 11px;text-align:center}
table.mx tr td:last-child,table.mx tr th:last-child{border-right:0}table.mx tr:last-child td{border-bottom:0}
table.mx th{background:linear-gradient(135deg,#13314c,#0e2740);color:#fff;font-weight:650}table.mx td.dim{text-align:left;font-weight:650}
table.mx tbody tr:nth-child(even){background:#f8fafc}table.mx tbody tr:hover{background:#eef5fa}
.ec{font-weight:800;border-radius:7px;padding:2px 9px;color:#fff;display:inline-block}
/* PLAN */
.fiche{border-top:5px solid transparent;border-image:linear-gradient(90deg,#0b6e99,#2e8b57) 1}
.fhead{display:flex;align-items:center;gap:11px;flex-wrap:wrap}
.fcode{background:linear-gradient(135deg,#0b6e99,#1f4e79);color:#fff;font-weight:800;border-radius:10px;padding:4px 12px;font-size:14px;box-shadow:0 2px 8px rgba(11,110,153,.3)}
.fiche h3{font-size:16px;margin:0;font-weight:750}
.prio{margin-left:auto;font-size:11px;font-weight:750;padding:4px 11px;border-radius:20px;color:#fff;letter-spacing:.2px}
.prio.hi{background:#b3261e}.prio.mid{background:#d97706}.prio.qw{background:#2e8b57}
.fhz{color:var(--mut);font-size:12px;margin:7px 0 4px;font-weight:550}
.fiche p{margin:8px 0 2px;font-size:13px}.fiche ul{margin:4px 0 6px;padding-left:18px;font-size:13px}.fiche li{margin:2px 0}
table.kpi{width:100%;border-collapse:separate;border-spacing:0;font-size:12.5px;margin:6px 0 2px;border:1px solid var(--line);border-radius:10px;overflow:hidden}
table.kpi th,table.kpi td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left}table.kpi tr:last-child td{border-bottom:0}
table.kpi th{background:#eef4f8;font-weight:700}
.timeline{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:760px){.timeline{grid-template-columns:1fr}}
.tl{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;border-top:5px solid transparent;border-image:linear-gradient(90deg,#0b6e99,#2e8b57) 1;box-shadow:var(--sh-sm)}
.tl h4{margin:0 0 9px;font-size:14px;font-weight:750}.tl ul{margin:0;padding-left:18px;font-size:12.5px}
.glo dt{font-weight:750;margin-top:9px}.glo dd{margin:0;color:var(--mut)}
.warn{background:linear-gradient(120deg,#fff7ed,#fff1e0);border:1px solid #f6dcb8;border-left:4px solid #c55a11;border-radius:11px;padding:11px 15px;font-size:12.5px;margin:12px 0;color:#5b3a17}
.src{font-size:10.5px;color:#94a3b8;margin-top:8px;line-height:1.45}
footer{border-top:1px solid var(--line);background:#fff;color:var(--mut);font-size:12.5px;text-align:center;padding:22px}
footer b{color:var(--ink)}
#toTop{position:fixed;right:18px;bottom:18px;z-index:40;width:48px;height:48px;border-radius:50%;border:0;background:linear-gradient(135deg,#0b6e99,#1f4e79);color:#fff;font-size:20px;cursor:pointer;box-shadow:0 6px 18px rgba(11,110,153,.4);opacity:0;visibility:hidden;transition:opacity .25s,visibility .25s,transform .2s}
#toTop:hover{transform:translateY(-3px) scale(1.05)}
#toTop.show{opacity:.95;visibility:visible}
</style></head>
<body>
<header class="top"><h1>GPECT du bassin d'Issoudun — Diagnostic emploi &amp; compétences + Plan d'action</h1>
<p>Enquête auprès de 4 collèges d'acteurs · analyse agrégée &amp; anonyme · 42 répondants (21 / 7 / 7 / 7)</p></header>
<nav id="nav"></nav>
<main>
 <section class="page active" id="p-synthese"></section>
 <section class="page" id="p-cxt"></section>
 <section class="page" id="p-ent"></section>
 <section class="page" id="p-of"></section>
 <section class="page" id="p-act"></section>
 <section class="page" id="p-syn"></section>
 <section class="page" id="p-comp"></section>
 <section class="page" id="p-cx"></section>
 <section class="page" id="p-mx"></section>
 <section class="page" id="p-plan1"></section>
 <section class="page" id="p-plan2"></section>
 <section class="page" id="p-plan3"></section>
 <section class="page" id="p-plan4"></section>
 <section class="page" id="p-met"></section>
</main>
<footer>Diagnostic GPECT du bassin d'Issoudun — analyse agrégée et anonyme · données vérifiées (audit de traçabilité).<br>
<b>Sophie Kirsch</b> (Ceterha) · <b>Sabrina Alamargot</b> (La Fabrique RH) · <b>Escale Digitale Solutions</b></footer>
<button id="toTop" title="Revenir en haut">&#8593;</button>
<script>__CHARTJS__</script>
<script>
const SV=__SVDATA__, COMMENTS=__COMMENTS__, ORDER=__ORDER__, PLAN=__PLAN__, CX=__CXDATA__;
const C={ent:'#1f4e79',of:'#2e8b57',act:'#c55a11',syn:'#7030a0'};
const COL={entreprises:'#1f4e79',of:'#2e8b57',acteurs:'#c55a11',syndicats:'#7030a0'};
const PAL=['#1f4e79','#2e8b57','#c55a11','#7030a0','#0b6e99','#b8860b','#8d6e63','#557','#3b7','#a55'];
Chart.defaults.font.family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif";Chart.defaults.font.size=12;Chart.defaults.color="#33414f";Chart.defaults.plugins.legend.display=false;
Chart.defaults.animation.duration=850;Chart.defaults.animation.easing='easeOutQuart';
const fmt=v=>(v==null?'—':String(v).replace('.',','));
const fmt1=v=>(v==null?'—':Number(v).toFixed(1).replace('.',','));  // toujours 1 décimale
const fmtT=v=>(v==null?'—':Number(v).toLocaleString('fr-FR'));        // séparateur de milliers
function Q(c,k){return (SV.donnees_colleges[c]||{}).questions[k];}
function lbl(s){s=String(s);for(let i=0;i<2;i++)s=s.replace(/^\s*Q[0-9][0-9.]*[a-z]?\s*[—–-]\s*/,'');return s;}
function shorten(s,n){s=String(s);return s.length>(n||34)?s.slice(0,(n||34)-1)+'…':s;}
function dim(n){return SV.dimensions_partagees.find(d=>d.dimension.toLowerCase().includes(n));}
let CQ=[];let _n=0;const nid=()=>'cv'+(++_n);
function chCanvas(id,tall){return `<div class="chartbox${tall?' tall':''}"><canvas id="${id}"></canvas></div>`;}
// plugin : affiche la valeur au bout de chaque barre (lisibilité)
const valLabel={id:'valLabel',afterDatasetsDraw(ch){const ds=ch.data.datasets;if(ds.length>1)return;const ctx=ch.ctx;const meta=ch.getDatasetMeta(0);ctx.save();ctx.font='bold 10.5px -apple-system,sans-serif';ctx.fillStyle='#33414f';
 meta.data.forEach((bar,i)=>{const v=ds[0].data[i];if(v==null)return;const suf=ch.$suffix||'';
  if(ch.options.indexAxis==='y'){ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(fmt(v)+suf,bar.x+5,bar.y);}
  else{ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText(fmt(v)+suf,bar.x,bar.y-4);}});ctx.restore();}};
function card(t,nt,body,cm,cls){return `<div class="card ${cls||''}"><h3>${t}</h3>${nt?`<p class="note">${nt}</p>`:''}${body}${cm?`<div class="lec"><b>💡 Ce que ça dit —</b> ${cm}</div>`:''}</div>`;}
function metricCard(num,lab,small){return `<div class="card metric"><div class="num">${num}</div><div class="lab">${lab}</div>${small?`<small>${small}</small>`:''}</div>`;}
function uid(c,k){return 'cv_'+c+'_'+k.replace(/[^a-z0-9]/gi,'');}
// charts
function hbar(id,labels,data,color,max,suf){const ch=new Chart(document.getElementById(id),{type:'bar',data:{labels,datasets:[{data,backgroundColor:color,borderRadius:4,maxBarThickness:26}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:{right:40}},scales:{x:{beginAtZero:true,max:max||undefined,grid:{color:'#eef2f7'}},y:{grid:{display:false},ticks:{autoSkip:false,font:{size:10.5},callback:function(v){const l=this.getLabelForValue(v);return l.length>32?l.slice(0,31)+'…':l;}}}},plugins:{tooltip:{callbacks:{title:items=>items[0].label,label:c=>' '+fmt(c.parsed.x)+(suf||'')}}}},plugins:[valLabel]});ch.$suffix=suf||'';ch.update();}
function vbar(id,labels,data,colors,max,suf){const ch=new Chart(document.getElementById(id),{type:'bar',data:{labels,datasets:[{data,backgroundColor:colors,borderRadius:5,maxBarThickness:70}]},options:{responsive:true,maintainAspectRatio:false,layout:{padding:{top:18}},scales:{y:{beginAtZero:true,max:max||5,grid:{color:'#eef2f7'}},x:{grid:{display:false}}},plugins:{tooltip:{callbacks:{label:c=>' '+fmt(c.parsed.y)+(suf||'')}}}},plugins:[valLabel]});ch.$suffix=suf||'';ch.update();}
function dough(id,labels,data,colors){new Chart(document.getElementById(id),{type:'doughnut',data:{labels,datasets:[{data,backgroundColor:colors,borderWidth:2,borderColor:'#fff'}]},options:{responsive:true,maintainAspectRatio:false,cutout:'56%',plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:11,font:{size:10.5}}},tooltip:{callbacks:{label:c=>' '+c.label+' : '+c.parsed}}}}});}
function radar(id,labels,data,col){new Chart(document.getElementById(id),{type:'radar',data:{labels,datasets:[{data,backgroundColor:col+'2e',borderColor:col,borderWidth:2,pointBackgroundColor:col,pointRadius:3}]},options:{responsive:true,maintainAspectRatio:false,scales:{r:{min:0,max:5,ticks:{stepSize:1,font:{size:9}},pointLabels:{font:{size:9.5}}}},plugins:{tooltip:{callbacks:{label:c=>' '+fmt(c.parsed.r)}}}}});}
function battChart(id,a,col){const sf=a[0]&&a[0].sans_financeur;
 if(sf){new Chart(document.getElementById(id),{type:'bar',data:{labels:a.map(x=>x.item),datasets:[{label:'Les 7 organismes',data:a.map(x=>x.moyenne),backgroundColor:col,borderRadius:4,maxBarThickness:16},{label:'Sans l\'organisme acheteur (non-formateur)',data:a.map(x=>x.sans_financeur?x.sans_financeur.moyenne:null),backgroundColor:col+'66',borderRadius:4,maxBarThickness:16}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,scales:{x:{beginAtZero:true,max:5,grid:{color:'#eef2f7'}},y:{grid:{display:false},ticks:{font:{size:10}}}},plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:11,font:{size:10.5}}},tooltip:{callbacks:{label:c=>' '+c.dataset.label+' : '+fmt(c.parsed.x)}}}}});}
 else hbar(id,a.map(x=>x.item),a.map(x=>x.moyenne),col,5);}
function verbList(arr,n){const sk=/^(ras|na|n\/a|ne sait pas|non renseign|pas de remarque|pas de partage|aucun|aucune|0)\.?$/i;
 const v=(arr||[]).filter(x=>x&&!sk.test(x.trim())&&x.trim().length>14).slice(0,n);
 return v.length?('<div style="margin-top:8px">'+v.map(x=>`<div class="verb">« ${x} »</div>`).join('')+'</div>'):'';}
// comparaison Bassin / Indre / France (barres horizontales) — indre nullable
function cmp(id,bassin,indre,france,suf){
 const labels=["Bassin d'Issoudun"],data=[bassin],cols=['#0b6e99'];
 if(indre!=null){labels.push('Indre (dépt.)');data.push(indre);cols.push('#6f9bbd');}
 labels.push('France (INSEE)');data.push(france);cols.push('#b6c2cf');
 const ch=new Chart(document.getElementById(id),{type:'bar',
 data:{labels,datasets:[{data,backgroundColor:cols,borderRadius:5,maxBarThickness:34}]},
 options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:{right:50}},
  scales:{x:{beginAtZero:true,grid:{color:'#eef2f7'}},y:{grid:{display:false},ticks:{font:{size:11.5}}}},
  plugins:{tooltip:{callbacks:{label:c=>' '+fmt(c.parsed.x)+(suf||'')}}}},plugins:[valLabel]});
 ch.$suffix=suf||'';ch.update();}
// carte de comparaison (graphe + source + lien diagnostic) — indre nullable
function ccard(title,sub,bassin,indre,france,id,suf,src,lien){CQ.push(()=>cmp(id,bassin,indre,france,suf));
 return `<div class="card"><h3>${title}</h3><p class="note">${sub}</p>${chCanvas(id)}<div class="src">Source : ${src}</div>${lien?`<div class="lec"><b>💡 Lien avec le diagnostic —</b> ${lien}</div>`:''}</div>`;}
// auto render by type
function auto(c,k){const d=Q(c,k);if(!d)return '';const cm=COMMENTS[c+'|'+k]||'';const t=d.type,id=nid(),col=COL[c],title=lbl(d.intitule||k);
 if(t==='echelle_1_5'){const sf=d.sans_financeur?`<br>hors organisme acheteur (non-formateur) : <b>${fmt(d.sans_financeur.moyenne)}</b>/5`:'';
   const gid=nid();CQ.push(()=>{const e=document.getElementById(gid);if(e)e.style.width=(d.moyenne/5*100)+'%';});
   return card(title,'Note moyenne sur 5',`<div class="bigrow"><div class="big">${fmt(d.moyenne)}<span>/5</span></div><div class="bigmeta">médiane ${fmt(d.mediane)} · mini ${d.min} · maxi ${d.max}<br>${d.n} répondants${sf}</div></div><div class="gauge"><span id="${gid}"></span></div><div class="gscale"><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span></div>`,cm);}
 if(t==='numerique'){const n=(d.n!=null?d.n:d.n_numerique);const s2=d.sans_plus_gros?`<br>sans le plus gros employeur : <b>${fmt(d.sans_plus_gros.somme)}</b> (médiane ${fmt(d.sans_plus_gros.mediane)})`:'';
   const nnx=(d.n_non_numerique_exclus!=null?d.n_non_numerique_exclus:(d.valeurs_non_numeriques?d.valeurs_non_numeriques.length:0));
   const nn=nnx?` · ${nnx} réponse(s) non chiffrable(s)`:'';
   return card(title,'Total déclaré',`<div class="bigrow"><div class="big">${fmt(d.somme)}</div><div class="bigmeta">total cumulé · médiane ${fmt(d.mediane)} · ${n} réponses${nn}${s2}</div></div>`,cm);}
 if(t==='choix_unique'){const m=d.modalites;CQ.push(()=>dough(id,m.map(x=>shorten(x.modalite,30)+' ('+x.n+')'),m.map(x=>x.n),PAL));
   return card(title,'Répartition des '+d.n_repondants+' réponses',chCanvas(id),cm);}
 if(t==='multi_select'){const a=d.modalites.filter(x=>x.n>0);CQ.push(()=>hbar(id,a.map(x=>x.modalite),a.map(x=>x.pct_repondants),col,100,'%'));
   return card(title,'% des '+d.n_repondants+' répondants — plusieurs réponses possibles',chCanvas(id,a.length>6),cm);}
 if(t==='batterie_echelle_1_5'){const a=(d.classement_par_moyenne||d.items);CQ.push(()=>battChart(id,a,col));
   return card(title,'Note moyenne sur 5 (du + élevé au + faible) — '+(a[0]?a[0].n:'')+' répondants',chCanvas(id,true),cm);}
 if(t==='texte_libre_code'){const a=d.themes.filter(x=>x.n>0);CQ.push(()=>hbar(id,a.map(x=>x.theme),a.map(x=>x.n),col,d.n_repondants));
   return card(title,'Nombre de répondants (sur '+d.n_repondants+') ayant cité chaque thème',chCanvas(id,a.length>6)+verbList(d.verbatims_anonymises,3),cm);}
 if(t==='texte_libre'){const vb=verbList(d.verbatims_anonymises,6);if(!vb&&!cm)return '';return card(title,'Verbatims anonymisés · '+d.n_repondants+' réponses',vb||'',cm);}
 return '';}
// pyramide entreprises (avec/sans Safran)
function pyrCard(){const p=Q('entreprises','Q4.1_pyramide');const id='cv_pyr';
 const html=card('Pyramide des âges (en nombre de salariés)','Bascule pour neutraliser le plus gros employeur (~la moitié de l\'effectif).',
  `<div class="toggle" id="tpyr" style="display:flex;gap:6px;margin-bottom:8px"><button class="on" data-v="AVEC_plus_gros" style="border:1px solid var(--line);background:var(--ent);color:#fff;border-radius:8px;padding:5px 9px;font-size:11.5px;cursor:pointer">Avec le plus gros employeur</button><button data-v="SANS_plus_gros" style="border:1px solid var(--line);background:#fff;color:var(--mut);border-radius:8px;padding:5px 9px;font-size:11.5px;cursor:pointer">Sans</button></div>`+chCanvas(id),
  "47 % des salariés ont 45 ans et + (robuste avec ou sans le grand employeur) : l'enjeu de transmission est réel, mais étalé (peu de 60 ans et +).");
 CQ.push(()=>{let ch;function draw(v){const a=p[v];const data=[a.tranche_moins30,a.tranche_31_44,a.tranche_45_59,a.tranche_60plus];if(ch)ch.destroy();
   ch=new Chart(document.getElementById(id),{type:'bar',data:{labels:['Moins de 30','31-44 ans','45-59 ans','60 ans et +'],datasets:[{data,backgroundColor:['#5b8fc9','#1f4e79','#143a5c','#0c2740'],borderRadius:5}]},options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,grid:{color:'#eef2f7'}},x:{grid:{display:false}}},plugins:{tooltip:{callbacks:{label:c=>' '+c.parsed.y+' salariés'}},subtitle:{display:true,text:'n='+a.n_repondants+' · '+a.total_tetes+' salariés · '+fmt(a.pct_seniors_45plus)+'% de 45 ans et +',color:'#5b6b7d',font:{size:11}}}}});}
   draw('AVEC_plus_gros');document.querySelectorAll('#tpyr button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#tpyr button').forEach(x=>{x.style.background='#fff';x.style.color='var(--mut)';x.classList.remove('on')});b.style.background='var(--ent)';b.style.color='#fff';draw(b.dataset.v);});});
 return html;}
// build a college page from ORDER spec
function buildCollege(c){let h='';let block='';
 const flush=()=>{if(block){h+='<div class="gauto">'+block+'</div>';block='';}};
 ORDER[c].forEach(e=>{
  if(e[0]==='#'){flush();const [t,desc]=e.slice(1).split('|');h+=`<h3 class="sec">${t}${desc?`<span>${desc}</span>`:''}</h3>`;}
  else if(e==='PYR'){block+=pyrCard();}
  else block+=auto(c,e);
 });flush();return h;}

const BANNERS={
 ent:"<b>En clair :</b> 95 % des entreprises sont en tension de recrutement, surtout faute de candidats sur des métiers techniques. Près de la moitié des salariés ont 45 ans ou plus, mais la transmission reste peu préparée. Vous trouverez ici l'intégralité des indicateurs du collège.",
 of:"<b>En clair :</b> l'infrastructure de formation existe (plateaux équipés), mais la capacité à former aux compétences de demain (IA, cybersécurité) est faible, et les OF jugent leur offre bien plus adaptée que ne le font les entreprises.",
 act:"<b>En clair :</b> les acteurs de l'emploi confirment les tensions (maintenance, usinage, machines numériques) et pointent un manque de qualification des candidats plus qu'un simple manque de bras.",
 syn:"<b>En clair :</b> atout n°1 = la position et le foncier ; freins = qualification de la main-d'œuvre et mobilité. La transmission-reprise est jugée prioritaire, l'engagement des entreprises plutôt faible. Réponses surtout qualitatives.",
};
const TITLES={ent:["Collège Entreprises","n=21 · le tissu industriel du bassin"],of:["Collège Organismes de formation","n=7 · l'offre de formation"],act:["Collège Acteurs de l'emploi","n=7 · France Travail, Mission Locale, Cap Emploi, APEC, intérim"],syn:["Collège Syndicats / organisations professionnelles","n=7 · patronal, salariés, consulaires"]};
const CMAP={ent:'entreprises',of:'of',act:'acteurs',syn:'syndicats'};

const BUILD={};
function pageCollege(short){return function(){const c=CMAP[short];const host=document.getElementById('p-'+short);
 host.innerHTML=`<div class="banner">${BANNERS[short]}</div><h2 class="pt">${TITLES[short][0]}</h2><p class="sub">${TITLES[short][1]}</p>`+buildCollege(c);
 CQ.forEach(f=>{try{f()}catch(e){}});CQ=[];};}
['ent','of','act','syn'].forEach(s=>BUILD[s]=pageCollege(s));

BUILD.synthese=function(){const host=document.getElementById('p-synthese');const co=SV._meta.colleges;
 const offre=dim("adéquation de l'offre").valeurs,trans=dim('transmission').valeurs;
 const afest=(Q('entreprises','Q4.8_dispositifs_transmission').items.find(x=>x.item.includes('AFEST'))||{}).moyenne;
 const seniors=Q('entreprises','Q4.1_pyramide').AVEC_plus_gros.pct_seniors_45plus;
 const imgV=Q('entreprises','Q8.2_image_issoudun').moyenne;
 const imgF=(Q('entreprises','Q8.1_facteurs_territoire').modalites.find(m=>m.modalite.includes('Image du territoire'))||{}).pct_repondants;
 const cl9=Q('entreprises','Q9.1_priorites_gpect').classement_par_moyenne;const trI=cl9.find(x=>x.item.includes('Gestion des seniors'));const trR=cl9.indexOf(trI)+1;
 host.innerHTML=`<div class="banner"><b>L'essentiel :</b> un bassin industriel en forte tension de recrutement, une offre de formation jugée en décalage par ceux qui l'utilisent, un risque de départs en retraite sous-estimé, et 4 familles d'acteurs qui ne voient pas toujours les mêmes priorités. Ce tableau de bord donne le diagnostic complet par collège, les croisements, et un plan d'action en 7 axes.</div>
 <h2 class="pt">Vue d'ensemble</h2><p class="sub">Qui a répondu, et les chiffres à retenir.</p>
 <div class="grid g4">${metricCard(co.entreprises.n,'Entreprises')}${metricCard(co.of.n,'Organismes de formation')}${metricCard(co.acteurs.n,"Acteurs de l'emploi")}${metricCard(co.syndicats.n,'Syndicats / orga pro')}</div>
 <div class="card" style="margin-top:16px"><h3>Les 4 plus grands écarts de perception entre acteurs</h3><p class="note">Moyennes 1-5. Plus les barres d'un même thème sont éloignées, plus les acteurs divergent.</p>${chCanvas('c-top',true)}</div>
 <div class="grid g3" style="margin-top:16px">
 ${metricCard(fmt1(offre.of)+' vs '+fmt1(offre.acteurs),"Offre de formation : note des OF vs note des acteurs de l'emploi (sur 5)",'écart de perception majeur (~2 pts)')}
 ${metricCard(seniors+' %','de salariés de 45 ans et + (entreprises)','enjeu de transmission')}
 ${metricCard(fmt(afest),'AFEST : maîtrise dans les entreprises (1-5)','dispositif quasi inexistant')}
 ${metricCard(fmt(imgV),'Image du territoire notée par les entreprises (1-5)','jamais supérieure à 3')}
 ${metricCard(fmt(imgF)+' %',"des entreprises citent l'image comme frein",'')}
 ${metricCard(fmt(trI.moyenne)+' · '+trR+'ᵉ/'+cl9.length,'Priorité de la transmission (entreprises)','la plus basse — prioritaire pour 5/7 syndicats')}</div>
 <div class="grid g2" style="margin-top:16px"><div class="card"><h3>Tension de recrutement (entreprises)</h3><p class="note">n=21</p>${chCanvas('c-tens')}</div>
 <div class="card"><h3>Comment lire ce tableau de bord</h3><p style="font-size:13px">Chaque chiffre vient des réponses, agrégées par collège et vérifiées (audit de traçabilité). <b>Une moyenne</b> pour les questions notées 1-5 ; <b>un effectif ou un %</b> pour les comptages. Trois collèges à <b>n=7</b> → on lit des <b>tendances</b>. Les encadrés <b>💡</b> expliquent les stats critiques. Les onglets <b>Plan d'action</b> déroulent les 7 axes.</p></div></div>`;
 const dims=[dim("adéquation de l'offre"),dim('mobilité'),dim('transmission'),dim('afest')];
 const cols=['entreprises','of','acteurs','syndicats'];
 new Chart(document.getElementById('c-top'),{type:'bar',data:{labels:[['Offre de','formation'],['Mobilité','(frein)'],['Transmission','(priorité)'],['AFEST','(maîtrise)']],datasets:cols.map((cc,i)=>({label:co[cc].libelle,data:dims.map(d=>d.valeurs[cc]??null),backgroundColor:[C.ent,C.of,C.act,C.syn][i],borderRadius:4,maxBarThickness:34}))},options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,max:5,grid:{color:'#eef2f7'}},x:{grid:{display:false}}},plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:12,font:{size:11}}},tooltip:{callbacks:{label:c=>' '+c.dataset.label+' : '+fmt(c.parsed.y)}}}}});
 const tt=Q('entreprises','Q3.2_tension').modalites;dough('c-tens',tt.map(m=>shorten(m.modalite.replace('Oui, ','').replace('Non, ',''),26)),tt.map(m=>m.n),[C.act,'#e0a26b','#bcd']);
};
BUILD.cxt=function(){const host=document.getElementById('p-cxt');const X=CX;
 const D=X.demographie,E=X.emploi_activite,I=X.industrie,DI=X.diplome_2022,MO=X.mobilite,LO=X.logement,TE=X.tissu_economique,J=X.jeunes_mission_locale_2025;
 host.innerHTML=`<div class="banner" style="border-left-color:#b3261e"><b>À lire avec précaution —</b> cette page ne provient <u>pas</u> de l'enquête GPEC-T (le déclaratif des 42 répondants), mais de <b>sources statistiques officielles</b> (INSEE, Mission Locale). Elle sert de <b>toile de fond objective</b> pour confirmer ou nuancer ce que les acteurs déclarent. Chaque chiffre porte sa source.</div>
 <h2 class="pt">Contexte territorial — ce que disent les données officielles</h2>
 <p class="sub">Périmètre : ${X._meta.perimetre_principal}. Sources : INSEE (recensement 2022, BPE 2024, SIDE 2023) · Mission Locale d'Issoudun (rapport d'activités 2025).</p>

 <h3 class="sec">Le bassin en chiffres clés (INSEE)<span>Population, vieillissement, emploi industriel — le décor du diagnostic.</span></h3>
 <div class="grid g4">
  ${metricCard(fmtT(D.population_2022),'habitants (2022)',fmt(D.evolution_2011_2022_pct)+' % depuis 2011')}
  ${metricCard(fmt(D.part_60_plus_pct)+' %','de 60 ans et plus','vieillissement marqué')}
  ${metricCard(fmt(I.part_industrie_emploi_pct_2022)+' %',"des emplois dans l'industrie",fmtT(I.emplois_industrie_2022)+' emplois — en hausse')}
  ${metricCard(fmt(E.taux_chomage_recensement_pct_2022)+' %','de chômage (recensement, 2022)','15-24 ans : '+fmt(E.taux_chomage_15_24_pct)+' %')}
 </div>

 <h3 class="sec">Le bassin face à son département et à la France (INSEE)<span>Définitions identiques de part et d'autre — chaque comparaison porte sa source exacte.</span></h3>
 <div class="warn">⚠️ <b>D'où viennent les repères —</b> ils ne figurent <u>pas</u> dans les documents locaux fournis. La colonne <b>France</b> vient de publications nationales INSEE/SDES ; la colonne <b>Indre (département)</b> est relevée sur le dossier INSEE du département. Le bassin est décrit au RP2022 (millésime des documents), l'Indre au RP2023 (dossier en ligne le plus récent) : l'écart d'un an est négligeable sur ces indicateurs structurels, et chaque année est indiquée. L'intérêt du repère départemental : il montre que le bassin <b>diverge même de son propre département</b>, déjà rural et industriel — le signal le plus fort restant la <b>surreprésentation de l'industrie</b>.</div>
 <div class="gauto">
  ${ccard("L'industrie, ADN du territoire","Part de l'industrie dans l'emploi · bassin 2022 / Indre & France",I.part_industrie_emploi_pct_2022,I.comparaison_indre.part_pct,I.comparaison_national.part_industrie_emploi_france_pct_2022,'cxt-ind','%',I.comparaison_national.source+' — Indre : '+X._meta.source_indre,"Le bassin est <b>près de 2 fois plus industriel que l'Indre</b> (déjà très industriel) et <b>2,5 fois plus que la France</b>. C'est ce qui rend les tensions sur les métiers techniques (maintenance, usinage, machines numériques) si centrales dans l'enquête.")}
  ${ccard("Un chômage au-dessus de la moyenne","Taux de chômage au sens du recensement · bassin 2022 / Indre & France",E.taux_chomage_recensement_pct_2022,E.comparaison_indre.taux_chomage_pct,E.comparaison_national.taux_chomage_recensement_france_metro_pct_2022,'cxt-cho','%',E.comparaison_national.source+' — Indre : '+X._meta.source_indre,"Un chômage supérieur à l'Indre comme à la France <u>coexiste</u> avec de fortes difficultés de recrutement : le problème est moins le nombre de demandeurs que <b>l'adéquation des qualifications</b> (adéquation jugée 2,9/5 par les acteurs de l'emploi).")}
  ${ccard("Un parc de logements en déprise","Part des logements vacants · bassin 2022 / Indre & France",LO.logements_vacants_pct_2022,LO.comparaison_indre.vacants_pct,LO.comparaison_national.logements_vacants_france_pct_2022,'cxt-log','%',LO.comparaison_national.source+' — Indre : '+X._meta.source_indre,"Au-dessus de l'Indre et près du double de la France, et en hausse (11,3 % en 2011). Un signal de déprise qui pèse sur l'attractivité — image notée 2,3/5 par les entreprises.")}
  ${ccard("Une population qui vieillit","Part des 60 ans et plus (repère France ; banding départemental non comparable)",D.part_60_plus_pct,null,D.comparaison_national.part_60_plus_france_pct,'cxt-a60','%',D.comparaison_national.source,"Le vieillissement redouble l'enjeu démographique relevé en entreprise (47 % des salariés ont 45 ans et +) : il faut <b>à la fois</b> attirer de la main-d'œuvre <b>et</b> transmettre les savoir-faire.")}
 </div>

 <h3 class="sec">Démographie & qualification<span>Une population âgée, peu diplômée, sur un socle d'ouvriers et de CAP-BEP.</span></h3>
 <div class="grid g2">
  <div class="card"><h3>Structure par âge (2022)</h3><p class="note">Répartition de la population par grande tranche d'âge.</p>${chCanvas('cxt-age')}<div class="src">Source : INSEE, RP2022, géographie au 01/01/2025.</div><div class="lec"><b>💡</b> Plus d'un tiers de la population a 60 ans et plus, et le cœur d'âge actif (15-44 ans) ne pèse que ~28 % : le <b>renouvellement de la main-d'œuvre</b> est un enjeu structurel.</div></div>
  <div class="card"><h3>Un territoire d'ouvriers et de CAP-BEP</h3><p class="note">Diplôme le plus élevé — population non scolarisée de 15 ans ou plus (2022).</p>${chCanvas('cxt-dip',true)}<div class="src">Source : INSEE, RP2022. Repère national : ${DI.comparaison_national.source}</div><div class="lec"><b>💡 Lien —</b> Le CAP-BEP est le diplôme dominant (32,2 %) ; les diplômés du supérieur ne sont que <b>19,8 %</b> (≈ un tiers au niveau national). Cela éclaire l'alerte des prescripteurs sur le niveau de qualification (frein n°1, 4,3/5) et celle des syndicats sur les savoirs de base.</div></div>
 </div>

 <h3 class="sec">Mobilité & tissu économique<span>Un bassin de déplacements, porté par quelques grosses unités industrielles.</span></h3>
 <div class="grid g3">
  ${metricCard(fmt(MO.part_actifs_travaillant_hors_commune_pct_2022)+' %','des actifs travaillent hors de leur commune (2022)','48,4 % en 2011 — mobilité croissante')}
  ${metricCard(fmt(E.indice_concentration_emploi_2022),'emplois pour 100 actifs résidents occupés','> 100 : le bassin attire des travailleurs')}
  ${metricCard(fmtT(TE.etablissements_actifs_2023),'établissements actifs (2023)','industrie = '+fmt(TE.repartition_pct.industrie)+' % des établissements mais 32 % des emplois')}
 </div>
 <div class="lec" style="margin-top:10px"><b>💡 Lien avec le diagnostic —</b> 55 % des actifs sortent de leur commune pour travailler : la mobilité — jugée très diversement dans l'enquête (2,1/5 par les entreprises, 3,7 par les acteurs, citée par 6/7 syndicats) — est bien un <b>enjeu objectif</b>. Et l'emploi industriel repose sur quelques grosses unités, ce qui correspond à l'effet de poids du plus gros employeur observé chez les entreprises.</div>

 <h3 class="sec">Les jeunes du territoire — Mission Locale (2025)<span>Jeunes de 16 à 25 ans accompagnés vers l'emploi et l'autonomie.</span></h3>
 <div class="grid g4">
  ${metricCard(fmtT(J.premier_accueil),'jeunes en 1er accueil (2025)',fmt(J.premier_accueil_evol_pct)+' % vs 2024')}
  ${metricCard(fmtT(J.accompagnes),'jeunes accompagnés','majorité de 18-21 ans')}
  ${metricCard('≈ '+fmt(J.niveau_infra_bac_1er_accueil_pct)+' %','de niveau infra-bac (1er accueil)','72,8 % parmi les accompagnés')}
  ${metricCard(fmt(J.sans_permis_pct)+' %','sans permis de conduire',"frein de mobilité à l'insertion")}
 </div>
 <div class="grid g2" style="margin-top:16px">
  <div class="card"><h3>Que deviennent les jeunes ? (entrées en situation 2025)</h3><p class="note">${fmtT(J.entrees_en_situation)} entrées en situation sur l'année.</p>${chCanvas('cxt-ml')}<div class="src">Source : ${J.source}</div><div class="lec"><b>💡 Lien —</b> L'insertion des jeunes passe surtout par <b>l'emploi direct</b> (${J.entrees_emploi}) plus que par la formation (${J.entrees_formation}) : cohérent avec un public peu qualifié et des entreprises en manque de bras. La Mission Locale est en lien avec <b>${J.entreprises_en_contact} entreprises</b> — un relais opérationnel pour la GPEC-T.</div></div>
  <div class="card"><h3>Un public jeune, peu qualifié et peu mobile</h3><p class="note">Profil des jeunes accueillis (2025).</p>
   <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.7">
    <li>Majoritairement âgés de <b>18 à 21 ans</b>, en début de parcours.</li>
    <li><b>~70 %</b> de niveau infra-bac (1er accueil), 72,8 % parmi les accompagnés.</li>
    <li><b>57,6 %</b> logés chez leurs parents · <b>52,5 %</b> sans permis.</li>
    <li>Orientations France Travail en forte hausse : <b>24,2 %</b> des entrées (vs 13,7 % avant), effet de la loi Plein Emploi.</li>
   </ul>
   <div class="lec"><b>💡 Lien —</b> Ces freins (qualification, mobilité, autonomie) recoupent exactement le diagnostic des acteurs de l'emploi et des syndicats. La jeunesse est le <b>vivier de main-d'œuvre à sécuriser</b> pour les axes A5 (mobilité) et A6 (qualification & socles).</div>
  </div>
 </div>

 <div class="card" style="margin-top:16px"><h3>Sources de cette page</h3><p class="src" style="font-size:12px;color:var(--mut)">
  ${X._meta.source_insee}<br>
  Département de l'Indre : ${X._meta.source_indre}<br>
  Industrie (France) : ${I.comparaison_national.source}<br>
  Chômage (France) : ${E.comparaison_national.source}<br>
  Logements vacants (France) : ${LO.comparaison_national.source}<br>
  60 ans et + (France) : ${D.comparaison_national.source}<br>
  Diplôme (repère national) : ${DI.comparaison_national.source}<br>
  Jeunes : ${J.source}<br>
  <i>${X._meta.verification} ${X._meta.note_vintage}</i></p></div>`;
 const a=D.ages_pct_2022, age15_44=Math.round((100-a['0_14']-a['45_59']-D.part_60_plus_pct)*10)/10;
 CQ.push(()=>dough('cxt-age',['0-14 ans','15-44 ans','45-59 ans','60 ans et +'],[a['0_14'],age15_44,a['45_59'],D.part_60_plus_pct],['#5b8fc9','#2e8b57','#c55a11','#7030a0']));
 const r=DI.repartition_pct;
 CQ.push(()=>hbar('cxt-dip',['Aucun diplôme / CEP','BEPC, brevet, DNB','CAP, BEP','Bac / brevet pro','Bac +2','Bac +3 / +4','Bac +5 et +'],
   [r.aucun_diplome_cep,r.bepc_dnb,r.cap_bep,r.bac_brevet_pro,r.bac_plus_2,r.bac_plus_3_4,r.bac_plus_5_et_plus],'#1f4e79',40,'%'));
 CQ.push(()=>hbar('cxt-ml',['Emploi','Formation','Retour en scolarité','Alternance','Service civique','Création'],
   [J.entrees_emploi,J.entrees_formation,J.entrees_retour_scolarite,J.entrees_alternance,J.entrees_service_civique,J.entrees_creation],'#c55a11',J.entrees_emploi));
 CQ.forEach(f=>{try{f()}catch(e){}});CQ=[];};
BUILD.comp=function(){const host=document.getElementById('p-comp');
 host.innerHTML=`<div class="banner"><b>En clair :</b> tout le monde anticipe l'IA et la robotique, mais l'offre locale n'est pas encore prête à les enseigner — le décalage le plus net concerne la cybersécurité.</div><h2 class="pt">Compétences &amp; intelligence artificielle</h2><p class="sub">Ce qui manque aujourd'hui et ce qu'il faudra savoir faire demain.</p>
 <div class="gauto">${auto('of','Q2.2_capacite_emergentes')}${auto('entreprises','Q6.5_competences_3_5ans')}${auto('acteurs','Q6.2_manque_formation')}${auto('of','Q8.2_domaines_evolutions')}${auto('entreprises','Q6.2_tech_manquantes')}${auto('syndicats','Q12_competences_techniques')}</div>`;
 CQ.forEach(f=>{try{f()}catch(e){}});CQ=[];};
BUILD.cx=function(){const host=document.getElementById('p-cx');const co=SV._meta.colleges;
 host.innerHTML=`<div class="banner"><b>En clair :</b> sur l'offre, la mobilité, la transmission et l'AFEST, les 4 collèges ne sont pas d'accord. Ces écarts sont le vrai sujet du diagnostic.</div><h2 class="pt">Croisements — les écarts de perception</h2><p class="sub">Sur un même sujet, qui voit quoi ? Moyennes 1-5.</p><div class="gauto" id="cxh"></div>
 <h3 class="sec" style="margin-top:22px">Points de consensus — les 4 collèges s'accordent</h3><div class="grid g2">${SV.convergences.map(x=>`<div class="card" style="border-left:4px solid var(--of)"><p style="font-size:13px;margin:2px 0">✅ ${x}</p></div>`).join('')}</div>
 <h3 class="sec" style="margin-top:22px">Paradoxes à porter au débat</h3><div class="grid g2" id="cxp"></div>`;
 const W=[['adéquation de l\'offre','Offre de formation locale'],['mobilité','Mobilité comme frein'],['transmission','Transmission (priorité)'],['afest','AFEST (maîtrise)'],['image','Image du territoire']];
 const host2=document.getElementById('cxh');
 W.forEach((w,i)=>{const d=dim(w[0]);if(!d)return;const cs=['entreprises','of','acteurs','syndicats'].filter(c=>typeof d.valeurs[c]==='number');const id='cxc'+i;
  host2.insertAdjacentHTML('beforeend',`<div class="card"><h3>${w[1]}</h3><p class="note">Moyenne 1-5 · écart ${fmt(d.ecart)}</p>${chCanvas(id)}</div>`);
  vbar(id,cs.map(c=>co[c].libelle),cs.map(c=>d.valeurs[c]),cs.map(c=>COL[c]));});
 document.getElementById('cxp').innerHTML=SV.paradoxes.map(p=>`<div class="card"><h3>${p.titre}</h3><p style="font-size:13px">${p.detail}</p></div>`).join('');};
BUILD.mx=function(){const host=document.getElementById('p-mx');
 function ec(e){if(e==null)return '#bcc6d0';if(e>=1.5)return '#b3261e';if(e>=1)return '#d97706';if(e>=.5)return '#ca8a04';return '#2e8b57';}
 let h=`<div class="banner"><b>En clair :</b> une vue d'ensemble de toutes les comparaisons et de l'ampleur des désaccords.</div><h2 class="pt">Matrice comparative</h2><p class="sub">Un collège par colonne. « — » = question non posée à ce collège. Écart = plus haute − plus basse valeur.</p><div style="overflow-x:auto"><table class="mx"><thead><tr><th>Dimension</th><th>Entreprises</th><th>OF</th><th>Acteurs</th><th>Syndicats</th><th>Écart</th></tr></thead><tbody>`;
 SV.dimensions_partagees.forEach(d=>{const v=d.valeurs;h+=`<tr><td class="dim">${d.dimension}</td><td>${fmt(v.entreprises)}</td><td>${fmt(v.of)}</td><td>${fmt(v.acteurs)}</td><td>${fmt(v.syndicats)}</td><td>${d.ecart==null?'<span style="color:#94a3b8">n.c.</span>':`<span class="ec" style="background:${ec(d.ecart)}">${fmt(d.ecart)}</span>`}</td></tr>`;});
 h+=`</tbody></table></div><p class="sub" style="margin-top:10px">Plus l'écart est foncé, plus les acteurs divergent.</p>`;host.innerHTML=h;};
// PLAN
function ficheHTML(f){return `<div class="card fiche"><div class="fhead"><span class="fcode">${f.code}</span><h3>${f.titre}</h3><span class="prio ${f.prioCls}">${f.prio}</span></div>
 <p class="fhz">⏱ ${f.horizon}</p><div class="lec"><b>📊 Constat —</b> ${f.constat}</div>
 <p><b>🎯 Objectif.</b> ${f.objectif}</p><p><b>👥 Cibles :</b> ${f.cibles.join(' · ')}</p>
 <p><b>🧭 Porteur pressenti :</b> ${f.porteur}</p><p><b>🤝 Partenaires :</b> ${f.partenaires.join(', ')}</p>
 <p><b>🔧 Actions concrètes</b></p><ul>${f.actions.map(a=>`<li>${a}</li>`).join('')}</ul>
 <p><b>🗓 Jalons</b></p><ul>${f.jalons.map(j=>`<li><b>${j.q} :</b> ${j.t}</li>`).join('')}</ul>
 <p><b>📦 Livrables :</b> ${f.livrables.join(' · ')}</p>
 <p><b>📈 Indicateurs de réussite</b></p><table class="kpi"><tr><th>Indicateur</th><th>Cible</th></tr>${f.kpi.map(k=>`<tr><td>${k.i}</td><td>${k.c}</td></tr>`).join('')}</table>
 <p><b>💶 Moyens / financements :</b> ${f.moyens}</p><p><b>⚠️ Risques &amp; vigilance :</b> ${f.risques}</p></div>`;}
BUILD.plan1=function(){const host=document.getElementById('p-plan1');
 host.innerHTML=`<div class="banner"><b>Plan d'action GPECT —</b> 7 axes pour passer du diagnostic à l'action, chacun fondé sur des chiffres vérifiés. Cette page : la vue d'ensemble (priorisation & calendrier). Les fiches détaillées sont dans les onglets suivants.</div>
 <h2 class="pt">Plan d'action — vue d'ensemble</h2><p class="sub">Priorisation par impact / effort, et séquencement dans le temps.</p>
 <div class="grid g2"><div class="card"><h3>Carte impact / effort</h3><p class="note">Estimation experte. En haut à gauche = fort impact, effort modéré (à lancer en premier).</p>${chCanvas('c-ie','tall')}</div>
 <div class="card"><h3>Les 7 axes en bref</h3><table class="kpi"><tr><th>Axe</th><th>Priorité</th><th>Horizon</th></tr>${PLAN.map(f=>`<tr><td><b>${f.code}</b> ${f.titre}</td><td>${f.prio}</td><td>${f.phase}</td></tr>`).join('')}</table></div></div>
 <h3 class="sec" style="margin-top:22px">Séquencement dans le temps</h3>
 <div class="timeline">
  <div class="tl"><h4>⚡ Court terme (0-6 mois)</h4><ul>${PLAN.filter(f=>f.phase=='Court terme').map(f=>`<li><b>${f.code}</b> ${f.titre}</li>`).join('')}<li><b>A7</b> Animation : démarrage immédiat</li></ul></div>
  <div class="tl"><h4>🚧 Moyen terme (6-24 mois)</h4><ul>${PLAN.filter(f=>f.phase=='Moyen terme').map(f=>`<li><b>${f.code}</b> ${f.titre}</li>`).join('')}</ul></div>
  <div class="tl"><h4>🏗 Long terme (24-36 mois)</h4><ul><li><b>A3</b> Offre Industrie 4.0 pérenne</li><li><b>A6</b> Pré-qualification ajustée aux tensions</li></ul></div>
 </div>`;
 const pts=PLAN.map(f=>({x:f.effort,y:f.impact,code:f.code}));
 new Chart(document.getElementById('c-ie'),{type:'scatter',data:{datasets:[{data:pts,backgroundColor:'#0b6e99',pointRadius:16,pointHoverRadius:18}]},
  options:{responsive:true,maintainAspectRatio:false,scales:{x:{title:{display:true,text:'Effort →'},min:1,max:5.4,grid:{color:'#eef2f7'}},y:{title:{display:true,text:'Impact →'},min:1,max:5.4,grid:{color:'#eef2f7'}}},
   plugins:{tooltip:{callbacks:{label:c=>PLAN[c.dataIndex].code+' — '+PLAN[c.dataIndex].titre+' (impact '+c.parsed.y+', effort '+c.parsed.x+')'}}},
   animation:false},plugins:[{afterDatasetsDraw(ch){const ctx=ch.ctx;ch.data.datasets[0].data.forEach((p,i)=>{const m=ch.getDatasetMeta(0).data[i];ctx.fillStyle='#fff';ctx.font='bold 11px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(p.code,m.x,m.y);});}}]});};
BUILD.plan2=function(){document.getElementById('p-plan2').innerHTML=`<div class="banner"><b>Fiches-actions détaillées (1/2)</b> — axes A1 à A4. Chaque fiche : constat chiffré, objectif, porteurs, actions, jalons, livrables, indicateurs, moyens, risques.</div><h2 class="pt">Fiches-actions A1 → A4</h2><div class="grid g2">${PLAN.slice(0,4).map(ficheHTML).join('')}</div>`;};
BUILD.plan3=function(){document.getElementById('p-plan3').innerHTML=`<div class="banner"><b>Fiches-actions détaillées (2/2)</b> — axes A5 à A7.</div><h2 class="pt">Fiches-actions A5 → A7</h2><div class="grid g2">${PLAN.slice(4).map(ficheHTML).join('')}</div>`;};
BUILD.plan4=function(){document.getElementById('p-plan4').innerHTML=`<div class="banner"><b>Pilotage de la démarche —</b> gouvernance, financements et facteurs clés de succès.</div><h2 class="pt">Pilotage &amp; conditions de réussite</h2>
 <div class="grid g2">
  <div class="card"><h3>🏛 Gouvernance proposée</h3><ul style="font-size:13px"><li><b>Comité de pilotage</b> : financeurs, intercommunalité, Région, État (DDETSPP), partenaires sociaux — décisions & arbitrages.</li><li><b>Animateur GPECT</b> dédié : cheville ouvrière, « aller-vers » les entreprises.</li><li><b>Groupes de travail thématiques</b> : un par axe, en ateliers courts (2h) à livrable.</li><li><b>Revue semestrielle</b> des indicateurs (ré-enquête à 24 mois).</li></ul></div>
  <div class="card"><h3>💶 Financements mobilisables</h3><ul style="font-size:13px"><li><b>OPCO</b> (dont OPCO 2i) : ingénierie, tutorat, AFEST, formation des salariés.</li><li><b>France Travail</b> : POEI, PMSMP, aides à la mobilité, forums.</li><li><b>Région Centre-Val de Loire</b> : carte des formations, attractivité, mobilité.</li><li><b>État</b> : Plan d'investissement dans les compétences, FNE-Formation, Territoires d'industrie.</li><li><b>Chambres consulaires</b> : transmission-reprise (artisanat).</li></ul></div>
 </div>
 <h3 class="sec" style="margin-top:20px">✅ Facteurs clés de succès (issus des verbatims)</h3>
 <div class="grid g3">
  <div class="card"><h3>Du concret, vite</h3><p style="font-size:13px">« Réunions qui ne mènent à rien » : chaque atelier doit produire un livrable. Des résultats rapides (forums, navettes) crédibilisent la démarche.</p></div>
  <div class="card"><h3>Aller-vers les entreprises</h3><p style="font-size:13px">L'animateur se déplace en entreprise (« bâton de pèlerin ») avec des outils simples (pyramide des âges, compétences clés).</p></div>
  <div class="card"><h3>N'oublier personne</h3><p style="font-size:13px">Inclure les artisans et sous-traitants, pas seulement les grands donneurs d'ordre ; associer patronat ET syndicats de salariés.</p></div>
 </div>
 <h3 class="sec" style="margin-top:20px">🔗 Synergies entre axes</h3>
 <div class="card"><p style="font-size:13px">L'<b>observatoire (A2)</b> alimente l'attractivité (A1), la pré-qualification (A6) et les compétences de demain (A3). L'<b>animation (A7)</b> conditionne la réussite de tous les autres axes. La <b>mobilité (A5)</b> est un prérequis transversal à l'accès à l'emploi et à la formation.</p></div>`;};
BUILD.met=function(){const m=SV.donnees_colleges;document.getElementById('p-met').innerHTML=`<div class="banner">Comment ce diagnostic a été produit, et ses limites — en toute transparence.</div><h2 class="pt">Méthode &amp; repères</h2>
 <div class="grid g2"><div class="card"><h3>Périmètre &amp; principe</h3><p style="font-size:13px"><b>42 répondants</b> : 21 entreprises, 7 organismes de formation, 7 acteurs de l'emploi, 7 syndicats/organisations professionnelles. Analyse <b>agrégée et anonyme</b> (jamais structure par structure ; aucun nom ; verbatims anonymisés). Choix multiples comptés par mot-clé. Chiffres <b>vérifiés par un audit de traçabilité</b> (recalcul depuis les fichiers sources).</p></div>
 <div class="card"><h3>Prudence statistique</h3><p style="font-size:13px">Trois collèges à <b>n=7</b> : résultats en <b>tendances</b>. <b>Effet de poids</b> : un employeur ≈ la moitié de l'effectif → effectif & pyramide donnés <b>avec/sans</b>. <b>Collège formation</b> : l'un des 7 organismes achète des formations sans en dispenser (non-formateur) — il tire les moyennes de capacité vers le bas, d'où la mention « avec / sans ». Données <b>déclaratives</b> (auto-évaluations à pondérer).</p></div></div>
 <div class="card" style="margin-top:16px"><h3>Glossaire</h3><dl class="glo" style="font-size:13px;columns:2;column-gap:24px">
 <dt>GPECT</dt><dd>Gestion Prévisionnelle des Emplois et des Compétences, à l'échelle d'un Territoire.</dd>
 <dt>OF</dt><dd>Organisme de formation.</dd><dt>AFEST</dt><dd>Action de Formation En Situation de Travail (se former en travaillant, encadré).</dd>
 <dt>OPCO</dt><dd>Opérateur de Compétences (finance la formation d'une branche).</dd>
 <dt>POEI</dt><dd>Préparation Opérationnelle à l'Emploi (formation avant embauche).</dd>
 <dt>PMSMP</dt><dd>Période de Mise en Situation en Milieu Professionnel (immersion).</dd>
 <dt>CNC</dt><dd>Commande Numérique (machines pilotées par ordinateur).</dd><dt>CAO / DAO</dt><dd>Conception / Dessin Assisté par Ordinateur.</dd>
 <dt>ERP / GPAO</dt><dd>Logiciels de gestion industrielle.</dd><dt>Cobotique</dt><dd>Robots collaboratifs.</dd>
 <dt>Métrologie</dt><dd>Science de la mesure (contrôle qualité).</dd><dt>CACES / SPL</dt><dd>Permis d'engins / poids lourds.</dd>
 <dt>VAE</dt><dd>Validation des Acquis de l'Expérience.</dd><dt>CFA</dt><dd>Centre de Formation d'Apprentis.</dd><dt>QPV</dt><dd>Quartier Prioritaire de la Ville.</dd></dl></div>
 <div class="card" style="margin-top:16px"><h3>Sources</h3><p style="font-size:12.5px;color:var(--mut)">Entreprises : ${m.entreprises.meta.source} (${m.entreprises.meta.source_date}).<br>Organismes de formation : ${m.of.meta.source} (${m.of.meta.source_date}).<br>Acteurs de l'emploi : ${m.acteurs.meta.source} (${m.acteurs.meta.source_date}).<br>Syndicats / orga pro : ${m.syndicats.meta.source} (${m.syndicats.meta.source_date}).<br>Tableau de bord généré à partir du fichier unique « source de vérité ».</p></div>`;};

const NAV=[['synthese','Synthèse',''],['cxt','Contexte territorial','REPÈRES INSEE'],['ent','Entreprises','COLLÈGES'],['of','Org. formation',''],['act','Acteurs emploi',''],['syn','Syndicats',''],['comp','Compétences & IA','TRANSVERSAL'],['cx','Croisements',''],['mx','Matrice',''],['plan1','Vue d\'ensemble','PLAN D\'ACTION'],['plan2','Fiches A1-A4',''],['plan3','Fiches A5-A7',''],['plan4','Pilotage',''],['met','Méthode','']];
document.getElementById('nav').innerHTML=NAV.map(n=>(n[2]?`<span class="grp">${n[2]}</span>`:'')+`<button data-id="${n[0]}" onclick="show('${n[0]}')">${n[1]}</button>`).join('');
const inited={};
function show(id){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.querySelectorAll('#nav button').forEach(b=>b.classList.remove('active'));
 document.getElementById('p-'+id).classList.add('active');const ab=document.querySelector('#nav button[data-id="'+id+'"]');if(ab){ab.classList.add('active');ab.scrollIntoView({inline:'center',block:'nearest'});}
 if(!inited[id]&&BUILD[id]){BUILD[id]();inited[id]=true;}window.scrollTo({top:0,behavior:'smooth'});}
BUILD.synthese();inited.synthese=true;
const tt=document.getElementById('toTop');tt.onclick=()=>window.scrollTo({top:0,behavior:'smooth'});
window.addEventListener('scroll',()=>tt.classList.toggle('show',window.scrollY>340),{passive:true});
function setNavH(){const n=document.getElementById('nav');if(n)document.documentElement.style.setProperty('--navh',n.offsetHeight+'px');}setNavH();window.addEventListener('resize',setNavH);
</script></body></html>"""

out=(HTML.replace("__CHARTJS__",CHARTJS).replace("__SVDATA__",SVDATA)
     .replace("__CXDATA__",CXDATA)
     .replace("__COMMENTS__",json.dumps(COMMENTS,ensure_ascii=False))
     .replace("__ORDER__",json.dumps(ORDER,ensure_ascii=False))
     .replace("__PLAN__",json.dumps(PLAN,ensure_ascii=False)))
(DASH/"dashboard_gpect_issoudun_final.html").write_text(out,encoding="utf-8")
print("OK -> dashboard_gpect_issoudun_final.html  (",len(out)//1024,"Ko )")
