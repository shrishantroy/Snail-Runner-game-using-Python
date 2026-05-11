import pygame as pg
from sys import exit
from random import randint
pg.init()

screen = pg.display.set_mode((800,400))
pg.display.set_caption("Snail Runner")
sky_surface = pg.image.load("Sky.png").convert()
ground_surface = pg.image.load("ground.png").convert()
clock = pg.time.Clock()
fps = 60 

font = pg.font.Font("PixelType.ttf",50)
font3 = pg.font.Font("PixelType.ttf",80)

font_surface = font3.render("Snail Runner",False,(64,64,200))
font_surface_rect = font_surface.get_rect(center = (400,100) )

snail1 = pg.image.load("snail1.png").convert_alpha()
fly1 = pg.image.load('Fly1.png').convert_alpha()
snail2 = pg.image.load("snail2.png").convert_alpha()
fly2 = pg.image.load('Fly2.png').convert_alpha()
snail_list = [snail1,snail2]
fly_list = [fly1,fly2]
snail_index = 0
fly_index = 0

player_stand = pg.image.load('player_stand.png').convert_alpha()
player_stand_game = player_stand
player_stand = pg.transform.rotozoom(player_stand,0,1.5)
player_stand_rect = player_stand.get_rect(bottom = 232)

player_walk_1 = pg.image.load("player_walk_1.png").convert_alpha()
player_walk_2 = pg.image.load("player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pg.image.load('jump.png')
player_pos = 250
player = player_stand_game
player_rect = player.get_rect(midbottom = (player_pos,232))

jump_sound = pg.mixer.Sound('jump.mp3')
background_sound = pg.mixer.Sound('music.wav')
background_sound.play(loops = -1)


score_surface = font.render("Score: ",False,(64,64,64))
score_surface_rect = score_surface.get_rect(center = (600,50))


intro_text = font.render("Press Space to play",False,'Black')
intro_text_rect = intro_text.get_rect(center = (400,200))

gover_surface = font.render("GAME OVER!",False,(255,50,50))
gover_rect  = gover_surface.get_rect(center = (400,100))

Time_surf = font.render("Time: ",False,'Red')
Time_rect = Time_surf.get_rect(top = score_surface_rect.bottom,left = score_surface_rect.left)

font2 = pg.font.Font("PixelType.ttf",30)
font2_text = font2.render("Press space to go to main menu",False,(0,0,255))
font2_text_rect = font2_text.get_rect(top = gover_rect.bottom,left = gover_rect.left)

player_gravity = 0
speed = 0
state = 2
score = 0
snail_initial_speed = 1
snail_speed = snail_initial_speed
fly_initial_speed = 2
fly_speed = fly_initial_speed

obstacle_timer = pg.USEREVENT + 1
time_int = 5000
pg.time.set_timer(obstacle_timer,time_int)
walk_timer = pg.USEREVENT + 2
snail_timer = pg.USEREVENT + 3
fly_timer = pg.USEREVENT + 4
pg.time.set_timer(snail_timer,150)
pg.time.set_timer(fly_timer,150)

while True:
    
    if state == 2:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,232))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(intro_text,intro_text_rect)
        screen.blit(font_surface,font_surface_rect)
        obstacle_rect_list = []
    
        start_time = pg.time.get_ticks()/1000

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    state = 1
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            
    elif state == 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and player_rect.bottom>=232:
                    player_gravity = -10
                    jump_sound.play()
                if event.key == pg.K_RIGHT:
                    pg.time.set_timer(walk_timer,150)
                    speed = 5
                if event.key == pg.K_LEFT:
                    pg.time.set_timer(walk_timer,150)
                    speed = -5
                if event.key == pg.K_DOWN:
                    player_gravity = 10
            
            if event.type == pg.KEYUP:
                speed = 0
                pg.time.set_timer(walk_timer,0)
            if event.type == obstacle_timer:
               if randint(0,1) == 0:
                    obstacle_rect_list.append(
                    {
                        'rect': snail.get_rect(midbottom = (randint(900,1400),232)),
                        'Passed' : False,
                        'Type' : 'Snail'
                    }
                    )
               else:
                    obstacle_rect_list.append(
                        {
                            'rect' : fly.get_rect(midbottom = (randint(900,1400),210)),
                            'Passed' : False,
                            'Type' : 'Fly'
                        }
                    )
            if event.type == walk_timer:
                if player_index == 0:
                    player_index = 1
                else:
                    player_index = 0
            if event.type == snail_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
            if event.type == fly_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                
        snail = snail_list[snail_index]
        fly = fly_list[fly_index]

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,232))

        if obstacle_rect_list:
            for obs_rect in obstacle_rect_list:
                if obs_rect['Type'] == 'Snail':
                    obs_rect['rect'].right -= snail_speed
                    screen.blit(snail,obs_rect['rect'])
                else:
                    obs_rect['rect'].right -= fly_speed
                    screen.blit(fly,obs_rect['rect'])


                if player_rect.left >= obs_rect['rect'].right and obs_rect['Passed'] == False:
                    score += 1
                    obs_rect['Passed'] = True
                if player_rect.colliderect(obs_rect['rect']) == True:
                    state = 0

            obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle['rect'].right>=0]

        score_val = font.render(str(score),False,'Black')
        score_val_rect = score_val.get_rect(left = score_surface_rect.right,bottom = score_surface_rect.bottom)
        screen.blit(score_val,score_val_rect)
        
        screen.blit(Time_surf,Time_rect)
        time = round(pg.time.get_ticks()/1000 - start_time)
        Time_val = font.render(str(time),False,'Red')
        Time_val_rect = Time_val.get_rect(left = Time_rect.right,bottom = Time_rect.bottom)
        screen.blit(Time_val,Time_val_rect)
       
        
        player_rect.bottom += player_gravity
        player_gravity += 0.3

        if player_rect.right >= 800 and speed>0:
            speed = 0
        if player_rect.left<=0 and speed<0:
            speed = 0
        
        player_rect.right += speed    
        

        if speed != 0:
            player = player_walk[player_index] 
        if speed == 0:
            player = player_stand_game
        if player_rect.bottom<232:
            player = player_jump
        
        if player_rect.bottom >= 232:
            player_gravity = 0
            player_rect.bottom = 232
        player_rect = player.get_rect(center = player_rect.center)
        screen.blit(player,player_rect)
    
        
        pg.draw.rect(screen,'#c0e8ec',score_surface_rect)
        pg.draw.rect(screen,'#c0e8ec',score_surface_rect,20)
        screen.blit(score_surface,score_surface_rect)
       
       
    else:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,232))
        screen.blit(player,player_rect)
        screen.blit(gover_surface,gover_rect)
        screen.blit(font2_text,font2_text_rect)
        screen.blit(score_surface,score_surface_rect)
        screen.blit(score_val,score_val_rect)
        screen.blit(Time_surf,Time_rect)
        screen.blit(Time_val,Time_val_rect)

        for obs_rect in obstacle_rect_list:
            if obs_rect['Type'] == 'Snail':
                screen.blit(snail,obs_rect['rect'])
            else:
                screen.blit(fly,obs_rect['rect'])

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    player_rect.left = 0
                    state = 2
                    player_gravity = 0
                    speed = 0
                    score = 0
                    snail_speed = snail_initial_speed

            if event.type == pg.QUIT:
                pg.quit()
                exit()


    pg.display.update()
    clock.tick(fps)