import pytest

from apps.aluno.core.enum import NivelAluno
from apps.aluno.models import Aluno
from apps.exercicios.models import Exercicio
from apps.treino.models import Treino
from apps.treino.serializers import TreinoExercicioSerializer


@pytest.mark.django_db
# valida se o serializer está válido
# envia o payload
# assegura se o .is_valid é true
# confirma se o nome bate com as informações do payload
def test_exercicio_serializer_valido():

    aluno = Aluno.objects.create(
        nome="miguel",
        idade=20,
        peso=70,
        tempo_pratica_meses=3,
    )

    Treino.objects.create(
        aluno=aluno,
        nivel=1,
        ativo=True,
    )

    Exercicio.objects.create(
        external_id="0018",
        name="Old name",
        target="triceps",
        difficulty=NivelAluno.INICIANTE.value,
        category="strength",
        body_part="upper arms",
        equipment="towel",
        secondary_muscles=[],
        instructions=[],
        description="old",
        gif_url="https://old.gif",
    )

    payload = {
        "treino": 1,
        "exercicio_id": 1,
        "dia": "A",
        "ordem": 1,
        "repeticoes": 10,
        "series": 3,
    }

    serializer = TreinoExercicioSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["dia"] == "A"


@pytest.mark.django_db
# valida se o serializer está inválido
# envia o payload
# não passa o paramêtro de nome exercio
# assegura se o is_valid é falso
# confirma se o erro tem relação com o parâmetro não passado
def test_serializer_invalido_nome_exercicio():
    payload = {
        "treino": "Biceps",
        # "exercicio":"Biceps",
        "dia": "A",
        "ordem": 1,
        "repeticoes": 10,
        "series": 3,
    }

    serializer = TreinoExercicioSerializer(data=payload)

    assert serializer.is_valid() is False
    assert "exercicio_id" in serializer.errors
