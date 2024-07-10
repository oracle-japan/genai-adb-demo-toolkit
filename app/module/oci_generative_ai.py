import os
from dotenv import load_dotenv, find_dotenv

import oracledb
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy

from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
from langchain_community.embeddings.oci_generative_ai import OCIGenAIEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class OciGenerativeAi:
    def __init__(
        self,
        compartment_id: str,
        service_endpoint: str,
        model_name: str = "cohere.command-r-plus",
        is_stream: bool = True,
        max_tokens: int = 500,
        temperature: float = 0.3,
        top_k: int = 0,
        top_p: float = 0.75,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
    ) -> None:
        """Initialize OciGenerativeAi"""
        self.chat_model = ChatOCIGenAI(
            auth_type="INSTANCE_PRINCIPAL",
            model_id=model_name,
            compartment_id=compartment_id,
            service_endpoint=service_endpoint,
            is_stream=is_stream,
            model_kwargs={
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
            },
            metadata={
                "model_name": model_name,
                "model_parameters": {
                    "is_stream": is_stream,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty,
                }
            }
        )
        embeddings_model = OCIGenAIEmbeddings(
            auth_type="INSTANCE_PRINCIPAL",
            compartment_id=compartment_id,
            service_endpoint=service_endpoint,
            model_id="cohere.embed-multilingual-v3.0"
        )
        _ = load_dotenv(find_dotenv())
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        dsn = os.getenv("DSN")
        config_dir = os.getenv("CONFIG_DIR")
        wallet_dir = os.getenv("WALLET_DIR")
        wallet_password = os.getenv("WALLET_PASSWORD")
        table_name = os.getenv("TABLE_NAME")
        connection = oracledb.connect(
            dsn=dsn,
            user=username,
            password=password,
            config_dir=config_dir,
            wallet_location=wallet_dir,
            wallet_password=wallet_password
        )
        oraclevs = OracleVS(
            client=connection,
            embedding_function=embeddings_model,
            table_name=table_name,
            distance_strategy=DistanceStrategy.COSINE,
            query="What is a Oracle database",
        )
        self.retriever = oraclevs.as_retriever()

    def chat(
        self,
        input: str,
        is_stream: bool = True,
        is_vector_search: bool = True
    ):
        """Chat feature with OCI Generative AI Services"""
        if is_vector_search == True:
            prompt_template = PromptTemplate.from_template(
                template="""
                    可能な限り、検索によって得られたコンテキスト情報を使って質問に回答してください。
                    
                    ##コンテキスト
                    {context}
                    
                    ## 質問
                    {query}
                """
            )
            chain = (
                {"query": RunnablePassthrough(), "context": self.retriever}
                | prompt_template
                | self.chat_model
                | StrOutputParser()
            )
            if is_stream == True:
                res = chain.stream(input)
                for chunk in res:
                    yield chunk
            else:
                res = chain.invoke(input)
                return res
        else:
            prompt_template = PromptTemplate.from_template(
                template="""
                    以下の質問に回答してください。
                    
                    ## 質問
                    {query}
                """
            )
            chain = (
                {"query": RunnablePassthrough()}
                | prompt_template
                | self.chat_model
                | StrOutputParser()
            )
            if is_stream == True:
                res = chain.stream(input)
                for chunk in res:
                    yield chunk
            else:
                res = chain.invoke(input)
                return res
