Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

Pour la lecture du fichier, nous avons créé une fonction "def char_to_sprite" qui lit chaque caractère de map1 pour retourner ce qu'elle représente.Puis nous avons créé une fonction "sprite_type" qui place les monstres sur la carte en fonction de ce qui a été lu dans le fichier. Enfin il y a la double boucle for qui appelle chaque fonction au bon moment.

Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

non il faudrai faire des test qui prennent en compte la map tel que l'on nous la donne et pas des tests prédéfinis

Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse.
Le code qui gère la lave ressemble beacoup plus à celui des blobs car il fait perdre la partie au joueur. Deplus, c'est un bloc transparent, donc on peut le traverser ce qui est le contraire des propriétés des blocs "wall" comme l'herbe. Il ressemble aussi à celui des pièces car le code se déclenche lors de la collision entre les 2.

Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?

Pour cela nous avons créé la fonction blob_collision qui detecte quand le bloc est soit en collision avec de l'air, un obstacle ou de la lave et la fonction blob_position fait changer la direction si cette fonction renvoit True en multipliant la vitesse du blob par -1.

### semaine 4

Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?
On a créé la fonction update_sword_orientation pour l'orientation de l'épée où l'orientation de l'épée est déterminée par l'angle entre le joueur et la souris. La formule utilisée est math.atan2(ref_x - world_x, ref_y - world_y), où : ref_x, ref_y sont les coordonnées du joueur et world_x, world_y sont les coordonnées de la souris dans le monde, calculées à partir des coordonnées de l'écran et de la caméra.
On utilise ces formules pour obtenir les coordonnées de la souris dans le monde : world_x = mouse_x + self.camera.position[0] - (self.WINDOW_WIDTH / 2) et world_y = mouse_y + self.camera.position[1] - (self.WINDOW_HEIGHT / 2).

Comment testez-vous l’épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?
On teste qu'elle apparait 

Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?
Le score est stocké dans score qui se réinitialise seulement lors d'un game over.

Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?
On le remet à 0 lors d'un game over. Pour ne pas avoir de code dupliqué nous avons créé une fonction game_over.

Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?
Quand la joueuse atteint le point E, on ajoute 1 a All.map.index grace a la fonction check_for_next_level

Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?
Pour l'instant si cela se passe le jeu crash.

### semaine 5

Quelles formules utilisez-vous exactement pour l’arc et les flèches ?
Pour l'orientation de l'arc nous utilisons la meme methode que pour l'épée qui est défini dans la class Parents.
Pour les flèches, on transforme premièrment l'angle d'orientation en radian, puis on créée un vecteur avec comme coordonnées 25*cos(angle) et 25*sin(-angle) que on va ensuite additionner à la vitesse de la flèche pour qu'on puisse la tirer.

Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?

Pour le déplacement des chauves souris, nous avons défini un carré défini par bundary, qui nous sert de barrière imaginaire. La chauve souris change de direction a 180 degré quand elle touche une paroi. Pour les changements de direction entre les parois nous utilisons random.gauss pour calculer la variation d'angle avec une moyenne de 60 et un écart type tres faible de pi/90 pour que les changements soit fluides et pas brutales. Les changements de direction se produisent seulement si random est inferieur à 0.01 pour que ca soit assez réaliste.

Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?
Nous avons premierement mis pass a la méthode parent update_weapon_position pour que la fleche ne soit pas toujours collé au joueur. Puis nous avonbs créé une nouvel méthode shoot dans la class Enfant Arrow qui calcul un vecteur, puis additionne ce vecteur à la position pour que la flèche aille dans la bonne direction.

Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d’armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?

Pour gérer le fait que l'on a maintenant 2 types de monstres et 2 types d'armes nous avons donc créé des classes hérité avec comme classes parents une class monstre et une class arme pour ensuite pouvoir avoir des class enfants et y mettre nos différents monstres et armes. Nous avons aussi du créer 2 listes (blob_Table et chauve_souris_TABLE pour pouvoir anger les instances de ces monstres séparement)

### semaine 9
Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?
Pour identifier les blocs, on utilise un algorithme recursif: si on bloc est a proximité d'une série de flèches on vérifie si les 4 blocs autour (en haut, bas, à droit et à gauche) peuvent bien être rajoutés en tant que platforme puis les rajoutent dans un set si c'est le cas. L'entiéreté de la platforme sera maintenant un frozenset qui sera associé à la longuer de la chaine de flèches dans un dictionnaire. Le déplacement est ensuite facilement calculé grace à la longueur des chaines de flèches

Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?
L'algorithme travaille sur des matrices et utilise des frozensets et des dictionnaires
Avantages : Cela permet de réellement séparer chaque étape du procéssus de recognisation et calcul des platformes, on travaille sur des matrices, frozensets et dictionnaires, ce qui simplifie grandement la tache et qui profite du hash (nottament recherche en teta(1)), 
Désavantages : L'algorithme qui reconnait les platformes est assez couteux (même si raisonnable dans le cadre du projet), et on est obligés d'imbriquer beacoup de fonctions pour traiter tous les cas (platformes qui se déplacent en haut et en bas), ce qui n'améliore pas les performances.


