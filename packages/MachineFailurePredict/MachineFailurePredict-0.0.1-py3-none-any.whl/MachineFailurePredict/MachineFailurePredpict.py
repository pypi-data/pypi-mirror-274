#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")


data = pd.read_csv('TrainingData.csv')
data.info()


# # Performing Exploratory Data Analysis (EDA)

# In[2]:


data.head(16)


# In[3]:


data.drop(["UDI", "ProductID","RNF","OSF","PWF","HDF","TWF"], axis=1, inplace=True)
data.info()


# In[4]:


data.shape


# In[1]:


data.drop_duplicates()
data.info()


# In[ ]:


# Perform Label Encoding on features of the dataset


# In[6]:


from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
for i in data.columns:
    if data[i].dtype=="object":
        data[i]=enc.fit_transform(data[i])
data.columns=['Type','Airtemperature','Processtemperature','Rotationalspeed','Torque','Toolwear','Machinefailure']
data.info()
data.head(16)


# # Visualizing the correlation of the dataset

# In[7]:


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score


# # Assigning dependent and independent values

# In[8]:


y=data["Machinefailure"]
x=data.drop(["Machinefailure"],axis =1)


# # Normalizing independent variables

# In[9]:


from sklearn.preprocessing import StandardScaler, Normalizer
scaler=StandardScaler()
x=scaler.fit_transform(x)
x=Normalizer().fit_transform(x)


# # Splitting the data (Testing and Training)

# In[10]:


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2, random_state=0)


# # Building Decision Tree Model

# In[11]:


#Create the object
model = DecisionTreeClassifier()

#Train the model
model = model.fit(x_train, y_train)

#Predict the model
y_pred = model.predict(x_test)


# # Evaluate the model (Obtain Accuracy)

# In[12]:


print("Accuracy score:%.3f"%accuracy_score(y_test, y_pred))
print('Precision: %.3f' % precision_score(y_test, y_pred, average = 'macro'))
print('Recall: %.3f' % recall_score(y_test, y_pred, average = 'macro'))
print('F1 score: %.3f'%f1_score(y_test,y_pred, average = 'macro'))


# # ROC Curve for Decision Tree

# In[13]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


# Predict the probabilities of the positive class
y_pred = model.predict_proba(x_test)[:,1]
y_pred.shape

# Calculate the ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred)

# Calculate the AUC score
auc_score = auc(fpr, tpr)
x1=np.linspace(0,1,100)
# Plot the ROC curve
plt.plot(fpr, tpr, label="ROC curve (AUC = %0.2f)" % auc_score)
plt.plot(x1,x1,label='baseline')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC curve for binary classification")
plt.legend()
# plt.show()


# # Random Forest Classifier

# In[14]:


from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state = 0)

model.fit(x_train,y_train)

y_pred = model.predict(x_test)


# # Evaluating the RFC model

# In[15]:


print("Accuracy score:%.3f"%accuracy_score(y_test, y_pred))
print('Precision: %.3f' % precision_score(y_test, y_pred, average = 'macro'))
print('Recall: %.3f' % recall_score(y_test, y_pred, average = 'macro'))
print('F1 score: %.3f'%f1_score(y_test,y_pred, average = 'macro'))


# In[16]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


# Predict the probabilities of the positive class
y_pred = model.predict_proba(x_test)[:,1]
y_pred.shape

# Calculate the ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred)

# Calculate the AUC score
auc_score = auc(fpr, tpr)
x1=np.linspace(0,1,100)
# Plot the ROC curve
plt.plot(fpr, tpr, label="ROC curve (AUC = %0.2f)" % auc_score)
plt.plot(x1,x1,label='baseline')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC curve for binary classification")
plt.legend()
# plt.show()


# # Logistic Regression

# In[17]:


from sklearn.linear_model import LogisticRegression
model = LogisticRegression(random_state = 16)
model.fit(x_train,y_train)
y_pred = model.predict(x_test)


# # Evaluation for Logistic Regression

# In[18]:


