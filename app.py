import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app
st.title("Linear Programming Solver & Visualizer")

# Define problem
st.sidebar.header("Define the Problem")
c1 = st.sidebar.number_input("Coefficient of x1 in objective function", value=3.0)
c2 = st.sidebar.number_input("Coefficient of x2 in objective function", value=4.0)
c = [-c1, -c2]  # Negate for maximization

a11 = st.sidebar.number_input("Coefficient of x1 in 1st constraint", value=2.0)
a12 = st.sidebar.number_input("Coefficient of x2 in 1st constraint", value=3.0)
b1 = st.sidebar.number_input("RHS of 1st constraint", value=12.0)

a21 = st.sidebar.number_input("Coefficient of x1 in 2nd constraint", value=4.0)
a22 = st.sidebar.number_input("Coefficient of x2 in 2nd constraint", value=1.0)
b2 = st.sidebar.number_input("RHS of 2nd constraint", value=8.0)

A = [[a11, a12], [a21, a22]]
b = [b1, b2]
x_bounds = (0, None)  # x1, x2 >= 0

# Solve using scipy.optimize.linprog
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds], method='highs')

if result.success:
    optimal_value = -result.fun
    optimal_solution = result.x
    st.write("### Optimal Solution Found")
    st.write(f"Optimal value: {optimal_value}")
    st.write(f"Optimal solution: x1 = {optimal_solution[0]:.2f}, x2 = {optimal_solution[1]:.2f}")
else:
    st.write("### No Solution Found")
    st.write(result.message)

# Visualization
st.write("### Feasible Region and Optimal Solution")

x1 = np.linspace(0, 10, 400)
x2_1 = (b1 - a11 * x1) / a12
x2_2 = (b2 - a21 * x1) / a22

plt.figure(figsize=(8, 6))
plt.plot(x1, x2_1, label=f"${a11}x_1 + {a12}x_2 \leq {b1}$")
plt.plot(x1, x2_2, label=f"${a21}x_1 + {a22}x_2 \leq {b2}$")
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.fill_between(x1, 0, np.minimum(x2_1, x2_2), where=(x2_1 >= 0) & (x2_2 >= 0), color='gray', alpha=0.5)
plt.scatter(*optimal_solution, color="red", label="Optimal Solution")
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.legend()
plt.title("Feasible Region and Optimal Solution")
plt.grid(True)

st.pyplot(plt)
