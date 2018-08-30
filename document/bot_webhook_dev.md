# DUEROS 技能开发

### V0.1 版本

sdp/botskill为DUEROS webhook实现

+ 支持DUEROS/bot webhook 规范
+ 解析请求并按请求类型和意图处理分发
+ 输出实现： 文本输出，session数据输出，session结束.满足基本语音交互要求
+ 数据库记录设备所有者USERID，设备DEVICEID，输入输出报文

### 下一版本

  + 完善面向音箱的多媒体输出，特别是音频播放功能
  + 测试代码

## 代码使用

  + clone项目
  + webhook接口路径，    https://demo.whereis.top/bot/demo/， https://demo.whereis.top为nginx的域名
  虚拟主机配置，bot在sdp/urls.py中配置，demo在botskill/urls.py中配置
  + webhook的入口为views.py的index方法，views.py中只需修改两个帮助信息
  + processer.py为skill的主要处理程序
    + init 方法中，对request进行了读取，需要按自己设定的变量名读取
      + slot值
      + session传递的自定义数据
    + launchRequest响应需要修改 START_MSG
    + 编写特定的意图处理
    
## 演示服务器

  本项目代码部署于demo.whereis.top。请访问：

    https://demo.whereis.top/admin/
    user:  demouser
    password: Sdp%2018

### 演示服务器的用途

开发者自己的webhook服务器可以工作之前，可以将自己的技能的webhook入口设置为

    https://demo.whereis.top/bot/demo/

在控制台配置意图并测试。演示服务器会返回一个格式正确的响应（内容需忽略）。开发者可以登录
演示服务器后台，按请求时间，找到数据库中保存的日志，从中获得请求的json，保存为文件后，
使用测试客户端（curl，httpclient等等）发送给自己的开发服务器进行功能测试。
