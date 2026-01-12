from unittest.mock import Mock, patch

import pytest
import requests_mock

from apps.aluno.core.enum import NivelAluno
from apps.aluno.models import Aluno
from apps.exercicios.models import Exercicio
from apps.exercicios.services import ExercicioService
from apps.treino.services import TreinoService


@pytest.mark.django_db
@patch("apps.exercicios.services.requests.get")
# testa busca de exercicios via Mock
# cria o mock - define um valor que é considerado 200
# passa o "triceps" como simulação e intercepta o request no busca_por_musculo
def test_buscar_exercicios_por_musculo_cria_exercicio(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "bodyPart": "upper arms",
            "equipment": "assisted (towel)",
            "id": "0018",
            "name": "assisted standing triceps extension (with towel)",
            "target": "triceps",
            "secondaryMuscles": ["shoulders"],
            "instructions": ["instruction 1"],
            "description": "Exercise description",
            "difficulty": NivelAluno.INICIANTE.value,
            "category": "strength",
            "gifUrl": "https://example.com/gif.gif",
        }
    ]

    mock_get.return_value = mock_response

    exercicios = ExercicioService.buscar_por_musculo("triceps")

    assert len(exercicios) == 1
    assert Exercicio.objects.count() == 1

    exercicio = exercicios[0]
    assert exercicio.external_id == "0018"
    assert exercicio.target == "triceps"
    assert exercicio.difficulty == NivelAluno.INICIANTE.value


@pytest.mark.django_db
@patch("apps.exercicios.services.requests.get")
# testa a atualização de exercicios sem cometer duplicidade
# cria o objeto no banco
# cria o mock/ payload e define que ele é um 200
# passa pelo define de atualizar
# assegura que não foi criado mais um objeto e os nomes foram atualizados
def test_buscar_exercicios_por_musculo_atualiza_exercicio(mock_get):
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

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "bodyPart": "upper arms",
            "equipment": "assisted (towel)",
            "id": "0018",
            "name": "New exercise name",
            "target": "triceps",
            "secondaryMuscles": ["shoulders"],
            "instructions": ["instruction 1"],
            "description": "Updated description",
            "difficulty": NivelAluno.EXPERIENTE.value,
            "category": "strength",
            "gifUrl": "https://new.gif",
        }
    ]

    mock_get.return_value = mock_response

    ExercicioService.buscar_por_musculo("triceps")

    assert Exercicio.objects.count() == 1

    exercicio = Exercicio.objects.first()
    assert exercicio.name == "New exercise name"
    assert exercicio.gif_url == "https://new.gif"


@pytest.mark.django_db
@patch("apps.exercicios.services.requests.get")
# testa a simulação de um erro 500 na API
# cria o mock passando o erro 500
# garante que o código dentro do with dê uma exceção do tipo RunTimeError
def test_buscar_exercicios_por_musculo_erro_api(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError):
        ExercicioService.buscar_por_musculo("triceps")


def gerar_exercicios_mock(
    target: str,
    quantidade: int,
    difficulty: str = "beginner",
):
    return [
        {
            "id": f"{target}-{i}",
            "name": f"Exercicio {target} {i}",
            "target": target,
            "difficulty": difficulty,
            "category": "strength",
            "bodyPart": "upper body",
            "equipment": "body weight",
            "instructions": ["Passo 1", "Passo 2"],
            "gifUrl": "http://test.com/gif.gif",
        }
        for i in range(quantidade)
    ]


EXERCISEDB_RESPONSE = (
    gerar_exercicios_mock("chest", 3)
    + gerar_exercicios_mock("biceps", 2)
    + gerar_exercicios_mock("back", 3)
    + gerar_exercicios_mock("triceps", 2)
    + gerar_exercicios_mock("legs", 5)
)


@pytest.fixture
def aluno_iniciante(db):
    return Aluno.objects.create(
        nome="Aluno Miguel",
        idade=21,
        peso=70,
        tempo_pratica_meses=1,
    )


@pytest.mark.django_db
def test_fluxo_completo_exercisedb_para_treino(
    aluno_iniciante,
):
    with requests_mock.Mocker() as m:
        m.get(
            "https://api.exercisedb.com/exercises",
            json=EXERCISEDB_RESPONSE,
        )

        response = EXERCISEDB_RESPONSE

        ExercicioService.importar_exercicios(response)

        treino = TreinoService.montar_treino(aluno_iniciante)

        assert treino is not None
        assert treino.exercicios.count() == 15
