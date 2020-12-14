from Test_file import HEALTH_BAR_LENGTH
import arcade
from arcade import key
from arcade import window_commands

import os.path

GAME_TITLE = "Pigeon Fighter"
CURRENT_FOLDER = os.path.dirname(__file__)
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
GROUND_HEIGHT = 50
STARTING_HEALTH = 100
SECONDS_PER_ROUND = 90
GRAVITY = 1
HORIZONTAL_SPEED = 10
VERTICAL_SPEED = 20
UPDATES_PER_FRAME = 10
SECONDS_PER_FRAME = 1/60

# ------------------------------------------------------------------------------
# Game Base Classes (to inherit from)
# ------------------------------------------------------------------------------
class Actor(arcade.Sprite):
    
    def on_draw(self):
        pass

    def on_key_press(self, key):
        pass
    
    def on_key_release(self, key):
        pass
    
    def on_update(self):
        pass

    def setup(self):
        pass


class CollisionHandler:

    def on_collision(self):
        pass


# ------------------------------------------------------------------------------
# Game Actor and Handler Classes
# ------------------------------------------------------------------------------
class Animation:

    def __init__(self, actor, file_pattern, num_files):
        super().__init__()
        self._actor = actor
        self._current_frame = 0
        self._file_pattern = file_pattern
        self._num_files = num_files
        self._textures = []
        
    def on_draw(self, direction):
        self._current_frame += 1
        if self._current_frame > (self._num_files - 1) * UPDATES_PER_FRAME:
            self._current_frame = 0
        frame_index = self._current_frame // UPDATES_PER_FRAME
        self._actor.texture = self._textures[frame_index][direction]
        self._actor.draw()

    def setup(self, direction):
        for index in range(self._num_files):
            image = CURRENT_FOLDER + self._file_pattern.format(index + 1)
            right = arcade.load_texture(image)
            left = arcade.load_texture(image, flipped_horizontally = True)
            self._textures.append( [right, left] )
        self._actor.texture = self._textures[0][direction]


class AttackHandler(CollisionHandler):
    
    def __init__(self, attacker, defender):
        self._attacker = attacker
        self._defender = defender
        
    def on_collision(self):
        # TODO: is all we need to do here? is it a more complicated if statment?
        collided = arcade.check_for_collision(self._attacker, self._defender)
        if collided == True and self._attacker.current_action == "attack":
            self._defender.health -= 5


class Background(Actor):
    
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
        
    def on_draw(self):
        bottom_left_x = 0
        bottom_left_y = 0
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x, 
            bottom_left_y, 
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            self.texture) 

    def setup(self):
        image = CURRENT_FOLDER + self._file_path
        self.texture = arcade.load_texture(image)


