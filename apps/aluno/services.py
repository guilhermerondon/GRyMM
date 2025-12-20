from enum import IntEnum

from aluno.models import Aluno
from django.utils.translation import gettext_lazy as _


class NivelAluno(IntEnum):
    INICIANTE = 1
    INTERMEDIARO = 2
    EXPERIENTE = 3
    # define regra matemática para comparação
    # mais robusta

    @property
    def label(self) -> str:
        labels = {
            NivelAluno.INICIANTE: _("Iniciante"),
            NivelAluno.INTERMEDIARO: _("Intermediário"),
            NivelAluno.EXPERIENTE: _("Experiente"),
        }
        # converte um valor do Enum em um rótulo legível
        return labels[self]


API_DIFICULDADE_MAP = {
    "begginer": NivelAluno.INICIANTE,
    "intermediate": NivelAluno.INTERMEDIARO,
    "expert": NivelAluno.EXPERIENTE,
}  # mapeia dificuldade da API externa


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
        exercicio_data: dict,
    ) -> None:
        # valida se o aluno pode executar um exercicio
        # retornado pela API externa

        nivel_aluno = AlunoService.definir_level(aluno)
        # pega o nível do aluno

        dificuldade_api = exercicio_data.get("difficulty")
        # pega nível do exercicio da API externa

        if not dificuldade_api:
            raise ValueError(_("Exercicio sem informação de dificuldade"))
            # valide se o exercicio tem o campo dificuldade

        nivel_exercicio = API_DIFICULDADE_MAP.get(dificuldade_api.lower())
        # passa nível do exercicio para mapeamento de API externa

        if nivel_exercicio is None:
            raise ValueError(_("Dificuldade de exercicio inválida"))
            # valida se é existente

        if nivel_exercicio > nivel_aluno:
            raise ValueError(
                _(
                    "Exercicio de nível %(dificuldade)s nao permitido"
                    "para aluno nível %(nivel)s"
                )
                % {
                    "dificuldade": nivel_exercicio.label,
                    "nivel": nivel_aluno.label,
                }
                # valida se é permitido o aluno executar determinado exercicio
                # trata erro
            )
