import json
import os
import subprocess
import keyboard

# Charger les raccourcis depuis le fichier JSON
with open('raccourcis.json', 'r') as file:
    data = json.load(file)

raccourcis = data.get("raccourcis", [])

def executer_script(path):
    if not os.path.exists(path):
        print(f"[ERREUR] Le fichier n'existe pas : {path}")
        return

    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == '.bat' or ext == '.exe':
            subprocess.Popen([path], shell=True)
        elif ext == '.ps1':
            subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", path], shell=True)
        elif ext == '.py':
            subprocess.Popen(["python", path], shell=True)
        else:
            print(f"[ERREUR] Extension non supportée : {ext}")
            return

        print(f"[INFO] Exécution de : {path}")

    except Exception as e:
        print(f"[ERREUR] Impossible d'exécuter {path} : {e}")

# Associer les raccourcis clavier
for racc in raccourcis:
    if racc.get("systeme") == 0:
        combo = racc.get("raccourci")
        path = racc.get("path")
        name = racc.get("name")

        if combo and path:
            keyboard.add_hotkey(combo, executer_script, args=(path,))
            print(f"[OK] Raccourci '{combo}' associé à : {name}")

print("[INFO] Le script est en attente des raccourcis... (CTRL+C pour quitter)")
keyboard.wait()  # Le script tourne en continu
