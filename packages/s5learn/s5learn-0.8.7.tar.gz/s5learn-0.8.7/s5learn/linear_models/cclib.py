def cclib():

    print("""
    
    Load JAR files.
import datetime 
import time 
import numpy as np
from pyspark.sql import Window 
from pyspark.sql.functions import udf, col, concat, count, lit, avg, lag, first, last, when 
from pyspark.sql.functions import min as Fmin, max as Fmax, sum as Fsum, round as Fround 
from pyspark.sql.types import IntegerType, DateType, TimestampType 
from pyspark.ml import Pipeline 
from pyspark.ml.feature import VectorAssembler, Normalizer, StandardScaler
from pyspark.ml.regression import LinearRegression 
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier 
from pyspark.ml.clustering import KMeans 
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder 
from pyspark.ml.evaluation import BinaryClassificationEvaluator, Evaluator

Data Understanding
Decompress the compressed data file
!unzip ./data/sparkify-event-data.zip -d ./data

Read the data file.
event_data = "data/sparkify-event-data.json" 
df = spark.read.json(event_data)

To gain a deeper understanding of the data, check the structure of a data frame.
df.printSchema()

Check the shape of the data frame.
nrows = df.count() 
ncols = len(df.dtypes) 
print(nrows) 
print(ncols)

Obtain the number of deduplicated users.
df.select(['userId']).dropDuplicates().count()

Obtain and analyze the distribution of interaction types in the dataset.
df.groupby('page').count().sort('count', ascending = False).show(22)

Feature Engineering and Exploratory Data Analysis
Classify sessions by sessionId, sort the sessions in each group by timestamp, and obtain the previous value of each page.
obs_start_default = 1538352000000 
obs_end_default = 1543622400000 
windowsession = Window.partitionBy('sessionId').orderBy('ts') 
df = df.withColumn("lagged_page", lag(df.page).over(windowsession)) 
windowuser = Window.partitionBy('userId').orderBy('ts').rangeBetween(Window.unboundedPreceding, Window.unboundedFollowing) 
df = df.withColumn("beforefirstlog", first(col('lagged_page')).over(windowuser)) 
df = df.withColumn("firstlogtime", first(col('ts')).over(windowuser)) 
df = df.withColumn("obsstart", when(df.beforefirstlog == "Submit Registration", df.firstlogtime).otherwise(obs_start_default)) 
df = df.withColumn("endstate", last(col('page')).over(windowuser)) 
df = df.withColumn("lastlogtime", last(col('ts')).over(windowuser)) 
df = df.withColumn("obsend", when(df.endstate == "Cancellation Confirmation", df.lastlogtime).otherwise(obs_end_default))

Calculate the time.
# For each log, calculate the time from the start of observation. 
df = df.withColumn("timefromstart", col('ts')-col("obsstart")) 
# Calculate the time before the observation ends. 
df = df.withColumn("timebeforeend", col('obsend')-col('ts'))

Obtain each user's previous subscription level and add it to the raw dataset.
df = df.withColumn("lastlevel", last(col('level')).over(windowuser))

Delete rows that do not have user IDs.
df = df.where(df.userId != "")

Delete rows that have damaged timestamps.
df = df.where(df.ts < obs_end_default)

Calculate and estimate the length of the activity trend window. 
trend_est_days = 14 
trend_est_hours = trend_est_days * 24 
trend_est = trend_est_days * 24 * 60 * 60 * 1000
# Aggregation by user ID
df_user = df.groupby('userId')\ .agg( 
	# User-level feature 
	first(when(col('lastlevel') == 'paid', 1).otherwise(0)).alias('lastlevel'), 
	first(when(col('gender') == "F", 1).otherwise(0)).alias('gender'), 
	first(col('obsstart')).alias('obsstart'), 
	first(col('obsend')).alias('obsend'), 
	first(col('endstate')).alias('endstate'),
	#first(col('location')).alias('location'), 
	#first(col('userAgent')).alias('userAgent') 
	#first(col('registration')).alias('registration'), 
	# Aggregated activity statistics 
	count(col('page')).alias('nact'), 
	Fsum(when(col('page') == "NextSong", 1).otherwise(0)).alias("nsongs"), 
	Fsum(when(col('page') == "Thumbs Up", 1).otherwise(0)).alias("ntbup"), 
	Fsum(when(col('page') == "Thumbs Down", 1).otherwise(0)).alias("ntbdown"), 
	Fsum(when(col('page') == "Add Friend", 1).otherwise(0)).alias("nfriend"),
	Fsum(when(col('page') == "Add to Playlist", 1).otherwise(0)).alias("nplaylist"), 
	Fsum(when(col('page') == "Submit Downgrade", 1).otherwise(0)).alias("ndgrade"), 
	Fsum(when(col('page') == "Submit Upgrade", 1).otherwise(0)).alias("nugrade"), 
	Fsum(when(col('page') == "Home", 1).otherwise(0)).alias("nhome"), 
	Fsum(when(col('page') == "Roll Advert", 1).otherwise(0)).alias("nadvert"), 
	Fsum(when(col('page') == "Help", 1).otherwise(0)).alias("nhelp"), 
	Fsum(when(col('page') == "Settings", 1).otherwise(0)).alias("nsettings"), 
	Fsum(when(col('page') == "Error", 1).otherwise(0)).alias("nerror"),
	# Activity summary statistics in different time segments 
	Fsum(when(col('timebeforeend') < trend_est, 1).otherwise(0)).alias("nact_recent"), 
	Fsum(when(col('timefromstart') < trend_est, 1).otherwise(0)).alias("nact_oldest"), 
	Fsum(when((col('page') == "NextSong") & (col('timebeforeend') < trend_est), 1).otherwise(0)).alias("nsongs_recent"), 
	Fsum(when((col('page') == "NextSong") & (col('timefromstart') < trend_est), 1).otherwise(0)).alias("nsongs_oldest") )
	Fsum(when((col('page') == "NextSong") & (col('timebeforeend') < trend_est), 1).otherwise(0)).alias("nsongs_recent"), Fsum(when((col('page') == "NextSong") & (col('timefromstart') < trend_est), 1).otherwise(0)).alias("nsongs_oldest") )

Calculate the defined features used to identify churned users. The first added column obshs indicates the length of each user's specific observation period, in hours. The column is not one of the features, but is used to calculate all aggregation statistics per hour.
df_user = df_user.withColumn('obshours', (col('obsend') - col('obsstart'))/1000/3600)\ 
.withColumn('nact_perh', col('nact') / col('obshours'))\ 
.withColumn('nsongs_perh', col('nsongs') / col('obshours'))\ 
.withColumn('ntbup_perh', col('ntbup') / col('obshours'))\ 
.withColumn('ntbdown_perh', col('ntbdown') / col('obshours'))\ 
.withColumn('nfriend_perh', col('nfriend') / col('obshours'))\ 
.withColumn('nplaylist_perh', col('nplaylist') / col('obshours'))\ 
.withColumn('nhome_perh', col('nhome') / col('obshours'))\ 
.withColumn('nadvert_perh', col('nadvert') / col('obshours'))\ 
.withColumn('nerror_perh', col('nerror') / col('obshours'))\ 
.withColumn('upgradedowngrade', col('nugrade') + col('ndgrade'))\ 
.withColumn('songratio', col('nsongs') / col('nact'))\ 
.withColumn('positiveratio', (col('ntbup') + col('nfriend') + col('nplaylist')) / col('nact'))\ 
.withColumn('negativeratio', (col('ntbdown') + col('nhelp') + col('nerror') + col('nsettings')) / col('nact'))\ 
.withColumn('updownratio', col('ntbup') / (col('ntbdown') + 0.1))\ 
.withColumn('nact_recent_perh', col('nact_recent') / trend_est_hours)\ 
.withColumn('nact_oldest_perh', col('nact_oldest') / trend_est_hours)\ 
.withColumn('nsongs_recent_perh', col('nsongs_recent') / trend_est_hours)\ 
.withColumn('nsongs_oldest_perh', col('nsongs_oldest') / trend_est_hours)\ 
.withColumn('trend_act', (col('nact_recent_perh') - col('nact_oldest_perh')) / col('obshours'))\ 
.withColumn('trend_songs', (col('nsongs_recent_perh') - col('nsongs_oldest_perh')) / col('obshours')) 
#.withColumn('timesincereg', (col('obsstart') - col('registration'))/1000/3600)\

Calculate the average number of items in each user session. 
session_avgnitems = df.groupby(['userId', 'sessionId'])\ 
.agg(Fmax(col('itemInSession')).alias('nitems'))\ 
.groupby('userId').agg(avg(col('nitems')).alias('avgsessionitems'))

Calculate the average session length of a user. 
session_avglength = df.groupby(['userId', 'sessionId'])\ 
.agg(Fmin(col('ts')).alias('startsession'), Fmax(col('ts')).alias('endsession'))\ 
.groupby('userId').agg(avg(col('endsession')-col('startsession')).alias('avgsessionlength'))

Calculate the average number of songs played by a user. 
windowhome = (Window.partitionBy('userId').orderBy('ts').rangeBetween(Window.unboundedPreceding, 0)) 
df = df.withColumn("phasehome", Fsum(when(df.page == "Home", 1).otherwise(0)).over(windowhome)) 

songs_home = df.groupby(['userId', 'phasehome'])\ 
.agg(Fsum(when(col('page') == "NextSong", 1).otherwise(0)).alias('total'))\ 
.groupby('userId').agg(avg(col('total')).alias('avgsongs'))

Add additional features and all other features to the df_user dataset. 
df_user = df_user\ 
.join(session_avgnitems, on = 'userId')\ 
.join(session_avglength, on = 'userId')\ 
.join(songs_home, on = 'userId')

Calculate the binary response variables. 
df_user = df_user.withColumn('label', when(df_user.endstate == "Cancellation Confirmation", 1).otherwise(0))

Check the distribution of binary response variables. 
df_user.groupby('label').count().show()

Check the architecture of the transformed dataset. 
df_user.printSchema()

Model Evaluation
Use VectorAssembler to pack multiple features together. 
numeric_columns = ['nsongs_perh', 'ntbup_perh','ntbdown_perh', 'nfriend_perh', 'nadvert_perh', 'nerror_perh', 'upgradedowngrade', 'songratio', 'positiveratio','negativeratio', 'updownratio', 'trend_songs', 'avgsessionitems','avgsongs'] 
numeric_assembler = VectorAssembler(inputCols = numeric_columns, outputCol = "numericvectorized")

Standardize all numerical features at once. 
scaler = StandardScaler(inputCol = "numericvectorized", outputCol = "numericscaled", withStd = True, withMean = True) 
#scaler = Normalizer(inputCol="numericvectorized", outputCol="numericscaled")

Add two binary features. 
binary_columns = ['lastlevel', 'gender'] 
total_assembler = VectorAssembler(inputCols = binary_columns + ["numericscaled"], outputCol = "features")

Customize a F1 score evaluator, which can be used to replace the binary classification evaluator in grid search. 
class F1score(Evaluator): 
	def __init__(self, predictionCol = "prediction", labelCol="label"): 
		self.predictionCol = predictionCol 
		self.labelCol = labelCol 
	def _evaluate(self, dataset): 
		# Calculate the F1 value. 
		tp = dataset.where((dataset.label == 1) & (dataset.prediction == 1)).count()
		fp = dataset.where((dataset.label == 0) & (dataset.prediction == 1)).count() 
		tn = dataset.where((dataset.label == 0) & (dataset.prediction == 0)).count() 
		fn = dataset.where((dataset.label == 1) & (dataset.prediction == 0)).count() 
		# Add ε to prevent division by zero. 
		precision = tp / float(tp + fp + 0.00001) 
		recall = tp / float(tp + fn + 0.00001) 
		f1 = 2 * precision * recall / float(precision + recall + 0.00001) 
		return f1 
	def isLargerBetter(self): 
		return True

Split data into training (and validation) and test sets. 
train_plus_val, test = df_user.randomSplit([0.8, 0.2], seed = 9) 
ntotal = df_user.count() 
ntrainval = train_plus_val.count() 
ntest = ntotal-ntrainval 
print(ntotal) 
print(ntrainval) 
print(ntest)

GBDT Classifier
Define three pipelines using three different classifiers. All of the pipelines contain default parameters. For pipelines with logistic regression, pipeline_lr = pipeline(stages = [digital assembler, scaler, chief assembler, lr]). For pipelines with the random forest classifier, pipeline_rf = pipeline (stages = [digital assembler, scaler, chief assembler, rf]). Grid search is performed by fitting grid search objects. 
gb1 = GBTClassifier(maxDepth = 5, maxIter = 20) 
pipeline_gb1 = Pipeline(stages = [numeric_assembler, scaler, total_assembler, gb1]) 
start = time.time() 
model_gb1 = pipeline_gb1.fit(train_plus_val) 
end = time.time() 
print('Time spent for training:') 
print(round(end-start))

Display feature importance. 
importances = model_gb1.stages[-1].featureImportances 
importances_list = [importances[i] for i in range(len(importances))] 
names = binary_columns + numeric_columns 
print(names) 
print(importances_list)

Evaluation
Obtain the prediction on the test set. 
results_gb1 = model_gb1.transform(test)

Obtain the AUC score on the test set. 
auc_evaluator = BinaryClassificationEvaluator() 
auc_gb1 = auc_evaluator.evaluate(results_gb1) 
print('Model gb1 AUC score:') 
print(auc_gb1)
    
    """)