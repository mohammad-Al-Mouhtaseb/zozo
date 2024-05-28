import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import set_config
from sklearn.metrics import accuracy_score
import xgboost as xgb
from xgboost import XGBClassifier

df = pd.read_csv('Notebooks/dataset/panic_disorder_dataset_training.csv')



df_No = df
columns = ['Gender','Family_History','Personal_History','Current_Stressors','Symptoms','Severity','Impact_on_Life','Demographics','Medical_History','Psychiatric_History','Substance_Use','Coping_Mechanisms','Social_Support','Lifestyle_Factors']
# Create a dictionary that maps each categorical value to a unique integer
mapping = {}
category = ''
encoding = 0
for column in columns:
    unique_values = df[column].unique()
    for i, value in enumerate(unique_values):
        mapping[value] = i
        category = value
        encoding = i
        
# Use the `replace()` method to replace the categorical values with their corresponding integers
pd.set_option('future.no_silent_downcasting', True)
df_No = df_No.replace(mapping).infer_objects(copy=False)


filter_b=df_No['Panic_Disorder_Diagnosis'].between(1,3)
mult_condition_filters = df_No[filter_b]


x_train,x_test,y_train,y_test = train_test_split(df_No.drop(columns = ['Panic_Disorder_Diagnosis','Participant_ID'] , axis = 1) , df_No['Panic_Disorder_Diagnosis'] , test_size = 0.3, random_state = 65)

tf1_xgc = ColumnTransformer([('Standard Scaler', StandardScaler(), slice(0,17))])
xgc = XGBClassifier()

pipe_xgc = Pipeline([('StandardScaler',tf1_xgc),('XG Boost Classifier',xgc)])

pipe_xgc.fit(x_train.values,y_train)

mapping["None Demographics"]=2
mapping["None Psychiatric History"]=3
mapping["None Substance Use"]=0

def predict(x):
    return pipe_xgc.predict([x])
