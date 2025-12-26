from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.aluno.services import AlunoService, NivelAluno
from .models import Treino, TreinoExercicio


class TreinoService:
    @staticmethod
    def estrutura_por_nivel(nivel: NivelAluno) -> list[str]:
        if nivel in (NivelAluno.INICIANTE, NivelAluno.INTERMEDIARO):
            return ["A", "B", "C"]
        return ["A", "B", "C", "D"]

    @staticmethod
    def criar_treino(aluno):
        if Treino.objects.filter(aluno=aluno, ativo=True).exists():
            raise ValidationError(_("Aluno já possui um treino ativo"))

        return Treino.objects.create(aluno=aluno)

    @staticmethod
    def _validar_exercicio_payload(exercicio: dict):
        campos = {"id", "repeticoes", "series"}
        faltando = campos - exercicio.keys()

        if faltando:
            raise ValidationError(
                _("Campos obrigatórios ausentes: %(campos)s")
                % {"campos": ", ".join(sorted(faltando))}
            )

    @staticmethod
    def adicionar_exercicio(
        treino: Treino,
        exercicio_data: dict,
        dia: str,
    ):
        TreinoService._validar_exercicio_payload(exercicio_data)

        aluno = treino.aluno

        AlunoService.validar_exercicio_para_aluno(
            aluno=aluno,
            exercicio_data=exercicio_data,
        )

        return TreinoExercicio.objects.create(
            treino=treino,
            exercicio_id_externo=exercicio_data["id"],
            dia=dia,
            repeticoes=exercicio_data["repeticoes"],
            series=exercicio_data["series"],
        )

    @staticmethod
    def montar_treino(
        aluno,
        exercicios_por_dia: dict[str, list[dict]],
    ):
        nivel = AlunoService.definir_level(aluno)
        dias_validos = TreinoService.estrutura_por_nivel(nivel)

        with transaction.atomic():
            treino = TreinoService.criar_treino(aluno)

            for dia in dias_validos:
                exercicios = exercicios_por_dia.get(dia)

                if not exercicios or len(exercicios) != 5:
                    raise ValidationError(
                        _(f"O dia {dia} deve conter exatamente 5 exercícios")
                    )

                for exercicio in exercicios:
                    TreinoService.adicionar_exercicio(
                        treino=treino,
                        exercicio_data=exercicio,
                        dia=dia,
                    )

        return treino
