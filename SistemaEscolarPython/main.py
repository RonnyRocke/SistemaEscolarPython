# Importações necessárias
import tkinter as tk  # Módulo para criação de interfaces gráficas
from tkinter import messagebox  # Módulo para exibir mensagens de caixa de diálogo
from tkinter import ttk  # Módulo de widgets adicionais para tkinter
import mysql.connector  # Módulo para conectar e interagir com o banco de dados MySQL

# Configuração do banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',  # Endereço do servidor MySQL
    user='root',       # Nome de usuário do MySQL
    password='',       # Senha do MySQL
    database='gestao_escolar'  # Nome do banco de dados
)
cursor = conn.cursor()  # Objeto para executar comandos SQL no banco de dados

# Criação das tabelas se não existirem
# Tabela para armazenar informações dos usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)''')

# Tabela para armazenar informações dos alunos
cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    matricula VARCHAR(255) UNIQUE,
    idade INT,
    turma VARCHAR(255)
)''')

# Tabela para armazenar notas dos alunos
cursor.execute('''
CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT,
    disciplina VARCHAR(255),
    nota DECIMAL(5, 2),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
    UNIQUE (aluno_id, disciplina)
)''')
conn.commit()  # Confirmar as alterações no banco de dados

# Função para verificar se o usuário está logado
logged_user = None

# Função para cadastrar um novo usuário no sistema
def cadastrar_usuario(username, password):
    try:
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso')
    except mysql.connector.IntegrityError:
        messagebox.showerror('Erro', 'Usuário já existe')

# Função para realizar o login do usuário
def logar_usuario(username, password):
    global logged_user
    cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    if user:
        logged_user = user
        messagebox.showinfo('Sucesso', 'Login realizado com sucesso')
        abrir_tela_principal()
    else:
        messagebox.showerror('Erro', 'Usuário ou senha incorretos')

# Função para cadastrar um novo aluno no sistema
def cadastrar_aluno(nome, matricula, idade, turma):
    try:
        cursor.execute('INSERT INTO alunos (nome, matricula, idade, turma) VALUES (%s, %s, %s, %s)', (nome, matricula, idade, turma))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Aluno cadastrado com sucesso')
    except mysql.connector.IntegrityError:
        messagebox.showerror('Erro', 'Matrícula já existe')

# Função para adicionar uma nova nota para um aluno
def adicionar_nota(aluno_id, disciplina, nota):
    try:
        cursor.execute('INSERT INTO notas (aluno_id, disciplina, nota) VALUES (%s, %s, %s)', (aluno_id, disciplina, nota))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Nota adicionada com sucesso')
    except mysql.connector.IntegrityError:
        messagebox.showerror('Erro', 'Nota para essa disciplina já existe')

# Função para atualizar uma nota existente
def atualizar_nota(nota_id, nota):
    cursor.execute('UPDATE notas SET nota = %s WHERE id = %s', (nota, nota_id))
    conn.commit()
    messagebox.showinfo('Sucesso', 'Nota atualizada com sucesso')

# Função para apagar uma nota
def apagar_nota(nota_id):
    cursor.execute('DELETE FROM notas WHERE id = %s', (nota_id,))
    conn.commit()
    messagebox.showinfo('Sucesso', 'Nota apagada com sucesso')

# Função para obter todas as notas de um aluno
def obter_notas(aluno_id):
    cursor.execute('SELECT id, disciplina, nota FROM notas WHERE aluno_id = %s', (aluno_id,))
    return cursor.fetchall()

# Função para abrir a tela de login
def abrir_tela_login():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg='blue')
    frame.pack(expand=True, fill='both')

    tk.Label(frame, text='Login', font=('Arial', 20), bg='blue', fg='white').pack(pady=20)

    tk.Label(frame, text='Usuário', bg='blue', fg='white').pack()
    username_entry = tk.Entry(frame)
    username_entry.pack()

    tk.Label(frame, text='Senha', bg='blue', fg='white').pack()
    password_entry = tk.Entry(frame, show='*')
    password_entry.pack()

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        logar_usuario(username, password)

    def on_register():
        abrir_tela_cadastro()

    btn_login = tk.Button(frame, text='Login', command=on_login)
    btn_login.pack(pady=10)
    configurar_botoes(btn_login)

    btn_register = tk.Button(frame, text='Cadastrar', command=on_register)
    btn_register.pack(pady=10)
    configurar_botoes(btn_register)

# Função para abrir a tela de cadastro de usuário
def abrir_tela_cadastro():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg='blue')
    frame.pack(expand=True, fill='both')

    tk.Label(frame, text='Cadastro', font=('Arial', 20), bg='blue', fg='white').pack(pady=20)

    tk.Label(frame, text='Usuário', bg='blue', fg='white').pack()
    username_entry = tk.Entry(frame)
    username_entry.pack()

    tk.Label(frame, text='Senha', bg='blue', fg='white').pack()
    password_entry = tk.Entry(frame, show='*')
    password_entry.pack()

    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        cadastrar_usuario(username, password)

    btn_register = tk.Button(frame, text='Cadastrar', command=on_register)
    btn_register.pack(pady=10)
    configurar_botoes(btn_register)

    def on_back():
        abrir_tela_login()

    btn_back = tk.Button(frame, text='Voltar', command=on_back)
    btn_back.pack(pady=10)
    configurar_botoes(btn_back)

    btn_back.pack(pady=10)
    configurar_botoes(btn_back)

# Função para abrir a tela principal do sistema
def abrir_tela_principal():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg='blue')
    frame.pack(expand=True, fill='both')

    logo = tk.PhotoImage(file="logo.png")  # Carregar a imagem da logo
    tk.Label(frame, image=logo, bg='blue').pack(pady=10)  # Exibir a logo

    tk.Label(frame, text='DESENVOLVEDORES: Ronald Soares, Danilo Stival, Matheus Barbosa, Will, Gabriel Magno', font=('Arial', 10), bg='blue', fg='white').pack(pady=10)

    tk.Label(frame, text='Gestão Escolar', font=('Arial', 20), bg='blue', fg='white').pack(pady=20)

    # Função para abrir a tela de cadastro de aluno
    def abrir_tela_cadastro_aluno():
        for widget in root.winfo_children():
            widget.destroy()

        frame = tk.Frame(root, bg='blue')
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text='Cadastro de Aluno', font=('Arial', 20), bg='blue', fg='white').pack(pady=20)

        tk.Label(frame, text='Nome', bg='blue', fg='white').pack()
        nome_entry = tk.Entry(frame)
        nome_entry.pack()

        tk.Label(frame, text='Matrícula', bg='blue', fg='white').pack()
        matricula_entry = tk.Entry(frame)
        matricula_entry.pack()

        tk.Label(frame, text='Idade', bg='blue', fg='white').pack()
        idade_entry = tk.Entry(frame)
        idade_entry.pack()

        tk.Label(frame, text='Turma', bg='blue', fg='white').pack()
        turma_entry = tk.Entry(frame)
        turma_entry.pack()

        def on_register():
            nome = nome_entry.get()
            matricula = matricula_entry.get()
            idade = int(idade_entry.get())
            turma = turma_entry.get()
            cadastrar_aluno(nome, matricula, idade, turma)

        btn_register = tk.Button(frame, text='Cadastrar', command=on_register)
        btn_register.pack(pady=10)
        configurar_botoes(btn_register)

        def on_back():
            abrir_tela_principal()

        btn_back = tk.Button(frame, text='Voltar', command=on_back)
        btn_back.pack(pady=10)
        configurar_botoes(btn_back)

    # Função para abrir a tela de gerenciamento de notas
    def abrir_tela_notas():
        for widget in root.winfo_children():
            widget.destroy()

        frame = tk.Frame(root, bg='blue')
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text='Gerenciamento de Notas', font=('Arial', 20), bg='blue', fg='white').pack(pady=20)

        tk.Label(frame, text='Matrícula do Aluno', bg='blue', fg='white').pack()
        matricula_entry = tk.Entry(frame)
        matricula_entry.pack()

        notas_tree = ttk.Treeview(frame, columns=('Disciplina', 'Nota'), show='headings')
        notas_tree.heading('Disciplina', text='Disciplina')
        notas_tree.heading('Nota', text='Nota')
        notas_tree.pack(pady=10)

        def on_search():
            for i in notas_tree.get_children():
                notas_tree.delete(i)

            matricula = matricula_entry.get()
            cursor.execute('SELECT id FROM alunos WHERE matricula = %s', (matricula,))
            aluno = cursor.fetchone()
            if aluno:
                aluno_id = aluno[0]
                notas = obter_notas(aluno_id)
                for nota in notas:
                    nota_id, disciplina, nota_valor = nota
                    notas_tree.insert('', 'end', values=(disciplina, nota_valor))

        btn_search = tk.Button(frame, text='Buscar Notas', command=on_search)
        btn_search.pack(pady=10)
        configurar_botoes(btn_search)

        tk.Label(frame, text='Disciplina', bg='blue', fg='white').pack()
        disciplina_entry = tk.Entry(frame)
        disciplina_entry.pack()

        tk.Label(frame, text='Nota', bg='blue', fg='white').pack()
        nota_entry = tk.Entry(frame)
        nota_entry.pack()

        def on_add():
            matricula = matricula_entry.get()
            cursor.execute('SELECT id FROM alunos WHERE matricula = %s', (matricula,))
            aluno = cursor.fetchone()
            if aluno:
                aluno_id = aluno[0]
                disciplina = disciplina_entry.get()
                nota = float(nota_entry.get())
                adicionar_nota(aluno_id, disciplina, nota)
                on_search()
            else:
                messagebox.showerror('Erro', 'Aluno não encontrado')

        btn_add = tk.Button(frame, text='Adicionar Nota', command=on_add)
        btn_add.pack(pady=10)
        configurar_botoes(btn_add)

        def on_update():
            selected_item = notas_tree.selection()
            if selected_item:
                item = notas_tree.item(selected_item)
                disciplina = item['values'][0]
                nota = float(nota_entry.get())
                matricula = matricula_entry.get()
                cursor.execute('SELECT id FROM alunos WHERE matricula = %s', (matricula,))
                aluno = cursor.fetchone()
                if aluno:
                    aluno_id = aluno[0]
                    cursor.execute('SELECT id FROM notas WHERE aluno_id = %s AND disciplina = %s', (aluno_id, disciplina))
                    nota_id = cursor.fetchone()[0]
                    atualizar_nota(nota_id, nota)
                    on_search()
                else:
                    messagebox.showerror('Erro', 'Aluno não encontrado')
            else:
                messagebox.showerror('Erro', 'Nenhuma nota selecionada')

        btn_update = tk.Button(frame, text='Atualizar Nota', command=on_update)
        btn_update.pack(pady=10)
        configurar_botoes(btn_update)

        def on_delete():
            selected_item = notas_tree.selection()
            if selected_item:
                item = notas_tree.item(selected_item)
                disciplina = item['values'][0]
                matricula = matricula_entry.get()
                cursor.execute('SELECT id FROM alunos WHERE matricula = %s', (matricula,))
                aluno = cursor.fetchone()
                if aluno:
                    aluno_id = aluno[0]
                    cursor.execute('SELECT id FROM notas WHERE aluno_id = %s AND disciplina = %s', (aluno_id, disciplina))
                    nota_id = cursor.fetchone()[0]
                    apagar_nota(nota_id)
                    on_search()
                else:
                    messagebox.showerror('Erro', 'Aluno não encontrado')
            else:
                messagebox.showerror('Erro', 'Nenhuma nota selecionada')

        btn_delete = tk.Button(frame, text='Apagar Nota', command=on_delete)
        btn_delete.pack(pady=10)
        configurar_botoes(btn_delete)

        def on_back():
            abrir_tela_principal()

        btn_back = tk.Button(frame, text='Voltar', command=on_back)
        btn_back.pack(pady=10)
        configurar_botoes(btn_back)

    btn_cadastro_aluno = tk.Button(frame, text='Cadastrar Aluno', command=abrir_tela_cadastro_aluno)
    btn_cadastro_aluno.pack(pady=10)
    configurar_botoes(btn_cadastro_aluno)

    btn_gerenciar_notas = tk.Button(frame, text='Gerenciar Notas', command=abrir_tela_notas)
    btn_gerenciar_notas.pack(pady=10)
    configurar_botoes(btn_gerenciar_notas)

    # Função para fazer logout do sistema
    def on_logout():
        global logged_user
        logged_user = None
        abrir_tela_login()

    btn_logout = tk.Button(frame, text='Logout', command=on_logout)
    btn_logout.pack(pady=10)
    configurar_botoes(btn_logout)

    root.mainloop()

# Função para configurar o efeito visual dos botões
def configurar_botoes(button):
    def on_enter(e):
        button['background'] = 'lightblue'
    def on_leave(e):
        button['background'] = 'SystemButtonFace'
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Criar a janela principal
root = tk.Tk()
root.title('Gestão Escolar')
root.geometry('600x600')
root.configure(bg='blue')

# Iniciar com a tela de login
abrir_tela_login()

# Iniciar o loop principal do tkinter
root.mainloop()


    