import pytest
from apps.aluno.models import Aluno
from apps.treino.services import TreinoService

@pytest.mark.django_db
def test_serializer_cria_treino():
    # Cria aluno válido
    aluno = Aluno.objects.create(
        nome="Aluno Teste",
        idade=20,
        peso=70.0,
        tempo_pratica_meses=12,
    )

    # Payload de exercícios
    payload = {
        "A": [
            {
                "id": "123",
                "nome": "Push Up",
                "grupo_muscular": "peito",
                "categoria": "strength",
                "repeticoes": 15,
                "series": 3,
                "difficulty": "INICIANTE",  # necessário para passar validação
            }
        ] * 5  # 5 exercícios por dia
    }

    # Monta o treino
    treino = TreinoService.montar_treino(
        aluno=aluno,
        exercicios_por_dia=payload,
    )

    assert treino.aluno == aluno
    assert treino.exercicios.count() == 5
    for exercicio in treino.exercicios.all():
        assert exercicio.nome_exercicio == "Push Up"
        assert exercicio.categoria == "strength"
