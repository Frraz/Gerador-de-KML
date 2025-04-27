import os
import sys
import re
import glob
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
from colorama import init, Fore, Style
import simplekml

# Inicializa o colorama
init(autoreset=True)

# Define BASE_DIR corretamente, inclusive para .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'proj')

# Ajusta PROJ_LIB para funcionar corretamente no .exe
import pyproj
os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'proj')

# Callbacks de GUI
nome_area_callback = None
cor_callback = None

def set_callback_nome_area(callback):
    global nome_area_callback
    nome_area_callback = callback

def set_callback_cor(callback):
    global cor_callback
    cor_callback = callback

def criar_diretorios(base_path):
    caminhos = {
        'csv': os.path.join(base_path, 'csv'),
        'kml': os.path.join(base_path, 'kml'),
        'shapefiles': os.path.join(base_path, 'shapefiles')
    }
    for caminho in caminhos.values():
        os.makedirs(caminho, exist_ok=True)
    return caminhos

def formatar_csv(arquivo_csv, pasta_saida):
    print("🔧 Entrou na função formatar_csv")
    print(Fore.CYAN + f"📄 Formatando CSV: {arquivo_csv}")
    
    with open(arquivo_csv, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    areas = []
    area_atual = []
    tamanho_area_atual = None

    for linha in linhas:
        if "Área:" in linha:
            if area_atual:
                areas.append((area_atual, tamanho_area_atual))
                area_atual = []
            match = re.search(r'\( Área: ([\d,\.]+) ha \)', linha)
            if match:
                tamanho_area_atual = match.group(1)
        if linha.strip():
            area_atual.append(linha.strip())

    if area_atual:
        areas.append((area_atual, tamanho_area_atual))

    for area, tamanho_area in areas:
        dados = []
        for item in area:
            partes = item.split(',')
            if len(partes) >= 4:
                ponto = partes[0]
                latitude = partes[1].strip().replace(',', '.')
                longitude = partes[2].strip().replace(',', '.')
                altitude = partes[3].strip().replace(',', '.') if len(partes) > 3 else '0'
                distancia = partes[4].strip().replace(',', '.') if len(partes) > 4 else '0'
                dados.append([ponto, latitude, longitude, altitude, distancia])

        df_area = pd.DataFrame(dados, columns=['Ponto', 'Latitude', 'Longitude', 'Altitude', 'Distancia'])
        df_area = df_area.iloc[2:].reset_index(drop=True)
        df_area.dropna(how='all', inplace=True)
        df_area.dropna(axis=1, how='all', inplace=True)
        df_area = df_area.loc[:, (df_area != '').any(axis=0)]

        nome_arquivo = nome_area_callback(tamanho_area) if nome_area_callback else f"area_{tamanho_area}"
        if not nome_arquivo:
            print(Fore.RED + "❌ Nome inválido. Pulando esta área.")
            continue

        nome_arquivo = re.sub(r'\s+', ' ', nome_arquivo).strip()
        nome_arquivo = re.sub(r'[^\w\-_\. ]', '_', nome_arquivo)

        base_nome = nome_arquivo
        contador = 1
        caminho_saida = os.path.join(pasta_saida, f"{nome_arquivo}.csv")

        while os.path.exists(caminho_saida):
            nome_arquivo = f"{base_nome}_{contador}"
            caminho_saida = os.path.join(pasta_saida, f"{nome_arquivo}.csv")
            contador += 1

        df_area.to_csv(caminho_saida, sep=',', index=False, encoding='utf-8')
        print(Fore.GREEN + f"✔ Área salva como: {caminho_saida}")

def carregar_csv_para_geodataframe(arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    pontos = [Point(lon, lat) for lon, lat in zip(df['Longitude'], df['Latitude'])]
    return gpd.GeoDataFrame(df, geometry=pontos, crs="EPSG:4326")

def criar_poligono(gdf):
    if len(gdf) < 3:
        raise ValueError("Um polígono deve ter pelo menos 3 pontos.")
    coords = gdf.geometry.tolist()
    if not coords[0].equals(coords[-1]):
        coords.append(coords[0])
    poligono = Polygon(coords)
    if not poligono.is_valid:
        raise ValueError("O polígono criado é inválido.")
    return poligono

def salvar_kml(gdf, caminho_saida, cor_preenchimento="7f000000"):
    nome_poligono = os.path.splitext(os.path.basename(caminho_saida))[0]
    
    coords = [(point.x, point.y) for point in gdf.geometry]
    if coords[0] != coords[-1]:
        coords.append(coords[0])  # Fecha o polígono se necessário

    kml = simplekml.Kml()
    pol = kml.newpolygon(name=nome_poligono)
    pol.outerboundaryis = coords

    # Convertendo cor do formato KML (AABBGGRR) para ARGB do simplekml
    hex_color = cor_preenchimento
    if len(hex_color) == 8:
        # simplekml usa a ordem ABGR
        pol.style.polystyle.color = simplekml.Color.changealphaint(
            int(hex_color[:2], 16),  # Alpha
            simplekml.Color.rgb(
                int(hex_color[6:8], 16),  # R
                int(hex_color[4:6], 16),  # G
                int(hex_color[2:4], 16)   # B
            )
        )
    pol.style.polystyle.fill = 1
    pol.style.polystyle.outline = 1
    pol.style.linestyle.width = 2
    pol.style.linestyle.color = simplekml.Color.red  # Borda vermelha, pode ajustar

    kml.save(caminho_saida)
    print(Fore.GREEN + f"✔ KML salvo com simplekml: {caminho_saida}")


def escolher_modelo():
    return cor_callback() if cor_callback else "ff096200"

def processar_csvs_para_kml(diretorio_csv, diretorio_kml):
    print("📍 Entrou na função processar_csvs_para_kml")
    print(Fore.MAGENTA + f"📂 Lendo arquivos CSV em: {diretorio_csv}")
    arquivos = glob.glob(os.path.join(diretorio_csv, "*.csv"))
    print(Fore.MAGENTA + f"🔍 Encontrados: {len(arquivos)} arquivos CSV")
    if not arquivos:
        print(Fore.YELLOW + "⚠ Nenhum arquivo CSV encontrado.")
        return

    cor = escolher_modelo()
    print(Fore.MAGENTA + f"🎨 Cor selecionada: {cor}")
    for arquivo in arquivos:
        try:
            print(Fore.LIGHTBLUE_EX + f"📍 Processando: {arquivo}")
            gdf = carregar_csv_para_geodataframe(arquivo)
            print(Fore.CYAN + f"🔢 GeoDataFrame com {len(gdf)} pontos")
            if len(gdf) < 3:
                print(Fore.YELLOW + "⚠ Área com menos de 3 pontos. Pulando.")
                continue
            nome_saida = os.path.splitext(os.path.basename(arquivo))[0].replace(" ", "_") + "_poligono.kml"
            caminho_saida = os.path.join(diretorio_kml, nome_saida)
            print(Fore.LIGHTBLUE_EX + f"💾 Salvando KML em: {caminho_saida}")
            salvar_kml(gdf, caminho_saida, cor)
        except Exception as e:
            print(Fore.RED + f"❌ Erro no arquivo {arquivo}: {e}")

def unir_kmls_em_um(diretorio_kml, caminho_saida_unico):
    print("📦 Entrou na função unir_kmls_em_um")
    arquivos_kml = glob.glob(os.path.join(diretorio_kml, "*.kml"))
    if not arquivos_kml:
        print(Fore.YELLOW + "⚠ Nenhum KML encontrado para unir.")
        return

    placemarks = []
    for arquivo in arquivos_kml:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                trechos = re.findall(r"<Style.*?</Style>|<Placemark.*?</Placemark>", conteudo, re.DOTALL)
                placemarks.extend(trechos)
        except Exception as e:
            print(Fore.RED + f"❌ Erro ao ler KML {arquivo}: {e}")

    if placemarks:
        kml_final = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    {"".join(placemarks)}
  </Document>
</kml>"""
        with open(caminho_saida_unico, 'w', encoding='utf-8') as f:
            f.write(kml_final)
        print(Fore.GREEN + f"🎯 KML unificado salvo em: {caminho_saida_unico}")
    else:
        print(Fore.YELLOW + "⚠ Nenhum conteúdo válido para unir.")
