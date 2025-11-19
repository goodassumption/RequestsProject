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

class TemporaryUnavailable(Exception):
    def __init__(self, message = 'Функция в разработке. Проверьте GitHub репозиторий на наличие обновлений'):
        self.message = message
        super().__init__(self.message)

class NotFound(Exception):
    def __init__(self, message = 'Ничего не найдено. Пожалуйста, проверьте ввод'):
        self.message = message
        super().__init__(self.message)

def make_log(log_text='Am I teapot?'):
    """
### `make_log(log_text='Am I teapot?')`

Добавляет новую запись с временной меткой в лог-файл `logs.txt`.

Функция работает путем полного считывания файла, добавления новой строки к содержимому и последующей полной перезаписи файла.

#### Параметры:
*   `log_text` (str, optional): Текст лог-сообщения для записи в файл. По умолчанию используется `'Am I teapot?'`.

#### Возвращаемое значение:
*   `None`: Функция ничего не возвращает.

#### Побочные эффекты:
*   Читает и полностью перезаписывает файл `logs.txt`.
*   Временно перенаправляет стандартный вывод (`sys.stdout`) в файл для выполнения записи.
*   Зависит от глобальной переменной `original_stdout` для восстановления стандартного вывода после записи.
"""

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
    """
### `clear()`

Очищает консоль, используя команду, соответствующую текущей операционной системе (Windows или POSIX-совместимые системы, например, Linux, macOS).

#### Параметры:
*   `None`: Функция не принимает параметров.

#### Возвращаемое значение:
*   `None`: Функция ничего не возвращает.

#### Побочные эффекты:
*   Выполняет системную команду (`cls` для Windows, `clear` для POSIX) для очистки экрана терминала.
*   Записывает в лог сообщение о том, что консоль была очищена.
"""

    make_log('Консоль очищена')
    platform = os.name
    if platform == 'nt':
        os.system('cls')
    elif platform == 'posix':
        os.system('clear')

def string_search():
    def_url = default_values.get('url')
    page_type = default_values.get('page_type')
    if page_type == 'users':
        pass
    else:
        def_url += '?&tittle'
    all_info = requests.get(url=def_url).json
    all_messages = []
    for dict in all_info:
        pass