class Fighter(Actor):

    def __init__(self, key_map, starting_direction, starting_x, walk_file, punch_file):
        super().__init__()
        self.current_action = "none"
        self._direction = starting_direction
        self._key_map = key_map
        self._starting_x = starting_x
        self._idle_animation = Animation(self, walk_file, 1)
        self._walk_animation = Animation(self, walk_file, 8)
        self._punch_animation = Animation(self, punch_file, 8)
        self.health = HEALTH_BAR_LENGTH

    def on_draw(self):
        if self.current_action == "idle":
            self._idle_animation.on_draw(self._direction)
        elif self.current_action == "left":
            self._walk_animation.on_draw(self._direction)  
        elif self.current_action == "right":
            self._walk_animation.on_draw(self._direction)  
        elif self.current_action == "jump":
            self._idle_animation.on_draw(self._direction)  
        elif self.current_action == "attack":
            self._punch_animation.on_draw(self._direction) 

    def on_key_press(self, key):
        self.current_action = self._key_map.get(key, "idle")

    def on_key_release(self, key):
        self.current_action = "idle"
    
    def on_update(self):
        if self.current_action == "none":
            self._update_starting_position()
        self._update_direction()
        self._update_horizontal_position()
        self._update_vertical_position()

    def setup(self):
        self._idle_animation.setup(self._direction)
        self._walk_animation.setup(self._direction)
        self._punch_animation.setup(self._direction)

    def _update_direction(self):
        if self.current_action == "left":
            self.change_x = -HORIZONTAL_SPEED
            self._direction = 1
        elif self.current_action == "right":
            self.change_x = HORIZONTAL_SPEED
            self._direction = 0
        elif self.current_action == "jump":
            self.change_y = VERTICAL_SPEED
        elif self.current_action == "idle":
            self.change_x = 0
            
    def _update_horizontal_position(self):
        self.center_x += self.change_x
        if self.left <= 0:
            self.left = 0
        elif self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
    
    def _update_starting_position(self):
        self.center_x = self._starting_x
        self.bottom = GROUND_HEIGHT

    def _update_vertical_position(self):
        self.change_y -= GRAVITY
        self.center_y += self.change_y
        if self.bottom <= GROUND_HEIGHT:
            self.bottom = GROUND_HEIGHT
        elif self.top >= SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class HealthBar(Actor):

    def __init__(self, fighter, starting_x):
        super().__init__()
        self._fighter = fighter
        self._starting_x = starting_x
        
    def on_draw(self):
        arcade.draw_rectangle_outline(225, 720, 400, 40, arcade.color.BLACK, 2)
        arcade.draw_rectangle_outline(1275, 720, 400, 40, arcade.color.BLACK, 2)
        arcade.draw_rectangle_filled(225, 720, self._fighter.health, 30, arcade.color.RED)
        arcade.draw_rectangle_filled(1275, 720, self._fighter.health, 30, arcade.color.RED)
        arcade.draw_text('Seagull', 25, 660, arcade.color.BURGUNDY, font_size= 20, font_name= 'BRITANIC')
        arcade.draw_text('Fries', 1415, 660, arcade.color.BURGUNDY, font_size=20,font_name='BRITANIC')

class Over_Instructions(Actor):

    def __init__(self):
        super().__init__()
        
    def on_draw(self):
        text = "Game Over!"
        start_x = SCREEN_WIDTH / 2
        start_y = (SCREEN_HEIGHT / 2) - 50
        color = arcade.color.WHITE
        font_size = 50
        arcade.draw_text(
            text, start_x, start_y, color, font_size, anchor_x = "center")

class Instructions(Actor):

    def __init__(self):
        super().__init__()
        
    def on_draw(self):
        text = "Press any key to start..."
        start_x = SCREEN_WIDTH / 2
        start_y = (SCREEN_HEIGHT / 2) - 50
        color = arcade.color.WHITE
        font_size = 20
        arcade.draw_text(
            text, start_x, start_y, color, font_size, anchor_x = "center")
    
    def on_key_press(self, key):
        factory = GameFactory()
        fight_view = factory.create_fightview()
        fight_view.setup()
        window = window_commands.get_window()
        window.show_view(fight_view)


class Referee(Actor):
    
    def __init__(self, attacker, defender, timer):
        super().__init__()
        self._attacker = attacker
        self._defender = defender
        self._timer = timer
        self.factory = GameFactory()
        self.overview = factory.create_overview()
        self.overview.setup()
    
    def on_update(self):
        # TODO: check if game is over and open "overview" if it is
        if self._attacker.health <= 0 and self._defender.health >= 0:
            window.show_view(self.overview)
        elif self._attacker.health >= 0 and self._defender.health <= 0:
            window.show_view(self.overview)
        elif self._attacker.health <= 0 and self._defender.health <= 0:
            window.show_view(self.overview)

class Timer(Actor):

    def __init__(self):
        super().__init__()
        self.seconds_remaining = SECONDS_PER_ROUND
        factory = GameFactory()
        overview = factory.create_overview()
        overview.setup()


    def on_draw(self):
        minutes = int(self.seconds_remaining) // 60 
        seconds = int(self.seconds_remaining) % 60 
        text = (f"{minutes:02d}:{seconds:02d}") 
        start_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT - 75
        color = arcade.color.RED
        font_size = 30
        anchor_x = "center"
        arcade.draw_text(
            text, start_x, start_y, color, font_size, anchor_x = "center")

    def on_update(self):
        self.seconds_remaining -= SECONDS_PER_FRAME
        if self.seconds_remaining <= 0.0:
            exit()


