import os
import os.path as pth


def search_duplicate_files(filepath):
    list_of_files = list()  # Список названий файлов
    list_of_dirs = list()  # Список папок
    duplicate_files = list()  # Повторяющиеся файлы
    # Проход по всем файлам и подпапкам начальной папки
    for root, dirs, file_names in os.walk(filepath):
        # Проход по всем файлам текущей папки
        for filename in file_names:
            # Если имя файла не встречается в списке имен
            # Добавляем имя в список имен, путь в список путей
            if filename not in list_of_files:
                list_of_files.append(filename)
                list_of_dirs.append({root})
            else:  # Имя файла уже было
                file_1 = pth.join(root, filename)
                file_2 = pth.join(list_of_dirs[list_of_files.
                                  index(filename)].pop(), filename)
                # Проверяем, одинаковый ли размер файлов
                # Если да, то добавляем путь до второго файла в множество
                if not pth.samefile(file_1, file_2) and\
                   pth.getsize(file_1) == pth.getsize(file_2):
                    list_of_dirs[list_of_files.index(filename)].update({root,
                                                        pth.dirname(file_2)})
                else:
                    list_of_dirs[list_of_files.index(filename)].\
                                  update({pth.dirname(file_2)})
                    list_of_files.append(filename)
                    list_of_dirs.append({root})
    # В списке путей ищем множества, имеющие больше одного элемента
    # Это значит, что файл посторялся
    # Создаем список посторяющихся файлов, который будем возвращать
    for i in range(len(list_of_files)):
        if len(list_of_dirs[i]) > 1:
            duplicate_files.append([list_of_files[i], list_of_dirs[i]])
    return duplicate_files


if __name__ == '__main__':
    root_dir = input('Введите папку: ')
    if not pth.isdir(root_dir):
        print('Это не папка')
    else:
        duplicate_files = search_duplicate_files(root_dir)
        if not duplicate_files:
            print('Повторяющихся файлов не найдено')
        else:
            for file in duplicate_files:
                print('------------------------------------')
                print('Файл', file[0], 'повторяется в папках: ')
                for dir in file[1]:
                    print(dir)
                answer = input('Удалить повторяющиеся файлы?(y/n) ')
                if answer == 'y' or answer == 'yes':
                    # Удаляем файлы
                    rem_files = list()  # Список файлов для удаления
                    for path in sorted(file[1]):
                        rem_files.append(pth.join(path, file[0]))
                    for i in range(len(rem_files)-1):
                        os.remove(rem_files[i])
                    # Не удаленным останется последний файл из списка rem_files
                    print('Копии удалены. Файл лежит в',
                          pth.dirname(rem_files[len(rem_files)-1]))
                print()
