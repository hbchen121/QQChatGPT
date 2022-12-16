# INSTALL 与开发学习过程

从[b站](https://www.bilibili.com/video/BV1aZ4y1f7e2?p=2&vd_source=6b34769ea077a5ecabfc797ebdd75c9b) 先看一下怎么入门，以下为我看完后的总结

- 安装分为两步，根据[教程](https://blog.csdn.net/m0_62223570/article/details/127429819?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EYuanLiJiHua%7EPosition-2-127429819-blog-120155711.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EYuanLiJiHua%7EPosition-2-127429819-blog-120155711.pc_relevant_default&utm_relevant_index=5) 所示，先安装`go-cqhttp`作为后端执行，再安装nonebot进行前端开发。然后最终的代码用 python 调用 nonebot 即可；

-  nonebot简单期间使用官方的脚手架进行安全开发，官方教程见[这里](https://v2.nonebot.dev/docs/start/installation) 。
-  如果有问题也可以看[B站教程](https://www.bilibili.com/video/BV1aZ4y1f7e2?p=5&vd_source=6b34769ea077a5ecabfc797ebdd75c9b) ，更直观详细；

## go-cqhttp

#### windows

- windows 下载这个`go-cqhttp_windows_amd64.exe`，注意是`amd`；
- 放在需要文件夹后，运行后产生`go-cqhttp.bat`文件，双击运行，选择3，即websocket反向代理；

- 生成一个 config，改一下qq号，（不输入密码则为扫码登录），然后把`universal`改为`ws://127.0.0.1:49731/onebot/v11/ws/`，其中端口为`49731`的随机数，后面NoneBot也要使用统一；

- 更改之后**再次运行**`go-cqhttp.bat`，扫码登录即可，注意提取将 cmd拉大，不然二维码显示不全，不过也不影响，拉大后重新执行`go-cqhttp.bat`即可，执行完成后会显示`开始尝试反向websocket`，具体见[教程里的图](https://img-blog.csdnimg.cn/97b47c89f0614b518616ecdf988b9381.png) ；

  

## NoneBot install

### windows

建议使用虚拟环境，防止环境影响运行（很重要），虚拟环境参考[这里](https://zhuanlan.zhihu.com/p/60647332) 的virtualenv使用；

```shell 
pip install virtualenv

virtualenv qqrobot

# activete
cd qqrobot
.\Scripts\activate.bat

# deactivate
.\Scripts\deactivate.bat
```

安装nonebot脚手架

```shell 
# 需要的话删除旧版
# pip uninstall nonebot

pip install nb-cli
# python -m pip install --upgrade  nb-cli

nb create
```

输入名称创建，具体看官方安装的[视频教程](https://v2.nonebot.dev/docs/tutorial/create-project) ，注意选择`adaptors`要空格选择

随机生成一个端口号`49731`，更改`.env.dev`里端口为`49731`，防止端口冲突；

我们使用`.env`控制运行环境，默认这里是dev，改一下 `.env.dev`配置

```shell 
HOST=127.0.0.1
PORT=49731
LOG_LEVEL=DEBUG
FASTAPI_RELOAD=true
# SUPERUSERS=["1085177243",]  # 超级管理员的QQ，这行已经可以去掉了
# NICKNAME=[bot"]  # 机器人名字，同样可以去掉
COMMAND_START=["/"] # 命令开始符，默认用 / ，去掉""，防止所有信息都是命令
COMMAND_SEP=[] # 命令分隔符，暂时用不上
```

还有`.env.prod`，这个部署时用：

```shell 
HOST=0.0.0.0
PORT=8080
SECRET=
ACCESS_TOKEN=
```

添加一个`echo`插件到指令到`bot.py`的代码中

```python 
nonebot.load_builtin_plugins("echo") 
```

然后在刚刚创建的虚拟环境中，`nb run`，就成功了，此时之前的`go-cqhttp`的内容也会变成链接成功；

最后发一个`echo`插件信息给机器人，测试一下：

```
/echo 你好
```

这样就完成了 简单echo的功能，后面继续群聊艾特回复功能，同时尝试搭载其他机器人，例如 ChatGPT，微信小V等等；

### 群聊艾特自动回复

先构建一个插件库：

- 学习这个[群聊与戳一戳响应chat](https://blog.csdn.net/starvapour/article/details/120155711) ，学习一下怎么回复信息；

- 然后参考这个`who_at_me`[插件](https://github.com/SEAFHMC/nonebot-plugin-who-at-me) ，学习一个怎么知道别人at了自己；
  - 其实就是看消息类型type是不是at；
  - 或者判断事件 event 是否与自己相关； 
- 最后把at+回复结合在一起，回复时调用 XiaoV 或者 ChatGPT 接口；

在编写回复函数时，可以利用异步执行[link](https://juejin.cn/post/7088892051470680078)  来提高速度`async with httpx.AsyncClient()  as client:`，具体

此外，插件放在 plugins 里面时会被自动导入，具体插件路径配置在`pyproject.toml`可见。

可以直接使用我的插件，`qqchatgpt/plugins/robot_chat`。