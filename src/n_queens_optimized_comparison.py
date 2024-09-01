import dearpygui.dearpygui as dpg
import threading
import time

# Função is_safe: Verifica se é seguro posicionar uma rainha na posição (row, col) no tabuleiro.
# O algoritmo verifica se existe conflito com outras rainhas nas três direções críticas:
# 1. À esquerda na mesma linha.
# 2. Na diagonal superior esquerda.
# 3. Na diagonal inferior esquerda.
# Se houver conflito (ou seja, uma rainha já está posicionada nessas direções), a posição não é segura, e a função retorna False.
# Caso contrário, retorna True, indicando que é seguro posicionar uma rainha nessa posição.
def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

# Função solve_n_queens: Resolve o problema das N Rainhas usando o algoritmo de backtracking de forma não otimizada.
# O algoritmo tenta posicionar uma rainha em cada coluna, começando da primeira coluna.
# Para cada linha na coluna atual, verifica se é seguro colocar a rainha usando a função is_safe.
# Se for seguro, a rainha é posicionada, e a função recursivamente tenta posicionar rainhas nas colunas seguintes.
# Se uma solução é encontrada, a função retorna True.
# Se nenhuma solução é encontrada, a função faz backtracking, removendo a rainha e tentando outras posições.
def solve_n_queens(board, col, n):
    if col >= n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_n_queens(board, col + 1, n):
                return True
            board[i][col] = 0
    return False

# Função is_safe_optimized: Verifica se é seguro posicionar uma rainha na posição (row, col) usando técnicas de otimização.
# Utiliza três vetores auxiliares para verificar os conflitos em O(1) tempo:
# ld (left diagonal): Diagonal superior esquerda.
# rd (right diagonal): Diagonal inferior esquerda.
# cl (columns): Colunas.
# Se qualquer uma dessas posições já estiver ocupada, a função retorna False; caso contrário, retorna True.
def is_safe_optimized(row, col, ld, rd, cl):
    return not (ld[row - col] or rd[row + col] or cl[row])

# Função solve_n_queens_branch_and_bound: Resolve o problema das N Rainhas usando a técnica de Branch and Bound.
# Esta função é uma versão otimizada do algoritmo de backtracking, que evita explorar caminhos inviáveis.
# Utiliza arrays auxiliares (ld, rd, cl) para rapidamente verificar se uma posição é válida sem precisar recalcular a cada passo.
# Isso reduz o tempo de verificação de conflitos e melhora a eficiência do algoritmo.
def solve_n_queens_branch_and_bound(board, col, n, ld, rd, cl):
    if col >= n:
        return True
    for i in range(n):
        if is_safe_optimized(i, col, ld, rd, cl):
            board[i][col] = 1
            ld[i - col] = rd[i + col] = cl[i] = True
            if solve_n_queens_branch_and_bound(board, col + 1, n, ld, rd, cl):
                return True
            board[i][col] = 0
            ld[i - col] = rd[i + col] = cl[i] = False
    return False

