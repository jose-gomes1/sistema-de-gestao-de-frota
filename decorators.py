import datetime

def log_operacao(funcao):
    def embrulho(*args, **kwargs):
        agora = datetime.datetime.now()
        print(f"[{agora}] A executar: {funcao.__name__}")
        return funcao(*args, **kwargs)
    return embrulho
