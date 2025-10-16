from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class Conta(BaseModel):
    nome: str
    descricao: str
    data: str
    valor: float
    situacao: str


contas: Dict[int, Conta] = {}


@app.get("/")
def home():
    return {"Contas a Pagar": len(contas)}


@app.post("/criarConta/")
def criar_conta(conta: Conta):
    print("Dados recebidos:", conta.dict())
    try:
        if not all(
            [conta.nome, conta.descricao, conta.data, conta.valor, conta.situacao]
        ):
            raise HTTPException(
                status_code=422, detail="Todos os campos são obrigatórios"
            )
        nova_conta_id = len(contas) + 1
        contas[nova_conta_id] = conta
        return {"id": nova_conta_id, "mensagem": "Conta criada com sucesso"}
    except Exception as e:
        print("Erro:", e)
        raise


@app.get("/pegarConta/{id_conta}")
def pegar_conta(id_conta: int):
    if id_conta in contas:
        return contas[id_conta]
    else:
        return {"Erro": "ID de conta inexistente"}


@app.put("/atualizarConta/{id_conta}")
def atualizar_conta(id_conta: int, conta: Conta):
    if id_conta in contas:
        contas[id_conta] = conta
        return {"mensagem": "Conta atualizada com sucesso"}
    else:
        return {"Erro": "ID de conta inexistente"}


@app.delete("/deletarConta/{id_conta}")
def deletar_conta(id_conta: int):
    if id_conta in contas:
        del contas[id_conta]
        return {"mensagem": "Conta deletada com sucesso"}
    else:
        return {"Erro": "ID de conta inexistente"}


@app.get("/listarContas/")
def listar_contas():
    return contas
