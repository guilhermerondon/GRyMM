from django.db import models
from django.utils.translation import gettext_lazy as _


class Treino(models.Model):
    class Nivel(models.TextChoices):
        INICIANTE = "INICIANTE", _("Iniciante")
        INTERMEDIARO = "INTERMEDIARO", _("Intermediario")
        AVANCADO = "AVANCADO", _("Avancado")

    aluno = models.ForeignKey(
        "aluno.Aluno",
        on_delete=models.CASCADE,
        related_name="treinos",
    )

    nivel = models.CharField(
        max_length=14,
        choices=Nivel.choices,
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [
            models.UniqueConstraint(
                fields=["aluno"],
                condition=models.Q(ativo=True),
                name="unique_treino_ativo_por_aluno",
            )
        ]

    def __str__(self):
        return f"Treino {self.nivel} - {self.aluno.nome}"


class TreinoExercicio(models.Model):

    treino = models.ForeignKey(
        "treino.Treino",
        on_delete=models.CASCADE,
        related_name="exercicios",
    )

    exercicio_id = models.ForeignKey(
        "exercicios.Exercicio",
        on_delete=models.CASCADE,
        related_name="treinos",
    )

    dia = models.CharField(
        max_length=1,
        choices=[("A", "Dia A"), ("B", "Dia B"), ("C", "Dia C"), ("D", "Dia D")],
    )

    ordem = models.PositiveSmallIntegerField(verbose_name=_("Ordem no treino"))

    repeticoes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    series = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["treino", "dia", "exercicio_id"],
                name="unique_exercicio_por_dia_no_treino",
            )
        ]
        ordering = ["dia", "ordem"]

    def __str__(self):
        return f"{self.treino} - {self.dia} - {self.exercicio_id}"
