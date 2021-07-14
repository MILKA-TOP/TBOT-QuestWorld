# Функция, проверяющая, является ли введенная срока числом
def is_digit(number):
    if number.isdigit():
        return True
    else:
        try:
            float(number)
            return True
        except ValueError:
            return False


# Форматированный и аккуратный вывод
def console_out_array(inputArray):
    for i in range(len(inputArray)):
        print("[{}] - {}".format(str(i), str(inputArray[i])))
    print("[{}] - {}".format('-1', 'Отмена'))


# Форматированный и аккуратный вывод для вывода возраста
def console_out_array_age(inputArray):
    print("[{}] - {}".format(str(0), str(inputArray[0])))
    print("Без сопровождения")
    for i in range(1, (len(inputArray) - 1) // 2 + 1):
        print("[{}] - {}".format(str(i), str(inputArray[i])))
    print("С сопровождением")
    for i in range((len(inputArray) - 1) // 2 + 1, len(inputArray)):
        print("[{}] - {}".format(str(i), str(inputArray[i])))
    print("[{}] - {}".format('-1', 'Отмена'))


# Считывание числа
def get_num(max_number):
    print('Введите число от -1 до ' + (str(max_number - 1)))
    value = input().replace(' ', '')
    while not is_digit(value) or (value.isdigit() and (max_number <= int(value) or int(value) < -1)):
        print('Введите число от -1 до ' + (str(max_number - 1)))
        value = input().replace(' ', '')
    return int(value)
