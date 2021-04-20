# BHBot
Gold/XP farming bot for Brawlhalla

Heavily inspired by [BrawlhallaEZ](https://github.com/jamunano/BrawlhallaEZ)


**WARNING:** Bot was initially made for personal use.
It should not, but still can cause some unexpected consequences, including making purchases from mallhalla (with in-game currencies).
Developer is not responsible for any harm the program may case. Use at your own risk

(it should work fine tho, I tested it for >500 hours at this point)

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

# Installation
Latest release can always be downloaded [here](https://sovamor.co/bhbot)

Bot will auto-update as soon as any updates are released according to selected branch in settings

# Usage
Should be pretty straightforward. Just select needed settings and click "Start" :)

# Limitations
As of now, bot works ONLY on 1920x1080 screens. If you want to request support for any other resolution, please [open an issue](https://github.com/sovamorco/bhbot/issues)

# Internal stuff
You can always check the code, but basically bot uses windows SendMessage API to send inputs directly to Brawlhalla window and pixel detection to detect states and
decide what to do at any given point

You can use BrawlhallaBot class directly or write your own wrapper for it. It should be completely independent and gui.py is just a wrapper for it
