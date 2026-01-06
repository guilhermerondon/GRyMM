from rest_framework import serializers

from .models import Treino, TreinoExercicio


class TreinoCreateSerializer(serializers.ModelSerializer):
    # passa dados esperados ao chamar este serializer
    class Meta:
        model = Treino
        fields = [
            "aluno",
            "nivel",
            "ativo",
        ]


class TreinoExercicioSerializer(serializers.ModelSerializer):
    # passa dados esperados ao chamar este serializer
    class Meta:
        model = TreinoExercicio
        fields = [
            "treino",
            "exercicio",
            "dia",
            "ordem",
            "repeticoes",
            "series",
        ]


class TreinoSerializer(serializers.ModelSerializer):
    # passa dados esperados ao chamar este serializer
    exercicios = TreinoExercicioSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Treino
        fields = [
            "id",
            "nivel",
            "ativo",
            "criado_em",
            "exercicios",
        ]
