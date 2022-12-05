import os, time, pygame
# Load our scenes
from States.title import Title
from States.gameplay import Gameplay
from States.story import Story

class Game(): 
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Polidroids") # Define o título da janela
            game_icon = pygame.image.load('Docs/Polidroids.png')
            pygame.display.set_icon(game_icon)
            self.GAME_W,self.GAME_H = 480, 270
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            self.running, self.playing = True, True
            self.actions = {"left": False, "right": False, "up" : False, "down" : False, "esc" : False, "space" : False, "enter" : False}
            self.dt, self.prev_time = 0, 0
            self.state_stack = []
            self.load_assets()
            self.load_states()

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.get_events()
                self.update()
                self.render()

        def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.actions['esc'] = True
                    if event.key == pygame.K_LEFT:
                        self.actions['left'] = True
                    if event.key == pygame.K_RIGHT:
                        self.actions['right'] = True
                    if event.key == pygame.K_UP:
                        self.actions['up'] = True
                    if event.key == pygame.K_DOWN:
                        self.actions['down'] = True
                    if event.key == pygame.K_ESCAPE:
                        self.actions['esc'] = True
                    if event.key == pygame.K_SPACE:
                        self.actions['space'] = True    
                    if event.key == pygame.K_RETURN:
                        self.actions['enter'] = True 
                    if event.key == pygame.K_p:
                        self.actions['pause'] = True  

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.actions['esc'] = False
                    if event.key == pygame.K_LEFT:
                        self.actions['left'] = False
                    if event.key == pygame.K_RIGHT:
                        self.actions['right'] = False
                    if event.key == pygame.K_UP:
                        self.actions['up'] = False
                    if event.key == pygame.K_DOWN:
                        self.actions['down'] = False
                    if event.key == pygame.K_ESCAPE:
                        self.actions['esc'] = False
                    if event.key == pygame.K_SPACE:
                        self.actions['space'] = False
                    if event.key == pygame.K_RETURN:
                        self.actions['enter'] = False
                    if event.key == pygame.K_p:
                        self.actions['pause'] = False

        def update(self):
            self.state_stack[-1].update(self.dt,self.actions)

        def render(self):
            if len(self.state_stack) == 0:
                exit()
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            if not isinstance(self.state_stack[-1], (Gameplay, Story)):
                pygame.display.flip()

        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def draw_text(self, surface, text, color, x, y, size):
            self.font = pygame.font.Font(os.path.join(self.font_dir, "Polybius1981.ttf"), size)
            text_surface = self.font.render(text, True, color)
            #text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("Assets")
            self.sprite_dir = os.path.join(self.assets_dir, "Sprites")
            self.font_dir = os.path.join(self.assets_dir, "Font")
            self.font= pygame.font.Font(os.path.join(self.font_dir, "Polybius1981.ttf"), 40)

        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()