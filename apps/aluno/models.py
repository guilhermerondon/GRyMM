from django.db import models
from django.utils.translation import gettext_lazy as _


class Aluno(models.Model):
    nome = models.CharField(
        max_length=100, verbose_name=_("Nome do Aluno")
    )  # campo nome

    idade = models.PositiveIntegerField(
        verbose_name=_("Idade"),
        help_text=_("Idade do Aluno em Anos"),
    )  # campo idade

    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Peso"),
        help_text=_("Peso do Aluno em Kg"),
    )  # campo peso

    tempo_pratica_meses = models.PositiveIntegerField(
        verbose_name=_("Tempo de prática"),
        help_text=_("Tempo de prática em meses"),
    )  # campo tempo pratica - meses
    # mais preciso e fácil de fazer as validações

    criado_em = models.DateTimeField(
        auto_now=True, verbose_name=_("Criado em")
    )  # campo criado em

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Atuaizado em"),
    )  # campo atualizado em

    class Meta:
        verbose_name = _("Aluno")
        verbose_name_plural = _("Alunos")
        ordering = ["nome"]
        # classe META - define nomes para query's
        # ordena a partir do nome

    def __str__(self) -> str:
        return self.nome
        # retorna nome - usado para depuração


# Create your models here.
