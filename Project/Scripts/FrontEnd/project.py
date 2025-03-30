import sqlite3
import customtkinter
import tkinter as tk
from config import TAMANHO, TITLE
from images import ICON, ImageAlunoBase, Add
from PIL import Image, ImageTk
from tkinter import filedialog

# Criar ou conectar ao banco de dados
conn = sqlite3.connect("alunos.db")
c = conn.cursor()

# Criar tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                idade INTEGER,
                sexo TEXT,
                classe TEXT,
                imagem TEXT
            )''')
conn.commit()

# =============CLASS APP======================

class App(customtkinter.CTk):
    
#==============INICIALIAZADOR======================

    #sistema para rodar o app
    def __init__(self):
        super().__init__()
        # Configuração principal
        customtkinter.set_appearance_mode("System")  # Modos: "Light", "Dark", "System"
        self.geometry(TAMANHO)
        self.title(TITLE)
        self.iconbitmap(ICON)
        self.resizable(False, False)
        self.labels()

#==============LABELS=====================

    def labels(self):
      # Classes que temos!
        Classes = ['1 ano', '2 ano', '3 ano', '4 ano', '5 ano']
        

#===============SALVAR NO BANCO DE DADOS E LISTAR==================== 

        def salvar_aluno():
          nome = txtBoxAluno.get("1.0", "end").strip()
          idade = txtIdadeAluno.get("1.0", "end").strip()
          sexo = CheckBoxSexo.get()
          classe = CheckBoxClasse.get()
        
          if nome and idade:
            conn = sqlite3.connect("alunos.db")
            c = conn.cursor()
            c.execute("INSERT INTO alunos (nome, idade, sexo, classe) VALUES (?, ?, ?, ?)", (nome, idade, sexo, classe))
            conn.commit()
            conn.close()
            print("Aluno cadastrado com sucesso!")

        def listar_alunos():
          conn = sqlite3.connect("alunos.db")
          c = conn.cursor()
          c.execute("SELECT * FROM alunos")
          alunos = c.fetchall()
          conn.close()
          print("Lista de Alunos:")
          for aluno in alunos:
            print(aluno)

      #LETREIROS

         # Master do letreiro
        MasterLetreiro = customtkinter.CTkFrame(self, bg_color='transparent', width=850, height=90)
        MasterLetreiro.pack()

         # letreiro
        letreiroCima = customtkinter.CTkLabel(master=MasterLetreiro,bg_color='black', text=None, width=850, height=45)
        letreiroCima.pack()

        textTitle = customtkinter.CTkLabel(master=MasterLetreiro, text='Registro de Estudantes', text_color='white', bg_color='black')
        textTitle.place(x=45, y=10)

      #COISAS

         # Master principal
        MasterInfosAluno = customtkinter.CTkFrame(self)
        MasterInfosAluno.place(x=50, y=120)

         # textbox do aluno
        txtName = customtkinter.CTkLabel(master=MasterInfosAluno, text='Informe o Nome do Aluno')
        txtName.pack()
        txtBoxAluno = customtkinter.CTkTextbox(master=MasterInfosAluno, width=110, height=12)
        txtBoxAluno.pack(padx=25,pady=10)

         # textbox da idade do mesmo
        txtIdd = customtkinter.CTkLabel(master=MasterInfosAluno, text='Informe a Idade do Aluno')
        txtIdd.pack()
        txtIdadeAluno = customtkinter.CTkTextbox(master=MasterInfosAluno, width=110, height=12)
        txtIdadeAluno.pack(pady=25, padx=10)

         # botão de adcionar aluno no Banco de Dados
        self.ButtonAddAluno = customtkinter.CTkButton(master=MasterLetreiro, width=55, height=25, text='Adcionar Aluno', command=salvar_aluno, image=Add)
        self.ButtonAddAluno.pack()

         # box 1
        CheckBoxSexo = customtkinter.CTkOptionMenu(master=MasterInfosAluno, values=["Masculino", "Feminino"])
        CheckBoxSexo.pack(padx=34)

         # box 2
        CheckBoxClasse = customtkinter.CTkOptionMenu(master=MasterInfosAluno, values=[Classes[0], Classes[1], Classes[2], Classes[3], Classes[4]])
        CheckBoxClasse.pack(pady=20)

         # Image Aluno
        self.ImageAluno = customtkinter.CTkLabel(self, text=None, image=(ImageAlunoBase))
        self.ImageAluno.place(x=349, y=100)

         # Listar alunos
        self.btn_listar = customtkinter.CTkButton(MasterLetreiro, width=55, height=25, text="Listar Alunos", command=listar_alunos)
        self.btn_listar.pack()
        self.btn_listar.place(x=235, y=44)

#================LOAD DE IMAGENS=================

        # Função pra adcionar imagem
        def load_image():
            file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if file_path:
              # Carregar e redimensionar a imagem
              img = Image.open(file_path)
              img = img.resize((185, 185), Image.LANCZOS)
              img = ImageTk.PhotoImage(img)

            # Atualizar o label com a nova imagem
              self.ImageAluno.configure(image=img)
              self.ImageAluno.image = img  # Evita que a imagem seja coletada pelo garbage collector

        # Botão para carregar imagem
        self.load_button = customtkinter.CTkButton(self, text="Selecionar Imagem", command=load_image)
        self.load_button.pack(pady=20)
        self.load_button.place(x=349, y=320)

      # Alunos Adcionados 
    
        # Alunos Adcionados Classe
        MasterAdd = customtkinter.CTkFrame(self, width=900)
        MasterAdd.place(x=-20,y=420)

    # CHAMADA

        # Frame da Chamada
        MasterChamadas = customtkinter.CTkFrame(self, width=320, height=500)
        MasterChamadas.place(x=550, y=50)

        LabelTextChamada = customtkinter.CTkLabel(master=MasterChamadas, text='Chamada', bg_color='transparent', text_color='white')
        LabelTextChamada.place(x=130, y=-7)

        #Checkbox da Classe 
        CheckBoxClasseChamada = customtkinter.CTkOptionMenu(master=MasterChamadas, values=[Classes[0], Classes[1], Classes[2], Classes[3], Classes[4]])
        CheckBoxClasseChamada.place(x=95, y=20)

        TextChamadaPresença = customtkinter.CTkLabel(master=MasterChamadas, text='Presente', bg_color='transparent')
        TextChamadaPresença.place(x=67, y=67)

        TextChamadaFalta = customtkinter.CTkLabel(master=MasterChamadas, text='Faltou', bg_color='transparent')
        TextChamadaFalta.place(x=210, y=67)

        TextNomeAlunoChamada = customtkinter.CTkLabel(master=MasterChamadas, text=None)
        TextNomeAlunoChamada.place(x=9, y=100)