import pandas as pd

# Inicializar listas para armazenar os dados
grupos = []
programas = []
nomes_programas = []

default_direct = r'C:\users\erica.araujo\onedrive - 200dev\documentos\pythonprojects\General'

# Abrir o arquivo de texto
with open(default_direct+'\ser004b.txt', 'r', encoding='latin-1') as file:
    grupo_atual = None
    for line in file:
        line = line.strip()

        # Desconsiderar linhas irrelevantes
        if ("DATASUL" in line or "Página:" in line or not line):
            continue

        # Identificar linhas de grupo de usuários
        if line.startswith("Grupo Usuários:"):
            grupo_atual = line.split(":")[1].strip()
            print(f"Lendo agora o grupo de usuários: {grupo_atual}")

        # Identificar linhas de programas
        elif line and not line.startswith("Programa"):
            partes = line.split()
            
            if len(partes) > 1:
                programa = partes[0]
                nome_programa = " ".join(partes[1:])
                grupos.append(grupo_atual)
                programas.append(programa)
                nomes_programas.append(nome_programa)

# Criar um DataFrame com os dados
df = pd.DataFrame({
    'Grupo de Usuários': grupos,
    'Programa': programas,
    'Nome do Programa': nomes_programas
})

# Exportar para um arquivo Excel
output_path = default_direct + '\programas.xlsx'
df.to_excel('output_path', index=False)

print("Arquivo Excel gerado com sucesso!")