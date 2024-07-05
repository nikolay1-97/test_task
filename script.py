import json
import os
from datetime import datetime

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

#Путь к файлу с расширением json с данными об операциях.
PATH_TO_FILE = DIR_NAME + '/' + 'operations1.json'

def get_dict_with_data(PATH_TO_FILE: str) -> dict:
    """Возвращает словарь с записями, где статус операции
       EXECUTED и тип операции перевод.

        Parameters
        ----------
        PATH_TO_FILE : str
            Файл с расширением json с данными об операциях.
    """
    dict_exe = {}
    with open(PATH_TO_FILE) as file:
        file_data = file.read()
        data = json.loads(file_data)
        for row in data:
            try:
                if row['state'] == 'EXECUTED' and 'from' in row:
                    dict_exe[row['id']] = row
            except KeyError:
                pass
    return dict_exe

#Словарь с данными об операциях, где
#статус операции EXECUTED и тип операции перевод.
dict_exe = get_dict_with_data(PATH_TO_FILE)

#Список с данными об операциях, отсортированный по датам.
ls_sort_on_date = sorted(
    dict_exe.values(),
    key = lambda row: datetime.strptime(
        row['date'],
        "%Y-%m-%dT%H:%M:%S.%f",
    ),
    reverse = True,
)

def convert_account_number(acc_number: list) -> str:
    """Преобразовывает строку с реквизитами счета
        к нужному формату.

        Parameters
        ----------
        acc_number : list
            Список с реквизитами счета.
    """
    acc_nmb = acc_number[-1]
    conv_acc_nmb = ''
    if len(acc_nmb) == 16:
        conv_acc_nmb = acc_nmb[0:4]+' '+acc_nmb[4:6]+'** ****' +' '+acc_nmb[-4:]
    elif len(acc_nmb) == 20:
        conv_acc_nmb = '**' + acc_nmb[-4:]
    if len(acc_number) <= 2:
        return acc_number[0] + ' ' + conv_acc_nmb
    else:
        return ' '.join(acc_number[:-1]) + ' ' + conv_acc_nmb


def show_rows(ls: list, count: int):
    """Выводит на экран список из последних
       совершенных клиентом операций.

        Parameters
        ----------
        ls: list
            Список с данными об операциях.
        count: int
            Количество операций.
    """
    for i in range(count):
        date = ls[i]['date']
        fromm = convert_account_number(ls[i]['from'].split())
        to = convert_account_number(ls[i]['to'].split())
        print(
            f'{date[8:10]}.{date[5:7]}.{date[0:4]}',
            ls[i]['description'],
            sep = ' ',
        )
        print(f'{fromm} -> {to}')
        print(
            ls[i]['operationAmount']['amount'],
            ls[i]['operationAmount']['currency']['name'],
            sep = ' '
        )
        print(' ')

show_rows(ls_sort_on_date, 5)
