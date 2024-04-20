import re

def format_phone_number(number):
    # Удаление всех нецифровых символов
    cleaned_text = re.sub(r'\D', '', number)

    # Проверка, что осталось ровно 10 цифр
    if len(cleaned_text) == 10:
        return 'Номер верно введет'
    else:
        return 'Номер должен содержать ровно 10 цифр после удаления всех нецифровых символов'

# Пример использования
print('Введите номер телефона:')
number = input()
print(format_phone_number(number))