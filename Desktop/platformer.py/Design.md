Analyse performance :

Analyse des platformes:
Si n est la taille de la map (width * height = n):
L'ajout des platformes est un algorithme assez compliqué: un algorithme qui lit le fichier ligne par ligne (en O(n)) reconnait si un block est proche d'une flèche:
Si cette condition est vérifiée, un algorithme récursif en O(n) regarde le blocks autour pour configurer la platforme (Il est bien en O(n), les blocks
qui ont déja été vérfifiés sont gardés en mémoires et on ne les re-vérifie pas).
L'algorithme est appliqué qu'une fois par flèche, et donc qu'une fois par platforme. On a donc les deux algorithmes imbriqués qui sont en O(n) + O(n) = O(n)
Si une platforme possède deux flèches qui la touchent (disons flèche gauche et droite):
l'algorithme ci-dessus est appliqué deux fois et la platforme touchée est considérée comme deux platformes différentes, on combine ensuite ces platformes.
On utilise un algorithme de transposition de matrices qui est en O(n)
L'algorithme qui combine les platforme est un algorithme de recherche en O(k) ou k est la taille des platformes (En effet, on utilise l'intersection de set qui en O(2k)), considérons ici que c'est du O(n).
On rajoute ensuite les platformes dans les listes: complexité (O(n)).
Ainsi, grossièrement, l'algorithme mis bout à bout devrait "théoriquement" être en O(n), les fonctions imbriquées ne sont appelées qu'une seule fois par platforme.

Pour vérifier cela expérimentalement, nous avons utilisé des fichiers avec des platformes de taille 1-1000 affectées par deux flèches.
On a le tableau suivant:
1 : 5.667891702614725e-05
5 : 0.00021472687507048248
50 : 0.0024823399169836193
100 : 0.004888056499999948
500 : 0.024687768124975265
1000 : 0.04772602575004566

La complexité est effectivement linéaire, cela est en accord avec l'analyse théorique, mais cela est quand même surprenant, en considérant la 
quantité de fonctions imbriquées.

Analyse des ennemis:
Soit n le nombre d'ennemis.
On a plusieurs algorithmes indépendants:
collision entre ennemi et joueur: Regarde si check_for_collision_with_list est vide, cet algorithme est en O(n) selon la documentation d'arcade.
Pour le dépacement des blobs, on regarde les collisions avec des sprite lists de lave ou murs et selon si ces listes sont vides ou non, la vitesse est inversée.
La complexité est donc également en O(n) (La complexité pourrait être améliorée en calculant la trajectoire dans le setup, mais le déplacement n'avait pas un gros effet sur
les performances lors du profiling).
Pour le déplacement des chauves-souris, le mouvement est conditionnel par rapport à sa position actuelle: changer son angle ou sa vitesse selon si elle touche les bords
de la boite. La complexité est en O(1)
Nous pouvons en conclure que la complexité totale est de O(n) pour chaque on_update.

Expérimentalement, on trouve effectivement que la complexité est linéaire:
1 : 0.00018311333027668298
5 : 0.0002929641597438604
50 : 0.00107578165945597
100 : 0.0018912087508942933
500 : 0.00840582708013244
1000 : 0.016534584999317304
10000 : 0.1643470825010445


