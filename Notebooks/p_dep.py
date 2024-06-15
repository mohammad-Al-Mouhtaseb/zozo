import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Dropout
from sklearn.impute import SimpleImputer


# data = pd.read_csv('Notebooks/dataset/b_depressed.csv')


# data.drop(["Survey_id","Ville_id","incoming_own_farm","incoming_agricultural","farm_expenses"],inplace=True,axis=1)
# data.ffill(inplace=True)


# education_labels = ['No Education', 'Primary', 'Secondary', 'High School', 'College']
# education_labels_num = [0,1,2,3,4]
# data['Education_Level'] = pd.cut(data['education_level'], bins=5, labels=education_labels_num, right=False)


# labels_bin_6=['Very Low','Low','Low Medium', 'High Medium', 'High', 'Very High']
# labels_bin_5=['Very Low','Low','Medium', 'High', 'Very High']

# labels_bin_6_num=[0,1,2,3,4,5]
# labels_bin_5_num=[0,1,2,3,4]

# data['gained_asset_Category']=pd.cut(data['gained_asset'], 5,labels=labels_bin_5_num)
# data['Durable_Asset_Category'] =pd.cut(data['durable_asset'], 6,labels=labels_bin_6_num)
# data['Save_Asset_Category'] =pd.cut(data['save_asset'], 6,labels=labels_bin_6_num)
# data['Living_Expenses_Category'] = pd.cut(data['living_expenses'], 6, labels=labels_bin_6_num)
# data['Other_Expenses_Category'] = pd.cut(data['other_expenses'], 6, labels=labels_bin_6_num)
# data['Lasting_Investment_Category'] = pd.cut(data['lasting_investment'],6, labels=labels_bin_6_num)
# data['No_Lasting_Investment_Category'] = pd.cut(data['no_lasting_investmen'], 6, labels=labels_bin_6_num)


# data.drop(["education_level","gained_asset","durable_asset","save_asset","living_expenses","other_expenses","lasting_investment","no_lasting_investmen"],inplace=True,axis=1)


# X = data.drop('depressed',axis=1)
# y = data['depressed']

# imputer = SimpleImputer()
# transformed_X = imputer.fit_transform(X)

# test_size = 0.33
# random_state = 5

# X_train, X_test, y_train, y_test = train_test_split(transformed_X, y, test_size=test_size, random_state=random_state)

# model = Sequential()
# model.add(Dense(36, input_dim=17, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(36, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(36, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(1, activation='sigmoid'))


# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# model.fit(X_train, y_train, epochs = 300, batch_size = 8)


def predict(x):
    # p = model.predict(np.array([x]))
    # if p>=0.5:
    #     p=1
    # else:
    #     p=0
    # return p
    pass