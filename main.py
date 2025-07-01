# main.py

import glob
import os
import sys
import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from processamento import (
    criar_diretorios, formatar_csv, gerar_kml_unificado,
    set_callback_nome_area, set_callback_cor, baixar_e_importar_shapefiles
)

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.abspath(relative_path)

def bring_window_to_front(win):
    try:
        win.lift()
        win.attributes('-topmost', True)
        win.after_idle(lambda: win.attributes('-topmost', False))
    except Exception:
        pass

def selecionar_pasta():
    bring_window_to_front(janela)
    pasta = filedialog.askdirectory(parent=janela, title="Selecione a pasta GEOGRÁFICOS")
    if pasta:
        entrada_caminho.set(pasta)

def definir_cor(cor, botao_clicado=None):
    cor_selecionada.set(cor)
    for botao in botoes_cultura:
        botao.configure(
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
    if botao_clicado:
        botao_clicado.configure(
            fg_color="#4CAF50",
            hover_color="#45a049"
        )

def definir_cor_personalizada():
    bring_window_to_front(janela)
    cor_rgb, cor_hex = colorchooser.askcolor(title="Escolha a Cor", parent=janela)
    if cor_hex:
        cor_hex = cor_hex.lstrip('#')
        rr, gg, bb = cor_hex[0:2], cor_hex[2:4], cor_hex[4:6]
        cor_personalizada = f"ff{bb}{gg}{rr}"
        cor_selecionada.set(cor_personalizada)
        for botao in botoes_cultura:
            botao.configure(
                fg_color="#3a3a3a",
                hover_color="#4a4a4a"
            )

def pedir_nome_area(tamanho_area):
    resultado, evento = {"nome": None}, threading.Event()
    def _ask():
        bring_window_to_front(janela)
        resultado["nome"] = simpledialog.askstring(
            "Nome da Área",
            f"Digite o nome da área (Tamanho: {tamanho_area} ha):",
            parent=janela
        )
        evento.set()
    janela.after(0, _ask)
    evento.wait()
    return resultado["nome"]

def pedir_adicionar_shapefiles():
    resultado, evento = {"val": False}, threading.Event()
    def _ask():
        bring_window_to_front(janela)
        resultado["val"] = messagebox.askyesno(
            "Adicionar Shapefiles de Fazenda",
            "Deseja adicionar um ou mais shapefiles de fazenda ao KML final?",
            parent=janela
        )
        evento.set()
    janela.after(0, _ask)
    evento.wait()
    return resultado["val"]

def pedir_recibo_e_nome_fazenda():
    resultado, evento = {"recibo": None, "nome": None}, threading.Event()
    def _ask():
        bring_window_to_front(janela)
        recibo = simpledialog.askstring(
            "Recibo do CAR",
            "Informe o número do recibo do CAR da fazenda (com ou sem pontos):",
            parent=janela
        )
        if not recibo:
            resultado["recibo"], resultado["nome"] = None, None
            evento.set()
            return
        nome = simpledialog.askstring(
            "Nome para o shapefile",
            "Informe o nome para este shapefile/fazenda:",
            parent=janela
        )
        if not nome:
            resultado["recibo"], resultado["nome"] = None, None
            evento.set()
            return
        resultado["recibo"], resultado["nome"] = recibo.strip(), nome.strip().replace(" ", "_")
        evento.set()
    janela.after(0, _ask)
    evento.wait()
    return resultado["recibo"], resultado["nome"]

def show_messagebox(tipo, title, msg):
    bring_window_to_front(janela)
    if tipo == "info":
        messagebox.showinfo(title, msg, parent=janela)
    elif tipo == "warning":
        messagebox.showwarning(title, msg, parent=janela)
    elif tipo == "error":
        messagebox.showerror(title, msg, parent=janela)

def status(msg, busy=False):
    status_label.configure(text=msg)
    if busy:
        botao_iniciar.configure(
            state="disabled",
            text="Processando...",
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

def adicionar_log(msg):
    log_text.configure(state="normal")
    log_text.insert("end", f"{msg}\n")
    log_text.see("end")
    log_text.configure(state="disabled")

def iniciar_processamento():
    caminho, cor = entrada_caminho.get().strip(), cor_selecionada.get()
    if not caminho or not cor:
        show_messagebox("warning", "Aviso", "Selecione uma pasta e uma cultura/cor.")
        return

    set_callback_nome_area(pedir_nome_area)
    set_callback_cor(lambda: cor)

    def tarefa():
        try:
            status("Processando...", busy=True)
            adicionar_log("Criando diretórios auxiliares...")
            caminhos = criar_diretorios(caminho)
            for arquivo in glob.glob(f"{caminho}/*.csv"):
                adicionar_log(f"Formatando CSV: {arquivo}")
                formatar_csv(arquivo, caminhos['csv'])

            adicionar = pedir_adicionar_shapefiles()
            if adicionar:
                baixar_e_importar_shapefiles(
                    pedir_recibo_e_nome_fazenda,
                    caminhos['shapefiles'],
                    janela
                )

            adicionar_log("Gerando KML unificado...")
            gerar_kml_unificado(
                caminhos['csv'],
                cor,
                caminhos['shapefiles'],
                os.path.join(caminho, "todos_poligonos.kml")
            )
            adicionar_log("Processamento finalizado!")
            show_messagebox("info", "Concluído", "Processamento finalizado!")
            status("Finalizado!")
        except Exception as e:
            print("Erro:", e)
            adicionar_log(f"Erro: {e}")
            show_messagebox("error", "Erro", str(e))
            status("Erro!")
        finally:
            botao_iniciar.configure(state="normal")
            progressbar.stop()

    threading.Thread(target=tarefa).start()

# ========== INTERFACE ==========
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Gerador de KML Agrícola")

largura = 820
altura = 670
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura // 2)
pos_y = (altura_tela // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
janela.resizable(True, True)

# Menu (opcional)
def abrir_link(url):
    webbrowser.open_new(url)

def sobre():
    botao_sobre.configure(state="disabled")  # Desativa botão para evitar múltiplas janelas
    janela_sobre = ctk.CTkToplevel(janela)
    janela_sobre.title("Sobre")
    janela_sobre.geometry("420x400")
    janela_sobre.resizable(False, False)

    # --- Centralizar na tela principal ---
    janela.update_idletasks()
    largura_s = 420
    altura_s = 400
    x = janela.winfo_x() + (janela.winfo_width() // 2) - (largura_s // 2)
    y = janela.winfo_y() + (janela.winfo_height() // 2) - (altura_s // 2)
    janela_sobre.geometry(f"{largura_s}x{altura_s}+{x}+{y}")

    # --- Sempre na frente e modal ---
    janela_sobre.transient(janela)
    janela_sobre.lift()
    janela_sobre.grab_set()
    janela_sobre.focus_force()

    # Ícone ou emoji (opcional, remova se não quiser)
    ctk.CTkLabel(janela_sobre, text="🌱", font=("Arial", 32)).pack(pady=(8, 0))

    ctk.CTkLabel(janela_sobre, text="Gerador de KML Agrícola", font=("Arial", 16, "bold")).pack(pady=(4, 0))
    ctk.CTkLabel(janela_sobre, text="Por Warley Ferraz (Frraz)\nVersão: 2025", font=("Arial", 13)).pack(pady=(0, 8))

    ctk.CTkLabel(janela_sobre, text="Contato:", font=("Arial", 13, "bold")).pack(pady=(10, 2))

    botoes = [
        ("Email", "mailto:warley.ferraz.wf@gmail.com", "#d44638"),
        ("Instagram", "https://www.instagram.com/ferraz.____/", "#E4405F"),
        ("WhatsApp", "https://wa.me/5594992083253", "#25D366"),
        ("LinkedIn", "https://www.linkedin.com/in/warley-ferraz-almeida-280a55185/", "#0077B5"),
        ("GitHub", "https://github.com/Frraz", "#181717"),
    ]
    for texto, url, cor in botoes:
        btn = ctk.CTkButton(
            janela_sobre, text=texto, width=220,
            fg_color=cor, hover_color="#444444",
            text_color="white", command=lambda u=url: webbrowser.open_new(u)
        )
        btn.pack(pady=3)

    def fechar_sobre():
        botao_sobre.configure(state="normal")
        janela_sobre.destroy()
    ctk.CTkButton(janela_sobre, text="Fechar", command=fechar_sobre, width=100).pack(pady=10)
    janela_sobre.protocol("WM_DELETE_WINDOW", fechar_sobre)

def ajuda():
    show_messagebox("info", "Ajuda", "1. Selecione a pasta GEOGRÁFICOS\n2. Escolha a cultura/cor\n3. Clique em Iniciar Processamento\n\nVocê será guiado durante o processo.")

menu_bar = ctk.CTkFrame(janela, fg_color="transparent")
menu_bar.place(x=0, y=0, relwidth=1)
botao_ajuda = ctk.CTkButton(menu_bar, text="Ajuda", width=60, command=ajuda)
botao_ajuda.pack(side="right", padx=12, pady=2)
botao_sobre = ctk.CTkButton(menu_bar, text="Sobre", width=60, command=sobre)
botao_sobre.pack(side="right", padx=2, pady=2)

entrada_caminho = ctk.StringVar()
cor_selecionada = ctk.StringVar()

frame_pasta = ctk.CTkFrame(janela, corner_radius=10)
frame_pasta.pack(pady=(35,7), padx=20, fill="x")
ctk.CTkLabel(frame_pasta, text="Selecione a pasta GEOGRÁFICOS:", font=("Arial", 15, "bold")).pack(pady=(10,0))
entrada = ctk.CTkEntry(frame_pasta, textvariable=entrada_caminho, width=500)
entrada.pack(pady=5)
ctk.CTkButton(frame_pasta, text="Procurar Pasta", command=selecionar_pasta).pack(pady=7)

frame_cultura = ctk.CTkFrame(janela, corner_radius=10)
frame_cultura.pack(pady=10, padx=20, fill="x")
ctk.CTkLabel(frame_cultura, text="Escolha a cultura:", font=("Arial", 15, "bold")).pack(pady=10)

botoes = ctk.CTkFrame(frame_cultura)
botoes.pack(pady=10)

botoes_cultura = []
for texto, cor in [("Soja", "ff096200"), ("Milho", "ffe3ff00")]:
    botao = ctk.CTkButton(botoes, text=texto, width=140, height=40)
    botao.configure(command=lambda c=cor, b=botao: definir_cor(c, b))
    botao.pack(side="left", padx=10, pady=5)
    botoes_cultura.append(botao)

botao_personalizada = ctk.CTkButton(
    botoes,
    text="Cor Personalizada",
    width=140,
    height=40,
    command=definir_cor_personalizada
)
botao_personalizada.pack(side="left", padx=10, pady=5)

frame_progresso = ctk.CTkFrame(janela, corner_radius=10)
frame_progresso.pack(padx=20, pady=8, fill="x")

botao_iniciar = ctk.CTkButton(
    frame_progresso,
    text="Iniciar Processamento",
    font=("Arial", 15, "bold"),
    width=250,
    height=50,
    command=iniciar_processamento
)
botao_iniciar.pack(pady=15)

status_label = ctk.CTkLabel(frame_progresso, text="Aguardando...", font=("Arial", 13))
status_label.pack(pady=(0,8))

progressbar = ctk.CTkProgressBar(frame_progresso, mode="indeterminate")
progressbar.pack(fill="x", padx=60, pady=10)
progressbar.stop()

frame_log = ctk.CTkFrame(janela, corner_radius=10)
frame_log.pack(padx=20, pady=(5,14), fill="both", expand=True)
ctk.CTkLabel(frame_log, text="Log de Execução:", font=("Arial", 13, "bold")).pack(pady=(6,0))
log_text = ctk.CTkTextbox(frame_log, height=110)
log_text.pack(padx=8, pady=(2,8), fill="both", expand=True)
log_text.configure(state="disabled")

set_callback_nome_area(pedir_nome_area)
set_callback_cor(lambda: cor_selecionada.get())

if __name__ == "__main__":
    bring_window_to_front(janela)
    janela.mainloop()