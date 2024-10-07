import streamlit as st  
import plotly.graph_objects as go
import numpy as np
import base64
from astroquery.jplhorizons import Horizons
import datetime

st.set_page_config(layout="wide")

# Load background image
background_image_path = "Images/JWT_star_formation.jpg"
import base64

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64(background_image_path)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


with st.sidebar:

    st.subheader(':red[Design Your Cosmic Canvas] ✨')

    start_date = st.date_input(':orange[Start date first]', datetime.date(2020, 1, 1), min_value=datetime.date(1800,1,1))
    end_date = st.date_input(':orange[End date]', datetime.date(2024, 1, 1))
    st.text(' ')

    st.write('')
    multiplier = st.slider(":orange[Change the size of the celestial bodies:]", 1, 20, 1)
    st.write(':red[Other options:]')
    st.checkbox(':orange[View real sizes]', key='real_sizes')
    st.checkbox(':orange[Toogle labels (on/off)]', key='labels')
    st.write('')

#Dates
Dates_short = {'start': str(start_date),
               'stop' : str(end_date),
               'step': '10d'}

Dates_long = {'start': '1801-01-01',
               'stop' : '2029-01-01',
               'step' :'30d'}
Dates_long_2000s = {'start': '2001-01-01',
               'stop' : '2029-01-01',
               'step' :'30d'}
#------------Loading Data:--------------
#Planets
Mercury = Horizons(id=199,location="@0",epochs= Dates_short)
Venus = Horizons(id=299,location="@0",epochs= Dates_short)
Earth = Horizons(id=399,location="@0",epochs= Dates_short)
Mars = Horizons(id=499,location="@0",epochs= Dates_short)
Jupiter = Horizons(id=599,location="@0",epochs= Dates_long)
Saturn = Horizons(id=699,location="@0",epochs= Dates_long)
Uranus = Horizons(id=799,location="@0",epochs= Dates_long)
Neptune = Horizons(id=899,location="@0",epochs= Dates_long)

#Small bodies
Pluto = Horizons(id=999,location="@0",epochs= Dates_long)
Quaoar = Horizons(id= 'Quaoar I',location="@0",epochs= Dates_long_2000s)
Haumea = Horizons(id='Haumea (system barycenter)',location="@0",epochs= Dates_long_2000s)
Makemake = Horizons(id='Makemake',location="@0",epochs= Dates_long_2000s)

#Planets
Mercury_vec = Mercury.vectors
Venus_vec = Venus.vectors
Earth_vec = Earth.vectors
Mars_vec = Mars.vectors
Jupiter_vec = Jupiter.vectors
Saturn_vec = Saturn.vectors
Uranus_vec = Uranus.vectors
Neptune_vec = Neptune.vectors

#Small bodies
Pluto_vec = Pluto.vectors
Quaoar_vec = Quaoar.vectors
Haumea_vec = Haumea.vectors
Makemake_vec = Makemake.vectors


#------------ App --------------


cols= st.columns([0.6,0.05,0.45])
with cols[0]:
    st.title(':red[Welcome to SkySphere!]')
    st.markdown('''<div>
                <span style="font-size: 22px; font-weight: bold">About</span>
                </div>''', unsafe_allow_html=True)
    st.markdown('''<div>
                <span style="font-size: 20px;">Discover the wonders of our Solar System through
                this engaging interactive virtual model, where you can uncover 
                intriguing details about each celestial body!</span>
                </div>''', unsafe_allow_html=True)


with cols[2]:
    st.title(' ')
    st.text(' ')
    st.audio("Music/North Edge.mp3", format="audio/mp3", loop=True, autoplay=True,)
    st.markdown('''<div>
            <span style="font-size: 12px;">Song: North Edge
    License: Creative Commons (CC BY 3.0) <a href="https://creativecommons.org/licenses/by/3.0">Creative commons</a>
    <a href="https://www.youtube.com/c/keysofmoonmusic">keysofmoonmusic</a>
    Music powered by BreakingCopyright: <a href="https://breakingcopyright.com">Breakingcopyright.com<a/></span>
            </div>''', unsafe_allow_html=True)


#Sizes:
if not st.session_state.real_sizes:
    Sizes = np.array([190000, 4879,12104,12756,6792,142984,120536,51118,49528,2376,1188*2,1100,1740,1434])*multiplier/20000
else:
    Sizes = np.array([1400000, 4879,12104,12756,6792,142984,120536,51118,49528,2376,1188*2,1100,1740,1434])/149597871

