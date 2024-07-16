from django.db import models

# Create your models here.


class Cliente(models.Model):
    primeiro_nome = models.CharField(max_length=30)
    ultimo_nome = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=30)
    endereco = models.CharField(max_length=100)
    empresa = models.CharField(max_length=30)
    #campo para observacao
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"


class Lead(models.Model):
    NOVO = "Novo"
    CONTATADO = "Contatado"
    QUALIFICADO = "Qualificado"
    PERDIDO = "Perdido"

    escolha_status = {
        (NOVO, "Novo"),
        (CONTATADO, "Contatado"),
        (QUALIFICADO, "Qualificado"),
        (PERDIDO, "Perdido"),
    }
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # fonte, por exemplo: recomendacao, site, redes sociais
    fonte = models.CharField(max_length=30)
    status = models.CharField(choices=escolha_status, default=NOVO,max_length=30)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead para {self.cliente}"


class Interacao(models.Model):
    CHAMADA = 'Chamada'
    EMAIL = 'Email'
    REUNIAO = 'Reunião'
    OUTRO = 'Outro'

    TIPO_CHOICES = [
        (CHAMADA, 'Chamada'),
        (EMAIL, 'Email'),
        (REUNIAO, 'Reunião'),
        (OUTRO, 'Outro'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    data = models.DateTimeField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    resumo = models.TextField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} em {self.data} para {self.lead}"


class Oportunidade(models.Model):
    PROSPECCAO = 'Prospecção'
    PROPOSTA = 'Proposta'
    NEGOCIACAO = 'Negociação'
    FECHADO = 'Fechado'

    ESTAGIO_CHOICES = [
        (PROSPECCAO, 'Prospecção'),
        (PROPOSTA, 'Proposta'),
        (NEGOCIACAO, 'Negociação'),
        (FECHADO, 'Fechado'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estagio = models.CharField(max_length=20,
                               choices=ESTAGIO_CHOICES,
                               default=PROSPECCAO)
    data_fechamento_prevista = models.DateField()
    data_fechamento_real = models.DateField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Oportunidade para {self.lead} no valor de {self.valor}"


class Vendedor(models.Model):
    primeiro_nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    leads_atribuídos = models.ManyToManyField(Lead, blank=True)

    def __str__(self):
        return f"{self.primeiro_nome} {self.sobrenome}"


class Tarefa(models.Model):
    descricao = models.CharField(max_length=200)
    data_vencimento = models.DateField()
    concluida = models.BooleanField(default=False)
    atribuida_a = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    lead_relacionado = models.ForeignKey(Lead, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao
