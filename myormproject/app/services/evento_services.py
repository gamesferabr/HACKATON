from app.repositories.evento import EventoRepository

class EventoService():
    def __init__(self):
        self.evento_repository = EventoRepository()

    def create(self, evento):
        return self.evento_repository.create(evento)

    def get_one(self, id):
        if self.evento_repository.verify_is_deleted(id):
            return None
        return self.evento_repository.get_one(id)
    
    def get_all(self):
        return list(self.evento_repository.get_all())

    def patch(self, id, evento):
        if self.evento_repository.verify_is_deleted(id):
            return None
        return self.evento_repository.patch(id, evento)

    def delete(self, id):
        if self.evento_repository.verify_is_deleted(id):
            return None
        return self.evento_repository.delete(id)
    