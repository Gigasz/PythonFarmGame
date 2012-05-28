'''
Created on 23-05-2012

@author: orneo1212
'''
import pygame

from seed import Seed

def draw_tools(surface, currenttool, currentseed, imgloader,
               drawnearcursor = True):
    #Draw selection on selected tool
    if currenttool == 'harvest':
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, 48, 48), 1)
    if currenttool == 'plant':
        pygame.draw.rect(surface, (255, 255, 255), (60, 10, 48, 48), 1)
    if currenttool == 'watering':
        pygame.draw.rect(surface, (255, 255, 255), (110, 10, 48, 48), 1)
    if currenttool == 'shovel':
        pygame.draw.rect(surface, (255, 255, 255), (160, 10, 48, 48), 1)
    if currenttool == 'pickaxe':
        pygame.draw.rect(surface, (255, 255, 255), (210, 10, 48, 48), 1)
    if currenttool == 'axe':
        pygame.draw.rect(surface, (255, 255, 255), (260, 10, 48, 48), 1)

    mx, my = pygame.mouse.get_pos()

    if drawnearcursor:
        img = None
        #Draw current tool
        if currenttool == "plant":
            #draw seed only when correct is selected
            if currentseed == None:
                img = None
            else:
                img = imgloader.loadimage('seed' + str(currentseed))
        if currenttool == "harvest":
            img = imgloader.loadimage('sickle')
        if currenttool == "watering":
            img = imgloader.loadimage('wateringcan')
        if currenttool == "shovel":
            img = imgloader.loadimage('shovel')
        if currenttool == "pickaxe":
            img = imgloader.loadimage('pickaxe')
        if currenttool == "axe":
            img = imgloader.loadimage('axe')
        if img:
            surface.blit(img, (mx, my - 48))

    #draw tools
    #SICKLE Harvest (10,10,48,48)
    #PLANT (60,10,48,48)
    surface.blit(imgloader.loadimage('sickle'), (10, 10))
    surface.blit(imgloader.loadimage('plant'), (60, 10))
    surface.blit(imgloader.loadimage('wateringcan'), (110, 10))
    surface.blit(imgloader.loadimage('shovel'), (160, 10))
    surface.blit(imgloader.loadimage('pickaxe'), (210, 10))
    surface.blit(imgloader.loadimage('axe'), (260, 10))

def draw_seed(surface, seedid, position, imgloader):
        img = imgloader.loadimage('seed' + str(seedid))
        surface.blit(img, position)

def draw_selected_seed(surface, selectedseed, imgloader):
    if  selectedseed == None:return
    #draw selected seed
    img = imgloader.loadimage('dryground')
    surface.blit(img, (65, 65))
    draw_seed(surface, selectedseed, (65, 65), imgloader)

def render_seed_notify(surface, font, posx, posy, farmobject, farmtile,
                       imgloader):
    """Render notification about farm object"""

    if farmobject is None:return

    sizex = 250
    sizey = 150
    posy += 5

    img = pygame.Surface((sizex, sizey))
    img.fill((48, 80, 80))
    pygame.draw.rect(img, (255, 255, 255), (0, 0, sizex - 1, sizey - 1), 1)

    #half of the tooltip width
    halfx = sizex / 2

    #name
    text = "" + farmobject.name + ""
    text = font.render(text, 0, (255, 255, 0), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (halfx - text.get_size()[0] / 2, 5))

    #Descriptions
    text = "" + farmobject.descriptions + ""
    text = font.render(text, 0, (255, 240, 40), (255, 0, 255))
    text.set_colorkey((255, 0, 255))
    img.blit(text, (halfx - text.get_size()[0] / 2, 25))

    #Draw Seed info
    if farmobject.type == "seed":
        #Draw seed
        draw_seed(img, farmobject.id, (sizex / 2 - 32, 100), imgloader)
        #remaining time
        text = "Complete in: " + farmobject.remainstring
        text = font.render(text, 0, (255, 0, 100), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (halfx - text.get_size()[0] / 2, 45))

        #Quentity
        text = "Quantity: " + str(farmobject.growquantity)
        text = font.render(text, 0, (255, 255, 150), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (halfx - text.get_size()[0] / 2, 65))

        #Water
        text = "Water: " + str(farmtile["water"]) + " %"
        text = font.render(text, 0, (0, 128, 255), (255, 0, 255))
        text.set_colorkey((255, 0, 255))
        img.blit(text, (halfx - text.get_size()[0] / 2, 85))

        #ready to harvest
        if farmobject.to_harvest:
            text = font.render("Ready to Harvest", 0, \
                               (255, 255, 255), (255, 0, 255))
            text.set_colorkey((255, 0, 255))
            img.blit(text, (halfx - text.get_size()[0] / 2, sizey - 20))

    #alpha
    img.set_alpha(128 + 64)
    if posx > 400:posx -= sizex
    surface.blit(img, (posx, posy))


def render_field(imgloader, farmfield, farmoffset):
    mainimg = pygame.surface.Surface((800, 600))

    #background
    mainimg.blit(imgloader['background'], (0, 0))

    for y in range(12):
        for x in range(12):
            farmtile = farmfield.get_farmtile(x, y)

            posx = (x - y) * 32 + farmoffset[0] + 150
            posy = (x + y) * 16 + farmoffset[1]

            rect = (posx, posy, 64, 32)

            #draw ground
            if farmtile['water'] > 20:
                img = imgloader['wetground']
            else:
                img = imgloader['dryground']
            mainimg.blit(img, rect)

            #draw grid
            mainimg.blit(imgloader['grid'], rect)

            #draw plant or seed
            farmobject = farmtile['object']

            #Avoid draw Null fieldobjects
            if not farmobject:continue

            if isinstance(farmobject, Seed):
                #not ready to harvest
                if not farmobject.to_harvest:
                    if not farmobject.wilted:
                        farmobject.update_remainig_growing_time()
                        #draw seeds on the ground
                        if farmobject.growtimeremaining <= 30 * 60:
                            img = imgloader['seedfullgrow']
                        elif farmobject.growtimeremaining <= 60 * 60:
                            img = imgloader['seedhalfgrow']

                        else:
                            img = imgloader['seed']
                    #seed is wilted
                    else:
                        img = imgloader['wiltedplant']
                #ready to harvest
                else:
                    img = imgloader['seed' + str(farmobject.id)]
            #Field object
            else:
                img = imgloader['object' + str(farmobject.id)]

            #Draw gield image
            if img:mainimg.blit(img, rect)
    #return mainimg object
    return mainimg
