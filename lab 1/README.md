# Вариант 9: Подсчитать числа, кратные пяти (Императивный стиль)

numbers = [4, 7, 2, 9, 12, 5, 8, 3, 15, 20, -5, 0]

count = 0
multiples_of_five = []
iterations = 0

for number in numbers:
    iterations += 1
    if number % 5 == 0:
        multiples_of_five.append(number)
        count += 1

print("--- Императивный стиль ---")
print("Числа, кратные 5:", multiples_of_five)
print("Количество чисел, кратных 5:", count)
print("Количество итераций цикла:", iterations)
