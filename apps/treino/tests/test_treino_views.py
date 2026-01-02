import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
# testa criação de aluno e atrelação de treino
# cria o aluno no DB
# cria o treino seguindo padrões no  views - serializers
# assegura se deu como created no retorno do response
def test_criar_treino_view():
    client = APIClient()

    payload_aluno = {
        "nome": "Aluno Miguel",
        "idade": 21,
        "peso": 70,
        "tempo_pratica_meses": 8,
    }

    response_aluno = client.post("/api/alunos/", payload_aluno, format="json")

    # Payload de treino
    payload_treino = {
        "aluno": 1,
        "nivel": "INICIANTE",
        "ativo": True,
    }

    response_treino = client.post(
        "/api/alunos/1/treinos/", payload_treino, format="json"
    )

    assert response_aluno.status_code == 201
    assert response_treino.status_code == 201, response_treino.data
