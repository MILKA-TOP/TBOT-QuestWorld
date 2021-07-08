def is_digit(number):
    if number.isdigit():
        return True
    else:
        try:
            float(number)
            return True
        except ValueError:
            return False

def console_out_array(inputArray):
    for i in range(len(inputArray)):
        print("[{}] - {}".format(str(i), str(inputArray[i])))
    print("[{}] - {}".format('-1', 'Отмена'))