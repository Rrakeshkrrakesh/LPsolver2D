import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

# Set up the Streamlit app
st.title("Interactive Linear Programming Solver & Visualizer")
st.markdown("""
This tool solves and visualizes 2D linear programming problems. 
You can define the objective function and constraints interactively and explore the solution dynamically.
""")

# Objective Function Inputs
st.sidebar.header("Objective Function")
c1 = st.sidebar.slider("Coefficient of x1 (c1)", min_value=-10.0, max_value=10.0, value=3.0)
c2 = st.sidebar.slider("Coefficient of x2 (c2)", min_value=-10.0, max_value=10.0, value=4.0)

# Constraint Management
st.sidebar.header("Constraints")
if "constraints" not in st.session_state:
    st.session_state.constraints = []

if st.sidebar.button("Add Constraint"):
    st.session_state.constraints.append({"a1": 0, "a2": 0, "b": 0, "type": "≤"})

for i, constraint in enumerate(st.session_state.constraints):
    cols = st.sidebar.columns([1, 1, 1, 1])
    st.session_state.constraints[i]["a1"] = cols[0].number_input(
        f"Constraint {i+1}: Coefficient of x1", value=constraint["a1"], key=f"a1_{i}"
    )
    st.session_state.constraints[i]["a2"] = cols[1].number_input(
        f"Constraint {i+1}: Coefficient of x2", value=constraint["a2"], key=f"a2_{i}"
    )
    st.session_state.constraints[i]["b"] = cols[2].number_input(
        f"Constraint {i+1}: RHS value", value=constraint["b"], key=f"b_{i}"
    )
    st.session_state.constraints[i]["type"] = cols[3].selectbox(
        "Type", options=["≤", "≥", "="], key=f"type_{i}", index=["≤", "≥", "="].index(constraint["type"])
    )

# Solve Linear Program
def solve_linear_program(c1, c2, constraints):
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    
    for constraint in constraints:
        a1, a2, b, ctype = constraint.values()
        if ctype == "≤":
            A_ub.append([a1, a2])
            b_ub.append(b)
        elif ctype == "≥":
            A_ub.append([-a1, -a2])
            b_ub.append(-b)
        elif ctype == "=":
            A_eq.append([a1, a2])
            b_eq.append(b)

    bounds = [(0, None), (0, None)]  # x1, x2 >= 0
    result = linprog(
        c=[-c1, -c2],  # Negate for maximization
        A_ub=A_ub if A_ub else None,
        b_ub=b_ub if b_ub else None,
        A_eq=A_eq if A_eq else None,
        b_eq=b_eq if b_eq else None,
        bounds=bounds,
        method="highs"
    )
    return result

result = solve_linear_program(c1, c2, st.session_state.constraints)

# Display Results
if result.success:
    st.write("### Optimal Solution Found")
    st.write(f"**Optimal Value:** {round(-result.fun, 2)}")
    st.write(f"**Optimal Solution:** x1 = {round(result.x[0], 2)}, x2 = {round(result.x[1], 2)}")
else:
    st.error("No feasible solution found.")
    st.write(result.message)

# Visualize the Problem
def visualize_feasible_region(c1, c2, constraints, result):
    x1 = np.linspace(0, 10, 400)
    plt.figure(figsize=(8, 6))

    # Plot each constraint
    for constraint in constraints:
        a1, a2, b, ctype = constraint.values()
        if ctype == "≤":
            x2 = (b - a1 * x1) / a2
            plt.plot(x1, x2, label=f"{a1}x1 + {a2}x2 ≤ {b}")
            plt.fill_between(x1, 0, x2, where=(x2 >= 0), color='gray', alpha=0.2)
        elif ctype == "≥":
            x2 = (b - a1 * x1) / a2
            plt.plot(x1, x2, label=f"{a1}x1 + {a2}x2 ≥ {b}")
            plt.fill_between(x1, x2, 10, where=(x2 >= 0), color='gray', alpha=0.2)
        elif ctype == "=":
            x2 = (b - a1 * x1) / a2
            plt.plot(x1, x2, label=f"{a1}x1 + {a2}x2 = {b}", linestyle="--")

    # Plot optimal solution
    if result.success:
        plt.scatter(result.x[0], result.x[1], color="red", s=100, label="Optimal Solution")
        plt.annotate(
            f"Optimal\n({round(result.x[0], 2)}, {round(result.x[1], 2)})",
            (result.x[0], result.x[1]),
            textcoords="offset points",
            xytext=(-20, 10),
            ha="center",
            color="red",
        )

    # Draw level curves for the objective function
    y = np.linspace(0, 10, 400)
    X, Y = np.meshgrid(x1, y)
    Z = c1 * X + c2 * Y
    plt.contour(X, Y, Z, levels=20, cmap="coolwarm", alpha=0.7)

    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.legend(loc="upper right")
    plt.title("Feasible Region and Optimal Solution")
    plt.grid(True)
    st.pyplot(plt)

visualize_feasible_region(c1, c2, st.session_state.constraints, result)
