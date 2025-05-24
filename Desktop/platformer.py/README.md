# 2D Mario Python Game

## Description

Mario Python Game est un projet de jeu de plateforme en 2D inspiré de Super Mario, développé en Python avec la bibliothèque Arcade. Le joueur, muni d'un arc et d'une épée, a pour objectif de traverser plusieurs cartes avec des ennemis et des obstacles differents.

## Fonctionnalités
- 🔹 **Plusieurs maps** : différents niveaux avec des fonctionnalités differentes
- 🔹 **Ennemis** : Blobs et chauves-souris, le joueur meurt si il les touche, et peut les éliminer avec ses armes
                    - Les blobs se déplacent de gauche à droite sans cesse et font demi tour quand il rencontrent un obstacle ou le vide.
                    - Les chauves souris volent dans un carré et se déplacent dedans de façon aléatoire. Elles peuvent traverser les obstacles.
- 🔹 **Zones** : dans certains niveaux, il y a des zones qui inversent la gravité et d'autre qui empêchent l'utilisation d'arme.
                 Un icône apparait quand on entre dedans.
- 🔹 **Interupteur/Portail** : Des leviers sont positionnés sur certaines maps, qui peuvent ouvrir/fermer un ou plusieurs       portails quand ils sont actionnés par une épée ou une flèche.Certains ont des fonctionnalité particulière comme le fait de fonctionner qu'une fois.
- 🔹 **Lave** : Le joueur meurt à son contact
- 🔹 **Plateformes mouvantes** : certaines plateformes se déplacent de haut en bas ou de gauche à droite
- 🔹 **Plateformes qui se cassent** : certaines plateformes (Rondins) se cassent au contact du joueur et réaparaissent quelque temps après

**Controle**

| Touche           | Action          |
| ---------------- | --------------- |
| Flèche gauche    | Aller à gauche  |
| Flèche droite    | Aller à droite  |
| Flèche haut      | Sauter          |
| ESC              | restart niveau  |
| clic gauche      | attaquer        |
| clic droit       | Changer d'arme  |


**MAP**

## Lecture de la carte

Chaque niveau est défini par un fichier map de largeur `width` et hauteur `height`. Chaque caractère représente une tuile ou un objet du jeu :

| Symbole | Signification                                                      |
| ------- | ------------------------------------------------------------------ |
| `=`     | Bloc de terre                                                      |
| `-`     | Demi-bloc de gazon                                                 |
| `£`     | Lave                                                               |
| `v`     | Chauve-souris                                                      |
| `o`     | Blob                                                               |
| `*`     | Pièce à collecter                                                  |
| `↑`     | Flèche indiquant que la plateforme reliée bouge dans ce sens       |
| `x`     | Caisse                                                             |
| `S`     | Point de spawn du joueur                                           |
| `E`     | Panneau pour aller au niveau suivant                               |
| `|`     | Portail s'ouvre ou se ferme avec un interupteur                    |
| `b`     | Rondin qui se casse sous le joueur                                 |


