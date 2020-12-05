#CURRENTLY DOES NOT WORK
import arcade
import os.path

WIDTH = 1500
HEIGHT = 750
MOVEMENT_SPEED = 15
GRAVITY = 1
JUMP_SPEED = 20
HEALTH_BAR_LENGTH = 390
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
        self.is_jumping = False
        filepath = os.path.dirname(__file__) + '/pictures/red_square'
        self.scale = 0.5
        self.character_textures = []
        self.texture = arcade.load_texture(filepath + '.jpg')
        self.character_textures.append(self.texture)
        self.texture = arcade.load_texture(filepath + '_punch.png')
        self.character_textures.append(self.texture)
        self.texture = self.character_textures[0]
        self.center_x = 100
        self.center_y = 100


    def update_animation(self, key = None):
        if key == arcade.key.J:
            self.texture = self.character_textures[1]
        self.texture = self.character_textures[0]

    def update_health_bars(self):
        collisions = 1
        arcade.start_render()
        arcade.draw_rectangle_filled(225, 720, (HEALTH_BAR_LENGTH - (collisions * 10)), 30, arcade.color.BLUE_GRAY)


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        filepath = os.path.dirname(__file__) + '/pictures/spike.jpg'
        self.scale = 0.5
        self.enemy_textures = []
        self.texture = arcade.load_texture(filepath)
        self.enemy_textures.append(self.texture)
        self.texture = self.enemy_textures[0]
        self.center_x = 1200
        self.center_y = 95

class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None #variable used in draw function to show background image.Choi
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False   
        self.total_time = 0.0 # to add time.Choi

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()    
        self.player_sprite = Player()
        self.enemy_sprite = Enemy()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list.append(self.player_sprite)
        self.enemy_list.append(self.enemy_sprite)
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

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background) # display McDonald background first.Choi
        arcade.draw_rectangle_filled(225, 720, HEALTH_BAR_LENGTH, 30, arcade.color.RED)
        arcade.draw_rectangle_filled(1275, 720, HEALTH_BAR_LENGTH, 30, arcade.color.RED)
        arcade.draw_rectangle_outline(225, 720, 400, 40, arcade.color.BLACK, 2)
        arcade.draw_rectangle_outline(1275, 720, 400, 40, arcade.color.BLACK, 2)
        arcade.draw_text('Player 1', 25, 660, arcade.color.BURGUNDY, font_size= 20, font_name= 'BRITANIC')
        arcade.draw_text('Player 2', 1375, 660, arcade.color.BURGUNDY, font_size=20,font_name='BRITANIC')
        self.wall_list.draw() # display bottom green floor on top of McDonald background.Choi
        self.player_list.draw() # display red square(player).Choi        
        self.enemy_list.draw()
        minutes = int(self.total_time) // 60 # Calculate minutes.Choi   
        seconds = int(self.total_time) % 60 # Calculate seconds by using a modulus (remainder).Choi
        output = (f"{minutes:02d}:{seconds:02d}") # Display time output.Choi
        arcade.draw_text(output, WIDTH/2, HEIGHT -50, arcade.color.RED, 30) # Display the timer text.Choi

    def process_keychange(self):
        if self.up_pressed and not self.down_pressed and self.physics_engine.can_jump() and not self.jump_needs_reset:
            self.player_sprite.change_y = JUMP_SPEED
            self.jump_needs_reset = True
        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.J:
            self.player_sprite.update_animation(key)
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.J:
            self.player_sprite.update_animation(key)
        self.process_keychange()

    def on_update(self, delta_time):
        self.physics_engine.update()
        
        #collision check for player
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True
        if self.player_sprite.center_x  > WIDTH - 27:
            self.player_sprite.center_x += -MOVEMENT_SPEED
        elif self.player_sprite.center_x < 40:
            self.player_sprite.center_x += MOVEMENT_SPEED
        elif self.player_sprite.center_y > HEIGHT:
            self.player_sprite.center_y -= MOVEMENT_SPEED

        for enemy in self.enemy_list:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.player_sprite.center_x -= MOVEMENT_SPEED + 60
                self.player_sprite.update_health_bars()

        self.total_time += delta_time #Update time.Choi
        #arcade.check_for_collision_with_list()
        #arcade.check_for_collision()
        #We can use one of these to help with the collions between players


if __name__ == "__main__":
    
    view = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = Menu_view()
    view.show_view(menu_view)
    arcade.run()