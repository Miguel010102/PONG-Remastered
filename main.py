import pygame
import importlib
import sys
from typing import *
import os
from pygame import *
from functools import cache
import webbrowser
from psutil import Process

allowed_mods = False
curState = "none"

# mod handling
@cache
def load_mods():
    loaded_mods = []
    for file in os.listdir("."):
        if file.endswith(".py") and file != "main.py" and os.path.isfile(os.path.join(".", file)):
            allowed_mods = True
            mod_data = {}
            with open(file, "r") as f:
                exec(f.read(), mod_data)
            if "mod_name" in mod_data and "mod_description" in mod_data and "mod_author" in mod_data and "mod_text_color" in mod_data and "visible_author" in mod_data:
                mod_data["filename"] = file
                loaded_mods.append(mod_data)
    return loaded_mods

mods = load_mods()

mod_names = []
mod_descriptions = []
mod_authors = []
mod_text_colors = []
visible_authors = []

for mos in mods:
    mod_name = mos["mod_name"]
    mod_description = mos["mod_description"]
    mod_author = mos["mod_author"]
    mod_text_color = mos["mod_text_color"]
    visible_author = mos["visible_author"]
    mod_names.append(mod_name)
    mod_descriptions.append(mod_description)
    mod_authors.append(mod_author)
    mod_text_colors.append(mod_text_color)
    visible_authors.append(visible_author)
    
# Create a dictionary to store the imported modules
imported_modules = {}

allowed_mods = True

# Loop through the mods and import them
for mod in mods:
    if allowed_mods:
    # Check if the module has already been imported
        if mod["mod_name"] in imported_modules:
            continue

        # Get the filename without the ".py" extension
        filename = os.path.splitext(mod["filename"])[0]

        # Import the mod
        mod_module = importlib.import_module(filename)

        # Store the imported module in the dictionary
        imported_modules[mod["mod_name"]] = mod_module

#print(f"Mod names: {mod_names} mod_descriptions: {mod_descriptions} mod_authors: {mod_authors}")

loaded_mods = len(mod_names)
print(loaded_mods)

pygame.init()

screen_width = 700
screen_height = 500

display = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF, pygame.HWSURFACE)

iconx = 32 / 2
icony = 32 / 2

icon_surface = pygame.Surface((32, 32))

icon = pygame.draw.circle(icon_surface, (255, 255, 255), (iconx, icony), 15, 20)

pygame.display.set_caption("PONG: Remastered")
pygame.display.set_icon(icon_surface)

running = True

debug = False

clock = pygame.time.Clock()

middlex = 700 / 2
middley = 500 / 2

pady = middley - 70
maxby = 360
maxty = 0

ballx = middlex
bally = middley
oppady = pady
blaing = 0

speed = 10
ballspeed = 10

bombx = 0
bomby = 0

def get_memory_usage() -> float:
    process: Process = Process(os.getpid())
    megabytes: float = process.memory_info().rss / (1024 * 1024)
    return megabytes

def draw_text(surface, text, font_size, x, y, color):
    # create a font object
    font = pygame.font.Font(None, font_size)
    # create a text surface objects:
    text_surface = font.render(text, True, color)
    # get the size of the text surface
    text_rect = text_surface.get_rect()
    # center the text surface on the given coordinates
    text_rect.center = (x, y)
    # draw the text surface onto the given surface
    surface.blit(text_surface, text_rect)


def draw_button(surface, text, font_size, x, y, width, height, color):
    # create a button surface object
    button_surface = pygame.Surface((width, height))
    button_surface.fill((255, 255, 255))
    # create a font object
    font = pygame.font.Font(None, font_size)
    # create a text surface object
    text_surface = font.render(text, True, color)
    button_surface.blit(
        text_surface, text_surface.get_rect(center=(width / 2, height / 2))
    )
    # get the size of the button surface
    button_rect = button_surface.get_rect()
    # center the button surface on the given coordinates
    button_rect.center = (x, y)
    # draw the button surface onto the given surface
    surface.blit(button_surface, button_rect)
    # return the button object
    return button_rect


