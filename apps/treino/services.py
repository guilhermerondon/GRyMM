from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.aluno.models import Aluno
from apps.aluno.services import AlunoService, NivelAluno
from apps.treino.models import Treino, TreinoExercicio


class TreinoService:
    @staticmethod
    # realiza a estrutura de do treino atráves do Nivel recebido
    # caso seja iniciante e intermediário - ABC
    # caso seja avançado ABCD
    def estrutura_por_nivel(nivel: NivelAluno) -> list[str]:
        if nivel in (NivelAluno.INICIANTE, NivelAluno.INTERMEDIARO):
            return ["A", "B", "C"]
        return ["A", "B", "C", "D"]

    @staticmethod
    # realiza a criação do treino passando o ID do aluno
    # regra que um aluno deve ter somente 1 treino ativo por vez
    # faz validação de treino ativo, caso haja ele não passa
    def criar_treino(aluno: Aluno) -> Treino:
        if Treino.objects.filter(aluno=aluno, ativo=True).exists():
            raise ValidationError(_("Aluno já possui um treino ativo"))

        return Treino.objects.create(aluno=aluno)

    @staticmethod
    # realiza a validação se o payload do exercicio tem todos os campos
    # especifica campos obrigatórios - ID, REP e SERIES
    # lógica feita através do .keys que pega os campos e compara
    # se faltar é lançado um erro amigável
    def _validar_exercicio_payload(exercicio: dict):
        campos = {"id", "repeticoes", "series"}
        faltando = campos - exercicio.keys()

        if faltando:
            raise ValidationError(
                _("Campos obrigatórios ausentes: %(campos)s")
                % {"campos": ", ".join(sorted(faltando))}
            )

    @staticmethod
    # adiciona um exercicio em um treino
    # garante que payload de exercicio seja válido
    # valida se o exercicio é adequado ao aluno
    # não duplica exercicios
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
        treino_exercicio, _ = TreinoExercicio.objects.update_or_create(
            treino=treino,
            exercicio_id_externo=exercicio_data["id"],
            # id que será usado com único para armazenar como exercicio externo
            dia=dia,
            defaults={
                # defaults - objetos que podem ser mudados após uma
                # criação ou nova consulta
                "repeticoes": exercicio_data["repeticoes"],
                "series": exercicio_data["series"],
            },
        )

        return treino_exercicio

    @staticmethod
    # realiza a montagem do treino
    # define nível do aluno e estrutura de treino
    # atomic - ou tudo passa ou nada é salvo
    # valida se existe um treino ativo no momento
    # garante que todos os dias obrigatórios existam
    # busca os exercicios no payload
    # valida a quantidade de 5 exercicios por dia
    # faz a criação dos exercicios
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
