import streamlit as st  
import plotly.graph_objects as go
import numpy as np
import base64
from astroquery.jplhorizons import Horizons
import datetime
from utils.styles import inject_custom_styles, inject_background_image, inject_side_bar_styles, inject_header_styles

st.set_page_config(layout="wide")


inject_background_image()
inject_custom_styles()
inject_side_bar_styles()
inject_header_styles()



# --- SIDEBAR COMPONENT (LEFT PANEL) ---
with st.sidebar:
    
    # 1. About Section - Kept clean and optional for returning users
    with st.expander("ℹ️ About", expanded=False):
        st.markdown(
            """
            Welcome to **Cosmic Canvas**, a high-precision interactive 3D 
            simulator engineered to explore our Solar System in real-time.
            
            **Key Features:**
            * 🌌 **Dynamic 3D Orbits:** Track and rotate celestial paths in an immersive space.
            * 📅 **Date Ranges:** Displays a 4-year planetary path by default, with complete freedom to customize any timeline you want.
            * 🪐 **Detailed Tooltips:** Hover over any body to uncover scientific descriptions.
            
            *Designed for astronomy enthusiasts, educators, and creators.*
            """
        )

    # Decorative subtitle for branding
    st.markdown(':red[Design Your Cosmic Canvas] ✨')

    # 2. Background Music - Safe attribution layout inside the expander container
    with st.expander("🎵 **Background Music**", expanded=False):
        
        st.markdown(
            """
            <div style="font-size: 11px; line-height: 1.4; color: #A0A0A0;">
                Song: North Edge<br>
                License: Creative Commons (CC BY 3.0) 
                <a href="https://creativecommons.org/licenses/by/3.0" target="_blank">Creative Commons</a> | 
                <a href="https://www.youtube.com/c/keysofmoonmusic" target="_blank">Keys of Moon Music</a><br>
                Music powered by <a href="https://breakingcopyright.com" target="_blank">BreakingCopyright.com</a>
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.audio("Music/North Edge.mp3", format="audio/mp3", loop=True, autoplay=True)


    # 3. Time Range Controls - Highly active component kept open by default
    with st.expander("📅 Time range", expanded=True):
        hoy = datetime.date.today()
        hace_cuatro_anos = hoy - datetime.timedelta(days=1461)

        start_date = st.date_input(':orange[Start date first]', hace_cuatro_anos, min_value=datetime.date(1800, 1, 1))
        end_date = st.date_input(':orange[End date]', hoy)
        st.text(' ')

    # 4. Visualization Controls - Fully organized layout for screen customization
    with st.expander("🌌 Model Visualization", expanded=True):
        multiplier = st.slider(":orange[Change the size of the celestial bodies:]", 1, 20, 1)
        st.write(':red[Other options:]')
        st.checkbox(':orange[View real sizes]', key='real_sizes')
        st.checkbox(':orange[Toggle labels (on/off)]', key='labels')
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
    st.markdown('<h1 class="main-title">Welcome to SkySphere ✨</h1>', unsafe_allow_html=True)




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
# Colors adjusted for high visibility over a dark space background, 
# maintaining their realistic composition-based appearance.
colors = [
    '#FF8C00',  # Sun (Bright, glowing orange)
    '#D3D3D3',  # Mercury (Reflective light gray)
    '#E6A15C',  # Venus (Light sulfuric gold)
    '#4A90E2',  # Earth (Bright, vibrant sky blue)
    '#FF4D4D',  # Mars (Glowing oxidized red)
    '#E5A65D',  # Jupiter (Saturated gas cream/tan)
    '#EAD39F',  # Saturn (Luminous sandy ring beige)
    '#70F3FF',  # Uranus (Neon icy cyan)
    '#3366FF',  # Neptune (Electric methane blue)
    '#FFFFE0',  # Pluto (Yellowish-white frozen nitrogen)
    '#F4A460',  # Quaoar (Light reflective rock brown)
    '#FFE4C4',  # Haumea (Bright crystalline ice bisque)
    '#FFF8DC'   # Makemake (Pale frozen methane cornsilk)
]


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
    'Sun': 'The Sun is the star at the heart of our solar system.<br>Its gravity holds the solar system together, keeping everything<br>-from the biggest planets to the smallest bits of debris — in its orbit.',
    
    'Mercury': '''Mercury is the smallest planet in our solar system and the nearest to the Sun.<br>
Mercury is only slightly larger than Earth's Moon. Its surface is covered in tens of thousands of impact craters.<br>
Despite its proximity to the Sun, Mercury is not the hottest planet in our solar system - that title belongs to nearby Venus, thanks to its dense atmosphere.<br>
But Mercury is the fastest planet, zipping around the Sun every 88 Earth days.''',
            
    'Venus': "Venus is the second planet from the Sun,<br>and Earth's closest planetary neighbor.<br>Venus is the third brightest object in the sky<br>after the Sun and Moon.<br>Venus spins slowly in the opposite direction from most planets.<br>Venus is similar in structure and size to Earth,<br>and is sometimes called Earth's evil twin.",
            
    'Earth': '''Earth is our home planet and the only place in the universe<br>known to harbor active life.<br>
It is the third planet from the Sun and the densest in the solar system.<br>
About 71% of Earth's surface is covered by vast liquid water oceans,<br>
earning it the famous nickname: the Blue Marble.''',
            
    'Mars': '''Mars is the fourth planet from the Sun and a cold, desert world.<br>
It is known as the Red Planet due to iron minerals rusting in its soil.<br>
Mars features giant extinct volcanoes like Olympus Mons, the largest in the system,<br>
and shows clear signs of having liquid water flowing billions of years ago.''',
            
    'Jupiter': '''Jupiter is the king of our solar system and its largest planet by far.<br>
This giant gas world is more than twice as massive as all the other planets combined.<br>
It is famous for its colorful bands of gas and the iconic Great Red Spot,<br>
a massive cosmic storm wider than Earth that has raged for hundreds of years.''',
            
    'Saturn': '''Saturn is the sixth planet from the Sun and the second-largest gas giant.<br>
While other planets have rings, none are as spectacular or complex as Saturn's.<br>
Its massive ring system is made of billions of chunks of ice and rock dust,<br>
and the planet itself is so light that it could float if put in a giant bathtub.''',
            
    'Uranus': '''Uranus is the seventh planet from the Sun and an icy, frozen world.<br>
It has a unique, beautiful pale cyan color caused by methane gas in its skies.<br>
Uranus is completely unique because it rotates completely on its side,<br>
rolling around the Sun like a football instead of spinning like a top.''',
            
    'Neptune': '''Neptune is the eighth and most distant major planet orbiting our Sun.<br>
It is a dark, cold ice giant swept by supersonic frozen winds up to 2,100 km/h.<br>
Neptune was the very first planet in history to be discovered using mathematical<br>
calculations before anyone actually saw it through a telescope.''',
            
    'Pluto': '''Pluto is the most famous dwarf planet located in the distant Kuiper Belt.<br>
Once considered the ninth planet, it is a complex world of rock and ice.<br>
Its most striking feature is a massive, bright glacier made of frozen nitrogen<br>
that forms a giant, beautiful heart shape on its frozen surface.''',
            
    'Quaoar': '''Quaoar is a mysterious dwarf planet candidate orbiting in the deep outer solar system.<br>
It is a dense world of ice and rock roughly half the size of Pluto.<br>
Quaoar baffled scientists when they discovered it is surrounded by a tight ring system<br>
located much farther away from its surface than physics laws say should be possible.''',
            
    'Haumea': '''Haumea is a fast-spinning dwarf planet located way past Neptune's orbit.<br>
It rotates so incredibly fast (once every 4 hours) that the extreme centrifugal force<br>
has distorted its shape, stretching it out into an elongated shape like a football.<br>
It is covered in pure crystalline ice and has two small companion moons.''',
            
    'Makemake': '''Makemake is the second-brightest dwarf planet out in the frozen Kuiper Belt.<br>
It takes Makemake about 305 Earth years to complete just one single orbit around the Sun.<br>
Its freezing surface is covered in ultra-pure, reflective frozen methane and ethane,<br>
giving it a distinct, bright pálido look against the darkness of deep space.'''
}



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
            
            hovertemplate=f'''<b> </b><br>{Descriptions[planet]}<br>''',
            showlegend=False
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
    height=750,
    margin=dict(l=0, r=0, t=0, b=0),
        
    # --- UX-OPTIMIZED LEGEND WITH AN INTERACTIVE TITLE ---
    legend=dict(
        title_text="🪐 Celestial Bodies", # Header displayed directly above the planet list
        title_font_color="#FFB03B",        # Golden accent tone for the legend header hierarchy
        title_font_size=20,                # Slightly larger font size for the group title
        font=dict(color="white", size=12), # High-contrast white font for individual planet items

        # Centering configuration on the vertical axis
        yanchor="middle",                  # Anchors the pivot point to the middle of the legend box
        y=0.5,                             # Positions the pivot exactly at 50% of the graph height
        
        xanchor="left",                         
        x=1.02                             # Seamlessly anchors the legend module to the right side
    ),
    
    scene=dict(  
    xaxis_title='X',  
    yaxis_title='Y',  
    zaxis_title='Z',
    xaxis = dict(visible=False),
    yaxis = dict(visible=False),
    zaxis =dict(visible=False),

    camera=dict(
            # 'eye' controls the camera distance (lower numbers = closer zoom)
            eye=dict(x=0.85, y=0.85, z=0.85),
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0)
        ),
        #aspectmode='cube' # Ensures identical scaling proportions across all 3 axes
    ),

    paper_bgcolor='rgba(0,0,0,0.3)',
    plot_bgcolor='rgba(0,0,0,0.3)',
    font=dict(
    family="Arial",
    size=15,
    color="white"
    ),
    legend_font_size=18
)  

st.plotly_chart(fig,  width='stretch')


