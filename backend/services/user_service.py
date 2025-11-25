from ..dao.user_dao import UserDAO
from ..models.user_model import User

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_new_user(self, name, email):
        # Exemplo de lógica de negócio: validação
        if not name or "@" not in email:
            raise ValueError("Dados de usuário inválidos.")
        
        new_user = User(name=name, email=email)
        user_id = self.user_dao.insert_user(new_user)
        return user_id

    # ... outros métodos de serviço