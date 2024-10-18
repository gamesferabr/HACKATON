import hashlib
from app.services.evento_services import EventoService
from app.api.schemas.evento_schema import EventoSchema
from app.services.utils.elastic import es
from app.services.scrap_articket_services import Scrap
from app.services.scrap_bilheteria_express import ScrapBilhetariaExpress


class SaveEventoService:
    @staticmethod
    def generate_unique_id(event):
        """ 
        Gera um ID único para cada evento a partir de uma string única.
        """
        unique_string = f"{event['nome']}_{event['local']}_{event['data_inicio']}"
        unique_id = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
        return unique_id
    
    @staticmethod
    def salvar_evento():
        """
        Salva eventos no MySQL e no Elasticsearch.
        """
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
        
        try:
            contador = SaveEventoService.count_elastic_documents()
                            
            if contador == 0:
                contador = 0

            for dado in dados:
                if isinstance(dado, dict):
                    unique_id = SaveEventoService.generate_unique_id(dado)
                    
                    if es.exists(index='eventos', id=unique_id):
                        print(f"Documento com ID {unique_id} já existe. Pulando...")
                        continue
                    
                    contador += 1
                    dado['contador'] = contador
                    dado['id'] = unique_id
                    
                    es.index(index='eventos', id=unique_id, body=dado)
                    
                    SaveEventoService.salvar_evento_mysql(dado)
                    
        except Exception as e:
            return f"Erro ao indexar documentos: {e}"
        
        return "Documentos indexados com sucesso"

    @staticmethod
    def salvar_evento_mysql(dado):
        """ 
        Salva um evento no MySQL.
        """
        try:            
            evento_model = EventoSchema(
                id=dado.get('id', ''),
                link_validacao=dado.get('link_validacao', ''),
                url_imagem=dado.get('url_imagem', ''),
                nome=dado.get('nome', ''),
                data_inicio=dado.get('data_inicio', ''),
                data_fim=dado.get('data_fim', ''),
                local=dado.get('local', ''),
                descricao=dado.get('descricao', ''),
                valor=dado.get('valor', 'R$0.0 - R$0.0')
            )
                        
            service = EventoService()
            service.create(evento_model)
            
            return "Evento salvo com sucesso"
        
        except Exception as e:
            return f"Erro ao salvar evento no MySQL: {e}"

    @staticmethod
    def get_elastic_events(page=1, size=10):
        """
        Recupera eventos ordenados pelo campo 'contador' 
        para garantir que os mais recentes sejam listados primeiro.
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
        """
        Retorna o número total de documentos indexados no índice 'eventos'.
        """
        response = es.count(index="eventos")
        return response['count']
    
    @staticmethod
    def delete_elastic_events():
        """ 
        Deleta todos os documentos indexados no índice 'eventos'.
        """
        query = {
            "query": {
                "match_all": {}
            }
        }
        
        response = es.delete_by_query(index="eventos", body=query)
        return response['deleted']
    
    @staticmethod
    def delete_one_elastic_event(evento_id):
        """ 
        Deleta um documento indexado no índice 'eventos'.
        """
        response = es.delete(index="eventos", id=evento_id)
        return response['result']
    
    @staticmethod
    def update_elastic_event(evento_id, evento):
        """ 
        Atualiza um documento indexado no índice 'eventos'.
        """
        response = es.update(index="eventos", id=evento_id, body={"doc": evento})
        return response['_id']
    