class Title(Actor):

    def __init__(self):
        super().__init__()
        
    def on_draw(self):
        text = GAME_TITLE
        start_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT / 2
        color = arcade.color.WHITE
        font_size = 50
        arcade.draw_text(
            text, start_x, start_y, color, font_size, anchor_x = "center")

# ------------------------------------------------------------------------------
# Game View Classes
# ------------------------------------------------------------------------------
class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        self._actors = []
        self._collision_handlers = []
    
    def add_actor(self, actor):
        if actor not in self._actors:
            self._actors.append(actor)

    def add_handler(self, handler):
        if handler not in self._collision_handlers:
            self._collision_handlers.append(handler)

    def on_draw(self):
        arcade.start_render()
        for actor in self._actors:
            actor.on_draw()
        
    def on_key_press(self, key, modifiers):
        for actor in self._actors:
            actor.on_key_press(key)

    def on_key_release(self, key, modifiers):
        for actor in self._actors:
            actor.on_key_release(key)

    def on_update(self, delta_time):
        for actor in self._actors:
            actor.on_update() 
        for handler in self._collision_handlers:
            handler.on_collision()
        
    def setup(self):
        for actor in self._actors:
            actor.setup()
    

# ------------------------------------------------------------------------------
# Game Factory Classes
# ------------------------------------------------------------------------------
class GameFactory:

    def create_fightview(self):
        # create player 1
        keys1 = {key.A: "left", key.D: "right", key.W: "jump", key.Q: "attack"}
        starting_direction1 = 0
        starting_x1 = 100
        walk_file1 = "/assets/seagull_w{0}.png"
        punch_file1 = "/assets/seagull_p{0}.png"
        player1 = Fighter(
            keys1, starting_direction1, starting_x1, walk_file1, punch_file1)
        player1.scale = 0.50

        # create player 2
        keys2 = {key.J: "left", key.L: "right", key.I: "jump", key.U: "attack"}
        starting_direction2 = 1
        starting_x2 = SCREEN_WIDTH - 100
        walk_file2 = "/assets/fries_w{0}.png"
        punch_file2 = "/assets/fries_p{0}.png"
        player2 = Fighter(
            keys2, starting_direction2, starting_x2, walk_file2, punch_file2)
        player2.scale = 0.25

        # create other actors
        background = Background("/assets/mcdonalds.jpg")
        timer = Timer()
        healthbar1 = HealthBar(player1, 100)
        healthbar2 = HealthBar(player2, SCREEN_WIDTH - 400)
        referee = Referee(player1, player2, timer)

        # create collision handlers
        attack_handler = AttackHandler(player1, player2)
        
        # create fight view
        fight_view = GameView()
        fight_view.add_actor(background)
        fight_view.add_actor(player1)
        fight_view.add_actor(player2)
        fight_view.add_actor(healthbar1)
        fight_view.add_actor(healthbar2)
        fight_view.add_actor(timer)
        fight_view.add_actor(referee)
        fight_view.add_handler(attack_handler)

        return fight_view

    def create_menuview(self):
        # create actors
        background = Background("/assets/bluetiles.jpg")
        title = Title()
        instructions = Instructions()
        
        # create view
        menu_view = GameView()
        menu_view.add_actor(background)
        menu_view.add_actor(title)
        menu_view.add_actor(instructions)
        return menu_view

    def create_overview(self):
        # TODO: update this with whatever you want on game over view
        # create actors

        background = Background("/assets/bluetiles.jpg")
        instructions = Over_Instructions()
        
        # create view
        over_view = GameView()
        over_view.add_actor(background)
        over_view.add_actor(instructions)
        return over_view


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    factory = GameFactory()
    menu_view = factory.create_menuview()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()