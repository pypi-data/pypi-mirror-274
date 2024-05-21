def binary_float_to_decimal(binary_str):
    if '.' in binary_str:
        # Разделяем строку на целую и дробную части
        whole_part, fractional_part = binary_str.split('.')
    else:
        whole_part = binary_str
        fractional_part = ''
    # Переводим целую часть
    decimal_value = 0
    for index, digit in enumerate(whole_part[::-1]):
        decimal_value += int(digit) * (2 ** index)
    # Переводим дробную часть
    for index, digit in enumerate(fractional_part):
        decimal_value += int(digit) * (2 ** -(index + 1))
    return decimal_value
def octal_float_to_decimal(octal_str):
    if '.' in octal_str:
        # Разделяем строку на целую и дробную части
        whole_part, fractional_part = octal_str.split('.')
    else:
        whole_part = octal_str
        fractional_part = ''
    # Переводим целую часть
    decimal_value = 0
    for index, digit in enumerate(whole_part[::-1]):
        decimal_value += int(digit) * (8 ** index)
    # Переводим дробную часть
    for index, digit in enumerate(fractional_part):
        decimal_value += int(digit) * (8 ** -(index + 1))
    return decimal_value
# Таблицы соответствия для шестнадцатеричных и двоичных чисел
hex_to_bin = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111"
}
def hex_to_binary(hex_str):
    # Проверка на наличие дробной части
    if '.' in hex_str:
        whole_part, fractional_part = hex_str.split('.')
    else:
        whole_part = hex_str
        fractional_part = ''
    # Перевод целой части
    binary_whole_part = ''.join([hex_to_bin[digit] for digit in whole_part])
    # Перевод дробной части
    binary_fractional_part = ''.join([hex_to_bin[digit] for digit in fractional_part])
    if fractional_part:
        return f"{binary_whole_part}.{binary_fractional_part}"
    else:
        return binary_whole_part
import struct
def float_to_hex_single(f, d=127):
    # Проверка, что смещение d в пределах допустимого диапазона
    if not (0 <= d < 256):
        raise ValueError("Смещение d должно быть в диапазоне от 0 до 255")

    # Проверка знака числа
    sign = 0
    if f < 0:
        sign = 1
        f = -f

    # Разделение числа на целую и дробную части
    int_part = int(f)
    frac_part = f - int_part

    # Представление целой части в двоичной системе
    int_part_bin = bin(int_part)[2:]

    # Представление дробной части в двоичной системе
    frac_part_bin = []
    while frac_part and len(frac_part_bin) < 23:
        frac_part *= 2
        bit = int(frac_part)
        frac_part_bin.append(str(bit))
        frac_part -= bit

    frac_part_bin = ''.join(frac_part_bin)

    # Нормализация числа
    if int_part != 0:
        exponent = len(int_part_bin) - 1
        mantissa = int_part_bin[1:] + frac_part_bin
    else:
        first_one_index = frac_part_bin.index('1')
        exponent = -first_one_index - 1
        mantissa = frac_part_bin[first_one_index+1:]

    mantissa = mantissa[:23]  # Обрезаем до 23 бит
    if len(mantissa) < 23:
        mantissa += '0' * (23 - len(mantissa))

    # Вычисление смещенного порядка
    exp = exponent + d
    exp_bin = bin(exp)[2:].zfill(8)

    # Формирование окончательной двоичной строки
    final_bin = f'{sign}{exp_bin}{mantissa}'

    # Перевод в шестнадцатеричную систему
    hex_str = hex(int(final_bin, 2))[2:].upper()
    return hex_str.zfill(8)
