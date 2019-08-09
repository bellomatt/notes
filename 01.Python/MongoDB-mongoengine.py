
mongoengine 提供对 MongoDB 的 ORM 操作

一、MongoDB 数据库操作
  1. 连接数据库
     如果我们的 MongoDB 是直接在本地电脑上面运行的，可以使用以下代码来连接到电脑上的 MongoDB 数据库：

        from mongoengine import connect
        connect('数据库名')
        # 如果数据库需要身份验证
        connect('数据库名', username='webapp'， password='pwd123')

    如果MongoDB不是运行在本地电脑上面的，就需要指定ip 地址和端口：

        from mongoengine import connect
        connect('数据库名', host='192.168.2.12', port=3456)

        # 如果数据库需要身份验证
        connect('数据库名', host='192.168.2.12', port=3456, username='webapp'， password='pwd123')

    # 方式三：
    connect('数据库名', host='mongodb://localhost:27017/数据库名')
    connect('数据库名', host='mongodb://用户名:密码@10.0.0.90:27017/数据库名?authSource=admin')

  2. 定义 model

    import datetime    
    from mongoengine import *

    SEX_CHOICES = (
        ('male','男'),
        ('female','女')
    )

    #成绩
    class Grade(EmbeddeDocument):
        name = StringField(required=True)
        score = FloatField(required=True)

    class People(Document):
        source_id = ObjectIdField(primary_key=True)  # uuid类型，且指定为主键
        name = StringField(required=True, unique=True)  # required=True 表示是必须填写的参数, unique=True 表示值唯一
        age = IntField(index=True)  # index=True 表示创建索引
        documentTTL = IntField(default=0) # 不指定默认值的话，默认空值而不是0
        title = StringField(index=True, index_type='keyword', unique_with=['name'])  # 创建索引，且指定索引类型。 unique_with指定联合唯一键
        sex = StringField(choices=SEX_CHOICES, index=True)  # 枚举类型
        status = StringField(default='pending', choices=['pending', 'running', 'error', 'deleted']) # 枚举 + 默认值
        score = FloatField()
        email = EmailField()
        is_tongzhao = BooleanField(db_field='is_tz') # 指定数据库对应字段名
        title = StringField(max_length=200)  # 指定最大字符串长度
        created = DateTimeField(default=datetime.datetime.utcnow)
        expires_at = DateTimeField(default=lambda: datetime.datetime.utcnow()+datetime.timedelta(seconds=30)) # 时间类型，且指定默认值
        # dict
        # 字典可以存储复杂的数据，其他字典，列表，对其他对象的引用，所以是最灵活的可用字段类型
        school_name_props = DictField(verbose_name='学校经历') # verbose_name指定名称
        options = DictField(default={})
        # list
        gaps = ListField(field=StringField(), index=True)  # list 类型，且 list 里面是字符串
        tags = ListField(StringField(max_length=50))
        values = ListField(IntField(), default=list) # 默认空列表
        values2 = ListField(IntField(), default=lambda: [1,2,3]) # 指定默认列表内容
        # 外键
        user = LazyReferenceField(document_type='Manager', db_field='user_id') # 外键关联,document_type指向外键对应的model,db_field指定本类字段名
        messages = RelationField(document_type='Message', relation_type='has_many', target_field='account') # 一对多的外键
        grades = ListField(EmbeddedDocumentField(Grade))

        # 额外设置，不是必须的
        meta = {
            'db_alias': 'importer',  # db_alias用于指定model绑定的mongo连接，和connect函数中的alias对应
            'collection': 'students', # 设置集合名称
            'ordering': ['-age'], # 设置默认排序方式
            'indexes': [ # 设置索引
                'title',
                '$title',  # 文本索引
                '#title',  # 散列索引
                ('title', '-name'), # 联合索引
                ('age', '_cls'), # cls（默认值：True） 如果您有多态模型可以继承并 allow_inheritance打开，则可以配置索引是否应该将该_cls字段自动添加到索引的开头
                {
                    'fields': ['created'], # 要索引的字段。与上述相同的格式指定。
                    'expireAfterSeconds': 3600 # 允许您通过设置以秒为单位的时间过期来自动将某个字段中的数据过期
                }
            ]
        }

    # 可用的字段类型如下所示:
    BinaryField 二进制数据字段 
    BooleanField 
    ComplexDateTimeField 
    DateTimeField 
    DecimalField 
    DictField 
    DynamicField 
    EmailField 
    EmbeddedDocumentField 
    EmbeddedDocumentListField 
    FileField GridFS存储字段 
    FloatField 
    GenericEmbeddedDocumentField 
    GenericReferenceField 
    GenericLazyReferenceField 
    GeoPointField 
    ImageField 图像文件存储区域 
    IntField 
    ListField 
    LineStringField 
    MapField 
    ObjectIdField 
    ReferenceField 
    LazyReferenceField 
    SequenceField 
    SortedListField 
    StringField 
    URLField 
    UUIDField 
    PointField 
    PolygonField 
    MultiPointField 
    MultiLineStringField 
    MultiPolygonField

  3. 创建对象

    kingname = People(name='kingname', age=18, sex='male', salary=99999) 
    kingname.save()

    # 当然，我们也可以这样写：
    kingname = People(name='kingname', age=18, sex='male')
    kingname.salary = 99999
    kingname.save()

    # 也可以用 create 函数创建
    b = People.objects.create(name='User A', age= 40)

  4. 读取对象

    # 读取所有的用户：
    for person in People.objects:
        print(person.name)

    # 按条件搜索也非常简单，在 objects 里面加参数即可，例如搜索所有年龄为22岁的人：
    for person in People.objects(age=22):
        print(person.name)

    # 查询第一条数据
    obj = People.objects.first()
    obj = People.objects.filter(name="xx").first()
    obj = People.objects(name="xx").first() # 进一步优化
    # get 也可以查询出一条数据，但需要注意它的报错。查询不到时报错 People.DoesNotExist
    obj = People.objects.get(name="xx")

    # 查询多条数据
    objects = People.objects.all()

    # 根据ID获取数据
    obj = People.objects.filter(pk=oid)

    # 排序
    # order_by 函数指定，+或者没符号表示升序，-表示降序
    first_post = People.objects.order_by("+created").first()

    # 查询结果个数限制
    # 跟传统的ORM一样，MongoEngine也可以限制查询结果的个数。一种方法是在QuerySet对象上调用limit和skip方法；另一种方法是使用数组的分片的语法。例如：
    users = User.objects[10:15]
    users = User.objects.skip(10).limit(5)

  5. 修改数据
    # 修改多条
    People.objects.filter(sex='male', age__ge=16).update(inc__age=10)

    # 修改一条数据
    People.objects.filter(sex='male').update_one(inc__age=100)

    # save 修改
    obj = People.objects.filter(sex='male').first()
    obj.age = 20
    obj.save()  # 会产生一个 ValidationError 错误
    obj.save(validate=False) # 不会抛出 ValidationError


    # dict 和 list 类型修改的神坑
    obj = People.objects.filter(name="kingname").first()
    d = {}
    l = []
    obj.school_name_props = d
    obj.tags = l
    d['aa'] = 5555
    l.append('3333')
    print(obj.school_name_props)  # 打印：{'aa': 5555}
    print(obj.tags)  # 打印: ['3333']
    obj.save()
    obj.reload()
    print(obj.school_name_props)  # 打印: {}
    print(obj.tags)  # 打印: []
    # 个人认为，是这个orm框架捕获了赋值事件，读取赋值时的值，而不是读取赋值的引用。
    # 所以保存时，其实还是取了刚赋值时的值，导致引用修改无效。需要在值修改后再赋值才生效。如下：
    obj = People.objects.filter(name="kingname").first()
    d = {}
    l = []
    d['aa'] = 5555
    l.append('3333')
    obj.school_name_props = d
    obj.tags = l
    obj.save()
    obj.reload()
    print(obj.school_name_props)  # 打印：{'aa': 5555}
    print(obj.tags)  # 打印: ['3333']


  5.1. 自动更新 
    你而已对一个QuerySet()使用update_one()或update()来实现自动更新，有一些可以与这两个方法结合使用的操作符

    set – 设置成一个指定的值强调内容 
    unset – 删除一个指定的值 
    inc – 将值加上一个给定的数 
    dec – 将值减去一个给定的数 
    pop – 将 list 里面的最后一项移除 
    push – 在 list 里面添加一个值 
    push_all – 在 list 里面添加好几个值 
    pull – 将一个值从 list 里面移除 
    pull_all – 将好几个值从 list 里面移除 
    add_to_set – 如果list里面没有这个值，则添加这个值自动更新的语法与查询的语法基本相同，区别在于操作符写在字段之前：*

    post = BlogPost(title='Test', page_views=0, tags=['database'])
    post.save()
    BlogPost.objects(id=post.id).update_one(inc__page_views=1)
    post.reload()  # 重新读取数据库信息，看更新是否成功
    post.page_views   #1

    BlogPost.objects(id=post.id).update_one(set__title='Example Post')
    post.reload()
    post.title  #'Example Post'

    BlogPost.objects(id=post.id).update_one(push__tags='nosql')
    post.reload()
    post.tags  # ['database', 'nosql']

  6. 删除记录
    如果你想删除记录，那就先把记录找出来，然后调用 delete() 方法吧：

    # 删除一条数据
    People.objects.filter(sex='male').first().delete()

    # 删除多条数据
    People.objects.filter(sex='female').delete()

  7. with_id使用
    # mongo默认id类型为ObjectId，所以使用id查询时，需将str转换为ObjectId
    from bson import ObjectId
    obj = People.objects.get(id=ObjectId(user_id))
    # 优化
    obj = People.objects.with_id(user_id)

  8. 复杂条件
    # contains 包含，icontains 包含(忽略大小写), 不包含 not__contains
    # 模糊检索时对象属性包含所查询字符,如name为abc,输入ab
    user = User.objects.filter(name__contains=search_str)
    user = User.objects.filter(name__not__contains="aa")

    # in 查询
    set_role = Role.objects.filter(pk__in=[i.pk for i in role_list if i])

    # 列举出各函数
    __exact  # 精确等于 like 'aaa'
    __iexact  # 精确等于 忽略大小写 ilike 'aaa'
    __contains  # 包含 like '%aaa%'
    __icontains  # 包含 忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
    __gt  # 大于
    __gte  # 大于等于
    __lt  # 小于
    __lte  # 小于等于
    __in  # 存在于一个list范围内
    __nin  # 值不在列表中
    __startswith  # 以…开头
    __istartswith  # 以…开头 忽略大小写
    __endswith  # 以…结尾
    __iendswith  # 以…结尾，忽略大小写
    __ne  # 不相等
    __not  # 取反
    __all  # 与列表的值相同
    __mod  # 取模
    __size  # 数组的大小
    __exists  # 字段的值存在
    __match  # 使你可以使用一整个document与数组进行匹配查询list
    #对于大多数字段，这种语法会查询出那些字段与给出的值相匹配的document，但是当一个字段引用 ListField 的时候，而只会提供一条数据，那么包含这条数据的就会被匹配上：

    # 上面没有判断是否为空的函数，所以改成下面的判断
    __ne=None

    # 多条件组合的 Q
    # 它可以将多个查询条件进行 &(与) 和 |(或) 操作。
    from mongoengine.queryset.visitor import Q
    # 例如下面的语句是查询所有年龄大于等于18岁的英国用户，或者所有年龄大于等于20岁的用户。
    User.objects((Q(country='uk') & Q(age__gte=18)) | Q(age__gte=20))


    class Page(Document):  
        tags = ListField(StringField())  

    # 普通查询
    Page.objects(tags='coding')

    # 可以通过list的位置来进行查询，你可以使用一个数字来作为查询操作符，例子如下
    Page.objects(tags__0='db')

    #如果你只是想取出list中的一部分，例子如下：
    # comments - skip 5, limit 10  
    Page.objects.fields(slice__comments=[5, 10])

    # 更新document的时候，如果你不知道在list中的位置，你可以使用 $ 这个位置操作符
    Post.objects(comments__by="joe").update(**{'inc__comments__$__votes': 1})

    # 可是，如果这种映射不能正常工作的时候可以使用大写 S 来代替：
    Post.objects(comments__by="joe").update(inc__comments__S__votes=1)


  8.1. 聚合
    # 统计结果个数即可以使用QuerySet的count方法，也可以使用Python风格的方法：
    num_users = len(User.objects)
    num_users = User.objects.count()

    # 求和
    yearly_expense = Employee.objects.sum('salary')
    # 求平均数
    mean_age = User.objects.average('age')

    # item_frequencies 的使用
    # 文档是这么写的:返回整个查询文档集中字段存在的所有项的字典及其对应的频率，即某字段所有值的集合(去重)和结果出现次数，简单来说就是group_by
    objects = People.objects.all()
    objects.item_frequencies('status')
    # 结果如： {'pending':50, 'running':1, 'error':33}

    # scalar 获取所查询的字段值的列表
    People.objects.scalar('name')
    # 结果如： ["kitty", "lily", "john"]

    # in_bulk 通过索引列表获取queryset
    result = Role.objects(pk__in=ids) # 不使用in_bulk
    # 使用in_bulk
    ids = [ObjectId(i) for i in ids]
    documents = Role.objects.in_bulk(ids)
    results = [documents.get(obj_id) for obj_id in ids]
    # 注意： 列表生成式会导致list类型发生变化，无法继续filter

  9. model转dict
    user = User.objects.get(name="xxx")
    # 需注意的是，若将此功能作为结果集的serializer使用，不应该包含外键关联字段
    # 用fields方法过滤指定字段也不起作用
    user_dict = user.to_mongo().to_dict()

    # Serializer 处理
    # todo: 外键、list和dict、嵌套model等 情况还需要考虑
    def mongo_to_dict(obj, fields=None, exclude=None):
        """mongo的model转成dict
        :param exclude: 要排除的字段列表
        :param fields: 只返回指定的字段列表
        """
        model_dict = obj.to_mongo().to_dict()
        if fields:
            exclude = list(exclude) if exclude else []
            exclude.extend(list(set(model_dict.keys()) - set(fields)))
        if exclude:
            assert isinstance(exclude, (list, tuple, set))
            list(map(model_dict.pop, exclude))
        if "_id" in model_dict.keys():
            model_dict["_id"] = str(model_dict["_id"])
        return model_dict

  10. 使用pymongo语法
    使用名称 Model 作为您在实例中为连接定义的实际类的占位符：

    Model._get_collection().aggregate([
        { '$group' : 
            { '_id' : { 'carrier' : '$carrierA', 'category' : '$category' }, 
              'count' : { '$sum' : 1 }
            }
        }
    ])

    所以你可以随时访问 pymongo 对象而不建立单独的连接. Mongoengine 本身建立在 pymongo 上.
    # 示例

    # 标签数量大于3的学生
    class Tag(documents):
      name = StringField()

    class Student(documents):
      name = StringField()
      tag = ListField(ReferenceField(Tag))

    # 使用原生查询
    db.student.find({ "tag.3" : { "$exists" : 1 } })
    # ORM查询
    Student.objects(__raw__={ "tag.3":{ "$exists":1}})

    # 姓名相同的学生数量
    # 原生mongo
    db.getCollection("student").aggregate([
        {"$match":{"status":0}},
        {"$sortByCount":"$name"},
        {"$match":{"count":{"$gt":1}}}
    ]).itcount()

    # ORM
    a = Student._get_collection().aggregate([
        {"$match":{"status":0}},
        {"$sortByCount":"$name"},
        {"$match":{"count":{"$gt":1}}}
    ])
    l = list(a)


  11. 在服务器端执行javascript代码
    # 通过MongoEngine QuerySet对象的 exec_js 方法可以将javascript代码作为字符串发送给服务器端执行，然后返回执行的结果。
    User.objects.exec_js("db.getCollectionNames()")  # 查询该数据库都有那些集合

