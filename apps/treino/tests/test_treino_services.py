from django.db import transaction
from django.core.exceptions import ValidationError

from apps.treino.models import Treino, TreinoExercicio


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
