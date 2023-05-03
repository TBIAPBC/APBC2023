import math

import numpy as np
from scipy.stats import skewnorm
import matplotlib.pyplot as plt

# Define parameters for the left-skewed normal distribution
a = -2  # skewness parameter
loc = 12  # mode
scale = 8  # standard deviation

# Create the distribution object
rv = skewnorm(a, loc=loc, scale=scale)

print(round(round(rv.pdf(13)*100)))

# Create a range of x-values to plot
x = np.linspace(0, 50, 1000)

# Calculate the y-values for the distribution
y = rv.pdf(x)

# Plot the distribution
plt.plot(x, y)
plt.title('Left-skewed Normal Distribution')
plt.xlabel('x')
plt.ylabel('PDF(x)')
plt.show()