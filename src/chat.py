from search import search_prompt

def main():
    print("Digite sua pergunta (ou 'sair' para encerrar):")
    while True:
        question = input("Pergunta: ").strip()
        if question.lower() in ("sair", "exit", "quit"):
            print("Encerrando chat.")
            break
        if not question:
            continue
        resposta = search_prompt(question)
        print(f"Assistente: {resposta}\n")

if __name__ == "__main__":
    main()