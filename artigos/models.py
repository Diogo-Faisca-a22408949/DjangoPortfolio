from django.db import models
from django.contrib.auth.models import User


class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artigos')

    class Meta:
        ordering = ['-data_criacao']
        verbose_name_plural = "Artigos"

    def __str__(self):
        return self.titulo

    def total_likes(self):
        return self.likes.count()

    def total_comentarios(self):
        return self.comentarios.count()


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artigo', 'usuario')
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.usuario.username} gostou de {self.artigo.titulo}"


class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.artigo.titulo}"
