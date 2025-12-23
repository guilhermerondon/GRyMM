import pytest

from apps.aluno.models import Aluno
from apps.aluno.services import AlunoService, NivelAluno

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

EXERCICIO_INICIANTE = {"difficulty": "begginer"}
EXERCICIO_INTERMEDIARIO = {"difficulty": "intermediate"}
EXERCICIO_EXPERIENTE = {"difficulty": "expert"}


# teste de definição de nível API Mockada
def test_exercicio_iniciante_para_aluno_iniciante(aluno_iniciante):
    AlunoService.validar_exercicio_para_aluno(
        aluno_iniciante,
        EXERCICIO_INICIANTE,
    )


def test_exercicio_iniciante_para_aluno_experiente(aluno_experiente):
    AlunoService.validar_exercicio_para_aluno(
        aluno_experiente,
        EXERCICIO_INICIANTE,
    )


def test_exercicio_intermediario_para_aluno_iniciante_erro(
    aluno_iniciante,
):
    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_iniciante,
            EXERCICIO_INTERMEDIARIO,
        )


def test_exercicio_experiente_para_aluno_intermediario_erro(
    aluno_intermediario,
):
    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_intermediario, EXERCICIO_EXPERIENTE
        )


def test_exercicio_sem_dificuldade(aluno_iniciante):
    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_iniciante,
            {},
        )


def test_exercicio_com_dificuldade_invalida(aluno_iniciante):
    with pytest.raises(ValueError):
        AlunoService.validar_exercicio_para_aluno(
            aluno_iniciante,
            {"difficulty": "unknown"},
        )
