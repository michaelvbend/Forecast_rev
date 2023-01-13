
## Documentation

### Load_data()

This code contains a function called "load_data()" that uses the Pandas library to read in and process 
a CSV file. Here is an explanation of what happens in the code:
1. The function starts by defining the variable "file" as the path to a file called "data.csv" in a 
folder called "static". This is the dataset with the advertisement data.

2. The function uses the Pandas function "pd.read_csv(file)" to read the contents of the CSV 
file into a DataFrame called "df".

3. The function uses the "[ ]" property of DataFrame to select only specific columns: 
"reporting_start", "reporting_end", "spent", "impressions", "clicks" and "campaign_id".

4. The function uses the DataFrame's dropna() function to remove the rows containing missing 
values.

5. The function calculates the quantile (0.01) and (0.99) of the "spent" column with no missing 
values.

6. The function filters the DataFrame by retaining only rows where the "spent" value is smaller 
than the calculated quantile (0.99) and larger than the calculated quantile (0.01)

7. The function returns the filtered DataFrame.

### Transform_data()

This code contains a function called "transform_data()" that processes data by filtering and 
transforming it into a suitable format for use in a statistical model. Here is an explanation of what 
happens in the code:
1. The function takes two arguments, a DataFrame called "df" and two strings "dependent" 
and "campaign".

2. The function uses the "[ ]" property of DataFrame to create a filtered DataFrame where the 
"campaign_id" column equals the "campaign" string.

3. The function defines the variable "y" as the values of the "dependent" column of the filtered 
DataFrame, using the values property and reshape() function to put the data in the right 
format for use in a model.

4. The function defines the variable "x" as the values of the "spent" column of the filtered 
DataFrame, using the values property and reshape() function to bring the data into the 
correct format for use in a model.

5. The function returns a tuple with the x and y data used for the model
This function can be used to filter the data based on a specific campaign and transform the data into 
a format suitable for use in a statistical model.

### Train_model()
This code contains a function called "train_model()" that trains a linear regression model based on 
two input arguments (x, y). Here is an explanation of what happens in the code:
1. The function takes two arguments, "x" and "y" prepared in an earlier step and corresponding 
to the independent and dependent variable.

2. The function imports the LinearRegression class from the sklearn.linear_model library and 
creates an instance of the class called "regressor".

3. The function applies the model to the data (x, y) using the "fit()" method of the regressor 
instance. This trains the model on the given data.

4. The function calculates the coefficients of the linear regression (coef) and the y-intercept 
(intercept) of the linear regression by using the respective regressor properties "coef_" and 
"intercept_".

5. The function returns a tuple with the coefficients and y-intercept calculated while training 
the model.
This function can be used to train a linear regression model based on the given data and determine 
the coefficients and y-intercept of the model. This data can then be used to make predictions using 
the trained model.

### Predict()
This code contains a function called "predict()" that makes a prediction for a given value of the 
independent variable based on a linear regression model. Here is an explanation of what happens in 
the code:
1. The function takes three arguments: "slope" and "interc" which represent the coefficients 
and y-intercept of the linear regression model, and "eu" which is the value of the 
independent variable for which to make the prediction.

2. The function returns the prediction for the dependent variable by using the formula of a 
linear regression model, y = slope * x + interc. The value of x (eu) is multiplied by the slope 
and added to the interc after which the result is rounded to 2 decimal places

3. The function returns the prediction as a float.
This function can be used to make predictions using a linear regression model. The user must 
provide the coefficients and y-intercept of the model as arguments and the value of the 
independent variable for which the prediction is to be made. The function then returns the 
prediction for the dependent variable.

### Evaluate()
This code contains a function called "evaluate()" that is used to evaluate the model on the given 
dataset. Here is an explanation of what happens in the code:
1. The function takes five arguments: a DataFrame called "df", "coef" and "interc" that 
represent the coefficients and y-intercept of the linear regression model, "campaign" is the 
campaign for which the evaluation is to be done and "target" is the column on which the 
evaluation is to be done.

2. The function filters the DataFrame to retain only data corresponding to the given campaign.

3. The function defines "y_actual" as the values of the "target" column of the filtered 
DataFrame.

4. The function creates a new column "prediction" in the DataFrame using the apply() method 
and lambda function. This column contains the predictions for the dependent variable, 
calculated using the formula y = coef * x + interc.

5. The function uses the mean_absolute_error(), mean_squared_error() and r2_score() 
functions from the sklearn.metrics library to determine the MAE, MSE, RMSE and R^2 score 
of the model and stores them in mae, mse and rs, respectively.

6. The function calculates the correlation between the target column and the spent column 
using the corr() method of the dataframe

7. The function returns a list of the calculated MAE, MSE, RMSE, R^2 score and correlation 
between the target and spent column
This function can be used to evaluate the model based on the given dataset. The user has to provide 
the DataFrame, coefficients and y-intercept of the model, campaign and target column as 
arguments. The function then returns a list of the MAE, MSE, RMSE, R^2 score and correlation 
between the target and spent column, which can be used to determine how well the model is 
performing.

### Create_report()
This function, called create_report, generates a report/message for the end user to interpret the 
evaluation values. It takes 4 input parameters: r2, correlation, mae, mse. These are respectively the 
R-squared value, correlation, Mean Absolute Error and Mean Squared Error of a model.
The report is constructed in 3 parts: for R2, MAE and MSE. For each part, the helper function 
helper_report is used to determine the performance of the model.
Based on the performance of R2, MAE and MSE, a total score is calculated. If the total score is 6, 
'good' is returned, if the score is greater than or equal to 2, 'neutral' is returned and 'bad' otherwise

