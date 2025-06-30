# 🌾 Gerador de KML Agrícola

Uma aplicação prática e eficiente para converter arquivos CSV de coordenadas em arquivos KML prontos para uso em softwares de geolocalização, como o Google Earth.

Desenvolvida com interface gráfica em **CustomTkinter**, é ideal para facilitar o dia a dia do **agronegócio**!

---

## ✨ Funcionalidades

- Seleção fácil de pastas contendo arquivos `.csv`.
- Escolha rápida de **cultura** (Soja, Milho) ou definição de **cor personalizada** para os polígonos.
- Processamento automático:
  - Formatação e padronização dos CSVs.
  - Geração de arquivos KML individuais para cada área.
  - Criação de um **KML unificado** com todos os polígonos.
- Interface gráfica moderna e intuitiva.
- Barra de progresso e status em tempo real.
- Edição dos nomes das áreas durante o processamento.
- Compatibilidade com sistemas de gestão agrícola.
- **Nova função:** Adicione shapefiles de fazendas diretamente pelo número do recibo do CAR, baixando, convertendo e unificando ao KML final.

---

## 🛠 Tecnologias Utilizadas

- Python 3.10+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pandas](https://pandas.pydata.org/)
- [GeoPandas](https://geopandas.org/)
- [Shapely](https://shapely.readthedocs.io/)
- [SimpleKML](https://simplekml.readthedocs.io/)
- [Colorama](https://pypi.org/project/colorama/)
- [PyProj](https://pyproj4.github.io/pyproj/)
- [Fiona](https://fiona.readthedocs.io/)
- [Requests](https://docs.python-requests.org/)

---

## 📦 Como Instalar

1. Clone o repositório:

   ```bash
   git clone https://github.com/Frraz/Gerador-de-KML.git
   cd Gerador-de-KML
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:

   ```bash
   python main.py
   ```

---

## 🗂 Estrutura de Saída

Após o processamento, os arquivos gerados estarão organizados assim:

```
/SuaPastaSelecionada
├── /csv           # CSVs formatados
├── /kml           # Arquivos KML individuais (incluindo fazendas adicionadas)
├── /shapefiles    # Shapefiles das fazendas baixados e processados
└── todos_poligonos.kml  # KML único com todos os polígonos e fazendas
```

---

## 🖼️ Capturas de Tela

### Tela Principal
![Tela Principal](img/tela_principal.png)

---

## 👨‍🌾 Como Usar

1. Clique em **Procurar Pasta** e selecione a pasta com os arquivos `.csv`.
2. Escolha a **cultura** ou defina uma **cor personalizada**.
3. Clique em **Iniciar Processamento**.
4. Insira os nomes das áreas quando solicitado.
5. Caso deseje, adicione shapefiles de fazendas informando o recibo do CAR e o nome da área.
6. Aguarde a finalização — o KML será gerado automaticamente!

---

## ⚡ Gerar Executável (Opcional)

Para compilar o programa como `.exe` usando o **auto-py-to-exe**:

1. Instale a ferramenta:

   ```bash
   pip install auto-py-to-exe
   ```

2. Execute o programa:

   ```bash
   auto-py-to-exe
   ```

3. Na interface que abrir:
   - Em **Script Location**, selecione o arquivo `main.py`.
   - Marque a opção **One File**.
   - Marque a opção **Window Based (noconsole)**.
   - Em **Additional Files**, adicione a pasta `proj` com:
     ```
     proj → proj
     ```
   - Clique em **Convert .py to .exe**.

> O executável será gerado na pasta `/output` dentro do diretório do projeto.

---

## ⚠️ Observações

- Os arquivos `.csv` devem conter colunas no formato correto (ponto, latitude, longitude...).
- É necessário um mínimo de **3 pontos válidos** para formar um polígono.
- Se o nome da área for deixado em branco, ela será ignorada.
- Para adicionar shapefiles de fazendas, tenha em mãos o número do recibo do CAR conforme orientado na aplicação.

---

## 💬 Contato

Desenvolvido por **Warley Ferraz**  
📧 Email: [warley.ferraz.wf@gmail.com](mailto:warley.ferraz.wf@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/warley-ferraz-almeida-280a55185/)

---

> _"Facilitando o agro com tecnologia."_ 🚜🌱