from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Artigo, Like, Comentario
from .forms import ArtigoForm, ComentarioForm


def _is_autor(user):
    """Verificar se o utilizador é membro do grupo 'autores'"""
    return user.is_authenticated and user.groups.filter(name='autores').exists()


# --- VISTAS DE LISTAGEM ---

def lista_artigos(request):
    """Listagem pública de todos os artigos"""
    artigos = Artigo.objects.all().order_by('-data_criacao')
    return render(request, 'artigos/lista_artigos.html', {
        'artigos': artigos,
        'is_autor': _is_autor(request.user),
    })


def detalhe_artigo(request, id):
    """Detalhe de um artigo com comentários e likes"""
    artigo = get_object_or_404(Artigo, id=id)
    comentarios = artigo.comentarios.all()
    usuario_gostou = False
    
    if request.user.is_authenticated:
        usuario_gostou = artigo.likes.filter(usuario=request.user).exists()
    
    # Formulário de comentário
    form_comentario = None
    if request.user.is_authenticated:
        form_comentario = ComentarioForm()
    
    context = {
        'artigo': artigo,
        'comentarios': comentarios,
        'usuario_gostou': usuario_gostou,
        'form_comentario': form_comentario,
        'is_autor': _is_autor(request.user),
        'pode_editar': request.user == artigo.autor,
    }
    return render(request, 'artigos/detalhe_artigo.html', context)


# --- CRUD DE ARTIGOS ---

@login_required
@user_passes_test(_is_autor)
def criar_artigo(request):
    """Criar novo artigo (apenas para autores)"""
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            messages.success(request, 'Artigo criado com sucesso!')
            return redirect('artigos:detalhe_artigo', id=artigo.id)
    else:
        form = ArtigoForm()
    
    return render(request, 'artigos/form_artigo.html', {
        'form': form,
        'titulo': 'Novo Artigo'
    })


@login_required
@user_passes_test(_is_autor)
def editar_artigo(request, id):
    """Editar artigo (apenas para o autor)"""
    artigo = get_object_or_404(Artigo, id=id)
    
    # Verificar se o utilizador é o autor
    if request.user != artigo.autor:
        messages.error(request, 'Apenas o autor pode editar este artigo.')
        return redirect('artigos:detalhe_artigo', id=artigo.id)
    
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artigo atualizado com sucesso!')
            return redirect('artigos:detalhe_artigo', id=artigo.id)
    else:
        form = ArtigoForm(instance=artigo)
    
    return render(request, 'artigos/form_artigo.html', {
        'form': form,
        'titulo': 'Editar Artigo'
    })


@login_required
@user_passes_test(_is_autor)
def deletar_artigo(request, id):
    """Deletar artigo (apenas para o autor)"""
    artigo = get_object_or_404(Artigo, id=id)
    
    # Verificar se o utilizador é o autor
    if request.user != artigo.autor:
        messages.error(request, 'Apenas o autor pode deletar este artigo.')
        return redirect('artigos:detalhe_artigo', id=artigo.id)
    
    if request.method == 'POST':
        titulo = artigo.titulo
        artigo.delete()
        messages.success(request, f'Artigo "{titulo}" foi deletado.')
        return redirect('artigos:lista_artigos')
    
    return render(request, 'artigos/confirmar_delete.html', {
        'artigo': artigo
    })


# --- LIKES ---

@login_required
@require_POST
def toggle_like(request, id):
    """Ativar/desativar like em um artigo"""
    artigo = get_object_or_404(Artigo, id=id)
    like, created = Like.objects.get_or_create(artigo=artigo, usuario=request.user)
    
    if not created:
        like.delete()
        gostou = False
    else:
        gostou = True
    
    # Se for AJAX, retornar JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'gostou': gostou,
            'total_likes': artigo.total_likes()
        })
    
    # Caso contrário, redirecionar
    return redirect('artigos:detalhe_artigo', id=artigo.id)


# --- COMENTÁRIOS ---

@login_required
@require_POST
def adicionar_comentario(request, id):
    """Adicionar comentário a um artigo"""
    artigo = get_object_or_404(Artigo, id=id)
    form = ComentarioForm(request.POST)
    
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        comentario.autor = request.user
        comentario.save()
        messages.success(request, 'Comentário adicionado com sucesso!')
    
    return redirect('artigos:detalhe_artigo', id=artigo.id)
