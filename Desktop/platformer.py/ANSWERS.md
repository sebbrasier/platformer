Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?

Pour la lecture du fichier, nous avons créé une fonction "def char_to_sprite" qui lit chaque caractère de map1 pour retourner ce qu'elle représente.Puis nous avons créé une fonction "sprite_type" qui place les monstres sur la carte en fonction de ce qui a été lu dans le fichier. Enfin il y a la double boucle for qui appelle chaque fonction au bon moment.

Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

non il faudrai faire des test qui prennent en compte la map tel que l'on nous la donne et pas des tests prédéfinis

Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse.
Le code qui gère la lave ressemble beacoup plus à celui des blobs car il fait perdre la partie au joueur. Deplus, c'est un bloc transparent, donc on peut le traverser ce qui est le contraire des propriétés des blocs "wall" comme l'herbe. Il ressemble aussi à celui des pièces car le code se déclenche lors de la collision entre les 2.

Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?

Pour cela nous avons créé la fonction blob_collision qui detecte quand le bloc est soit en collision avec de l'air, un obstacle ou de la lave et la fonction blob_position fait changer la direction si cette fonction renvoit True en multipliant la vitesse du blob par -1.

