import streamlit as st  
import plotly.graph_objects as go
import numpy as np
import base64
from astroquery.jplhorizons import Horizons
import time

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

#st.markdown(f"""
#<audio src="http://localhost:8501/media/a318c54acdc8fc15e8c9d8b88543ed17be024d690c61c9d1c0819043.mp3" controls autoplay loop width="20%">
#  Your browser does not support the audio element.
#</audio>
#""", unsafe_allow_html=True)


#Dates
Dates_short = {'start': '2020-01-01',
               'stop' : '2022-01-01',
               'step': '10d'}
Dates_long = {'start': '1750-01-01',
               'stop' : '2099-01-01',
               'step' :'30d'}

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
Quaoar = Horizons(id= 'Quaoar',location="@0",epochs= Dates_long)
Haumea = Horizons(id='Haumea',location="@0",epochs= Dates_long)
Makemake = Horizons(id='Makemake',location="@0",epochs= Dates_long)

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



with st.sidebar:

    st.title('Customize the plot!:')

    st.checkbox('View real sizes', key='real_sizes')
    st.checkbox('Toogle labels', key='labels')


st.title('Welcome to the interactive Orrery!')
st.subheader('Discover the wonders of our Solar System through this engaging interactive virtual model, where you can uncover intriguing details about each celestial body!')
#Sizes:
if not st.session_state.real_sizes:
    Sizes = np.array([140000, 4879,12104,12756,6792,142984,120536,51118,49528,2376])/10000
else:
    Sizes = np.array([1400000, 4879,12104,12756,6792,142984,120536,51118,49528,2376])/149597871

if not st.session_state.labels:
    mode_plot = 'lines+markers+text'
else:
    mode_plot = 'markers'

#Colors:
colors = ['orange','#a9a9a9', '#966919', 'darkblue', 'red', '#D27D2D','#C19A6B','cyan','blue']

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
            name=planet + ' Orbit'  
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
        text='Sun'
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
        ))
        counter+=1
  
# Customize the plot title and axis labels  
fig.update_layout(  
   #title='Solar System 3D Graph',  
    #width=1000,
    height=1100,
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

  
# Display the plot in the Streamlit app  
st.plotly_chart(fig, filename='transparent-background')


st.audio("Music/North Edge.mp3", format="audio/mp3", loop=True, autoplay=True,)
st.write('''Song: North Edge
License: Creative Commons (CC BY 3.0) https://creativecommons.org/licenses/by/3.0
https://www.youtube.com/c/keysofmoonmusic
Music powered by BreakingCopyright: https://breakingcopyright.com''')