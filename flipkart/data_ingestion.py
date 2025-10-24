from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import FlipartRecommenderConfig

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=FlipartRecommenderConfig.EMBEDDING_MODEL)
        self.vectorstore = AstraDBVectorStore(
            collection_name='flipkart_database',
            embedding=self.embedding,
            api_endpoint=FlipartRecommenderConfig.ASTRA_DB_API_ENDPOINT,
            token=FlipartRecommenderConfig.ASTRA_DB_APPLICATION_TOKEN,
            namespace=FlipartRecommenderConfig.ASTRA_DB_KEYSPACE
        )

    def ingest(self, load_existing=True):
        if load_existing==True:
            return self.vectorstore
        
        docs = DataConverter("data/flipkart_product_review.csv").convert_to_doc()

        self.vectorstore.add_documents(docs)

        return self.vectorstore
    
if __name__=='__main__':
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)    