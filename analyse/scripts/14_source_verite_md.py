#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Version lisible de source_verite.json (lecture seule)."""
import json
RES="/home/user/Gpect/analyse/resultats/"
SV=json.load(open(RES+"source_verite.json",encoding="utf-8"))
L=[]; w=L.append
m=SV["_meta"]
w("# GPECT Issoudun — SOURCE DE VÉRITÉ (analyse territoriale croisée)\n")
w(f"*Généré {m['genere_le']} · {m['regle']}*\n")
c=m["colleges"]
w(f"**Périmètre : {m['total_repondants']} répondants** — Entreprises {c['entreprises']['n']} · OF {c['of']['n']} · Acteurs emploi {c['acteurs']['n']} · Syndicats {c['syndicats']['n']}.")
w(f"\n> ⚠️ {m['avertissement']}\n")

w("## 1-2. Dictionnaire des questions partagées & écarts de perception\n")
w("*Échelles 1-5 sauf mention. « — » = question non posée à ce collège (voir `detail` pour les indicateurs catégoriels).*\n")
w("| Dimension | Entreprises | OF | Acteurs | Syndicats | Écart |")
w("|---|:--:|:--:|:--:|:--:|:--:|")
def cell(v): return "—" if v is None else (str(v) if not isinstance(v,bool) else v)
for d in SV["dimensions_partagees"]:
    val=d["valeurs"]
    w(f"| {d['dimension']} | {cell(val.get('entreprises'))} | {cell(val.get('of'))} | {cell(val.get('acteurs'))} | {cell(val.get('syndicats'))} | {cell(d.get('ecart'))} |")
w("\n### Détail & lecture par dimension\n")
for d in SV["dimensions_partagees"]:
    w(f"**{d['dimension']}** — *{d['echelle']}*  ")
    w(f"Lecture : {d['lecture']}  ")
    det=" ; ".join(f"{k} = {v}" for k,v in d.get("detail",{}).items())
    if det: w(f"Détails sourcés : {det}  ")
    w(f"Sources : {d.get('sources')}\n")

w("\n## 3. Convergences (accord des collèges)\n")
for x in SV["convergences"]: w(f"- {x}")
w("\n## 4. Angles morts & paradoxes\n")
for p in SV["paradoxes"]: w(f"- **{p['titre']}** — {p['detail']}")
w("\n## 5. Corrélations / hypothèses à vérifier\n")
for h in SV["hypotheses_a_verifier"]: w(f"- {h}")
w("\n## 6. Axes stratégiques (sourcés)\n")
for a in SV["axes_strategiques"]:
    w(f"- **{a['axe']}** — *fondé sur :* {a['fondé_sur']}")
    for p in a["pistes"]: w(f"    - piste : {p}")
w("\n## 7. Données complètes par collège\n")
w("Le fichier `source_verite.json` embarque l'intégralité des indicateurs des 4 collèges "
  "(clé `donnees_colleges`) — **c'est l'unique source du dashboard**.")
open(RES+"source_verite.md","w",encoding="utf-8").write("\n".join(L))
print("OK -> source_verite.md (",len(L),"lignes )")
