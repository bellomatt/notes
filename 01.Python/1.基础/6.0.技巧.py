
交换变量

    x = 6
    y = 5

    x, y = y, x

    print(x)  # 打印:5
    print(y)  # 打印:6



if 语句在行内
    作用相当于 C/Java 的三目运算符

    a = "Hello" if True else "World"
    b = "Hello" if False else "World"

    print(a)  # 打印:Hello
    print(b)  # 打印:World


连接
    # 列表、元组 拼接
    nfc = ["Packers", "49ers"]
    afc = ["Ravens", "Patriots"]
    print nfc + afc  # 打印:['Packers', '49ers', 'Ravens', 'Patriots']

    # 字符串 拼接
    print(str(1) + " world") # 打印:1 world

    # 数值的这种写法，我还不清楚是什么, 会当成字符串处理，却又不是真正的字符串
    print(`1` + " world") # 打印:1 world


    # python2.x 的 print 可以这样打印多个不同类型的内容
    print 1, "world" # 打印:1 world
    print nfc, 1 # 打印:['Packers', '49ers'] 1

    # python3.x 的 print 可以这样打印多个不同类型的内容(效果同上面 2.x 的)
    print(1, "world", end=' ') # 打印:1 world
    print(nfc, 1, end=' ') # 打印:['Packers', '49ers'] 1


序列(包括:列表、元组、字符串)

带索引的 序列 迭代(很实用的获取索引的写法)

    teams = ["Packers", "49ers", "Ravens", "Patriots"]
    for index, team in enumerate(teams):
        print(index, team)  # 打印如:0 Packers

序列 的乘法
    items = [0]*3
    print(items)

序列 拼接为字符串
    teams = ["Packers", "49ers", "Ravens", "Patriots"]
    print(", ".join(teams))

序列 的子集
    teams = ["Packers", "49ers", "Ravens", "Patriots"]
    print(teams[-2])     # 最后两项(负数表示倒数几项)
    print(teams[:])      # 复制一份
    print(teams[::-1])   # 反序
    print(teams[::2])    # 奇数项
    print(teams[1::2])   # 偶数项


数值比较
    这是我见过诸多语言中很少有的如此棒的简便法

    x = 2
    if 3 > x > 1:
        print(x)  # 打印:2

    if 1 < x > 0:
        print(x)  # 打印:2


同时迭代两个列表

    nfc = ["Packers", "49ers"]
    afc = ["Ravens", "Patriots"]
    for teama, teamb in zip(nfc, afc):
         print(teama + " vs. " + teamb)
    # 打印1: Packers vs. Ravens
    # 打印2: 49ers vs. Patriots


60个字符解决FizzBuzz
    前段时间Jeff Atwood 推广了一个简单的编程练习叫FizzBuzz，问题引用如下：
    写一个程序，打印数字1到100，3的倍数打印“Fizz”来替换这个数，5的倍数打印“Buzz”，对于既是3的倍数又是5的倍数的数字打印“FizzBuzz”。

    这里就是一个简短的，有意思的方法解决这个问题：
    for x in range(1,101):print("Fizz"[x%3*4:]+"Buzz"[x%5*4:] or x)


False == True
    比起实用技术来说这是一个很有趣的事，在python中, True 和 False 是全局变量(值允许改变)，因此：

    False = True  # 仅py2可行，py3这行报错
    if False:
        print("Hello")
    else:
        print("World")
    # 打印: Hello


换行符分割技巧

    s = "a\r\nb\n"
    print(s.split('\n'))  # ['a\r', 'b', '']
    print(s.splitlines())  # ['a', 'b']


嵌套上下文管理器
    当我们要写一个嵌套的上下文管理器时，可能会这样写

    import contextlib

    @contextlib.contextmanager
    def test_context(name):
        print('enter, my name is {}'.format(name))

        yield

        print('exit, my name is {}'.format(name))

    with test_context('aaa'):
        with test_context('bbb'):
            print('========== in main ============')

    输出结果如下
    enter, my name is aaa
    enter, my name is bbb
    ========== in main ============
    exit, my name is bbb
    exit, my name is aaa


    除此之外，你或许不知道，它还有另一种更加简洁的写法
    with test_context('aaa'), test_context('bbb'):
        print('========== in main ============')


