import hashlib
from app.services.evento_services import EventoService
from app.api.schemas.evento_schema import EventoSchema
from app.services.utils.elastic import es
from app.services.scrap_articket_services import Scrap
from app.services.scrap_bilheteria_express import ScrapBilhetariaExpress

class SaveEventoService:
    @staticmethod
    def generate_unique_id(event):
        unique_string = f"{event['nome']}_{event['local']}_{event['data_inicio']}"
        unique_id = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
        return unique_id
    
    @staticmethod
    def salvar_evento():
        cidade = [  "santos",
                    "são+vicente",
                    "praia+grande",
                    "guarujá",
                    "bertioga",
                    "mongaguá"]
        
        dados = []
        
        for i in range(len(cidade)):
            eventos = Scrap.get_all(cidade[i])
            if len(eventos) > 0:
                dados.extend(eventos)
        
        eventos = ScrapBilhetariaExpress.get_all_bilheteria_express()
        if len(eventos) > 0:
            dados.extend(eventos)
                
        
        len_dados = len(dados)
        
        print(f"Executando salvar_evento! {len_dados} eventos encontrados")
        
        try:
            print("Contando documentos existentes...")
            contador = SaveEventoService.count_elastic_documents()
                            
            if contador == 0:
                contador = 0

            for dado in dados:
                if isinstance(dado, dict):
                    unique_id = SaveEventoService.generate_unique_id(dado)
                    
                    # Verificar se o documento já existe no índice
                    if es.exists(index='eventos', id=unique_id):
                        print(f"Documento com ID {unique_id} já existe. Pulando...")
                        continue
                    
                    contador += 1
                    dado['contador'] = contador
                    print(f"Indexando documento {contador}...")
                    dado['id'] = unique_id
                    
                    # Indexa o documento usando o ID gerado e o contador atualizado
                    es.index(index='eventos', id=unique_id, body=dado)
                    print(dado)
                    
                    SaveEventoService.salvar_evento_mysql(dado)
                    
        except Exception as e:
            print(f"Erro ao indexar documentos: {e}")
            return f"Erro ao indexar documentos: {e}"
        
        return "Documentos indexados com sucesso"

    @staticmethod
    def salvar_evento_mysql(dado):
        try:
            print("Salvando evento no MySQL...")
            
            # Criar a instância do modelo Evento com os dados
            evento_model = EventoSchema(
                id=dado.get('id', ''),
                link_validacao=dado.get('link_validacao', ''),
                url_imagem=dado.get('url_imagem', ''),
                nome=dado.get('nome', ''),
                data_inicio=dado.get('data_inicio', ''),
                data_fim=dado.get('data_fim', ''),
                local=dado.get('local', ''),
                descricao=dado.get('descricao', ''),
                valor=dado.get('valor', 'R$0.0 - R$0.0')  # Valor padrão caso esteja ausente
            )
            
            print(evento_model)
            
            # Utilizar o serviço para salvar o evento no banco de dados
            service = EventoService()
            service.create(evento_model)

            print("Evento salvo com sucesso")
            
            return "Evento salvo com sucesso"
        
        except Exception as e:
            print(f"Erro ao salvar evento no MySQL: {e}")
            return f"Erro ao salvar evento no MySQL: {e}"

    @staticmethod
    def get_elastic_events(page=1, size=10):
        """
        Recupera eventos ordenados pelo campo 'contador' para garantir que os mais recentes sejam listados primeiro.
        """
        query = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {"contador": {"order": "desc"}}
            ],
            "from": (page - 1) * size,
            "size": size
        }
        
        response = es.search(index="eventos", body=query)
        return response['hits']['hits']
    
    @staticmethod
    def count_elastic_documents():
        response = es.count(index="eventos")
        return response['count']
    
    @staticmethod
    def delete_elastic_events():
        query = {
            "query": {
                "match_all": {}
            }
        }
        
        response = es.delete_by_query(index="eventos", body=query)
        return response['deleted']