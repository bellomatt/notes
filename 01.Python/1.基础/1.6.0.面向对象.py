
面向对象的编程
    面向过程的编程:根据操作数据的函数或语句块来设计程序的。
    面向对象的编程:把数据和功能结合起来, 用称为对象的东西包裹起来组织程序的方法。
    类和对象是面向对象编程的两个主要方面。“类”创建一个新类型, 而“对象”是这个类的实例。
    域:属于一个对象或类的变量。
    方法:属于类的函数, 被称为类的方法。
    域和方法可以合称为类的属性。
    域有两种类型——属于每个实例/类的对象或属于类本身。它们分别被称为实例变量和类变量。
    类使用class关键字创建。类的域和方法被列在一个缩进块中。

self 参数
    类的方法与普通的函数只有一个特别的区别——它们“必须”有一个额外的第一个参数名称, 但是在调用这个方法的时候你不为这个参数赋值, Python会提供这个值。这个特别的变量指对象本身, 按照惯例它的名称是self。
    虽然你可以给这个参数任何名称, 但是“强烈建议”使用self这个名称——其他名称都是不赞成使用的。
    使用一个标准的名称有很多优点——1.方便别人阅读；2.有些IDE(集成开发环境)也可以帮助你。
    Python中的self等价于C++中的self指针和Java、C#中的this参考。

    例:
    class Person:
        def sayHi(self):  # self参数必须写
            print('Hello, how are you?')

    p = Person()
    p.sayHi() # self参数不需赋值
    print(p)  # 打印: <__main__.Person instance at 0xf6fcb18c>   (已经在__main__模块中有了一个Person类的实例)


类的变量和对象的变量
    类的变量: 由一个类的所有对象(实例)共享使用。当某个对象对类的变量做了改动的时候, 这个改动会反映到所有其他的实例上。
    对象的变量: 由类的每个对象/实例拥有。它们不是共享的, 在同一个类的不同实例中, 虽然对象的变量有相同的名称, 但是是互不相关的。
    使用的数据成员名称以“双下划线前缀”且不是双下划线后缀,比如__privatevar, Python的名称管理体系会有效地把它作为私有变量。
    惯例: 如果某个变量只想在类或对象中使用, 就应该以单下划线前缀。而其他的名称都将作为公共的, 可以被其他类/对象使用。

    例:
    class Person:
        '''Represents a person.'''
        population = 0 # 类的变量

        def __init__(self, name):
            '''Initializes the person's data.'''
            # 每创建一个对象都增加1
            Person.population += 1 # 调用类的变量,必须用 类名.变量名,如果写 self.变量名 则是对象的变量了
            self.name = name # 对象的变量,每个对象独立的
            print('(Initializing %s) We have %d persons here.' % (self.name, Person.population))

        def __del__(self):
            '''I am dying.'''
            print('%s says bye.' % self.name)
            Person.population -= 1

        def sayHi(self):
            self.__sayHi2() # 调用私有方法,外部不能调用的

        # 以双下划线开头(但没有双下划线结尾),则变成私有,仅供内部调用
        def __sayHi2(self): # 使用 self.population 也可以读取类的变量,只是改变的时候却只改变对象的变量
            print('Hi, my name is %s. We have %d persons here.' % (self.name, self.population))

    swaroop = Person('Swaroop')
    swaroop.sayHi() # 打印: Swaroop, 1

    kalam = Person('Abdul Kalam')
    kalam.sayHi() # 打印: Abdul Kalam, 2

    swaroop.sayHi() # 打印: Swaroop, 2
    print(Person.population) # 打印: 2
    del swaroop # 调用对象的 __del__ 方法
    print(Person.population) # 打印: 1

    print(Person.__doc__) # 打印类的docstring
    print(Person.__init__.__doc__) # 打印类的方法的docstring


对象序列化
    class A(object):
        a = 5

        # 如果 __repr__, __str__, __unicode__ 只想写一个的话，建议写 __repr__, 因为 str/unicode/repr 函数都会调用到
        def __repr__(self):return 'repr:%s' % self.a

        def __str__(self):return 'str:%s' % self.a

        def __unicode__(self):return 'unicode:%s' % self.a

    a = A()
    print str(a) # 先 __str__, 再找 __repr__, 没有就用 object 默认的
    print unicode(a) # 先 __unicode__, 再找 __str__, 再找 __repr__, 没有就用 object 默认的
    print repr(a) # 先 __repr__, 没有就用 object 默认的



