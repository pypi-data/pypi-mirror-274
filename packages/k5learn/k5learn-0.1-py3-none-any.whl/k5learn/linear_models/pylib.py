def pylib():


    print("""
    
###PCA Dimensionality Reduction

#Initialize the PySpark environment
import numpy as np
import pandas as pd import matplotlib.pyplot as plt 
from sklearn.datasets import load_iris 
from pyspark.conf import SparkConf 
from pyspark.ml.feature import VectorAssembler, StandardScaler, PCA 
from pyspark.context import SparkContext 
from pyspark.sql import SparkSession 
sc = SparkContext('local', 'test') 
spark = SparkSession(sc) sc

#Load data and convert it into a DataFrame.
iris = load_iris() 
X = iris['data'] 
y = iris['target'] 
data = pd.DataFrame(X, columns = iris.feature_names) 
dataset = spark.createDataFrame(data, iris.feature_names) 
dataset.show(6)

#Specify the names of the input and output columns.
assembler = VectorAssembler( inputCols = iris.feature_names, outputCol = 'features')

#Transform the dataset and produce the result.
df = assembler.transform(dataset).select('features') 
df.show(6)

#Specify the assembled columns as the input features
scaler = StandardScaler( inputCol = 'features', outputCol = 'scaledFeatures', withMean = True, withStd = True ).fit(df) 
df_scaled = scaler.transform(df) 
df_scaled.show(6)

#After the preprocessing, use PCA to reduce dimensions
n_components = 3 pca = PCA( k = n_components, inputCol = 'scaledFeatures', outputCol = 'pcaFeatures' ).fit(df_scaled) 
df_pca = pca.transform(df_scaled) print('Explained Variance Ratio', pca.explainedVariance.toArray()) 
df_pca.show(6)

###K-means Clustering

#Visualize data by assigning a unique color to each data point that accurately represents its corresponding data type.
list1 = df_pca.rdd.map(lambda x: (x[2][0],x[2][1],x[2][2])).collect() df_origin = spark.createDataFrame([(float(tup[0]), float(tup[1]), float(tup[2])) for tup in list1],['x','y','z']) 
df_Pandas = df_origin.toPandas() 
threedee = plt.figure(figsize=(12,10)).gca(projection='3d') 
threedee.scatter(df_Pandas.iloc[:,0], df_Pandas.iloc[:,1], 
df_Pandas.iloc[:,2], c=y) threedee.set_xlabel('x') threedee.set_ylabel('y') threedee.set_zlabel('z') 
plt.show()

#Add the id column.
df_Pandas['id'] = 'row'+df_Pandas.index.astype(str) 
cols = list(df_Pandas) cols.insert(0, cols.pop(cols.index('id'))) 
df_Pandas = df_Pandas.loc[:, cols] df_Pandas.head()

#Convert the dataset to the CSV format, save it to the local PC, and read the CSV data file.
df_Pandas.to_csv('data/input.csv', index=False) 
path='data/input.csv' 
df = spark.read.csv(path, header=True) 
df.show()

lines = sc.textFile(path) 
data = lines.map(lambda line: line.split(",")) 
data.take(2)

#Convert data into a SparkDataFrame
df = data.toDF(['id', 'x', 'y', 'z']) 
print (df) df.show()

#Convert all data columns to floating points
df_feat = df.select(*(df[c].cast("float").alias(c) for c in df.columns[1:])) 
df_feat.show()

#Convert these columns one by one.
FEATURES_COL = ['x', 'y', 'z'] for col in df.columns: if col in FEATURES_COL: 
df = df.withColumn(col,df[col].cast('float')) df.show()

#Because the header row is included as the first row in the DataFrame, 
it is now filled with null values. Delete the row and any other rows that may contain null values.
df = df.na.drop() df.show()

#As the original columns are no longer needed, use the select statement to filter them out
vecAssembler = VectorAssembler(inputCols=FEATURES_COL, outputCol="features") 
df_kmeans = vecAssembler.transform(df).select('id', 'features') 
df_kmeans.show()

###PySpark MLlib Shopping Basket Data Analysis

#Install the PySpark plotting library.
!pip install pyspark_dist_explore

#Initialize the PySpark environment.
from pyspark.context import SparkContext 
from pyspark.sql import SparkSession 
from pyspark.sql import functions as f, SparkSession, Column 
from pyspark_dist_explore import hist import matplotlib.pyplot as plt 
from pyspark.ml.fpm import FPGrowth 
sc = SparkContext('local', 'test') 
spark = SparkSession(sc) sc

#Read data.
df = spark.read.csv("data/basket.csv", header=True).withColumn("id", f.monotonically_increasing_id()) 
df_all = spark.read.csv("data/Groceries data.csv", header=True).withColumn("id", f.monotonically_increasing_id())

#Display the first five records
df.show(5) 
df_all.show(5)


###PySpark MLlib Collaborative Filtering

#Initialize the environment
from pyspark.sql import SparkSession, column 
from pyspark.context import SparkContext 
from pyspark.sql import SparkSession
sc = SparkContext('local', 'test') 
spark = SparkSession(sc) 
sc

#Decompress the compressed data file.
!unzip ./data/Amazon_Consumer_Reviews.zip -d ./data

#Read data.
df = spark.read.csv('data/Amazon_Consumer_Reviews.csv', inferSchema=True, header=True) 
df.printSchema()

#Rename columns
import re from pyspark.sql.functions import col def rename_cols(df): for column in df.columns: 
new_column = column.replace('.','') df = df.withColumnRenamed(column, new_column) 
return df

#Call the corresponding function to rename columns and select three of them.
df_2 = rename_cols(df) df_2.columns

#Use the ALS algorithm to train a model
from pyspark.ml.recommendation import ALS 
from pyspark.sql.types import IntegerType 
train = train.withColumn("reviewsrating", train["reviewsrating"].cast(IntegerType())) 
test = test.withColumn("reviewsrating", test["reviewsrating"].cast(IntegerType())) 
rs = ALS(maxIter=10, regParam=0.01, userCol='userid', itemCol='id_int', ratingCol='reviewsrating', nonnegative=True, coldStartStrategy="drop") 
rs = rs.fit(train) pred = rs.transform(test)

#Use RegressionEvaluator to evaluate the model
from pyspark.ml.evaluation import RegressionEvaluator 
evaluator = RegressionEvaluator(metricName='rmse', predictionCol='prediction', labelCol='reviewsrating') 
rmse = evaluator.evaluate(pred) print(rmse)

    
    """)