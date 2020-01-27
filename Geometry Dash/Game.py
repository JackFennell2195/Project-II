import arcade 

#Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Geometry Dash"

CHARACTER_SCALING = 1.1
GROUND_SCALING = 1
COLLISION_SCALING = 1.1
OBSTACLE_SCALING = 1.1

PLAYER_MOVEMENT_SPEED = 4
GRAVITY = 1
PLAYER_JUMP_SPEED = 18

LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()

        self.player_sprite = None
        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        #Player set up list
        self.player_sprite = arcade.Sprite("Geometry Dash/Assets/Images/player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        #Ground set up list
        
        for x in range(-150, 7500, 50):
            ground = arcade.Sprite("Geometry Dash/Assets/Images/ground.png", GROUND_SCALING)
            ground.center_x = x
            ground.center_y = 25
            self.ground_list.append(ground)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.ground_list, GRAVITY)
    
        #Obstacles set up 
        coordinate_list = [[512,78],
                           [780,78],
                           [1000,78],
                           [1239,78],
                           [1500,78],
                           [1750,78],
                           [2050,78],
                           [2280,78],
                           [2510,78],
                           [2780,78],
                           [3100,78],
                           [3290,78],
                           [3560,78],
                           [3830,78],
                           [4210,78],
                           [4560,78],]
        for coordinate in coordinate_list:
            ground = arcade.Sprite("Geometry Dash/Assets/Images/obstacle.png", OBSTACLE_SCALING)
            ground.position = coordinate
            self.ground_list.append(ground)

        #Collision set up
        coordinate_list2 = [[511,76],
                           [779,76],
                           [999,76],
                           [1238,76],
                           [1499,76],
                           [1749,76],
                           [2049,76],
                           [2279,76],
                           [2509,76],
                           [2779,76],
                           [3099,76],
                           [3289,76],
                           [3559,76],
                           [3829,76],
                           [4209,76],
                           [4559,76],]
        for coordinate in coordinate_list2:
            collision = arcade.Sprite("Geometry Dash/Assets/Images/collision.png", COLLISION_SCALING)
            collision.position = coordinate
            self.collision_list.append(collision)

    def on_show(self):
       arcade.set_background_color(arcade.csscolor.MAROON)

    def on_draw(self):

        arcade.start_render()
        self.collision_list.draw()
        self.ground_list.draw()
        self.player_list.draw()

        score_text = f"Score: {self.window.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 460 + self.view_bottom,
                         arcade.csscolor.WHITE, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        self.physics_engine.update()
        self.window.score +=1
        changed = False

        player_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.collision_list)

        for collision in player_hit_list:
            game_over_view = GameOverView()
            self.player_sprite.center_x = 50
            self.player_sprite.center_y = 100
            self.window.show_view(game_over_view)


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


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        arcade.start_render()
        game_view = GameView()
        arcade.draw_text("Game Over", 230 ,360,
                        arcade.color.WHITE,50)
        arcade.draw_text("Click to Restart", 230 ,280 ,
                        arcade.color.WHITE,40)
        score_text = f"Score: {self.window.score}"
        arcade.draw_text(score_text, 230, 200,
                         arcade.csscolor.WHITE, 30)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        game_view = GameView()
        self.window.show_view(game_view)



def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    window.score = 0 
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()

    

