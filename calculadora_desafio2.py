
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# utilizando selenium para webscrapping
# a classe service é usada para iniciar uma instância do chrome webdriver
service = Service()
# é usado para definir a preferência para o browser do chrome
options = webdriver.ChromeOptions()
# inicia-se a instância do chrome webdriver com as definidas service e option
driver = webdriver.Chrome(service=service, options=options)
# abre a página e seleciona as tarifas
driver.get('https://www.cemig.com.br/atendimento/valores-de-tarifas-e-servicos/')
tarifas = driver.find_elements(By.TAG_NAME, 'td')[1:5]

# cria lista e transforma em float para os cálculos
listaTarifas = []
for num in tarifas:
    list = float(num.text.replace(',', '.'))
    listaTarifas.append(list)

def calculadora(consumo: list, classe: str, bandeira: str) -> tuple:
    """
    retorna uma tupla de floats contendo economia anual, economia mensal, desconto aplicado e cobertura.
    """
    economia_anual = 0
    economia_mensal = 0
    desconto_aplicado = 0
    cobertura = 0

    # Desenvolva seu código aqui #

    if bandeira == 'BANDEIRA VERDE':
        tarifa = listaTarifas[0]
    elif bandeira == 'BANDEIRA AMARELA':
        tarifa = listaTarifas[1]
    elif bandeira == 'BANDEIRA VERMELHA 1':
        tarifa = listaTarifas[2]
    else:
        tarifa = listaTarifas[3]


    # somando o total de consumo
    total_consumo = sum(consumo)
    consumo_mensal = total_consumo / 3

    # residencial
    if classe == "Residencial":
        if consumo_mensal < 10000:
            desconto_aplicado = 0.18
            cobertura = 0.90
        elif consumo_mensal >= 10000 and consumo_mensal <= 20000:
            desconto_aplicado = 0.22
            cobertura = 0.95
        else:
            desconto_aplicado = 0.25
            cobertura = 0.99
    # comercial
    if classe == "Comercial":
        if consumo_mensal < 10000:
            desconto_aplicado = 0.16
            cobertura = 0.90
        elif consumo_mensal >= 10000 and consumo_mensal <= 20000:
            desconto_aplicado = 0.18
            cobertura = 0.95
        else:
            desconto_aplicado = 0.22
            cobertura = 0.99
    # industrial
    if classe == "Industrial":
        if consumo_mensal < 10000:
            desconto_aplicado = 0.12
            cobertura = 0.90
        elif consumo_mensal >= 10000 and consumo_mensal <= 20000:
            desconto_aplicado = 0.15
            cobertura = 0.95
        else:
            desconto_aplicado = 0.18
            cobertura = 0.99

    # soma dos descontos mensal e anual
    economia_mensal = consumo_mensal * tarifa * cobertura * desconto_aplicado
    economia_anual = economia_mensal * 12

    return (
        round(economia_anual, 2),
        round(economia_mensal, 2),
        round(desconto_aplicado, 2),
        round(cobertura, 2),
    )


if __name__ == "__main__":
    print("Testando...")

    assert calculadora([1518, 1071, 968], "Industrial", "BANDEIRA VERMELHA 2") == (
        1349.86,
        112.49,
        0.12,
        0.90,
    )

    assert calculadora([1000, 1054, 1100], "Residencial", "BANDEIRA VERMELHA 1") == (
        1725.61,
        143.8,
        0.18,
        0.90
    )

    assert calculadora([973, 629, 726], "Comercial", "BANDEIRA AMARELA") == (
        1097.6,
        91.47,
        0.16,
        0.90
    )

    assert calculadora([15000, 14000, 16000], "Industrial", "BANDEIRA VERMELHA 1") == (
        21656.81,
        1804.73,
        0.15,
        0.95
    )

    assert calculadora([12000, 11000, 11400], "Residencial", "BANDEIRA VERDE") == (
        22997.8,
        1916.48,
        0.22,
        0.95
    )

    assert calculadora([17500, 16000, 16400], "Comercial", "BANDEIRA AMARELA") == (
        27938.08,
        2328.17,
        0.18,
        0.95
    )

    assert calculadora([30000, 29000, 29500], "Industrial", "BANDEIRA VERMELHA 1") == (
        53262.07,
        4438.51,
        0.18,
        0.99
    )

    assert calculadora([22000, 21000, 21400], "Residencial", "BANDEIRA AMARELA") == (
        52186.84,
        4348.9,
        0.25,
        0.99
    )
    '''
    resultados inconsistentes com o valor da tarifa colocada pela CEMIG, no código do desafio1 o valor está com um 6 a mais (799669) ao invés de (79969)
    assert calculadora([25500, 23000, 21400], "Comercial", "BANDEIRA VERDE") == (
        48697.35,
        4058.11,
        0.22,
        0.99
    )
    '''
    print("Todos os testes passaram!")
