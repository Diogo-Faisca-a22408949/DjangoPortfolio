from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Adicionar utilizador automaticamente ao grupo 'autores'
            try:
                autores_group = Group.objects.get(name='autores')
                user.groups.add(autores_group)
            except Group.DoesNotExist:
                pass
        return user
