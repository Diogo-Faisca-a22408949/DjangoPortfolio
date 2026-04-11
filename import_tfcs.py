import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from portfolio.models import TFC

def importar_tfcs():
    caminho = 'data/jsonTFC.json'
    if not os.path.exists(caminho):
        print("Ficheiro não encontrado.")
        return

    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        for item in dados:
            # Limpar o ano de forma segura
            try:
                ano_str = str(item.get('ano', '2025')).strip()
                ano = int(ano_str)
            except ValueError:
                ano = 2025

            # ---------------------------------------------------------
            # O SEGREDO ESTÁ AQUI: Lidar com nulls e listas em segurança
            # O "or []" garante que se vier um null/None, passa a ser 
            # uma lista vazia, evitando o erro do .join()
            # ---------------------------------------------------------
            autores_lista = item.get('autores') or []
            orientadores_lista = item.get('orientadores') or []
            
            # Vai buscar 'areas', mas se não existir, tenta 'palavras_chave'
            areas_lista = item.get('areas') or item.get('palavras_chave') or []

            # Converte tudo para string e junta com vírgulas
            autores = ", ".join([str(x).strip() for x in autores_lista])
            orientadores = ", ".join([str(x).strip() for x in orientadores_lista])
            areas = ", ".join([str(x).strip() for x in areas_lista])

            # Guarda na Base de Dados
            TFC.objects.get_or_create(
                titulo=item.get('titulo', 'Sem Título'),
                autores=autores,
                orientadores=orientadores,
                curso=item.get('curso', 'N/A'),
                ano=ano,
                resumo=item.get('resumo', ''),
                link_pdf=item.get('pdf', ''),
                link_imagem=item.get('imagem', ''),
                areas=areas
            )
            
    print("TFCs importados com sucesso à prova de bala!")

if __name__ == '__main__':
    importar_tfcs()