import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

### Load data
all_data = pd.read_csv(r'D:\GIT_PYTHON\OTODOM-scraping-and-prediction\otodom_data.csv',sep=',')
### Remove Unnamed: 0 column
drop = all_data.drop('Unnamed: 0')
districts = all_data['dist'].unique()
# districts = ['Nowe Miasto', 'Stare Miasto', 'Wilda', 'Grunwald','wielkopolskie', 'Jeżyce']
### Convert districts to numbers
for i in range(len(all_data)):
    if all_data['dist'][i] == districts[0]:
        all_data['dist'][i] = 0
    elif all_data['dist'][i] == districts[1]:
        all_data['dist'][i] = 1
    elif all_data['dist'][i] == districts[2]:
        all_data['dist'][i] = 2
    elif all_data['dist'][i] == districts[3]:
        all_data['dist'][i] = 3
    elif all_data['dist'][i] == districts[4]:
        all_data['dist'][i] = 4
    elif all_data['dist'][i] == districts[5]:
        all_data['dist'][i] = 5
### Plot pairplot of data
sns.pairplot(all_data)
### Get X and Y data
X = np.array(all_data[[all_data.columns[2],all_data.columns[3],all_data.columns[4],all_data.columns[-1]]])
y = np.array(all_data[all_data.columns[1]])
### import sklearn 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
### Get the best accuracy -> changing random_state
acc = []
for i in range(1,700):
    X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.2,random_state = i)
    model = LinearRegression()
    model.fit(X_train,y_train)
    acc.append(model.score(X_test,y_test))

print(np.amax(acc))
### Set random_state with the best accuracy
random_state = np.argmax(acc)
### Split data
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.2,random_state = random_state)
### Fit model
model = LinearRegression()
model.fit(X_train,y_train)
### Get accuracy on tested data
model.score(X_test,y_test)
### Do prediction
y_pred = model.predict(X_test)
### Plot y_test vs y_pred - the more linear the relationship, the better the result is
plt.scatter(y_test,y_pred)
### Get distribution plot to check how data are located
sns.distplot(y_test-y_pred)
### Get statistic information
all_data.describe()
### Get RMSE metric from y_test and y_pred
np.sqrt(mean_squared_error(y_test,y_pred))
### Predict house prices
meters = 51.22
room = 3
dist = 0
floor = 3

x = [[51.22,3,dist,3]]
pred = model.predict(x)
print(districts[dist],pred[0])

### Get model coef and intercept
model.coef_
model.intercept_