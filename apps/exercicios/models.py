from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.aluno.core.enum import NivelAluno


class Exercicio(models.Model):
    # cria parâmetros do exercicio que será recebido da API exeterna
    external_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("ID Externo"),
        help_text=_("ID do exercicio no ExerciseDB"),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Nome do Exercicio"),
    )

    target = models.CharField(
        max_length=100,
        verbose_name=_("Músculo Alvo"),
    )

    secondary_muscles = models.JSONField(
        default=list, verbose_name=_("Musculos Secundários")
    )

    body_part = models.CharField(max_length=100, verbose_name=_("Parte do corpo"))

    equipment = models.CharField(
        max_length=100,
        verbose_name=_("Equipamento"),
    )

    category = models.CharField(max_length=50, verbose_name=_("Categoria"))

    difficulty = models.IntegerField(
        choices=[(n.value, n.label) for n in NivelAluno],
        verbose_name=_("Nível do Exercício"),
    )

    instructions = models.JSONField(default=list, verbose_name=_("Instruções"))

    description = models.TextField(verbose_name=_("Descrição"))

    gif_url = models.URLField(verbose_name=_("Gif do Exercicio"))

    criado_em = models.DateTimeField(auto_now=True, verbose_name=_("Criado em"))

    atualizado_em = models.DateField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Exercício")
        verbose_name_plural = _("Exercícios")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


# Create your models here.
