from json import loads

with open('handlers/crud_handlers/driver_crud_handlers/driver_crud_texts.json', 'r', encoding='utf-8') as file:
    texts = loads(file.read())