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

        assert response.data["data"]["nivel"] == "Intermediário"
        assert response.data["message"] == "Aluno criado com sucesso"

    def test_patch_aluno_atualiza_apenas_um_campo(self):
        aluno = Aluno.objects.create(
            nome="Aluno Mitsuo",
            idade=24,
            peso=70,
            tempo_pratica_meses=3,
        )

        payload = {"peso": 75}

        response = self.client.patch(f"/api/alunos/{aluno.id}/", payload, format="json")

        assert response.status_code == 200
        assert response.data["data"]["peso"] == "75.00"
        assert response.data["data"]["nome"] == "Aluno Mitsuo"

    def test_put_aluno_atualiza_todos_os_campos(self):
        aluno = Aluno.objects.create(
            nome="Aluno Pierre", idade=20, peso=94, tempo_pratica_meses=27
        )

        payload = {
            "nome": "Aluno Charles",
            "idade": 21,
            "peso": 98,
            "tempo_pratica_meses": 28,
        }

        response = self.client.put(
            f"/api/alunos/{aluno.id}/",
            payload,
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["nome"] == "Aluno Charles"
        assert response.data["data"]["nivel"] == "Experiente"

    def test_delete_aluno(self):
        aluno = Aluno.objects.create(
            nome="Aluno Lunardi", idade=24, peso=100, tempo_pratica_meses=1
        )

        response = self.client.delete(
            f"/api/alunos/{aluno.id}/",
        )

        assert response.status_code == 204
        assert Aluno.objects.count() == 0
