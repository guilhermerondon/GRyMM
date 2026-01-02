from enum import IntEnum

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