def game_over():
    global clock
    global middlex
    global running
    global pady
    global middley
    global maxby
    global maxty
    global ballx
    global bally
    global oppady
    global blaing
    global mods
    global curState
    global speed
    global ballspeed
    global debug
    running = True
    
    curState = "game_over"
    
    if allowed_mods:
        for mod in mods:
            mod = imported_modules[mod["mod_name"]]
            mod.create(curState)

    clock = pygame.time.Clock()
    middlex = 700 / 2
    middley = 500 / 2

    pady = middley - 70
    maxby = 360
    maxty = 0

    ballx = middlex
    bally = middley
    oppady = pady
    blaing = 0

    speed = 10
    ballspeed = 10

    bombx = 0
    bomby = 0

    while running:    
        display.fill((0, 0, 0))
        if allowed_mods:
            for mod in mods:
                mod = imported_modules[mod["mod_name"]]
                mod.update(curState)
        
        draw_text(display, "Game Over!", 40, middlex, middley - 160, (255, 255, 255))
        draw_text(
            display,
            "Press Enter to Restart!",
            40,
            middlex,
            middley + 160,
            (255, 255, 255),
        )
        for event in pygame.event.get():
            dt = clock.tick(60)
            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                main()
            match event.type:
                case pygame.QUIT: 
                    sys.exit()
            
        pygame.display.update()

def main():
    global clock
    global middlex
    global running
    global pady
    global middley
    global maxby
    global maxty
    global ballx
    global debug
    global bally
    global oppady
    global blaing
    global speed
    global ballspeed
    
    global mods
    global curState

    global bombx
    global bomby
    
    curState = "main"

    score = 0
    stamina = 140

    bombs = True

    font = pygame.font.Font(None, 230)
    
    if allowed_mods:
        for mod in mods:
            mod = imported_modules[mod["mod_name"]]
            mod.create(curState)

    while running:
        display.fill((0, 0, 0))
        
        if allowed_mods:
            for mod in mods:
                mod = imported_modules[mod["mod_name"]]
                mod.update(curState)
        
        if score != 64:
            font = pygame.font.Font(None, 230)
            scor = font.render(str(score), True, (255, 255, 255))
        else:
            font = pygame.font.Font(None, 140)
            scor = font.render("A Stack", True, (255, 255, 255))
        if debug:
            font = pygame.font.Font(None, 55)
            debugtext = font.render("VSpeed: " + str(blaing), True, (255, 255, 255))
            debugrect = debugtext.get_rect()
            debugrect.center = (110, 80)
        scor_rect = scor.get_rect()
        scor_rect.center = (middlex, middley)

        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        rect = pygame.draw.rect(display, (255, 255, 255), (20, pady, 30, 140))
        oprect = pygame.draw.rect(display, (255, 255, 255), (650, bally - 70, 30, 140))
        staminabar = pygame.draw.rect(display, (0, 255, 255), (20, 20, stamina, 30))
        draw_text(display, f'STAMINA: {str(stamina)}', 30, 90, 40, (255,255,255))
        display.blit(scor, scor_rect)
        if debug:
            display.blit(debugtext, debugrect)
        ball = pygame.draw.circle(display, (255, 255, 255), (ballx, bally), 15, 20)
        collide = rect.collidepoint(ballx, bally)
        collideop = oprect.collidepoint(ballx, bally)
        if score > 1 and blaing == 0:
            blaing = 1
        # bombx = random.randint(300,300)
        # bomby = random.randint(300,300)
        # if bombs:
        # bomb = pygame.draw.circle(display, (255,0,0), (bombx, bomby), 15, 20)
        # bombdrop = ball.collidepoint(bombx,bomby)
        # if bombdrop:
        # bombs = False
        if ballx < 15 or ballx > 700 - 15:
            if ballx < 20:
                game_over()
            else:
                ballspeed = -ballspeed
        if bally < 15 or bally > 500 - 15:
            blaing = -blaing
        if blaing > 20 or blaing == 20:
            blaing = 18
        if blaing < -20 or blaing == -20:
            blaing = -18
        if collide or collideop:
            # determine the direction the ball is moving
            direction = 1 if ballspeed > 0 else -1
            # calculate the angle of incidence (based on the location of the ball on the paddle)
            angle = ((bally - (pady + 70)) / 70) * 3.14159265359 / 3
            # calculate the new y velocity based on the angle of incidence and the direction of the ball
            if collide:
                blaing = int(direction * 10 * angle)
                ballspeed = -ballspeed
            else:
                blaing = int(direction * 5 * angle)
                # reverse the direction of the ball
                ballspeed = -ballspeed
        ballx -= ballspeed
        bally += blaing
        # rint(ballx)
        oppady = bally
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if keys[K_UP]:
            if pady > 0:
                if keys[K_LSHIFT] or keys[K_RSHIFT]:
                    pady += -speed - (stamina / 5)
                    if not stamina < 1:
                        stamina -= speed
                    # pady = 1
                else:
                    if pady > speed:
                        pady -= speed
        if keys[K_ESCAPE]:
            start()
        if keys[K_DOWN]:
            if pady < 355:
                if keys[K_LSHIFT] or keys[K_RSHIFT]:
                    pady += speed + (stamina / 5)
                    if not stamina < 1:
                        stamina -= speed
                    # pady = 355
                else:
                    pady += speed
                    # pady = 355
            else:
                if pady < 355 - speed:
                    pady += speed
                    # pady = 355

        if stamina != 140 and not keys[K_LSHIFT] and not keys[K_RSHIFT]:
            stamina += speed
        if ballx == 370:
            score += 1

        pygame.display.update()

