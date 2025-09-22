# CS4412 : Data Mining
# Kennesaw State University
# Author: Youssef El-Shaer
# Homework 2


import numpy as np
import matplotlib.pyplot as plt  # For plotting
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd


# Read CSV file and return header and data as numpy array
def read_csv(filename):
    with open(filename,'r') as f:
        lines = f.readlines()
    header = lines[0].strip().split(',')
    data = [ line.strip().split(',') for line in lines[1:] ]
    data = np.array(data).astype('float')
    return header,data


# File paths for datasets
filename_one = "data/dataset-one.csv"
filename_two = "data/dataset-two.csv"


# Load data from CSV files
headerOne,dataOne = read_csv(filename_one)
headerTwo,dataTwo = read_csv(filename_two)


# Create DataFrames from loaded data
dfOne = pd.DataFrame(dataOne,columns=headerOne)
dfTwo = pd.DataFrame(dataTwo,columns=headerTwo)


# Define age bins and labels, then assign age groups
bins = [20, 30, 40, 50, 60, 70, 80]
labels = ['20-29','30-39','40-49','50-59','60-69','70-79']
dfTwo['age_group'] = pd.cut(dfTwo['age'], bins=bins, labels=labels, right=False)


# Perform regression on all data in dfOne
def question_one():
    X = dfOne[['exercise']]
    y = dfOne[['cholesterol']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    m = lr.coef_[0][0]
    b = lr.intercept_[0]
    return m, b, mse, r2



# Print regression results and plot for all data
m, b, mse, r2 = question_one()
print("Question One Results:")
print("")
print(f"Slope (m): {m}")
print(f"Intercept (b): {b}")
print(f"Mean Squared Error: {mse}")
print(f"R2 Score: {r2}")
print("")
# Scatter plot and regression line for dfOne
plt.figure()
plt.scatter(dfOne['exercise'], dfOne['cholesterol'], label='Data')  # Plot data points
lr_one = LinearRegression()
lr_one.fit(dfOne[['exercise']], dfOne[['cholesterol']])
y_pred_one = lr_one.predict(dfOne[['exercise']])
plt.plot(dfOne['exercise'], y_pred_one, color='red', label='Regression Line')  # Plot regression line
plt.title('All Data (dfOne)')
plt.xlabel('Exercise')
plt.ylabel('Cholesterol')
plt.legend()
plt.show()


# Perform regression for a specific age group in dfTwo
def question_two(age_group):
    dfT = dfTwo[dfTwo['age_group'] == age_group]
    X = dfT[['exercise']]
    y = dfT[['cholesterol']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    m = lr.coef_[0][0]
    b = lr.intercept_[0]
    return m, b, mse, r2


# Print regression results and plot for each age group
age_groups = ['20-29','30-39','40-49','50-59','60-69','70-79']
print("Question Two Results:")
print("")
for age_group in age_groups:
    m, b, mse, r2 = question_two(age_group)
    print(f"Age Group {age_group} Results:")
    print(f"  Slope (m): {m}")
    print(f"  Intercept (b): {b}")
    print(f"  Mean Squared Error: {mse}")
    print(f"  R2 Score: {r2}")
    print("")
    # Scatter plot and regression line for each age group
    dfT = dfTwo[dfTwo['age_group'] == age_group]
    if not dfT.empty:
        plt.figure()
        plt.scatter(dfT['exercise'], dfT['cholesterol'], label='Data')  # Plot data points
        lr = LinearRegression()
        lr.fit(dfT[['exercise']], dfT[['cholesterol']])
        y_pred = lr.predict(dfT[['exercise']])
        plt.plot(dfT['exercise'], y_pred, color='red', label='Regression Line')  # Plot regression line
        plt.title(f'Age Group {age_group}')
        plt.xlabel('Exercise')
        plt.ylabel('Cholesterol')
        plt.legend()
        plt.show()