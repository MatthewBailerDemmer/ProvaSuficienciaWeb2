def resposta_api(data=None, message="Sucess", status: int = 200, erro=None):
    return{
        "status": status,
        "message": message,
        "data": data,
        "erro":erro
    }