def credits():
    global curState
    global mods
    global running

    # First type in the name, then put a space and n/ and the thing that they did! (the oversensitivity of the system is because if it wasnt like this, you wouldnt be able to place dots)
    credits = ["MiguelItsOut n/Made the remaster."]
    people = ["CreativePepper n/Gave Me Ideas", "timmychaan n/Supported me :)"]

    curState = "credits"

    if allowed_mods:
        for mod in mods:
            mod = imported_modules[mod["mod_name"]]
            mod.create(curState)

    while running:
        dt = clock.tick(60)
        
        display.fill((0, 0, 0))

        if allowed_mods:
            for mod in mods:
                mod = imported_modules[mod["mod_name"]]
                mod.update(curState)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        count = 0
        draw_text(display, "Credits", 80, middlex, (middley - 150), (255,255,255))
        count += 70
        for text in credits:
            split_text = text.split(" n/")
            draw_text(
                display,
                split_text[0],
                50,
                middlex - len(split_text[1]) * 8,
                (middley - 150) + count,
                (255, 255, 255),
            )
            draw_text(
                display,
                split_text[1],
                30,
                middlex + len(split_text[0]) * 10,
                (middley - 150) + count,
                (125, 125, 125),
            )
            count += 70
        draw_text(display, "Supporters", 80, middlex, (middley - 150) + count, (255,255,255))
        count += 70
        for text in people:
            split_text = text.split(" n/")
            draw_text(
                display,
                split_text[0],
                50,
                middlex - len(split_text[1]) * 8,
                (middley - 150) + count,
                (255, 255, 255),
            )
            draw_text(
                display,
                split_text[1],
                30,
                middlex + len(split_text[0]) * 10,
                (middley - 150) + count,
                (125, 125, 125),
            )
            count += 70
        draw_text(display, "<-- ESC", 40, 50, 20, (255, 255, 255))
        draw_text(display, "Thanks for the support!", 40, middlex, 20, (255, 255, 255))
        # count += 70
        draw_text(
            display,
            "You",
            50,
            middlex - len("For downloading!") * 8,
            (middley - 150) + count,
            (255, 255, 255),
        )
        draw_text(
            display,
            "For downloading!",
            30,
            middlex + len("You") * 10,
            (middley - 150) + count,
            (125, 125, 125),
        )
        pygame.display.update()
        if keys[K_ESCAPE]:
            start()
            
def modmenu(): 
    global running
    global middlex
    global middley
    global clock
    curState = "mods"
    
    clock = pygame.time.Clock()
    
    
    if allowed_mods:
        for mod in mods:
            mod = imported_modules[mod["mod_name"]]
            mod.create(curState)

    while running:
        if allowed_mods:
            for mod in mods:
                mod = imported_modules[mod["mod_name"]]
                mod.update(curState)
        offset = 70
        dt = clock.tick(60)
        pygame.display.update()
        display.fill((0,0,0))
        draw_text(display, "MOD SUPPORT IS BROKEN RIGHT NOW!", 30, middlex, middley - 140, (255,255,255))
        for i in mods:
            draw_text(display, i["mod_name"], 40, middlex, middley - offset, i["mod_text_color"])
            draw_text(display, i["mod_description"], 25, middlex + 20, middley - offset + 30, (255,255,255))
            if i["visible_author"]:
                draw_text(display, "Author: " + i['mod_author'], 25, middlex + 200 + len(i["mod_description"]) + len(i["mod_author"]), middley - offset + 30, (255,255,255))
            offset -= 70
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                    sys.exit()
        if keys[K_ESCAPE]:
            start()

