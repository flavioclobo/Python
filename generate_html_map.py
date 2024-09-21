import numpy as np
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Criar um DataFrame de exemplo
df = pd.DataFrame({
    'Descrição' : ['Memorial da América Latina', 'Pico do Jaraguá', 'Parque do Ibirapuera', 'Edifício Italia', 'COPAN', 'Teatro Municipal', 'Edifício Martinelli', 'Espaço Alto', 'Edifício Altino Arantes', 'Edifício João Brícola', 'Edifício Matarazzo', 'CCBB', 'MASP', 'Pinacoteca', 'Padaria Santa Tereza', 'Sala São Paulo', 'Museu da Língua Portuguesa', 'Museu do Futebol', 'MAC Museu de Arte Contemporânea'],
    'Endereço' : ['Av. Mário de Andrade, 664 - Barra Funda, São Paulo - SP, 01156-001', 'Estrada Turística do Jaraguá', 'Av. Pedro Álvares Cabral - Vila Mariana, São Paulo', 'Av. Ipiranga, 344 - Centro, São Paulo', 'Av. Ipiranga, 200 - Centro Histórico de São Paulo, São Paulo - SP, 01046-010', 'Praça Ramos de Azevedo, s/n - República, São Paulo', 'Rua Libero Badaró, 504', 'R. Líbero Badaró, 336', 'Rua João Brícola, 24 - Centro - São Paulo', 'Rua João Brícola, 59', 'Viaduto do Chá, 15', 'Rua Álvares Penteado, 112, Sé, São Paulo', 'Av. Paulista, 1578, São Paulo - SP', 'Praça da Luz, 2, São Paulo', 'Praça Dr. João Mendes, 150 - São Paulo - SP, 01501-000', 'Praça Julio Prestes, 16, São Paulo', 'Praça da Luz, s/nº, Centro - São Paulo', 'Praça Charles Miller, S/N, São Paulo', 'Avenida Pedro Álvares Cabral, 1301, São Paulo'],
    'Telefone' : ['(11) 3823-4600', '(11) 3941-2162', '(11) 5574-5045', '(11) 2189-2999', '(11) 3259-5917', '(11) 3053-2100', '(11) 3104-2477', '(11) 91786-6891', '(11) 3249-7466', '(11) 93206-7698', np.nan, '(11) 3113-3651', '(11) 3149-5959', '(11) 3324-1000', '(11) 3111-1030', '(11) 3367-9573', '(11) 3322-0080', '(11) 3664-3848', '(11) 2648-0254'],
    'Website' : ['http://www.memorial.org.br', 'http://www.ambiente.sp.gov.br/parque-estadual-do-jaragua', 'http://www.parquedoibirapuera.com', 'http://www.edificioitalia.com.br', 'http://www.copansp.com.br', 'http://theatromunicipal.org.br', 'http://www.prediomartinelli.com.br', 'https://espacoalto.com', 'prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/se/noticias/?p=41682', 'http://www.ilbarista.com.br', np.nan, 'http://culturabancodobrasil.com.br', 'https://masp.org.br', 'https://pinacoteca.org.br', np.nan, 'https://salasaopaulo.art.br', 'http://www.museudalinguaportuguesa.org.br', 'https://museudofutebol.org.br', 'http://www.mac.usp.br'],
    'Latitude' : ['-23.526783', '-23.456323', '-23.589832', '-23.545417', '-23.546627', '-23.545546', '-23.545334', '-23.546797', '-23.545835', '-23.545302', '-23.547465', '-23.547611', '-23.561641', '-23.534267', '-23.552267', '-23.534159', '-23.535213', '-23.547695', '-23.588997'],
    'Longitude' : ['-46.664289', '-46.766211', '-46.653353', '-46.643458', ' -46.644833', '-46.638770', '-46.635428', ' -46.636327', '-46.634053', '-46.633838', ' -46.637557', '-46.634718', '-46.656188', '-46.633928', ' -46.634926', '-46.640021', '-46.634760', '-46.665137', '-46.650997']
})

# Alterar as colunas latitude e longitude para float
dtype_dict = {'Latitude':'float64', 'Longitude':'float64'}
df = df.astype(dtype_dict)

# Criar um mapa centrado na média das coordenadas
mapa = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12, tiles='OpenStreetMap')

# Adicionar camadas com tipos de mapas diferentes
folium.TileLayer('OpenTopoMap', name='OpenTopoMap').add_to(mapa)
folium.TileLayer('cartodbpositron', name='Positron').add_to(mapa)
folium.TileLayer('cartodbdark_matter', name='Dark').add_to(mapa)
folium.TileLayer('CartoDB Voyager', name='CartoDB Voyager').add_to(mapa)

folium.TileLayer(
    tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
    name='CyclOSM',
    attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    ).add_to(mapa)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
    attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    name='World Imagery'
    ).add_to(mapa)

# Criar agrupamento de marcadores
markerCluster = MarkerCluster(name='Padrão').add_to(mapa)

# Adicionar marcadores ao mapa
for row in df.itertuples():
    folium.Marker(
        location=[row.Latitude, row.Longitude],
        popup=folium.Popup(
            f"{row.Descrição}<br>{row.Endereço}<br>{row.Telefone}<br><a href='{row.Website}'>{row.Website}</a>",
            parse_html=False,
            max_width=200
            ),
        tooltip=row.Descrição,
    ).add_to(markerCluster)

# Adicionando seletor de camadas
folium.LayerControl().add_to(mapa)

# Salvar o mapa como um arquivo HTML
mapa.save("mapa.html")