print("Accuracy score:%.3f"%accuracy_score(y_test, y_pred))
print('Precision: %.3f' % precision_score(y_test, y_pred, average = 'macro'))
print('Recall: %.3f' % recall_score(y_test, y_pred, average = 'macro'))
print('F1 score: %.3f'%f1_score(y_test,y_pred, average = 'macro'))


# # Evaluation using Confusion Matrix

# In[19]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


# Predict the probabilities of the positive class
y_pred = model.predict_proba(x_test)[:,1]
y_pred.shape

# Calculate the ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred)

# Calculate the AUC score
auc_score = auc(fpr, tpr)
x1=np.linspace(0,1,100)
# Plot the ROC curve
plt.plot(fpr, tpr, label="ROC curve (AUC = %0.2f)" % auc_score)
plt.plot(x1,x1,label='baseline')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC curve for binary classification")
plt.legend()
# plt.show()


# # Gradient Boosting

# In[20]:


from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.datasets import load_digits


# In[21]:


SEED = 23
y=data["Machinefailure"]
x=data.drop(["Machinefailure"],axis =1)
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25, random_state = SEED)


# In[22]:


model = GradientBoostingClassifier(n_estimators=300,learning_rate=0.05,random_state=100,max_features = 5)
model.fit(x_train, y_train)
y_pred=model.predict(x_test)


# In[23]:


print("Accuracy score:%.3f"%accuracy_score(y_test, y_pred))
print('Precision: %.3f' % precision_score(y_test, y_pred, average = 'macro'))
print('Recall: %.3f' % recall_score(y_test, y_pred, average = 'macro'))
print('F1 score: %.3f'%f1_score(y_test,y_pred, average = 'macro'))


# In[24]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


# Predict the probabilities of the positive class
y_pred = model.predict_proba(x_test)[:,1]
y_pred.shape

# Calculate the ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred)

# Calculate the AUC score
auc_score = auc(fpr, tpr)
x1=np.linspace(0,1,100)
# Plot the ROC curve
plt.plot(fpr, tpr, label="ROC curve (AUC = %0.2f)" % auc_score)
plt.plot(x1,x1,label='baseline')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC curve for binary classification")
plt.legend()
# plt.show()


# In[25]:


data.columns


# # Test Run (Using GradientBoost)

# In[27]:


import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier

#Load the trained model
# model = DecisionTreeClassifier()  #16 records，84%
# model = RandomForestClassifier(random_state = 0) #2 records,98%
# model = LogisticRegression(random_state = 16) #8 records, 92%
model = GradientBoostingClassifier(n_estimators=300,learning_rate=0.05,random_state=100,max_features = 5) #1 records, 99%

model.fit(x_train,y_train)
#Create a StandardScaler object
scaler = StandardScaler()   
    
test=pd.read_csv("TestData.csv",header=0)
test1=test.loc[:,:]
test=test.drop(["Machinefailure"],axis =1)
# test= scaler.fit_transform(test)
predictresult=model.predict(test)
row=test1.loc[test1.index]
output = pd.DataFrame({'Airtemperature':row.Airtemperature,'Processtemperature':row.Processtemperature,'Rotationalspeed':row.Rotationalspeed,'Torque':row.Torque,'Toolwear':row.Toolwear,'Machinefailure':row.Machinefailure,'MachinefailurePredict': predictresult})
output.to_csv("ResultPredict.csv",index=0)

# save model to local file
import pickle
filename ='finalmodel.sav'
pickle.dump(model,open(filename,'wb'))
load_model= pickle.load(open(filename,'rb'))
predictresult=load_model.predict(test)
row=test1.loc[test1.index]
output = pd.DataFrame({'Airtemperature':row.Airtemperature,'Processtemperature':row.Processtemperature,'Rotationalspeed':row.Rotationalspeed,'Torque':row.Torque,'Toolwear':row.Toolwear,'Machinefailure':row.Machinefailure,'MachinefailurePredict': predictresult})
output.to_csv("ResultPredict_LoadModel.csv",index=0)


