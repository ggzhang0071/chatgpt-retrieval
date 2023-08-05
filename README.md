---
title: guihua_chatgpt
app_file: chatgpt.py
sdk: gradio
sdk_version: 3.39.0
---

-- 创建 conda 环境
``` bash
conda create -n guihua_chatgpt  --channel=conda-forge python==3.9

```

-- 启动 conda 环境
``` bash
conda activate guihua_chatgpt  

```
-- 安装依赖
``` bash
conda install --file requirements.txt
```
-- 运行代码
```bash 
python chatgpt.py
```
最后服务运行再 本地 URL: http://127.0.0.1:7860

注： 如果出现/tmp 文件 permission 拒绝的话， 更改/tmp 文件权限
``` bash
chmod -R 777 /tmp
```

os.environ["OPENAI_API_KEY"] ="***" 
os.environ["OPENAI_API_BASE"] = "https://nodomainname.win/v1/"












Modify `constants.py.default` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys), and rename it to `constants.py`.

Place your own data into `data/data.txt`.

change the /tmp file to write&read.


## Example usage
Test reading `data/data.txt` file.
```
> python chatgpt.py "what is my dog's name"
Your dog's name is Sunny.
```

Test reading `data/cat.pdf` file.
```
> python chatgpt.py "what is my cat's name"
Your cat's name is Muffy.
```
