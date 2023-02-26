# BHBot

[Этот файл доступен на Русском языке](README_RU.md)

Gold/XP farming bot for Brawlhalla

Heavily inspired by [BrawlhallaEZ](https://github.com/jamunano/BrawlhallaEZ)

### -------------------------------------------------------------------

### BOT IS NO LONGER ACTIVELY MAINTAINED!

#### (you can still leave [issues](https://github.com/sovamorco/bhbot/issues) and some will be addressed)

### -------------------------------------------------------------------

**WARNING:** Bot was initially made for personal use. It should not, but still can cause some unexpected consequences, including making purchases from mallhalla (with in-game currencies). Developer is
not responsible for any harm the program may case. Use at your own risk

(it should work fine tho, I tested it for >600 hours at this point)

# Installation
Latest release can always be downloaded [here](https://sovamor.co/bhbot)

Bot _should_ auto-update as soon as any updates are released according to selected branch in settings

# Features

- Works completely in background
- Sends inputs directly to Brawlhalla to not disturb you
- Automatically launches the game
- Automatically creates/sets up lobby
- Automatically picks/changes character and game duration
- Automatically detects and resets xp limit
- Supports custom modes
- Supports custom languages
- Even supports custom fonts
- ~~Brews you coffee~~ (only tea supported for now)

# Usage
Should be pretty straightforward. Just select needed settings and click "Start" :)

# Limitations
- Bot requires "Collapse crossovers" to be set to Yes. If you think it should automatically set it to be so, please [open an issue](https://github.com/sovamorco/bhbot/issues)
- Bot requires ingame language to be set to English. If you think it should automatically set it to be so, please [open an issue](https://github.com/sovamorco/bhbot/issues)

# Internal stuff
You can always check the code, but basically bot uses windows SendMessage API to send inputs directly to Brawlhalla window and pixel detection to detect states and
decide what to do at any given point

You can use BrawlhallaBot class directly or write your own wrapper for it. It should be completely independent and gui.py is just a PySimpleGUI graphical wrapper
