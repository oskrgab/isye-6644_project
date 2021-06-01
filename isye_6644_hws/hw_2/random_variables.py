from scipy.stats import uniform
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%%
U = uniform.rvs(size=1000)
V = uniform.rvs(size=1000)

Z = np.sqrt(-2 * np.log(U)) * np.cos(2 * np.pi * V)
sns.distplot(Z)
plt.show()
