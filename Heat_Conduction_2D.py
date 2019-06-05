# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:28:01 2019

@author: WilmesD
"""

import pygame
import numpy as np

            
xmax = 400
ymax = 400
coord_x, coord_y = np.mgrid[:xmax,:ymax]

def draw_circle(x,y,r,array,temperature):
    circle = (coord_x - x) ** 2 + (coord_y - y) ** 2     
    donut = (circle < r) * temperature
    array[:,:,0] = np.where(donut>0,donut,array[:,:,0])
    return array

def divergence(f):
    num_dims = len(f)
    return np.ufunc.reduce(np.add, [np.gradient(f[i], axis=i) for i in range(num_dims)])
    
pygame.init()
logo = pygame.image.load("dog.jpg")
pygame.display.set_icon(logo)
pygame.display.set_caption("Heat Condunction 2D")

display = pygame.display
surface = pygame.display.set_mode((xmax,ymax))
#surface.set_at((200,100), (255,0,0,0))
#display.flip()
#print(surface.get_at((2,2)))
dt = pygame.time.Clock()
dt.tick(30)
mouse_position = (0,0)
mouse_buttons = (False, False, False)
conductance = 1*np.ones((xmax,ymax), dtype=np.float16)
conductance[:,200:] = 30
conductance[200:,:] = 10
conductance[200:,200:] = 20
temp_save = np.zeros([xmax,ymax,3],dtype=np.float32)
current_temp = np.zeros([xmax,ymax,3], dtype=np.float32)
Gradient_field = np.zeros([xmax,ymax], dtype=np.float32)
Divergence_fieldx = np.zeros([xmax,ymax], dtype=np.float16)
Divergence_fieldy = np.zeros([xmax,ymax], dtype=np.float16)
running = True
#    pygame.draw.circle(surface, (255,0,0,0), (100,100), 30)
#main loop
#px = pygame.PixelArray(surface)
#current_temp = surface.unmap_rgb(px[1,1])[0]

draw_circle(xmax/2,ymax/2,1000,current_temp,255)
while running:
    if mouse_buttons[0] == True:
        draw_circle(mouse_position[0],mouse_position[1],200,current_temp,255)
    #            pygame.draw.circle(surface, (255,0,0,0), mouse_position, 10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
#            print(surface.get_at(mouse_position))
    #                print(len(Gradient_field))
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_buttons = pygame.mouse.get_pressed()
            
            
    Gradient_field = np.gradient(current_temp[:,:,0])
    Divergence_fieldx = np.gradient(Gradient_field[0])
    Divergence_fieldy = np.gradient(Gradient_field[1])
    
#    div = conductance * dt.get_time()/1000 * (Divergence_fieldy[0] + Divergence_fieldy[1] + Divergence_fieldx[0] + Divergence_fieldx[1])/4
    div = divergence(Gradient_field) * conductance * dt.get_time()/1000
#    div = np.clip(div, 0, 255)
    current_temp[:,:,0] = current_temp[:,:,0] + div
    current_temp[0,:,0] = 0
    current_temp[:,0,0] = 0
    current_temp[xmax-1,:,0] = 0
    current_temp[:,ymax-1,0] = 0
#    current_temp[:,:,0] = temp_save[:,:,0]
    
    
    
    #Heat conduction
#    for x in range(xmax):
#        for y in range(ymax):
#            temp = np.float64(current_temp[x,y,0])
#            #current_temp[x,y,0]
#            #calculate divergence
#            if x > 0 and x < xmax-1 and y > 0 and y < ymax-1:
#                divx = (temp - current_temp[x+1,y,0] + temp - current_temp[x-1,y,0])/2
#                divy = (temp - current_temp[x,y+1,0] + temp - current_temp[x,y-1,0])/2
#    #            divx = (temp - current_temp[i+1,j,0] + temp - current_temp[i-1,j,0])/2
#    #            divy = (temp - current_temp[i,j+1,0] + temp - current_temp[i,j-1,0])/2
#                divxy = (temp - current_temp[x+1,y+1,0] + temp - current_temp[x-1,y-1,0])/2
#                divyx = (temp - current_temp[x-1,y+1,0] + temp - current_temp[x+1,y-1,0])/2
#                #calculate new temp and save in temporary array
#                temp_save[x,y,0] = temp - (divx+divy+divxy+divyx)/8 * conductance  
#    current_temp = np.uint8(temp_save)
    pygame.surfarray.blit_array(surface,np.uint8(current_temp))
    display.flip()
            
    
    
    
    
    