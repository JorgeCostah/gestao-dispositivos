import sqlite3
import os

caminho_projeto = os.path.dirname(os.path.dirname(__file__))
caminho_db = os.path.join(caminho_projeto, 'database', 'gestao_dispositivos.db')

def listar_aparelhos():
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        
        cursor.execute("SELECT id, modelo, imei, numero_serie, status FROM aparelhos")
        aparelhos = cursor.fetchall()
        
        if not aparelhos:
            print("Nenhum aparelho cadastrado. ")
        else:
            print("--- Lista de Aparelhos Cadastrados ---")
            for a in aparelhos:
                print(f"ID: {a[0]} | Modelo: {a[1]} | IMEI: {a[2]} | N° de Série: {a[3]} | Status: {a[4]}")
                
        conexao.close()
    except Exception as e:
        print(f"Erro ao listar: {e}")

def cadastrar_aparelho():
    print("--- Cadastro de Novo Aparelho ---")
    #informações do user
    modelo = input("Modelo do aparelho: ")
    imei =  input("IMEI do aparelho: ")
    serie = input("Numero de série do aparelho: ")
    status = "Disponível"
    
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        
        sql = """
        INSERT INTO aparelhos (modelo, imei, numero_serie, status)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (modelo, imei, serie, status))
        conexao.commit()
        
        print(f"\n Sucesso: {modelo} cadastrado com ID {cursor.lastrowid}!")
        
    except sqlite3.IntegrityError:
        print("\n Erro: Este IMEI ou numero de Série já existe no sistema. ")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar aparelho: {e}")
    finally:
        conexao.close()
        
def registar_saida():
    print(" --- Registrar Saída de Aparelho --- ")
    
    id_aparelho = input("ID do aparelho a ser retirado: ")
    id_colaborador = input("ID do colaborador: ")
    tipo_movimentacao = input("Tipo de movimentação: ")
    obs =  input("Observações: ")
    itens =  input("Itens incluso: ")
    
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor =  conexao.cursor()
        sql_mov = """
        INSERT INTO movimentacoes (aparelho_id, colaborador_id, tipo_movimentacao, observacao_estado, itens_inclusos)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_mov, (id_aparelho, id_colaborador, tipo_movimentacao, obs, itens))
        
        sql_aparelho = "UPDATE aparelhos SET status = 'Em Uso' WHERE id = ?"
        cursor.execute(sql_aparelho, (id_aparelho,))
        
        conexao.commit()
        print("\n Saída registrada com sucesso! ")
        
    except Exception as e:
        print(f"Erro ao registrar saída: {e}")
    finally:
        conexao.close()
        
def registrar_devolucao():
    print("  === Registrar Devolução do Aparelho === ")
    
    id_aparelho = input("ID do aparelho Devolvido: ")
    obs_estado = input("Obervações sobre o estado do aparelho: ")
    itens = input("Itens devolvidos: ")
    
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor =  conexao.cursor()
        
        sql_mov = """
        INSERT INTO movimentacoes (aparelho_id, tipo_movimentacao, observacao_estado, itens_inclusos)
        VALUES (?, 'Devolução', ?, ?)
        """
        cursor.execute(sql_mov, (id_aparelho, obs_estado, itens))
        
        sql_aparelho = "UPDATE aparelhos SET status = 'Disponível' WHERE id = ?"
        cursor.execute(sql_aparelho, (id_aparelho,))
        
        conexao.commit()
        print(f"\n Devolução registrada com sucesso! O aparelho ID {id_aparelho} está Disponível. ")
        
    except Exception as e:
        print(f"Erro ao registrar devolução: {e}")
    finally:
        conexao.close()
        
