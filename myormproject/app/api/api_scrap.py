from app.services.scrap import Scrap
from ninja import Router

router = Router()

@router.get("/scrap")
def get_scrap_events(request):
    cidade = ["santos", "são+vicente", "praia+grande", "guarujá", "bertioga", "mongaguá"]
    eventos_lista = []
    
    for i in range(len(cidade)):
        eventos = Scrap.get_all(cidade[i])
        eventos_lista.append(eventos)
       
    
    return {"eventos": eventos_lista}

@router.post("/eventos")
def salvar_eventos(request):
    resultados = []
    
    resultado = Scrap.salvar_evento()
    resultados.append(resultado)
    
    return {"status": "processamento concluído", "resultados": resultados}

@router.get("/eventos/elasticsearch")
def get_elastic_events(request, page: int = 1, size: int = 10):
    eventos = Scrap.get_elastic_events(page, size) 
    eventos = [evento['_source'] for evento in eventos]
    
    count_documentos = Scrap.count_elastic_documents()
    if count_documentos:
        return {"total_documentos": count_documentos, "eventos": eventos}
    
    return eventos