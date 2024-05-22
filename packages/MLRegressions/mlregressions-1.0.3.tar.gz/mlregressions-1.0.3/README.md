from MLRegressions import Regressors

Example:

import pandas as pd

df = pd.read_csv('Sampledata.csv')

x = df.iloc[:,1:-1].values # Features

y = df.iloc[:,-1].values # Depended Variable

reg = Regressors(x,y,skip_regressor=[],poly_degree=5, test_size=0.2, random_state=0)

obj = reg.fit_models() # To train Models & return class obj [LinearRegression(), LinearRegression(),
 SVR(), DecisionTreeRegressor(random_state=0), RandomForestRegressor(n_estimators=10, random_state=0)]

Linear Regression     : obj[0].predict()

Polynomial Regression : obj[1].predict()

SVR                   : obj[2].predict()

DecisionTreeRegressor : obj[3].predict()

RandomForestRegressor : obj[4].predict()

data = reg.r2_score() # To get r2_scores data for train test set.

reg.plot_train_data() # To plot graphs for Trained set.



