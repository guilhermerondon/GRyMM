import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.aluno.core.enum import NivelAluno
from apps.exercicios.models import Exercicio


class ExercicioService:

    # regra de MAP de API externa para definir level int

    API_DIFICULDADE_MAP = {
        "beginner": NivelAluno.INICIANTE,
        "intermediate": NivelAluno.INTERMEDIARO,
        "expert": NivelAluno.EXPERIENTE,
    }

    # monta variáveis de base que serão feita as requisições a API externa

    BASE_URL = "https://exercisedb.p.rapidapi.com"

    HEADERS = {
        "x-rapidapi-key": settings.EXERCISE_DB_API_KEY,
        "x-rapidapi-host": "exercisedb.p.rapidapi.com",
    }

    @staticmethod
    # realiza a busca por musculos
    # faz um request a API externa - endpoint de listar por músuculos
    # retorna uma mensagem amigável caso dê erro
    # valida se nenhum dos exercicios já são existentes no DB
    # usa o append para adicionar o exercicio e retornar
    def buscar_por_musculo(musculo: str) -> list[Exercicio]:
        url = f"{ExercicioService.BASE_URL}/exercises/target/{musculo}"

        response = requests.get(url, headers=ExercicioService.HEADERS, timeout=10)

        if response.status_code != 200:
            raise RuntimeError("Erro ao buscar exercícios na ExerciseDB")

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
        exercicio, _ = Exercicio.objects.update_or_create(
            external_id=data["id"],
            defaults={
                "name": data["name"],
                "target": data["target"],
                "secondary_muscles": data.get("secondaryMuscles", []),
                "body_part": data.get("bodyPart"),
                "equipment": data.get("equipment"),
                "category": data.get("category"),
                "difficulty": data.get("difficulty"),
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
            raise ValueError(_("Dificuldade inválida recebida da API Externa"))

        return nivel

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
