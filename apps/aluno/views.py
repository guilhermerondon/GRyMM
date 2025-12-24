from rest_framework import viewsets

from apps.aluno.models import Aluno
from apps.aluno.serializers import AlunoSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    # Crud completo Alunos

    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    # somente usuários autenticados podem
    # criar ou editar alunos


# Create your views here.
