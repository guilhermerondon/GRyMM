import random

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.aluno.models import Aluno
from apps.aluno.services import AlunoService, NivelAluno
from apps.exercicios.models import Exercicio
from apps.exercicios.services import ExercicioService
from apps.treino.models import Treino, TreinoExercicio


class TreinoService:
    # realiza montagem de requests para API externa
    ESTRUTURA_MUSCULAR = {
        "A": {"chest": 3, "biceps": 2},
        "B": {"back": 3, "triceps": 2},
        "C": {"legs": 5},
        "D": {"shoulders": 3, "abs": 2},
    }

    @staticmethod
    # realiza a estrutura de do treino atráves do Nivel recebido
    # caso seja iniciante e intermediário - ABC
    # caso seja avançado ABCD
    def estrutura_por_nivel(nivel: NivelAluno) -> list[str]:
        if nivel in (NivelAluno.INICIANTE, NivelAluno.INTERMEDIARO):
            return ["A", "B", "C"]
        return ["A", "B", "C", "D"]

    @staticmethod
    # realiza a busca de exercicios no banco
    # faz fallback caso os exercicios sejam insuficientes
    # faz a randomização dos exercicios
    # garante que não venha a quantidade incorreta de exercicios
    def _buscar_exercicios(
        musculo: str,
        nivel: NivelAluno,
        quantidade: int,
    ) -> list[Exercicio]:

        exercicios = list(
            Exercicio.objects.filter(
                target=musculo,
                difficulty__lte=nivel.value,
            )[:quantidade]
        )

        if len(exercicios) < quantidade:
            ExercicioService.buscar_por_musculo(musculo)

            exercicios = list(
                Exercicio.objects.filter(
                    target=musculo,
                    difficulty__lte=nivel.value,
                )[:quantidade]
            )

        random.shuffle(exercicios)
        selecionados = exercicios[:quantidade]

        if len(selecionados) < quantidade:
            raise ValidationError(
                _(f"Exercícios insuficientes para o musculo {musculo}")
            )
        return selecionados

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
    def _validar_exercicio_payload(exercicio: Exercicio):
        campos = {"id", "repeticoes", "series"}
        faltando = campos - exercicio.keys()

        if faltando:
            raise ValidationError(
                _("Campos obrigatórios ausentes: %(campos)s")
                % {"campos": ", ".join(sorted(faltando))}
            )

    @staticmethod
    # adiciona um exercicio em um treino
    # traduz dificuldade da API para intEnum
    # valida se o exercicio é adequado ao aluno
    # não duplica exercicios
    def adicionar_exercicio(
        treino: Treino,
        exercicio: Exercicio,
        dia: str,
        ordem: int,
    ):

        aluno = treino.aluno

        nivel_exercicio = ExercicioService.traduzir_dificuldade_api(
            exercicio.difficulty
        )

        AlunoService.validar_exercicio_para_aluno(
            aluno=aluno, exercicio=nivel_exercicio
        )

        treino_exercicio, _ = TreinoExercicio.objects.update_or_create(
            treino=treino,
            exercicio=exercicio,
            dia=dia,
            defaults={
                # defaults - objetos que podem ser mudados após uma request
                "ordem": ordem,
            },
        )

        return treino_exercicio

    @staticmethod
    # realiza a montagem do treino
    # valida nível e dias validos de acordo com a estrutura
    # valida se aluno possui treino ativo
    # define 1 exercicio com base em cada dia na estrutura muscular
    # para cada músculo na estrutura muscular é buscado um exercicio
    # e cada exercicio retornado é salvo no treino
    def montar_treino(aluno: Aluno) -> Treino:
        nivel = AlunoService.definir_level(aluno)
        dias_validos = TreinoService.estrutura_por_nivel(nivel)

        with transaction.atomic():
            treino = TreinoService.criar_treino(aluno)

            for dia in dias_validos:
                if dia not in TreinoService.ESTRUTURA_MUSCULAR:
                    raise ValidationError(
                        _(f"Estrutura muscular não definida para o dia {dia}")
                    )

                ordem = 1
                musculos = TreinoService.ESTRUTURA_MUSCULAR[dia]

                for musculo, quantidade in musculos.items():

                    exercicios = TreinoService._buscar_exercicios(
                        musculo=musculo,
                        nivel=nivel,
                        quantidade=quantidade,
                    )

                    for exercicio in exercicios:
                        TreinoService.adicionar_exercicio(
                            treino=treino,
                            exercicio=exercicio,
                            dia=dia,
                            ordem=ordem,
                        )
                        ordem += 1

        return treino
