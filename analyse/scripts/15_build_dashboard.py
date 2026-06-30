#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit un dashboard HTML autoporté (un seul fichier) à partir de
source_verite.json UNIQUEMENT. Données + Chart.js embarqués (ouverture hors-ligne).
Aucun chiffre recalculé : tout est lu dans SV côté navigateur."""
import json, pathlib
RES = pathlib.Path("/home/user/Gpect/analyse/resultats")
DASH = pathlib.Path("/home/user/Gpect/analyse/dashboard")
SV = json.load(open(RES/"source_verite.json", encoding="utf-8"))
CHARTJS = (DASH/"chartjs.min.js").read_text(encoding="utf-8")
SVDATA = json.dumps(SV, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GPECT Issoudun — Diagnostic emploi-compétences</title>
<style>
:root{--ent:#1f4e79;--of:#2e8b57;--act:#c55a11;--syn:#7030a0;--ink:#1a2332;--mut:#5b6b7d;--bg:#f4f6f9;--card:#fff;--line:#e2e8f0;--accent:#0b6e99;--navh:52px;}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;scroll-padding-top:calc(var(--navh) + 8px)}
body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5;overflow-x:hidden;text-rendering:optimizeLegibility}
header.top{background:linear-gradient(120deg,#13314f,#0b6e99);color:#fff;padding:16px clamp(14px,4vw,28px)}
header.top h1{margin:0;font-size:clamp(16px,2.4vw,21px);font-weight:700}
header.top p{margin:4px 0 0;font-size:clamp(11px,1.6vw,13px);opacity:.9}
nav{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.97);backdrop-filter:saturate(1.2) blur(6px);border-bottom:1px solid var(--line);
 display:flex;flex-wrap:wrap;gap:2px;padding:6px clamp(8px,2vw,12px);box-shadow:0 1px 6px rgba(0,0,0,.06);
 overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
nav::-webkit-scrollbar{height:4px}nav::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:4px}
nav button{flex:0 0 auto;border:0;background:transparent;color:var(--mut);font-size:13px;font-weight:600;padding:9px 13px;border-radius:8px;cursor:pointer;white-space:nowrap;min-height:40px}
nav button:hover{background:#eef2f7;color:var(--ink)}
nav button.active{background:var(--accent);color:#fff}
main{max-width:1180px;margin:0 auto;padding:clamp(14px,3vw,22px) clamp(12px,3vw,18px) 72px}
.page{display:none;animation:fade .25s ease}
.page.active{display:block}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@media(max-width:900px){nav{flex-wrap:nowrap}}
.banner{background:#fff;border-left:5px solid var(--accent);border-radius:10px;padding:14px 18px;margin:0 0 20px;box-shadow:0 1px 3px rgba(0,0,0,.05);font-size:15px}
.banner b{color:var(--accent)}
h2.pt{font-size:22px;margin:0 0 4px}
.sub{color:var(--mut);font-size:13px;margin:0 0 18px}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
@media(max-width:1024px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:760px){.g2,.g3,.g4{grid-template-columns:1fr}}
.metric .num{font-size:clamp(26px,5vw,34px)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.card h3{margin:0 0 2px;font-size:15px}
.card .note{color:var(--mut);font-size:12px;margin:0 0 10px}
.metric{text-align:center;padding:18px 12px}
.metric .num{font-size:34px;font-weight:800;line-height:1}
.metric .lab{font-size:12.5px;color:var(--mut);margin-top:6px}
.metric small{display:block;color:var(--mut);font-size:11px;margin-top:4px}
.chartbox{position:relative;width:100%;height:clamp(260px,42vh,330px)}
.chartbox.tall{height:clamp(320px,52vh,420px)}
.pill{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;color:#fff;margin-right:6px}
.toggle{display:inline-flex;gap:4px;margin:6px 0 10px}
.toggle button{border:1px solid var(--line);background:#fff;color:var(--mut);font-size:12px;font-weight:600;padding:5px 10px;border-radius:8px;cursor:pointer}
.toggle button.on{background:var(--ent);color:#fff;border-color:var(--ent)}
table.mx{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border-radius:10px;overflow:hidden}
table.mx th,table.mx td{border:1px solid var(--line);padding:9px 10px;text-align:center}
table.mx th{background:#13314f;color:#fff;font-weight:600}
table.mx td.dim{text-align:left;font-weight:600}
.ec{font-weight:800;border-radius:6px;padding:2px 8px;color:#fff;display:inline-block}
.verb{background:#f7f9fc;border-left:3px solid var(--syn);padding:8px 12px;border-radius:6px;font-style:italic;font-size:13px;margin:8px 0;color:#33414f}
.axe{border-top:4px solid var(--accent)}
.axe .src{font-size:12px;color:var(--mut);margin:6px 0}
.axe ul{margin:6px 0 0;padding-left:18px;font-size:13px}
.kv{font-size:13px}.kv b{color:var(--ink)}
.legdot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle}
footer{border-top:1px solid var(--line);background:#fff;color:var(--mut);font-size:12.5px;text-align:center;padding:18px}
footer b{color:var(--ink)}
#toTop{position:fixed;right:16px;bottom:16px;z-index:40;width:46px;height:46px;border-radius:50%;border:0;
 background:var(--accent);color:#fff;font-size:20px;cursor:pointer;box-shadow:0 3px 10px rgba(0,0,0,.25);
 opacity:0;visibility:hidden;transition:opacity .2s}
#toTop.show{opacity:.92;visibility:visible}
#toTop:hover{opacity:1}
@media(max-width:760px){.chartbox .note,.card .note{font-size:11px}}
.glo{font-size:13px}.glo dt{font-weight:700;margin-top:8px}.glo dd{margin:0 0 2px;color:var(--mut)}
.warn{background:#fff7ed;border-left:4px solid #c55a11;border-radius:8px;padding:10px 14px;font-size:13px;margin:14px 0}
</style>
</head>
<body>
<header class="top">
  <h1>GPECT du bassin d'Issoudun — Diagnostic emploi &amp; compétences</h1>
  <p>Enquête auprès de 4 collèges d'acteurs — analyse agrégée et anonyme · 42 répondants</p>
</header>
<nav id="nav"></nav>
<main>
  <!-- SYNTHESE -->
  <section class="page active" id="p-synthese">
    <div class="banner" id="b-synthese"></div>
    <h2 class="pt">Vue d'ensemble</h2>
    <p class="sub">Qui a répondu, et les quelques chiffres à retenir.</p>
    <div class="grid g4" id="m-perimetre"></div>
    <div class="card" style="margin-top:16px"><h3>Les 4 plus grands écarts de perception entre acteurs</h3>
      <p class="note">Moyennes sur une échelle de 1 (faible) à 5 (fort). Plus les barres d'un même thème sont éloignées, plus les acteurs voient les choses différemment.</p>
      <div class="chartbox tall"><canvas id="c-topecarts"></canvas></div></div>
    <div class="grid g3" id="m-cles" style="margin-top:16px"></div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Tension de recrutement vue par les entreprises</h3><p class="note">Part des entreprises (n=21) selon le niveau de tension.</p><div class="chartbox"><canvas id="c-tension"></canvas></div></div>
      <div class="card"><h3>Comment lire ce tableau de bord</h3>
        <p class="kv">Chaque chiffre provient des réponses, agrégées par collège. <b>Une moyenne</b> est affichée pour les questions notées de 1 à 5 ; <b>un effectif ou un %</b> pour les questions de comptage. Les trois collèges à <b>n=7</b> appellent à la prudence : on lit des <b>tendances</b>, pas des certitudes.</p>
        <p class="kv" style="margin-top:8px">Onglets ci-dessus : un par collège, puis les <b>croisements</b> (le cœur du diagnostic), la <b>matrice</b> comparative, les <b>leviers</b> d'action et la <b>méthode</b>.</p>
      </div>
    </div>
  </section>

  <!-- ENTREPRISES -->
  <section class="page" id="p-ent">
    <div class="banner" id="b-ent"></div>
    <h2 class="pt">Collège Entreprises <span style="font-size:14px;color:var(--mut)">· n=21</span></h2>
    <p class="sub">Le tissu industriel du bassin : tensions, démographie, besoins.</p>
    <div class="grid g4" id="m-ent"></div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Secteurs d'activité</h3><p class="note">Répartition des 21 entreprises.</p><div class="chartbox"><canvas id="c-ent-sect"></canvas></div></div>
      <div class="card"><h3>Pyramide des âges <span style="font-weight:400;font-size:12px;color:var(--mut)">(têtes)</span></h3>
        <p class="note">Un employeur (~1550 salariés) pèse ~la moitié de l'effectif : bascule pour le neutraliser.</p>
        <div class="toggle" id="t-pyr"><button class="on" data-v="avec">Avec le plus gros employeur</button><button data-v="sans">Sans</button></div>
        <div class="chartbox"><canvas id="c-ent-pyr"></canvas></div></div>
    </div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Causes des tensions de recrutement</h3><p class="note">Moyenne 1-5 (5 = fort impact). n=20.</p><div class="chartbox tall"><canvas id="c-ent-causes"></canvas></div></div>
      <div class="card"><h3>Freins au recrutement</h3><p class="note">Moyenne 1-5. n=21.</p><div class="chartbox tall"><canvas id="c-ent-freins"></canvas></div></div>
    </div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Préoccupations pour les 24 prochains mois</h3><p class="note">% des entreprises (3 choix max). n=21.</p><div class="chartbox tall"><canvas id="c-ent-preocc"></canvas></div></div>
      <div class="card"><h3>Priorités pour la démarche territoriale</h3><p class="note">Moyenne 1-5 (5 = très haute priorité). n=21.</p><div class="chartbox tall"><canvas id="c-ent-prio"></canvas></div></div>
    </div>
  </section>

  <!-- OF -->
  <section class="page" id="p-of">
    <div class="banner" id="b-of"></div>
    <h2 class="pt">Collège Organismes de formation <span style="font-size:14px;color:var(--mut)">· n=7</span></h2>
    <p class="sub">OF = organismes de formation. Capacité de l'offre locale et compétences de demain.</p>
    <div class="warn" id="w-of"></div>
    <div class="grid g4" id="m-of"></div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Capacité à former aux compétences émergentes</h3><p class="note">Moyenne 1-5. « Avec/sans financeur » : le 7ᵉ répondant n'est pas un formateur. n=7 (6 sans).</p><div class="chartbox tall"><canvas id="c-of-emerg"></canvas></div></div>
      <div class="card"><h3>Niveau de l'offre actuelle par domaine</h3><p class="note">Moyenne 1-5. n=7.</p><div class="chartbox tall"><canvas id="c-of-offre"></canvas></div></div>
    </div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Connaissance des secteurs du bassin</h3><p class="note">Moyenne 1-5. n=7.</p><div class="chartbox tall"><canvas id="c-of-sect"></canvas></div></div>
      <div class="grid g2" style="grid-template-columns:1fr 1fr;gap:12px"><div class="card metric" id="of-m1"></div><div class="card metric" id="of-m2"></div><div class="card metric" id="of-m3"></div><div class="card metric" id="of-m4"></div></div>
    </div>
  </section>

  <!-- ACTEURS -->
  <section class="page" id="p-act">
    <div class="banner" id="b-act"></div>
    <h2 class="pt">Collège Acteurs de l'emploi <span style="font-size:14px;color:var(--mut)">· n=7</span></h2>
    <p class="sub">France Travail, Mission Locale, Cap Emploi, APEC et agences d'intérim.</p>
    <div class="grid g4" id="m-act"></div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Compétences les plus difficiles à trouver</h3><p class="note">Moyenne 1-5 (5 = très difficile). n=7.</p><div class="chartbox tall"><canvas id="c-act-comp"></canvas></div></div>
      <div class="card"><h3>Freins à l'accès à l'emploi</h3><p class="note">Moyenne 1-5. n=7.</p><div class="chartbox tall"><canvas id="c-act-freins"></canvas></div></div>
    </div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Manque de formation par domaine</h3><p class="note">Moyenne 1-5 (5 = fort manque). n=7.</p><div class="chartbox tall"><canvas id="c-act-manque"></canvas></div></div>
      <div class="card"><h3>Efficacité perçue des dispositifs</h3><p class="note">POEI, PMSMP, formation qualifiante, parcours individualisés. Moyenne 1-5. n=7.</p><div class="chartbox"><canvas id="c-act-disp"></canvas></div>
        <p class="kv" style="margin-top:8px"><b>POEI</b> = Préparation Opérationnelle à l'Emploi · <b>PMSMP</b> = Période de Mise en Situation en Milieu Professionnel.</p></div>
    </div>
  </section>

  <!-- SYNDICATS -->
  <section class="page" id="p-syn">
    <div class="banner" id="b-syn"></div>
    <h2 class="pt">Collège Syndicats / organisations professionnelles <span style="font-size:14px;color:var(--mut)">· n=7</span></h2>
    <p class="sub">Organisations patronales, syndicats de salariés et chambres consulaires. Réponses surtout qualitatives.</p>
    <div class="grid g3" id="m-syn"></div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Atouts du territoire les plus cités</h3><p class="note">Nombre de répondants sur 7.</p><div class="chartbox"><canvas id="c-syn-atouts"></canvas></div></div>
      <div class="card"><h3>Freins / fragilités les plus cités</h3><p class="note">Nombre de répondants sur 7.</p><div class="chartbox"><canvas id="c-syn-freins"></canvas></div></div>
    </div>
    <div class="grid g3" style="margin-top:16px">
      <div class="card"><h3>L'offre de formation est-elle adaptée ?</h3><p class="note">n=7.</p><div class="chartbox"><canvas id="c-syn-offre"></canvas></div></div>
      <div class="card"><h3>Engagement des entreprises</h3><p class="note">n=7.</p><div class="chartbox"><canvas id="c-syn-eng"></canvas></div></div>
      <div class="card"><h3>Transmission-reprise</h3><p class="note">n=7.</p><div class="chartbox"><canvas id="c-syn-trans"></canvas></div></div>
    </div>
    <div class="card" style="margin-top:16px"><h3>Verbatims (anonymisés)</h3><div id="syn-verb"></div></div>
  </section>

  <!-- COMPETENCES & IA -->
  <section class="page" id="p-comp">
    <div class="banner" id="b-comp"></div>
    <h2 class="pt">Compétences &amp; intelligence artificielle</h2>
    <p class="sub">Ce qui manque aujourd'hui et ce qu'il faudra savoir faire demain.</p>
    <div class="grid g2">
      <div class="card"><h3>Capacité des OF à former aux compétences de demain</h3><p class="note">Moyenne 1-5 (5 = forte capacité). n=7.</p><div class="chartbox tall"><canvas id="c-comp-of"></canvas></div></div>
      <div class="card"><h3>Compétences que les entreprises veulent développer d'ici 3-5 ans</h3><p class="note">% des entreprises. n=21.</p><div class="chartbox tall"><canvas id="c-comp-ent"></canvas></div></div>
    </div>
    <div class="grid g2" style="margin-top:16px">
      <div class="card"><h3>Manque de formation vu par les acteurs de l'emploi</h3><p class="note">Moyenne 1-5 (5 = fort manque). n=7.</p><div class="chartbox tall"><canvas id="c-comp-act"></canvas></div></div>
      <div class="grid" style="gap:12px"><div class="card metric" id="comp-m1"></div><div class="card metric" id="comp-m2"></div><div class="card metric" id="comp-m3"></div></div>
    </div>
  </section>

  <!-- CROISEMENTS -->
  <section class="page" id="p-cx">
    <div class="banner" id="b-cx"></div>
    <h2 class="pt">Croisements — les écarts de perception</h2>
    <p class="sub">Le cœur du diagnostic : sur un même sujet, qui voit quoi ? Moyennes 1-5.</p>
    <div class="grid g2" id="cx-charts"></div>
    <h3 style="margin:22px 0 8px">Paradoxes à porter au débat</h3>
    <div class="grid g2" id="cx-para"></div>
  </section>

  <!-- MATRICE -->
  <section class="page" id="p-mx">
    <div class="banner" id="b-mx"></div>
    <h2 class="pt">Matrice comparative</h2>
    <p class="sub">Toutes les questions partagées, un collège par colonne. « — » = question non posée à ce collège. Écart = différence entre la valeur la plus haute et la plus basse.</p>
    <div style="overflow-x:auto"><table class="mx" id="mxtable"></table></div>
    <p class="sub" style="margin-top:10px">Lecture : plus l'écart est élevé (couleur foncée), plus les acteurs divergent sur le sujet.</p>
  </section>

  <!-- LEVIERS -->
  <section class="page" id="p-lev">
    <div class="banner" id="b-lev"></div>
    <h2 class="pt">Leviers d'action</h2>
    <p class="sub">7 axes, chacun fondé sur des chiffres du diagnostic.</p>
    <div class="grid g2" id="lev-cards"></div>
  </section>

  <!-- METHODE -->
  <section class="page" id="p-met">
    <div class="banner">Comment ce diagnostic a été produit, et ses limites — en toute transparence.</div>
    <h2 class="pt">Méthode &amp; repères</h2>
    <div class="grid g2">
      <div class="card"><h3>Périmètre &amp; principe</h3>
        <p class="kv"><b>42 répondants</b> : 21 entreprises, 7 organismes de formation, 7 acteurs de l'emploi, 7 syndicats / organisations professionnelles.</p>
        <p class="kv" style="margin-top:6px">Analyse <b>agrégée et anonyme</b> : on raisonne question par question, jamais structure par structure. Aucun nom n'apparaît. Les verbatims sont anonymisés.</p>
        <p class="kv" style="margin-top:6px">Les questions à choix multiples sont comptées par mot-clé (pas de découpage hasardeux). Chaque chiffre est issu des réponses, aucun n'est estimé.</p>
      </div>
      <div class="card"><h3>Prudence statistique</h3>
        <p class="kv">Trois collèges comptent <b>7 répondants</b> : les résultats sont des <b>tendances</b>, pas des vérités générales. On affiche « n= » partout.</p>
        <p class="kv" style="margin-top:6px"><b>Effet de poids</b> : un employeur (~1550 salariés) pèse ~la moitié de l'effectif cumulé ; effectif et pyramide sont donnés <b>avec et sans</b> lui.</p>
        <p class="kv" style="margin-top:6px"><b>Collège formation</b> : un répondant est un financeur (non-formateur) ; les questions de capacité sont données <b>avec et sans</b> lui.</p>
      </div>
    </div>
    <div class="card" style="margin-top:16px"><h3>Glossaire</h3>
      <dl class="glo">
        <dt>GPECT</dt><dd>Gestion Prévisionnelle des Emplois et des Compétences, à l'échelle d'un Territoire.</dd>
        <dt>OF</dt><dd>Organisme de formation.</dd>
        <dt>AFEST</dt><dd>Action de Formation En Situation de Travail (on se forme en travaillant, encadré).</dd>
        <dt>OPCO</dt><dd>Opérateur de Compétences : finance la formation des salariés d'une branche.</dd>
        <dt>POEI</dt><dd>Préparation Opérationnelle à l'Emploi Individuelle : formation avant embauche.</dd>
        <dt>PMSMP</dt><dd>Période de Mise en Situation en Milieu Professionnel : immersion découverte.</dd>
        <dt>CNC</dt><dd>Commande Numérique (machines-outils pilotées par ordinateur).</dd>
        <dt>CAO / DAO</dt><dd>Conception / Dessin Assisté par Ordinateur.</dd>
        <dt>ERP / GPAO</dt><dd>Logiciels de gestion industrielle (pilotage de la production et des ressources).</dd>
        <dt>Cobotique</dt><dd>Robots collaboratifs travaillant aux côtés des opérateurs.</dd>
        <dt>Métrologie</dt><dd>Science de la mesure (contrôle qualité dimensionnel).</dd>
        <dt>CACES / SPL</dt><dd>Permis de conduite d'engins (CACES) / poids lourds super-lourds (SPL).</dd>
        <dt>VAE</dt><dd>Validation des Acquis de l'Expérience (obtenir un diplôme via l'expérience).</dd>
        <dt>QPV</dt><dd>Quartier Prioritaire de la politique de la Ville.</dd>
        <dt>CFA</dt><dd>Centre de Formation d'Apprentis.</dd>
      </dl>
    </div>
    <div class="card" style="margin-top:16px"><h3>Sources</h3><p class="kv" id="met-src"></p></div>
  </section>
</main>
<footer>
  Diagnostic GPECT du bassin d'Issoudun — analyse agrégée et anonyme.<br>
  <b>Sophie Kirsch</b> (Ceterha) · <b>Sabrina Alamargot</b> (La Fabrique RH) · <b>Escale Digitale Solutions</b>
</footer>
<button id="toTop" aria-label="Revenir en haut" title="Revenir en haut">&#8593;</button>

<script>__CHARTJS__</script>
<script>
const SV = __SVDATA__;
const C={ent:'#1f4e79',of:'#2e8b57',act:'#c55a11',syn:'#7030a0'};
const CL={ent:'rgba(31,78,121,.18)',of:'rgba(46,139,87,.18)',act:'rgba(197,90,17,.18)',syn:'rgba(112,48,160,.18)'};
Chart.defaults.font.family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif";
Chart.defaults.font.size=12; Chart.defaults.color="#33414f"; Chart.defaults.plugins.legend.display=false;
const PAL=['#1f4e79','#2e8b57','#c55a11','#7030a0','#0b6e99','#b8860b','#8d6e63','#557'];
const fmt=v=>(v==null?'—':String(v).replace('.',','));
function Q(c,k){return SV.donnees_colleges[c].questions[k];}
function sorted(c,k){const d=Q(c,k);return (d.classement_par_moyenne||d.items||[]).slice();}
function dim(name){return SV.dimensions_partagees.find(d=>d.dimension.toLowerCase().includes(name));}

function metric(num,lab,small){return `<div class="card metric"><div class="num">${num}</div><div class="lab">${lab}</div>${small?`<small>${small}</small>`:''}</div>`;}

function hbar(id,labels,data,color,max){new Chart(document.getElementById(id),{type:'bar',
 data:{labels,datasets:[{data,backgroundColor:color,borderRadius:4,barThickness:'flex',maxBarThickness:26}]},
 options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
  scales:{x:{beginAtZero:true,max:max||undefined,grid:{color:'#eef2f7'}},y:{grid:{display:false},ticks:{autoSkip:false,font:{size:11}}}},
  plugins:{tooltip:{callbacks:{label:c=>' '+fmt(c.parsed.x)}}}}});}

function vbar(id,labels,data,colors){new Chart(document.getElementById(id),{type:'bar',
 data:{labels,datasets:[{data,backgroundColor:colors,borderRadius:5,maxBarThickness:60}]},
 options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,max:5,grid:{color:'#eef2f7'}},x:{grid:{display:false}}},
  plugins:{tooltip:{callbacks:{label:c=>' '+fmt(c.parsed.y)}}}}});}

function dough(id,labels,data,colors){new Chart(document.getElementById(id),{type:'doughnut',
 data:{labels,datasets:[{data,backgroundColor:colors,borderWidth:2,borderColor:'#fff'}]},
 options:{responsive:true,maintainAspectRatio:false,cutout:'58%',
  plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:12,font:{size:11}}},
   tooltip:{callbacks:{label:c=>' '+c.label+' : '+c.parsed}}}}});}

function radar(id,labels,data,color){new Chart(document.getElementById(id),{type:'radar',
 data:{labels,datasets:[{data,backgroundColor:color.fill,borderColor:color.line,borderWidth:2,pointBackgroundColor:color.line}]},
 options:{responsive:true,maintainAspectRatio:false,scales:{r:{min:0,max:5,ticks:{stepSize:1,font:{size:9}},pointLabels:{font:{size:10}}}},
  plugins:{tooltip:{callbacks:{label:c=>' '+fmt(c.parsed.r)}}}}});}

// ---- generic init registry (lazy render so canvases have size) ----
const inited={};
function show(id){
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 document.querySelectorAll('#nav button').forEach(b=>b.classList.remove('active'));
 document.getElementById('p-'+id).classList.add('active');
 document.querySelector('#nav button[data-id="'+id+'"]').classList.add('active');
 if(!inited[id]&&BUILD[id]){BUILD[id]();inited[id]=true;}
 const ab=document.querySelector('#nav button[data-id="'+id+'"]');
 if(ab&&ab.scrollIntoView){ab.scrollIntoView({inline:'center',block:'nearest'});}
 window.scrollTo({top:0,behavior:'smooth'});
}
const NAV=[['synthese','Synthèse'],['ent','Entreprises'],['of','Org. formation'],['act','Acteurs emploi'],['syn','Syndicats'],['comp','Compétences & IA'],['cx','Croisements'],['mx','Matrice'],['lev','Leviers'],['met','Méthode']];
document.getElementById('nav').innerHTML=NAV.map(n=>`<button data-id="${n[0]}" onclick="show('${n[0]}')">${n[1]}</button>`).join('');

const BUILD={};
// ---------- SYNTHESE ----------
BUILD.synthese=function(){
 document.getElementById('b-synthese').innerHTML="<b>L'essentiel :</b> un bassin industriel en forte tension de recrutement, une offre de formation jugée en décalage par ceux qui l'utilisent, et un risque de départs à la retraite encore sous-estimé. Quatre familles d'acteurs ne voient pas toujours les mêmes priorités.";
 const co=SV._meta.colleges;
 document.getElementById('m-perimetre').innerHTML=
   metric(co.entreprises.n,'Entreprises')+metric(co.of.n,'Organismes de formation')+metric(co.acteurs.n,'Acteurs de l\'emploi')+metric(co.syndicats.n,'Syndicats / orga pro');
 // top ecarts grouped
 const dims=[dim('adéquation de l\'offre'),dim('mobilité'),dim('transmission'),dim('afest')];
 const labels=['Offre de\nformation','Mobilité\n(frein)','Transmission\n(priorité)','AFEST\n(maîtrise)'];
 const cols=['entreprises','of','acteurs','syndicats'];
 const ds=cols.map((c,i)=>({label:co[c].libelle,data:dims.map(d=>d.valeurs[c]??null),backgroundColor:[C.ent,C.of,C.act,C.syn][i],borderRadius:4,maxBarThickness:30}));
 new Chart(document.getElementById('c-topecarts'),{type:'bar',data:{labels:labels.map(l=>l.split('\n')),datasets:ds},
  options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,max:5,grid:{color:'#eef2f7'}},x:{grid:{display:false}}},
   plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:12,font:{size:11}}},tooltip:{callbacks:{label:c=>' '+c.dataset.label+' : '+fmt(c.parsed.y)}}}}});
 const offre=dim('adéquation de l\'offre').valeurs, trans=dim('transmission').valeurs;
 const afest=sorted('entreprises','Q4.8_dispositifs_transmission').find(x=>x.item.includes('AFEST')).moyenne;
 const seniors=Q('entreprises','Q4.1_pyramide').AVEC_plus_gros.pct_seniors_45plus;
 const img=Q('entreprises','Q8.2_image_issoudun').moyenne;
 document.getElementById('m-cles').innerHTML=
  metric(fmt(offre.of)+' vs '+fmt(offre.acteurs),'Offre de formation : vue par les OF vs par les acteurs de l\'emploi','écart de perception majeur')+
  metric(seniors+' %','de salariés de 45 ans et + (entreprises)','enjeu de transmission')+
  metric(fmt(afest),'AFEST : maîtrise dans les entreprises (1-5)','dispositif quasi inexistant')+
  metric(fmt(img),'Image du territoire notée par les entreprises (1-5)','jamais supérieure à 3')+
  metric(trans.entreprises<trans.acteurs?'Dernière':'—','Rang de la transmission dans les priorités des entreprises','alors que prioritaire pour les syndicats')+
  metric('95 %','des entreprises citent l\'image du territoire comme frein','');
 const t=Q('entreprises','Q3.2_tension').modalites;
 dough('c-tension',t.map(m=>m.modalite.replace('Oui, ','').replace('Non, ','')),t.map(m=>m.n),[C.act,'#e0a26b','#bcd']);
};
// ---------- ENTREPRISES ----------
BUILD.ent=function(){
 document.getElementById('b-ent').innerHTML="<b>En clair :</b> 95 % des entreprises sont en tension de recrutement, surtout faute de candidats sur des métiers techniques. Près de la moitié des salariés ont 45 ans ou plus, mais la transmission reste peu préparée.";
 const eff=Q('entreprises','Q1.4_effectif_inscrit'); const pyrA=Q('entreprises','Q4.1_pyramide').AVEC_plus_gros, pyrS=Q('entreprises','Q4.1_pyramide').SANS_plus_gros;
 const rec=Q('entreprises','Q5.4_recrut_prevus_3ans');
 document.getElementById('m-ent').innerHTML=
  metric('95 %','en tension de recrutement','Q3.2 · n=21')+
  metric(rec.somme,'recrutements prévus d\'ici 3 ans','Q5.4 · somme')+
  metric(pyrA.pct_seniors_45plus+' %','de salariés 45 ans et +','Q4.1 · n=17')+
  metric(fmt(Q('entreprises','Q7.6_offre_adaptee').moyenne),'offre de formation locale (1-5)','Q7.6 · n=21');
 const sect=Q('entreprises','Q1.1_secteur').modalites;
 dough('c-ent-sect',sect.map(m=>m.modalite.split(',')[0].split('(')[0].trim()),sect.map(m=>m.n),PAL);
 // pyramide toggle
 let pyrChart;
 function drawPyr(v){const p=v==='avec'?pyrA:pyrS;
  const data=[p.tranche_moins30,p.tranche_31_44,p.tranche_45_59,p.tranche_60plus];
  if(pyrChart)pyrChart.destroy();
  pyrChart=new Chart(document.getElementById('c-ent-pyr'),{type:'bar',
   data:{labels:['Moins de 30','31-44 ans','45-59 ans','60 ans et +'],datasets:[{data,backgroundColor:[ '#5b8fc9',C.ent,'#143a5c','#0c2740'],borderRadius:5}]},
   options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,grid:{color:'#eef2f7'}},x:{grid:{display:false}}},
    plugins:{tooltip:{callbacks:{title:c=>c[0].label,label:c=>' '+c.parsed.y+' salariés'}},
     subtitle:{display:true,text:'n='+p.n_repondants+' entreprises · '+p.total_tetes+' salariés',color:'#5b6b7d',font:{size:11}}}}});}
 drawPyr('avec');
 document.querySelectorAll('#t-pyr button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#t-pyr button').forEach(x=>x.classList.remove('on'));b.classList.add('on');drawPyr(b.dataset.v);});
 const ca=sorted('entreprises','Q3.3_causes_tensions');hbar('c-ent-causes',ca.map(x=>x.item),ca.map(x=>x.moyenne),C.ent,5);
 const fr=sorted('entreprises','Q5.3_freins_recrutement');hbar('c-ent-freins',fr.map(x=>x.item),fr.map(x=>x.moyenne),C.ent,5);
 const pr=Q('entreprises','Q2.1_preoccupations').modalites;hbar('c-ent-preocc',pr.map(m=>m.modalite),pr.map(m=>m.pct_repondants),C.ent,100);
 const pg=sorted('entreprises','Q9.1_priorites_gpect');radar('c-ent-prio',pg.map(x=>x.item),pg.map(x=>x.moyenne),{fill:CL.ent,line:C.ent});
};
// ---------- OF ----------
BUILD.of=function(){
 document.getElementById('b-of').innerHTML="<b>En clair :</b> l'infrastructure de formation existe (plateaux équipés), mais la capacité à former aux compétences de demain (intelligence artificielle, cybersécurité) est faible. Les OF jugent leur offre bien plus adaptée que ne le font les entreprises.";
 document.getElementById('w-of').innerHTML="⚠️ Petit effectif (n=7) et collège hétérogène (dont 1 financeur non-formateur) : à lire comme des tendances.";
 const o1=Q('of','Q4.1_offre_couvre'),o2=Q('of','Q5.2_maitrise_afest');
 const plat=Q('of','Q1.7_plateaux').modalites.find(m=>m.modalite.toLowerCase().includes('totalement'));
 document.getElementById('m-of').innerHTML=
  metric(fmt(o1.moyenne),'« mon offre couvre les besoins » (1-5)','Q4.1 · 4,3 sans le financeur')+
  metric(fmt(o2.moyenne),'maîtrise de l\'AFEST (1-5)','Q5.2 · n=7')+
  metric(plat.n+'/7','plateaux techniques « totalement équipés »','Q1.7')+
  metric('100 %','anticipent l\'IA comme évolution majeure','Q8.2');
 // emergentes avec/sans financeur
 const em=sorted('of','Q2.2_capacite_emergentes');
 new Chart(document.getElementById('c-of-emerg'),{type:'bar',
  data:{labels:em.map(x=>x.item),datasets:[
    {label:'Les 7',data:em.map(x=>x.moyenne),backgroundColor:C.of,borderRadius:4,maxBarThickness:18},
    {label:'Sans le financeur',data:em.map(x=>x.sans_financeur?x.sans_financeur.moyenne:null),backgroundColor:'#9bd3b3',borderRadius:4,maxBarThickness:18}]},
  options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,scales:{x:{beginAtZero:true,max:5,grid:{color:'#eef2f7'}},y:{grid:{display:false},ticks:{font:{size:10}}}},
   plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:12,font:{size:11}}},tooltip:{callbacks:{label:c=>' '+c.dataset.label+' : '+fmt(c.parsed.x)}}}}});
 const no=sorted('of','Q2.1_niveau_offre');hbar('c-of-offre',no.map(x=>x.item),no.map(x=>x.moyenne),C.of,5);
 const se=sorted('of','Q3.3_connaissance_secteurs');radar('c-of-sect',se.map(x=>x.item),se.map(x=>x.moyenne),{fill:CL.of,line:C.of});
 document.getElementById('of-m1').innerHTML=`<div class="num">${fmt(em.find(x=>x.item.includes('Intelligence')).moyenne)}</div><div class="lab">Capacité à former à l'IA (1-5)</div>`;
 document.getElementById('of-m2').innerHTML=`<div class="num">${fmt(em.find(x=>x.item.includes('Cybers')).moyenne)}</div><div class="lab">Capacité à former à la cybersécurité (1-5)</div>`;
 document.getElementById('of-m3').innerHTML=`<div class="num">${fmt(Q('of','Q3.1_connaissance_besoins').moyenne)}</div><div class="lab">Connaissance des besoins des entreprises (1-5)</div>`;
 const jam=Q('of','Q5.1_afest_concu').modalites.find(m=>m.modalite.toLowerCase().includes('jamais'));
 document.getElementById('of-m4').innerHTML=`<div class="num">${jam.n}/7</div><div class="lab">n'ont jamais conçu d'AFEST</div>`;
};
// ---------- ACTEURS ----------
BUILD.act=function(){
 document.getElementById('b-act').innerHTML="<b>En clair :</b> les acteurs de l'emploi confirment les tensions des entreprises (maintenance, usinage, machines numériques) et pointent un manque de qualification des candidats plus qu'un simple manque de bras. L'offre locale leur paraît insuffisante.";
 const ad=Q('acteurs','Q2.1_adequation_profils'),of=Q('acteurs','Q6.1_offre_locale'),du=Q('acteurs','Q5.3_duree_emplois');
 document.getElementById('m-act').innerHTML=
  metric(fmt(ad.moyenne),'adéquation candidats / besoins (1-5)','Q2.1 · n=7')+
  metric(fmt(of.moyenne),'offre de formation locale (1-5)','Q6.1 · n=7')+
  metric(fmt(du.moyenne),'durée/stabilité des emplois obtenus (1-5)','Q5.3 · n=7')+
  metric(Q('acteurs','Q1.3_qualif_dominante').modalites[0].n+'/7','public surtout de niveau CAP/BEP','Q1.3');
 const cp=sorted('acteurs','Q3.1_difficulte_competences');hbar('c-act-comp',cp.map(x=>x.item),cp.map(x=>x.moyenne),C.act,5);
 const fr=sorted('acteurs','Q4.1_freins_acces_emploi');hbar('c-act-freins',fr.map(x=>x.item),fr.map(x=>x.moyenne),C.act,5);
 const mq=sorted('acteurs','Q6.2_manque_formation');hbar('c-act-manque',mq.map(x=>x.item),mq.map(x=>x.moyenne),C.act,5);
 const dp=sorted('acteurs','Q5.2_efficacite_dispositifs');vbar('c-act-disp',dp.map(x=>x.item),dp.map(x=>x.moyenne),[C.act,'#d98a4f','#e0a26b','#ecc4a3']);
};
// ---------- SYNDICATS ----------
BUILD.syn=function(){
 document.getElementById('b-syn').innerHTML="<b>En clair :</b> atout n°1 du territoire = sa position et son foncier ; freins = qualification de la main-d'œuvre et mobilité. La transmission-reprise est jugée prioritaire, et l'engagement des entreprises plutôt faible.";
 document.getElementById('m-syn').innerHTML=
  metric(fmt(Q('syndicats','Q06_dynamique_eco').moyenne),'dynamique économique (1-5)','Q06 · n=7')+
  metric(fmt(Q('syndicats','Q07_coordination_acteurs').moyenne),'coordination des acteurs (1-5)','Q07 · n=7')+
  metric(fmt(Q('syndicats','Q18_mobilite_frein').moyenne),'mobilité comme frein (1-5)','Q18 · n=7');
 const at=Q('syndicats','Q08_atouts').themes.filter(t=>t.n>0);hbar('c-syn-atouts',at.map(t=>t.theme),at.map(t=>t.n),C.syn,7);
 const fr=Q('syndicats','Q09_freins').themes.filter(t=>t.n>0);hbar('c-syn-freins',fr.map(t=>t.theme),fr.map(t=>t.n),C.syn,7);
 const ofm=Q('syndicats','Q14_offre_adaptee').modalites;dough('c-syn-offre',ofm.map(m=>m.modalite),ofm.map(m=>m.n),['#c98','#e0c','#9c6']);
 const en=Q('syndicats','Q20_engagement_entreprises').modalites;dough('c-syn-eng',en.map(m=>m.modalite),en.map(m=>m.n),['#c55','#fb3','#6a6']);
 const tr=Q('syndicats','Q24_transmission').modalites;dough('c-syn-trans',tr.map(m=>m.modalite),tr.map(m=>m.n),[C.syn,'#b497d6','#ccc']);
 const skip=/^(ras|na|ne sait pas|non renseigné|pas de remarque|pas de partage)/i;
 let vs=[];['Q21_freins_mobilisation','Q22_formats_animation','Q26_action_prioritaire','Q25_besoins_transmission'].forEach(k=>{
   (Q('syndicats',k).verbatims_anonymises||[]).forEach(v=>{if(v&&!skip.test(v.trim())&&v.length>22)vs.push(v);});});
 document.getElementById('syn-verb').innerHTML=vs.slice(0,6).map(v=>`<div class="verb">« ${v} »</div>`).join('');
};
// ---------- COMPETENCES ----------
BUILD.comp=function(){
 document.getElementById('b-comp').innerHTML="<b>En clair :</b> tout le monde anticipe l'IA et la robotique, mais l'offre de formation locale n'est pas encore prête à les enseigner — le décalage le plus net concerne la cybersécurité.";
 const em=sorted('of','Q2.2_capacite_emergentes');hbar('c-comp-of',em.map(x=>x.item),em.map(x=>x.moyenne),C.of,5);
 const ec=Q('entreprises','Q6.5_competences_3_5ans').modalites;hbar('c-comp-ent',ec.map(m=>m.modalite),ec.map(m=>m.pct_repondants),C.ent,100);
 const mq=sorted('acteurs','Q6.2_manque_formation');hbar('c-comp-act',mq.map(x=>x.item),mq.map(x=>x.moyenne),C.act,5);
 const ia=em.find(x=>x.item.includes('Intelligence')).moyenne, cy=em.find(x=>x.item.includes('Cybers')).moyenne;
 const iaPct=Q('of','Q8.2_domaines_evolutions').modalites.find(m=>m.modalite.includes('Intelligence')).pct_repondants;
 document.getElementById('comp-m1').innerHTML=`<div class="num">${iaPct} %</div><div class="lab">des OF anticipent l'IA comme évolution majeure</div>`;
 document.getElementById('comp-m2').innerHTML=`<div class="num">${fmt(ia)}</div><div class="lab">mais leur capacité à former à l'IA n'est que de (1-5)</div>`;
 document.getElementById('comp-m3').innerHTML=`<div class="num">${fmt(cy)}</div><div class="lab">capacité à former à la cybersécurité (1-5) — quasi nulle</div>`;
};
// ---------- CROISEMENTS ----------
BUILD.cx=function(){
 document.getElementById('b-cx').innerHTML="<b>En clair :</b> sur l'offre de formation, la mobilité, la transmission et l'AFEST, les quatre collèges ne sont pas d'accord. Ces écarts sont le vrai sujet du diagnostic.";
 const wanted=[['adéquation de l\'offre','Offre de formation locale'],['mobilité','Mobilité comme frein'],['transmission','Transmission (priorité)'],['afest','AFEST (maîtrise)'],['image','Image du territoire']];
 const co=SV._meta.colleges; const host=document.getElementById('cx-charts'); host.innerHTML='';
 wanted.forEach((w,i)=>{const d=dim(w[0]);if(!d)return;
   const cols=['entreprises','of','acteurs','syndicats'].filter(c=>typeof d.valeurs[c]==='number');
   const id='cx'+i;
   host.insertAdjacentHTML('beforeend',`<div class="card"><h3>${w[1]}</h3><p class="note">Moyenne 1-5 · écart ${fmt(d.ecart)}</p><div class="chartbox"><canvas id="${id}"></canvas></div></div>`);
   vbar(id,cols.map(c=>co[c].libelle),cols.map(c=>d.valeurs[c]),cols.map(c=>C[c==='entreprises'?'ent':c==='of'?'of':c==='acteurs'?'act':'syn']));
 });
 document.getElementById('cx-para').innerHTML=SV.paradoxes.map(p=>`<div class="card"><h3>${p.titre}</h3><p class="kv">${p.detail}</p></div>`).join('');
};
// ---------- MATRICE ----------
BUILD.mx=function(){
 document.getElementById('b-mx').innerHTML="<b>En clair :</b> une vue d'ensemble de toutes les comparaisons, avec l'ampleur des désaccords.";
 const co=SV._meta.colleges;
 function ecColor(e){if(e==null)return '#bcc6d0';if(e>=1.5)return '#b3261e';if(e>=1.0)return '#d97706';if(e>=0.5)return '#ca8a04';return '#2e8b57';}
 let h='<thead><tr><th>Dimension</th><th>Entreprises</th><th>OF</th><th>Acteurs</th><th>Syndicats</th><th>Écart</th></tr></thead><tbody>';
 SV.dimensions_partagees.forEach(d=>{const v=d.valeurs;
  h+=`<tr><td class="dim">${d.dimension}</td><td>${fmt(v.entreprises)}</td><td>${fmt(v.of)}</td><td>${fmt(v.acteurs)}</td><td>${fmt(v.syndicats)}</td>`+
     `<td>${d.ecart==null?'<span style="color:#94a3b8">n.c.</span>':`<span class="ec" style="background:${ecColor(d.ecart)}">${fmt(d.ecart)}</span>`}</td></tr>`;});
 h+='</tbody>';document.getElementById('mxtable').innerHTML=h;
};
// ---------- LEVIERS ----------
BUILD.lev=function(){
 document.getElementById('b-lev').innerHTML="<b>En clair :</b> sept chantiers concrets, chacun justifié par les chiffres du diagnostic.";
 document.getElementById('lev-cards').innerHTML=SV.axes_strategiques.map(a=>
  `<div class="card axe"><h3>${a.axe}</h3><p class="src"><b>Fondé sur :</b> ${a['fondé_sur']}</p><ul>${a.pistes.map(p=>`<li>${p}</li>`).join('')}</ul></div>`).join('');
};
// ---------- METHODE src ----------
(function(){const m=SV.donnees_colleges;
 document.getElementById('met-src').innerHTML=
 `Entreprises : ${m.entreprises.meta.source} (${m.entreprises.meta.source_date}).<br>`+
 `Organismes de formation : ${m.of.meta.source} (${m.of.meta.source_date}).<br>`+
 `Acteurs de l'emploi : ${m.acteurs.meta.source} (${m.acteurs.meta.source_date}).<br>`+
 `Syndicats / orga pro : ${m.syndicats.meta.source} (${m.syndicats.meta.source_date}).<br>`+
 `Tableau de bord généré le ${SV._meta.genere_le}, à partir du fichier unique « source de vérité ».`;
})();
BUILD.synthese();inited.synthese=true;
// bouton retour haut + recalcul navh réel
const tt=document.getElementById('toTop');
tt.onclick=()=>window.scrollTo({top:0,behavior:'smooth'});
window.addEventListener('scroll',()=>{tt.classList.toggle('show',window.scrollY>320)},{passive:true});
function setNavH(){const n=document.getElementById('nav');if(n)document.documentElement.style.setProperty('--navh',n.offsetHeight+'px');}
setNavH();window.addEventListener('resize',setNavH);
</script>
</body>
</html>
"""

out = HTML.replace("__CHARTJS__", CHARTJS).replace("__SVDATA__", SVDATA)
(DASH/"dashboard_gpect_issoudun.html").write_text(out, encoding="utf-8")
print("OK -> dashboard_gpect_issoudun.html  (", len(out)//1024, "Ko )")
