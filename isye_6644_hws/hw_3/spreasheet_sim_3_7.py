from scipy.stats import uniform
import numpy as np

n = 1000000
# Costs
tuition = 8400
dormitory = 5400
meals = uniform.rvs(900, 1350-900, size=n)
entertainment = uniform.rvs(600, 1200-600, size=n)
transportation = uniform.rvs(200, 600-200, size=n)
books = uniform.rvs(400, 800-400, size=n)

# Income
scholarship = 3000
parents = 4000
waiting_tables = uniform.rvs(3000, 5000-3000, size=n)
library_job = uniform.rvs(2000, 3000-2000, size=n)

costs = tuition + dormitory + meals + entertainment + transportation + books
income = scholarship + parents + waiting_tables + library_job

loan = np.mean(costs - income)
print(loan)
