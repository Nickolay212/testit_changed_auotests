import csv
import pathlib


def write_to_csv(name_file: str, values: list):
    """
    Запись в csv файл. \n
    :param name_file: имя файла.
    :param values: список значений в строке.
    """
    with open(f"{get_project_root()}/data/{name_file}.csv", 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(values)


def get_project_root() -> str:
    """
    Возвращает путь включительно до корневой папки проекта, поднимаясь из папки с текущим файлом utils.py.
    :return: возвращает абсолютный путь до корня проекта
    """
    return pathlib.Path(__file__).parent.parent


def get_path_file(path: any, name: str = "", ext: str = "") -> str:
    """
    Получает путь до файла. \n
    :param path: путь до папки в которой запущен тест.
    :param name: имя файла, ищется перебором рекурсивно, относительно path.
    :param ext: расширение файла или правило на расширение, например: json или [jJ][sS][oO][nN]
    :return: возвращает путь до файла.
    """
    if type(path) is pathlib.Path or pathlib.WindowsPath or pathlib.PosixPath:
        return str(list(path.rglob(f"{name}.{ext}"))[0])

