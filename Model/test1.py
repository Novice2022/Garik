# <>------------------------<> First <>------------------------<> #

A = input("Введите массив A (значения через пробел): ").split()
B = input("Введите массив B (значения через пробел): ").split()

C = []

for i in range(2):
    C.append(A[i])
    C.append(B[i])

print(f"Массив А: {A}")
print(f"Массив B: {B}")
print(f"Ответ (массив C): {C}")


# <>------------------------<> Second <>------------------------<> #

A = open("A.dat").readline().split()
B = open("B.dat").readline().split()
C = []

for i in range(min(len(A), len(B))):
    C.append(int(A[i]))
    C.append(-int(B[i]))

print(f"Массив А: {A}")
print(f"Массив B: {B}")
print(f"Ответ (массив C): {C}")
