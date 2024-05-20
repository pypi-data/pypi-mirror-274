# OpenI

> PYPI package for 启智 AI 协作平台。

## 安装

_适配 python3.6 及以上版本_

```bash
pip install openi
```

## 功能介绍

- 提供命令行与代码使用
- 具体请参考 [帮助文档-API参考](https://openi.pcl.ac.cn/docs/index.html#/api/intro)

```python
from openi.dataset import download_file

download_file(
    file="my_data.zip",
    repo_id="user1/repo1",
    cluster="gpu",
    save_path="local_path/",
)

""" output
Complete( my_data.zip)(gpu): 100%|██████████████████████████████████████████| 22.0MB/22.0MB [00:01<00:00, 15.9MB/s]
"""
```

```bash
>>> openi
usage: openi {login, whoami, dataset, ...} [<args>] [-h]

OpenI command line tool 启智AI协作平台命令行工具

commands:
  {login,logout,whoami,dataset,d,model,m}
    login               使用令牌登录启智并保存到本机
    logout              登出当前用户并删除本地令牌文件
    whoami              查询当前登录用户
    dataset (d)         {upload,download} 上传/下载启智AI协作平台的数据集
    model (m)           {upload,download} 上传/下载启智AI协作平台的模型
```

```bash
>>> openi login


             ██████╗   ██████╗  ███████╗  ███╗   ██╗  ██████╗
            ██╔═══██╗  ██╔══██╗ ██╔════╝  ████╗  ██║    ██╔═╝
            ██║   ██║  ██████╔╝ █████╗    ██╔██╗ ██║    ██║
            ██║   ██║  ██╔═══╝  ██╔══╝    ██║╚██╗██║    ██║
            ╚██████╔╝  ██║      ███████╗  ██║ ╚████║  ██████╗
             ╚═════╝   ╚═╝      ╚══════╝  ╚═╝  ╚═══╝  ╚═════╝


点击链接获取令牌并复制粘贴到下列输入栏 https://openi.pcl.ac.cn/user/settings/applications

[WARNING] 若本机已存在登录令牌，本次输入的令牌会将其覆盖
          粘贴前请先按 退格键⇦ 删除多余空格

  🔒 token:

```