+= 并不等同于 =+
    对列表 进行 += 操作相当于 extend, 而使用 =+ 操作是新增了一个列表。
    因此会有如下两者的差异。

    # =+
    >>> a = [1, 2, 3, 4]
    >>> b = a
    >>> a = a + [5, 6, 7, 8]
    >>> # a[:] = a + [5, 6, 7, 8]  # 改成这句，则 a 和 b 的值同时改变，可以用 id(b) 查看引用的变化
    >>> a
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> b
    [1, 2, 3, 4]

    # += 
    >>> a = [1, 2, 3, 4]
    >>> b = a
    >>> a += [5, 6, 7, 8]
    >>> a
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> b
    [1, 2, 3, 4, 5, 6, 7, 8]


Python 也可以有 end
    有不少编程语言，循环、判断代码块需要用 end 标明结束（比如 Shell），这样一定程序上会使代码逻辑更加清晰一点，
    其实这种语法在 Python 里并没有必要，但如果你想用，也不是没有办法，具体你看下面这个例子。

    __builtins__.end = None

    def m(x):
        if x >= 0:
            return x
        else:
            return -x
        end
    end

    print(m(5))  # 打印：5
    print(m(-5)) # 打印：5

    # 其实只是加了一个全局变量 end, 且这个变量的值指定为 None，但没法强制要求函数写end


省略号 ...
    ... 这是省略号，在Python中，一切皆对象。它也不例外。
    在 Python 中，它叫做 Ellipsis 。
    在 Python 3 中你可以直接写 ... 来得到这玩意。
    >>> ...
    Ellipsis
    >>> type(...)
    <class 'ellipsis'>


    而在 py2 中没有 ... 这个语法，只能直接写Ellipsis来获取。
    >>> Ellipsis
    Ellipsis
    >>> type(Ellipsis)
    <type 'ellipsis'>


    它转为布尔值时为真,且不可以赋值
    >>> bool(...)
    True

    最后，这东西是一个单例。
    >>> id(...)
    4362672336
    >>> id(...)
    4362672336

    这东西有啥用呢？据说它是 Numpy 的语法糖，不玩 Numpy 的人，可以说是没啥用的。
    在网上只看到这个 用 ... 代替 pass ，稍微有点用，但又不是必须使用的。

    try:
        1/0
    except ZeroDivisionError:
        ...


修改解释器提示符
    这个当做今天的一个小彩蛋吧。应该算是比较冷门的，估计知道的人很少了吧。
    正常情况下，我们在 终端下 执行Python 命令是这样的。

    >>> for i in range(2):
    ...     print (i)
    ...
    0
    1

    你是否想过 >>> 和 ... 这两个提示符也是可以修改的呢？

    >>> import sys
    >>> sys.ps1
    '>>> '
    >>> sys.ps2
    '... '
    >>>
    >>> sys.ps2 = '---------------- '
    >>> sys.ps1 = 'Python编程时光>>>'
    Python编程时光>>>for i in range(2):
    ----------------    print (i)
    ----------------
    0
    1

    注：只在终端的情况下可以，如果是文件里面，则会报错: AttributeError: 'module' object has no attribute 'ps1'


for 死循环
    用 while 写死循环很容易，但用 for 可就不容易了。那 for 该怎么写死循环呢？
    while 的写法：  while True: pass

    某网友的 for 写法：
    for i in iter(int, 1):pass 

    是不是懵逼了。 iter 还有这种用法？这为啥是个死循环？
    这真的是个冷知识，关于这个知识点，你如果看中文网站，可能找不到相关资料。
    还好你可以通过 IDE 看py源码里的注释内容，介绍了很详细的使用方法。

    def iter(source, sentinel=None): # known special case of iter
        """
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator

        Get an iterator from an object.  In the first form, the argument must
        supply its own iterator, or be a sequence.
        In the second form, the callable is called until it returns the sentinel.
        """
        pass

    原来 iter 有两种使用方法，通常我们的认知是第一种，将一个列表转化为一个迭代器。
    而第二种方法，他接收一个 callable 对象，和一个 sentinel 参数。第一个对象会一直运行，直到它返回 sentinel 值才结束。

    那 int 呢，这又是一个知识点， int 是一个内建方法。通过看注释，可以看出它是有默认值 0 的。你可以在终端上输入 int() 看看是不是返回 0 。

    class int(object):

        def __init__(self, x, base=10): # known special case of int.__init__
            """
            int(x=0) -> integer
            int(x, base=10) -> integer

            Convert a number or string to an integer, or return 0 if no arguments
            are given.  If x is a number, return x.__int__().  For floating point
            numbers, this truncates towards zero.

            If x is not a number or if base is given, then x must be a string,
            bytes, or bytearray instance representing an integer literal in the
            given base.  The literal can be preceded by '+' or '-' and be surrounded
            by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
            Base 0 means to interpret the base from the string as an integer literal.
            >>> int('0b100', base=0)
            4
            """
            pass





