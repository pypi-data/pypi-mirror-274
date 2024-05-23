def sparklib():


    print("""
    
1) Enter spark-shell
spark-shell
2) Load data from a Linux Local File System
val lines = sc.textFile("file:///root/log1.txt")
3) Count number of lines 
lines.count()
4) Convert RDD to array
lines.collect()
5) Load data from HDFS
val lines1 = sc.textFile("hdfs://hacluster/user/stu01/input/cx_input_data1.txt")
6) Create an RDD using a parallel set (array and list)
val array = Array(1,2,3,4,5)
val rdd = sc.parallelize(array)

val list = List(1,2,3,4,5)
rdd = sc.parallelize(list)

7) RDD Shell Operations

common transformations:
map(func) - Returns a new RDD formed by passing each element of the source through a function func.
filter(func) - Returns a new RDD formed by selecting those elements of the source on which func returns true.
flatMap(func) - Similar to Map, but each input item can be mapped to 0 or more output items (so func should return a Seq instead of a single item).
mapPartitions(func) - Resembles Map but runs independently on each fragment of the RDD. Therefore, when the operator runs on the RDD whose type is T, the type of the func must be Iterator[T] => Iterator[U].
mapPartitionsWithIndex(func) - Similar to mapPartitions, but also provides func with an integer value representing the index of the partition, so func must be of type (Int, Iterator<T>) => Iterator<U> when running on an RDD of type T.
union(otherDataset) - Returns a new RDD that contains the union of the elements in the source RDD and the argument.
intersection(otherDataset) - Returns a new RDD that contains the intersection of the elements in the source RDD and the argument.
distinct([numTasks])) - Returns a new RDD after deduplicating the source RDD.
groupByKey([numTasks]) - When called on an RDD of (K, V) pairs, returns an RDD of (K, Iterable<V>) pairs.
reduceByKey(func, [numTasks]) - When called on an RDD of (K, V) pairs, returns an RDD of (K, V) pairs where the values for each key are aggregated using the given reduce function func, which must be of type (V,V) => V. Like in groupByKey, the number of Reduce tasks is configurable through an optional second argument.
sortByKey([ascending], [numTasks]) - When called on an RDD of (K, V) pairs where K implements Ordered, returns an RDD of (K, V) pairs sorted by keys in descending order.
sortBy(func,[ascending], [numTasks]) - Similar to sortByKey, but more flexible.
join(otherDataset, [numTasks]) - When called on RDDs of type (K, V) and (K, W), returns an RDD of (K, (V, W)) pairs with all pairs of elements for each key.
cogroup(otherDataset, [numTasks]) - When called on RDDs of type (K, V) and (K, W), returns an RDD of (K, (Iterable<V>, Iterable<W>)) tuples.
union(otherDataset) - Returns a new RDD that contains the union of the elements in the source RDD and the argument.
intersection(otherDataset) - Returns a new RDD that contains the intersection of the elements in the source RDD and the argument.
distinct([numTasks])) - Returns a new RDD after deduplicating the source RDD.
groupByKey([numTasks]) - When called on an RDD of (K, V) pairs, returns an RDD of (K, Iterable<V>) pairs.
reduceByKey(func, [numTasks]) - When called on an RDD of (K, V) pairs, returns an RDD of (K, V) pairs where the values for each key are aggregated using the given reduce function func, which must be of type (V,V) => V. Like in groupByKey, the number of Reduce tasks is configurable through an optional second argument.
sortByKey([ascending], [numTasks]) - When called on an RDD of (K, V) pairs where K implements Ordered, returns an RDD of (K, V) pairs sorted by keys in descending order.
coalesce(numPartitions) - Decreases the number of partitions in the RDD to numPartitions.
repartition(numPartitions) - Reshuffles the data in the RDD randomly to create either more or fewer partitions and balance it across them.
repartitionAndSortWithinPartitions(partitioner) - Repartitions the RDD according to the given partitioner and, within each resulting partition, sorts records by their keys.

common actions:
reduce(func) - Aggregates the elements of the RDD using a function which takes two arguments and returns one.
collect() - Returns all the elements of the RDD as an array at the driver program.
count() - Returns the number of elements in the RDD.
first() - Returns the first element of the RDD, which is similar to take(1).
take(n) - Returns an array consisting of the first n elements of a data set.
takeOrdered(n, [ordering]) - Return the first n elements of the RDD using either their natural order or a custom comparator.
saveAsTextFile(path) - Writes the elements of the RDD as a text file (or set of text files) in a given directory in the local file system, HDFS or any other Hadoop-supported file system. Spark will call toString on each element to convert it to a line of text in the file.
saveAsSequenceFile(path) - Writes the elements of the RDD as a Hadoop SequenceFile in a given path in the local file system, HDFS or any other Hadoop-supported file system.
saveAsObjectFile(path) - Writes the elements of the RDD in a simple format using Java serialization.
countByKey() - Returns a hashmap of (K, Int) pairs with the count of each key. Only available on RDDs of type (K, V).
foreach(func) - Runs the func function on each element of the dataset.
foreachPartition(func) - Runs the func function on each partition of a data set.
reduce(func) - Aggregates the elements of the RDD using a function which takes two arguments and returns one.
collect() - Returns all the elements of the RDD as an array at the driver program.
count() - Returns the number of elements in the RDD.
first() - Returns the first element of the RDD, which is similar to take(1).
take(n) - Returns an array consisting of the first n elements of a data set.

Use map and filter:
val rdd1 = sc.parallelize(List(5, 6, 4, 7, 3, 8, 2, 9, 1, 10))
//Multiply each element in rdd1 by 2 and sort the results.
val rdd2 = rdd1.map(_ * 2).sortBy(x => x, true)
//Filter elements greater than or equal to 5.
val rdd3 = rdd2.filter(_ >= 5)
//Display elements on the client in array mode.
rdd3.collect

Use flatMap:
val rdd1 = sc.parallelize(Array("a b c", "d e f", "h i j"))
//Divide each element in rdd1 and flatten the elements.
val rdd2 = rdd1.flatMap(_.split(" "))
rdd2.collect

Use intersection and union:
val rdd1 = sc.parallelize(List(5, 6, 4, 3))
val rdd2 = sc.parallelize(List(1, 2, 3, 4))
//Obtain the union set.
val rdd3 = rdd1.union(rdd2)
//Obtain the intersection.
val rdd4 = rdd1.intersection(rdd2)
//Deduplicate data
rdd3.distinct.collect
rdd4.collect

Use join and groupByKey:
val rdd1 = sc.parallelize(List(("tom", 1), ("jerry", 3), ("kitty", 2)))
val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 1), ("shuke", 2)))
//Obtain the join.
val rdd3 = rdd1.join(rdd2)
rdd3.collect
//Obtain the union set.
val rdd4 = rdd1 union rdd2
rdd4.collect
//Group by key.
val rdd5=rdd4.groupByKey
rdd5.collect

Use cogroup:
val rdd1 = sc.parallelize(List(("tom", 1), ("tom", 2), ("jerry", 3), ("kitty", 2)))
val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 1), ("jim", 2)))
//cogroup
val rdd3 = rdd1.cogroup(rdd2)
//Pay attention to the difference between cogroup and groupByKey.
rdd3.collect

Use Reduce:
val rdd1 = sc.parallelize(List(1, 2, 3, 4, 5))
//Reduce aggregation.
val rdd2 = rdd1.reduce(_ + _)
rdd2

Use reduceByKey and sortByKey:
val rdd1 = sc.parallelize(List(("tom", 1), ("jerry", 3), ("kitty", 2), ("shuke", 1)))
val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 3), ("shuke", 2), ("kitty", 5)))
val rdd3 = rdd1.union(rdd2)
//Aggregate by key.
val rdd4 = rdd3.reduceByKey(_ + _)
rdd4.collect
//Sort by value in descending order.
val rdd5 = rdd4.map(t => (t._2, t._1)).sortByKey(false).map(t => (t._2, t._1))
rdd5.collect

Perform persistence operations:
val list = List("Hadoop","Spark","Hive")
val rdd = sc.parallelize(list)
println(rdd.count())
println(rdd.collect().mkString(","))
After the preceding instance is added, the execution process after a persistence statement is added is as follows:
val list = List("Hadoop","Spark","Hive")
val rdd = sc.parallelize(list)
rdd.cache()
//persist(MEMORY_ONLY) is called. However, when the statement is executed, the RDD is not cached because the RDD has not been calculated and generated.
println(rdd.count())
//The first action triggers a real start-to-end calculation. In this case, the preceding rdd.cache() is executed and the RDD is stored in the cache. 3
println(rdd.collect().mkString(","))
//The second action does not need to trigger a start-to-end calculation. Only the RDD in the cache needs to be reused.

Spark SQL DataFrame Programming
val lineRDD= sc.textFile("/user/stu01/cx_person.txt").map(_.split(" "))

Define a case class.
A class is equivalent to a schema of a table.
case class Person(id:Int, name:String, age:Int)
val personRDD = lineRDD.map(x => Person(x(0).toInt, x(1), x(2).toInt))

Transform the RDD into DataFrame.
val personDF = personRDD.toDF

View information about DataFrame.
personDF.show
personDF.printSchema

Use the domain-specific language (DSL).
personDF.select(personDF.col("name")).show

Check another format of the name field.
personDF.select("name").show
personDF.select(col("name"), col("age")).show

Query all names and ages and increase the value of age by 1.
personDF.select(col("id"), col("name"), col("age") + 1).show
personDF.select(personDF("id"), personDF("name"), personDF("age") + 1).show

Use the filter method to filter the records where age is no less than 25.
personDF.filter(col("age") >= 25).show

Count the number of people who are older than 30
personDF.filter(col("age")>30).count()

Group people by age and collect statistics on the number of people of the same age.
personDF.groupBy("age").count().show

Use SQL:
If the SQL is used, you need to register DataFrame as a table in the following way:
personDF.registerTempTable("cx_t_person")

Display the schema information of the table.
spark.sql("desc cx_t_person ").show

Query the two oldest people:
spark.sql("select * from cx_t_person order by age desc limit 2").show

Query information about people older than 30:
spark.sql("select * from cx_t_person where age > 30 ").show

Spark SQL DataSet Programming

Create a dataset using spark.createDataset.
val ds1 = spark.createDataset(1 to 5)
ds1.show

Create a dataset using a file.
val ds2 = spark.createDataset(sc.textFile("/user/stu01/cx_person.txt"))
ds2.show

Create a dataset using the toDS method.
case class Person2(id:Int, name:String, age:Int)
val data = List(Person2(1001,"liubei",20),Person2(1002,"guanyu",30))
val ds3 = data.toDS

Create a database by using DataFrame and as[Type].
val ds4= personDF.as[Person2]
ds4.show

Collect statistics on the number of people older than 30 in the dataset.
ds4.filter(col("age") >= 25).show

Hive command to start the spark shell and initialize the hive context and name the initialized context as sqlContext
spark-shell --master local --conf spark.sql.catalogImplementation=hive
val sqlContext = new org.apache.spark.sql.hive.HiveContext(sc)
    
    """)