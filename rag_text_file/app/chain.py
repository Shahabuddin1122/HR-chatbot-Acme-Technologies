import os
import chromadb
import dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

dotenv.load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv('GROQ_API_KEY'),
            model="llama-3.1-8b-instant",
        )
        self.chroma_client = chromadb.PersistentClient('vectordb')
        self.collection = self.chroma_client.get_or_create_collection(name="acme_tech")

    def get_response(self, message):
        retriever = self.collection.query(
            query_texts=message,
            n_results=2
        ).get('documents')

        template = """
        You are an expert in HR topics. The user has a question, and you will answer it based on the relevant information provided from the HR manual.

        User question: {user_question}
        Relevant information: {answer}

        Provide a specific and accurate response based on the relevant information above.(NO PREAMBLE)
        """

        prompt_template = PromptTemplate.from_template(template)

        chain = prompt_template | self.llm
        res = chain.invoke(input={'user_question': message, 'answer': retriever})

        return res.content
