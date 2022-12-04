import pygame, os
from States.state import State
from States.menu import Menu
from States.utils import get_random_position, load_sound, load_sprite
from States.models import GameObject, Spaceship, Asteroids, Life
from States.game_over import GameOver

class Gameplay(State):
    MIN_ASTEROID_DISTANCE = 250
    
    def __init__(self, game):
        State.__init__(self,game)
        self.background = pygame.image.load(os.path.join(self.game.assets_dir, "Sprites", "background_space.png"))
        self.GAME_W,self.GAME_H = 480, 270
        self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540
        self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock() # Cria um objeto Clock
        self.life = []
        self.asteroids = [] # Cria uma lista de asteroides
        self.bullets = [] # Cria uma lista de tiros
        self.spaceship = Spaceship(3, (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2), self.bullets.append) # Cria uma instância da classe Spaceship
        self.score_value = 0 # Inicializa a pontuação com 0
        self.explosion_sound = load_sound("explosion_1") # Define o método para gerar um som de explosão
        self.song_sound = load_sound("Game_soundtrack_3") # Define o método para tocar a música tema da gameplay
        
        for i in range(self.spaceship.lifes):
            self.life.append(Life((30+(i * 50)+10*i, 25)))
        
        self.enemy = GameObject(
            (400, 300), load_sprite("enemy_spaceship", 0.1), (0, 1)
        ) # Cria uma instância da classe GameObject para o inimigo

    def show_score(self,x,y): # Método para mostrar o placar
        score_font = pygame.font.Font('Assets/Font/Polybius1981.ttf', 32) # Define a fonte e o tamanho da pontuação
        score = score_font.render("Score : " + str(self.score_value), True, (255,255,255)) # Define o texto do placar
        self.screen.blit(score, (x, y)) # Mostra o placar na tela

    def update(self, delta_time, actions):
        # Check if the game was paused 
        if actions["enter"]:
            new_state = Menu(self.game)
            new_state.enter_state()
        if actions["up"]:
            self.spaceship.accelerate() # Acelera a nave
        if actions["left"]:
            self.spaceship.rotate(clockwise=False)
        if actions["right"]:
            self.spaceship.rotate(clockwise=True)
        if actions["space"]:
            self.spaceship.shoot()
            actions["space"] = False

        self._process_game_logic() # Processa a lógica do jogo


    def _process_game_logic(self): # Método processa a lógica do jogo
        for game_object in self._get_game_objects(): # Percorre todos os objetos do jogo
            game_object.move(self.screen) # Move o objeto

        while len(self.asteroids) < 5: # Enquanto a quantidade de asteroides for menor que 5
            for _ in range(1): # Cria 6 asteroides
                while True:
                    position = get_random_position(self.screen) # Pega uma posição aleatória
                    if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                    ): # Verifica se a posição do asteroide está a uma distância mínima da nave
                        break
                self.asteroids.append(Asteroids(position, self.asteroids.append)) # Adiciona o asteroide na lista de asteroides
            
        if self.spaceship: # Verifica se a nave existe
            for asteroid in self.asteroids: # Percorre todos os asteroides
                if asteroid.collides_with(self.spaceship): # Verifica se o asteroide colidiu com a nave
                    self.explosion_sound.play() # Toca o som de explosão
                    self.spaceship.life_lost() # Chama o método life_lost da nave
                    self.life.pop(-1) # Remove uma vida da lista de vidas
                    self.spaceship.set_velocity((0, 0)) # Zera a velocidade da nave
                    self.spaceship.set_position((self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)) # Coloca a nave no centro da tela
                    
                    if self.spaceship.lifes == 0:
                        new_state = GameOver(self.game, self.score_value)
                        new_state.enter_state()
        
        for bullet in self.bullets[:]: # Percorre todos os tiros
            for asteroid in self.asteroids[:]: # Percorre todos os asteroides
                if asteroid.collides_with(bullet): # Verifica se o asteroide colidiu com o tiro
                    self.explosion_sound.play() # Toca o som de explosão
                    self.asteroids.remove(asteroid) # Remove o asteroide
                    self.bullets.remove(bullet) # Remove o tiro
                    asteroid.split() # Divide o asteroide em 2
                    if asteroid.size == 1:
                        self.score_value += 100
                    elif asteroid.size == 2:
                        self.score_value += 50
                    elif asteroid.size == 3:
                        self.score_value += 20
                    elif asteroid.size == 4:
                        self.score_value += 10
                    break
                
        for bullet in self.bullets[:]: # Percorre todos os tiros
            if not self.screen.get_rect().collidepoint(bullet.position): # Verifica se o tiro saiu da tela
                self.bullets.remove(bullet) # Remove o tiro da lista de tiros
    
    def _get_game_objects(self): # Método retorna todos os objetos do jogo
        game_objects = [*self.asteroids, *self.bullets, *self.life] # Cria uma lista com todos os asteroides e tiros
        
        if self.spaceship:
            game_objects.append(self.spaceship) # Adiciona a nave na lista de objetos do jogo
            game_objects.append(self.enemy) # Adiciona o inimigo na lista de objetos do jogo

        return game_objects # Retorna a lista de objetos do jogo
    
    def render(self, display): # Método desenha na tela
        self.screen.blit(self.background, (0, 0)) # Desenha a imagem de fundo na tela
        
        for game_object in self._get_game_objects(): # Percorre todos os objetos do jogo
            game_object.draw(self.screen) # Desenha o objeto na tela
        
        self.show_score(self.screen.get_size()[0]-200, 25) # Mostra o placar na tela
        
        pygame.display.flip() # Atualiza a tela
        self.clock.tick(60) # Define o FPS