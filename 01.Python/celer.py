

启动 Celery Worker ，通过delay() 或 apply_async() 将任务发布到broker 
(delay 方法封装了 apply_async, apply_async支持更多的参数 )



apply_async 指定时间的参数如下：
    * countdown：延迟多少秒后执行任务，不指定则默认立即执行
    * eta (estimated time of arrival)：指定任务被调度的具体时间，参数类型是 datetime
    当这两个参数同时存在时， countdown 优先。

celery 指定时间执行 / 延期特定时间执行
    task_name.apply_async(args=None, kwargs=None, eta=None)
    task_name.apply_async(args=(2, 3), countdown=5) # 5 秒后执行任务

    # 当前 UTC 时间再加 10 秒后执行任务
    from datetime import datetime, timedelta
    task1.multiply.apply_async(args=[3, 7], eta=datetime.utcnow() + timedelta(seconds=10))

