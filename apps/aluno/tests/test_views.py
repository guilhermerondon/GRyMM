import pytest
from rest_framework.test import APIClient

from apps.aluno.models import Aluno


@pytest.mark.django_db
class TestAlunoViewSet:

    def setup_method(self):
        # cria api client capaz de simular requisições
        self.client = APIClient()

    def test_listar_alunos(self):
        # testa listagem de alunos
        # garante que retornou sucesso
        # garante que foi criado mais um len no .data
        Aluno.objects.create(
            nome="Aluno Guilherme", idade=24, peso=100, tempo_pratica_meses=12
        )

        response = self.client.get("/api/alunos/")

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_criar_aluno(self):
        # testa criação de aluno
        # garante que retornou created
        # garante que foi feito a criação de um objeto no bd
        # garante que nível foi passado na validação de service
        payload = {
            "nome": "Aluno Miguel",
            "idade": 21,
            "peso": 70,
            "tempo_pratica_meses": 8,
        }

        response = self.client.post("/api/alunos/", payload, format="json")

        assert response.status_code == 201
        assert Aluno.objects.count() == 1
        assert response.data["nivel"] == "Intermediário"
