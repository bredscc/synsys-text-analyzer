import spacy
from collections import Counter
import json
from nltk.corpus import wordnet as wn

try:
    NLP = spacy.load("pt_core_news_sm")
    STOP_WORDS_EXTRA = {"hoje", "pra", "ta", "vou", "ser",
                        "ter", "ir", "fazer", "dar", "querer", "poder"}
except OSError:
    print("ERRO: O modelo 'pt_core_news_sm' não foi encontrado.")
    NLP = None


def obter_sinonimos_sugeridos(palavra: str) -> str:
    """
    Tenta obter sinônimos via WordNet (Inteligência Semântica).
    Se não encontrar no WordNet (comum em PT), retorna ao dicionário estático (Fallback).
    """
    sinonimos_encontrados = set()
    for synset in wn.synsets(palavra, lang='por'):
        for lemma in synset.lemmas('por'):
            sinonimo = lemma.name().replace('_', ' ')
            if sinonimo.lower() != palavra.lower() and len(sinonimo) > 2:
                sinonimos_encontrados.add(sinonimo)

    sugestoes_dinamicas = list(sinonimos_encontrados)[:3]

    if sugestoes_dinamicas:
        return ", ".join(sugestoes_dinamicas)
    sinonimos_estaticos = {
        'sustentabilidade': ['ecologia', 'preservação', 'conservação', 'perenidade'],
        'crucial': ['vital', 'essencial', 'chave', 'fundamental'],
        'futuro': ['porvir', 'destino', 'amanhã', 'prospecto'],
        'ação': ['medidas', 'iniciativas', 'providências', 'atitudes'],
        'requer': ['necessita', 'exige', 'demanda', 'pede'],
        'sociedade': ['comunidade', 'coletividade', 'povo', 'nação'],
        'melhorar': ['aprimorar', 'otimizar', 'aperfeiçoar', 'elevar'],
        'sistema': ['estrutura', 'mecanismo', 'modelo', 'arcabouço'],
        'projeto': ['plano', 'empreendimento', 'esquema', 'desígnio']
    }

    sugestoes_estaticas = sinonimos_estaticos.get(palavra.lower(), [])

    if sugestoes_estaticas:
        return ", ".join(sugestoes_estaticas[:3])

    return "N/A - Sem sugestões no léxico."


def analisar_texto(texto_entrada: str) -> list:
    if not NLP:
        return []

    doc = NLP(texto_entrada)

    palavras_lematizadas = []

    for token in doc:
        is_valid = (
            not token.is_punct and
            not token.is_space and
            not token.is_stop and
            not token.like_num and
            token.is_alpha
        )

        if is_valid and token.lemma_.lower() not in STOP_WORDS_EXTRA:
            palavras_lematizadas.append(token.lemma_.lower())

    frequencias = Counter(palavras_lematizadas)
    palavras_repetidas = {palavra: freq for palavra,
                          freq in frequencias.items() if freq > 1}

    ranking = sorted(palavras_repetidas.items(),
                     key=lambda item: item[1], reverse=True)

    resultados = []
    for palavra, frequencia in ranking:
        resultados.append({
            'palavra': palavra.capitalize(),
            'frequencia': frequencia,
            'sinonimos': obter_sinonimos_sugeridos(palavra)
        })

    return resultados


def formatar_tabela(resultados: list) -> str:
    """Formata os resultados para exibição em console/Markdown."""

    if not resultados:
        return "\n| Palavra Original | Frequência | Sinônimos Sugeridos |\n| :--- | :--- | :--- |\n| Nenhuma palavra significativa repetida. | - | - |"

    tabela = "| Palavra Original | Frequência | Sinônimos Sugeridos |\n"
    tabela += "| :--- | :--- | :--- |\n"

    for item in resultados:
        tabela += f"| **{item['palavra']}** | {item['frequencia']} | {item['sinonimos']} |\n"

    return tabela


if __name__ == '__main__':
    texto_teste_semantico = "As grandes ações que a sociedade realiza são cruciais para um futuro melhor. A sociedade necessita de ações para garantir a sustentabilidade. Tais ações requerem decisões cruciais hoje para o futuro que queremos."

    print("--- 📚 Teste do SYNSYS Core (analise.py) com WordNet ---")
    print(f"Texto de Entrada: '{texto_teste_semantico}'\n")

    ranking = analisar_texto(texto_teste_semantico)
    tabela_saida = formatar_tabela(ranking)
    print(tabela_saida)

    print("\n--- Saída JSON (Para a API) ---")
    print(json.dumps(ranking, indent=4, ensure_ascii=False))
