from django.shortcuts import render
from .models import Licenciatura, Competencia, Formacao, InteressePessoal, MakingOf, TFC

def cursos_view(request):
    # O segredo para as tecnologias dentro das UCs está aqui:
    licenciaturas = Licenciatura.objects.prefetch_related('ucs__projeto_set__tecnologias').all()
    return render(request, 'portfolio/cursos.html', {'licenciaturas': licenciaturas})

def pessoal_view(request):
    context = {
        'competencias': Competencia.objects.prefetch_related('tecnologias_associadas', 'projetos_associados').all(),
        'formacoes': Formacao.objects.all(),
        'interesses': InteressePessoal.objects.all(),
    }
    return render(request, 'portfolio/pessoal.html', context)

def makingof_view(request):
    makingofs = MakingOf.objects.all().order_by('-data') # Mais recentes primeiro
    return render(request, 'portfolio/makingof.html', {'makingofs': makingofs})

def tfcs_view(request):
    tfcs = TFC.objects.all().order_by('-ano')
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})