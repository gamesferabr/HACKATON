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
