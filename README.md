# 🌾 Gerador de KML Agrícola

Uma aplicação prática e eficiente que converte arquivos CSV de coordenadas em arquivos KML prontos para uso em softwares de geolocalização como o Google Earth.

Com interface gráfica desenvolvida em **CustomTkinter**, é ideal para facilitar o uso no dia a dia do **agronegócio**!

---

## ✨ Funcionalidades

- Seleção de pastas com arquivos `.csv`.
- Escolha de **cultura** (Soja, Milho) ou definição de **cor personalizada** para os polígonos.
- Processamento automático com:
  - Formatação dos CSVs.
  - Geração de arquivos KML individuais.
  - Criação de um **KML unificado** com todos os polígonos.
- Interface gráfica amigável.
- Barra de progresso e status em tempo real.
- Edição dos nomes das áreas durante o processamento.
- Arquivos compatíveis com sistemas de gestão agrícola.

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

Após o processamento, os arquivos gerados estarão organizados da seguinte forma:

```
/SuaPastaSelecionada
├── /csv           # CSVs formatados
├── /kml           # Arquivos KML individuais
├── /shapefiles    # (Reservado para futuras versões)
└── todos_poligonos.kml  # KML único com todos os polígonos
```

---

## 👨‍🌾 Como Usar

1. Clique em **Procurar Pasta** e selecione a pasta com os arquivos `.csv`.
2. Escolha a **cultura** ou defina uma **cor personalizada**.
3. Clique em **Iniciar Processamento**.
4. Insira os nomes das áreas quando solicitado.
5. Aguarde a finalização — o KML estará pronto!

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
- Mínimo de **3 pontos válidos** é necessário para formar um polígono.
- Se o nome da área for deixado em branco, ela será ignorada.

---

## 💬 Contato

Desenvolvido por **Warley Ferraz**  
📧 Email: [warley.ferraz.wf@gmail.com](mailto:warley.ferraz.wf@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/warley-ferraz-almeida-280a55185/)

---

> _"Facilitando o agro com tecnologia."_ 🚜🌱
