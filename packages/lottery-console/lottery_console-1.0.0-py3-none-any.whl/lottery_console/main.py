__author__ = 'VadimTrubay'

import random
import sys
import time
import os
from colorama import init, Fore

init()


def get_ball(amount_num, start_list):

    """
    The get_ball function takes two arguments:
        amount_num - the number of balls to be drawn from the start_list.
        start_list - a list of numbers that will be used as a pool for drawing balls.

    :param amount_num: Determine the number of balls that will be drawn
    :param start_list: Pass the list of balls to the function
    :return: A list of random numbers
    :doc-author: Trelent
    """

    new_list = []
    for i in range(1, amount_num + 1):
        random.shuffle(start_list)
        num = random.choice(start_list)
        start_list.remove(num)
        new_list.append(num)
        print(Fore.GREEN + f'Кулька номер {i} >>>: ' + Fore.WHITE + f'{num}')
        time.sleep(1)
    return new_list


def result_list_ball(new_list):

    """
    The result_list_ball function takes the new_list argument and prints it out in a formatted way.
        The function also uses time.sleep to pause for 1.5 seconds before printing the next line.

    :param new_list: Pass the list of numbers to the function
    :return: A list of balls in the order of their appearance
    :doc-author: Trelent
    """

    print(Fore.MAGENTA + '\nВ порядку випадіння' + Fore.WHITE)
    print(Fore.WHITE + '=' * 20)
    print(', '.join(map(str, new_list)))
    time.sleep(1.5)


def sort_ball_min_max(new_list):

    """
    The sort_ball_min_max function sorts the list of balls from min to max.
        Args:
            new_list (list): The list of balls.

    :param new_list: Pass the list of balls to the function
    :return: A list of sorted balls
    :doc-author: Trelent
    """

    print(Fore.MAGENTA + '\nПосле сортування min > max' + Fore.WHITE)
    print(Fore.WHITE + '=' * 26)
    list_sort = sorted(new_list)
    print(*list_sort, sep=', ')
    time.sleep(1.5)


def main():

    """
    The main function.

    :param:
    :return:
    :doc-author: Trelent
    """
    
    while True:
        os.system('cls')
        print(Fore.RED + 'Генератор лотереї')
        print(Fore.WHITE + '=' * 46)
        amount_num = int(input(Fore.BLUE + 'Введіть кількість номерів для випадіння' + Fore.WHITE +'\n>>>: '))
        amount_all = int(input(Fore.BLUE + 'Введіть загальну кількість номерів' + Fore.WHITE +'\n>>>: '))
        time.sleep(1)
        if amount_all <= amount_num:
            print(Fore.CYAN + '\nПомилка вводу! ')
            print(Fore.RED + 'Загальна кількість номерів не може бути\n'
                             'менша або дорівнювати кількісті номерів для випадіння\n'
                             'спробуйте ще раз\n')
            input(Fore.YELLOW + 'Натисніть Enter для продовження\n')
            continue

        else:
            os.system('cls')
            print(Fore.YELLOW + f'Це {amount_num} випадкових кульок з барабану від 1 до {amount_all}: ')
            print(Fore.WHITE + '=' * 45)
            start_list = list(range(1, amount_all + 1))
            time.sleep(1)

            new_list = get_ball(amount_num, start_list)
            result_list_ball(new_list)
            sort_ball_min_max(new_list)

            while True:
                ex = input(Fore.YELLOW + '\nСпробуємо ще раз? (y/n) >>>: ')
                if ex == 'y':
                    break
                elif ex == 'n':
                    time.sleep(1.5)
                    print(Fore.CYAN + 'До побачення!')
                    sys.exit()


if __name__ == '__main__':
    main()


