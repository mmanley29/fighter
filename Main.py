import arcade
import os.path

WIDTH = 1500
HEIGHT = 750
MOVEMENT_SPEED = 5
GRAVITY = 1
JUMP_SPEED = 30
TITLE = 'Test Window'

class Menu_view(arcade.View):
    def on_show(self):
        pass
    def on_draw(self):
        directory = os.path.dirname(__file__) #Bro Manley
        filepath = directory + '/pictures/background_image.jpg'#Bro Manley
        #folder = os.path.dirname(os.path.abspath(__file__)) + "\pictures\\"
        arcade.start_render()
        self.background = arcade.load_texture(filepath)
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        arcade.draw_text('Menu Screen', WIDTH/2, HEIGHT/2, arcade.color.WHITE, font_size = 50, anchor_x='center')
        arcade.draw_text('Click to Advance', WIDTH/2, HEIGHT/2 - 75, arcade.color.WHITE, font_size=50, anchor_x='center')
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        window = MyGame()
        window.setup()
        #instructions_view = Instructions_view()
        #self.window.show_view(instructions_view)
        
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        directory = os.path.dirname(__file__) #Bro Manley
        filepath = directory + '/pictures/red_square.jpg'
        #filepath = os.path.join(directory, "/pictures", 'red_square.jpg') #Bro Manley
        #folder = os.path.dirname(os.path.abspath(__file__)) + "\pictures\\"
        self.player_sprite = arcade.Sprite(filepath, 0.5) #Bro Manley
        self.physics_engine = None
        self.total_time = 0.0 # to add time

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        #Spatial hashing speeds the time it takes to find collisions, but increases the time it takes to move a sprite.
        #use_spatial_hash is set to false by default
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
        directory = os.path.dirname(__file__) #Bro Manley
        filepath = directory + '/pictures/wall.jpg' #Bro Manley
        #folder = os.path.dirname(os.path.abspath(__file__)) + "\pictures\\"
        for x in range(0, 1500, 32):
            wall = arcade.Sprite(filepath)
            wall.center_x = x
            wall.center_y = 50
            self.wall_list.append(wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        self.total_time = 0.0 # to add time

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out time output
        output = (f"Time: {minutes:02d}:{seconds:02d}")

        # Output the timer text.
        arcade.draw_text(output, 300, 300, arcade.color.RED, 30)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        #colision check for player
        if self.player_sprite.center_x  > 1500 - 100:
            self.player_sprite.center_x += -5
        elif self.player_sprite.center_x < 0 + 30:
            self.player_sprite.center_x += 5
        
        self.total_time += delta_time
        #arcade.check_for_collision_with_list()
        #arcade.check_for_collision()
        #We can use one of these to help with the collions between players


if __name__ == "__main__":
    
    #view = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = Menu_view()
    #view.show_view(menu_view)
    
    mygame = MyGame()
    magame.show_view(menu_view)
    mygame.setup()
    arcade.run()