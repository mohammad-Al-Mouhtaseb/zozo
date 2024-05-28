import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

mental_data = pd.read_csv("Notebooks/dataset/Dataset-Mental-Disorders.csv")
# mental_data['Suicidal thoughts'].replace('YES ', 'YES', inplace=True)
mental_data.drop("Patient Number",axis=1,inplace=True)
ordinal_cols = ['Sadness', 'Euphoric', 'Exhausted', 'Sleep_Dissorder']
categorical_cols = ['Mood_Swing','Suicidal_Thoughts','Anorxia','Authority_Respect','Try_Explanation','Aggressive_Response','Ignore_And_Move_On','Nervous_BreakDown','Admit_Mistakes','Overthinking']
scale_cols= ['Sexual_Activity','Concentration','Optimisim']
preprocessor = ColumnTransformer(transformers=[
        ('encoder_ordinal', OrdinalEncoder(), ordinal_cols),
        ('encoder_nominal', OneHotEncoder(), categorical_cols),
        ('encoder_scale', OrdinalEncoder(),scale_cols)
])

# pipeline chains steps together sequentially
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', MLPClassifier(solver='lbfgs', alpha=1e-5, early_stopping = True, random_state=42))
])

X = mental_data.drop('Expert_Diagnose', axis=1)  # Specify axis=1 to drop columns
y = mental_data['Expert_Diagnose']

# Label encode the target variable 'Diagnoses'
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)

model.fit(X_train, y_train)

def predict(x):
    return model.predict(x)