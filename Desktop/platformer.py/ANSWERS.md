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


Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?
Le score est stocké dans score qui se réinitialise seulement lors d'un game over.

Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?
On le remet à 0 lors d'un game over. Pour ne pas avoir de code dupliqué nous avons créé une fonction game_over.

Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?
Quand la joueuse atteint le point E, on ajoute 1 a All.map.index grace a la fonction check_for_next_level

Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?
Pour l'instant si cela se passe le jeu crash.


