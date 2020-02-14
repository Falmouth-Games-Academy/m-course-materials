import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib


from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

import numpy

# Make a data set
from random import *

in_columns= ['year_built','num_bedrooms','total_sqft','garage_sqft','sale_price']

df_in = pd.DataFrame([], columns= in_columns)


room_size_factor = [200,400,600]
garage_size_factor = [0,500,1000]

rand = Random(0)

price_histogram = {}
prices = []


for i in range(0,7500):
    year_built = rand.randint(1940,2020)
    num_bedrooms = rand.randint(1,6)
    total_sqft = num_bedrooms * room_size_factor[rand.randint(0,len(room_size_factor)-1)]
    garage_sqft = garage_size_factor[rand.randint(0,len(garage_size_factor))-1]
    sale_price = ((total_sqft * 200) + (garage_sqft *4)) * ((100 + randrange(-10,10))/100.0)

    range_step = 25000

    price_range = int((sale_price + (range_step-1)) /range_step)*range_step

    if not price_range in price_histogram:
        price_histogram[price_range] = 0

    price_histogram[price_range] += 1
    prices.append(price_range)

    sale_price = float(price_range)


    total_sqft = int((total_sqft + 249)/250)*250

    garage_sqft =int((garage_sqft + 99) / 100) * 100

    year_built = int((year_built / 10) * 10)+5


    temp = pd.DataFrame([[year_built,num_bedrooms,total_sqft,garage_sqft,sale_price]], columns=in_columns)

    df_in = pd.concat([temp, df_in])



#the output values will be an array of sale_prices
y = df_in['sale_price'].values


#Scale input values to make the more useful for the classifier
#remove the sale_price from the input data

sc = StandardScaler()
features_df = df_in.copy()
del features_df['sale_price']

X = sc.fit_transform(features_df)

#X = features_df

# Split the data set in a training set (25%) and a test set (75%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

model = MLPClassifier(max_iter = 2000)

print('doing training ...')
model.fit(X_train, y_train)
print('done training ...')

# Save the trained model to a file so we can use it in other programs
joblib.dump(model, 'trained_house_bp_model.pkl')
joblib.dump(sc, 'trained_house_bp_scaler.pkl')

# Find the error rate on the training set
mse = mean_absolute_error(y_train, model.predict(X_train))
print("Training Set Mean Absolute Error: %.4f" % mse)

# Find the error rate on the test set
mse = mean_absolute_error(y_test, model.predict(X_test))
print("Test Set Mean Absolute Error: %.4f" % mse)

predicted_home_values = model.predict(X)

for val in predicted_home_values:
    print("This house has an estimated value of ${:,.2f}".format(val))


