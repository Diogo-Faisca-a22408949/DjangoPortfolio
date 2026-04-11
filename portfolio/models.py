from django.db import models

class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    apresentacao = models.TextField()
    logo = models.ImageField(upload_to='licenciaturas/', blank=True)

    def __str__(self):
        return self.nome

class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    ects = models.IntegerField()
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True) # REQUISITO: Imagem na UC
    docente_nome = models.CharField(max_length=100, blank=True, null=True)
    docente_link_lusofona = models.URLField(blank=True, null=True) # REQUISITO: Link docente
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE, related_name='ucs')

    def __str__(self):
        return self.nome

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='tecnologias/', blank=True)
    descricao = models.TextField(blank=True)
    link_oficial = models.URLField(blank=True, null=True) # REQUISITO: Website oficial
    nivel_interesse = models.IntegerField(default=1, help_text="Escala de 1 a 5") # REQUISITO: Nível de interesse

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField(blank=True, null=True) # REQUISITO: Conceitos aplicados
    imagem = models.ImageField(upload_to='projetos/', blank=True)
    video_demo = models.URLField(blank=True, null=True) # REQUISITO: Video Demo
    github_link = models.URLField(blank=True, null=True) # REQUISITO: Link GitHub
    uc = models.ForeignKey(UnidadeCurricular, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True)

    def __str__(self):
        return self.titulo

class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.CharField(max_length=200)
    orientadores = models.CharField(max_length=200)
    curso = models.CharField(max_length=100)
    ano = models.IntegerField()
    resumo = models.TextField()
    link_pdf = models.URLField(blank=True, null=True)
    link_imagem = models.URLField(blank=True, null=True)
    areas = models.CharField(max_length=200, blank=True)
    destaque = models.BooleanField(default=False, help_text="Marcar para destacar na página principal") # REQUISITO: Forma de classificar/destacar

    def __str__(self):
        return self.titulo

class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    projetos_associados = models.ManyToManyField(Projeto, blank=True) # REQUISITO: Relação com outras entidades
    tecnologias_associadas = models.ManyToManyField(Tecnologia, blank=True)

    def __str__(self):
        return self.nome

class Formacao(models.Model):
    titulo = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    ano = models.IntegerField()
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ['-ano'] 

    def __str__(self):
        return self.titulo

class MakingOf(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    descricao_processo = models.TextField(help_text="Descrição de decisões e justificação de modelos")
    erros_encontrados = models.TextField(blank=True, help_text="Erros encontrados e respetivas correções")
    uso_ia = models.TextField(blank=True, help_text="Como a IA contribuiu (ou não) para o processo") 
    imagem_caderno = models.ImageField(upload_to='makingof/', blank=True, null=True, help_text="Registo em papel, DER, etc.")

    def __str__(self):
        return self.titulo