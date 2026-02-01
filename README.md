# mentalbot_base_qwen

## 环境要求
1. 硬件配置
显卡：NVIDIA RTX 3090（24GB 显存，支持 CUDA 计算）
内存：≥ 32GB（推荐，避免模型加载时内存不足）

2. 创建环境

使用依赖创建环境
conda create -n test   
conda activate chat
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

## 部署

1. 下载 Qwen3-8B 模型
模型获取地址：https://www.modelscope.cn/models/Qwen/Qwen3-8B/files
2. 代码中模型地址需要修改，mental_health_chat.py第十行：model_path = "/home2/zzl/model/Qwen3-8B"

## 运行

1. 激活 chat 环境
conda activate chat

2. 切换到目前代码目录
cd /home/...

3.后台运行服务（端口目前写的8501，可替换，日志输出到 chat_log.log）
nohup streamlit run mental_health_chat.py --server.port 8501 --server.address 0.0.0.0 > chat_log.log 2>&1 &

## 验证服务状态

1. 查看 streamlit 进程（确认是否在运行）
ps aux | grep streamlit

2. 查看后台进程状态
jobs -l

3. 查看服务启动日志（确认是否成功）
tail -f chat_log.log

4.正常启动日志特征：
You can now view your Streamlit app in your browser.
Network URL: http://172.xx.xx.xx:8501
External URL: http://xxx.xxx.xxx.xxx:8501

5. 开放端口（Ubuntu 防火墙）
sudo ufw allow 8501（可替换）
sudo ufw reload

验证端口是否开放
sudo ufw status

## 日常运维命令
操作需求	执行命令	
查看实时日志	tail -f /home2/zzl/chat/chat_log.log	
停止服务	kill -9 进程PID（PID 通过 `ps aux	grep streamlit` 获取）
重启服务	kill -9 进程PID && cd /home2/zzl/chat && conda activate chat && nohup streamlit run mental_health_chat.py --server.port 8501 --server.address 0.0.0.0 > chat_log.log 2>&1 &	
检查 GPU 状态	nvidia-smi（查看显存占用和显卡状态）	
检查端口占用	`netstat -tulpn	grep 8501`
清空日志文件	> /home2/zzl/chat/chat_log.log	
重新激活环境	conda activate chat（终端重启后需执行）	
