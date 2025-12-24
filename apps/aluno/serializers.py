from rest_framework import serializers

from apps.aluno.models import Aluno
from apps.aluno.services import AlunoService


class AlunoSerializer(serializers.ModelSerializer):
    nivel = serializers.SerializerMethodField()
    # usado para campos calculados

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "idade",
            "peso",
            "tempo_pratica_meses",
            "nivel",
            "criado_em",
            "atualizado_em",
        ]
        # campos que não podem ser alterados
        read_only_fields = [
            "id",
            "nivel",
            "criado_em",
            "atualizado_em",
        ]

    def get_nivel(self, aluno: Aluno) -> str:
        # retorna o nível do aluno de forma legível

        nivel = AlunoService.definir_level(aluno)
        return nivel.label
