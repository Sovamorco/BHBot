LANGUAGE = 'English'

LAYOUT_MAPPING = {
    # Main window
    'main_window_title': 'BHBot',
    'title': 'BHBot by Sovamorco',
    'version': 'Version: {0.APP_VERSION}',
    'press_start': ['Press "Start" to start the bot', 'Press "Stop" to stop the bot'],
    'toggle': ['Start', 'Stop'],
    'delayed_stop': ['Delayed Stop', 'Cancel Stop'],
    'settings': 'Settings',
    'instructions': 'Instructions',
    'exit': 'Exit',
    'test': 'Test',
    'update_available_title': 'Update available!',
    'update_available_version': 'New version: {0.new_version.version}',
    'update_available_button': 'Update',
    # Settings window
    'settings_window_title': 'Settings',
    'settings_title': 'Settings',
    'settings_help': 'For extra information hover above settings',
    'language_name_text': 'Language: ',
    'font_text': 'Font: ',
    'autostart_text': 'Automatically start the bot: ',
    'branch_text': 'Update channel: ',
    'debug_text': 'Print debug info: ',
    'mode_name_text': 'Mode: ',
    'character_text': 'Character: ',
    'duration_text': 'Duration: ',
    'auto_stop_text': 'Automatic xp limit reset: ',
    'auto_detect_auto_stop_text': 'Automatic xp limit detection: ',
    'auto_stop_frequency_text': 'Reset frequency (hours): ',
    'auto_stop_duration_text': 'Reset wait duration (minutes): ',
    'bots_text': 'Bots amount: ',
    'stealth_text': 'Stealth-mode (hidden game window): ',
    'mute_text': 'Disable sound: ',
    'hotkey_settings': 'Hotkey settings',
    'save': 'Save',
    'back': 'Back',
    # Hotkeys settings window
    'hotkeys_window_title': 'Hotkeys',
    'hotkeys_title': 'Hotkeys',
    'up_text': 'Jump + Aim Up',
    'left_text': 'Left',
    'down_text': 'Down',
    'right_text': 'Right',
    'throw_text': 'Throw',
    'quick_text': 'Light attack',
    'dodge_text': 'Dodge',
    'heavy_text': 'Heavy attack',
    # Instructions window
    'instructions_window_title': 'Instructions',
    'instructions_contents': ['Bot usage instructions:',
                              '1. VERY IMPORTANT\n'
                              'Either use stealth mode option in the bot, or DO NOT disturb the bot in any way. '
                              'Moving the mouse over Brawlhalla window, resizing or moving window itself or using your keyboard with Brawlhalla in focus '
                              'while the bot is working may cause unexpected consequences '
                              'like picking wrong characters or even making purchasese in Mallhalla or in Battle pass. '
                              'If you notice that you accidentally moved something, restart the bot (but better use stealth mode, really)',
                              '2. Make sure your ingame language is set to English',
                              '3. Make sure "Collapse crossovers" setting is enabled',
                              '4. Put game into windowed if bot doesn\'t do so automatically',
                              '5. Configure everything else as you prefer and click "Start"',
                              'Enjoy c:'],
    # Popups
    'changelog_popup_title': 'Changelog',
}

TOOLTIPS = {
    # Main window
    'delayed_stop': [
        'Stop the bot after finishing current game or before starting new one',
        'Cancel any queued stops',
    ],
    # Settings window
    'settings_help': '\n     :)     \n',
    'language_name_column': 'Choose a language (automatically updates)',
    'font_column': 'Choose a font (automatically updates)',
    'autostart_column': 'Automatically start the bot if the program is running and you are not playing Brawlhalla\n'
                        'Checks every 5 minutes',
    'branch_column': 'Beta may have experimental and unstable updates',
    'debug_column': 'Will print A LOT of useless debug info into the output',
    'mode_name_column': 'Choose a mode bot will follow while choosing characters/duration',
    'character_column': 'Choose a character (disabled for some modes)',
    'duration_column': 'Choose a duration\n'
                       'For some modes this is max duration that the bot will use',
    'auto_stop_column': 'Brawlhalla imposes xp/gold limit which is triggered if you play too much\n'
                        'This option enables automatically stopping the bot to reset said limit\n'
                        'Otherwise, bot will continue to work but will get close to no xp/gold',
    'auto_detect_auto_stop_column': 'Enables automatic detection of xp limit from xp earnings after the game\n'
                                    'Disables following 2 options\n'
                                    '!!Can be unstable for character levels higher than 60!!',
    'auto_stop_frequency_column': 'How often will bot stop to reset xp/gold limit\n'
                                  'From experience, 4.5-5 hours is average time needed to get to the limit',
    'auto_stop_duration_column': 'How much time bot will wait to reset xp/gold limit\n'
                                 'From experience, 30 minutes is enough (25 is not afaik)',
    'bots_column': 'How many bots (not including player) will there be in a game\n'
                   'Hits and goals do not actually affect xp/gold gain, so 2 is optimal value\n'
                   'Brawlhalla is known to work extremely unstable with >4 players and long games',
    'stealth_column': 'Will hide the game window after Brawlhalla startsn\n'
                      'Also automatically sets following option to True',
    'mute_column': 'If bot should disable sounds/music ingame after getting into menu',
}

