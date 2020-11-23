#CURRENTLY DOES NOT WORK
import arcade
import os.path

WIDTH = 1500
HEIGHT = 750
MOVEMENT_SPEED = 5
GRAVITY = 1
JUMP_SPEED = 30
TITLE = 'Test Window'

class Menu_view(arcade.View):
    def on_draw(self):
        directory = os.path.dirname(__file__) #Bro Manley
        filepath = directory + '/pictures/background_image.jpg'#Bro Manley
        arcade.start_render()
        arcade.load_texture(filepath).draw_sized(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)
        arcade.draw_text('Menu Screen', WIDTH/2, HEIGHT/2, arcade.color.WHITE, font_size = 50, anchor_x='center')
        arcade.draw_text('Click to Advance', WIDTH/2, HEIGHT/2 - 75, arcade.color.WHITE, font_size=50, anchor_x='center')
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        mygame = MyGame()
        mygame.setup()
        self.window.show_view(mygame)
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.filepath = os.path.dirname(__file__) + '/pictures/'
        self.scale = 0.5
        self.textures = []
        texture = arcade.load_texture(self.filepath + 'red_square.jpg')
        self.textures.append(texture)
        texture = arcade.load_texture(self.filepath + 'red_square.jpg', flipped_horizontally=True)
        self.textures.append(texture)
        texture = arcade.load_texture(self.filepath + 'red_square_punch.png')
        self.textures.append(texture)
        self.texture = self.textures[0]
    
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x < 0:
            self.texture = self.textures[1]
            #moving left
        elif self.change_x > 0:
            self.texture = self.textures[0]
            #moving right
        elif key == arcade.key.J:
            self.texture = self.textures[2]


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        directory = os.path.dirname(__file__) # Load all directory path for image files.Choi
        self.background = None #variable used in draw function to show background image.Choi
        filepath = directory + '/pictures/'
        self.player_sprite = None
        #self.player_sprite = arcade.Sprite(filepath, 0.5) #variable to show the player with a scale.Choi
        self.physics_engine = None
        self.total_time = 0.0 # to add time.Choi


    def setup(self):
        self.player_list = arcade.SpriteList()        
        self.player_sprite = Player()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list.append(self.player_sprite)
        #Spatial hashing speeds the time it takes to find collisions, but increases the time it takes to move a sprite.
        #use_spatial_hash is set to false by default
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
        directory = os.path.dirname(__file__) # Load all directory path for image files.Choi
        filepath_mcd = directory + '/pictures/mcdonalds.jpg'
        filepath_wall = directory + '/pictures/wall.jpg'
        self.background = arcade.load_texture(filepath_mcd)
        for x in range(0, 1500, 32):
            wall = arcade.Sprite(filepath_wall)
            wall.center_x = x
            wall.center_y = 40
            self.wall_list.append(wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        self.total_time = 0.0 # to add time.Choi

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background) # display McDonald background first.Choi
        self.wall_list.draw() # display bottom green floor on top of McDonald background.Choi
        self.player_list.draw() # display red square(player).Choi
        arcade.draw_rectangle_outline(225, 720, 400, 40, arcade.color.BLACK, 2)
        arcade.draw_rectangle_outline(1275, 720, 400, 40, arcade.color.BLACK, 2)   
        arcade.draw_text('Player 1', 25, 660, arcade.color.BURGUNDY, font_size= 20, font_name= 'BRITANIC')
        arcade.draw_text('Player 2', 1375, 660, arcade.color.BURGUNDY, font_size=20,font_name='BRITANIC')
        
        minutes = int(self.total_time) // 60 # Calculate minutes.Choi   
        seconds = int(self.total_time) % 60 # Calculate seconds by using a modulus (remainder).Choi
        output = (f"{minutes:02d}:{seconds:02d}") # Display time output.Choi
        arcade.draw_text(output, WIDTH/2, HEIGHT -50, arcade.color.RED, 30) # Display the timer text.Choi

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
        elif key == arcade.key.J:
            self.player_sprite.update()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.J:
            self.player_sprite.update()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update()
        #collision check for player
        if self.player_sprite.center_x  > WIDTH - 30:
            self.player_sprite.center_x += -10
        elif self.player_sprite.center_x < 0 + 30:
            self.player_sprite.center_x += 10
        
        self.total_time += delta_time #Update time.Choi
        #arcade.check_for_collision_with_list()
        #arcade.check_for_collision()
        #We can use one of these to help with the collions between players


if __name__ == "__main__":
    
    view = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = Menu_view()
    view.show_view(menu_view)
    arcade.run()