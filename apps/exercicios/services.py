import logging

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.aluno.core.enum import NivelAluno
from apps.exercicios.models import Exercicio

logger = logging.getLogger(__name__)


class ExercicioService:

    # regra de MAP de API externa para definir level int

    API_DIFICULDADE_MAP = {
        "beginner": NivelAluno.INICIANTE,
        "intermediate": NivelAluno.INTERMEDIARO,
        "advanced": NivelAluno.EXPERIENTE,
    }

    # regra de MAP com base o TargetList do ExerciseDb

    API_TARGET_MAP = {
        # domínio -> ExerciseDB
        "chest": "pectorals",
        "back": "upper back",
        "legs": "quads",
        "shoulders": "delts",
        "abs": "abs",
        "biceps": "biceps",
        "triceps": "triceps",
    }

    API_TARGET_MAP_TRANSLATOR = {
        # Peito
        "pectorals": "chest",
        # Costas
        "upper back": "back",
        "lats": "back",
        "spine": "back",
        # Ombros
        "delts": "shoulders",
        # Pernas
        "quads": "legs",
        "hamstrings": "legs",
        "glutes": "legs",
        "calves": "legs",
        # Braços
        "biceps": "biceps",
        "triceps": "triceps",
        "forearms": "forearms",
        # Abdômen
        "abs": "abs",
    }

    # monta variáveis de base que serão feita as requisições a API externa

    BASE_URL = "https://exercisedb.p.rapidapi.com"

    HEADERS = {
        "x-rapidapi-key": settings.EXERCISE_DB_API_KEY,
        "x-rapidapi-host": "exercisedb.p.rapidapi.com",
    }

    @staticmethod
    # realiza a busca por musculos
    # cria api_target responsável por mapear dados
    # da API exeterna com estrtura por nível
    # faz um request a API externa - endpoint de listar por músuculos
    # retorna uma mensagem amigável caso dê erro
    # valida se nenhum dos exercicios já são existentes no DB
    # usa o append para adicionar o exercicio e retornar
    def buscar_por_musculo(musculo: str) -> list[Exercicio]:

        api_target = ExercicioService.API_TARGET_MAP.get(musculo)

        url = f"{ExercicioService.BASE_URL}/exercises/target/{api_target}"

        response = requests.get(url, headers=ExercicioService.HEADERS, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro ao buscar exercícios na ExerciseDB ({response.status_code})"
            )

        exercicios_api = response.json()

        exercicio_salvos = []

        for exercicio_data in exercicios_api:
            exercicio = ExercicioService._salvar_ou_atualizar_exercicio(exercicio_data)
            exercicio_salvos.append(exercicio)

        return exercicio_salvos

    @staticmethod
    # realiza a ação de alterar ou salvar exericio
    # sempre mantém o id da API Externa como base
    # impede duplicidade de exercicios
    # defaults - serão os únicos dados que podem ser alterados
    def _salvar_ou_atualizar_exercicio(data: dict) -> Exercicio:

        logger.warning(
            "Exercise API payload | id=%s | target=%s | keys=%s",
            data.get("id"),
            data.get("target"),
            list(data.keys()),
        )

        target_traduzido = ExercicioService.traduzir_target_api(data.get("target"))

        nivel = ExercicioService.traduzir_dificuldade_api(data.get("difficulty"))

        exercicio, _ = Exercicio.objects.update_or_create(
            external_id=data["id"],
            defaults={
                "name": data["name"],
                "target": target_traduzido,
                "secondary_muscles": data.get("secondaryMuscles", []),
                "body_part": data.get("bodyPart"),
                "equipment": data.get("equipment"),
                "category": data.get("category"),
                "difficulty": nivel.value,
                "instructions": data.get("instructions", []),
                "description": data.get("description", ""),
                "gif_url": data.get("gifUrl", ""),
            },
        )
        return exercicio

    @staticmethod
    # passa dificuldade como str
    # valida se há o campo difficulty
    # valida se o dado já está tratado no banco
    # pega o que veio inserido no campo e passa a API MAP
    # retorna NivelAluno de acordo com o que foi passado no MAP
    def traduzir_dificuldade_api(difficulty: str) -> NivelAluno:
        if not difficulty:
            raise (ValueError)(_("Exercicio sem dificuldade"))

        if isinstance(difficulty, int):
            return NivelAluno(difficulty)

        if not isinstance(difficulty, str):
            raise ValueError(_(f"Dificuldade inválida: {difficulty}"))

        nivel = ExercicioService.API_DIFICULDADE_MAP.get(difficulty.lower())

        if nivel is None:
            raise ValueError(
                _(f"Dificuldade inválida recebida da API Externa: {nivel}")
            )

        return nivel

    @staticmethod
    # traduz target que vem da API externa para
    # passar na função de montar treino
    def traduzir_target_api(target: str) -> str:

        target_normalizado = target.lower().strip()

        traducao = ExercicioService.API_TARGET_MAP_TRANSLATOR.get(target_normalizado)

        if traducao is None:
            raise ValueError(
                f"Target inválido recebido da API externa {target_normalizado}"
            )

        return traducao

    @staticmethod
    def importar_exercicios(api_data: list):
        exercicios = []

        for i, item in enumerate(api_data):
            nivel = ExercicioService.traduzir_dificuldade_api(item["difficulty"])

            exercicio = Exercicio.objects.create(
                external_id=item["id"],
                name=item["name"],
                target=item["target"],
                difficulty=nivel.value,
                category=item["category"],
                body_part=item["bodyPart"],
                equipment=item["equipment"],
                instructions=item["instructions"],
                gif_url=item["gifUrl"],
            )

            exercicios.append(exercicio)

        return exercicios
