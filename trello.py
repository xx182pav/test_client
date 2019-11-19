import requests
import datetime

# Данные авторизации в API Trello
auth_params = {
    'key': "",
    'token': "", }

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"
board_id = ""


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #    Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print('Количество задач:', len(task_data))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create():
    name = input("Введите название новой задачи\n")
    column_name = input("Введите название колонки, куда поместить создаваемую задачу\n")
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move():
    name = input("Введите название задачи, которую хотите переместить\n")
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_move = ''
    task_id = []
    col_with_tasks = []
    timestamps = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id.append(task['id'])
                col_with_tasks.append(column['name'])
                timestamps.append(
                    datetime.datetime.strptime(task['dateLastActivity'].split(".")[0], "%Y-%m-%dT%H:%M:%S"))
    if len(task_id) > 1:
        print("Задач с таким именем несколько:")
        for i in range(len(task_id)):
            print(f"{i + 1}: из колонки {col_with_tasks[i]}, последнее изменение: {timestamps[i]}")
        target_task = int(input("Введите номер задачи, которую нужно переместить\n")) - 1
        task_move = task_id[target_task]
    else:
        task_move = task_id[0]
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    column_name = input("Введите название колонки, куда поместить задачу\n")
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_move + '/idList',
                         data={'value': column['id'], **auth_params})


def add_column():
    name = input("Введите название новой колонки\n")
    pos = input("Хотите поместить новую колонку в начало или конец?"
                "\n Варианты ввода: 'top' и 'bottom'"
                "\n Если ничего не вводить, то по умолчанию будет 'в конец'\n")
    if not pos:
        pos = 'bottom'
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': name, 'pos': pos, **auth_params})


def main_interface():
    print("Добро пожаловать в интерфейс программы по работе с сервером Trello через консоль ")
    choice = input("Нажмите 1, если хотите увидеть список задач,"
                   "\nнажмите 2, чтобы добавить новую колонку,"
                   "\nнажмите 3, чтобы переместить задачу из одной колонки в другую."
                   "\nнажмите 4, чтобы создать новую задачу\n")
    if choice == "1":
        read()
    elif choice == "2":
        add_column()
    elif choice == "3":
        move()
    elif choice == "4":
        create()


if __name__ == "__main__":
    main_interface()
