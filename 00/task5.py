def parse_float(s):
    if not s:
        return None
    
    sign = -1 if s[0] == '-' else 1
    if s[0] in '+-':
        s = s[1:]

    parts = s.split('.')
    if len(parts) > 2:
        return None
    
    integer_part = 0
    for char in parts[0]:
        if not char.isdigit():
            return None
        integer_part = integer_part * 10 + (ord(char) - ord('0'))

    fractional_part = 0
    if len(parts) == 2:
        fraction_length = len(parts[1])
        for i, char in enumerate(parts[1]):
            if not char.isdigit():
                return None
            fractional_part = fractional_part * 10 + (ord(char) - ord('0'))
        fractional_part /= 10**fraction_length
    return sign * (integer_part + fractional_part)

def main():
    try:
        s = input("Введите строку: ").strip()
        number = parse_float(s)
        if number is None:
            print("Invalid input")
            return
        result = number * 2
        print(f"{result:.3f}")
    
    except Exception:
        print("Invalid input")

if __name__ == "__main__":
    main()