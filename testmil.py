from pymilvus import MilvusClient, model

# Ensure you have the correct connection details
client = MilvusClient(uri="tcp://172.17.48.1:19530")  # Update the URI if necessary

try:
    # Check if the collection exists and drop it if it does
    if client.has_collection(collection_name="demo_collection"):
        client.drop_collection(collection_name="demo_collection")

    # Create a new collection
    client.create_collection(
        collection_name="demo_collection",
        dimension=768,  # The vectors we will use in this demo have 768 dimensions
    )

    # Initialize the embedding function
    embedding_fn = model.DefaultEmbeddingFunction()

    # Sample documents
    docs = [
        "Artificial intelligence was founded as an academic discipline in 1956.",
        "Alan Turing was the first person to conduct substantial research in AI.",
        "Born in Maida Vale, London, Turing was raised in southern England.",
    ]

    # Encode documents to vectors
    vectors = embedding_fn.encode_documents(docs)
    print("Dim:", embedding_fn.dim, vectors[0].shape)  # Dim: 768 (768,)

    # Prepare data for insertion
    data = [
        {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"}
        for i in range(len(vectors))
    ]

    print("Data has", len(data), "entities, each with fields: ", data[0].keys())
    print("Vector dim:", len(data[0]["vector"]))

except Exception as e:
    print(f"An error occurred: {e}")
