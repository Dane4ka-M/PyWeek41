import pygame

import sys
import time

pygame.init()

pygame.mixer.init()

from windows import dead_window
from windows import menu_window
from windows.quit_window import game_quit
from windows.pause_window import pause
from levels.level_manager import load_level, set_background, level_update
from classes.player import Player, set_animation
from classes.camera import Camera
from classes.enemy import Enemy
from classes.markers import Marker
from classes.audio import Audio


running = False

current_level = 0

tile_size = 16

trigger_next_level = False

screen_width, screen_height = 1024, 576
#screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height))


# библиотека звуков 

audio = Audio()

audio.load_audio('button_click', 'sounds/buttonclick.wav') #Нажатие кнопки
audio.load_audio('change_level', 'sounds/ChangeLevel.wav') #Изменение уровня+

audio.load_audio('player_walk', 'sounds/GGshag.wav') #Игрок идёт+
audio.load_audio('player_jump', 'sounds/GGUp.wav') #Игрок прыгает+
audio.load_audio('player_land', 'sounds/GGJump.wav') #Игрок приземляется
audio.load_audio('player_collect', 'sounds/CollectBerry.wav') #Игрок собирает ягоды+
audio.load_audio('player_turnoff', 'sounds/GGTurnOff.wav') #Игрок теряет сознание
audio.load_audio('player_dead', 'sounds/SoundDead.wav') #Игрок умирает +- (не слышно)

audio.load_audio('vamp_walk', 'sounds/VampShag.wav') #Вампир идёт+
audio.load_audio('vamp_jump', 'sounds/VampUp.wav') #Вампир прыгает+
audio.load_audio('vamp_land', 'sounds/VampJump.wav') #Вампир приземляется
audio.load_audio('vamp_trig', 'sounds/VampTrig.wav') #Вампир заметил игрока+

audio.load_audio('bat_fly', 'sounds/Bat.wav') #Летучая мышь летит

audio.load_audio('menu', 'sounds/BG_Melody_SlowDynamic.wav') #Музыка меню +
audio.load_audio('thinking', 'sounds/BG_Melody_ThinkingDynamic.wav') #Музыка на начале и рычагах +- (на рычагах почему-то не работает)
audio.load_audio('what', 'sounds/BG_Melody_WhatDynamic.wav') #Музыка 1 уровень до встречи с вампиром+
audio.load_audio('run', 'sounds/BG_Melody_MoreDynamic.wav') #Музыка побега+

def change_level(number, screen, camera, audio):

    """
    СЮДА МОЖНО ВОТКНУТЬ ЗВУК ПЕРЕХОДА НА ДРУГОЙ УРОВЕНЬ
    """

    print('change to level ', number)

    background_color = set_background(number) #пока цвет, потом заменить на картинку
    
    platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level = load_level(number, tile_size, camera, screen, audio) 
    

    if enemy:
        enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'IDLE', player, level) #заспавнить врага

    
    if len(mobs) >0:
        if current_level == 2:
            for i in range(len(mobs)):
                mobs[i].create_enemy(mobs_spawn_xy[i][0], mobs_spawn_xy[i][1], 'IDLE', player, level) 
                mobs[i].destroy_enemy() 
        else:
            for i in range(len(mobs)):
                mobs[i].create_enemy(mobs_spawn_xy[i][0], mobs_spawn_xy[i][1], 'IDLE', player, level) 

    screen.fill(background_color)

    camera.set_bounds(screen, level_width, level_height)

    player.set_jump_length(current_level)



    return background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level




