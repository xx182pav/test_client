import sys 
import requests    

api_key = ""
token = ""

base_url = "https://api.trello.com/1/{}" 
auth_params = {    
    'key': api_key,    
    'token': token, }
board_id = ""    
    
def read():   
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
  
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()       
        if len(task_data) == 1:
            print(column['name'], "[Currently 1 item]")
        else:
            print(column['name'], f"[Currently {len(task_data)} items]")   

        if not task_data:      
            print('\t' + 'No tasks found')      
            continue      
        for task in task_data:
            print('\t' + task['name'], f"[{task['id']}]")   
    
def create(name, column_name): 
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      

    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), params={'name': name, 'idList': column['id'], **auth_params})      
            break

    
def move(name, column_name):       
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
            
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json() 
        tasks = {}   
        for task in column_tasks:
            if task['name'] in tasks.keys():
                tasks[task['name']].append(task['id'])
            else:
                tasks[task['name']] = [task['id']]

        if name not in tasks.keys():
                continue
        else:
            if len(tasks[name]) > 1:
                for i in range(len(tasks[name])):
                    print(f"\t {i+1} {tasks[name][i]}")
                task_id = tasks[name][int(input(f"There are more than 1 occurence of the task '{name}'. Which one do you want to move? \n"))-1]
                break
            task_id = tasks[name][0]

    columns = {}
    for column in column_data:

        if column['name'] in columns.keys():
            columns[column['name']].append(column['id'])
        else:
            columns[column['name']] = [column['id']]
    if len(columns[column_name]) > 1:
        for i in range(len(columns[column_name])):
                    print(f"\t {i+1} {columns[column_name][i]}")
        column_id = columns[column_name][int(input(f"There are more than 1 occurence of the column '{column_name}'. Which one do you want the task to be moved to? \n"))-1]

    else:
        column_id = columns[column_name][0]

    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})       


def create_column(column_name, name=""):
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', params={'name': column_name, "pos": "bottom", **auth_params})
    if name:
    	create(name, column_name)

if __name__ == "__main__":
    while True:
        action = input("Choose an action: \ntype 'read' to see the list of list and cards\ntype 'move' to move a card from one list to another\ntype 'create' to create a new card\ntype 'create_column' to create a new list\ntype 'break' to quit\n")    
        if action == 'read':
            read() 

        elif action == 'create':
            while True:
                try:
                    name = input("Give a name to your card: ")
                    column_name = input("Type the name of the list where your card will be created: ")
                    create(name, column_name)
                    print("Success")
                    break
                except KeyboardInterrupt:
                    break
                except:
                    print("Incorrect values. Use CTRL+C to exit, or continue\n")

        elif action == 'move':    
            while True:
                try:
                    name = input("Type the name of the card you want to move: ")
                    column_name = input("Type the name of the list where your card will be moved: ")
                    move(name, column_name)
                    print("Success")
                    break
                except KeyboardInterrupt:
                    break
                except:
                    print("Incorrect values. Use CTRL+C to exit, or continue\n")

        elif action == 'create_column':
            while True:
                try:
                    column_name = input("Give a name to your list: ")
                    resp = input("Do you want do add a task to your list? If no, your list will be empty. Y/N: ")
                    try:
                        if resp.lower() == 'y':
                            name = input('Give your new task a name: ')
                            create_column(column_name, name)
                            print("Success")
                            break
                        elif resp.lower() == 'n':
                            create_column(column_name)
                            print('Success')
                            break
                    except KeyboardInterrupt:
                        break
                    except:
                        print("Incorrect values. Use CTRL+C to exit, or continue\n")

                    
                    break
                except KeyboardInterrupt:
                    break
                except:
                    print("Incorrect values. Use CTRL+C to exit, or continue\n")

        elif action == 'break':
            print('Terminating...')
            break
