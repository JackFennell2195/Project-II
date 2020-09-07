import arcade 
import numpy as np 
import csv
import tflearn

from arcade.gui import *
from numpy.random import seed
from numpy.random import randint
#seed random number generator
seed(1)

#Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Geometry Dash"

CHARACTER_SCALING = 1.1
GROUND_SCALING = 1
COLLISION_SCALING = 1.1
OBSTACLE_SCALING = 1.1

LOOP_BORDER_SCALING = 1.1

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 19

LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class GameMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.theme = None
        self.pause = False
        self.setup_theme()
        self.set_buttons()
    def on_show(self):
        arcade.set_background_color(arcade.color.AZURE)
        

    def set_button_textures(self):
        normal = "Geometry Dash/Assets/Images/button.png"
        hover = "Geometry Dash/Assets/Images/buttonHover.png"
        clicked = "Geometry Dash/Assets/Images/buttonClicked.png"
        locked = "Geometry Dash/Assets/Images/button.png"
        self.theme.add_button_textures(normal,hover,clicked,locked)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(20, arcade.color.WHITE)
        self.set_button_textures()

    def set_buttons(self):
        self.button_list.append(PlayButton(self,500,360,200,60,theme= self.theme))
        self.button_list.append(AI_GA_PlayButton(self,500,240,200,60,theme= self.theme))
        self.button_list.append(AI_BP_PlayButton(self,500,180,200,60,theme= self.theme))
    def on_draw(self):
        arcade.start_render()
        super().on_draw()

    def update(self, delta_time):
        if self.pause:
            self.pause = False
            game_view = GameView()
            self.window.show_view(game_view)
          

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        #Create and assign varibles
        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.loop_list = arcade.SpriteList()

        self.player_sprite = None
        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0
        
        self.jump = 0

        self.closet_block = ()
        self.Player = True
        self.AI = False	
        self.capture = False

        if self.AI == True:
            input_data = tflearn.input_data(shape=[None, 3])
            hidden_layer = tflearn.fully_connected(input_data, 6)
            output = tflearn.fully_connected(hidden_layer,2,activation='softmax')

            network = tflearn.regression(output)
            # Define model
            self.model = tflearn.DNN(network)
            self.load_model()

        #Player set up list
        self.player_sprite = arcade.Sprite("Geometry Dash/Assets/Images/player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 78
        self.player_list.append(self.player_sprite)

        #Ground set up list
        
        for x in range(-150, 6500, 50):
            ground = arcade.Sprite("Geometry Dash/Assets/Images/ground.png", GROUND_SCALING)
            ground.center_x = x
            ground.center_y = 25
            self.ground_list.append(ground)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.ground_list, GRAVITY)
        
        values = randint(7, 92, 16)*51
        np.sort(values)
        
        #Obstacles set up 
        coordinate_list = [[values[0],78],
                          [values[1],78],
                          [values[2],78],
                          [values[3],78],
                          [values[4],78],
                          [values[5],78],
                          [values[6],78],
                          [values[7],78],
                          [values[8],78],
                          [values[9],78],
                          [values[10],78],
                          [values[11],78],
                          [values[12],78],
                          [values[13],78],
                          [values[14],78],
                          [values[15],78],]
        for coordinate in coordinate_list:
            ground = arcade.Sprite("Geometry Dash/Assets/Images/obstacle.png", OBSTACLE_SCALING)
            ground.position = coordinate
            self.ground_list.append(ground)

        #Collision boxes set up
        coordinate_list2 = [[values[0]-1,75],
                           [values[1]-1,75],
                           [values[2]-1,75],
                           [values[3]-1,75],
                           [values[4]-1,75],
                           [values[5]-1,75],
                           [values[6]-1,75],
                           [values[7]-1,75],
                           [values[8]-1,75],
                           [values[9]-1,75],
                           [values[10]-1,75],
                           [values[11]-1,75],
                           [values[12]-1,75],
                           [values[13]-1,75],
                           [values[14]-1,75],
                           [values[15]-1,75],]
        for coordinate in coordinate_list2:
            collision = arcade.Sprite("Geometry Dash/Assets/Images/collision.png", COLLISION_SCALING)
            collision.position = coordinate
            self.collision_list.append(collision)

        loop = arcade.Sprite("Geometry Dash/Assets/Images/loop_border.png", LOOP_BORDER_SCALING)
        loop.center_x = 4800
        loop.center_y = 100
        self.loop_list.append(loop)
        #self.write_to_csv() 
    
    def on_show(self):
        #set background colour
       arcade.set_background_color(arcade.csscolor.MAROON)

    def load_model(self):
        self.model.load('Model_1')
        print("loaded model") 
        

    def on_draw(self):
        #Draw all sprites and text
        arcade.start_render()
        self.collision_list.draw()
        self.loop_list.draw()
        self.ground_list.draw()
        self.player_list.draw()
        score_text = f"Score: {self.window.score}"
        capture_text = f"Press C to capture data"
        cancel_text = f"Press X to stop capturing data"
        arcade.draw_text(score_text, 10 + self.view_left, 460 + self.view_bottom,
                         arcade.csscolor.WHITE, 20)
        arcade.draw_text(capture_text, 10 + self.view_left, 440 + self.view_bottom,
                         arcade.csscolor.WHITE, 12)
        arcade.draw_text(cancel_text, 10 + self.view_left, 420 + self.view_bottom,
                         arcade.csscolor.WHITE, 12)

    def on_key_press(self, key, modifiers):
        #Event when key is pressed 
        if key == arcade.key.C:
            self.capture = True

        if key == arcade.key.X:
            self.capture = True

        if self.Player == True:
            if key == arcade.key.SPACE:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    self.jump = 1
                    if self.capture == True:
                        self.write_to_csv(self.player_sprite)
                    self.jump = 0
       
                
           
    def on_update(self, delta_time):

        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        self.physics_engine.update()
        self.window.score +=1
        changed = False
        self.closet_block = arcade.get_closest_sprite(self.player_sprite,self.collision_list)
    

        if self.capture == True:
            self.write_to_csv(self.player_sprite)

        player_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.collision_list)
        for collision in player_hit_list:
            game_over_view = GameOverView()
            self.player_sprite.center_x = 50
            self.player_sprite.center_y = 78
            self.window.show_view(game_over_view)

        loop_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.loop_list)
        for collision in loop_hit_list:
            self.player_sprite.center_x = 0
            self.player_sprite.center_y = 78
       

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left <left_boundary:
            self.view_left -=  left_boundary - self.player_sprite.left
            changed = True
        
        right_boundary = self.view_left + RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left +=  self.player_sprite.left -right_boundary
            changed = True
        
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary -self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,SCREEN_WIDTH+self.view_left,
                                self.view_bottom,SCREEN_HEIGHT + self.view_bottom)

    def write_to_csv(self,player_sprite):
        with open('dataset.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_sprite.center_x, player_sprite.center_y, int(self.closet_block[1]),self.jump])  
    
    def read_csv(self):
        with open('weights.csv''r',newline='') as weight_file:
            reader = csv.reader(weight_file)
           

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 230 ,360,
                        arcade.color.WHITE,50)
        arcade.draw_text("Click to Restart", 230 ,280 ,
                        arcade.color.WHITE,32)
        score_text = f"Score: {self.window.score}"
        arcade.draw_text(score_text, 230, 200,
                         arcade.csscolor.WHITE, 30)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        game_view = GameView()
        
        self.window.show_view(game_view)
        

class PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="PLAY", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True
       
    def on_release(self):
        if self.pressed:
            self.game.pause = True
            self.pressed = False
           

class AI_GA_PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="GA PLAY", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.game.pause = True
            self.pressed = False
            
class AI_BP_PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="BP PLAY", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.game.pause = True
            self.pressed = False
def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    window.score = 0 
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()

    

