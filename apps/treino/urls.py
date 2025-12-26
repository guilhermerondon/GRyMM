# apps/treino/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreinoViewSet

router = DefaultRouter()
router.register(r'treinos', TreinoViewSet, basename='treinos')

urlpatterns = [
    path('alunos/<int:aluno_id>/', include(router.urls)),
]
