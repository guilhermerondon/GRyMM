import pytest

from apps.aluno.models import Aluno
from apps.aluno.serializers import AlunoSerializer


@pytest.mark.django_db
class TestAlunoSerializer:
    # faz a criação de um aluno, passa pelo serializer
    # garante que o resultado esperado no serializer
    # bata com as informações do .data
    def test_serializer_retorna_nivel(self):
        aluno = Aluno.objects.create(
            nome="Aluno Ronnie",
            idade=54,
            peso=120,
            tempo_pratica_meses=48,
        )

        serializer = AlunoSerializer(aluno)
        data = serializer.data

        assert data["nome"] == "Aluno Ronnie"
        assert data["nivel"] == "Experiente"
