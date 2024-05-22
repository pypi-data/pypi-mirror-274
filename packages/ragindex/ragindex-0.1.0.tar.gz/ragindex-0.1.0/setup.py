# from setuptools import setup, find_packages

# with open('requirements.txt') as f:
#     required_packages = f.read().splitlines()

# setup(
#     name='ragpy',
#     version='0.1.0',
#     author="BayesLabs",
#     author_email="contact@bayeslabs.co",
#     packages=find_packages(),
#     py_modules=["ragpy.src.dataprocessing.data_loader",
#     "ragpy.src.embeddings_creation.embedding_generator",
#     "ragpy.src.retriever.retrieval",
#     "ragpy.src.retriever.retrieval_benchmarking",
#     "ragpy.src.generator.generation_benchmarking"],
#     install_requires = required_packages
# )
from setuptools import setup, find_packages
setup( 
    name='ragindex',
    version='0.1.0',                                                                                                                  
    author="BayesLabs", 
    author_email="contact@bayeslabs.co",
    packages=find_packages(),
    py_modules=[
        "ragpy.src.dataprocessing.data_loader",
        "ragpy.src.embeddings_creation.embedding_generator",
        "ragpy.src.retriever.retrieval",
        "ragpy.src.retriever.retrieval_benchmarking",
        "ragpy.src.generator.generation_benchmarking"
    ],
    install_requires=[
        "langchain==0.1.9",
        "sentence_transformers==2.2.2",
        "langchain_community==0.0.34",
        "datasets>=2.19.1",
        "langchain-openai==0.1.3",
        "langchain-fireworks==0.1.2",
        "pypdf2>=3.0.1",
        "chardet>=5.2.0",
        "nltk>=3.8.1",
        "chromadb>=0.4.24",
        "faiss-cpu>=1.8.0",
        "InstructorEmbedding>=1.0.1",
        "langchain_text_splitters>=0.0.2",
        "pandas==2.2.2"     
    ]  
) 

