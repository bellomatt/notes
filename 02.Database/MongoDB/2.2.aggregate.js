
MongoDB aggregate 做统计数据(group进阶)


相关使用: 
	db.collection.aggregate([pipeline], options);

	pipeline 可是是任何一个或多个操作符。
	group 和 match 的用法，使用过sqlserver，group的用法很好理解，根据指定列进行分组统计，可以统计分组的数量，也能统计分组中的和或者平均值等。
	group 之前的 match，是对源数据进行查询，group 之后的 match 是对 group 之后的数据进行筛选；
	同理，sort，skip，limit 也是同样的原理；


array 操作符介绍: 
	$project: 包含、排除、重命名和显示字段
	$match: 查询，需要同find()一样的参数
	$limit: 限制结果数量
	$skip: 忽略结果的数量
	$sort: 按照给定的字段排序结果
	$group: 按照给定表达式组合结果
	$count: 返回统计行数
	$unwind: 分割嵌入数组到自己顶层文件

options 操作符介绍:
	allowDiskUse: Aggregation pipeline 操作有内存限制，如果需要处理大量数据，可以设 allowDiskUse=true 来写文件处理大量数据。
	hint: 使用指定索引。



下面以实例介绍用法: 
	for (var i=1; i<=22; i++) {
		db.collection.insert({_id:i, name:"u"+i, status:i%2, age:i%5});
	}


1. 单列 group
	// 统计各 status 的数量和 age 累计值
	db.collection.aggregate([
		{$group:{_id:"$status", count:{$sum:1}, total_age:{$sum:"$age"}}}
	]);
	// 结果:
	{"_id":0,"count":11,"total_age":22}
	{"_id":1,"count":11,"total_age":21}

	// 按 age 分组
	db.collection.aggregate([
		{$group:{_id:"$age",count:{$sum:1}, status_sum:{$sum:"$status"}}},
		{$sort:{_id:1}}
	]);
	// 结果:
	{"_id":0,"count":4,"status_sum":2}
	{"_id":1,"count":5,"status_sum":3}
	{"_id":2,"count":5,"status_sum":2}
	{"_id":3,"count":4,"status_sum":2}
	{"_id":4,"count":4,"status_sum":2}


2.group 之前的 match 过滤
	// 统计 status=1 的 age 分组
	db.collection.aggregate([
		{$match:{status:1}},
		{$group:{_id:"$age",count:{$sum:1}, age_sum:{$sum:"$age"}}},
		{$sort:{_id:1}}
	]);
	// 结果:
	{"_id":0,"count":2,"age_sum":0}
	{"_id":1,"count":3,"age_sum":3}
	{"_id":2,"count":2,"age_sum":4}
	{"_id":3,"count":2,"age_sum":6}
	{"_id":4,"count":2,"age_sum":8}


3.group 之后的 match 过滤
	// 按 age 分组，并且 age平均值 小于等于2的；
	db.collection.aggregate([
		{$group:{_id:"$age",count:{$sum:1},age_avg:{$avg:"$age"}, age_sum:{$sum:"$age"}}},
		{$match:{age_avg:{$lte:2}}},
		{$sort:{_id:1}}
	]);
	// 结果:
	{"_id":0,"count":4,"age_avg":0,"age_sum":0}
	{"_id":1,"count":5,"age_avg":1,"age_sum":5}
	{"_id":2,"count":5,"age_avg":2,"age_sum":10}


4.group 前后都执行 match 过滤
	// 统计 stauts=1 的 age 分组，并且 age平均值 小于等于2的；
	db.collection.aggregate([
		{$match:{status:1}},
		{$group:{_id:"$age",count:{$sum:1},age_avg:{$avg:"$age"}, age_sum:{$sum:"$age"}}},
		{$match:{age_avg:{$lte:2}}},
		{$sort:{_id:1}}
	]);
	// 结果:
	{"_id":0,"count":2,"age_avg":0,"age_sum":0}
	{"_id":1,"count":3,"age_avg":1,"age_sum":3}
	{"_id":2,"count":2,"age_avg":2,"age_sum":4}


5.多列 group
	// 根据 status 和 age 进行多列 group
	db.collection.aggregate([
		{$group:{_id:{status:"$status", age:"$age"},count:{$sum:1}, age_avg:{$avg:"$age"},age_sum:{$sum:"$age"}}},
		{$sort:{_id:1}}
	]);
	// 结果:
	{"_id":{"status":0,"age":0},"count":2,"age_avg":0,"age_sum":0}
	{"_id":{"status":0,"age":1},"count":2,"age_avg":1,"age_sum":2}
	{"_id":{"status":0,"age":2},"count":3,"age_avg":2,"age_sum":6}
	{"_id":{"status":0,"age":3},"count":2,"age_avg":3,"age_sum":6}
	{"_id":{"status":0,"age":4},"count":2,"age_avg":4,"age_sum":8}
	{"_id":{"status":1,"age":0},"count":2,"age_avg":0,"age_sum":0}
	{"_id":{"status":1,"age":1},"count":3,"age_avg":1,"age_sum":3}
	{"_id":{"status":1,"age":2},"count":2,"age_avg":2,"age_sum":4}
	{"_id":{"status":1,"age":3},"count":2,"age_avg":3,"age_sum":6}
	{"_id":{"status":1,"age":4},"count":2,"age_avg":4,"age_sum":8}


6. $project 操作符
	db.collection.aggregate([
		{$match:{age:{$lte:2},status:0}},
		{$project:{name:1,age:1}}
	]);
	// 结果是，只有 _id,name,age 三个字段的表数据，相当于sql表达式 select _id,name,age from collection
	{"_id":2,"name":"u2","age":2}
	{"_id":6,"name":"u6","age":1}
	{"_id":10,"name":"u10","age":0}
	{"_id":12,"name":"u12","age":2}
	{"_id":16,"name":"u16","age":1}
	{"_id":20,"name":"u20","age":0}
	{"_id":22,"name":"u22","age":2}


7. $unwind 操作符
	这个操作符可以将一个数组的文档拆分为多条文档，在特殊条件下有用，本人暂没有进行过多的研究。


8. $count 操作符
	db.collection.aggregate([
		{$match:{status:1}},
		{$count:"status"}
	]);
	// 返回结果
	{"status": 11}


options 操作符
1. 性能分析, explain
	db.collection.explain().aggregate([  // explain() 提供性能分析
		{$match:{age:{$lte:2},status:0}},
		{$group:{_id:{status:"$status", age:"$age"},count:{$sum:1}}},
		{$sort:{_id:1}}
	]);


2. 大量数据 allowDiskUse
	db.collection.aggregate([
		{$match:{age:{$lte:2},status:0}},
		{$group:{_id:{status:"$status", age:"$age"},count:{$sum:1}}},
		{$sort:{_id:1}}
	],
	{allowDiskUse: true}  // allowDiskUse 设为true允许写文件来处理超出内存的数据
	);


3. hint 指定索引
	// 使用前必须先有索引，否则会报错
	db.collection.createIndex( { status: 1, age: 1 } );
	// 查询时
	db.collection.aggregate([
		{$match:{age:{$lte:2},status:0}},
		{$group:{_id:{status:"$status", age:"$age"},count:{$sum:1}}},
		{$sort:{_id:1}}
	],
	{ hint: { status: 1, age: 1 } }  // 使用指定的这个索引
	);



