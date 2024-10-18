from elasticsearch import Elasticsearch

# Conectando-se ao Elastic Cloud usando as credenciais
es = Elasticsearch(
   "http://localhost:9201",
)

def create_index_if_not_exists(index_name):
    try:
        # Verifica se o índice já existe
        if not es.indices.exists(index=index_name):
            # Cria o índice se ele não existir
            es.indices.create(index=index_name)
            print(f"Índice '{index_name}' criado com sucesso.")
        else:
            print(f"Índice '{index_name}' já existe.")
    except Exception as e:
        print(f"Erro ao verificar ou criar o índice '{index_name}': {e}")

create_index_if_not_exists("eventos")

# Verificar se a conexão foi bem-sucedida
if es.ping():
    print("Conectado ao Elasticsearch!")
else:
    print("Falha ao conectar ao Elasticsearch.")
    
# Definir a query que corresponde a todos os documentos
query = {
    "query": {
        "match_all": {}
    }
}

# Deletar todos os documentos
response = es.delete_by_query(index="eventos", body=query)

# Exibir resposta da operação
print(f"Documentos deletados: {response['deleted']}")