MESSAGES = {
    'waiting_for_bh_window': 'Waiting for brawlhalla window',
    'found_bh': 'Found Brawlhalla',
    'not_windowed_mode': 'Not windowed mode, restarting',
    'stealth_mode': 'Entering stealth mode',
    'initialized': 'Initialized',
    'initial_on_exit': '\nSession Stats:\n\nTime running: %s\nGames completed: %s\nCrashes/restarts: %s\nXP earned: %s\n',
    'on_exit_has_rewards': 'Gold earned: %s\n',
    'on_exit_no_rewards': 'Gold earned: %s (+level-up rewards)\n',
    'started_fighting': 'Started fighting',
    'ended_fighting': 'Ended fighting',
    'reinitializing': 'Reinitializing',
    'queued_recalc': 'Restarting for queued character recalculation',
    'not_in_menu': 'Not in menu',
    'collecting_bonus': 'Collecting daily bonus',
    'accepting_event_popup': 'Accepting event bonus',
    'offline': 'Offline, trying to connect',
    'item_not_selected': '%s not selected',
    'sorting_by_date': 'Sorting by date',
    'collecting_character_data': 'Collecting character data',
    'skip_lvl_valid': 'Skipping level validation',
    'calc_xp': 'Calculated xp: %s',
    'pixel_xp': 'Pixelsearch xp: %s',
    'xp_discrep': 'Discrepancy in xp earnings detected\nScheduling xp reset and character recalculation',
    'waiting_for_loading': 'Waiting for loading',
    'loading': 'Loading',
    'pick_char': 'Picking %s',
    'setting_dur': 'Setting duration to %s',
    'wait_for_xp_reset': 'Waiting %s minutes for xp reset',
    'wait_remaining': 'Waiting for xp reset: %s seconds left',
    'creating_lobby': 'Creating lobby',
    'setting_lobby': 'Setting lobby up',
    'starting_game': 'Starting game',
    'loaded': 'Loaded',
    'disconnected': 'Disconnected from the game, restarting',
    'return_to_lobby': 'Going back to lobby',
    'no_modes': 'No modes found. Program will not function with empty modes directory.',
    'old_config': 'Config was made for older bot version. Please, make sure everything is up to date.',
    'level_error': 'Error recognizing level\nBot only works with levels 1-100',
    'cant_save_hotkeys': 'Could not save hotkeys. Exception: %s',
    'cant_save_config': 'Could not save config. Exception: %s',
    'start_bot': 'Starting the bot',
    'stop_bot': 'Stopping the bot',
    'test': 'Test',
    'downloading': 'Downloading: %s%%',
    'downloaded': 'Download completed in %s',
    'resize': 'Game window size: %sx%s\nGame client area size: %sx%s\nScreen size: %sx%s',
    'move_offscreen': 'Moving game window off-screen',
    'update_total_stats': 'Updating all-time stats',
    'total_stats': '\nAll-Time Stats:\n\nGames completed: %s\nXP earned: %s\nGold earned: %s\nTime running: %s\n',
    'autostart_check': 'Checking autostart conditions',
    'rotation_error': 'Error getting character rotation:\n%s',
    'muting': 'Muting sounds',
    'reconnected': 'Reconnected',
    'settings': 'Current settings:\n'
                '------------------------\n'
                'App Name: {0.APP_NAME}\n'
                'App Version: {0.APP_VERSION}\n'
                'Compiled: {0.compiled}\n'
                'Branch: {0.branch}\n'
                'New version: {0.new_version}\n'
                'Language: {0.language_name}\n'
                'Font: {0.font}\n'
                'Autostart: {0.autostart}\n'
                'Debug: {0.debug}\n'
                '------------------------\n',
    'config': 'Current config:\n'
              '------------------------\n'
              'Mode: {0.mode_name}\n'
              'Character: {0.character}\n'
              'Duration: {0.duration}\n'
              'Auto-stop: {0.auto_stop}\n'
              'Auto detect auto-stop: {0.auto_detect_auto_stop}\n'
              'Auto-stop frequency: {0.auto_stop_frequency}\n'
              'Auto-stop duration: {0.auto_stop_duration}\n'
              'Bots: {0.bots}\n'
              'Stealth: {0.stealth}\n'
              'Mute: {0.mute}\n'
              '------------------------\n',
    'resized_warning': 'Game window was resized. Please read the instructions. Bot will now restart',
    'danger_zone_warning': 'Bot is in danger zone (Mallhalla or Battle Pass). Restarting',
    'invalid_state_warning': 'Bot is in invalid state. Something went wrong. Restarting',
    'no_steam_exe': 'Steam client exe cannot be found. Please launch Steam and try to run bot again',
    'delayed_stop': 'Bot will stop after finishing current game or before beginning a new one',
    'cancel_stop': 'All queued stops were cancelled',
    'menu_pixels_error': 'Error getting pixels for state detection. Don\'t worry, this just means that the default ones will be used:\n%s',
}
