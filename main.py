import csv

class Imovel:
    def __init__(self, tipo):
        self.tipo = tipo
        self.valor_base = 0.0
        self.adicionais = 0.0
        self.desconto = 0.0

    def calcular_total_aluguel(self):
        return (self.valor_base + self.adicionais) - self.desconto


class Apartamento(Imovel):
    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento")
        self.valor_base = 700.0  # Base: 1 Quarto
        
        # Regra c: Acréscimo de 2 quartos
        if quartos == 2:
            self.adicionais += 200.0
            
        # Regra e: Vaga de garagem
        if tem_garagem:
            self.adicionais += 300.0
            
        # Regra g: Desconto de 5% para quem não possui crianças
        if not tem_criancas:
            # O desconto se aplica sobre o valor total do aluguel acumulado até aqui
            self.desconto = (self.valor_base + self.adicionais) * 0.05


class Casa(Imovel):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa")
        self.valor_base = 900.0  # Base: 1 Quarto
        
        # Regra d: Acréscimo de 2 quartos
        if quartos == 2:
            self.adicionais += 250.0
            
        # Regra e: Vaga de garagem
        if tem_garagem:
            self.adicionais += 300.0


class Estudio(Imovel):
    def __init__(self, vagas):
        super().__init__("Estúdio")
        self.valor_base = 1200.0
        
        # Regra f: Vagas de estacionamento para estúdio
        if vagas == 2:
            self.adicionais += 250.0
        elif vagas > 2:
            # 250 pelas duas primeiras + 60 por vaga extra
            self.adicionais += 250.0 + ((vagas - 2) * 60.0)


class Orcamento:
    def __init__(self, imovel, parcelas_contrato):
        self.imovel = imovel
        self.valor_contrato_total = 2000.0
        self.parcelas_contrato = parcelas_contrato
        
    def exibir_resumo(self):
        aluguel_mensal = self.imovel.calcular_total_aluguel()
        valor_parcela_contrato = self.valor_contrato_total / self.parcelas_contrato
        
        print("\n" + "="*40)
        print("        ORÇAMENTO IMOBILIÁRIA R.M        ")
        print("="*40)
        print(f"Tipo de Imóvel: {self.imovel.tipo}")
        print(f"Valor do Aluguel Mensal: R$ {aluguel_mensal:.2f}")
        print(f"Taxa de Contrato: R$ {self.valor_contrato_total:.2f}")
        print(f"Parcelamento do Contrato: {self.parcelas_contrato}x de R$ {valor_parcela_contrato:.2f}")
        print("-"*40)
        print(f"Total no 1º Mês (Aluguel + Parcela): R$ {(aluguel_mensal + valor_parcela_contrato):.2f}")
        print("="*40)

    def gerar_csv(self):
        aluguel_mensal = self.imovel.calcular_total_aluguel()
        valor_parcela_contrato = self.valor_contrato_total / self.parcelas_contrato
        
        nome_arquivo = "orcamento_12_meses.csv"
        
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            # Cabeçalho do CSV
            escritor.writerow(["Mês", "Valor Aluguel (R$)", "Parcela Contrato (R$)", "Total Mensal (R$)"])
            
            # Gerando as 12 parcelas do orçamento (Regra i)
            for mes in range(1, 13):
                # O contrato só divide em até 5 vezes, depois o custo do contrato zera
                parcela_atual = valor_parcela_contrato if mes <= self.parcelas_contrato else 0.0
                total_mes = aluguel_mensal + parcela_atual
                
                escritor.writerow([f"Mês {mes}", f"{aluguel_mensal:.2f}", f"{parcela_atual:.2f}", f"{total_mes:.2f}"])
                
        print(f"\n[Sucesso] Arquivo '{nome_arquivo}' gerado com as 12 parcelas!")


# --- Fluxo Principal do Programa (Interface do Console) ---
def main():
    print("Bem-vindo ao Sistema de Orçamentos da Imobiliária R.M")
    print("Escolha o tipo de imóvel para locação:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    
    opcao = input("Digite a opção desejada (1-3): ")
    
    imovel_selecionado = None
    
    if opcao == "1":
        quartos = int(input("Quantidade de quartos (1 ou 2): "))
        garagem = input("Deseja vaga de garagem? (S/N): ").strip().upper() == "S"
        criancas = input("Possui crianças morando? (S/N): ").strip().upper() == "S"
        imovel_selecionado = Apartamento(quartos, garagem, criancas)
        
    elif opcao == "2":
        quartos = int(input("Quantidade de quartos (1 ou 2): "))
        garagem = input("Deseja vaga de garagem? (S/N): ").strip().upper() == "S"
        imovel_selecionado = Casa(quartos, garagem)
        
    elif opcao == "3":
        vagas = int(input("Digite a quantidade de vagas de estacionamento (0 para nenhuma): "))
        imovel_selecionado = Estudio(vagas)
    else:
        print("Opção inválida! Reinicie o programa.")
        return

    # Validação das parcelas da taxa de contrato (máximo 5 vezes - Regra b)
    print("\nA taxa de contrato padrão é de R$ 2.000,00.")
    parcelas = int(input("Em quantas vezes deseja parcelar a taxa de contrato (1 a 5)? "))
    while parcelas < 1 or parcelas > 5:
        print("Quantidade de parcelas inválida. Permitido apenas de 1 a 5 vezes.")
        parcelas = int(input("Digite novamente (1 a 5): "))

    # Criando o orçamento com base nas escolhas
    orcamento = Orcamento(imovel_selecionado, parcelas)
    orcamento.exibir_resumo()
    
    # Exportação para CSV (Regra i)
    exportar = input("\nDeseja exportar o orçamento de 12 meses para um arquivo .csv? (S/N): ").strip().upper()
    if exportar == "S":
        orcamento.gerar_csv()

if __name__ == "__main__":
    main()