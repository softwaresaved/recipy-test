import recipy
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file-import.csv", data, delimiter=",")