if not st.session_state.labels:
    mode_plot = 'lines+markers+text'
else:
    mode_plot = 'markers'

#Colors:
colors = ['orange','#a9a9a9', '#966919', 'darkblue', 'red', '#D27D2D','#C19A6B','cyan','blue','#f5f5dc','#deb887','#ffe4c4','#fffacd']

Sizes = Sizes.tolist()
orbits = {'Sun':[0,0,0],
    'Mercury': Mercury_vec,
            'Venus' : Venus_vec,
            'Earth' : Earth_vec,
            'Mars' : Mars_vec,
            'Jupiter' : Jupiter_vec,
            'Saturn' : Saturn_vec,
            'Uranus' : Uranus_vec,
            'Neptune' : Neptune_vec,
            'Pluto':Pluto_vec,
            'Quaoar':Quaoar_vec,
            'Haumea':Haumea_vec,
            'Makemake':Makemake_vec,
             }
Descriptions = {
            'Sun':'The Sun is the star at the heart of our solar system.<br>Its gravity holds the solar system together, keeping everything<br>-from the biggest planets to the smallest bits of debris — in its orbit.',
            'Mercury': '''Mercury is the smallest planet in our solar system and the nearest to the Sun.<br>
Mercury is only slightly larger than Earth's Moon. Its surface is covered in tens of thousands of impact craters.<br>
Despite its proximity to the Sun, Mercury is not the hottest planet in our solar system - that title belongs to nearby Venus, thanks to its dense atmosphere.<br>
But Mercury is the fastest planet, zipping around the Sun every 88 Earth days.''',
            'Venus' : "Venus is the second planet from the Sun,<br>and Earth's closest planetary neighbor.<br>Venus is the third brightest object in the sky<br>after the Sun and Moon.<br>Venus spins slowly in the opposite direction from most planets.<br>Venus is similar in structure and size to Earth,<br>and is sometimes called Earth's evil twin.",
            'Earth' : '',
            'Mars' : '',
            'Jupiter' : '',
            'Saturn' : '',
            'Uranus' : '',
            'Neptune' : '',
            'Pluto':'',
            'Quaoar':'',
            'Haumea':'',
            'Makemake':'',

}
#with st.empty():
#    for seconds in range(1):
#        with st.spinner("Loading..."):
#            time.sleep(5)

# Create a figure with a 3D scatter plot for each planet  
fig = go.Figure()  

counter=1
# Add each planet's orbit as a line  
for planet, orbit in orbits.items(): 
    
    if planet != 'Sun':
        fig.add_trace(go.Scatter3d(  
            x=orbit()['x'].value,  
            y=orbit()['y'].value,
            z=orbit()['z'].value,
            mode='lines',  
            line=dict(  
                color=colors[counter],  
                width=2  
            ),  
            name=planet + ' Orbit',
            
            hovertemplate=    ' ',

        ))  
        counter+=1

counter = 0
# Add each planet's position as a marker  
for planet, orbit in orbits.items(): 
    if planet == 'Sun':
        fig.add_trace(go.Scatter3d(  
        x=[orbit[0]], 
        y=[orbit[1]],
        z=[orbit[2]],
        mode=mode_plot, 
        marker=dict(  
            size=Sizes[counter],  
            color=colors[counter]
        ),  
        name=planet,
        text='Sun',
        hovertemplate=    ' ',
            ))
        counter+=1
    else:
        fig.add_trace(go.Scatter3d(  
            x=[orbit()['x'].value[0]], 
            y=[orbit()['y'].value[0]],
            z=[orbit()['z'].value[0]],
            mode=mode_plot, 
            marker=dict(  
                size=Sizes[counter],  
                color=colors[counter]  
            ),  
            name=planet,
            text=planet,            
            hovertemplate=f'''<b> </b><br>{Descriptions[planet]}<br>'''

            
        ))
        counter+=1
  
# Customize the plot title and axis labels  
fig.update_layout(  
   #title='Solar System 3D Graph',  
    #width=1000,
    height=1200,
   scene=dict(  
    xaxis_title='X',  
    yaxis_title='Y',  
    zaxis_title='Z',
    xaxis = dict(visible=False),
    yaxis = dict(visible=False),
    zaxis =dict(visible=False),
   ),
    paper_bgcolor='rgba(0,0,0,0.3)',
    plot_bgcolor='rgba(0,0,0,0.3)',
    font=dict(
    family="Arial",
    size=15,
    color="white"
    ),
    legend_font_size=20
)  

st.plotly_chart(fig, filename='transparent-background')