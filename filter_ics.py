import urllib.request
import sys

# Ton lien Google Drive direct
URL_SOURCE = "https://drive.google.com/uc?export=download&id=14WWkythOj_TWrM3lvDlJ6XZN_-tdh0-5"
FICHIER_SORTIE = "edt_propre.ics"
MOT_CLE_FILTRE = "[GB]"

try:
    # On masque le user-agent pour éviter le blocage par l'anti-bot de Google
    req = urllib.request.Request(URL_SOURCE, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        # Google Drive renvoie le fichier directement via les redirections internes
        lignes = response.read().decode('utf-8').splitlines()
except Exception as e:
    print(f"Erreur de téléchargement du flux source GDrive : {e}")
    sys.exit(1)

lignes_filtrees = []
bloc_en_cours = []
dans_vevent = False
a_supprimer = False

for ligne in lignes:
    if ligne.startswith("BEGIN:VEVENT"):
        dans_vevent = True
        bloc_en_cours.append(ligne)
        continue
    
    if dans_vevent:
        bloc_en_cours.append(ligne)
        if MOT_CLE_FILTRE in ligne:
            a_supprimer = True
            
        if ligne.startswith("END:VEVENT"):
            if not a_supprimer:
                lignes_filtrees.extend(bloc_en_cours)
            dans_vevent = False
            bloc_en_cours = []
            a_supprimer = False
    else:
        lignes_filtrees.append(ligne)

with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
    for ligne in lignes_filtrees:
        f.write(ligne + "\n")

print(f"Filtrage terminé avec succès. Fichier {FICHIER_SORTIE} généré.")