import pygame
import time
import random
from math import sqrt
from sklearn.cluster import KMeans
pygame.init()
 
white = (255, 255, 255)
white2 = (245,222,179)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
cyan = (0, 255, 255)
magenta = (255, 0, 255)


dis_width = 900
dis_height = 600
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('k')
dot_size = 5
clock = pygame.time.Clock()
panel = [50,50,400,400]
outline = [45,45,410,410]
render_pos = [500, 50]
button_render_dots = [500, 50, 150, 50]
button_render_color_dots = [500, 250, 150, 50]
excecuse_button = [500, 400, 150, 50]
algorithm_button = [500, 500, 150, 50]
excecuse_button_pos = [500, 400]
algorithm_button_pos = [500, 500]

minus_pos = [700,100]
plus_pos = [760,100]
minus_color_pos = [700,250]
plus_color_pos = [760,250]
minus_button = [minus_pos[0], minus_pos[1], 50, 50]
plus_button = [plus_pos[0], plus_pos[1] , 50, 50]
minus_color_button = [minus_color_pos[0], minus_color_pos[1], 50, 50]
plus_color_button = [plus_color_pos[0], plus_color_pos[1] , 50, 50]
num_dot_pos = [500, 100]
num_dot_color_pos = [500, 300]
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
def draw_text(text:str, pos):
    value = score_font.render(f"{text}", True, black)
    dis.blit(value, pos)


def num_dots_text(num):
    value = score_font.render("Amount: " + str(num), True, black)
    dis.blit(value, num_dot_pos)

def num_dots_color_text(num):
    value = score_font.render("Amount Color: " + str(num), True, black)
    dis.blit(value, num_dot_color_pos)

def get_random_dots(num):
    dots = []
    for i in range(num):
        dot = (random.randint(50,450),random.randint(50,450))
        dots.append(dot)
    return dots

def get_random_color_dots(num):
    dots = []
    for i in range(num):
        dot = (random.randint(50,450),random.randint(50,450))
        dots.append(dot)
    return dots


def draw_random_dots(list_dots):
    for i in range(len(list_dots)):
        pygame.draw.circle(dis,black,list_dots[i],dot_size)



def draw_random_match_dots(list_dots, list_closest):
    colors = [green,red,yellow,magenta]
    for i in range(len(list_dots)): 
        pygame.draw.circle(dis,colors[list_closest[i]],list_dots[i],dot_size)

def draw_random_color_dots(list_dots):
    colors = [green,red,yellow,magenta]
    for i in range(len(list_dots)):
        pygame.draw.circle(dis,black,list_dots[i],dot_size+2)
        pygame.draw.circle(dis,colors[i],list_dots[i],dot_size+1)



def find_distance(color_dots,black_dots):
    pos = []
    for dot in black_dots:
        distances = []
        for cdot in color_dots:
            distances.append(sqrt((cdot[0]-dot[0])**2 + (cdot[1]-dot[1])**2))
        pos.append(distances.index(min(distances)))
    return pos
                

def find_new_color_pos(closest_dot_pos, black_dots,color_dots):
    new_list = []
    for i in range(len(color_dots)):
        sum_x = sum_y = count = 0
        for j in range(len(black_dots)):
            if closest_dot_pos[j] == i:
                sum_x+= black_dots[j][0]
                sum_y+= black_dots[j][1]
                count +=1 
        new_color_pos_x = sum_x//count
        new_color_pos_y = sum_y//count
        new_list.append([new_color_pos_x, new_color_pos_y])
    return new_list



def gameLoop():
    dots_draw = []
    dots_color_draw = []
    running = True
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    dots_count = 20
    dots_color_count = 0
    list_closest = []
    color_math = False
    while running:

        dis.fill(white)
        # draw rect 
        panel_space = pygame.draw.rect(dis,black,outline)
        panel_space = pygame.draw.rect(dis,white2,panel)
        render_dot = pygame.draw.rect(dis,red,button_render_dots)
        render_color_dot = pygame.draw.rect(dis,red,button_render_color_dots)
        render_excecuse = pygame.draw.rect(dis,red,excecuse_button)
        algorithm = pygame.draw.rect(dis,red,algorithm_button)
        minus = pygame.draw.rect(dis,blue,minus_button)
        plus = pygame.draw.rect(dis,blue,plus_button)
        minus_color_dot = pygame.draw.rect(dis,blue,minus_color_button)
        plus_color_dot = pygame.draw.rect(dis,blue,plus_color_button)
        # draw text
        
        draw_text("Run",excecuse_button_pos)
        draw_text("algorithms",algorithm_button_pos)
        draw_text("-",minus_pos)
        draw_text("+",plus_pos)
        draw_text("Render",render_pos)
        draw_text("Color Dot",[render_pos[0],render_pos[1]+200])
        draw_text("-",[render_pos[0]+220,render_pos[1]+200])
        draw_text("+",[render_pos[0]+270,render_pos[1]+200])

        num_dots_text(dots_count) 
        num_dots_color_text(dots_color_count)       
        if dots_count <= 0:
            dots_count = 0
        if dots_color_count < 0 or dots_color_count > 4:
            dots_color_count = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if algorithm.collidepoint(pos):
                    if dots_color_count == 0:
                        ...
                    else:
                        kmeans = KMeans(n_clusters=dots_color_count).fit(dots_draw)
                        dots_color_draw = kmeans.cluster_centers_

                if panel_space.collidepoint(pos):
                    dots_draw.append(pos)
                if minus.collidepoint(pos):
                    dots_count-=1
                if plus.collidepoint(pos):
                    dots_count+=1
                if render_dot.collidepoint(pos):
                    color_math = False
                    dots_draw = get_random_dots(dots_count)
                if minus_color_dot.collidepoint(pos):
                    dots_color_count-=1
                if plus_color_dot.collidepoint(pos):
                    dots_color_count+=1
                if render_color_dot.collidepoint(pos):
                    dots_color_draw = get_random_color_dots(dots_color_count)
                if render_excecuse.collidepoint(pos):
                    try:
                        color_math = True
                        list_closest = find_distance(dots_color_draw,dots_draw)
                        dots_color_draw = find_new_color_pos(list_closest,dots_draw,dots_color_draw)
                    except:
                        ...
        try:
            if color_math:
                draw_random_match_dots(dots_draw, list_closest)
            else:
                draw_random_dots(dots_draw)
            draw_random_color_dots(dots_color_draw)
        except:
            ...

 
        pygame.display.update()
 
        clock.tick(30)
 
    pygame.quit()
    quit()
 
 
gameLoop()