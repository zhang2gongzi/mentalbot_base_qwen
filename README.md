# mentalbot_base_qwen

## 简介
本仓库用于部署基于 Qwen3-8B 的心理健康聊天服务（Streamlit）。下面说明环境要求、部署及日常运维命令。

## 环境要求

### 硬件
- 显卡：NVIDIA RTX 3090（24GB 显存，支持 CUDA）
- 内存：≥ 32GB（推荐，避免模型加载时内存不足）

### 软件 / 依赖
使用 conda 创建并激活虚拟环境，然后通过 pip 安装依赖：
```bash
conda create -n chat python=3.10 -y
conda activate chat
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

> 注：上面 `python` 版本仅为示例，请根据 `requirements.txt` 的兼容性调整。

## 部署

1. 下载 Qwen3-8B 模型  
   模型获取地址：  
   https://www.modelscope.cn/models/Qwen/Qwen3-8B/files

2. 修改代码中的模型路径  
   打开 `mental_health_chat.py`，在第 10 行左右将 `model_path` 修改为你的模型实际路径，例如：
```python
model_path = "/home2/zzl/model/Qwen3-8B"
```

## 运行

1. 激活环境：
```bash
conda activate chat
```

2. 切换到项目代码目录：
```bash
cd /path/to/your/project
```

3. 后台运行 Streamlit 服务（默认端口为 8501，日志输出到 `chat_log.log`）：
```bash
nohup streamlit run mental_health_chat.py --server.port 8501 --server.address 0.0.0.0 > chat_log.log 2>&1 &
```
你可以替换 `8501` 为其他端口。

## 验证服务状态

- 查看 Streamlit 进程（确认是否在运行）：
```bash
ps aux | grep streamlit
```

- 查看后台作业状态：
```bash
jobs -l
```

- 查看服务启动日志（实时查看）：
```bash
tail -f chat_log.log
```

- 正常启动时日志特征（示例）：
```
You can now view your Streamlit app in your browser.
Network URL: http://172.xx.xx.xx:8501
External URL: http://xxx.xxx.xxx.xxx:8501
```

- 开放端口（Ubuntu 防火墙示例）：
```bash
sudo ufw allow 8501/tcp
sudo ufw reload
sudo ufw status
```

## 日常运维命令

| 操作需求       | 执行命令（示例） |
|---------------|------------------|
| 查看实时日志   | `tail -f /home2/zzl/chat/chat_log.log` |
| 停止服务       | `kill -9 <进程PID>`（PID 通过 `ps aux | grep streamlit` 获取） |
| 重启服务       | `kill -9 <进程PID> && cd /home2/zzl/chat && conda activate chat && nohup streamlit run mental_health_chat.py --server.port 8501 --server.address 0.0.0.0 > chat_log.log 2>&1 &` |
| 检查 GPU 状态  | `nvidia-smi` |
| 检查端口占用   | `netstat -tulpn | grep 8501` |
| 清空日志文件   | `> /home2/zzl/chat/chat_log.log` |
| 重新激活环境   | `conda activate chat`（终端重启后需执行） |

## 常见注意事项
- 确保模型路径正确且模型文件完整，否则模型加载会报错或 OOM。
- 如果显存不足，考虑使用更小模型、启用显存优化或在更大显存的机器上运行。
- 如果需要长期稳定运行，建议将服务通过 systemd 或 docker 容器管理（可按需提供示例）。

## 后续改进建议（可选）
- 添加 systemd 单元文件或 Dockerfile 以实现开机自启与容器化部署。
- 增加健康检查接口及监控（Prometheus / Grafana）。
- 提供更详细的依赖版本锁定（如 `pip freeze` / `environment.yml`）。
