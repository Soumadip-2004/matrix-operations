import streamlit as st
from new_matrix import Matrix
from fraction import Fraction


# ---------------------------------------------------------------------------
# Core parsing logic (same rules as the terminal program)
# ---------------------------------------------------------------------------
def parse_element(token):
    """Convert a single input token into int, float, or Fraction."""
    token = token.strip()
    if token == "":
        raise ValueError("Empty cell — please fill in every value.")
    if '/' in token:
        num_str, den_str = token.split('/')
        return Fraction(int(num_str.strip()), int(den_str.strip()))
    elif '.' in token:
        return float(token)
    else:
        return int(token)


TWO_MATRIX_OPS = {"Addition", "Subtraction", "Multiplication"}
ONE_MATRIX_OPS = {"Transpose", "Determinant", "Adjoint", "Inverse"}


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Matrix Calculator", page_icon="🔢", layout="centered")

st.title("🔢 Matrix Calculator")
st.caption(
    "Supports whole numbers (5), decimals (2.5), and fractions (3/4) — "
    "mixed freely in the same matrix."
)

with st.expander("📋 Instructions", expanded=False):
    st.markdown(
        "- **Addition / Subtraction** need two matrices of the **exact same size**.\n"
        "- **Multiplication** needs Matrix A's columns to equal Matrix B's rows.\n"
        "- **Transpose, Determinant, Adjoint, Inverse** work on a **single** matrix.\n"
        "- **Determinant, Adjoint, Inverse** additionally require a **square** matrix.\n"
        "- Enter each cell as an int (`5`), a decimal (`2.5`), or a fraction (`3/4`)."
    )

operation = st.selectbox(
    "What operation do you want to perform?",
    ["Addition", "Subtraction", "Multiplication", "Transpose", "Determinant", "Adjoint", "Inverse"],
)


# ---------------------------------------------------------------------------
# Reusable matrix-input widget: pick dimensions, then a grid of cells appears
# ---------------------------------------------------------------------------
def matrix_input(label, key_prefix):
    st.subheader(label)
    dim_col1, dim_col2 = st.columns(2)
    rows = dim_col1.number_input(
        "Rows", min_value=1, max_value=8, value=2, step=1, key=f"{key_prefix}_rows"
    )
    cols = dim_col2.number_input(
        "Columns", min_value=1, max_value=8, value=2, step=1, key=f"{key_prefix}_cols"
    )

    st.write(f"Enter the {rows * cols} values for a {rows}×{cols} matrix:")
    grid = []
    for i in range(rows):
        row_cols = st.columns(cols)
        row_values = []
        for j in range(cols):
            val = row_cols[j].text_input(
                label=f"{key_prefix}_{i}_{j}",
                value="0",
                key=f"{key_prefix}_cell_{i}_{j}",
                label_visibility="collapsed",
            )
            row_values.append(val)
        grid.append(row_values)
    return grid


matrix_a_raw = matrix_input("Matrix A", "a")

matrix_b_raw = None
if operation in TWO_MATRIX_OPS:
    matrix_b_raw = matrix_input("Matrix B", "b")


# ---------------------------------------------------------------------------
# Calculate
# ---------------------------------------------------------------------------
if st.button("Calculate", type="primary"):
    try:
        data_a = [[parse_element(cell) for cell in row] for row in matrix_a_raw]
        matrix_a = Matrix(data_a)

        matrix_b = None
        if operation in TWO_MATRIX_OPS:
            data_b = [[parse_element(cell) for cell in row] for row in matrix_b_raw]
            matrix_b = Matrix(data_b)

        if operation == "Addition":
            result = matrix_a + matrix_b
        elif operation == "Subtraction":
            result = matrix_a - matrix_b
        elif operation == "Multiplication":
            result = matrix_a * matrix_b
        elif operation == "Transpose":
            result = matrix_a.transpose()
        elif operation == "Determinant":
            result = matrix_a.determinant()
        elif operation == "Adjoint":
            result = matrix_a.adjoint()
        elif operation == "Inverse":
            result = matrix_a.inverse()

        st.success("Result:")
        st.code(str(result), language=None)

    except ZeroDivisionError as e:
        st.error(f"Error: {e}")
    except ValueError as e:
        st.warning(f"⚠️ {e}")
    except Exception as e:
        st.error(f"Invalid input: {e}")