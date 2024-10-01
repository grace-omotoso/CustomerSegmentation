import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
df_wlb = pd.read_excel('work_life_balance.xlsx', header = 1)
# create a dictionary from the wlb dataframe
wlb_dict = dict(zip(df_wlb['wlb_code'], df_wlb['category_value']))
class DataSetCleaner(BaseEstimator, TransformerMixin):
    
    def fit(self, x, y=None):
        return self

    def transform(self, X):
        # remove duplicates
        X = X.copy()
        X = X.drop_duplicates()
        # get and drop columns with majority NAN
        #X_clean = drop_rows_with_majority_NAN(X)
        # get and drop columns with majority NAN
        #nan_columns = get_columns_with_majority_NAN(X_clean)
        #X_clean.drop(nan_columns, axis=1, inplace=True)
        
        # replace string values with floats
        # Convert CAMEO_DEUG_2015 to float
        X = preprocess_df_column(X, 'CAMEO_DEUG_2015', 0, 'X', '-1')
        
        # Convert CAMEO_DEU_2015 to float
        # wlb_dict = dict(zip(df_wlb['wlb_code'], df_wlb['category_value']))
        X = preprocess_df_column(X, 'CAMEO_DEU_2015', 0, 'XX', '-1', wlb_dict)
        # Convert CAMEO_INTL_2015 to float
        X = preprocess_df_column(X, 'CAMEO_INTL_2015', 0, 'XX', '-1')
        # Convert OST_WEST_KZ to float
        gdr_frg = {'O': 0, 'W': 1}
        X = preprocess_df_column(X, 'OST_WEST_KZ', 0, rpl_dict = gdr_frg)
        # Most of our columns should now have numeric values. We will drop the ones that do not have float values
        # We have identified the two columns: 'D19_LETZTER_KAUF_BRANCHE' and 'EINGEFUEGT_AM'
        # The column EINGEFUEGT_AM contains timestamp in string format, we will extract the year and drop the other column
        X['EINGEFUEGT_AM'] = pd.to_datetime(X['EINGEFUEGT_AM'])
        X['EINGEFUEGT_AM'] = X['EINGEFUEGT_AM'].dt.year
        X.drop(['D19_LETZTER_KAUF_BRANCHE'], axis = 1, inplace = True )
        # replace all NAN with -1
        X = X.fillna(-1)
    
        return X
        
def get_columns_with_majority_NAN(df):
    missing_percentage = df.isna().mean()
    # Select columns where more than 75% of the data is NaN
    columns_with_75_percent_nan = missing_percentage[missing_percentage > 0.75].index
    return list(columns_with_75_percent_nan)

def drop_rows_with_majority_NAN(df):
    missing_percentage_per_row = df.isna().mean(axis=1)
    # Drop rows where more than 50% of the data is NaN
    df_cleaned = df[missing_percentage_per_row <= 0.50]
    return df_cleaned
        
def preprocess_df_column(df, column, nan_value= None, str_to_replace=None, replacement_str=None, rpl_dict=None):
    """ 
        DESC: preprocesses dataframe replacing NAN with appropriate values
        INPUT: a dataframe to be cleaned
        OUTPUT: a clean dataframe
    """
    # Convert CAMEO_DEUG_2015 to string
    if nan_value:
        df[column] = df[column].fillna(nan_value)
    # Some  CAMEO_DEUG_2015 columns have a value of X in them, this makes it difficult to convert to int
    # we will replace those with -1 which is the number given to unknown on the data dictionary
    if str_to_replace:
        df[column].replace(str_to_replace, replacement_str, inplace=True)
    # We should now be able to convert all the column values to integers
    if rpl_dict:
        df = convert_categories_to_int(df, column, rpl_dict)
    df = df.astype({column:'float'})
    return df

def convert_categories_to_int(df, column, category_dict):
    """
        DESC: converts a dataframe column content from string to int
        INPUT: df - dataframe containing data
               column - dataframe column
               category_dict - dictionary with keys are strings to be converted and values as replacement number
        OUTPUT: a dataframe with specified column converted to int
    """
    df[column] = df[column].replace(category_dict)
    return df
        