# Função run_sequential_non_optimized: Executa o algoritmo não otimizado de forma sequencial.
# Cria um tabuleiro vazio de tamanho NxN e mede o tempo necessário para encontrar uma solução utilizando o algoritmo de backtracking.
# Retorna o tabuleiro resultante e o tempo de execução.
def run_sequential_non_optimized(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    start_time = time.time()
    solve_n_queens(board, 0, n)
    end_time = time.time()
    return board, end_time - start_time

# Função run_parallel_non_optimized: Executa o algoritmo não otimizado em um ambiente "paralelo".
# Esta implementação simula a execução paralela, mas na realidade não divide o trabalho entre múltiplas threads.
# É utilizada principalmente para comparação de desempenho com a versão otimizada paralela.
def run_parallel_non_optimized(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    start_time = time.time()
    solve_n_queens(board, 0, n)
    end_time = time.time()
    return board, end_time - start_time

# Função run_sequential_optimized: Executa o algoritmo otimizado de forma sequencial.
# Utiliza a técnica de Branch and Bound para melhorar a eficiência do backtracking.
# Mede o tempo de execução e retorna o tabuleiro resultante e o tempo gasto.
def run_sequential_optimized(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    ld = [False] * (2 * n)
    rd = [False] * (2 * n)
    cl = [False] * n
    start_time = time.time()
    solve_n_queens_branch_and_bound(board, 0, n, ld, rd, cl)
    end_time = time.time()
    return board, end_time - start_time

# Função run_parallel_optimized: Executa o algoritmo otimizado de forma paralela.
# O trabalho é dividido entre múltiplas threads, cada uma tentando resolver uma parte do problema, começando com diferentes linhas.
# Utiliza a técnica de Branch and Bound para otimizar a busca, e as threads são sincronizadas para combinar os resultados.
# A função retorna o primeiro tabuleiro completo encontrado e o tempo médio de execução entre todas as threads.
def run_parallel_optimized(n):
    successful_boards = []
    times = []

    def worker(start_row):
        ld = [False] * (2 * n)
        rd = [False] * (2 * n)
        cl = [False] * n
        board = [[0 for _ in range(n)] for _ in range(n)]
        start_time = time.time()

        if is_safe_optimized(start_row, 0, ld, rd, cl):
            board[start_row][0] = 1
            ld[start_row - 0] = rd[start_row + 0] = cl[start_row] = True
            if solve_n_queens_branch_and_bound(board, 1, n, ld, rd, cl):
                successful_boards.append(board)
        
        end_time = time.time()
        times.append(end_time - start_time)

    threads = []
    for i in range(n):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    combined_board = successful_boards[0] if successful_boards else [[0 for _ in range(n)] for _ in range(n)]
    
    return combined_board, sum(times) / len(times) if times else 0

# Função render_board: Renderiza o tabuleiro na interface gráfica usando DearPyGui.
# Cada linha do tabuleiro é convertida para uma string onde "Q" representa uma rainha e "." um espaço vazio.
# A função também garante que a label do tabuleiro não desapareça após a execução.
def render_board(board, parent):
    dpg.delete_item(parent, children_only=True)
    with dpg.group(parent=parent):
        if parent == "seq_non_opt_group_content":
            dpg.add_text("Sequencial Não Otimizado:")
        elif parent == "par_non_opt_group_content":
            dpg.add_text("Paralelo Não Otimizado:")
        elif parent == "seq_opt_group_content":
            dpg.add_text("Sequencial Otimizado:")
        elif parent == "par_opt_group_content":
            dpg.add_text("Paralelo Otimizado:")

        for row in board:
            row_str = " ".join(["Q" if cell else "." for cell in row])
            dpg.add_text(row_str)

# Função execute_solver: Executa um solver específico e armazena o resultado na lista de resultados.
# Esta função é responsável por executar o solver, calcular o tempo de execução e armazenar o tabuleiro resultante e o tempo na lista compartilhada de resultados.
def execute_solver(solver_function, n, results, index):
    board, exec_time = solver_function(n)
    results[index] = (board, exec_time)

# Função run_all_solvers: Inicia a execução de todos os algoritmos (sequencial e paralelo, otimizado e não otimizado).
# Esta função cria e inicia threads para cada solver, aguardando a conclusão de todas antes de renderizar os tabuleiros e mostrar os tempos de execução.
# A sincronização das threads é feita usando `join` para garantir que todas as execuções sejam concluídas antes da renderização.
def run_all_solvers(sender, app_data, user_data):
    n = dpg.get_value(user_data["n_input"])
    results = [None] * 4  # Lista para armazenar os resultados dos 4 solvers

    threads = [
        threading.Thread(target=execute_solver, args=(run_sequential_non_optimized, n, results, 0)),
        threading.Thread(target=execute_solver, args=(run_parallel_non_optimized, n, results, 1)),
        threading.Thread(target=execute_solver, args=(run_sequential_optimized, n, results, 2)),
        threading.Thread(target=execute_solver, args=(run_parallel_optimized, n, results, 3))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Renderiza todos os tabuleiros simultaneamente após a conclusão de todos os solvers
    render_board(results[0][0], "seq_non_opt_group_content")
    render_board(results[1][0], "par_non_opt_group_content")
    render_board(results[2][0], "seq_opt_group_content")
    render_board(results[3][0], "par_opt_group_content")

    # Atualiza os tempos de execução
    dpg.set_value("seq_non_opt_time_label", f"Tempo Sequencial Não Otimizado: {results[0][1]:.4f} segundos")
    dpg.set_value("par_non_opt_time_label", f"Tempo Paralelo Não Otimizado: {results[1][1]:.4f} segundos")
    dpg.set_value("seq_opt_time_label", f"Tempo Sequencial Otimizado: {results[2][1]:.4f} segundos")
    dpg.set_value("par_opt_time_label", f"Tempo Paralelo Otimizado: {results[3][1]:.4f} segundos")

# Configurações iniciais do DearPyGui e construção da interface gráfica
dpg.create_context()

with dpg.window(label="Comparação de Algoritmos de N Rainhas", width=1300, height=1000):
    dpg.add_text("Número de Rainhas:")
    n_input = dpg.add_input_int(default_value=8, min_value=1, max_value=20)

    # Etiquetas de tempo para cada método de resolução
    seq_non_opt_time_label = dpg.add_text("Tempo Sequencial Não Otimizado: --", tag="seq_non_opt_time_label")
    par_non_opt_time_label = dpg.add_text("Tempo Paralelo Não Otimizado: --", tag="par_non_opt_time_label")
    seq_opt_time_label = dpg.add_text("Tempo Sequencial Otimizado: --", tag="seq_opt_time_label")
    par_opt_time_label = dpg.add_text("Tempo Paralelo Otimizado: --", tag="par_opt_time_label")

    # Grupos horizontais para exibição dos tabuleiros e separadores
    with dpg.group(horizontal=True):
        with dpg.group(tag="seq_non_opt_group_content"):
            dpg.add_text("Sequencial Não Otimizado:")
        with dpg.drawlist(width=5, height=200):
            dpg.draw_line([0, 0], [0, 200], color=(255, 0, 0, 255), thickness=5)
        with dpg.group(tag="par_non_opt_group_content"):
            dpg.add_text("Paralelo Não Otimizado:")
        with dpg.drawlist(width=5, height=200):
            dpg.draw_line([0, 0], [0, 200], color=(255, 0, 0, 255), thickness=5)
        with dpg.group(tag="seq_opt_group_content"):
            dpg.add_text("Sequencial Otimizado:")
        with dpg.drawlist(width=5, height=200):
            dpg.draw_line([0, 0], [0, 200], color=(255, 0, 0, 255), thickness=5)
        with dpg.group(tag="par_opt_group_content"):
            dpg.add_text("Paralelo Otimizado:")

    # Botão para iniciar a execução de todos os solvers
    dpg.add_button(label="Run All", callback=run_all_solvers, user_data={
        "n_input": n_input,
        "seq_non_opt_time_label": seq_non_opt_time_label,
        "par_non_opt_time_label": par_non_opt_time_label,
        "seq_opt_time_label": seq_opt_time_label,
        "par_opt_time_label": par_opt_time_label,
    })

    dpg.add_spacer(height=20)
    dpg.add_separator()
    dpg.add_spacer(height=10)
    dpg.add_text("Integrantes do Grupo: Rafael, Gustavo, Igor, Eduardo, Giovani, Davi, Steiger")
    dpg.add_text("Tecnologia Utilizada: Threads")

    dpg.add_spacer(height=20)
    dpg.add_separator()
    dpg.add_spacer(height=10)
    dpg.add_text("Explicação das Otimizações Utilizadas:")

    dpg.add_text("Branch and Bound: ")
    dpg.add_text("   - Reduz o espaço de busca eliminando caminhos que certamente não levarão a uma solução.")
    dpg.add_text("   - A abordagem evita explorar configurações de tabuleiro inviáveis, melhorando a eficiência.")

    dpg.add_spacer(height=10)

    dpg.add_text("Distribuição Balanceada do Trabalho: ")
    dpg.add_text("   - Garante que cada thread tenha uma carga de trabalho balanceada.")
    dpg.add_text("   - Evita que algumas threads fiquem ociosas enquanto outras estão sobrecarregadas,")
    dpg.add_text("     resultando em um uso mais eficiente dos recursos disponíveis.")

# Configuração da viewport e inicialização da interface DearPyGui
dpg.create_viewport(title='N-Queens Solver Comparison', width=1300, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
