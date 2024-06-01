import pandas as pd
import numpy as np


def f12(x1, x2):
    return 3 * (x1**2) + 6 * x1 * x2 - 12 * x2 - 72


def f21(x1, x2):
    return 4 * (x2**2) - 8 * x2 + 10 * (x1**2) * x2 - 32 * x1 + 64


x1_min, x1_max = 0, 3
x2_min, x2_max = 0, 2

h = 0.01
x1_values = np.arange(x1_min, x1_max + h, h)
x2_values = np.arange(x2_min, x2_max + h, h)

x1_x2_pairs = [(x1, x2) for x1 in x1_values for x2 in x2_values]
f12_values = [f12(x1, x2) for x1, x2 in x1_x2_pairs]
f21_values = [f21(x1, x2) for x1, x2 in x1_x2_pairs]

df = pd.DataFrame(
    {
        "x1": [x1 for x1, _ in x1_x2_pairs],
        "x2": [x2 for _, x2 in x1_x2_pairs],
        "f12(x1,x2)": f12_values,
        "f21(x1,x2)": f21_values,
    }
)

print(df)
print("\n======================\n")

f12_star = max([min(df[df["x1"] == x1]["f12(x1,x2)"]) for x1 in x1_values])
x1_f12_star = next(
    x1 for x1 in x1_values if min(df[df["x1"] == x1]["f12(x1,x2)"]) == f12_star
)
x2_f12_star = df[(df["x1"] == x1_f12_star) & (df["f12(x1,x2)"] == f12_star)][
    "x2"
].values[0]
print(f"f12* = {f12_star}, x1 = {x1_f12_star}, x2 = {x2_f12_star}")

f21_star = max([min(df[df["x2"] == x2]["f21(x1,x2)"]) for x2 in x2_values])
x2_f21_star = next(
    x2 for x2 in x2_values if min(df[df["x2"] == x2]["f21(x1,x2)"]) == f21_star
)
x1_f21_star = df[(df["x2"] == x2_f21_star) & (df["f21(x1,x2)"] == f21_star)][
    "x1"
].values[0]
print(f"f21* = {f21_star}, x1 = {x1_f21_star}, x2 = {x2_f21_star}")
