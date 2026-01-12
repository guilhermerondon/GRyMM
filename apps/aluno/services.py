from django.utils.translation import gettext_lazy as _

from apps.aluno.core.enum import NivelAluno
from apps.aluno.models import Aluno


class AlunoService:
    @staticmethod
    def definir_level(aluno: Aluno) -> NivelAluno:
        # Define o nível do aluno com base no tempo de prática em meses
        tempo = aluno.tempo_pratica_meses

        if tempo <= 6:
            return NivelAluno.INICIANTE

        if 7 <= tempo <= 24:
            return NivelAluno.INTERMEDIARO

        return NivelAluno.EXPERIENTE

    @staticmethod
    def validar_exercicio_para_aluno(
        aluno: Aluno,
        exercicio: NivelAluno,
    ) -> None:
        # valida se o aluno pode executar um exercicio
        # retornado pela API externa

        nivel_aluno = AlunoService.definir_level(aluno)
        # pega o nível do aluno

        if exercicio is None:
            raise ValueError(_("Exercício sem informação de nível"))
            # garante integridade do domínio

        try:
            nivel_exercicio = NivelAluno(exercicio).value
        except (ValueError, TypeError):
            raise ValueError(_("Nivel de exercicio inválido"))

        if nivel_exercicio > nivel_aluno:
            raise ValueError(
                _(
                    "Exercício de nível %(dificuldade)s não permitido "
                    "para aluno nível %(nivel)s"
                )
                % {
                    "dificuldade": nivel_exercicio.label,
                    "nivel": nivel_aluno.label,
                }
            )