def choose_page_type(url=default_values.get('CONST_URL')):
    """
### `choose_page_type(url=default_values.get('CONST_URL'))`

Отображает пользователю меню для выбора раздела API и обновляет конфигурацию приложения в соответствии с выбором.

#### Параметры:
*   `url` (str, optional): Базовый URL, к которому будет добавлен путь к выбранному разделу. По умолчанию используется значение из `default_values.get('CONST_URL')`.

#### Возвращаемое значение:
*   `None`: Функция ничего не возвращает.

#### Побочные эффекты:
*   Выводит в консоль меню для выбора раздела и ожидает ввод от пользователя.
*   Модифицирует глобальный словарь `default_values`, обновляя ключи `url` и `page_type` в зависимости от выбора:
    *   **'1' (Посты):** Настраивает приложение для работы с разделом постов.
    *   **'2' (Комментарии):** Настраивает приложение для работы с разделом комментариев.
    *   **'3' (Фотографии):** Инициирует поиск по строке или подстроке.
    *   **'4' (Пользователи):** Настраивает приложение для работы с разделом пользователей.
*   Вызывает функцию `exit_mod` в следующих случаях:
    *   При выборе опции **'0'** для корректного завершения работы приложения.
    *   При некорректном вводе для обработки ошибки.
*   При вызове записывает в лог сообщение о переключении на страницу выбора раздела.
"""

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
            exit_mod(TemporaryUnavailable, main)
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
    """
### `choose_parameter(url = default_values.get('CONST_URL'), page_type=default_values.get('page_type'))`

Отображает пользователю меню для выбора параметра поиска в зависимости от ранее выбранного раздела (`page_type`). Формирует и сохраняет конечный URL для API-запроса на основе выбора пользователя.

#### Параметры:
*   `url` (str, optional): Базовый URL раздела, который будет дополнен параметрами поиска. По умолчанию используется `default_values.get('CONST_URL')`.
*   `page_type` (str, optional): Тип раздела ('posts', 'comments', 'users'), который определяет, какое меню параметров будет показано. По умолчанию используется `default_values.get('page_type')`.

#### Возвращаемое значение:
*   `None`: Функция ничего не возвращает.

#### Побочные эффекты:
*   Выводит в консоль меню для выбора конкретного параметра поиска и ожидает ввод от пользователя.
*   Модифицирует глобальный словарь `default_values`, обновляя ключ `url` сформированным конечным URL.
*   В зависимости от значения `page_type`, предлагает различные параметры поиска:
    *   **'posts':**
        *   `'1' (ID поста)`: Запрашивает ID и добавляет его в путь URL (e.g., `/posts/1`).
        *   `'2' (ID автора)`: Запрашивает ID и добавляет его как query-параметр (e.g., `/posts?&userId=1`).
        *   `'3' (Заголовок)`: Опция временно недоступна.
    *   **'comments':**
        *   `'1' (ID поста)`: Запрашивает ID и добавляет его как query-параметр (e.g., `/comments?&postId=1`).
        *   `'2' (ID комментария)`: Запрашивает ID и добавляет его в путь URL.
        *   `'3' (Заголовок)`: Опция временно недоступна.
    *   **'photos':**
        *   Весь раздел временно недоступен.
    *   **'users':**
        *   `'1' (ID)`: Запрашивает ID и добавляет его в путь URL.
        *   `'2' (Username)` и `'3' (ФИО)`: Опции временно недоступны.
*   При некорректном вводе или выборе недоступной опции вызывает функцию `exit_mod` или перезапускает себя для повторного ввода.
*   При вызове записывает в лог сообщение о переключении на страницу выбора параметра.
"""
        
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
                    exit_mod(TemporaryUnavailable, choose_parameter)
                    print('Начинаю поиск по заголовку')
                    string_search()
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
                    exit_mod(TemporaryUnavailable, choose_parameter)
                    print('Начинаю поиск по заголовку')
                case _:
                    print('\nНекорректный ввод. Попробуйте снова')
                    clear()
                    choose_parameter(url=default_values.get('CONST_URL') + 'comments', page_type=page_type)
        
        case 'photos': # Поиск в фотографиях 
            exit_mod(TemporaryUnavailable, choose_parameter)
        
        case 'users': # Поиск в пользователях 
            print('1 - Поиск по ID')
            print('2 - Поиск по Username')
            print('3 - Поиск по ФИО')
            
            parameter = input('По какому параметру хотите искать: ')
            match parameter:
                case '1':
                    print('Начинаю поиск по ID')
                    id = input('Введите ID: ')
                    url += id
                case '2':
                    print('Начинаю поиск по Username')
                    exit_mod(TemporaryUnavailable, choose_parameter)
                case '3':
                    print('Начинаю поиск по ФИО')
                    exit_mod(TemporaryUnavailable, choose_parameter)
                case _:
                    print('\nНекорректный ввод. Попробуйте снова')
                    clear()
                    choose_parameter(url=default_values.get('CONST_URL') + 'users', page_type=page_type)
    default_values['url'] = url

