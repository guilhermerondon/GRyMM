import pytest
from apps.aluno.models import Aluno
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_criar_treino_view():
    client = APIClient()

    # Criação do aluno
    aluno = Aluno.objects.create(
        nome="Aluno Teste",
        idade=20,
        peso=70.0,
        tempo_pratica_meses=12,
    )

    # Payload de exercícios
    payload = {
        "nivel": "INICIANTE",
        "exercicios_por_dia": {
            "A": [
                {
                    "id": "123",
                    "nome": "Push Up",
                    "grupo_muscular": "peito",
                    "categoria": "strength",
                    "repeticoes": 15,
                    "series": 3,
                    "difficulty": "INICIANTE",  # necessário
                }
            ]
            * 5
        },
    }

    response = client.post(f"/treinos/", payload, format="json")
    assert response.status_code == 201
