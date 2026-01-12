import pytest

from apps.aluno.core.enum import NivelAluno
from apps.aluno.models import Aluno
from apps.aluno.services import AlunoService
from apps.exercicios.models import Exercicio

# cria alunos fakes


@pytest.fixture
def aluno_iniciante():
    return Aluno(
        nome="miguel",
        idade=20,
        peso=70,
        tempo_pratica_meses=3,
    )


@pytest.fixture
def aluno_intermediario():
    return Aluno(
        nome="Guilherme",
        idade=24,
        peso=103,
        tempo_pratica_meses=12,
    )


@pytest.fixture
def aluno_experiente():
    return Aluno(
        nome="Ronnie",
        idade=50,
        peso=130,
        tempo_pratica_meses=36,
    )


# assegura que o nível do aluno esteja correto


def exercicio_begginer_mock(nivel: int | None = None):
    return Exercicio.objects.create(
        external_id="0018",
        name="Old name",
        target="triceps",
        difficulty=nivel,
        category="strength",
        body_part="upper arms",
        equipment="towel",
        secondary_muscles=[],
        instructions=[],
        description="old",
        gif_url="https://old.gif",
    )


def test_definir_nivel_iniciante(aluno_iniciante):
    nivel = AlunoService.definir_level(aluno_iniciante)
    assert nivel == NivelAluno.INICIANTE


def test_definir_nivel_intermediario(aluno_intermediario):
    nivel = AlunoService.definir_level(aluno_intermediario)
    assert nivel == NivelAluno.INTERMEDIARO


def test_definir_nivel_experiente(aluno_experiente):
    nivel = AlunoService.definir_level(aluno_experiente)
    assert nivel == NivelAluno.EXPERIENTE


# mock da API externa


@pytest.mark.django_db
# teste de definição de nível API Mockada
def test_exercicio_iniciante_para_aluno_iniciante(aluno_iniciante):

    exercicio = exercicio_begginer_mock(nivel=NivelAluno.INICIANTE.value)

    AlunoService.validar_exercicio_para_aluno(
        aluno_iniciante,
        exercicio=NivelAluno(exercicio.difficulty),
    )


@pytest.mark.django_db
def test_exercicio_iniciante_para_aluno_experiente(aluno_experiente):

    exercicio = exercicio_begginer_mock(nivel=NivelAluno.INICIANTE.value)

    AlunoService.validar_exercicio_para_aluno(
        aluno_experiente,
        exercicio=NivelAluno(exercicio.difficulty),
    )


@pytest.mark.django_db
def test_exercicio_intermediario_para_aluno_iniciante_erro(
    aluno_iniciante,
):

    exercicio = exercicio_begginer_mock(nivel=NivelAluno.INTERMEDIARO.value)

    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_iniciante,
            exercicio,
        )


@pytest.mark.django_db
def test_exercicio_experiente_para_aluno_intermediario_erro(
    aluno_intermediario,
):

    exercicio = exercicio_begginer_mock(nivel=NivelAluno.EXPERIENTE.value)

    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_intermediario,
            exercicio,
        )


@pytest.mark.django_db
def test_exercicio_com_dificuldade_invalida(aluno_iniciante):

    exercicio = exercicio_begginer_mock(nivel=20)

    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_iniciante,
            exercicio,
        )
