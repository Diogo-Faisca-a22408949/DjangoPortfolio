from django.db import models

class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    apresentacao = models.TextField()
    logo = models.ImageField(upload_to='licenciaturas/', blank=True)

    def __str__(self):
        return self.nome

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='tecnologias/', blank=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    ects = models.IntegerField()
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE, related_name='ucs')

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='projetos/', blank=True)
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

    def __str__(self):
        return self.titulo

# Making Of OBRIGATÓRIO
class MakingOf(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='makingof/')

    def __str__(self):
        return self.titulo