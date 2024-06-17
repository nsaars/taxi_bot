from json import loads

with open('handlers/menu_handlers/driver_menu_handlers/driver_menu_texts.json', 'r', encoding='utf-8') as file:
    texts = loads(file.read())