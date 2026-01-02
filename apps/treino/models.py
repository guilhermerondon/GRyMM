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

    # categorias/escolhas da API externa
    CATEGORIAS_API = [
        ("strength", "Strength"),
        ("cardio", "Cardio"),
        ("mobility", "Mobility"),
        ("balance", "Balance"),
        ("stretching", "Stretching"),
        ("plyometrics", "Plyometrics"),
        ("rehabilitation", "Rehabilitation"),
    ]

    treino = models.ForeignKey(
        "treino.Treino",
        on_delete=models.CASCADE,
        related_name="exercicios",
    )

    exercicio_id_externo = models.CharField(max_length=100)
    nome_exercicio = models.CharField(max_length=255)
    grupo_muscular = models.CharField(max_length=100)
    repeticoes = models.CharField(max_length=100, default=0)
    series = models.CharField(max_length=100, default=0)

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS_API,
    )

    dia = models.CharField(
        max_length=1,
        choices=[("A", "Dia A"), ("B", "Dia B"), ("C", "Dia C"), ("D", "Dia D")],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["treino", "dia", "exercicio_id_externo"],
                name="unique_exercicio_por_dia_no_treino",
            )
        ]
        indexes = [
            models.Index(fields=["treino", "dia"]),
            models.Index(fields=["categoria"]),
            models.Index(fields=["grupo_muscular"]),
        ]

    def __str__(self):
        return f"{self.nome_exercicio} ({self.categoria}) - Dia {self.dia}"
