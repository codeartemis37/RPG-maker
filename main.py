import json

class Sortie:
    def __init__(self, texte, id_sortie):
        self.texte = texte
        self.id_sortie = id_sortie

class Scene:
    def __init__(self, id_scene, texte, sorties):
        self.id_scene = id_scene  # C'est un entier maintenant
        self.texte = texte
        self.sorties = sorties

class Jeu:
    def __init__(self, fichier_json):
        self.scenes = {}
        self.charger_scenes(fichier_json)

    def charger_scenes(self, fichier_json):
        with open(fichier_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for scene_data in data:
            sorties = [Sortie(s['texte'], s['id_sortie']) for s in scene_data['sorties']]
            scene = Scene(scene_data['id'], scene_data['texte'], sorties)
            self.scenes[scene.id_scene] = scene

    def jouer(self, id_scene_depart):
        id_scene_courante = id_scene_depart
        while True:
            scene = self.scenes.get(id_scene_courante)
            if not scene:
                print("Scène introuvable.")
                break
            print("\n" + scene.texte)
            if not scene.sorties:
                print("Fin du jeu.")
                break
            for idx, sortie in enumerate(scene.sorties):
                print(f"{idx+1}. {sortie.texte}")
            choix = input("Choisissez une option: ")
            try:
                choix_int = int(choix) - 1
                id_scene_courante = scene.sorties[choix_int].id_sortie
            except (ValueError, IndexError):
                print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    jeu = Jeu("scenes.json")  # Mets le nom de ton fichier JSON
    jeu.jouer(1)              # L'id de départ est maintenant un entier
