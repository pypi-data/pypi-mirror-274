def hpplib():

    print("""
    
Load required JAR files.

from pyspark.sql.types import * 
from pyspark.sql import Row

Data Loading
Load data.
houses_data = spark.read\ 
.format('org.apache.spark.sql.execution.datasources.csv.CSVFileFormat')\ 
.option('header', 'true')\ 
.option('inferSchema', 'true')\ 
.load("data/houses_data.csv")

View data.
rdd = sc.textFile('data/houses_data.csv') 
rdd.take(5)

Data Preprocessing
rdd = rdd.map(lambda line: line.split(",")) 
rdd.take(2)

Use filter to delete any row that contains a header from the RDD.
header = rdd.first() 
rdd = rdd.filter(lambda line:line != header) 
rdd.take(2)

Convert the RDD to a DataFrame.
df = rdd.map(lambda line: Row(street = line[0], city = line[1], zip=line[2], beds=line[4], baths=line[5], sqft=line[6], price=line[9])).toDF() 
df.show()

df.toPandas().head()

Group the quantities of beds and calculate the number of houses based on the data. It will show that there are 108 houses without beds, which is impossible.
df.groupBy("beds").count().show()
df.describe(['baths', 'beds','price','sqft']).show()

Import modules required for linear regression.
import pyspark.mllib 
import pyspark.mllib.regression 
from pyspark.mllib.regression import LabeledPoint 
from pyspark.sql.functions import *

Create a DataFrame that contains only subsets of features we are interested in. Then predict the house prices based on the bathroom, bed, and house areas.
df = df.select('price','baths','beds','sqft')

Remove all abnormal values from the DataFrame.
df = df[df.baths > 0] 
df = df[df.beds > 0] 
df = df[df.sqft > 0] 
df.describe(['baths','beds','price','sqft']).show()

Use labeled points to represent features. The format of a labeled point contains a tuple of response values and a vector of predicted values.
temp = df.rdd.map(lambda line:LabeledPoint(line[0],[line[1:]])) 
temp.take(5)

When using stochastic gradient descent, it becomes clear that the value representing house area is significantly larger than values representing bed and bathroom quantities. In this case, use StandardScaler to standardize data for easy calculation and measurement.
from pyspark.mllib.util import MLUtils 
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.feature import StandardScaler 
features = df.rdd.map(lambda row: row[1:]) 
features.take(5)

standardizer = StandardScaler() 
model = standardizer.fit(features) 
features_transform = model.transform(features) 
features_transform.take(5)

Obtain the price from each row.
lab = df.rdd.map(lambda row: row[0]) 
lab.take(5)

transformedData = lab.zip(features_transform) 
transformedData.take(5)

transformedData = transformedData.map(lambda row: LabeledPoint(row[0],[row[1]])) 
transformedData.take(5)

Modeling
Split the dataset into a training set and a test set.
trainingData, testingData = transformedData.randomSplit([.8,.2],seed=1234)

Introduce linear regression of stochastic gradient descent and build a model. Set the number of iterations to 1000, and the step to 0.2.
from pyspark.mllib.regression import LinearRegressionWithSGD 
linearModel = LinearRegressionWithSGD.train(trainingData,1000,.2)

Extract coefficients and intercepts from the model.
linearModel.weights

Display the first 10 points of the test set. Use the model to predict one of them.
testingData.take(10)

Predict a data point in the test set. The output is the estimated house price.
linearModel.predict([1.49297445326,3.52055958053,1.73535287287])
    
    """)