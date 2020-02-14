from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler


# Load the model we trained previously
predictor = joblib.load('trained_house_bp_model.pkl')
predictor_sc= joblib.load('trained_house_bp_scaler.pkl')

# For the house we want to value, we need to provide the features in the exact same
# arrangement as our training data set.
house_to_value = [ #280000
    1975,  # year_built
    1,  # num_bedrooms
    2000,  # total_sqft
    600,  # garage_sqft
]

house_to_value2 = [#530000
    1985,  # year_built
    2,  # num_bedrooms
    2750,  # total_sqft
    600,  # garage_sqft
]

# scikit-learn assumes you want to predict the values for lots of houses at once, so it expects an array.
# We just want to look at a single house, so it will be the only item in our array.
homes_to_value = [
    house_to_value,
    house_to_value2,

    [
        1985,  # year_built
        4,  # num_bedrooms
        3000,  # total_sqft
        1200,  # garage_sqft
    ]
]

#scale the input data with the scale factor we used for the training & test data
homes_to_value = predictor_sc.transform(homes_to_value)
predicted_home_values = predictor.predict(homes_to_value)

# Since we are only predicting the price of one house, just look at the first prediction returned
predicted_value = predicted_home_values[0]

for val in predicted_home_values:
    print("This house has an estimated value of ${:,.2f}".format(val))
