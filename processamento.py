# processamento.py

import os
import sys
import re
import glob
import requests
import zipfile
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
from colorama import init
import simplekml
import threading

# Inicializa o colorama
init(autoreset=True)

# Define BASE_DIR corretamente, inclusive para .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'proj')

import pyproj
os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'proj')

try:
    from tkinter import messagebox
except ImportError:
    messagebox = None

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
    print("Entrou na função formatar_csv")
    print(f"Formatando CSV: {arquivo_csv}")

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
            print("Nome inválido. Pulando esta área.")
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
        print(f"Área salva como: {caminho_saida}")

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

def salvar_kml(gdf, folder, cor_preenchimento=None):
    nome_poligono = getattr(gdf, "nome_poligono", None)
    if nome_poligono is None:
        nome_poligono = "Polígono"
    coords = [(point.x, point.y) for point in gdf.geometry]
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    pol = folder.newpolygon(name=nome_poligono)
    pol.outerboundaryis = coords
    if cor_preenchimento:  # Personalizado para coordenadas
        pol.style.polystyle.color = cor_preenchimento
        pol.style.polystyle.fill = 1
        pol.style.linestyle.width = 2
    else:  # Padrão para shapes
        pol.style.polystyle.fill = 0  # Sem preenchimento

def processar_csvs_para_kml(diretorio_csv, folder, cor_preenchimento):
    print("Entrou na função processar_csvs_para_kml")
    print(f"Lendo arquivos CSV em: {diretorio_csv}")
    arquivos = glob.glob(os.path.join(diretorio_csv, "*.csv"))
    print(f"Encontrados: {len(arquivos)} arquivos CSV")
    if not arquivos:
        print("Nenhum arquivo CSV encontrado.")
        return
    for arquivo in arquivos:
        try:
            print(f"Processando: {arquivo}")
            gdf = carregar_csv_para_geodataframe(arquivo)
            print(f"GeoDataFrame com {len(gdf)} pontos")
            if len(gdf) < 3:
                print("Área com menos de 3 pontos. Pulando.")
                continue
            nome_saida = os.path.splitext(os.path.basename(arquivo))[0].replace(" ", "_")
            gdf.nome_poligono = nome_saida
            salvar_kml(gdf, folder, cor_preenchimento)
        except Exception as e:
            print(f"Erro no arquivo {arquivo}: {e}")

def adicionar_shapes_ao_folder(shp_dir, folder):
    """
    Para cada shapefile encontrado em shp_dir (inclusive em subpastas),
    cria uma subpasta dentro de 'folder' com o nome da fazenda,
    e adiciona os polígonos daquele shapefile nela.
    """
    arquivos_shp = glob.glob(os.path.join(shp_dir, "**", "*.shp"), recursive=True)
    for arquivo in arquivos_shp:
        try:
            gdf = gpd.read_file(arquivo)
            nome_fazenda = os.path.splitext(os.path.basename(arquivo))[0]
            subfolder = folder.newfolder(name=nome_fazenda)
            nome_col = None
            # Tenta descobrir uma coluna de nome para os polígonos, caso exista
            for c in ['uso', 'classeuso', 'nome', 'legenda', 'desc', 'tipo', 'CLASSE', 'DESCRICAO', 'DESCR', 'TIPO']:
                if c.lower() in [x.lower() for x in gdf.columns]:
                    nome_col = [x for x in gdf.columns if x.lower() == c.lower()][0]
                    break
            for _, row in gdf.iterrows():
                placemark_name = row[nome_col] if nome_col else nome_fazenda
                geom = row.geometry
                if geom.geom_type == 'Polygon':
                    poly = subfolder.newpolygon(outerboundaryis=list(geom.exterior.coords), name=str(placemark_name))
                    poly.style.polystyle.fill = 0  # Sem preenchimento
                elif geom.geom_type == 'MultiPolygon':
                    for polygeom in geom.geoms:
                        poly = subfolder.newpolygon(outerboundaryis=list(polygeom.exterior.coords), name=str(placemark_name))
                        poly.style.polystyle.fill = 0  # Sem preenchimento
        except Exception as e:
            print(f"Erro ao processar shapefile {arquivo}: {e}")

def gerar_kml_unificado(diretorio_csv, cor_preenchimento, diretorio_shapefiles, caminho_saida_unico):
    print("Gerando KML unificado...")
    kml = simplekml.Kml()
    # Pasta para os polígonos das coordenadas
    folder_csv = kml.newfolder(name="Polígonos das Coordenadas")
    processar_csvs_para_kml(diretorio_csv, folder_csv, cor_preenchimento)
    # Pasta para os shapes
    folder_shapes = kml.newfolder(name="Shapes das Fazendas")
    adicionar_shapes_ao_folder(diretorio_shapefiles, folder_shapes)
    kml.save(caminho_saida_unico)
    print(f"KML unificado salvo em: {caminho_saida_unico}")

def formatar_recibo_car(recibo):
    return recibo.replace('.', '')

def baixar_shape_zip(url, destino):
    try:
        resp = requests.get(url, verify=True)
        resp.raise_for_status()
    except requests.exceptions.SSLError:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(url, verify=False)
        resp.raise_for_status()
    with open(destino, 'wb') as f:
        f.write(resp.content)

def extrair_e_renomear_shape(zip_path, pasta_destino, novo_nome):
    pasta_fazenda = os.path.join(pasta_destino, novo_nome)
    os.makedirs(pasta_fazenda, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(pasta_fazenda)
    exts = ['.shp', '.shx', '.dbf', '.prj', '.cpg', '.qix']
    for ext in exts:
        for arquivo in glob.glob(os.path.join(pasta_fazenda, f"*{ext}")):
            base = os.path.join(pasta_fazenda, f"{novo_nome}{ext}")
            if not os.path.exists(base):
                os.rename(arquivo, base)
    return os.path.join(pasta_fazenda, f"{novo_nome}.shp")

def baixar_e_importar_shapefiles(callback_recibo_nome, pasta_shapefiles, janela=None):
    while True:
        if janela:
            janela.after(0, lambda: None)
        recibo, nome = callback_recibo_nome()
        if not recibo or not nome:
            break
        recibo_fmt = formatar_recibo_car(recibo)
        url = f"https://car.semas.pa.gov.br/site/consulta/imoveis/baixarShapeFile/{recibo_fmt}"
        zip_path = os.path.join(pasta_shapefiles, f"{nome}.zip")
        try:
            print(f"Baixando {url} ...")
            baixar_shape_zip(url, zip_path)
            extrair_e_renomear_shape(zip_path, pasta_shapefiles, nome)
            print(f"Shapefile {nome} baixado e extraído.")
        except Exception as e:
            print(f"Erro ao importar shapefile {nome}: {e}")
            if janela and messagebox:
                errormsg = f"Erro ao importar shapefile {nome}:\n{e}"
                janela.after(0, lambda msg=errormsg: messagebox.showerror("Erro", msg))
        if janela and messagebox:
            resposta, evento = {"val": False}, threading.Event()
            def perguntar():
                resposta["val"] = messagebox.askyesno(
                    "Adicionar Outro Shapefile",
                    "Deseja adicionar outro shapefile de fazenda?",
                    parent=janela
                )
                evento.set()
            janela.after(0, perguntar)
            evento.wait()
            if not resposta["val"]:
                break
        else:
            mais = input("Deseja adicionar outro shapefile? (s/n): ").strip().lower()
            if mais != "s":
                break