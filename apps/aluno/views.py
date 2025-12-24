from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.aluno.models import Aluno
from apps.aluno.serializers import AlunoSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    # Crud completo Alunos

    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    # somente usuários autenticados podem
    # criar ou editar alunos

    def create(self, request, *args, **kwargs):
        # tratamento de erro ao acontecer um POST
        serializer = self.get_serializer(data=request.data)

        # valida se o serializer está incorreto - 400
        # retorna mensagem amigável informando criação de aluno - 200
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Erro ao criar aluno",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_create(serializer)

        return Response(
            {
                "message": "Aluno criado com sucesso",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        # tratamento de erro ao acontencer um PUT ou PATCH
        # busca objeto no banco com base no id da URL
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # pega aluno existente, atualiza os dados enviadas
        # respeita se a mudança é parcial ou não
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        # valida se o serializer está incorreto - 400
        # retorna mensagem amigável informando atualização de aluno - 200
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Erro ao atualizar aluno",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_update(serializer)

        return Response(
            {"message": "Aluno atualizado com sucesso", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        # tratamento de erro ao acontencer um DELETE
        # busca objeto pelo id passado na URL
        instance = self.get_object()
        self.perform_destroy(instance)

        # retorna mensagem amigável informando exclusão de aluno - 204
        return Response(
            {"message": "Aluno removido com sucesso"},
            status=status.HTTP_204_NO_CONTENT,
        )
