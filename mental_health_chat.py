import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

# ========== 1. 模型加载 ==========
@st.cache_resource
def load_model():
    with st.spinner("🧠 加载Qwen3-8B模型..."):
        model_path = "/home2/zzl/model/Qwen3-8B"
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
    return model, tokenizer

model, tokenizer = load_model()

# ========== 2. 强约束提示词 ==========
SYSTEM_PROMPT = (
    "你是一名专业心理咨询师。请严格遵守：\n"
    "• 只输出最终回复，禁止任何思考过程、内部推理\n"
    "• 禁止输出 <think> 标签、括号内容或思考开头\n"
    "• 保持温暖专业，每次回复不超过5句话"
    "• 以倾听者和支持者身份提供帮助\n"
    "• 不做评判，只提供情感支持\n"
    "• 优先关注用户当下的情绪状态\n"
    "• 必要时提供专业求助渠道\n\n"
)

# ========== 3. 初始化对话历史 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 4. 侧边栏 ==========
with st.sidebar:
    if st.button("🔄 清除对话"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("### 🆘 紧急求助")
    st.markdown("`400-161-9995` 全国心理援助热线")
    st.markdown("`12356` 四川省心理援助热线")

# ========== 5. 主界面 ==========
st.title("💬 心理咨询助手")
st.caption("🔒 安全私密 · 这里是一个安全、私密的空间，你可以自由分享想法和感受，我会认真倾听")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ========== 6. 用户输入处理 ==========
if prompt := st.chat_input("请分享你的感受..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 构造对话
    messages_for_model = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    
    text = tokenizer.apply_chat_template(
        messages_for_model,
        tokenize=False,
        add_generation_prompt=True
    )
    
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # ========== 7. 生成回复 ==========
    with st.chat_message("assistant"):
        with st.spinner("💭 思考中..."):
            outputs = model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id
            )
        
        # 解码
        generated_tokens = outputs[0][inputs.input_ids.shape[1]:]
        response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        # ========== 8. 终极过滤（四重保险）==========
        # 第1重：移除 <think> 标签（核心问题！）
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        response = re.sub(r'<think>', '', response)  # 移除未闭合标签
        response = re.sub(r'</think>', '', response)  # 移除闭合标签
        
        # 第2重：移除零宽字符（兼容其他情况）
        response = re.sub(r'[\u200B-\u200D\uFEFF\u2060\u202A-\u202E\u0000-\u001F]', '', response)
        
        # 第3重：移除括号内容
        response = re.sub(r'（[^）]*）', '', response)
        response = re.sub(r'\([^)]*\)', '', response)
        
        # 第4重：移除思考开头
        response = re.sub(r'^(嗯|好|好的|明白了|思考：|推理：)[，,：:\s]*', '', response)
        
        # 清理多余换行和空格
        response = re.sub(r'\n\s*\n', '\n', response)
        response = re.sub(r'^\s+|\s+$', '', response)
        
        # 空回复保护
        if not response or len(response) < 2:
            response = "我在这里倾听你，可以多说说你的感受吗？"
        
        # 直接显示纯净结果
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})