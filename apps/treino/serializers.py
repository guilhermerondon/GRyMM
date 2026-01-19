from rest_framework import serializers

from .models import Treino, TreinoExercicio
from apps.exercicios.services import ExercicioService


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

    exercicio = serializers.SerializerMethodField()

    class Meta:
        model = TreinoExercicio
        fields = [
            "treino",
            "exercicio_id",
            "dia",
            "ordem",
            "repeticoes",
            "series",
            "exercicio",
        ]
    
    def get_exercicio(self, obj):

        exercicio_data = obj.exercicio_id
        
        if not exercicio_data:
            return None
        
        return{
            "external_id": exercicio_data.external_id,
            "name": exercicio_data.name,
            "target": exercicio_data.target,
            "difficulty": exercicio_data.difficulty,
            "category": exercicio_data.category,
            "body_part": exercicio_data.body_part,
            "equipment": exercicio_data.equipment,
            "instructions": exercicio_data.instructions,
        }


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
