import json
import os

SAVE_FILE = "save.json"
SCENES_FILE = "scenes.json"

def charger_sauvegarde():
    if not os.path.exists(SAVE_FILE):
        data = {
            "log": [],
            "inventaire": [],
            "scene_actuelle": "village"
        }
        sauvegarder(data)
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def charger_scenes():
    with open(SCENES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def afficher_scene(scene, sauvegarde):
    print(f"\n== {scene['titre']} ==")
    print(scene["description"])
    if scene.get("objet"):
        print(f"Vous voyez ici : {scene['objet']}")
    print("Actions possibles :")
    for i, option in enumerate(scene["options"], 1):
        print(f"{i}. {option['texte']}")
    print("0. Sauvegarder et quitter")

def main():
    scenes = charger_scenes()
    sauvegarde = charger_sauvegarde()
    
    while True:
        id_scene = sauvegarde["scene_actuelle"]
        scene = scenes[id_scene]
        afficher_scene(scene, sauvegarde)

        choix = input("Votre choix : ")
        if choix == "0":
            print("Sauvegarde...")
            sauvegarder(sauvegarde)
            print("Au revoir !")
            break

        try:
            idx = int(choix) - 1
            if 0 <= idx < len(scene["options"]):
                action = scene["options"][idx]["action"]
                if action.startswith("aller_"):
                    sauvegarde["scene_actuelle"] = action.replace("aller_", "")
                    sauvegarde["log"].append(f"Aller vers {scenes[sauvegarde['scene_actuelle']]['titre']}")
                elif action.startswith("prendre_"):
                    objet = action.replace("prendre_", "")
                    if objet not in sauvegarde["inventaire"]:
                        sauvegarde["inventaire"].append(objet)
                        sauvegarde["log"].append(f"Pris {objet}")
                        print(f"Vous avez pris : {objet}")
                    else:
                        print("Vous avez déjà cet objet.")
                elif action == "parler_ancien":
                    print("L'ancien vous souhaite la bienvenue.")
                    sauvegarde["log"].append("A parlé à l'ancien")
                else:
                    print("Action inconnue.")
            else:
                print("Choix invalide.")
        except ValueError:
            print("Entrez le numéro d'une action.")

if __name__ == "__main__":
    main()
