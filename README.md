# Silent-test-agent

## 1 概述

silent-test-agent 目前实现了api接口自动化的agent模块，UI自动化待后续实现

### 1.1 实现思想

1、python + sqlmodel + httpx 等模块，实现的异步请求agent
2、python语言版本是3.9.12，理论可以下降到3.8.10

### 1.2 适用范围

目前适用于通用的接口自动化测试任务执行(包含测试事务以及普通接口等)   

## 2 使用方式

1、找一台linux服务器   
2、上传代码至一个目录   
3、创建目录，如：agent   
```
    mkdir apiagent
```
4、创建python虚拟环境
```
    python3.9 -m venv (虚拟环境名称)
```
5、激活虚拟环境
```
    source myvenv/bin/activate
```
6、安装需要使用到的模块(仅首次)
```
    pip3 install -r requirements.txt
```
7、启动agent   
目前仅实现了向中心服务(str-backend)注册自身，但获取任务还没有实现（css太难了）
```
    python3.9 agent.py
```

## 3 源代码结构

### 3.1 目录

```
silent-agent/
├── agent.py agent服务的启动入口（主要用于来注册、汇报自身的状态|获取任务|分进程执行）
├── interfaceMain.py 接口自动化执行任务的目录
├── src 源代码
├── apispecs  存放接口描述文件的目录
├── components 执行任务组件的地方
|   ├── assertions 断言组件，如：响应断言器（用来实现想要的断言）、响应对比断言器（用来对比不同版本接口的对比断言[匹配两个接口提取出来的json相似度]）
|   ├── config_element 配置组件，如：缓存读取器（设置读取agent全局缓存的数据）、csv读取器（从csv读取内容，设置为变量）、数据库读取器（从数据库读取内容设置为变量）、请求头管理器、变量设置器
|   ├── listener 监听器 如：结果汇报监听器（负责将一个执行链上的结果，输出到数据库）【如果想要保存本地json，应该继承listener，在使用新类重写】
|   ├── logic_controller 逻辑控制器（在什么样的情况下，执行树中子节点的逻辑） 如：if控制器，while循环管理器
|   ├── parser 项目解析的核心 如：接口描述文件解释器 和 测试用例解释器（将xml转为执行树）
|   ├── post_processors 后置处理器（在接口发送之后执行的逻辑） 如：表达式提取器（expression）、头提取器（head【用来提取header管理器中的auth或者其他认证】）
|   ├── pre_processors 前置处理器（在接口发送之前执行的逻辑）如：变量修改器，变量重命名器
|   ├── sqmpler 取样器 如：http取样器（发送接口请求）、代码取样器（支持执行python代码，并且提取执行结果存储到用户变量【比如sql窗口的token】）
|   ├── threads 协程组（由于python在3.14.0之前，GIL锁问题,这里改用协程实现） 如：前置协程组（执行真正测试代码前执行的内容，如：铺底数据等）、协程组、后置协程组
|   ├── timer 定时器（解决接口请求的落点时间分布问题） 如：固定定时器，随机定时器，高斯定时器等
|   ├── testpaln.py 测试计划元件 继承自basenode, 增加了测试计划中特有的方法，向数据库plan表中汇报
|   ├── basenode.py 所有配置组件继承的根  所有子代中要执行共同的代码，应该在此处写
|   └── context.py 引用python 3.16版本中上下文模块 contextvars，可以隔离每个线程或者协程中的上下文(极为重要，避免了不同协程中变量混乱)
├── config agent的配置文件
├── logs 日志
├── storage 维护了agent启动后，全局缓存数据库
├── models 存放数据模型的地方，项目使用sqlmodel orm框架定义对象-表模型
├── temp_tools 已经废弃（转移到str-backend中实现）
├── template 如果使用了csv读取器，那么csv的数据应该放到这里，在xml引入
├── testcases 测试用例描述文件存放的地方
├── utils 工具类存放的地方
|   ├── str_client.py 定义如何获取异步请求session的模块。维护着httpx client的会话池，每个http请求都会从池子中获取会话
|   ├── str_config.py 读取项目配置文件
|   ├── str_db.py 维护着和数据库交互的池子（连接池），不可以每个协程都打开新的链接
|   ├── str_get_path.py 项目获取全路径的模块
|   ├── str_helper.py 项目常用的方法，比如汇报节点状态、ip、cpu、内存、io等
|   ├── str_log.py 定义日志使用的方式（loguru：异步非阻塞）
|   ├── str_log_decorate.py 日志装饰器，需要使用的函数上应该使用
├── requirements.txt agent或者项目使用到的模块
```