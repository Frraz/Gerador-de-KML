# 🌾 Gerador de KML Agrícola

Uma aplicação simples e eficiente que converte arquivos CSV de coordenadas em arquivos KML prontos para uso em softwares de geolocalização como Google Earth.

Feito com interface gráfica em **CustomTkinter**, para facilitar o uso no dia a dia do agronegócio!

---

## ✨ Funcionalidades

- Seleção de pasta contendo arquivos `.csv`.
- Escolha de **cultura** (Soja, Milho) ou **cor personalizada** para o polígono.
- Processamento automático dos arquivos:
  - Formatação dos CSVs.
  - Geração de KMLs individuais.
  - Criação de um arquivo **KML unificado** com todos os polígonos.
- Interface gráfica amigável.
- Barra de progresso e status em tempo real.
- Permite editar os nomes das áreas durante o processamento.
- Exportação compatível com sistemas de gestão agrícola.

---

## 🛠 Tecnologias Utilizadas

- Python
- CustomTkinter
- Pandas
- GeoPandas
- Shapely
- SimpleKML
- Colorama
- PyProj

---

## 📦 Instalação

1. Clone o repositório ou baixe os arquivos:

```bash
git clone https://github.com/seu-usuario/gerador-kml-agricola.git
cd gerador-kml-agricola
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o programa:

```bash
python main.py
```

---

## 🗂 Organização dos Arquivos

Após o processamento, a estrutura dentro da pasta escolhida será:

```
/SuaPastaSelecionada
    ├── /csv           # CSVs formatados
    ├── /kml           # Arquivos KML individuais
    ├── /shapefiles    # (Reservado para futuras versões)
    └── todos_poligonos.kml  # KML único com todos os polígonos
```

---

## 👋 Instruções de Uso

1. Clique em **Procurar Pasta** e selecione a pasta contendo os arquivos `.csv`.
2. Escolha a **cultura** ou defina uma **cor personalizada**.
3. Clique em **Iniciar Processamento**.
4. Informe os nomes das áreas conforme solicitado.
5. Aguarde o processo terminar — seu KML estará pronto!

---

## ⚡ Compilar para EXE (Opcional)

Para gerar um executável:

```bash
pyinstaller --onefile --add-data "proj;proj" --noconsole main.py
```

- O executável será gerado na pasta `/dist`.
- Ideal para facilitar a distribuição sem necessidade de Python instalado.

---

## 🧐 Notas Importantes

- Certifique-se que os arquivos `.csv` tenham o formato correto (ponto, latitude, longitude...).
- O aplicativo exige pelo menos 3 pontos válidos para formar um polígono.
- Caso o nome da área seja deixado em branco, a área será ignorada.

---

## 💬 Contato

Desenvolvido por Warley.  
📧 Email: warley.ferraz.wf@gmail.com
📍 LinkedIn: https://www.linkedin.com/in/warley-ferraz-almeida-280a55185/

---

> "Facilitando o agro com tecnologia." 🚜🌱

