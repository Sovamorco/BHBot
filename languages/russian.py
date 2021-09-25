LANGUAGE = 'Русский'

LAYOUT_MAPPING = {
    # Основное окно
    'main_window_title': 'BHBot',
    'title': 'BHBot от Sovamorco',
    'version': 'Версия: {0.APP_VERSION}',
    'press_start': ['Нажми "Старт" чтобы начать работу бота', 'Нажми "Стоп" чтобы завершить работу бота'],
    'toggle': ['Старт', 'Стоп'],
    'settings': 'Настройки',
    'instructions': 'Инструкции',
    'exit': 'Выход',
    'test': 'Тест',
    'update_available_title': 'Доступно обновление!',
    'update_available_version': 'Новая версия: {0.new_version.version}',
    'update_available_button': 'Обновить',
    # Окно настроек
    'settings_window_title': 'Настройки',
    'settings_title': 'Настройки',
    'settings_help': 'Для дополнительной информации наведите на пункт настроек',
    'language_name_text': 'Язык: ',
    'font_text': 'Шрифт: ',
    'autostart_text': 'Автоматически запускать бота: ',
    'branch_text': 'Ветка обновлений: ',
    'debug_text': 'Дебаг-выводы: ',
    'mode_name_text': 'Режим: ',
    'character_text': 'Персонаж: ',
    'duration_text': 'Длительность: ',
    'auto_stop_text': 'Сброс лимита опыта: ',
    'auto_detect_auto_stop_text': 'Автоматическое определение лимита: ',
    'auto_stop_frequency_text': 'Частота сброса в часах: ',
    'auto_stop_duration_text': 'Длительность ожидания для сброса в минутах: ',
    'bots_text': 'Количество ботов: ',
    'stealth_text': 'Стелс-режим (скрытое окно игры): ',
    'mute_text': 'Выключать звук: ',
    'hotkey_settings': 'Настройки горячих клавиш',
    'save': 'Сохранить',
    'back': 'Назад',
    # Окно настройки горячих клавиш
    'hotkeys_window_title': 'Горячие клавиши',
    'hotkeys_title': 'Горячие клавиши',
    'up_text': 'Вверх (Не прыжок!)',
    'left_text': 'Влево',
    'down_text': 'Вниз',
    'right_text': 'Вправо',
    'throw_text': 'Бросок',
    'quick_text': 'Слабая атака',
    'dodge_text': 'Уворот',
    'heavy_text': 'Сильная атака',
    # Окно инструкций
    'instructions_window_title': 'Инструкции',
    'instructions_contents': ['Инструкции по использованию бота:',
                              '1. ОЧЕНЬ ВАЖНО\n'
                              'Либо используйте стелс-режим в настройках бота, либо никак не мешайте его работе. '
                              'Движение мышью над окном игры, изменение размера или перемещение этого окна и использование клавиатуры при выбранном окне игры '
                              'во время работы бота может привести к неожиданным и нежелательным последствиям,  '
                              'таким как выбор неверных персонажей или даже совершение покупок в внутриигровом магазине или боевом пропуске. '
                              'Если вы заметили что случайно что-то передвинули, перезапустите бота (а лучше используйте стелс-режим, серьезно)',
                              '2. Убедитесь что внутриигровой язык - Английский',
                              '3. Убедитесь, что настройка "Свернуть разноплановых" ("Collapse crossovers") - включена',
                              '4. Переведите игру в оконный режим если бот не делает это сам',
                              '5. Настройте все по своему усмотрению и нажмите "Старт"',
                              'Наслаждайтесь c:'],
    # Высвечивающиеся окна
    'changelog_popup_title': 'Новая версия',
}

TOOLTIPS = {
    # Окно настроек
    'settings_help': '\n     :)     \n',
    'language_name_column': 'Выбор языка (автоматически обновляется)',
    'font_column': 'Выбор шрифта (автоматически обновляется)',
    'autostart_column': 'Автоматически запускать бота, если запущена программа и вы не играете в Brawlhall\'у\n'
                        'Условия проверяются каждые 5 минут',
    'branch_column': 'В бете могут быть экспериментальные/нестабильные изменения',
    'debug_column': 'Выводит МНОГО бесполезной дебаг-информации в окно вывода',
    'mode_name_column': 'Выбор режима, который бот будет использовать для выбора персонажей/длительности',
    'character_column': 'Выбор персонажа (выключен для некоторых режимов)',
    'duration_column': 'Выбор длительности\n'
                       'Для некоторых режимов это максимальная длительность игры',
    'auto_stop_column': 'Brawlhalla накладывает лимит на количество опыта/золота, которое можно получить за одну сессию игры\n'
                        'Эта настройка автоматически приостанавливает бота для сброса данного лимита\n'
                        'Иначе, бот будет продолжать работать, но почти не получая опыта/золота',
    'auto_detect_auto_stop_column': 'Включает автоматическое определение момента достижения лимита по опыту, получаемому после игры\n'
                                    'Выключает следующие две настройки\n'
                                    '!!Может быть нестабильным для персонажей уровня 60 и выше!!',
    'auto_stop_frequency_column': 'Как часто боту стоит останавливаться для сброса лимита\n'
                                  'Из опыта, 4.5-5 часов - среднее время достижения лимита',
    'auto_stop_duration_column': 'Как долго боту стоит ждать сброса лимита\n'
                                 'Из опыта, 30 минут - минимальное значение, полностью сбрасывающее лимит',
    'bots_column': 'Как много ботов (не включая игрока) будет в игре\n'
                   'Урон и голы не влияют на получаемый опыт/золото, так что оптимальное значение - 2\n'
                   'Известно, что Brawlhalla работает очень нестабильно с >4 игроками и долгими играми',
    'stealth_column': 'Прячет окно игры после запуска Brawlhall\'ы\n'
                      'Так же автоматически включает следующую настройку',
    'mute_column': 'Стоит ли боту выключать звук/музыку после попадания в меню',
}