def relatorio_cautelas():
    print("==== Relatório de Cautelas (Em uso)====")
    print("-" * 90)
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        
        sql = """
        SELECT
            a.modelo,
            ifnull(c.nome, 'NÃO IDENTIFICADO'),
            ifnull(m.data_movimentacaO, 'SEM REGISTRO'),
            ifnull(m.itens_inclusos, '-')
        FROM aparelhos a
        LEFT JOIN movimentacoes m ON a.id = m.aparelho_id
        LEFT JOIN colaboradores c ON m.colaborador_id = c.id
        WHERE a.status = 'Em Uso'
        ORDER BY m.data_movimentacaO DESC
        """
        
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhum aparelho está em uso no momento. ")
        else:
            print(f"{'APARELHO':<20} | {'COLABORADOR':<20} | {'DATA':<20} | {'ITENS INCLUSOS':<20}")
            print("-" * 90)
            for r in resultados:
                print(f"{r[0]:<20} | {r[1]:<20} | {r[2]:<20}")
            
        conexao.close()
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        
def historico_aparelho():
    print("==== Histórico de Movimentações ====")
    id_busca = input("Digite o ID do aparelho para consultar: ")
    
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        
        cursor.execute("SELECT modelo, numero_serie FROM aparelhos WHERE id = ?", (id_busca,))
        aparelho =  cursor.fetchone()
        
        if not aparelho:
            print("Aparelho não encontrado. ")
            return
        
        print(f"Historico do aparelho: {aparelho[0]} (N° de Série: {aparelho[1]})")
        print("-" * 60)
        
        sql = """
        SELECT
            m.data_movimentacaO,
            m.tipo_movimentacao,
            ifnull(c.nome, 'NÂO IDENTIFICADO') as colaborador,
            m.observacao_estado
        FROM movimentacoes m
        LEFT JOIN colaboradores c ON m.colaborador_id = c.id
        WHERE m.aparelho_id = ?
        ORDER BY m.data_movimentacaO DESC
        """
        
        cursor.execute(sql, (id_busca,))
        historico = cursor.fetchall()
        
        if not historico:
            print("Nenhuma movimentação registrada para este aparelho. ")
        else:
            for h in historico:
                data = h[0]
                tipo = h[1]
                colaborador = h[2]
                obs = h[3]
                print(f"[{data} | {tipo} | {colaborador} | {obs}]")
                
        conexao.close()
    except Exception as e:
        print(f"Erro ao consultar histórico: {e}")
        
def buscar_aparelho():
    print("==== Busca de Aparelho ====")
    termo = input("Digite o N° de Série/IMEI para buscar: ")
    
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        
        sql = """
        SELECT id, modelo, imei, numero_serie, status
        FROM aparelhos
        WHERE imei LIKE ? OR numero_serie LIKE ?
        """
        busca = f"%{termo}"
        
        cursor.execute(sql, (busca, busca))
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhum aparelho registrado com o dado fornecido. ")
        else:
            print(f"{'ID':<5} | {'MODELO':<20} | {'IMEI':<15} | {'N° DE SÉRIE':<15} | {'STATUS'}")
            print("-" * 70)
            for r in resultados:
                print(f"{r[0]:<4} | {r[1]:<15} | {r[2]:<15} |{r[3]:<15} |{r[4]}")
                
        conexao.close()
    except Exception as e:
        print(f"Erro ao buscar aparelho: {e}")
def main():
    while True:
        print("\n===== Sistema de Gestão de Dispositivos =====")
        print("1. Cadastrar novo aparelho")
        print("2. Listar aparelhos cadastrados")
        print("3. Registrar saída de aparelho")
        print("4. Registrar devolução de aparelho")
        print("5. Relatório de cautelas ativas")
        print("6. Histórico de um aparelho")
        print("7. Buscar aparelho por IMEI ou N° de Série")
        print("8. Sair")
        
        opcao =  input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_aparelho()
        elif opcao == "2":
            listar_aparelhos()
        elif opcao == "3":
            registar_saida()
        elif opcao == "4":
            registrar_devolucao()
        elif opcao == "5":
            relatorio_cautelas()
        elif opcao == "6":
            historico_aparelho()
        elif opcao == "7":
            buscar_aparelho()
        elif opcao == "8":
            print("Encerrando Sistema... Até logo!.....")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
if __name__ == "__main__":
    main()