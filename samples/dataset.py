"""Sample dataset for the RAG demo. Includes documents about Python and ML basics."""

SAMPLE_DOCUMENTS = [
    {
        "id": "doc_python_intro",
        "text": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming."
    },
    {
        "id": "doc_python_features",
        "text": "Key features of Python include dynamic typing, automatic memory management, extensive standard library, and strong community support. Python is widely used for web development, data science, and machine learning."
    },
    {
        "id": "doc_ml_basics",
        "text": "Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. Common ML tasks include classification, regression, and clustering."
    },
    {
        "id": "doc_ml_algorithms",
        "text": "Popular machine learning algorithms include decision trees, random forests, support vector machines (SVM), neural networks, and gradient boosting. Each has different use cases and performance characteristics."
    },
    {
        "id": "doc_neural_networks",
        "text": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers. Deep learning uses neural networks with many layers."
    },
    {
        "id": "doc_nlp_overview",
        "text": "Natural Language Processing (NLP) is a branch of AI that focuses on enabling computers to understand, interpret, and produce human language. Applications include translation, sentiment analysis, and question answering."
    },
    {
        "id": "doc_embeddings",
        "text": "Embeddings are dense vector representations of text or other data. Word embeddings like Word2Vec and GloVe capture semantic relationships between words. Embeddings are fundamental to modern NLP and retrieval systems."
    },
    {
        "id": "doc_rag_definition",
        "text": "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with generative AI. It retrieves relevant documents and uses them to augment the prompt for a language model, improving factuality and relevance."
    },
]
