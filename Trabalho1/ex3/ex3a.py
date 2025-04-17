import random

def gerar_fonte_fmp(alfabeto, fmp, N, nome_ficheiro):
    assert len(alfabeto) == len(fmp), "Alfabeto e FMP devem ter o mesmo tamanho"
    assert abs(sum(fmp) - 1.0) < 1e-6, "As probabilidades devem somar 1"

    simbolos = random.choices(alfabeto, weights=fmp, k=N)

    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        f.write("".join(simbolos))

    print(f"Ficheiro gerado: {nome_ficheiro}")


if __name__ == "__main__":

    alfabeto = ['A', 'B', 'C', 'D']

    fmp = [0.5, 0.25, 0.125, 0.125]

    N = 100
    
    gerar_fonte_fmp(alfabeto, fmp, N, "fonte_1.txt")
