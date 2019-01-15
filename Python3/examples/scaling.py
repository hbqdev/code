import numpy as np
from sklearn import preprocessing
input_data = np.array([[5.1, -2.9, 3.3],
[-1.2, 7.8, -6.1],
[3.9, 0.4, 2.1],
[7.3, -9.9, -4.5]])

#Min max scaling 
data_scaler_minmax= preprocessing.MinMaxScaler(feature_range=(0,1))
data_scaled_minmax= data_scaler_minmax.fit_transform(input_data)
print("\nMin max scaled data:\n", data_scaled_minmax)


