import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

import dill
Price_Patent_Reg = dill.load(open('data/features_created.pkd', 'rb'))

Price_Patent_Reg = Price_Patent_Reg.drop([
                                         'drug_age',
                                         'classification_for_rate_setting',
                                         'corresponding_generic_drug_nadac_per_unit',
                                         'pricing_unit',
                                         'ingredient',
                                         'applicant',
                                         'type',
                                         'route',
                                         ], axis = 1)

Price_Patent_Reg = pd.get_dummies(Price_Patent_Reg, drop_first = True)

from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(Price_Patent_Reg,
                                         test_size = 0.2,
                                         random_state = 1,
#                                          shuffle = True
                                        )    #shuffle data to avoid correlation to the natural order of the data

from sklearn import base
class GroupbyEstimator(base.BaseEstimator, base.RegressorMixin):


    def __init__(self, groupby_column, pipeline_factory):
        # column is the value to group by; estimator_factory can be called to produce estimators
        self.groupby_column = groupby_column
        self.pipeline_factory = pipeline_factory


    def fit(self, dataframe, label):
        # Create an estimator and fit it with the portion in each group (create and fit a model per city
        self.drugs_dict = {}
        self.label = label
        self.coefs_dict = {}
        self.intercepts_dict = {}

        dataframe = pd.get_dummies(dataframe)  #onehot encoder had problems with the data, so I'm getting the dummies with pandas here

        for name, values in dataframe.groupby(self.groupby_column):
            y = values[label]
            X = values.drop(columns = [label, self.groupby_column], axis = 1)
            self.drugs_dict[name] = self.pipeline_factory().fit(X, y)
            self.coefs_dict[name] = self.drugs_dict[name].named_steps["lin_reg"].coef_
            self.intercepts_dict[name] = self.drugs_dict[name].named_steps["lin_reg"].intercept_
        return self

    #Method to get the coefficients for each regression
    def get_coefs(self):
        return self.coefs_dict

    #Method to get the intercepts for each regression
    def get_intercepts(self):
        return self.intercepts_dict


    def predict(self, test_data):
        price_pred_list = []

        for idx, row in test_data.iterrows():
            name = row[self.groupby_column]                                 #get drug name from drug column
            regression_coefs = self.drugs_dict[name]                        #get coefficients from fitting in drugs_dict
            row = pd.DataFrame(row).T
            X = row.drop(columns = [self.label, self.groupby_column], axis = 1).values.reshape(1, -1) #Drop ndc and price cols

            drug_price_pred = regression_coefs.predict(X)
            price_pred_list.append([name, drug_price_pred])
        return price_pred_list

def pipeline_factory():
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LinearRegression

    return Pipeline([
                     ('lin_reg', LinearRegression())
                    ])

lin_model = GroupbyEstimator('ndc', pipeline_factory).fit(train_data,'nadac_per_unit')

# Prep data for plotting (from training/testing data)
def format_data(dataframe, filename, test = False):#########
    #change columns to datetime
    if test:
        dataframe.loc[:, 'ndc'] = dataframe.loc[:, 'ndc'].astype('int64')
        dataframe.loc[:, ['effective_date_year', 'effective_date_month', 'effective_date_day']] = dataframe.loc[:, ['effective_date_year', 'effective_date_month', 'effective_date_day']].astype(str)
        dataframe.rename(columns = {'effective_date_year': 'year', 'effective_date_month': 'month', 'effective_date_day': 'day'}, inplace = True)
        dataframe.loc[:, 'date'] = pd.to_datetime(dataframe[['year', 'month', 'day']], format = '%Y-%m-%d')
        dataframe.rename({'year': 'effective_date_year', 'month': 'effective_date_month', 'day': 'effective_date_day'}, inplace = True)
        dataframe.loc[:, ['year', 'month', 'day']] = dataframe.loc[:, ['year', 'month', 'day']].astype(float).astype(int)
        dataframe.sort_values(['ndc', 'date'])
    else:
        dataframe.rename(columns = {'effective_date_year': 'year', 'effective_date_month': 'month', 'effective_date_day': 'day'}, inplace = True)

    #Keep only unique values
    dataframe = dataframe.drop_duplicates(subset = 'ndc')
    return dataframe

#Save formatted data as follows
historical_data = format_data(train_data, 'historical_data', test = True)
prediction_data = format_data(test_data, 'pred_data')

#Attempting new plotting session
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, DataRange1d, HoverTool
from bokeh.plotting import figure

# Set up (initial) data
historical_data = historical_data.loc[:, ['ndc', 'date', 'nadac_per_unit']]
historical_data = historical_data.sort_values('date')
historical_source = ColumnDataSource(historical_data[historical_data.loc[:, 'ndc']=='781593600'])
#
import datetime as dt
# prediction_data.loc[:, 'date'] = dt.datetime(2020, 3, 31)
prediction_data.loc[:, 'year'] = 2020
prediction_data.loc[:, 'month'] = 3
prediction_data.loc[:, 'day'] = 31
first_prediction = lin_model.predict(prediction_data)
first_prediction = pd.DataFrame(data = {'ndc':first_prediction[0][0], 'predictions':first_prediction[0][1][0]}, index = [0]) #these element slices are correct
first_prediction['date'] = pd.to_datetime(prediction_data[['year', 'month', 'day']], infer_datetime_format=True, errors = 'coerce')
prediction_source = ColumnDataSource(first_prediction[first_prediction.loc[:, 'ndc']=='781593600'])

id_list = list(prediction_data['ndc'].astype(str))

# Set up plot
plot = figure(plot_height=800, plot_width=800, title='Drug Price Over Time',
              x_axis_type = 'datetime',
              tools="crosshair, pan, reset, save, wheel_zoom")
plot.x_range = DataRange1d(range_padding = .01)
plot.add_tools(HoverTool(tooltips=[('Date', '@date{%F}'), ('Price', '@nadac_per_unit')],
                                    formatters = {'date': 'datetime'}))

plot.line('date', 'nadac_per_unit', source=historical_source)
plot.scatter('date', 'predictions', source=prediction_source)

# Set up widgets
id_select = Select(title='drug_id', value='781593600', options=id_list)

# Set up callbacks
def update_data(attrname, old, new):

    #Get the current select value
    curr_id = id_select.value
    # Generate the new data
    new_historical = historical_data[historical_data['ndc']==curr_id]
    new_historical = new_historical.sort_values('date')

    prediction_data = prediction_data[prediction_data.loc[:, 'ndc']==curr_id]
    new_prediction_data = lin_model.predict(prediction_data)
    new_prediction_data = pd.DataFrame(data = {'ndc':new_prediction_data[0][0], 'predictions':new_prediction_data[0][1][0]}, index = [0]) #these element slices are correct
    new_prediction_data['date'] = pd.to_datetime(prediction_data[['year', 'month', 'day']], infer_datetime_format=True, errors = 'coerce')
    new_prediction_source = ColumnDataSource(new_prediction_data)
    # Overwrite current data with new data
    historical_source.data = ColumnDataSource.from_df(new_historical)
    # prediction_source.data = ColumnDataSource.from_df(new_predicted)

# Action when select menu changes
id_select.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(id_select)

curdoc().add_root(row(inputs, plot, width = 1000))
curdoc().title = 'Drug Price Predictor'
