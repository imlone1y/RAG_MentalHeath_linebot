from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.chat_engine.context import ContextChatEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.prompts import PromptTemplate
from transformers import pipeline
import os


def manage_chat(user_id, user_name):
    input_dir_path = f'./chat_record/{user_name}'
    
    # 設定嵌入模型和 LLM
    llm = Ollama(model="gemma3:27b", request_timeout=120.0)

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3", trust_remote_code=True)

    # **載入數據**
    loader = SimpleDirectoryReader(input_dir=input_dir_path, required_exts=[".txt"], recursive=True)
    docs = loader.load_data()

    # **創建索引**
    index = VectorStoreIndex.from_documents(docs, embed_model=embed_model, show_progress=True)


    # **創建檢索器**
    retriever = VectorIndexRetriever(index=index)
    retriever.retrieve("最近的諮詢紀錄")


    # **創建記憶體緩衝區**
    memory = ChatMemoryBuffer(token_limit=10000)

    # **設定 Prompt**
    prompt = """
    你是一位專業的心理諮商記錄分析師，專門負責整理心理諮商對話的重點，並評估諮詢是否成功。你的任務包括：
    1. **摘要本次諮詢的核心內容**：
    - 患者的主要困擾是什麼？
    - 患者在對話中表達了哪些情緒變化？
    - 這次諮詢的關鍵轉折點是什麼？（例如患者開始願意表達感受、接受建議）
    2. **分析諮詢過程**：
    - 機器人如何引導患者表達情緒？
    - 是否提供了適當的建議？
    - 患者是否接受這些建議？
    3. **判斷諮詢是否成功**：
    - 患者是否表達感謝或情緒明顯改善？
    - 他是否表示感覺「好一些了」或「問題得到幫助」？
    - 是否仍然存在未解決的問題？
    - 是否需要進一步跟進？

    請以簡單易懂的方式整理重點，不要逐字抄寫對話。最後請給出對這次諮詢的**總結與評估**，並標示「諮詢成功」或「需要進一步諮詢」。

    **請使用繁體中文回應，格式如下：**

    **📌 諮詢摘要：**
    - **患者姓名**：{user_name}
    - **主要困擾**：{patient_issue}
    - **情緒變化**：
    - 初始狀態：{initial_emotion}
    - 過程中變化：{emotion_changes}
    - 最終狀態：{final_emotion}
    - **關鍵對話轉折點**：
    - {turning_points}

    **📊 分析與評估：**
    - **機器人引導方式**：{guidance_analysis}
    - **患者對建議的反應**：{response_to_advice}
    - **是否需要後續諮詢**：{follow_up_needed}

    **✅ 諮詢結果：**
    {consultation_result}
    """

    # context_template = PromptTemplate(prompt)

    # **創建 ContextChatEngine**
    chat_engine = ContextChatEngine(
        retriever=retriever,
        llm=llm,
        memory=memory,
        prefix_messages=[],
        # context_template=context_template
    )

    path = f"./chat_analyzed/{user_name}"
    if not os.path.isdir(path):
        os.mkdir(path)

    # **開始諮詢紀錄分析**
    response = chat_engine.chat(prompt)

    # **儲存整理後的紀錄**
    with open(f"./chat_analyzed/{user_name}/{user_name}的諮詢整理.txt", 'a') as f:
        f.write(str(response))

    print(f"🎉 用戶[ {user_name} ]對話紀錄彙整完畢")
