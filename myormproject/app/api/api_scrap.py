from app.services.scrap_articket_services import Scrap
from app.services.scrap_bilheteria_express import ScrapBilhetariaExpress
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

@router.get("/scrap/bilheteriaexpress")
def get_scrap_bilheteriaexpress_events(request):
    eventos = ScrapBilhetariaExpress.get_all_bilheteria_express()
       
    return {"eventos": eventos}