import spacy
from collections import Counter
import json

try:
    NLP = spacy.load("pt_core_news_sm")
    STOP_WORDS_EXTRA = {"hoje", "pra", "ta",
                        "vou", "ser", "ter", "ir", "fazer", "dar"}
except OSError:
    print("ERRO: O modelo 'pt_core_news_sm' não foi encontrado. Execute o comando de download novamente.")
    NLP = None


def obter_sinonimos_sugeridos(palavra: str) -> str:
    """
    Função de Dicionário (Placeholder) para Sinônimos.
    Simula um léxico para fornecer sugestões relevantes de vocabulário.
    """
    # Dicionário robusto de sinônimos relevantes
    sinonimos = {
        'sustentabilidade': ['ecologia', 'preservação', 'conservação', 'perenidade'],
        'crucial': ['vital', 'essencial', 'chave', 'fundamental'],
        'futuro': ['porvir', 'destino', 'amanhã', 'prospecto'],
        # Nota: O lema é 'ação'
        'ação': ['medidas', 'iniciativas', 'providências', 'atitudes'],
        'requer': ['necessita', 'exige', 'demanda', 'pede'],
        'melhorar': ['aprimorar', 'otimizar', 'aperfeiçoar', 'elevar'],
        'sistema': ['estrutura', 'mecanismo', 'modelo', 'arcabouço']
    }

    sugestoes = sinonimos.get(palavra.lower(), [])

    if not sugestoes:
        return "N/A - Sugestões de vocabulário"

    return ", ".join(sugestoes[:3])


def analisar_texto(texto_entrada: str) -> list:
    """
    Processa o texto usando spaCy para lematização e contagem de frequência,
    filtrando palavras vazias (stop words).
    """
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


# --- Bloco de Teste ---
if __name__ == '__main__':
    texto_exemplo = "A sustentabilidade é crucial para o futuro. Sustentabilidade requer ações práticas hoje. Nós fazemos as ações para melhorar o sistema, pois ele é vital para o futuro."

    print("--- 📚 Teste do SYNSYS Core (analise.py) ---")
    print(f"Texto de Entrada: '{texto_exemplo}'\n")

    ranking = analisar_texto(texto_exemplo)

    tabela_saida = formatar_tabela(ranking)
    print(tabela_saida)

    print("\n--- Saída JSON (Para a API) ---")
    print(json.dumps(ranking, indent=4, ensure_ascii=False))