def make_request(url=default_values.get('url'), page_type=default_values.get('page_type')):
    """
### `make_request(url=default_values.get('url'), page_type=default_values.get('page_type'))`

Выполняет HTTP GET-запрос по указанному URL, обрабатывает полученный JSON-ответ и выводит отформатированные данные в консоль в зависимости от типа страницы.

#### Параметры:
*   `url` (str, optional): Конечный URL для API-запроса. По умолчанию используется значение из `default_values.get('url')`.
*   `page_type` (str, optional): Тип запрашиваемого контента ('posts', 'comments', 'users'), который определяет логику форматирования ответа. По умолчанию используется `default_values.get('page_type')`.

#### Возвращаемое значение:
*   `None`: Функция ничего не возвращает.

#### Побочные эффекты:
*   Отправляет GET-запрос на указанный `url`.
*   Записывает в лог информацию о запросе и его HTTP-статусе.
*   Обрабатывает и выводит данные в консоль в зависимости от `page_type`:
    *   **'posts'**: Выводит заголовок и текст поста.
    *   **'comments'**: Выводит ID поста, имя автора и текст комментария.
    *   **'users'**: Выводит подробную информацию о пользователе (ФИО, email, адрес, телефон, компания и т.д.).
    *   **'photos'**: Раздел временно недоступен; вызывает `exit_mod`.
*   Обрабатывает HTTP-статусы ответа:
    *   `4xx (ошибки клиента)`: Прерывает выполнение через `exit_mod`, передавая ошибку `ClientSideError`.
    *   `5xx (ошибки сервера)`: Прерывает выполнение через `exit_mod`, передавая ошибку `ServerSideError`.
*   Перехватывает и логирует непредвиденные исключения, которые могут возникнуть во время сетевого запроса или парсинга JSON.
*   В случае получения пустого списка в ответе, информирует пользователя об ошибке и перезапускает главный цикл приложения (`main()`).
"""
    
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
            err = ClientSideError(message=f'{status_code} {http_status_descriptions.get(status_code)}')
            exit_mod(err, main)
        elif 500 <= status_code < 600: # Коды ошибок сервера 
            err = ServerSideError(message=f'{status_code} {http_status_descriptions.get(status_code)}')
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
                            exit_mod(TemporaryUnavailable, main)
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
                status_code = 404
                err = ClientSideError(message=f'{status_code} {http_status_descriptions.get(status_code)}')
                exit_mod(err, main)

        else:
            answer = answers
            match page_type:
                case 'posts':
                    print(f'Заголовок: {answer['title']}')
                    print(f'Текст: {answer['body']}')
                case 'comments':
                    print(f'Комментарий к посту номер {answer['postId']} пользователя {answer['name']}:\n{answer['body']}')
                case 'photos':
                    exit_mod(TemporaryUnavailable, main)
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
                                print(f'Работает в компаниии {answer[key]['name']}. Их бизнес-стратегия - {answer[key]['bs']}.\nСлоган компании - {answer[key]['catchPhrase']}')

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

def exit_mod(e = SillyException, funk_to_go = None, isException = True):
    """
    ### `exit_mod(e = SillyException, funk_to_go = None, isException = True)`

    Универсальный обработчик исключений и завершения работы программы. В зависимости от флага `isException`, функция либо обрабатывает ошибку с возможностью перехода к другой функции, либо корректно завершает приложение.

    #### Параметры:
    *   `e` (Exception, optional): Класс или объект исключения для обработки. По умолчанию `SillyException`.
    *   `funk_to_go` (function, optional): Функция, которую нужно вызвать после обработки исключения (например, для возврата в предыдущее меню). Используется, только если `isException` равно `True`. По умолчанию `None`.
    *   `isException` (bool, optional): Флаг, определяющий режим работы. `True` — режим обработки исключения. `False` — режим штатного завершения программы. По умолчанию `True`.

    #### Возвращаемое значение:
    *   Не возвращает значение. Завершает свою работу вызовом другой функции (`funk_to_go`) или полным прекращением выполнения скрипта (`exit(0)`).

    #### Побочные эффекты:
    *   **В режиме исключения (`isException=True`):**
        *   Выводит текст исключения в консоль.
        *   Записывает информацию об исключении в лог-файл с помощью `make_log()`.
        *   Приостанавливает выполнение на 3 секунды.
        *   Если передана `funk_to_go`, вызывает эту функцию для продолжения работы программы.
    *   **В режиме завершения (`isException=False`):**
        *   Выводит прощальное сообщение в консоль.
        *   Записывает в лог информацию о завершении работы.
        *   Приостанавливает выполнение на 3 секунды.
        *   ~~И эпично прыгает с крыши~~ Принудительно завершает выполнение всего скрипта с кодом `0`.
    """

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
