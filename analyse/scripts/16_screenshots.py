#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planche de contrôle : capture chaque page du dashboard."""
import glob, os
from playwright.sync_api import sync_playwright
DASH="/home/user/Gpect/analyse/dashboard"
HTML="file://"+DASH+"/dashboard_gpect_issoudun.html"
SHOTS=DASH+"/captures"; os.makedirs(SHOTS,exist_ok=True)
pages=[("synthese","1_synthese"),("ent","2_entreprises"),("of","3_organismes_formation"),
       ("act","4_acteurs_emploi"),("syn","5_syndicats"),("comp","6_competences_ia"),
       ("cx","7_croisements"),("mx","8_matrice"),("lev","9_leviers"),("met","10_methode")]
# trouver le binaire chromium
cands=glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")+glob.glob("/opt/pw-browsers/chromium/chrome-linux/chrome")
exe=cands[0] if cands else None
print("chromium:",exe)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe,args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":1280,"height":900},device_scale_factor=2)
    pg.goto(HTML,wait_until="networkidle")
    for tab,name in pages:
        pg.evaluate(f"show('{tab}')")
        pg.wait_for_timeout(900)
        path=f"{SHOTS}/{name}.png"
        pg.screenshot(path=path,full_page=True)
        print("ok",name)
    b.close()
print("captures ->",SHOTS)
