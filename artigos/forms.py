from django import forms
from .models import Artigo, Comentario


class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do artigo'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conteúdo do artigo',
                'rows': 10
            }),
            'fotografia': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'link_externo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com (opcional)'
            }),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva seu comentário...',
                'rows': 4
            }),
        }
