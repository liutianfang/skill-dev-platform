
## 安装python虚拟环境的依赖包

    source /opt/venv/bin/activate
    pip install -Ur /opt/sdp/requirements.txt

更新源码到/opt/sdp,可以采用git同步或ftp/sftp方式传输。


## 系统设置

数据库驱动加载，sdp/__init__.py中，加载mysql。尽量不要用sqlite,需要python编译增加参数

    import pymysql
    pymysql.install_as_MySQLdb()

### 数据库连接参数

检查和设置sdp/settings.py的DATABASES，代码库中的现有值是按本机mysql服务器设置。
### 其他

设置静态文件目录。以下设置就是/opt/sdp/staitc 为静态文件目录。nginx虚拟主机设置中会用到，

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    SITE_ID = 1




## django基本操作

激活为django配置的python虚拟环境，输入可以看到全部参数：

    python manage.py

###常用参数

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

当增加了新的模块，或模块的model产生了修改，就需要使用makemigrations和migrate，makemigrations产生数据变更代码，migrate导入数据库。

python manage.py runserver是运行django服务器，一般在开发机上使用此命令运行

### 初始化操作

初始化管理后台数据库后，需要创建管理员用户。根据提示输入用户名，邮件和密码

    python manage.py createsuperuser

收集各个模块的静态文件到静态文件目录

    python manage.py collectstatic
