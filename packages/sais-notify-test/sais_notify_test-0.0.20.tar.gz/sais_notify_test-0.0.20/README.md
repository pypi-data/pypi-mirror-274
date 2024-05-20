[TOC]

# sais-notify

## 介绍
SAIS 消息通知服务Python SDK，方便开发者快速集成消息通知服务。

### 功能

**DONE：**
- 飞书用户文本通知
- 飞书用户富文本通知

**TODO：**
- 飞书用户文本通知
- 飞书用户富文本通知

### 使用

> 安装sais-notify

```bash 
pip install sais-notify -U
```

> 使用sais-notify

### 给飞书用户发送文本消息

```python
from sais.notify import MessageHandler, EnvVarCredentialsProvider, NotifyType
# 需设置环境变量SAIS_NOTIFY_AUTH_TOKEN
credentials_provider = EnvVarCredentialsProvider()
message_handler = MessageHandler(credentials_provider)
message_handler.send_notification(NotifyType.FEISHU_USER_TEXT, to="手机号，多个逗号隔开", message="文本内容")
```

### 给飞书用户发送富文本消息

```python
from sais.notify import MessageHandler, EnvVarCredentialsProvider, NotifyType
# 需设置环境变量SAIS_NOTIFY_AUTH_TOKEN
credentials_provider = EnvVarCredentialsProvider()
message_handler = MessageHandler(credentials_provider)
message_handler.send_notification(NotifyType.FEISHU_USER_RICH_TEXT, to="手机号，多个逗号隔开", message='{\"zh_cn\":{\"title\":\"我是一个标题\",\"content\":[[{\"tag\":\"text\",\"text\":\"第一行 :\"},{\"tag\":\"a\",\"href\":\"http://www.feishu.cn\",\"text\":\"超链接\"},{\"tag\":\"at\",\"user_id\":\"ou_1avnmsbv3k45jnk34j5\",\"user_name\":\"tom\"}],[{\"tag\":\"img\",\"image_key\":\"img_7ea74629-9191-4176-998c-2e603c9c5e8g\"}],[{\"tag\":\"text\",\"text\":\"第二行:\"},{\"tag\":\"text\",\"text\":\"文本测试\"}],[{\"tag\":\"img\",\"image_key\":\"img_7ea74629-9191-4176-998c-2e603c9c5e8g\"}]]}}')
```
### 给飞书群组发送文本消息
```python
from sais.notify import MessageHandler, EnvVarCredentialsProvider, NotifyType
# 需设置环境变量SAIS_NOTIFY_AUTH_TOKEN
credentials_provider = EnvVarCredentialsProvider()
message_handler = MessageHandler(credentials_provider)
message_handler.send_notification(NotifyType.FEISHU_GROUP_TEXT, to="群组id，多个逗号隔开", message='文本消息')

```

### 给飞书群组发送文本消息
```python
from sais.notify import MessageHandler, EnvVarCredentialsProvider, NotifyType
# 需设置环境变量SAIS_NOTIFY_AUTH_TOKEN
credentials_provider = EnvVarCredentialsProvider()
message_handler = MessageHandler(credentials_provider)
message_handler.send_notification(NotifyType.FEISHU_GROUP_MESSAGE_CARD, to="群组id，多个逗号隔开", message='{\"config\":{\"wide_screen_mode\":true},\"elements\":[{\"alt\":{\"content\":\"\",\"tag\":\"plain_text\"},\"img_key\":\"img_7ea74629-9191-4176-998c-2e603c9c5e8g\",\"tag\":\"img\"},{\"tag\":\"div\",\"text\":{\"content\":\"你是否曾因为一本书而产生心灵共振，开始感悟人生？\\n你有哪些想极力推荐给他人的珍藏书单？\\n\\n加入 **4·23 飞书读书节**，分享你的**挚爱书单**及**读书笔记**，**赢取千元读书礼**！\\n\\n📬 填写问卷，晒出你的珍藏好书\\n😍 想知道其他人都推荐了哪些好书？马上[入群围观](https://open.feishu.cn/)\\n📝 用[读书笔记模板](https://open.feishu.cn/)（桌面端打开），记录你的心得体会\\n🙌 更有惊喜特邀嘉宾 4月12日起带你共读\",\"tag\":\"lark_md\"}},{\"actions\":[{\"tag\":\"button\",\"text\":{\"content\":\"立即推荐好书\",\"tag\":\"plain_text\"},\"type\":\"primary\",\"url\":\"https://open.feishu.cn/\"},{\"tag\":\"button\",\"text\":{\"content\":\"查看活动指南\",\"tag\":\"plain_text\"},\"type\":\"default\",\"url\":\"https://open.feishu.cn/\"}],\"tag\":\"action\"}],\"header\":{\"template\":\"turquoise\",\"title\":{\"content\":\"📚晒挚爱好书，赢读书礼金\",\"tag\":\"plain_text\"}}}')
```


## 代码结构
```
├── README.md
├── pyproject.toml
└── sais
    ├── __init__.py
    └── notify
        ├── __init__.py
        ├── auth
        │   ├── __init__.py
        │   └── auth_info.py
        ├── clients
        │   ├── __init__.py
        │   └── notify_client.py
        ├── config
        │   ├── __init__.py
        │   ├── const.py
        │   └── version.py
        ├── handler
        │   ├── __init__.py
        │   └── message_handler.py
        ├── model
        │   ├── __init__.py
        │   └── message_model.py
        ├── requirements.txt
        └── types
            └── __init__.py
```

## 更多
**联系我们：** SAIS 团队
