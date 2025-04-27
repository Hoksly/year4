from geometry import *

def try_parse_int(s):
    try:
        try:
            qq = float(s)
            if '.' in s in s:
                print(f"Помилка: {s} не є ЦІЛИМ числом, спробуйте ще раз")
                return None
        except ValueError:
            pass
        
        res = int(s)
        
        if not (-127 <= res <= 127):
            print(f"Число {res} поза діапазоном [-127; 127], спробуйте ще раз")
            return None
        return res
    except ValueError:
        print(f"Помилка: {s} не є ЦІЛИМ числом, спробуйте ще раз")
        return None

def validate_a_b(a, b):
    if a**2 + b**2 != 0:
        return True
    print("Помилка: A^2 + B^2 != 0, спробуйте ще раз")
    return False

def try_input_A_B():
    while True:
        while True:
            A = try_parse_int(input("a (для Ax+By+C=0): "))
            if A is not None:
                break
            
        while True:
            B = try_parse_int(input("b (для Ax+By+C=0): "))
            if B is not None:
                break
        if validate_a_b(A, B):
            return A, B

def try_parse_b(b, index):
    b = try_parse_int(b)
    if b is not None:
        if b == 0:
            print(f"b{index} не може бути 0, спробуйте ще раз")
            return None
        return b



def try_input_b(index):
    while True:
        b = input(f"b{index} (для y=k{index}x+b{index}): ")
        b = try_parse_b(b, index)
        if b is not None:
            return b

def main():
    N = 127  # Згідно з варіантом
    print("Введіть параметри трьох прямих:")
    
    # Введення даних
    try:
        a, b = try_input_A_B()
        c = try_parse_int(input("c (для Ax+By+C=0): "))

        while c is None:
            c = try_parse_int(input("c (для Ax+By+C=0): "))
        
        k1 = try_parse_int(input("k1 (для y=k1x+b1): "))
        while k1 is None:
            k1 = try_parse_int(input("k1 (для y=k1x+b1): "))
        b1 = try_input_b(1)

        k2 = try_parse_int(input("k2 (для y=k2x+b2): "))
        while k2 is None:
            k2 = try_parse_int(input("k2 (для y=k2x+b2): "))
        b2 = try_input_b(2)
                
    except ValueError as e:
        print(f"Помилка: {e}")
        return

    # Convert input to line format
    line1 = {'A': a, 'B': b, 'C': c}
    line2 = {'A': -k1, 'B': 1, 'C': -b1}  # Convert y = k1x + b1 to -k1x + y - b1 = 0
    line3 = {'A': -k2, 'B': 1, 'C': -b2}  # Convert y = k2x + b2 to -k2x + y - b2 = 0
    
    # Classify the lines
    classification, points = classify_lines(line1, line2, line3)
    
    # Output results based on classification
    print()
    if classification == 1:
        print("Прямі співпадають")
    elif classification == 2:
        print("Прямі паралельні або деякі співпадають")
    elif classification == 3:
        print("Прямі перетинаються в одній точці")
        print(f"Точка перетину: ({points[0][0]:.5f}, {points[0][1]:.5f})")
    elif classification == 4:
        print("Прямі перетинаються в двох точках")
        for i, point in enumerate(points, 1):
            print(f"Точка {i}: ({point[0]:.5f}, {point[1]:.5f})")
    elif classification == 5:
        print("Прямі перетинаються в трьох різних точках")
        for i, point in enumerate(points, 1):
            print(f"Точка {i}: ({point[0]:.5f}, {point[1]:.5f})")
    else:
        print("Невідомий випадок взаємного розташування прямих")

if __name__ == "__main__":
    while True:
        print()
        main()