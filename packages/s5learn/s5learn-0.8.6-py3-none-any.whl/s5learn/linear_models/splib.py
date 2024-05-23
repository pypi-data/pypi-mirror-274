def splib():


    print("""
    
PySpark Environment Initialization
from pyspark.context import SparkContext 
from pyspark.sql import SparkSession 
sc = SparkContext('local', 'test') 
spark = SparkSession(sc) 
sc

Load required packages.
import numpy as np 
from pyspark.mllib.stat import Statistics

Load the required resilient distributed dataset (RDD).
observations = sc.parallelize( [ (1.0, 10.0, 100.0), (2.0, 20.0, 200.0), (3.0, 30.0, 300.0) ] )

Load the statistical model.
summary = Statistics.colStats(observations)

Output the statistical result.
print(summary.mean())

Correlation Analysis
Load the required package.
from pyspark.mllib.stat import Statistics

Load the required RDD.
seriesX = sc.parallelize([1, 2, 3, 3, 5]) 
seriesY = sc.parallelize([11, 22, 33, 33, 555])

Conduct correlation analysis.
correlation = Statistics.corr(seriesX, seriesY, "pearson")

Load data in multiple rows and columns to the RDD.
data = sc.parallelize( [ (1.0, 10.0, 100.0), (2.0, 20.0, 200.0), (5.0, 33.0, 366.0) ])

Analyze correlation coefficients in different columns.
correlMatrix = Statistics.corr(data, method="pearson")

Stratified Sampling
Perform attribute-based sampling and set a sampling ratio.
fractions = {"female": 0.6, "male": 0.4}

Load the required RDD.
rdd = sc.parallelize(fractions.keys()).cartesian(sc.parallelize(range(0, 1000)))

Use the sampleByKey method to perform stratified sampling and check the displayed sampling result.
sample = dict(rdd.sampleByKey(False, fractions, 2).groupByKey().collect()) 
len(sample["female"])
len(sample["male"])

Random Number Generation
Load the required package.
from pyspark.mllib.random import RandomRDDs

Load the random number generation module to generate random numbers.
u = RandomRDDs.normalRDD(sc, 10000000, 10) 
v = u.map(lambda x: 1.0 + 2.0 * x) 
v.collect()

Kernel Density Estimation
from pyspark.mllib.stat import KernelDensity

Load data to the RDD.
sample = sc.parallelize([0.0, 1.0])

Load the kernel density estimation module, estimate the kernel density, and output the following result:
kd = KernelDensity() 
kd.setSample(sample) 
kd.estimate([0.0, 1.0])
    
    """)