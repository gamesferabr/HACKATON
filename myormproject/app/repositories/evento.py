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
        return Evento.objects.create(**evento.model_dump())

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
        