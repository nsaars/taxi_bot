from json import loads

with open('handlers/crud_handlers/office_crud_handlers/office_crud_texts.json', 'r', encoding='utf-8') as file:
    texts = loads(file.read())

with open('handlers/crud_handlers/office_crud_handlers/office_crud_answer_texts.json', 'r', encoding='utf-8') as file:
    answer_texts = loads(file.read())
