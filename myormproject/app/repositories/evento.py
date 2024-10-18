from app.models.model_eventos import Evento
from app.api.schemas.evento_schema import CreateEventoSchema

class EventoRepository():
    def __init__(self):
        pass
    
    @staticmethod
    def verify_is_deleted(evento_id: str):
        """ 
        Verifica se um evento foi deletado logicamente.
        """
        if Evento.objects.filter(id=evento_id, is_deleted=True).exists():
            return True
        return False
    
   
    def create(self, evento: CreateEventoSchema):
        """ 
        Cria um evento no banco de dados.
        """
        evento_data = evento.dict() if hasattr(evento, 'dict') else dict(evento)
        return Evento.objects.create(**evento_data)

    def get_one(self, evento_id: str):
        """ 
        Retorna um evento a partir de seu ID.
        """
        return Evento.objects.get(pk=evento_id)
    
    def get_all(self):
        """ 
        Retorna todos os eventos.
        """
        return Evento.objects.all()
    
    def patch(self, evento_id: str, evento: dict):
        """ 
        Atualiza um evento a partir de seu ID.
        """
        existing_evento = Evento.objects.get(pk=evento_id)
        
        for key, value in evento.items():
            setattr(existing_evento, key, value)
        
        existing_evento.save()
        
        return existing_evento  
    
    def logic_delete(self, evento_id: str):
        """ 
        Deleta logicamente um evento a partir de seu ID.
        """
        evento = Evento.objects.get(pk=evento_id)
        evento.is_deleted = True
        evento.save()
        
        return evento