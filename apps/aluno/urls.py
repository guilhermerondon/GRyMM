from rest_framework.routers import DefaultRouter

from apps.aluno.views import AlunoViewSet

router = DefaultRouter()
router.register(r"alunos", AlunoViewSet, basename="aluno")

urlpatterns = router.urls
