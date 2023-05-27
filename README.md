# PONG-Remastered
-- Mod support is there but is kindda MEEHHH --

# Modding

There are 2 ways of modifying the game.

First of all, you can use the built-in mod support to compile mods to the main game.

- You will find examples of how to use the built-in mod support in the "mod_examples" folder.

---

Or, you can modify the game directly by modifying the main.py file.

- You can basically modify anything using this.

# Compiling The Game
(WITHOUT MODS):

1 - Make sure you have the latest version of pyinstaller using "pip install pyinstaller" and the latest pip version.

2 - Open up CMD in the folder with the main.py inside of it.

3 - Copy this into the command line and run it: "pyinstaller main.py --windowed --onefile"

(WITH MODS):

1 - Make sure you have the latest version of pyinstaller using "pip install pyinstaller" and the latest pip version.

2 - Open up CMD in the folder with the main.py inside of it.

3 - Copy this into the command line and run it:

    "pyinstaller main.py --windowed --onefile --add-data "mods/*.py;mods/" "