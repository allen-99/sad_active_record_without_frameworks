
# Просто лаба по работе с паттерном Active Record
## Запуск
### Установить зависимости из `requirements.txt` 
```
pip install -r requirements.txt
```
### Поднять БД mysql и ввести свои логин/пароль для входа

## Основные роуты
Удаление и поиск по id находятся на одной странице. Показ всех сообщений и поиск по полю и его значению тоже на одной. 

- ``` all_messages ``` - получение списка всех сообщений
- ``` one_message ``` - поиск сообщения id
- ``` some_messages ``` - поиск сообщений по названию поля и его значению
- ``` save ``` - добавление нового сообщения
- ``` delete ``` - удаление сообщения по id 


