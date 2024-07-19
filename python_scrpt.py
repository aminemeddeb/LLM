from pymilvus import    connections,utility, MilvusException

connections.connect(host ="localhost", port="19530")

try :
    collections = utility.list_collections()
    print(f"list all collections :\n", collections)
except MilvusException as e :
    print(e)