特殊的方法
__init__ 方法
    创建完对象后调用, 对当前对象的实例的一些初始化, 无返回值
    注意, 这个名称的开始和结尾都是双下划线。( __init__ 方法类似于C++、C#和Java中的 constructor )

__new__ 方法
    创建对象前，先创建的类实例调用, 返回当前对象的一个类实例。
    __new__ 方法的调用是发生在 __init__ 之前的。先是 __new__ 创建了 类实例，然后才可以用 __init__ 初始化实例。
    __new__() 方法始终都是类的静态方法，即使没有被加上静态方法装饰器。

__call__ 方法
    让类的实例（对象）可以被当做函数对待

    例:
    class Person(object):  # 注：py2的旧类不执行 __new__, 得用新类
        def __new__(cls, name):
            print('NEW ', name)
            return super(Person, cls).__new__(cls)
        def __init__(self, name):
            print('INIT ', name)
            self.test_name = name
        def __call__(self, a, b):
            self.a = a
            self.b = b
            print('CALL ({}, {})'.format(self.a, self.b))
        def sayHi(self):
            self.test = 'sss'  # 属性可以随处定义,不需事先定义
            print('Hello, my name is ' + self.test_name + ', ' + self.test)

    p = Person('Swaroop')  # 先打印 NEW, 然后再打印 INIT
    p.sayHi()  # 打印: Hello, my name is Swaroop, sss
    print('the Person test is ' + p.test)  # 打印: the Person test is sss
    p.test2 = 'haha...'
    print('the Person test2 is ' + p.test2)  # 打印: the Person test2 is haha...
    p(1, 2)  # 打印: CALL (1, 2)
    print(callable(p))  # True


    名称   说明
    __init__(self,...) 这个方法在新建对象恰好要被返回使用之前被调用。
    __del__(self) 在对象要被删除之前调用。如使用 del 删除时。
    __str__(self) 在我们对对象使用 print 语句或是使用 str() 的时候调用。
    __lt__(self,other) 当使用 小于 运算符 (<) 的时候调用。
    __gt__(self,other) 当使用 大于 运算符 (>) 的时候调用。
    __eq__(self,other) 当使用 等于 运算符 (==) 的时候调用。
    __ne__(self,other) 当使用 不等于 运算符 (!=) 的时候调用。
    __le__(self,other) 当使用 小于等于 运算符 (<=) 的时候调用。
    __ge__(self,other) 当使用 大于等于 运算符 (>=) 的时候调用。
    __add__(self,other)当使用 加 运算符 (+) 的时候调用。
    __getitem__(self,key) 使用x[key]索引操作符的时候调用。
    __len__(self) 对序列对象使用内建的 len() 函数的时候调用。


__new__ 的作用
    依照Python官方文档的说法， __new__ 方法主要是当你继承一些不可变的 class 时(比如 int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。
    另一个作用就是实现类的自定义的 metaclass 。
    首先我们来看一下第一个功能，具体我们可以用int来作为一个例子：
    假如我们需要一个永远都是正数的整数类型，通过集成int，我们可能会写出这样的代码。

        class PositiveInteger(int):
            def __init__(self, value):
                super(PositiveInteger, self).__init__(self, abs(value))

        i = PositiveInteger(-3)
        print(i)

    但运行后会发现，结果根本不是我们想的那样，我们任然得到了-3。
    这是因为对于 int 这种 不可变的对象，我们只有重载它的 __new__ 方法才能起到自定义的作用。
    这是修改后的代码：

        class PositiveInteger(int):
            def __new__(cls, value):
                return super(PositiveInteger, cls).__new__(cls, abs(value))

        i = PositiveInteger(-3)
        print(i)

    通过重载 __new__ 方法，我们实现了需要的功能。


类变量,容易出错的:
    ##### 范例1, 错误示范 #####
        class A(object):
            x = 1

        class B(A):
            pass

        class C(A):
            pass

        # 初始化正常
        print(A.x, B.x, C.x) # 打印: 1 1 1

        # 改变类变量的值,也正常
        B.x = 2
        print(A.x, B.x, C.x) # 打印: 1 2 1

        # 下面就晕菜了,怎么改变 A 会影响 C,而又不影响 B ?
        A.x = 3
        print(A.x, B.x, C.x) # 打印: 3 2 3


    ##### 解说 范例1 #####
        python 的类变量是存放在一个内部处理的字典中,这字典通常被称为方法解析顺序(Method Resolution Order, 缩写为 MRO)
        所以, 在上面的代码中, 由于属性 x 未能在 C 类中找到, 它会被抬起到其父类中查找(即 A 类)。换句话说, C 不具有自己独立于 A 的 x 属性。
        所以, C.x 其实是一个 A.x 的引用。而 B.x 被赋值过,所以它有自己的 x 属性了。

        #### 把上面的 x 属性是否在类的 __dict__ 判断打印出来,会更容易理解 ####
        class A(object):
            x = 1

        class B(A):
            pass

        class C(A):
            pass

        # A 类里面有 x 属性, 而 B、C 类里面没有, B、C 类得去到父类里面才能找到这个属性
        print(A.x, B.x, C.x) # 打印: 1 1 1
        print('x' in A.__dict__, 'x' in B.__dict__, 'x' in C.__dict__) # 打印: True, False, False

        # B 类赋值了一个 x 属性, 所以有了自己独立于 A 类的 x 属性
        B.x = 2
        print(A.x, B.x, C.x) # 打印: 1 2 1
        print('x' in A.__dict__, 'x' in B.__dict__, 'x' in C.__dict__) # 打印: True, True, False

        # 改变了 A 类的 x 属性的值, C 类里面由于没有这个属性, 所以得用 A 类的。 B 类有自己独立的 x 属性,就用自己的了。
        A.x = 3
        print(A.x, B.x, C.x) # 打印: 3 2 3
        print('x' in A.__dict__, 'x' in B.__dict__, 'x' in C.__dict__) # 打印: True, True, False
