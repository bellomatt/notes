﻿
虚拟环境 virtualenv
一、安装虚拟环境
    1.首次使用python环境需要安装pip（注：Linux下默认未安装pip，需要手动安装）
        安装pip命令： sudo apt install python-pip : python2.7安装
        sudo apt install python3-pip : python3.5安装
        注：如果pip版本过低,需要升级，pip install --upgrade pip，安装成功后,最好重启

    2.安装虚拟环境virtualenv
        安装命令：pip install virtualenv

        可能出现的问题：
        问题1:Could not get lock /var/lib/dpkg/lock
            出现这个问题可能是有另外一个程序正在运行，导致资被锁不可用。
            而导致资源被锁的原因可能是上次运行安装或更新时没有正常完成，进而出现此状况，解决的办法其实很简单：
            在终端中敲入以下两句：
                sudo rm /var/cache/apt/archives/lock
                sudo rm /var/lib/dpkg/lock
        问题2: Consider using the `--user` option or check the permissions
            解决方法：pip install --user virtualenv

二、使用虚拟环境
    1、创建虚拟环境
      1.创建一个目录存放虚拟环境 mkdir,并进入该目录
        命令：mkdir vir
         cd vir
      2.创建虚拟环境
        virtualenv -p python语言版本的路径 虚拟环境的名称
        例：virtualenv -p /usr/bin/python3.6 virtual
       （默认python版本为python2.7,默认会自动在对应目录下创建与虚拟环境同名的目录名）

    2.激活虚拟环境
      1.激活虚拟环境，当虚拟环境被激活后，在命令前可以看到(虚拟环境名称)
        source 虚拟环境目录/bin/activate
      2.退出虚拟环境
        deactivate
        如果要删除虚拟环境，只需退出虚拟环境后，删除对应的虚拟环境目录即可。不影响其他环境。

三、统一管理虚拟环境软件virtualenvwrapper
  1.安装管理软件
    sudo easy_install virtualenvwrapper
    默认virtualenvwrapper安装在/usr/local/bin下面，
    实际上需要运行virtualenvwrapper.sh文件才行；所以需要先进行配置一下：

  2.配置环境变量(配置软件的运行路径及虚拟环境的存储位置)

    创建虚拟环境管理目录: mkdir $HOME/.local/virtualenvs
    $HOME /home/当前用户
    vim ~/.bashrc中添加下面内容：
        export VIRTUALENV_USE_DISTRIBUTE=1
        export WORKON_HOME=$HOME/.local/virtualenvs   
        if [ -e $HOME/.local/bin/virtualenvwrapper.sh ];then 
        source $HOME/.local/bin/virtualenvwrapper.sh 
        else if [ -e /usr/local/bin/virtualenvwrapper.sh ];then 
        source /usr/local/bin/virtualenvwrapper.sh 
        fi 
        fi 
        export PIP_VIRTUALENV_BASE=$WORKON_HOME 
        export PIP_RESPECT_VIRTUALENV=true

    刷新环境变量: source ~/.bashrc

    激活虚拟环境管理软件
        source /usr/local/bin/virtualenvwrapper.sh

  3.使用虚拟环境
    1.创建并激活虚拟环境 ： mkvirtualenv 虚拟环境名称 （默认创建python2.7）
    2.创建指定语言版本的虚拟环境
      mkvirtualenv -p python语言版本的路径 虚拟环境的名称
      mkvirtualenv -p /usr/bin/python3.5 虚拟环境的名称
    3、退出虚拟环境 ： deactivate
    4.、继续使用之前的虚拟环境： workon 虚拟环境名称 （该虚拟环境必须存在）
    5、删除虚拟环境：rmvirtualenv 虚拟环境名称
    6、列出所有环境：workon 或者 lsvirtualenv -b





