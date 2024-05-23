def dplib():

    print("""
    
    ###pyspark datapreprocessing 


#importing required packages 
from pyspark.ml import Pipeline 
from pyspark.ml.classification import LogisticRegression 
from pyspark.ml.feature import HashingTF,Tokenizer

#Construct training data from a list of tuples.
training = spark.createDataFrame([ (0, "a b c d e spark", 1.0), (1, "b d", 0.0), 
(2, "spark f g h", 1.0), (3, "hadoop mapreduce", 0.0)],["id", "text", "label"]) training

#Add the words column to the initial DataFrame and convert the data in the text column to words.
tokenizer = Tokenizer(inputCol="text",outputCol="words")

#Convert the output column (words column) of the DataFrame obtained in the previous step to feature vectors and add them to a new column named features.
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(),outputCol='features')

#Create a logistic regression instance.
lr = LogisticRegression(maxIter=10,regParam=0.001)

#Create a pipeline to combine the preceding stages in sequence
pipeline = Pipeline(stages=[tokenizer,hashingTF,lr])

#Train a model. Call the fit() method of the pipeline to generate a pipeline model, which is a Transformer
model = pipeline.fit(training)

#Generate test data.
test = spark.createDataFrame([ (4, "spark i j k"), (5, "l m n"), (6, "spark hadoop spark"), (7, "apache hadoop") ], ["id", "text"])

#Use the trained model to call the transform() method for prediction
prediction = model.transform(test)

#View the prediction.
selected = prediction.select("id", "text", "probability", "prediction") 
for row in selected.collect(): rid, text, prob, prediction = row print("(%d, %s) --> prob=%s, 
prediction=%f" % (rid, text, str(prob), prediction))


###Word2vec

#import required packages 
from pyspark.ml.classification import LogisticRegression 
from pyspark.mllib.feature import Word2Vec 
from pyspark.mllib.feature import Word2VecModel

#Create a model
sentence = "a b " * 100 + "a c " * 10 
localDoc = [sentence, sentence] 
doc = sc.parallelize(localDoc).map(lambda line: line.split(" ")) 
model = Word2Vec().setVectorSize(10).setSeed(42).fit(doc)

#Query synonyms
syms = model.findSynonyms("a", 2) [s[0] for s in syms]

#Querying synonyms of a vector may return words represented by the vector
vec = model.transform("a") syms = model.findSynonyms(vec, 2) [s[0] for s in syms]

#Transform text into a matrix.
import os, tempfile path = tempfile.mkdtemp() model.save(sc, path) 
sameModel = Word2VecModel.load(sc, path) 
model.transform("a") == sameModel.transform("a")

#Output the text transformation result.
syms = sameModel.findSynonyms("a", 2) [s[0] for s in syms]

###Count Vectorizer 

#Load the required package.
from pyspark.ml.feature import CountVectorizer

#Load data and convert it into a DataFrame
df = spark.createDataFrame( [(0, ["a", "b", "c"]), 
(1, ["a", "b", "b", "c", "a"])], ["label", "raw"])

#Load the transformation model.
cv = CountVectorizer() cv.setInputCol("raw") 
cv.setOutputCol("vectors") model = cv.fit(df)
model.setInputCol("raw")

#Print the model running result.
model.transform(df).show(truncate=False)

###RegexTokenizer

#Load the required package.
from pyspark.ml.feature import RegexTokenizer

#Import data to a DataFrame.
df = spark.createDataFrame([("A B c",)], ["text"])

#Invoke Tokenizer models, that is, general string and regular expression models.
reTokenizer = RegexTokenizer()

#Invoke the Tokenizer.
reTokenizer.setInputCol("text") 
reTokenizer.setOutputCol("words")

#Print the tokenization result.
reTokenizer.transform(df).head()

###StopWordsRemover

#Load the required package.
from pyspark.ml.feature import StopWordsRemover

#Load the stop word module and configure related parameters and the input and output modes.
remover = StopWordsRemover().setInputCol("raw").setOutputCol("filtered")

#Import data and encapsulate it using a DataFrame
dataSet = spark.createDataFrame( [(0, ["I", "saw", "the", "red", "balloon"]), 
(1, ["Mary", "had", "a", "little", "lamb"])], ["id", "raw"])

#Output the result after the stop words are removed.
remover.transform(dataSet).show()

###n-gram

#Load the required package.
from pyspark.ml.feature import NGram

#Load test data to an RDD and convert it into a DataFrame
wordDataFrame = spark.createDataFrame( [(0, ["Hi", "I", "heard", "about", "PySpark"]), 
(1, ["I", "wish", "Java", "could", "use", "case", "classes"]),
(2, ["Logistic", "regression", "models", "are", "neat"])], ["id", "words"])

#Invoke the NGram module, configure the set size to 2, and set the input to the words column and the output to the ngrams column. 
Generate a set of datasets and apply the model to the datasets
ngram = NGram().setN(2).setInputCol("words").setOutputCol("ngrams") ngramDataFrame = ngram.transform(wordDataFrame)

#Output the conversion result.
ngramDataFrame.select("ngrams").show()

###Binarizer

#Load the required package
from pyspark.ml.feature import Binarizer

#Import the dataset.
data = [(0, 0.1), (1, 0.8), (2, 0.2)]

#Convert the dataset into the DataFrame data structure
dataFrame = spark.createDataFrame(data,["id", "feature"])

#Call the module to perform binarization.
binarizer = Binarizer().setInputCol("feature").setOutputCol("binarized_feature").setThreshold(0.5) 
binarizedDataFrame = binarizer.transform(dataFrame)

#Output the binarization result
binarizedDataFrame.show()

###PCA

#Load the required package.
from pyspark.ml.feature import PCA 
from pyspark.ml.linalg import Vectors

#Load the test set.
data = [(Vectors.sparse(5, [(1, 1.0), (3, 7.0)]),), 
(Vectors.dense([2.0, 0.0, 3.0, 4.0, 5.0]),), 
(Vectors.dense([4.0, 0.0, 0.0, 6.0, 7.0]),)]

#Store the dataset to a DataFrame.
df = spark.createDataFrame(data,["features"])

#Invoke the PCA module to reduce data dimensionality, 
set the input to features, output to pcaFeatures, and dimension to 3, and complete model training.
pca = PCA(k=3, inputCol="features") 
pca.setOutputCol("pca_features") 
model = pca.fit(df)
model.explainedVariance

#Select the output dataset and output the result.
model.transform(df).take(1)

###PolynomialExpansion

#Load required packages
from pyspark.ml.feature import PolynomialExpansion 
from pyspark.ml.linalg import Vectors

#Load the dataset to data and store it as a dense matrix.
data = [ (Vectors.dense([2.0, 1.0]),), 
(Vectors.dense([0.0, 0.0]),), (Vectors.dense([3.0, -1.0]),) ]

#Convert the dataset into a DataFrame.
df = spark.createDataFrame(data,["features"])

#Invoke the polynomial expansion module, configure the input and output columns, set the Degree, and then process the dataset
polyExpansion = PolynomialExpansion().setInputCol("features").setOutputCol("polyFeatures").setDegree(3) 
polyDF = polyExpansion.transform(df)

#Print the program execution result.
polyDF.show()

###DCT

#Load required packages.
from pyspark.ml.feature import DCT 
from pyspark.ml.linalg import Vectors 
from pyspark.ml.feature import PolynomialExpansion

#Load the dataset to data and store it as serialized data
data = [ (Vectors.dense([0.0, 1.0, -2.0, 3.0]),), 
(Vectors.dense([-1.0, 2.0, 4.0, -7.0]),), 
(Vectors.dense([14.0, -2.0, -5.0, 1.0]),) ]

#Convert the dataset into a DataFrame.
df = spark.createDataFrame(data,["features"])

#invoke the discretization module to discretize the dataset
dct = DCT().setInputCol("features").setOutputCol("featuresDCT").setInverse(False) 
dctDf = dct.transform(df) 
polyExpansion = PolynomialExpansion(degree=3, inputCol="features", outputCol="polyFeatures") 
polyDF = polyExpansion.transform(df)

#Print the program execution result.
dctDf.select("featuresDCT").show()

###StringIndexer

#Load the required package.
from pyspark.ml.feature import IndexToString, StringIndexer

#data = [ ([0, "a"]), ([1, "b"]), ([2, "c"]), ([3, "a"]), ([4, "a"]), ([5, "c"]) ] 
df = spark.createDataFrame(data,["id", "category"])

#Invoke the index-string transformation module to transform the dataset
indexer = StringIndexer().setInputCol("category").setOutputCol("categoryIndex").fit(df) 
indexed = indexer.transform(df) indexed

#Print the transformation result.
indexed.show()

###IndexToString

#Load the required package
from pyspark.ml.feature import StringIndexer

#Load data to a DataFrame.
data = [ ([0, "a"]), ([1, "b"]), ([2, "c"]), ([3, "a"]), ([4, "a"]), ([5, "c"]) ] 
df = spark.createDataFrame(data,["id", "category"])

#Invoke the string-index transformation module to transform the dataset
indexer = StringIndexer().setInputCol("category").setOutputCol("categoryIndex") 
indexed = indexer.fit(df).transform(df)

#Print the transformation result
indexed.show()

###OneHotEncoder

#Load required packages
from pyspark.ml.feature import OneHotEncoder 
from pyspark.ml.feature import StringIndexer

#Load data to a DataFrame
data = [ ([0, "a"]), ([1, "b"]), ([2, "c"]), ([3, "a"]), ([4, "a"]), ([5, "c"]) ] 
df = spark.createDataFrame(data,["id", "category"])

#Invoke the OneHotEncoder module to transform the dataset
indexer = StringIndexer().setInputCol("category").setOutputCol("categoryIndex").fit(df) 
indexed = indexer.transform(df) 
encoder = OneHotEncoder().setInputCol("categoryIndex").setOutputCol("categoryVec") 
encoded = encoder.transform(indexed)

#Print the transformation result
encoded.show()

###VectorIndexer


#Load the required package
from pyspark.ml.feature import VectorIndexer

#Load data to a DataFrame. Note that an HDFS dataset is loaded here.
data = spark.read.format("libsvm").load("./data/sample_libsvm_data.txt")

#Invoke the VectorIndexer module to transform the dataset
indexer = VectorIndexer() 
indexer.setInputCol("features").setOutputCol("indexed").setMaxCategories(10) 
indexerModel = indexer.fit(data)

#Invoke the model for dataset transformation
indexedData = indexerModel.transform(data)

#Print the transformation result.
indexedData.show()

###Normalizer (p-norm Normalization)

#Load required packages.
from pyspark.ml.feature import Normalizer from pyspark.ml.linalg import Vectors

#Load data to a DataFrame
data = [(0,Vectors.dense([1.0, 0.5, -1.0]),), (1,Vectors.dense([2.0, 1.0, 1.0]),), (2,Vectors.dense([4.0, 10.0, 2.0]),) ] 
df = spark.createDataFrame(data, ["id", "features"])

#Invoke the L1 p-norm normalization module to transform the dataset.
normalizer = Normalizer().setInputCol("features").setOutputCol("normFeatures").setP(1.0) 
l1NormData = normalizer.transform(df)

#Print the L1 transformation result.
l1NormData.show()

#
    
    """)