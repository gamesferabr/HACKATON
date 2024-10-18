from app.models.model_eventos import Evento
from app.api.schemas.evento_schema import CreateEventoSchema

class EventoRepository():
    def __init__(self):
        pass
    
    @staticmethod
    def verify_is_deleted(evento_id: str):
        if Evento.objects.filter(id=evento_id, is_deleted=True).exists():
            return True
        return False
    
   
    def create(self, evento: CreateEventoSchema):
        # Converte o schema para um dicionário usando o método adequado do Pydantic ou manualmente
        evento_data = evento.dict() if hasattr(evento, 'dict') else dict(evento)
        return Evento.objects.create(**evento_data)

    def get_one(self, evento_id: str):
        return Evento.objects.get(pk=evento_id)
    
    def get_all(self):
        return Evento.objects.all()
    
    def patch(self, evento_id: str, evento: dict):
        existing_evento = Evento.objects.get(pk=evento_id)
        
        for key, value in evento.items():
            setattr(existing_evento, key, value)
        
        existing_evento.save()
        
        return existing_evento  
    
    def logic_delete(self, evento_id: str):
        evento = Evento.objects.get(pk=evento_id)
        evento.is_deleted = True
        evento.save()
        
        return evento