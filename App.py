#!/usr/bin/env python
# coding: utf-8

# # Modeling

# ### Import Relevant Libraries

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.filterwarnings("ignore", category = DeprecationWarning)
warnings.filterwarnings("ignore", category = FutureWarning)
warnings.filterwarnings("ignore", category = UserWarning)

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE, RandomOverSampler
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

import time

import streamlit as st


# ### Read in the Data

# In[181]:


df = pd.read_parquet('./Data/mockdraft.parquet')


# In[182]:


df.reset_index(inplace=True)


# In[183]:


df.drop(['index'],axis=1,inplace=True)


# In[184]:


df['year_col'] = df.year_col.astype('Int64')


# In[176]:


st.title('NFL Mock Draft Simulator')


# In[ ]:


st.write("---")
year = st.selectbox('Select Year:',
                   df.year_col.unique())
'You selected: ',year


# ### Create Mock Draft

# In[198]:


if st.button('Mock Draft'):
    year = year
    
    # Implement Random Forest Model (best for Mock Drafting)
    X = df.drop(['Pick_col'],axis=1)
    label_encoder = LabelEncoder()

    X_train = X[X.year_col != year]
    X_test = X[X.year_col == year]
    y_train = label_encoder.fit_transform(df.Pick_col[df.year_col != year])
    y_test = label_encoder.fit_transform(df.Pick_col[df.year_col == year])

    player_name = X_test.player_col
    player_year = X_test.year_col
    player_round = X_test.Round_col
    player_target = X_test.target_col
    player_pos = X_test.pos_col

    X_train.drop(['player_col','year_col','Round_col','target_col'],axis=1,inplace=True)
    X_test.drop(['player_col','year_col','Round_col','target_col'],axis=1,inplace=True)

    num_cols = X_train.select_dtypes(['Int64','float64'])
    cat_cols = X_train.select_dtypes('object')

    num_transformer = Pipeline(steps=[('ss',StandardScaler()),
                                 ('impute',SimpleImputer(strategy='constant'))])

    cat_transformer = Pipeline(steps=[('ohe',OneHotEncoder(drop='first',sparse=False,handle_unknown='ignore'))])

    transformer = ColumnTransformer(transformers=[
        ('num',num_transformer,num_cols.columns),
        ('cat',cat_transformer,cat_cols.columns)
    ])

    # Pipeline for transformations, sampling and the model
    rfc_pipe = Pipeline([
        ('transformer',transformer),
        ('sample',None),
        ('forest',RandomForestRegressor())
    ])

    grid = {
        'sample':[RandomOverSampler(random_state=42),SMOTE(random_state=42)],
        'forest__n_estimators':[102],
        'forest__max_depth':[24],
        'forest__min_samples_split':[2],
        'forest__min_samples_leaf':[6]
    }

    forest = GridSearchCV(estimator=rfc_pipe,
                              param_grid=grid,
                              cv=5)
    forest.fit(X_train, y_train)

    y_pred = forest.predict(X_test)

    results = pd.concat([player_name.reset_index(),player_round.reset_index(),player_year.reset_index(),X_test.reset_index(),pd.Series(y_pred),pd.Series(y_test)],axis=1)
    mock_draft_year = results.sort_values(by=0)
    mock_draft_year['Actual_Pick'] = mock_draft_year[1] + 1
    mock_draft_year['Diff'] = (mock_draft_year[0] - mock_draft_year.Actual_Pick).abs() 
    mock = mock_draft_year[['player_col','Round_col', 'Actual_Pick',0,'Diff','ovr_rk_col']].reset_index()
    mock = mock[['player_col','Round_col', 'Actual_Pick',0,'Diff','ovr_rk_col']]
    mock.columns = ['Player','Drafted_Round','Actual_Pick','Predicted_Pick','Difference','Overall_Rank']
    mock['Predicted_Pick'] = round(mock['Predicted_Pick'],2)
    mock['Difference'] = round(mock.Difference,2)
    mock['Mock_Pick'] = range(1, len(mock) + 1)
    mock['Mock_Difference'] = round(mock.Mock_Pick - mock.Actual_Pick,2)
    final = mock[['Player','Mock_Pick','Actual_Pick','Predicted_Pick','Difference','Mock_Difference','Drafted_Round']]
    final = final.style.background_gradient(cmap='rocket',subset='Difference')
    
    with st.spinner('Simulating...'):
        time.sleep(1)
    
    st.write(final)

