numbers = {
    "ноль": 0, "одна": 1, "один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,
    "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14, "пятнадцать": 15,
    "шестнадцать": 16, "семнадцать": 17, "восемнадцать": 18, "девятнадцать": 19,
    "двадцать": 20, "тридцать": 30, "сорок": 40, "пятьдесят": 50, "шестьдесят": 60,
    "семьдесят": 70, "восемьдесят": 80, "девяносто": 90
}
reversed_numbers = {value: key for key, value in numbers.items()}

def text_to_num(text):
    if ' и ' in text:
        integer_part, decimal_part = text.split(' и ')
        integer_num = text_to_num(integer_part)
        decimal_text = decimal_part.split()
        if 'десятая' in decimal_part or 'десятых' in decimal_part:
            factor = 10
        elif 'сотая' in decimal_part or 'сотых' in decimal_part:
            factor = 100
        elif 'тысячная' in decimal_part or 'тысячных' in decimal_part:
            factor = 1000
        else:
            return ValueError(f'Неизвестный формат дробной части: {decimal_part}')
        decimal_num = text_to_num(" ".join(decimal_text[:-1])) / factor
        return integer_num + decimal_num
    parts = text.split()
    if not parts:
        return None
    number = 0
    negative = False
    if parts[0] == 'минус':
        negative = True
        parts = parts[1:]
    for part in parts:
        if part in numbers:
            number += numbers[part]
        else:
            return ValueError(f"Ошибка: не удалось распознать часть числа '{part}'")
    return -number if negative else number

def num_to_text(num):
    if num == 0:
        return 'ноль'

    integer_part = int(num)
    decimal_part = num - integer_part
    parts = []

    for value in sorted(reversed_numbers.keys(), reverse=True):
        if value == 0:
            continue
        while integer_part >= value:
            parts.append(reversed_numbers[value])
            integer_part -= value

    result = " ".join(parts)

    if decimal_part > 0:
        decimal_part_as_int = int(round(decimal_part * 100))
        if decimal_part_as_int == 0:
            return result

        decimal_text = num_to_text(decimal_part_as_int)
        result += f" и {decimal_text} сотых"

    return result


def calc(expression):
    expression = expression.strip().replace("  ", " ").replace(" на ", " ")
    if 'минус минус' in expression:
        expression = expression.replace('минус минус', 'плюс')
    if len(expression.split()) < 3:
        return 'Неверный формат выражения'
    if 'плюс' in expression:
        operation = 'плюс'
    elif 'минус' in expression:
        operation = 'минус'
    elif 'умножить' in expression:
        operation = 'умножить'
    elif 'разделить' in expression:
        operation = 'разделить'
    else:
        return 'Неверная операция'

    left, right = expression.split(f' {operation} ')
    left_num = text_to_num(left)
    right_num = text_to_num(right)

    if left_num is None or right_num is None:
        return 'Ошибка: неверный формат чисел'

    if operation == 'плюс':
        result = left_num + right_num
    elif operation == 'минус':
        result = left_num - right_num
    elif operation == 'умножить':
        result = left_num * right_num
    elif operation == 'разделить':
        if right_num == 0:
            return 'Ошибка: деление на ноль'
        result = left_num / right_num

    else:
        return 'Ошибка: неверная операция'
    return num_to_text(result)

while True:
    expression = input('Введите выражение (<число> <операция> <число>): ')
    if expression.lower() == 'стоп':
        break
    print('Результат: ' + calc(expression))