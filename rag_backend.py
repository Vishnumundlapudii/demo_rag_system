import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

load_dotenv()

class LangChainChatbot:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        
        if os.getenv("E2E_LLM_ENDPOINT"):
            self.llm = ChatOpenAI(
                openai_api_key=os.getenv("E2E_API_KEY"),
                openai_api_base=os.getenv("E2E_LLM_ENDPOINT"),
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
        else:
            self.llm = ChatOpenAI(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 200))
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.vector_store = None
        self.chat_chain = None

    def load_langchain_docs(self):
        """Load LangChain documentation"""
        print("📚 Loading LangChain documentation...")
        
        docs_urls = [
            "https://python.langchain.com/docs/get_started/introduction",
            "https://python.langchain.com/docs/modules/data_connection/document_loaders/",
            "https://python.langchain.com/docs/modules/data_connection/text_splitters/",
            "https://python.langchain.com/docs/modules/data_connection/vectorstores/",
            "https://python.langchain.com/docs/modules/model_io/llms/",
            "https://python.langchain.com/docs/modules/chains/",
            "https://python.langchain.com/docs/use_cases/question_answering/",
            "https://python.langchain.com/docs/modules/memory/",
            "https://python.langchain.com/docs/modules/agents/"
        ]
        
        documents = []
        
        for url in docs_urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                for script in soup(["script", "style"]):
                    script.decompose()
                
                content = soup.get_text()
                content = ' '.join(content.split())
                
                if len(content) > 200:
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": url,
                            "title": soup.title.string if soup.title else "LangChain Documentation"
                        }
                    )
                    documents.append(doc)
                    print(f"✅ Loaded: {url}")
                
            except Exception as e:
                print(f"❌ Error loading {url}: {str(e)}")
                continue
        
        print(f"📖 Successfully loaded {len(documents)} documents")
        return documents

    def setup_vector_store(self, documents):
        """Create and setup vector store"""
        print("🔍 Setting up vector store...")
        
        texts = self.text_splitter.split_documents(documents)
        print(f"📄 Split into {len(texts)} chunks")
        
        vector_store_path = os.getenv("VECTOR_STORE_PATH", "./chroma_db")
        collection_name = os.getenv("COLLECTION_NAME", "langchain_docs")
        
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=vector_store_path,
            collection_name=collection_name
        )
        
        print("✅ Vector store created!")

    def setup_chat_chain(self):
        """Setup conversational retrieval chain"""
        print("🤖 Setting up chat chain...")
        
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        self.chat_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
        
        print("✅ Chat chain ready!")

    def initialize(self):
        """Initialize the complete system"""
        try:
            # Check if vector store already exists
            vector_store_path = os.getenv("VECTOR_STORE_PATH", "./chroma_db")
            
            if os.path.exists(vector_store_path):
                print("📂 Loading existing vector store...")
                self.vector_store = Chroma(
                    persist_directory=vector_store_path,
                    embedding_function=self.embeddings,
                    collection_name=os.getenv("COLLECTION_NAME", "langchain_docs")
                )
            else:
                # Load fresh documents
                documents = self.load_langchain_docs()
                self.setup_vector_store(documents)
            
            self.setup_chat_chain()
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {str(e)}")
            return False

    def chat(self, message):
        """Chat with the bot"""
        if not self.chat_chain:
            return "❌ System not initialized. Please restart the application."
        
        try:
            result = self.chat_chain({"question": message})
            return result["answer"]
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def get_sources(self, message):
        """Get source documents for a query"""
        if not self.chat_chain:
            return []
        
        try:
            result = self.chat_chain({"question": message})
            sources = []
            for doc in result.get("source_documents", []):
                sources.append({
                    "url": doc.metadata.get("source", "Unknown"),
                    "title": doc.metadata.get("title", "LangChain Docs")
                })
            return sources
        except:
            return []

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        return "🧹 Conversation history cleared!"