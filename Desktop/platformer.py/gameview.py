import arcade

class GameView(arcade.View):

    player_sprite : arcade.Sprite
    player_sprite_list : arcade.SpriteList[arcade.Sprite]
    wall_list : arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    camera: arcade.camera.Camera2D
    #Variables de Control de Camera
    y_min = 64
    y_max = 128
    x_min = 64
    x_max = 1200
   
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
            self.allow_movement = False


    def on_draw(self) -> None:
        """Render the screen"""
        self.clear()
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()


    """Main in-game view."""
    def on_update(self, delta_time: float) -> None:
        self.player_sprite.center_x += self.player_sprite.change_x
        self.physics_engine.update()

        self.camera.position = self.player_sprite.position # type: ignore

        coin_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit:
            coin.remove_from_sprite_lists()
        
        



