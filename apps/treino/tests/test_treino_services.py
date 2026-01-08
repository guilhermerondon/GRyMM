import pytest
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.aluno.models import Aluno
from apps.aluno.services import NivelAluno
from apps.exercicios.models import Exercicio
from apps.treino.models import Treino, TreinoExercicio
from apps.treino.services import TreinoService


@transaction.atomic
def criar_treino(*, aluno, nivel, exercicios_por_dia=None):
    """
    Cria um treino ativo para um aluno.
    Não permite mais de um treino ativo por aluno.
    """

    # Verifica se já existe treino ativo
    if Treino.objects.filter(aluno=aluno, ativo=True).exists():
        raise ValidationError("Aluno já possui um treino ativo.")

    # Cria o treino
    treino = Treino.objects.create(
        aluno=aluno,
        nivel=nivel,
        ativo=True,
    )

    # Cria os exercícios do treino, se houver
    if exercicios_por_dia:
        for dia, exercicios in exercicios_por_dia.items():
            for exercicio in exercicios:
                TreinoExercicio.objects.create(
                    treino=treino,
                    dia=dia,
                    exercicio_id_externo=exercicio["id"],
                    nome_exercicio=exercicio["nome"],
                    grupo_muscular=exercicio["grupo_muscular"],
                    categoria=exercicio["categoria"],
                )

    return treino


def test_estrutura_iniciante():
    # valida a regra de estrutura de treinos atráves dos níveis
    # assegura que o INCIANTE terá somente o ABC
    dias = TreinoService.estrutura_por_nivel(NivelAluno.INICIANTE)

    assert dias == ["A", "B", "C"]


def test_validar_exercicio_payload_valido():
    # valida passagem de payload valido
    exercicio = {
        "id": 123,
        "repeticoes": 12,
        "series": 3,
    }

    TreinoService._validar_exercicio_payload(exercicio)


def test_validar_exercicio_payload_invalido():
    # barra passagem de payload inválido
    # falta de paramêtro - series
    exercicio = {
        "id": 123,
        "repeticoes": 12,
    }

    with pytest.raises(ValidationError) as exc_info:
        TreinoService._validar_exercicio_payload(exercicio)

        assert "series" in str(exc_info.value)


@pytest.fixture
def aluno_iniciante(db):
    return Aluno.objects.create(
        nome="Aluno Miguel",
        idade=21,
        peso=70,
        tempo_pratica_meses=1,
    )


def criar_exercicios(
    target: str,
    nivel: NivelAluno,
    quantidade: int,
):
    for i in range(quantidade):
        Exercicio.objects.create(
            external_id=f"{target}-{i}",
            name=f"Exercicio {target} {i}",
            target=target,
            difficulty=nivel,
            category="strength",
            body_part="upper body",
            equipment="body weight",
            instructions=["Passo 1", "Passo 2"],
            gif_url="http://test.com/gif.gif",
        )


@pytest.mark.django_db
# descontinuar após passar .montat via mock
def testar_montar_treino_iniciante_cria_treino_completo(aluno_iniciante):

    aluno = aluno_iniciante

    # treino A
    criar_exercicios(target="chest", quantidade=3, nivel=NivelAluno.INICIANTE.value)
    criar_exercicios(target="biceps", quantidade=2, nivel=NivelAluno.INICIANTE.value)

    # treino B
    criar_exercicios(target="back", quantidade=3, nivel=NivelAluno.INICIANTE.value)
    criar_exercicios(target="triceps", quantidade=2, nivel=NivelAluno.INICIANTE.value)

    # treino C
    criar_exercicios(target="legs", quantidade=5, nivel=NivelAluno.INICIANTE.value)

    treino = TreinoService.montar_treino(aluno)

    assert treino is not None

    assert treino.exercicios.count() == 15
