🌾 Gerador de KML Agrícola
Uma aplicação simples e eficiente que converte arquivos CSV de coordenadas em arquivos KML prontos para uso em softwares de geolocalização como Google Earth.

Feito com interface gráfica em CustomTkinter, para facilitar o uso no dia a dia do agronegócio!

✨ Funcionalidades
Seleção de pasta contendo arquivos .csv.

Escolha de cultura (Soja, Milho) ou cor personalizada para o polígono.

Processamento automático dos arquivos:

Formatação dos CSVs.

Geração de KMLs individuais.

Criação de um arquivo KML unificado com todos os polígonos.

Interface gráfica amigável.

Barra de progresso e status em tempo real.

Permite editar os nomes das áreas durante o processamento.

Exportação compatível com sistemas de gestão agrícola.

🛠 Tecnologias Utilizadas
Python

CustomTkinter

Pandas

GeoPandas

Shapely

SimpleKML

Colorama

PyProj

📦 Instalação
Clone o repositório ou baixe os arquivos:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/gerador-kml-agricola.git
cd gerador-kml-agricola
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute o programa:

bash
Copiar
Editar
python main.py
🗂 Organização dos Arquivos
Após o processamento, a estrutura dentro da pasta escolhida será:

bash
Copiar
Editar
/SuaPastaSelecionada
    ├── /csv           # CSVs formatados
    ├── /kml           # Arquivos KML individuais
    ├── /shapefiles    # (Reservado para futuras versões)
    ├── todos_poligonos.kml  # KML único com todos os polígonos
📋 Instruções de Uso
Clique em Procurar Pasta e selecione a pasta contendo os arquivos .csv.

Escolha a cultura ou defina uma cor personalizada.

Clique em Iniciar Processamento.

Informe os nomes das áreas conforme solicitado.

Aguarde o processo terminar — seu KML estará pronto!

⚡ Compilar para EXE (Opcional)
Para gerar um executável:

bash
Copiar
Editar
pyinstaller --onefile --add-data "proj;proj" --noconsole main.py
O executável será gerado na pasta /dist.

Ideal para facilitar a distribuição sem necessidade de Python instalado.

🧠 Notas Importantes
Certifique-se que os arquivos .csv tenham o formato correto (ponto, latitude, longitude...).

O aplicativo exige pelo menos 3 pontos válidos para formar um polígono.

Caso o nome da área seja deixado em branco, a área será ignorada.

💬 Contato
Desenvolvido por Warley.
📧 Email: warley.ferraz.wf@gmail.com
📍 LinkedIn: https://www.linkedin.com/in/warley-ferraz-almeida-280a55185/
