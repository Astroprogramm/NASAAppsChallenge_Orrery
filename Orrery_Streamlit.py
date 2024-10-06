import streamlit as st  
import plotly.graph_objects as go
import numpy as np
import base64
from astroquery.jplhorizons import Horizons

st. set_page_config(layout="wide")

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
[data-testid="stAppViewContainer"] > .main {{
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
#background-image: url("data:image/png;base64,{img}");
#background-image: url("https://images.unsplash.com/photo-1641357445458-5540762f0cab?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");

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
# Create a figure with a 3D scatter plot for each planet  
fig = go.Figure()  


# Add each planet's orbit as a line  
for planet, orbit in orbits.items():  
    if planet != 'Sun':
        fig.add_trace(go.Scatter3d(  
            x=orbit()['x'].value,  
            y=orbit()['y'].value,
            z=orbit()['z'].value,
            mode='lines',  
            line=dict(  
                color='blue',  
                width=2  
            ),  
            name=planet + ' Orbit'  
        ))  

# Add each planet's position as a marker  
for planet, orbit in orbits.items(): 
    if planet == 'Sun':
        fig.add_trace(go.Scatter3d(  
        x=[orbit[0]], 
        y=[orbit[1]],
        z=[orbit[2]],
        mode='markers',  
        marker=dict(  
            size=20,  
            color='Orange'  
        ),  
        name=planet  
            ))
    else:
        fig.add_trace(go.Scatter3d(  
            x=[orbit()['x'].value[0]], 
            y=[orbit()['y'].value[0]],
            z=[orbit()['z'].value[0]],
            mode='markers',  
            marker=dict(  
                size=5,  
                color='red'  
            ),  
            name=planet  
        ))
  
# Customize the plot title and axis labels  
fig.update_layout(  
   #title='Solar System 3D Graph',  
    #width=1000,
    height=1000,
   scene=dict(  
    xaxis_title='X',  
    yaxis_title='Y',  
    zaxis_title='Z',
    xaxis = dict(visible=False),
    yaxis = dict(visible=False),
    zaxis =dict(visible=False),
   ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)  

  
# Display the plot in the Streamlit app  
st.plotly_chart(fig,use_container_width = True, filename='transparent-background')

st.write('Photo by <a href="https://unsplash.com/@olenkasergienko?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Olena Bohovyk</a> on <a href="https://unsplash.com/photos/stars-in-the-sky-during-night-time-Cq5NaI0yKBE?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>')