MESSAGES = {
    'waiting_for_bh_window': 'Жду окна игры',
    'found_bh': 'Окно игры найдено',
    'not_windowed_mode': 'Игра не в оконном режиме, перезапускаюсь',
    'stealth_mode': 'Вхожу в стелс-режим',
    'initialized': 'Бот инициализирован',
    'initial_on_exit': '\nИтоги сессии:\n\nВремя работы: %s\nИгр завершено: %s\nКрашей/Перезапусков: %s\nОпыта получено: %s\n',
    'on_exit_has_rewards': 'Золота получено: %s\n',
    'on_exit_no_rewards': 'Золота получено: %s (+награды за повышение уровня)\n',
    'started_fighting': 'Начинаю бой',
    'ended_fighting': 'Завершаю бой',
    'reinitializing': 'Перезапускаюсь',
    'queued_recalc': 'Перезапускаю игру для запланированного пересчета опыта персонажей',
    'not_in_menu': 'Не в меню',
    'collecting_bonus': 'Собираю награду за вход',
    'accepting_event_popup': 'Принимаю награду события',
    'offline': 'Не в сети, пытаюсь подключиться',
    'item_not_selected': '%s не выбран',
    'sorting_by_date': 'Сортирую по дате',
    'collecting_character_data': 'Собираю информацию о персонажах',
    'skip_lvl_valid': 'Пропускаю проверку уровня',
    'calc_xp': 'Подсчитанный опыт: %s',
    'pixel_xp': 'Опыт по пикселям: %s',
    'xp_discrep': 'Обнаружено несоответствие в полученном опыте\nПланирую сброс лимита опыта и пересчет опыта персонажей',
    'waiting_for_loading': 'Жду загрузки',
    'loading': 'Загрузка',
    'pick_char': 'Выбираю %s',
    'setting_dur': 'Устанавливаю длительность на %s',
    'wait_for_xp_reset': 'Жду сброса лимита %s минут',
    'wait_remaining': 'Жду сброса лимита: осталось %s секунд',
    'creating_lobby': 'Создаю лобби',
    'setting_lobby': 'Настраиваю лобби',
    'starting_game': 'Начинаю игру',
    'loaded': 'Загрузка завершена',
    'disconnected': 'Отключился от игры, перезапускаю',
    'return_to_lobby': 'Возвращаюсь в лобби',
    'no_modes': 'Не найдено ни одного режима. Программа не будет работать с пустой папкой modes.',
    'old_config': 'Настройки были сделаны для старой версии бота. Пожалуйста, убедитесь что они актуальны.',
    'level_error': 'Ошибка при распознавании уровня\nБот работает только с уровнями 1-100',
    'cant_save_hotkeys': 'Не получилось сохранить горячие клавиши. Ошибка: %s',
    'cant_save_config': 'Не получилось сохранить настройки. Ошибка: %s',
    'start_bot': 'Запускаю бота',
    'stop_bot': 'Выключаю бота',
    'test': 'Тест',
    'downloading': 'Загрузка: %s%%',
    'downloaded': 'Загрузка завершена за %s',
    'resize': 'Размер окна игры: %sx%s\nРазмер клиент-зоны игры: %sx%s\nРазмер экрана: %sx%s',
    'move_offscreen': 'Перемещаю окно игры в другое измерение',
    'update_total_stats': 'Обновляю статистику за все время',
    'total_stats': '\nСтатистика за все время:\n\nИгр завершено: %s\nОпыта получено: %s\nЗолота получено: %s\nВремя работы: %s\n',
    'autostart_check': 'Проверяю условия автозапуска',
    'rotation_error': 'Ошибка при получении ротации персонажей:\n%s',
    'muting': 'Выключаю звук',
    'reconnected': 'Переподключился',
    'settings': 'Настройки:\n'
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
    'config': 'Конфиг:\n'
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
    'resized_warning': 'Размер окна игры был изменен. Пожалуйста, прочитайте инструкции. Бот сейчас перезапустится',
    'danger_zone_warning': 'Бот в опасном состоянии (в внутриигровом магазине или боевом пропуске). Перезапускаюсь',
    'invalid_state_warning': 'Бот в нестандартном состоянии. Что-то пошло не так. Перезапускаюсь',
}
