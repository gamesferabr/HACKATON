from app.services.save_evento_services import SaveEventoService
from ninja import Router

router = Router()

@router.post("/eventos")
def salvar_eventos(request):
    resultados = []
    
    resultado = SaveEventoService.salvar_evento()
    resultados.append(resultado)
    
    return {"status": "processamento concluído", "resultados": resultados}

@router.get("/eventos/elasticsearch")
def get_elastic_events(request, page: int = 1, size: int = 10):
    eventos = SaveEventoService.get_elastic_events(page, size) 
    eventos = [evento['_source'] for evento in eventos]
    
    count_documentos = SaveEventoService.count_elastic_documents()
    if count_documentos:
        return {"total_documentos": count_documentos, "eventos": eventos}
    
    return eventos

@router.delete("/eventos/elasticsearch")
def delete_elastic_events(request):
    resultado = SaveEventoService.delete_elastic_events()
    
    return {"status": resultado}

@router.delete("/eventos/elasticsearch/{evento_id}")
def delete_elastic_event(request, evento_id: str):
    resultado = SaveEventoService.delete_one_elastic_event(evento_id)
    
    return {"status": resultado}

@router.patch("/eventos/elasticsearch/{evento_id}")
def update_elastic_event(request, evento_id: str, evento: dict):
    resultado = SaveEventoService.update_elastic_event(evento_id, evento)
    
    return {"status": resultado}
