# 开发教程
## 前言
首先感谢你看到这里，无论最后你是否提交了代码，都感谢你为开源项目做出的贡献。  
由于本项目采用模块化设计，应该可以兼容不少nexus架构的站点，以下是一个简单的开发教程，希望对你有所帮助。  
请确认代码无误后提交pull request

## 开发流程
1. fork本项目
2. git clone 你fork的项目
3. 安装以下的开发环境确保你的代码可以正常运行
   - python 3.6+
   - requests
   - lxml
   - pyyaml
4. 以下以CarPT为例进行代码编写
### CarPT
**首先请观察站点的域名，剔除如PT、BT等关键词，留下一个简单的名字并确保首字母大写，这是本项目的规范**。因此我们将名字定为Car。
#### 1. 编写站点文件
在`nexus/`目录下新建一个文件`Car.py`，并编写以下代码
```python
from .NexusPHP import NexusPHP


class Car(NexusPHP):# 这边是站点的简单名字，即Car，同时与文件名一一对应

    def __init__(self, cookie):
        super().__init__("https://carpt.net", cookie) # 这边是站点的域名，请保证右侧不要有/，以及无关的如/index.php等字符



class Tasks:
    def __init__(self, cookie: str):
        self.car = Car(cookie) # 这边请确保与上方的类名一致，实例名称将首字母小写，即car


    def daily_checkin(self): # 如果是签到任务，请统一使用该名称
        return self.car.attendance() # 这边self.{实例名称}，也请和上方确保一致，即car

    def daily_shotbox(self): # 如果站点有每日喊话的奖励，可以添加上本函数
        shbox_text_list = ["car总，求上传", "car总，求下载"] # 这边是要喊话的内容，多条喊话像这样进行间隔
        return "\n".join([self.car.send_messagebox(item) for item in shbox_text_list]) # 这边代码需要确保为self.{实例名称}.send_messagebox，即self.car.send_messagebox,其他不需要改动
```
#### 2. 编写站点配置文件
在上面我们已经编写了站点文件，并在Task下写了两个任务分别为`daily_checkin`以及`daily_shotbox`  
现在我们需要对根目录的`config_task.yml`文件进行修改。请拉到文件最底部并加上以下代码
```yaml
  Car: # 这边是站点的简单名字，即Car，与前文对应
    enabled: true # 这边是站点是否启用，true为启用，false为禁用 默认true即可不需要改动
    cookie: "" # 这边是站点的cookie，请保证是空字符串，不要不小心将自己的cookie传上来
    tasks: [
      "daily_shotbox",
      "daily_checkin"
    ]
    # tasks中的任务名称请与站点文件中的函数名称一一对应，不要有多余的空格或者其他字符
    # 若站点Task类中写了一个签到任务，那么这里也请务必保证只有一条数据
    # 总而言之，请与前文填写一一对应
```
#### 3. 测试
在完成以上两步后，我们可以进行测试了。请在配置文件中填上cookie并启用站点，然后运行`main.py`文件，查看是否有报错。  
**如无误后请确保删除cookie内容后再commit，以免不小心泄露自己的cookie。**

## 结语
通过以上内容后，你应该可以完成一个简单的站点添加开发，如果有些站点特例化无法直接获取也可以寻求开发者帮助。