import requests
import os
import json
import datetime
import sys
from http_status_descriptions import http_status_descriptions
from time import sleep

original_stdout = sys.stdout
default_values = {
    'url': 'https://jsonplaceholder.typicode.com/',
    'CONST_URL': 'https://jsonplaceholder.typicode.com/',
    'page_type': '',
}

class ClientSideError(Exception):
    """
    Пользовательское исключение для ошибок на стороне клиента.
    """
    def __init__(self, message="Ошибка на стороне клиента. Попробуйте снова."):
        self.message = message
        super().__init__(self.message)

class ServerSideError(Exception):
    """
    Пользовательское исключение для ошибок на стороне сервера.
    """
    def __init__(self, message="Ошибка на стороне сервера. Простите, но мы не можем ничего сделать."):
        self.message = message
        super().__init__(self.message)

class SillyException(Exception):
        def __init__(self, message="Непонятная ошибка, завершаю работу"):
            self.message = message
            super().__init__(self.message)

class IncorrectInput(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    def __str__(self):
        return 'Неверный ввод. Попробуй снова.'

class MyValueError(Exception):
        def __init__(self, message='Введено неправильное значение. Попробуйте снова'):
            self.message = message
            super().__init__(self.message)

def make_log(log_text='Am I teapot?'):
    with open('logs.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    with open('logs.txt', 'w', encoding='utf-8') as file:
        sys.stdout = file
        print(f'{text}{datetime.datetime.now().strftime("%H:%M:%S")} - {log_text}')
        sys.stdout = original_stdout

def check_int(object: str,  cur_funk, range = None):
    try:
        object_ = int(object)
        if range is None or range[0] <= object_ <= range[1]:
            return str(object_)
        else: raise IncorrectInput
    except ValueError:
        exit_mod(MyValueError, cur_funk)
    except IncorrectInput:
        exit_mod(IncorrectInput, cur_funk)

def clear():
    make_log('Консоль очищена') 
    try:
        os.system('cls')
    except:
        os.system('clear')

def choose_page_type(url=default_values.get('CONST_URL')):
    make_log('Переключено на страницу выбора раздела')
    print('В каком разделе вы хотите искать?')
    print('1 - Посты')
    print('2 - Комментарии')
    print('3 - Фотографии')
    print('4 - Пользователи')
    print('0 - Покинуть приложение')
    page_type = input('Что вы хотите открыть: ')
    match page_type:
        case '1':
            url = url + 'posts/'
            page_type = 'posts'
        case '2':
            url = url + 'comments/'
            page_type = 'comments'
        case '3':
            url = url + 'photos/'
            page_type = 'photos'
            sorry(main)
        case '4':
            url = url + 'users/'
            page_type = 'users'
        case '0':
            exit_mod(e=None, isException=False)
        case _:
            exit_mod(IncorrectInput, choose_page_type)
    default_values['page_type'] = page_type
    default_values['url'] = url

def choose_parameter(url = default_values.get('CONST_URL'), page_type=default_values.get('page_type')):
    make_log('Переключено на страницу выбора параметра')
    print('По какому параметру хотите начать поиск?')
    match page_type:
        case 'posts': # Поиск в постах 
            print('1 - Поиск по ID поста')
            print('2 - Поиск по ID автора')
            print('3 - Поиск по заголовку')
            parameter = input('По какому параметру хотите искать: ')
            match parameter:
                case '1':
                    print('Начинаю поиск по ID поста')
                    id = input('Введите ID: ')
                    id = check_int(id, choose_parameter)
                    url += id
                case '2':
                    print('Начинаю поиск по ID автора')
                    tmp = input('Введите ID: ')
                    id = '?&userId=' + check_int(tmp, choose_parameter)
                    url += id
                case '3':
                    sorry(choose_parameter)
                    print('Начинаю поиск по заголовку')
                case _:
                    exit_mod(IncorrectInput, choose_parameter)
        
        case 'comments': # Поиск в комментариях 
            print('1 - Поиск по ID поста')
            print('2 - Поиск по ID комментария')
            print('3 - Поиск по заголовку')
            parameter = input('По какому параметру хотите искать: ')
            match parameter:
                case '1':
                    # Если выбрали поиск по ID
                    print('Начинаю поиск по ID поста')
                    id = '?&postId=' + input('Введите ID: ')
                    url += id
                case '2':
                    print('Начинаю поиск по ID комментария')
                    id = input('Введите ID: ') + '/'
                    url += id
                case '3':
                    print('Начинаю поиск по заголовку')
                    sorry(choose_parameter)
                case _:
                    print('\nНекорректный ввод. Попробуйте снова')
                    clear()
                    choose_parameter(url=default_values.get('CONST_URL') + 'comments', page_type=page_type)
        
        case 'photos': # Поиск в фотографиях 
            sorry(choose_parameter)
        
        case 'users': # Поиск в пользователях 
            print('1 - Поиск по ID')
            print('2 - Поиск по Username')
            print('3 - Поиск по ФИО')
            
            parameter = input('По какому параметру хотите искать: ')
            match parameter:
                case '1':
                    # Если выбрали поиск по ID
                    print('Начинаю поиск по ID')
                    id = input('Введите ID: ')
                    url += id
                case '2':
                    # Если выбрали поиск по ID
                    print('Начинаю поиск по Username')
                    sorry(choose_parameter)
                case '3':
                    # Если выбрали поиск по ID
                    print('Начинаю поиск по ФИО')
                    sorry(choose_parameter)
                case _:
                    print('\nНекорректный ввод. Попробуйте снова')
                    clear()
                    choose_parameter(url=default_values.get('CONST_URL') + 'users', page_type=page_type)
    default_values['url'] = url

def make_request(url=default_values.get('url'), page_type=default_values.get('page_type')):
    try:
        responce = requests.get(url=url)
        status_code = responce.status_code
        make_log(f'Выполнен запрос по ссылке {url}. Код: {status_code}')
        make_log(f'{http_status_descriptions.get(status_code, 'Описание не найдено')}')

        if 200 <= status_code < 300: # Всё получилось, всем пофиг (коды успеха) 
            pass
        elif 300 <= status_code < 400: # Коды перенаправления (всем всё ещё пофиг) 
            pass
        elif 400 <= status_code < 500: # Коды ошибок клиента 
            exit_mod(ClientSideError, main)
        elif 500 <= status_code < 600: # Коды ошибок сервера 
            exit_mod(ServerSideError, None, False)

    except Exception as e:
        print(f'Произошла непредвиденная ошибка при переходе по ссылке {url}')
        print(f'Текст ошибки: {e}')
        make_log(f'Произошла непредвиденная ошибка при переходе по ссылке {url}')
        make_log(f'Текст ошибки: {e}')

    try:
        answers = responce.json()
        if isinstance(answers, list):
            if len(answers) != 0:
                for answer in answers:
                    match page_type:
                        case 'posts':
                            print(f'Заголовок: {answer['title']}')
                            print(f'Текст: {answer['body']}')
                        case 'comments':
                            print(f'Комментарий к посту номер {answer['postId']} пользователя {answer['name']}:\n{answer['body']}')
                        case 'photos':
                            sorry(main)
                        case 'users':
                            for key in answer.keys:
                                match key:
                                    case 'name':
                                        print(f'ФИО: {answer[key]}')
                                    case 'username':
                                        print(f'Username: {answer[key]}')
                                    case 'email':
                                        print(f'Email: {answer[key]}')
                                    case 'address':
                                        print(f'Адрес: город {answer[key['city']]}, улица {answer[key['street']]}, дом {answer[key['suite']]}')
                                    case 'phone':
                                        print(f'Номер телефона: {answer[key]}')
                                    case 'website':
                                        print(f'Личный сайт: {answer[key]}')
                                    case 'company':
                                        print(f'Работает в компаниии {answer[key['name']]}. Их бизнес-стратегия - {answer[key['bs']]}. Слоган компании - {answer[key['catchPhrase']]}')
                    print()
            else:
                print('Ошибка ввода. Попробуйте снова')
                sleep(2)
                main()

        else:
            answer = answers
            match page_type:
                case 'posts':
                    print(f'Заголовок: {answer['title']}')
                    print(f'Текст: {answer['body']}')
                case 'comments':
                    print(f'Комментарий к посту номер {answer['postId']} пользователя {answer['name']}:\n{answer['body']}')
                case 'photos':
                    sorry(main)
                case 'users':
                    for key in answer.keys():
                        match key:
                            case 'name':
                                print(f'ФИО: {answer[key]}')
                            case 'username':
                                print(f'Username: {answer[key]}')
                            case 'email':
                                print(f'Email: {answer[key]}')
                            case 'address':
                                print(f'Адрес: город {answer[key]['city']}, улица {answer[key]['street']}, дом {answer[key]['suite']}')
                            case 'phone':
                                print(f'Номер телефона: {answer[key]}')
                            case 'website':
                                print(f'Личный сайт: {answer[key]}')
                            case 'company':
                                print(f'Работает в компаниии {answer[key]['name']}. Их бизнес-стратегия - {answer[key]['bs']}. Слоган компании - {answer[key]['catchPhrase']}')

    except Exception as e:
        print(f'Произошла непредвиденная ошибка при получении информации. Ссылка: {url}')
        print(f'Текст ошибки: {e}')
        make_log(f'Произошла непредвиденная ошибка при получении информации. Ссылка: {url}')
        make_log(f'Текст ошибки: {e}')

def main():
    while True:
        make_log('Запущено главное меню')
        url = default_values.get('CONST_URL')
        clear()
        choose_page_type()
        clear()
        choose_parameter(url=default_values.get('url'), page_type=default_values.get('page_type'))
        clear()
        make_request(url=default_values.get('url'), page_type=default_values.get('page_type'))
        input('Нажмите ENTER, чтобы продолжить...')

def sorry(funk = main):
    print('Временно недоступно')
    sleep(3)
    funk()

def exit_mod(e = SillyException, funk_to_go = None, isException = True):
    if isException:
        try:
            raise e
        except Exception as e:
            print(e)
            make_log(e)
            sleep(3)
            if funk_to_go is not None:
                funk_to_go()

    else:
        if e is not None:
            try:
                raise e
            except Exception as e:
                print(e)
                make_log(e)
        print('Спасибо, что воспользовались нашим приложением!')
        make_log('Программа завершила работу')
        sleep(3)
        exit(0)

if __name__ == '__main__':
    with open('logs.txt', 'w', encoding='utf-8') as file:
        pass
    make_log('Программа запущена')
    main()