def main():
    global current_level
    global trigger_next_level
    global runnning
    global screen
    global screen_width, screen_height

    fps = 60
    clock = pygame.time.Clock()

    '''
    https://www.daniweb.com/programming/software-development/threads/54881/pygame-get-screen-size 
    изучить потом, чтобы сделать окно подстраивающимся под размеры экрана. вывести это в окно настройки?
    '''

    
    
    camera = Camera(screen_width, screen_height)


    '''для отладки, удалить позже'''
    #platforms, level_width, level_height, player, enemy, enemy_spawn_xy, level = load_level(0, tile_size) 
    #background_color = set_background(0)
    #camera.set_bounds(level_width, level_height)
    #enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'CHASE', player, level) #заспавнить врага и назначить следить за игроком

    final_started = True
    frame = 0
    wait_play = 0

    background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level = change_level(current_level, screen, camera, audio)

    running = True

    while running:
        clock.tick(fps)
        
        #---ОБРАБОТКА СОБЫТИЙ---
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = game_quit(screen, screen_width, screen_height)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    to_menu = pause(screen, screen_width, screen_height)
                    if to_menu == True:
                        #print('to menu is ', to_menu)
                        to_menu = False
                        running = False

                if event.key == pygame.K_TAB:
                    current_level +=1
                    background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level = change_level(current_level, screen, camera, audio) #ОТЛАДКА, потом удалить
                    
                if event.key in ([pygame.K_SPACE], keys[pygame.K_UP], keys[pygame.K_w]):
                    audio.play_player('player_jump')

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    player.jump_stop()
                

        if not current_level == 4:
        
            keys = pygame.key.get_pressed()

            jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
            player.velocity_x = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.velocity_x = -player.speed
                player.direction = 0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.velocity_x = player.speed
                player.direction = 1

            if jump_pressed:
                player.jump(audio)

        
            jumping = jump_pressed



        #---ОТРИСОВКА---

        if player.alive:

            screen.fill(background_color)

            for platform in platforms:

                platform_rect_transformed, platform_image_transformed = camera.apply(platform)
                screen.blit(platform_image_transformed, platform_rect_transformed)

            for marker in markers:
                marker_rect_transformed, marker_image_transformed = camera.apply(marker)
                screen.blit(marker_image_transformed, marker_rect_transformed)

            for item in items:
                item_rect_transformed, item_image_transformed = camera.apply(item)
                if item.alive:
                    screen.blit(item_image_transformed, item_rect_transformed)
        
            player_rect_transformed, player_image_transformed = camera.apply(player)
            screen.blit(player_image_transformed, player_rect_transformed)

            if len(mobs) > 0:
                for mob in mobs:
                    mob_rect_transformed, mob_image_transformed = camera.apply(mob)
                    screen.blit(mob_image_transformed, mob_rect_transformed)

            if enemy:
                enemy_rect_transformed, enemy_image_transformed = camera.apply(enemy)
                screen.blit(enemy_image_transformed, enemy_rect_transformed)

        
        if not player.alive:
            audio.stop_music()
            audio.stop_enemy()
            audio.play_player('player_dead')
            should_reset = dead_window.game_over(screen, screen_width, screen_height) #enter не всегда срабатывает с первого раза

            if should_reset:
                background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level = change_level(current_level, screen, camera, audio)


        #---ОБНОВЛЕНИЕ ИГРЫ---
        

        for marker in markers:
            marker.update(screen, player, items, current_level)
            if marker.is_triggered:
                if marker.type == 'NEXTLEVEL':
                    if current_level == 2:
                        print('level 2')
                        trigger_next_level = level_update(current_level, camera, screen, markers, items)
                        marker.is_triggered = False
                        break
                    trigger_next_level = level_update(current_level, camera, screen, markers, items)
                    marker.is_triggered = False

                if marker.type == 'TRIGGER_1':

                    

                    if current_level == 1:
                        marker.alive = False
                        
                        audio.play_enemy('vamp_trig')

                        audio.stop_music()

                        if enemy.detect_timer == None:
                            enemy.detect_timer = time.time()

                        #print('MARKER: the enemy is processing...')
                        time_passed = time.time() - enemy.detect_timer
                        if time_passed >= enemy.detect_delay:
                            #print('MARKER: start chasing')
                            enemy.state = 'CHASE'
                            enemy.can_chase = True

                            audio.play_music('run')
                            marker.is_triggered = False

                        for item in items:
                            if current_level == 1:
                                if item.type == 'FOREST':
                                    item.image_surface.set_alpha(255)
                                    item.can_pass = True
                                    item.can_interact = False
                                    item.alive = False

                            

                    
                                

                    if current_level == 2: #маркер в начале уровня, спавнит волков слева и триггерит вампира справа
                        
                        

                        if enemy.detect_timer == None:
                            enemy.detect_timer = time.time()

                        print('the enemy is processing...')
                        time_passed = time.time() - enemy.detect_timer

                        if time_passed < 1:
                            audio.play_enemy('vamp_trig')
                        if time_passed >= 3:
                            #print('start chasing')
                            enemy.state = 'CHASE'
                            enemy.can_chase = True

                            audio.play_music('run')
                            
                            if marker.alive:
                                marker.alive = False
                                i = 0
                                for mob in mobs:
                                    if mob.type == 'WOLF':
                                        mob.create_enemy(mobs_spawn_xy[i][0], mobs_spawn_xy[i][1], 'IDLE', player)
                                        i += 1
                                    if i == 3:
                                        marker.is_triggered = False
                                        break
                
                if marker.type == 'TRIGGER_2':

                    if current_level == 2: #деспавнит первых трёх волков для экономии ресурсов, спавнит ещё пять на дне ямы 
                        marker.alive = False

                        i = 0
                        for mob in mobs:
                            if mob.type == 'WOLF':
                                mob.destroy_enemy()
                                i += 1

                                if i == 3:
                                    break

                        for mob in mobs:
                            if mob.type == 'WOLF':
                                mob.create_enemy(mobs_spawn_xy[i][0], mobs_spawn_xy[i][1], 'IDLE', player)
                                i += 1

                                if i == 8:
                                    marker.is_triggered = False
                                    break
                            
                if marker.type == 'TRIGGER_3': #затухание музыки, потому что погоня прекратилась (вампир задеспавнен)
                    #print('marker 3 triggered')
                    if current_level == 2:

                        audio.stop_music()

                        music_wait = time.time()

                        if music_wait - time.time() >= 3:
                            

                            enemy.destroy_enemy()
                            enemy.state = 'IDLE'
                            enemy.can_chase = False
                            

                            marker.alive = False
                            marker.is_triggered = False

                            
                            audio.play_music('thinking')

                            break

                if marker.type == 'TRIGGER_0':
                    print('DO YOU WANNA HAVE A BAD TIMEEEE')
                    if current_level == 2: #деспавнит первых трёх волков для экономии ресурсов, спавнит ещё пять на дне ямы 
                        marker.alive = False

                        audio.play_enemy('vamp_trig')

                        audio.stop_music()

                        print('trigger 4, level 2')
                        enemy.destroy_enemy()
                        enemy.create_enemy(tile_size*217, 256, 'IDLE', player)
                        enemy.can_chase = False
                        print('enemy on ', enemy.rect.x, enemy.rect.y, enemy.alive)
                        print('player on ', player.rect.x, player.rect.y)

                        if enemy.detect_timer == None:
                            enemy.detect_timer = time.time()
                        
                        for item in items:
                            if item.type == 'LEVER_3':
                                item.is_triggered = True

                        print('MARKER: the enemy is processing...')
                        time_passed = time.time() - enemy.detect_timer
                        if time_passed >= 2:

                            audio.play_music('run')

                            print('MARKER: start chasing')
                            enemy.state = 'CHASE'
                            enemy.can_chase = True

                        marker.is_triggered = False

                        


        for item in items:
            item.update(screen, camera, player, items, audio)
            if item.is_triggered:
                #print('item triggered', current_level, item.type)
                if item.type == 'BUSH_BLUE' and current_level == 0:
                    trigger_next_level = level_update(0, camera, screen, markers, items)
                    item.is_triggered = False
                    #print('trigger level')

                if current_level == 2:
                                
                    if item.type == 'LEVER_1':
                        #print('triggered lever 1')
                        for target in items:
                            if target.type == 'BRIDGE_1':
                                #print('found bridge 1')
                                target.y = target.y + tile_size*5
                                target.width = tile_size*6
                                target.height = tile_size
                                target.image_surface = pygame.Surface((target.width, target.height))
                                target.image = pygame.image.load('images/tileset/_17.png')
                                target.rect = pygame.Rect(target.x, target.y, target.width, target.height)
                                break
                        item.is_triggered = False

                    if item.type == 'LEVER_2':
                        #print('triggered lever 2')
                        for target in items:
                            if target.type == 'BRIDGE_2':
                                #print('found bridge 2')
                                target.y = target.y + tile_size*5
                                target.width = tile_size*6
                                target.height = tile_size
                                target.image_surface = pygame.Surface((target.width, target.height))
                                target.image = pygame.image.load('images/tileset/_19.png')
                                target.rect = pygame.Rect(target.x, target.y, target.width, target.height)
                                break
                        item.is_triggered = False

                    if item.type == 'LEVER_3':
                        #print('triggered lever 3')
                        for target in items:
                            print(target.type)
                            if target.type == 'BRIDGE_3':
                                #print('found bridge 3')
                                target.y = target.y - tile_size*5
                                target.width = tile_size
                                target.height = tile_size*6
                                target.image_surface = pygame.Surface((target.width, target.height))
                                target.image = pygame.image.load('images/tileset/_20.png')
                                target.rect = pygame.Rect(target.x, target.y, target.width, target.height)
                                break
                        item.is_triggered = False




        if current_level == 4: #финальная кацсцена
            print('final')

            

            for item in items:
                if item.type == 'POLICE':
                    camera.target = item
                    print('camera target set to police')
                    camera.camera.y = camera.camera.y - 16

            enemy.state = 'IDLE'
            enemy.can_chase = False
            
            
            if final_started:
                scene_start = time.time()
                final_started = False

            print('difference ', time.time() - scene_start)
            if time.time() - scene_start >= 1:
                player.speed = 2
                player.play_speed = 10
                player.velocity_x = player.speed
                player.direction = 1

            if time.time() - scene_start >= 3:
                player.velocity_x = 0

            if time.time() - scene_start >= 4:

                audio.fadeout_music()
                audio.play_other('vamp_trig') #заменить на стук

            
            if time.time() -scene_start >= 7:
                audio.stop_other()

                enemy.speed = 2
                enemy.play_speed = 8
                enemy.velocity_x = enemy.speed
                enemy.direction = 1


            if time.time() - scene_start >= 9:
                enemy.velocity_x = 0

            if time.time() - scene_start >= 10:
                enemy.velocity_x = 1

            if time.time() - scene_start >= 11:
                enemy.velocity_x = 0

            if time.time() - scene_start >= 12:
                enemy.velocity_x = 0.8

            if time.time() - scene_start >= 13:
                enemy.velocity_x = 0

            if time.time() - scene_start >= 13.5:
                player.direction = 0

            if time.time() - scene_start >= 14.5:
                player.direction = 0
                player.velocity_x = 0.5 
                player.play_speed = 20

            if time.time() - scene_start >= 15:
                player.velocity_x = 0

            if time.time() - scene_start >= 16:
                player.direction = 1
                player.velocity_x = 3
                player.play_speed = 20
                enemy.cut_scene = True #маркер для включения анимации полёта
                enemy.velocity_x = 7

            if time.time() - scene_start >= 16.5:
                audio.stop_player()
                enemy.velocity_x = 0
                enemy.animation = set_animation('enemy_right_fly')
                player.velocity_x = 0
                audio.play_player('player_dead')

            if time.time() - scene_start >= 17:
                audio.stop_player()
                player.cut_scene = True

            if time.time() - scene_start >= 19.8:
                player.cut_scene = False
                player.frame = 0
                player.wait_play = 0
                player.cut_scene_finish = True

            if time.time() - scene_start >= 20:
                audio.play_player('vamp_trig')
                while True:
                    screen.fill((0, 0, 0))
                    pygame.display.flip()

                    if time.time() - scene_start >= 23:
                        to_menu = True
                        running = False
                        break
                    
                

            




        if trigger_next_level:
            current_level += 1
            audio.stop_music()
            audio.play_other('change_level')
            background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level = change_level(current_level, screen, camera, audio)
            trigger_next_level = False

            
        



        player.update(screen, platforms, items, camera, enemy, audio)
        
        camera.update(player, screen)

        if enemy:
            enemy.update(platforms, markers, camera, player, audio)

        if len(mobs)>0:
            for mob in mobs:
                mob.update(platforms, markers, camera, player, audio, screen)
        
        """if trigger_next_level:
            camera.fade_in(screen, (0, 0, 0), background_color, platforms, items, player) убрала из-за багов"""



        # ЗВУКИ
        





        pygame.display.flip()


while True:
    game_start = menu_window.show(screen, screen_width, screen_height, audio)
    if game_start == True:
        game_start = False
        running = True
        audio.stop_music()
        main()

    if __name__ == '__main__':
        menu_window.show(screen, screen_width, screen_height, audio)