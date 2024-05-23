def geslib():

    print("""
    
    Load required JAR files.
from pyspark.sql.functions import explode 
from pyspark.sql.functions import split

Data Loading
Decompress the compressed data file.
!unzip ./data/creditcard.zip -d ./data

Read the data file.
data_O = spark.read.load('data/creditcard.csv', 
format='csv', 
header='true', 
inferSchema='true') 
type(data_O)

To gain a deeper understanding of the data, check the structure of a data frame.
classFreq = data_O.groupBy("Class").count() 
classFreq.show()

Data Preprocessing
import pandas as pd 
data= data_O.toPandas() 
data= data.sample(frac=1) 
# The fraud sample contains 492 rows. 
fraud_df = data.loc[data['Class'] == 1] 
non_fraud_df = data.loc[data['Class'] == 0][:492] 
normal_distributed_df = pd.concat([fraud_df, non_fraud_df]) 
new_df = normal_distributed_df.sample(frac=1, random_state=42) 
new_df.shape

View the distribution of classes in the sample.
import seaborn as sns 
from matplotlib import pyplot as plt 
print('Distribution of the Classes in the subsample dataset') 
print(new_df['Class'].value_counts()/len(new_df)) 
sns.countplot('Class', data=new_df) 
plt.title('Equally Distributed Classes', fontsize=14) 
plt.show()

View heatmaps.
# Ensure that we use a subsample in the correlation. 
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(24,20)) 
corr = data.corr() 
sns.heatmap(corr, cmap='coolwarm_r', annot_kws={'size':20}, ax=ax1) 
ax1.set_title("Imbalanced Correlation Matrix \n (don't use for reference)", fontsize=14) 
sub_sample_corr = new_df.corr() 
sns.heatmap(sub_sample_corr, cmap='coolwarm_r', annot_kws={'size':20}, ax=ax2) 
ax2.set_title('SubSample Correlation Matrix \n (use for reference)', fontsize=14) 
plt.show()

View label-related attributes.
f, axes = plt.subplots(ncols=4, figsize=(20,4)) 
# Negative correlation with the "our" class (A lower feature value indicates a more likely fraudulent transaction.) 
colors = ['#B3F9C5', '#f9c5b3'] 
sns.boxplot(x="Class", y="V17", data=new_df, ax=axes[0]) 
axes[0].set_title('V17 vs Class Negative Correlation') 
sns.boxplot(x="Class", y="V14", data=new_df, ax=axes[1])
axes[1].set_title('V14 vs Class Negative Correlation') 
sns.boxplot(x="Class", y="V12", data=new_df, ax=axes[2]) 
axes[2].set_title('V12 vs Class Negative Correlation') 
sns.boxplot(x="Class", y="V10", data=new_df, ax=axes[3]) 
axes[3].set_title('V10 vs Class Negative Correlation') 
plt.show() 
#----------------- 
f, axes = plt.subplots(ncols=4, figsize=(20,4))
# A higher positive feature correlation also indicates a more likely fraudulent transaction. 
sns.boxplot(x="Class", y="V11", data=new_df, palette=colors, ax=axes[0]) 
axes[0].set_title('V11 vs Class Positive Correlation') 
sns.boxplot(x="Class", y="V4", data=new_df, palette=colors, ax=axes[1]) 
axes[1].set_title('V4 vs Class Positive Correlation') 
sns.boxplot(x="Class", y="V2", data=new_df, palette=colors, ax=axes[2]) 
axes[2].set_title('V2 vs Class Positive Correlation') 
sns.boxplot(x="Class", y="V19", data=new_df, palette=colors, ax=axes[3])
axes[3].set_title('V19 vs Class Positive Correlation') 
plt.show()

Delete outliers.
import numpy as np 
# # -----> Delete outliers from feature V14. 
v14_fraud = new_df['V14'].loc[new_df['Class'] == 1].values 
q25, q75 = np.percentile(v14_fraud, 25), np.percentile(v14_fraud, 75) 
print('Quartile 25: {} | Quartile 75: {}'.format(q25, q75)) 
v14_iqr = q75 - q25 
print('iqr: {}'.format(v14_iqr))
v14_cut_off = v14_iqr * 1.5 
v14_lower, v14_upper = q25 - v14_cut_off, q75 + v14_cut_off 
print('Cut Off: {}'.format(v14_cut_off)) 
print('V14 Lower: {}'.format(v14_lower)) 
print('V14 Upper: {}'.format(v14_upper)) 
outliers = [x for x in v14_fraud if x < v14_lower or x > v14_upper] 
print('Feature V14 Outliers for Fraud Cases: {}'.format(len(outliers))) 
print('V10 outliers:{}'.format(outliers))
new_df = new_df.drop(new_df[(new_df['V14'] > v14_upper) | (new_df['V14'] < v14_lower)].index) 
print('----' * 44) 
# -----> Delete outliers from feature V12. 
v12_fraud = new_df['V12'].loc[new_df['Class'] == 1].values 
q25, q75 = np.percentile(v12_fraud, 25), np.percentile(v12_fraud, 75) 
v12_iqr = q75 - q25 
v12_cut_off = v12_iqr * 1.5
v12_lower, v12_upper = q25 - v12_cut_off, q75 + v12_cut_off 
print('V12 Lower: {}'.format(v12_lower)) 
print('V12 Upper: {}'.format(v12_upper)) 
outliers = [x for x in v12_fraud if x < v12_lower or x > v12_upper] 
print('V12 outliers: {}'.format(outliers)) 
print('Feature V12 Outliers for Fraud Cases: {}'.format(len(outliers))) 
new_df = new_df.drop(new_df[(new_df['V12'] > v12_upper) | (new_df['V12'] < v12_lower)].index) 
print('Number of Instances after outliers removal: {}'.format(len(new_df))) 
print('----' * 44)
# Delete outliers from feature V10. 
v10_fraud = new_df['V10'].loc[new_df['Class'] == 1].values 
q25, q75 = np.percentile(v10_fraud, 25), np.percentile(v10_fraud, 75) 
v10_iqr = q75 - q25 
v10_cut_off = v10_iqr * 1.5 
v10_lower, v10_upper = q25 - v10_cut_off, q75 + v10_cut_off 
print('V10 Lower: {}'.format(v10_lower))
print('V10 Upper: {}'.format(v10_upper)) 
outliers = [x for x in v10_fraud if x < v10_lower or x > v10_upper] 
print('V10 outliers: {}'.format(outliers)) 
print('Feature V10 Outliers for Fraud Cases: {}'.format(len(outliers))) 
new_df = new_df.drop(new_df[(new_df['V10'] > v10_upper) | (new_df['V10'] < v10_lower)].index) 
print('Number of Instances after outliers removal: {}'.format(len(new_df)))

Draw outliers.
f,(ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,6)) 
colors = ['#B3F9C5', '#f9c5b3'] 
# Remove the box plot of outliers. 
# Feature V14 
sns.boxplot(x="Class", y="V14", data=new_df,ax=ax1, palette=colors) 
ax1.set_title("V14 Feature \n Reduction of outliers", fontsize=14) 
ax1.annotate('Fewer extreme \n outliers', xy=(0.98, -17.5), xytext=(0, -12), arrowprops=dict(facecolor='black'), fontsize=14)
# Feature 12 
sns.boxplot(x="Class", y="V12", data=new_df, ax=ax2, palette=colors) 
ax2.set_title("V12 Feature \n Reduction of outliers", fontsize=14) 
ax2.annotate('Fewer extreme \n outliers', xy=(0.98, -17.3), xytext=(0, -12), arrowprops=dict(facecolor='black'), fontsize=14) 
# Feature V10 
sns.boxplot(x="Class", y="V10", data=new_df, ax=ax3, palette=colors) 
ax3.set_title("V10 Feature \n Reduction of outliers", fontsize=14) 
ax3.annotate('Fewer extreme \n outliers', xy=(0.95, -16.5), xytext=(0, -12),arrowprops=dict(facecolor='black'), fontsize=14) 
plt.show()

Convert pandas to spark.sql data frames and add indexes.
dfff = spark.createDataFrame(new_df) 
from pyspark.sql.functions import * 
from pyspark.sql.window import Window 
win = Window().orderBy('Time') 
dfff = dfff.withColumn("idx", row_number().over(win))

Modeling
from pyspark.ml import Pipeline 
from pyspark.ml.classification import GBTClassifier 
from pyspark.ml.feature import VectorIndexer, VectorAssembler 
from pyspark.ml.evaluation import BinaryClassificationEvaluator 
from pyspark.ml.linalg import DenseVector

Split data into a training set and a test set.
training_df = dfff.rdd.map(lambda x: (DenseVector(x[0:29]),x[30],x[31])) # Dense Vector required in spark to train the data 
training_df = spark.createDataFrame(training_df,["features","label","index"]) 
training_df = training_df.select("index","features","label") 
train_data, test_data = training_df.randomSplit([.8,.2],seed=1234)

Calculate the training and test sets.
train_data.groupBy("label").count().show()
test_data.groupBy("label").count().show()

With GBTClassifier, you can use any type of classifiers, such as Logistic-R and others, and compare your results with those found here.
gbt = GBTClassifier(featuresCol="features", maxIter=100,maxDepth=8) 
model = gbt.fit(train_data) 
predictions = model.transform(test_data) 
predictions.groupBy("prediction").count().show()
predictions.groupBy("label").count().show()

Use BinaryClassificationEvaluator.
evaluator = BinaryClassificationEvaluator() 
evaluator.evaluate(predictions)

predictions = predictions.withColumn("fraudPrediction",when((predictions.label==1)&(predictions.prediction==1),1).otherwise(0)) 
predictions.groupBy("fraudPrediction").count().show()

predictions.groupBy("label").count().show()

Obtain the prediction accuracy.
from pyspark.sql.functions import col 
accurateFraud = predictions.groupBy("fraudPrediction").count().where(predictions.fraudPrediction==1).head()[1] 
totalFraud = predictions.groupBy("label").count().where(predictions.label==1).head()[1] 
FraudPredictionAccuracy = (accurateFraud/totalFraud)*100 
FraudPredictionAccuracy

Calculate the confusion matrix to gain a deeper understanding of the data.
tp = predictions[(predictions.label == 1) & (predictions.prediction == 1)].count() 
tn = predictions[(predictions.label == 0) & (predictions.prediction == 0)].count() 
fp = predictions[(predictions.label == 0) & (predictions.prediction == 1)].count() 
fn = predictions[(predictions.label == 1) & (predictions.prediction == 0)].count() 
print("True Positive: ",tp,"\nTrue Negative: ",tn,"\nFalse Positive: ",fp,"\nFalse Negative: ",fn) 
print("Recall: ",tp/(tp+fn)) 
print("Precision: ", tp/(tp+fp))
    
    """)