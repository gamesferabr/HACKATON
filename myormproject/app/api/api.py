from ninja import Router
from app.api.schemas.evento_schema import EventoSchema, CreateEventoSchema, UpdateEventoSchema
from app.services.evento_services import EventoService

router = Router()

@router.get("/eventos", response={200: list[EventoSchema]})
def get_eventos(request):
    service = EventoService()
    users = service.get_all()
    return list(users)

@router.get("/eventos/{evento_id}", response={200: EventoSchema})
def get_evento(request, evento_id: str):
    service = EventoService()
    one_user = service.get_one(evento_id)
    return one_user

@router.post("/eventos", response={201: EventoSchema})
def create_evento(request, evento: CreateEventoSchema):
    service = EventoService()
    user_created = service.create(evento)
    return user_created

@router.patch("/eventos/{evento_id}", response={200: EventoSchema})
def patch_evento(request, evento_id: str, evento: UpdateEventoSchema):
    service = EventoService()
    user_patch = service.patch(evento_id, evento.model_dump())
    return user_patch

@router.delete("/eventos/{evento_id}", response={200: str})
def delete_evento(request, evento_id: str):
    service = EventoService()
    service.delete(evento_id)
    return "Evento deletado com sucesso!"
