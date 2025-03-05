import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        p_walk1 = pygame.image.load('asset/p_walk1.png').convert_alpha()
        p_walk2 = pygame.image.load('asset/p_walk2.png').convert_alpha()
        self.player_walk = [p_walk1, p_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('asset/playerjump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('asset/audio_jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type,):
        super().__init__()

        if type == 'bat':
            bat_1 = pygame.image.load('asset/bat1.png').convert_alpha()
            bat_2 = pygame.image.load('asset/bat2.png').convert_alpha()
            self.frames = [bat_1, bat_2]
            y_pos = 170
        else:
            frog_1 = pygame.image.load('asset/frog1.png').convert_alpha()
            frog_2 = pygame.image.load('asset/frog2.png').convert_alpha()
            self.frames = [frog_1, frog_2]
            y_pos = 300


        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -50: #100
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - startTime
    score_surf = font.render(f'Pontuacao: {current_time}', False, (86, 7, 12))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Meu Jogo')
clock = pygame.time.Clock()
font = pygame.font.Font('Pixeltype.ttf', 50)
game_ativo = False
startTime = 0
score = 0
music = pygame.mixer.Sound('asset/music.wav')
music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

bg_castle = pygame.image.load('asset/bg_castle.png').convert()
ground = pygame.image.load('asset/ground.png').convert()

# Intro screen
player_img = pygame.image.load('asset/playerstand.png').convert_alpha()
player_img = pygame.transform.rotozoom(player_img, 0, 2)
player_img_rect = player_img.get_rect(center=(400, 200))

game_name = font.render('Corrida', False, (86, 7, 12))
game_name_rect = game_name.get_rect(center=(400, 80))

start_message = font.render('Pressione  SPACE  para jogar', False, (86, 7, 12))
start_message_rect = start_message.get_rect(center=(400, 330))

# Timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_ativo:
            if event.type == obstacleTimer:
                obstacle_group.add(Obstacle(choice(['bat', 'frog', 'frog', 'frog'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_ativo = True
                startTime = int(pygame.time.get_ticks() / 1000)

    if game_ativo:
        screen.blit(bg_castle, (0, 0))
        screen.blit(ground, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_ativo = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_img, player_img_rect)

        score_message = font.render(f'Sua pontuacao: {score}', False, (86, 7, 12))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(start_message, start_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)