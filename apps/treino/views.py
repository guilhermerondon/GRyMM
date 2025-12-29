from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.aluno.models import Aluno

from .models import Treino
from .serializers import TreinoCreateSerializer, TreinoSerializer


class TreinoViewSet(viewsets.ViewSet):
    """
    Gerenciamento de treinos vinculados a alunos
    """

    def list(self, request, aluno_id=None):
        # valida se exite um id de aluno atrelado a requiisição
        aluno = get_object_or_404(Aluno, id=aluno_id)

        treinos = aluno.treinos.prefetch_related("exercicios").order_by("-criado_em")

        serializer = TreinoSerializer(treinos, many=True)

        return Response(
            {
                "message": "Treinos listados com sucesso",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        # valida se exite um id de aluno atrelado a requiisição
        treino = get_object_or_404(
            Treino.objects.prefetch_related("exercicios"),
            id=pk,
        )

        serializer = TreinoSerializer(treino)

        return Response(
            {
                "message": "Treino encontrado",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request, aluno_id=None):
        # valida se exite um id de aluno atrelado a requisição
        # chama o TreinoSerializer para validação de payload
        # se for válido, faz a criação 
        aluno = get_object_or_404(Aluno, id=aluno_id)

        serializer = TreinoCreateSerializer(
            data=request.data,
            context={"aluno": aluno},
        )

        serializer.is_valid(raise_exception=True)
        treino = serializer.save()

        return Response(
            {
                "message": "Treino criado com sucesso",
                "data": TreinoSerializer(treino).data,
            },
            status=status.HTTP_201_CREATED,
        )
