import os

# --------------------- 以下保留 llamaindex.py 內原本的 import -----------------------
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.chat_engine.context import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.prompts import PromptTemplate
from prompt import assistant_prompt

# --------------------- 以下為 rag_test.py 所需的 import -----------------------
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import BaseRetriever, VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import QueryBundle
from llama_index.core.schema import Node, NodeWithScore
from langchain.schema import Document as LangChainDocument
from langchain_community.retrievers import BM25Retriever
from typing import List

# --------------------- rag_test.py 中的自定義 Hybrid Retriever ----------------------
class CustomHybridRetriever(BaseRetriever):
    def __init__(self, vector_retriever, keyword_retriever, mode="OR"):
        self.vector_retriever = vector_retriever
        self.keyword_retriever = keyword_retriever
        self.mode = mode  # 支援 "OR" 或 "AND"

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        vector_nodes = self.vector_retriever.retrieve(query_bundle)
        keyword_docs = self.keyword_retriever.invoke(query_bundle.query_str)

        vector_content_map = {n.node.get_content(): n for n in vector_nodes}
        keyword_content_map = {d.page_content: d for d in keyword_docs}

        if self.mode == "AND":
            shared_keys = set(vector_content_map.keys()).intersection(set(keyword_content_map.keys()))
        else:  # OR 模式
            shared_keys = set(vector_content_map.keys()).union(set(keyword_content_map.keys()))

        # 將 keyword_docs 補成 NodeWithScore
        converted_keyword_nodes = []
        for content in keyword_content_map:
            if content not in vector_content_map:  # 避免重複加入
                fake_node = NodeWithScore(node=Node(text=content, metadata={}), score=0.0)
                converted_keyword_nodes.append(fake_node)

        return list(vector_content_map.values()) + converted_keyword_nodes


# --------------------- 以下保留 llamaindex.py 原本核心邏輯：管理多使用者 + 對話 ----------------------
user_chat_engines = {}

def assistant_create(user_id, user_name):
    """為特定使用者創建 ChatEngine，並替換 RAG 為 Hybrid Retriever"""
    global user_chat_engines

    # 原本的部分
    input_dir_path = './files'
    llm = Ollama(
        model="gemma3:27b",
        request_timeout=120.0
    )
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-m3",
        trust_remote_code=True
    )

    # ------------------- 以下替換成 rag_test 的做法：載入資料 + 建 Hybrid Retriever -------------------
    documents = SimpleDirectoryReader(
        input_dir=input_dir_path, 
        required_exts=[".pdf"],  # 依實際需求調整
        recursive=True
    ).load_data()

    # 切分段落
    parser = SentenceSplitter(chunk_size=256, chunk_overlap=64)
    nodes = parser.get_nodes_from_documents(documents)

    # 建立向量索引
    index = VectorStoreIndex(nodes, embed_model=embed_model)
    vector_retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

    # 建立 BM25 Retriever
    langchain_documents = [
        LangChainDocument(page_content=doc.get_content(), metadata=doc.metadata)
        for doc in documents
    ]
    keyword_retriever = BM25Retriever.from_documents(langchain_documents)

    # Hybrid Retriever
    retriever = CustomHybridRetriever(
        vector_retriever=vector_retriever,
        keyword_retriever=keyword_retriever,
        mode="OR"
    )

    # ------------------- 其餘(記憶體、prompt、ContextChatEngine)保持不動 -------------------
    memory = ChatMemoryBuffer(token_limit=10000)

    prompt, profile = assistant_prompt(user_name)
    context_template = PromptTemplate(prompt)

    # 建立患者對話紀錄資料夾
    path = f"./chat_record/{user_name}"
    if not os.path.isdir(path):
        os.mkdir(path)

    # 寫入患者基本資料
    with open(f"./chat_record/{user_name}/{user_id}.txt", 'w', encoding='utf-8') as f:
        f.write("---------------------------------------------\n")
        f.write(f"{profile}\n")
        f.write("---------------------------------------------\n")

    # 使用 ContextChatEngine，但 retriever 換成自訂 Hybrid
    user_chat_engines[user_id] = ContextChatEngine(
        retriever=retriever,
        llm=llm,
        memory=memory,
        prefix_messages=[],
        context_template=context_template
    )

    print(f"✅ ChatEngine 初始化成功，使用者 {user_name} ({user_id})")

def assistant_reply(user_id, user_name, message):
    """根據使用者 ID 回應訊息，並印出 RAG 搜尋依據"""
    global user_chat_engines

    # 進行對話
    response = user_chat_engines[user_id].chat(str(message))

    # 將回應記錄到檔案
    with open(f"./chat_record/{user_name}/{user_id}.txt", 'a', encoding='utf-8') as f:
        f.write(f"client: {message}\n")
        f.write("---------------------------------------------\n")
        f.write(f"mental health: {response}\n")
        f.write("---------------------------------------------\n")

    # ------------------- 以下為印出搜尋依據的功能（模仿 rag_test.py） -------------------
    print("\n=== 🔎 回答 ===")
    print(str(response))

    # 注意：以下示範如果 response 沒有 source_nodes 屬性，需要先檢查
    print("\n=== 📄 資料來源 ===")
    if hasattr(response, "source_nodes") and response.source_nodes:
        for i, node in enumerate(response.source_nodes):
            score = getattr(node, "score", "N/A")
            # metadata 可能存有 'file_path' 或其他關鍵資訊，依實際情況調整
            file_path = node.node.metadata.get('file_path') if hasattr(node, 'node') else ""
            content = node.node.get_content()[:200] if hasattr(node, 'node') else "N/A"

            print(f"[來源 {i+1}] (score: {score}) 來自檔案: {file_path}")
            print(content)
            print("-" * 40)
    else:
        print("沒有來源資料或 response 不包含 source_nodes")

    return str(response)
