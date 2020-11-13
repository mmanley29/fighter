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
        folder = os.path.dirname(os.path.abspath(__file__)) + "\pictures\\"
        arcade.start_render()
        self.background = arcade.load_texture((folder + 'background_image.jpg'))
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
        folder = os.path.dirname(os.path.abspath(__file__)) + "\pictures\\"
        self.player_sprite = arcade.Sprite((folder + 'red_square,jpg'), 0.5)
        self.physics_engine = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        #Spatial hashing speeds the time it takes to find collisions, but increases the time it takes to move a sprite.
        #use_spatial_hash is set to false by default
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
        folder = os.path.dirname(os.path.abspath(__file__)) + "\pictures\\"
        for x in range(0, 1500, 32):
            wall = arcade.Sprite(folder + 'wall.jpg')
            wall.center_x = x
            wall.center_y = 50
            self.wall_list.append(wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()

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
        #arcade.check_for_collision_with_list()
        #arcade.check_for_collision()
        #We can use one of these to help with the collions between players


if __name__ == "__main__":
    '''
    view = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = Menu_view()
    view.show_view(menu_view)
    '''
    mygame = MyGame()
    mygame.setup()
    arcade.run()