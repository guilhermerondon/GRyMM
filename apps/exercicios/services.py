import requests
from django.conf import settings

from apps.exercicios.models import Exercicio


class ExercicioService:
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

    def _salvar_ou_atualizar_exercicio(data: dict) -> Exercicio:
        # realiza a ação de alterar ou salvar exericio
        # sempre mantém o id da API Externa como base
        # impede duplicidade de exercicios
        # defaults - serão os únicos dados que podem ser alterados
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
