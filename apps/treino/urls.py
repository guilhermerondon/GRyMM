from django.urls import path

from apps.treino.views import TreinoViewSet

treino_list = TreinoViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

treino_detail = TreinoViewSet.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns = [
    path("alunos/<int:aluno_id>/treinos/", treino_list, name="treinos-por-aluno"),
    path("treinos/<int:pk>/", treino_detail, name="treino_detail"),
]