# HIT X 370
def start():
    global clock
    global middlex
    global running
    global pady
    global middley
    global curState
    global maxby
    global maxty
    global ballx
    global bally
    global oppady
    global blaing
    global speed
    global ballspeed
    curState = "title"

    running = True

    clock = pygame.time.Clock()
    middlex = 700 / 2
    middley = 500 / 2

    pady = middley - 70
    maxby = 360
    maxty = 0

    ballx = middlex
    bally = middley
    oppady = pady
    blaing = 0

    speed = 10
    ballspeed = 10

    bombx = 0
    bomby = 0

    curselected = 0
    down_pressed = False
    up_pressed = False

    url = "https://www.google.com/"

    if allowed_mods:
        for mod in mods:
            mod = imported_modules[mod["mod_name"]]
            mod.create(curState)

    while running:
        if allowed_mods:
            for mod in mods:
                mod = imported_modules[mod["mod_name"]]
                mod.update(curState)

        btn1 = (255, 255, 255)
        btn2 = (255, 255, 255)
        btn3 = (255, 255, 255)

        dt = clock.tick(60)

        font = pygame.font.Font(None, 36)
        fonte = pygame.font.Font(None, 60)

        #    Render the text
        text_surface = font.render("PONG Remastered", True, (255, 255, 255))

        # Set the position of the text on the screen
        text_rect = text_surface.get_rect()
        text_rect.center = (middlex, 80)

        pygame.display.update()

        # Draw the text onto the scree
        display.fill((0, 0, 0))
        display.blit(text_surface, text_rect)
        pygame.draw.circle(display, (255, 255, 255), (middlex, middley - 50), 70, 70)
        selected_color = (255, 255, 255)
        unselected_color = (128, 128, 128)

        unavailable_color = (255, 0, 0)
        unavailable_selected = (125, 0, 0)

        # draw buttons with selected and unselected colors based on "curselected" variable
        draw_text(
            display,
            "Play",
            60,
            middlex - 200,
            middley + 150,
            selected_color if curselected == 0 else unselected_color,
        )
        draw_text(
            display,
            "Mod",
            60,
            middlex,
            middley + 150,
            selected_color if curselected == 1 else unselected_color,
        )
        draw_text(
            display,
            "Settings",
            60,
            middlex + 200,
            middley + 150,
            unavailable_color if curselected == 2 else unavailable_selected,
        )
        draw_text(
            display,
            "Credits",
            60,
            middlex,
            middley + 200,
            selected_color if curselected == 3 else unselected_color,
        )

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if (
            keys[K_LEFT] and not left_pressed
        ):  # check if left key is pressed and wasn't previously pressed
            if curselected > 0 and curselected < 4:
                curselected -= 1
            else:
                curselected = 3
            left_pressed = True  # set left_pressed flag to True
        elif not keys[K_LEFT]:  # check if left key is released
            left_pressed = False  # reset left_pressed flag

        if (
            keys[K_RIGHT] and not right_pressed
        ):  # check if right key is pressed and wasn't previously pressed
            if curselected < 3:
                curselected += 1
            else:
                curselected = 0
            right_pressed = True  # set right_pressed flag to True
        elif not keys[K_RIGHT]:  # check if right key is released
            right_pressed = False  # reset right_pressed flag

        if keys[K_DOWN] and not down_pressed:
            curselected = 3
            down_pressed = True
        elif not keys[K_DOWN]:
            down_pressed = False

        if keys[K_UP] and not up_pressed:
            curselected = 1
            up_pressed = True
        elif not keys[K_UP]:
            up_pressed = False

        if keys[K_RETURN]:
            match curselected:
                case 0:
                    main()
                case 1:
                    modmenu()
                case 2:
                    pass
                case 3:
                    credits()
                case _:
                    print("Invalid selection")
                

    # main()


start()
