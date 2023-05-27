import pygame

# PUT INSIDE YOUR MAIN FOLDER!!!

#NECESSARY DATA!!
mod_name = "Cool Mod Name"
mod_description = "Cool Mod Description"
mod_author = "Such Cool Author"
visible_author = True
mod_text_color = (255,0,255)

def create(curState):
    import main
    # This function will get called once, when a state is created. WARNING: Returning any value will NOT do anything.
    print(curState)


def update(curState):
    import main
    # This function will get called every frame of a state. WARNING: Returning any value will NOT do anything.
    pass