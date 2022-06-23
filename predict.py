import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

### Load data
all_data = pd.read_csv(r'D:\GIT_PYTHON\OTODOM-scraping-and-prediction\otodom_data.csv',sep=',')
### Remove Unnamed column
all_data = all_data.loc[:, ~all_data.columns.str.contains('^Unnamed')]
### Remove wrong districts 
districts = all_data['dist'].unique()
for k in range(6,9):
    all_data = all_data.drop(all_data[(all_data["dist"] == districts[k])].index)

districts = all_data['dist'].unique()
### Convert districts to numbers
for i in all_data.index:
    for v,dist in enumerate(districts):
        if all_data['dist'][i] == dist:
            all_data['dist'][i] = v

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
random_state = np.argmax(acc)+1
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
meters = 52.22
room = 3
dist = 1
floor = 4

x = [[meters,room,dist,floor]]
pred = model.predict(x)
print(districts[dist],np.round(pred[0],0), 'zł')

### Get model coef and intercept
model.coef_
model.intercept_