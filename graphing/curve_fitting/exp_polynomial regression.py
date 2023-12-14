# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


# %%
data = [
    (6, 12),
    (5, 15),
    (7, 10),
    (10, 7),
    (4, 21),
    (12, 6),
    (8, 9),
    (9, 8),
    (15, 5),
    (5, 15)
    # (21.2,3.9),
    # (21.8,3.8),
    # (24.9,3.4)
]
data.sort(key=lambda x: x[0])
xdata: list[float] = []
ydata: list[float] = []
for x, y in data:
    xdata.append(x)
    ydata.append(y)


# %%
degrees = 5


def print_func(*numbers: float):
    return " + ".join(f"{v}x^{{{i}}}" for i, v in enumerate(numbers))


poly = PolynomialFeatures(degree=degrees, include_bias=True)
poly_reg_model = LinearRegression(fit_intercept=False)
xdata2 = [[x] for x in xdata]


model = make_pipeline(poly, poly_reg_model)
model.fit(xdata2, ydata)

new_data = np.linspace(xdata[0], xdata[-1], 1000).reshape(-1, 1)
y_predicted = model.predict(new_data)

plt.scatter(xdata2, ydata)
plt.plot(new_data, y_predicted, c="red")


# %%
print_func(*model.steps[1][1].coef_)


# %%
