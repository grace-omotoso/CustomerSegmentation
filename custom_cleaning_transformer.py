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
        
    def transform1(self, df):
        # remove duplicates
        df = df.copy()
        df = df.drop_duplicates()
        # replace string values with floats
        # Convert CAMEO_DEUG_2015 to float
        df = preprocess_df_column(df, 'CAMEO_DEUG_2015', 0, 'X', '-1')
        # Convert CAMEO_DEU_2015 to float
        wlb_dict = dict(zip(df_wlb['wlb_code'], df_wlb['category_value']))
        df = self.preprocess_df_column(df, 'CAMEO_DEU_2015', 0, 'XX', '-1', wlb_dict)
        # Convert CAMEO_INTL_2015 to float
        df = self.preprocess_df_column(df, 'CAMEO_INTL_2015', 0, 'XX', '-1')
        # Convert OST_WEST_KZ to float
        gdr_frg = {'O': 0, 'W': 1}
        df = self.preprocess_df_column(df, 'OST_WEST_KZ', 0, rpl_dict = gdr_frg)
        if has_extras:
            # Convert PRODUCT_GROUP to float
            prdt_grp = {'FOOD': 1, 'COSMETIC': 2, 'COSMETIC_AND_FOOD': 3}
            df = preprocess_df_column(df, 'PRODUCT_GROUP', rpl_dict = prdt_grp)
            # Convert Customer CUSTOMER_GROUP to float
            cust_grp = {'MULTI_BUYER': 1 , 'SINGLE_BUYER': 2}
            df = preprocess_df_column(df, 'CUSTOMER_GROUP', 0, rpl_dict = cust_grp)
        # Most of our columns should now have numeric values. We will drop the ones that do not have float values
        # We have identified the two columns: 'D19_LETZTER_KAUF_BRANCHE' and 'EINGEFUEGT_AM'
        # The column EINGEFUEGT_AM contains timestamp in string format, we will extract the year and drop the other column
        df['EINGEFUEGT_AM'] = pd.to_datetime(df['EINGEFUEGT_AM'])
        df['EINGEFUEGT_AM'] = df['EINGEFUEGT_AM'].dt.year
        df.drop(['D19_LETZTER_KAUF_BRANCHE'], axis = 1, inplace = True )
        # replace all NAN with -1
        df = df.fillna(-1)
        return df
        
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
        
