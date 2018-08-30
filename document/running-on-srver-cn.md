# 在主机运行服务

我第一个应用实现是使用alexa lambda实现，连接了RDS数据库。但是很不方便：
  1. 调试困难。alexa提供了日志服务和测试数据，只能说可以测试，测试效率很低
  2. 数据库查询不方便。通过安全域的ec2主机访问数据库
  3. 成本不低，lambda几乎免费，但是数据库实例和EC2收费
  4. 最无法忍受的是，不能安装使用的第三方库，比如nltk

本文主要介绍centos7上运行安装方法。目录规划为：/opt/venv为python的虚拟环境，/opt/sdp为django site路径

 ## 编译安装python

 从https://www.python.org/downloads/下载源码（3.6.5和3.7.0版本测试通过）

 ### 安装centos 必需程序及库

    yum groupinstall "Development Tools"
    yum install epel-release
    yum -y install zlib*  openssl-devel zilb-devel python3-devel gcc  libsqlite3x-devel libsqlite-dev sqlite-dev libffi-devel

### 编译安装
  进入python 源码目录

    /configure --prefix=/usr/local/python3 --enable-optimizations  #选择了--enable-optimizations会时间很长
    make && make install
    ln -s /usr/local/python3/bin/python3 /usr/bin/python3

### python虚拟环境
    cd /opt
    python3 -m virtualenv -p /usr/local/python3/bin/python3 venv

##  mariadb数据库
### 安装
    yum install mariadb mariadb-server
    systemctl start mariadb   #启动mariadb
    systemctl enable mariadb  #设置开机自启动
    mysql_secure_installation #设置root密码等相关
### 创建数据库及用户

自行替换库，用户名，密码，高版本mysql对密码复杂度有要求

    CREATE DATABASE IF NOT EXISTS whereistop DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    grant all privileges on whereistop.* to 'zana'@'%' identified by 'password' WITH GRANT OPTION;
    FLUSH   PRIVILEGES;

## nginx安装
采用yum命令安装

    yum install -y nginx
    systemctl start nginx.service
    systemctl enable nginx.service


## 防火墙
检查状态

systemctl status firewalld

###增加端口

      firewall-cmd --zone=public --add-port=80/tcp --permanent
      firewall-cmd --zone=public --add-port=8000/tcp --permanent
      firewall-cmd --zone=public --add-port=443/tcp --permanent

重启
    firewall-cmd --reload

### https

将sdp/deploy/demo.conf 中的域名修改为自己的域名，放到/etc/nginx/conf.d下。重新启动nginx

    wget https://dl.eff.org/certbot-auto  
    chmod a+x certbot-auto
    ./certbot-auto

第一次执行回先安装python虚拟环境，时间较长，它会自动分析nginx配置文件，按提示操作即可。

使用非www的域名申请证书，如api.yourdomain, server2server


## 开发阶段运行方式

先参考djano_setup.md配置django。将uwsgi和nginx同时运行，即将https的服务器运行起来了。

开发阶段，推荐使用screen方式运行uwsgi。

    yum install screen
    screen
     /opt/venv/bin/uwsgi --ini /opt/sdp/deploy/uwsgi.ini
优点是可以看到控制台打印信息，非常适合开发阶段。即使连接中断，也可以使用screen -r 再次连接。

python代码更新后，需要重新启动uwsgi，CTRL+c停止，上箭头键可以打开上次执行命令，回车即再次启动了uwsgi
