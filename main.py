import glob
import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from processamento import (
    criar_diretorios, formatar_csv, processar_csvs_para_kml, unir_kmls_em_um,
    set_callback_nome_area, set_callback_cor
)

# Funções
def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.abspath(relative_path)

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entrada_caminho.set(pasta)

def definir_cor(cor, botao_clicado=None):
    cor_selecionada.set(cor)
    for botao in botoes_cultura:
        botao.configure(
            fg_color="#3a3a3a",   # Cinza escuro (não selecionado)
            hover_color="#4a4a4a" # Levemente mais claro no hover
        )
    if botao_clicado:
        botao_clicado.configure(
            fg_color="#4CAF50",    # Verde forte (selecionado)
            hover_color="#45a049"  # Verde um pouco mais claro no hover
        )

def definir_cor_personalizada():
    cor_rgb, cor_hex = colorchooser.askcolor(title="Escolha a Cor")
    if cor_hex:
        cor_hex = cor_hex.lstrip('#')
        rr, gg, bb = cor_hex[0:2], cor_hex[2:4], cor_hex[4:6]
        cor_personalizada = f"ff{bb}{gg}{rr}"
        cor_selecionada.set(cor_personalizada)

        # Reseta os botões para a cor padrão (não selecionado)
        for botao in botoes_cultura:
            botao.configure(
                fg_color="#3a3a3a",
                hover_color="#4a4a4a"
            )


def pedir_nome_area(tamanho_area):
    return simpledialog.askstring("Nome da Área", f"Digite o nome da área (Tamanho: {tamanho_area} ha):")

def iniciar_processamento():
    caminho, cor = entrada_caminho.get().strip(), cor_selecionada.get()
    if not caminho or not cor:
        messagebox.showwarning("Aviso", "Selecione uma pasta e uma cultura/cor.")
        return

    def obter_nome(tamanho):
        resultado, evento = {"nome": None}, threading.Event()
        janela.after(0, lambda: (resultado.update(nome=simpledialog.askstring("Nome da Área", f"Tamanho: {tamanho} ha")) or evento.set()))
        evento.wait()
        return resultado["nome"]

    set_callback_nome_area(obter_nome)
    set_callback_cor(lambda: cor)

    def tarefa():
        try:
            status("🔵 Processando...", busy=True)
            caminhos = criar_diretorios(caminho)
            for arquivo in glob.glob(f"{caminho}/*.csv"):
                formatar_csv(arquivo, caminhos['csv'])
            processar_csvs_para_kml(caminhos['csv'], caminhos['kml'])
            unir_kmls_em_um(caminhos['kml'], f"{caminho}/todos_poligonos.kml")
            messagebox.showinfo("Concluído", "Processamento finalizado!")
            status("✅ Finalizado!")
        except Exception as e:
            print("Erro:", e)
            messagebox.showerror("Erro", str(e))
            status("❌ Erro!")
        finally:
            botao_iniciar.configure(state="normal")
            progressbar.stop()

    threading.Thread(target=tarefa).start()

def status(msg, busy=False):
    status_label.configure(text=msg)
    if busy:
        botao_iniciar.configure(
            state="disabled",
            text="⏳ Processando...",
            fg_color="#3b8ed0",
            hover_color="#569cd6",
            text_color="white",
            anchor="center"
        )
        progressbar.start()
    else:
        botao_iniciar.configure(
            state="normal",
            text="Iniciar Processamento",
            fg_color="#1f6aa5",
            hover_color="#3b8ed0",
            text_color="white",
            anchor="center"
        )
        progressbar.stop()

# ========== INTERFACE ==========
ctk.set_appearance_mode("System")    # Dark / Light / System
ctk.set_default_color_theme("blue")  # Tema azul (pode ser "green", "dark-blue", etc.)

janela = ctk.CTk()
janela.title("🌾 Gerador de KML Agrícola")

largura = 800
altura = 600
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura // 2)
pos_y = (altura_tela // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

entrada_caminho = ctk.StringVar()
cor_selecionada = ctk.StringVar()

frame_pasta = ctk.CTkFrame(janela, corner_radius=10)
frame_pasta.pack(pady=20, padx=20, fill="x")

ctk.CTkLabel(frame_pasta, text="Selecione a pasta GEOGRÁFICOS:", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkEntry(frame_pasta, textvariable=entrada_caminho, width=500).pack(pady=5)
ctk.CTkButton(frame_pasta, text="Procurar Pasta", command=selecionar_pasta).pack(pady=10)

frame_cultura = ctk.CTkFrame(janela, corner_radius=10)
frame_cultura.pack(pady=20, padx=20, fill="x")

ctk.CTkLabel(frame_cultura, text="Escolha a cultura:", font=("Arial", 16, "bold")).pack(pady=10)

botoes = ctk.CTkFrame(frame_cultura)
botoes.pack(pady=10)

botoes_cultura = []

# Botões de cultura
for texto, cor in [("Soja", "ff096200"), ("Milho", "ffe3ff00")]:
    botao = ctk.CTkButton(botoes, text=texto, width=140, height=40)
    botao.configure(command=lambda c=cor, b=botao: definir_cor(c, b))
    botao.pack(side="left", padx=10, pady=5)
    botoes_cultura.append(botao)

# Botão de cor personalizada
botao_personalizada = ctk.CTkButton(botoes, text="Cor Personalizada", width=140, height=40, command=definir_cor_personalizada)
botao_personalizada.pack(side="left", padx=10, pady=5)

botao_iniciar = ctk.CTkButton(
    janela, 
    text="Iniciar Processamento",
    font=("Arial", 15, "bold"),
    width=250,
    height=50,
    command=iniciar_processamento
)
botao_iniciar.pack(pady=30)

status_label = ctk.CTkLabel(janela, text="Aguardando...", font=("Arial", 14))
status_label.pack(pady=10)

progressbar = ctk.CTkProgressBar(janela, mode="indeterminate")
progressbar.pack(fill="x", padx=60, pady=20)
progressbar.stop()

set_callback_nome_area(pedir_nome_area)
set_callback_cor(lambda: cor_selecionada.get())

# Iniciar aplicação
if __name__ == "__main__":
    janela.mainloop()
