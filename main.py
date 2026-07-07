from new_matrix import Matrix
from fraction import Fraction


def parse_element(token):
    """Convert a single input token into int, float, or Fraction."""
    token = token.strip()
    if '/' in token:
        num_str, den_str = token.split('/')
        return Fraction(int(num_str), int(den_str))
    elif '.' in token:
        return float(token)
    else:
        return int(token)


def show_instructions():
    print("=" * 55)
    print("MATRIX OPERATIONS - INSTRUCTIONS")
    print("=" * 55)
    print("1. Addition and subtraction can only be performed")
    print("   between matrices of the exact same size.")
    print("2. For multiplication, the number of columns in")
    print("   Matrix A must equal the number of rows in Matrix B.")
    print("3. Transpose, Determinant, Adjoint, and Inverse are")
    print("   performed on a single matrix.")
    print("4. Determinant, Adjoint, and Inverse require a square matrix")
    print("   (same number of rows and columns).")
    print("=" * 55)


def get_positive_int(prompt):
    """Safely ask for a single positive whole number. Re-prompts on any bad input."""
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("  -> Invalid input. Please enter a single whole number (no spaces, letters, or symbols).")
            continue
        value = int(raw)
        if value <= 0:
            print("  -> Please enter a number greater than zero, becz dimensions are neither 0 nor -ve")
            continue
        return value


def input_matrix(name):
    print(f"\n--- Enter details for Matrix {name} ---")
    rows = get_positive_int("Enter number of rows: ")
    cols = get_positive_int("Enter number of columns: ")

    print(f"Enter {rows * cols} elements for a {rows}x{cols} matrix, row by row.")
    print("Each element can be an int (5), a float (2.5), or a fraction (3/4).")
    data = []
    for i in range(rows):
        while True:
            raw = input(f"Row {i + 1} ({cols} values separated by space): ").split()
            if len(raw) != cols:
                print(f"  -> Please enter exactly {cols} values.")
                continue
            try:
                row = [parse_element(x) for x in raw]
            except (ValueError, ZeroDivisionError) as e:
                print(f"  -> Invalid value ({e}). Please try again.")
                continue
            data.append(row)
            break

    return Matrix(data)


TWO_MATRIX_OPS = {"1", "2", "3"}        # Addition, Subtraction, Multiplication
ONE_MATRIX_OPS = {"4", "5", "6", "7"}   # Transpose, Determinant, Adjoint, Inverse


def choose_operation():
    print("\nWhat operation do you want to perform?")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Transpose")
    print("5. Determinant")
    print("6. Adjoint")
    print("7. Inverse")
    while True:
        choice = input("Enter your choice (1-7): ").strip()
        if choice in TWO_MATRIX_OPS or choice in ONE_MATRIX_OPS:
            return choice
        print("  -> Please enter a number from 1 to 7.")


def perform_operation(choice, a, b=None):
    try:
        if choice == "1":
            print("\nA + B:")
            print(a + b)
        elif choice == "2":
            print("\nA - B:")
            print(a - b)
        elif choice == "3":
            print("\nA * B:")
            print(a * b)
        elif choice == "4":
            print("\nTranspose of Matrix:")
            print(a.transpose())
        elif choice == "5":
            print("\nDeterminant of Matrix:")
            print(a.determinant())
        elif choice == "6":
            print("\nAdjoint of Matrix:")
            print(a.adjoint())
        elif choice == "7":
            print("\nInverse of Matrix:")
            print(a.inverse())
    except ValueError as e:
        print("\nWarning:", e)


def main():
    show_instructions()

    while True:
        choice = choose_operation()

        if choice in TWO_MATRIX_OPS:
            a = input_matrix("A")
            print("\nMatrix A:")
            print(a)

            b = input_matrix("B")
            print("\nMatrix B:")
            print(b)

            perform_operation(choice, a, b)
        else:
            a = input_matrix("A")
            print("\nMatrix A:")
            print(a)

            perform_operation(choice, a)

        print("\n1. Perform another operation")
        print("2. Exit")
        continue_choice = input("Enter your choice (1/2): ").strip()

        if continue_choice != "1":
            print("Exiting program. Goodbye!")
            return   # exit main() entirely


if __name__ == "__main__":
    main()