import pytest

from apps.treino.serializers import TreinoExercicioSerializer


@pytest.mark.django_db
# valida se o serializer está válido
# envia o payload
# assegura se o .is_valid é true
# confirma se o nome bate com as informações do payload
def test_exercicio_serializer_valido():
    payload = {
        "dia": "B",
        "exercicio_id_externo": 1,
        "nome_exercicio": "Push-Up",
        "grupo_muscular": "Peito",
        "categoria": "strength",
    }

    serializer = TreinoExercicioSerializer(data=payload)

    assert serializer.is_valid() is True
    assert serializer.validated_data["nome_exercicio"] == "Push-Up"


@pytest.mark.django_db
# valida se o serializer está inválido
# envia o payload
# não passa o paramêtro de nome exercio
# assegura se o is_valid é falso
# confirma se o erro tem relação com o parâmetro não passado
def test_serializer_invalido_nome_exercicio():
    payload = {
        "dia": "B",
        "exercicio_id_externo": 11,
        "grupo_muscular": "Triceps",
        "categoria": "balance",
    }

    serializer = TreinoExercicioSerializer(data=payload)

    assert serializer.is_valid() is False
    assert "nome_exercicio" in serializer.errors
