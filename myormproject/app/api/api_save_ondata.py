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