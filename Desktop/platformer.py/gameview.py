import arcade

class GameView(arcade.View):

    player_sprite : arcade.Sprite
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    wall_list : arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    camera: arcade.camera.Camera2D
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
   
    """Lateral speed of the player, in pixels per frame."""
    

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE


        # Setup our game
        self.setup()
    


    def setup(self) -> None:
        """Set up the game here."""
        PLAYER_GRAVITY = 1
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=64,
            center_y=128
        )
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        for i in range(20):
            wall_sprite = arcade.Sprite(":resources:images/tiles/grassMid.png",
                center_x = (64*i),
                center_y=32, 
                scale = 0.5
            )
            self.wall_list.append(wall_sprite)
        for i in range(1,4):
            box_sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                center_x = (128 + 256*i),
                center_y=96, 
                scale = 0.5
            )
            self.wall_list.append(box_sprite)
        for i in range(1, 5):
            coin_sprite = arcade.Sprite(":resources:images/items/coinGold.png",
                center_x = (256*i),
                center_y=96, 
                scale = 0.5
            )
            self.coin_list.append(coin_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls = self.wall_list,
            gravity_constant=PLAYER_GRAVITY,
        )
        self.camera = arcade.camera.Camera2D()

        # initialisation des variables pour le son 

        self.coin_sound = arcade.load_sound(":resources:/sounds/coin4.wav")
        self.jump_sound = arcade.load_sound(":resources:/sounds/jump3.wav")


    key_right : bool = False
    key_left : bool = False

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        PLAYER_MOVEMENT_SPEED = 5
        PLAYER_JUMP_SPEED = 18
        
        if key == arcade.key.RIGHT:
                # start moving to the right
                self.player_sprite.change_x = + PLAYER_MOVEMENT_SPEED
                self.key_right = True
    
        if key == arcade.key.LEFT:
                # start moving to the left
                self.player_sprite.change_x = - PLAYER_MOVEMENT_SPEED
                self.key_left = True

        if key == arcade.key.UP and self.physics_engine.can_jump(): 
                # start moving to the left
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        if key == arcade.key.ESCAPE:
                self.setup()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        if key == arcade.key.RIGHT:
            self.key_right = False
        if key == arcade.key.LEFT:
            self.key_left = False
        if (key == arcade.key.RIGHT or key == arcade.key.LEFT) and (self.key_right == False and self.key_left == False):
            #stop later mouvement
            self.player_sprite.change_x = 0
  


    def on_draw(self) -> None:
        """Render the screen"""
        self.clear()
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()


    #fonction de control de camera
    def cam_control(self) -> None:
         player_x = self.player_sprite.center_x
         player_y = self.player_sprite.center_y
         #Calcule des "Bords" de la caméra:
         right_edge = self.camera.position[0] + (self.WINDOW_WIDTH // 2) - 410
         left_edge = self.camera.position[0] - (self.WINDOW_WIDTH // 2) + 410
         upper_edge = self.camera.position[1] + (self.WINDOW_HEIGHT // 2) - 300
         down_edge = self.camera.position[1] - (self.WINDOW_HEIGHT // 2) + 250

         if player_x >= right_edge:
              self.camera.position = (self.camera.position[0] + abs(player_x - right_edge) , self.camera.position[1]) #type ignore
         if player_x <= left_edge:
              self.camera.position = (self.camera.position[0]  - abs(player_x - left_edge) , self.camera.position[1]) #type ignore
         if player_y >= upper_edge:
              self.camera.position = (self.camera.position[0], self.camera.position[1] + abs(player_y - upper_edge))#type ignore
         if player_y <= down_edge:
              self.camera.position = (self.camera.position[0], self.camera.position[1] - abs(player_y - down_edge))#type ignore



    """Main in-game view."""
    def on_update(self, delta_time: float) -> None:
        self.player_sprite.center_x += self.player_sprite.change_x
        self.physics_engine.update()

        self.cam_control()


        coin_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.coin_sound)
        
        



