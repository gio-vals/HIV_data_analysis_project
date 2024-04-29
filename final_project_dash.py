import dash
from dash import Dash, html, dcc # components we are going to use
import plotly.express as px
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
import plotly.graph_objects as go



#image_path = "san_fransisco_gay_choir.jpg"
image_path = "https://imgs.classicfm.com/images/243259?crop=16_9&width=660&relax=1&format=webp&signature=Eapm15AinBBggMkZ3_pTd_Lhxws="

image_path1 = './assets/san_fransisco_gay_choir.jpg'
image_path2 = './assets/Python-logo.png'
image_path3 = './assets/pandas-logo.png'
image_path4 = './assets/numpy-logo.png'
image_path5 = './assets/seaborn_logo.png'
image_path6 = './assets/matplotlib_logo.png'
image_path7 = './assets/plotly_logo.png'
image_path8 = './assets/Dash_plotly_logo.png'


# initializing the app
app =dash.Dash()


deaths_new_cases = pd.read_csv("./data/deaths-and-new-cases-of-hiv.csv")
deaths_new_cases.rename(columns={"Deaths - HIV/AIDS - Sex: Both - Age: All Ages (Number)": "Deaths", 
                                 "Incidence - HIV/AIDS - Sex: Both - Age: All Ages (Number)": "Incidence", 
                                 "Prevalence - HIV/AIDS - Sex: Both - Age: All Ages (Number)": "Prevalence"}, 
    inplace=True)
# droping the irrelevant rows
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'African Region (WHO)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Eastern Mediterranean Region (WHO)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'European Region (WHO)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Region of the Americas (WHO)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'South-East Asia Region (WHO)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Western Pacific Region (WHO)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'East Asia & Pacific (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Europe & Central Asia (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Latin America & Caribbean (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Middle East & North Africa (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'North America (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'South Asia (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Sub-Saharan Africa (WB)'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'OECD Countries'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'G20'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'World Bank High Income'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'World Bank Low Income'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'World Bank Lower Middle Income'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'World Bank Upper Middle Income'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'England'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Scotland'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Wales'].index, inplace = True)
deaths_new_cases.drop(deaths_new_cases[deaths_new_cases['Entity']== 'Northern Ireland'].index, inplace = True)
# renaming 'Micronesia (country)' to 'Micronesia'
deaths_new_cases['Entity'] = deaths_new_cases['Entity'].replace({'Micronesia (country)': 'Micronesia'})

# fig1 = px.choropleth(deaths_new_cases, 
#                     locations='Code',
#                     locationmode='ISO-3',
#                     color='Deaths',
#                     hover_name='Entity',
#                     animation_frame='Year',
#                     range_color=(0, 50_000),
#                     #title='HIV-related deaths by country and year',
#                     color_continuous_scale='rdbu_r')
                   
# fig1.layout.width = 1000
# fig1.layout.height = 800
# fig1.update_layout(updatemenus=[dict(type="buttons",
#                                   buttons=[dict(#label="Play",
#                                                 method="animate",
#                                                 args=[None, {"frame": {"duration": 1000}}])])])
# fig1.show()

continents = pd.read_csv("./data/continents.csv", delimiter=';')
continents.rename(columns={'country': 'Entity'}, inplace=True)
deaths_new_cases_continent = continents.merge(deaths_new_cases, on='Entity', how='inner')

fig2 = px.bar(deaths_new_cases_continent, x='Year', y='Deaths', color='continent', barmode='group')

fig2.update_layout(
    #title='Distribution of HIV-related deaths over years by Continent',
    xaxis_title='Year',
    yaxis_title='Deaths'
)

art_averted_deaths = pd.read_csv("./data/hivaids-deaths-and-averted-due-to-art.csv")
art_averted_deaths.rename(columns={"Deaths averted due to ART - estimate": "ART Survivors", 
                                   "AIDS-related deaths - all ages - All ages estimate": "Deaths"}, 
    inplace=True)
art_averted_deaths.rename(columns={'Deaths':'Deaths2', 'ART Survivors': 'ART averted deaths'}, inplace=True)
df_merged = deaths_new_cases.merge(art_averted_deaths, left_on=['Entity','Code', 'Year'], right_on=['Entity','Code', 'Year'], how='outer')
# Specify the countries for the dropdown menu
selected_countries = ['World','Brazil', 'China', 'Colombia', 'Eswatini', 'Ethiopia', 'Germany', 'Indonesia', 'Netherlands', 
                      'Nigeria', 'Malawi', 'Mexico', 'Mozambique','South Africa', 'United Kingdom', 'United States']

# Create a line graph
fig3 = px.line(df_merged[df_merged['Entity'].isin(selected_countries)], 
              x='Year', y=['Incidence', 'Deaths', 'ART averted deaths'], color_discrete_sequence=['darkorange', 'red', 'navy'])

# Update the layout
fig3.update_layout(
    #title='Incidence, Deaths and ART-averted deaths by HIV in years (1990-2019)',
    xaxis_title='Year',
    yaxis_title='Number of affected people',
    updatemenus=[
        dict(
            type="dropdown",
            buttons=list([
                dict(
                    args=[{'y': [df_merged[(df_merged['Entity'] == country)]['Incidence'],
                                 df_merged[(df_merged['Entity'] == country)]['Deaths'], 
                                 df_merged[(df_merged['Entity'] == country)]['ART averted deaths']]}],
                    label=country,
                    method="update"
                )
                for country in selected_countries
            ]),
            active=0,
            x=1.15,  # Adjust the x value for horizontal positioning
            xanchor="left",
            y=1.0,  # Adjust the y value for vertical positioning
            yanchor="bottom"
        ),
    ]
)

art_coverage = pd.read_csv("./data/API_SH.HIV.ARTC.COVERAGE.csv")
art_coverage.drop('2022', axis=1, inplace=True) 
art_coverage_melted = art_coverage.melt(id_vars=['Country','Code'], var_name='Year', value_name='ART_coverage')
art_coverage_melted.sort_values(['Country','Year'], inplace=True)
# Specify the countries for the dropdown menu
selected_countries2 = ['World','Brazil', 'Colombia', 'Eswatini', 'Ethiopia', 'France', 'Indonesia', 'Madagascar', 'Malawi', 
                      'Mexico', 'Netherlands', 'New Zealand', 'Nigeria', 'Pakistan', 'South Africa']

# Create a line graph
fig4 = px.line(art_coverage_melted[art_coverage_melted['Country'].isin(selected_countries2)], 
              x='Year', y=['ART_coverage'], color_discrete_sequence=['navy'])

# Update the layout
fig4.update_layout(
    #title='ART coverage among people living with HIV (%) by Year (2000-2021)',
    xaxis_title='Year',
    yaxis_title='% of affected people',
    updatemenus=[
        dict(
            type="dropdown",
            buttons=list([
                dict(
                    args=[{'y': [art_coverage_melted[(art_coverage_melted['Country'] == country)]['ART_coverage']]}],
                    label=country,
                    method="update"
                )
                for country in selected_countries2
            ]),
            active=0,
            x=1.15,  # Adjust the x value for horizontal positioning
            xanchor="left",
            y=1.0,  # Adjust the y value for vertical positioning
            yanchor="bottom"
        ),
    ]
)
fig4.update_yaxes(range=[0, 100])

prep_tracker = pd.read_excel("./data/prep_tracker.xlsx")
prep_tracker_melted =prep_tracker.melt(id_vars=['Country'], var_name='Year', value_name='PREP usage')
prep_tracker_melted.sort_values(['Country','Year'], inplace=True)
# Specify the countries for the dropdown menu
selected_countries3 = ['World','Brazil', 'Eswatini', 'Ethiopia', 'France', 'Malawi', 
                      'Mexico', 'Netherlands', 'New Zealand', 'Nigeria', 'South Africa', 'United States']

# Create a line graph
fig5 = px.line(prep_tracker_melted[prep_tracker_melted['Country'].isin(selected_countries3)], 
              x='Year', y=['PREP usage'], color_discrete_sequence=['navy'])
# Update the layout
fig5.update_layout(
    #title='Prep usage by Year (2016-2022)',
    xaxis_title='Year',
    yaxis_title='Number of people',
    updatemenus=[
        dict(
            type="dropdown",
            buttons=list([
                dict(
                    args=[{'y': [prep_tracker_melted[(prep_tracker_melted['Country'] == country)]['PREP usage']]}],
                    label=country,
                    method="update"
                )
                for country in selected_countries3
            ]),
            active=0,
            x=1.15,  # Adjust the x value for horizontal positioning
            xanchor="left",
            y=1.0,  # Adjust the y value for vertical positioning
            yanchor="bottom"
        ),
    ]
)

country_restrictions = pd.read_excel('./data/country_restrictions.xlsx', sheet_name='restrictions')
country_restrictions.drop('other', axis=1, inplace=True)
country_restrictions.drop('continent', axis=1, inplace=True)
country_restrictions.rename(columns={'country':'Country'}, inplace=True)

# Define the colors for each category
category_colors = {'yes': 'red', 'no': 'navy', 'unclear': 'orange', 'no data': 'darkgrey'}

# Calculate the value counts and percentages for each column
columns = ['Testing', 'Entry', 'Short_stay', 'Residence', 'Work', 'Deportation']
percentages = {}
for col in columns:
    value_counts = country_restrictions[col].value_counts()
    percentages[col] = value_counts / value_counts.sum() * 100

# Create a stacked bar graph for each column
fig6 = go.Figure()

# Keep track of the legend labels
legend_labels = set()

# Iterate over each column and add a stacked bar graph
for col in columns:
    base_values = [0] * len(percentages[col])
    for category, percentage in percentages[col].items():
        if category not in legend_labels:
            fig6.add_trace(go.Bar(
                x=[col],
                y=[percentage],
                name=category,
                hovertemplate=f'{col}: {category}<br>Percentage: {percentage:.2f}%<extra></extra>',
                base=base_values,
                width=0.6,
                marker_color=category_colors.get(category, 'grey')
            ))
            legend_labels.add(category)
        else:
            fig6.add_trace(go.Bar(
                x=[col],
                y=[percentage],
                showlegend=False,
                hovertemplate=f'{col}: {category}<br>Percentage: {percentage:.2f}%<extra></extra>',
                base=base_values,
                width=0.6,
                marker_color=category_colors.get(category, 'grey')
            ))
        base_values = [base_values[i] + percentage for i in range(len(base_values))]

# Configure the layout
fig6.update_layout(
    #title='Country restrictions in 2023',
    #xaxis=dict(title='Columns'),
    yaxis=dict(title='Percentage (%) of countries', range=[0, 100]),
    barmode='stack',
    showlegend=True
)



# set app layout
app.layout = html.Div([html.Div([
                        html.H1('HIV: Medical or Political Issue?' , style= {"textAlign":"center" , "margin": "35px", "fontSize":"5rem" , "color": "rgb(211,0,0)"}),
                        html.Div([
                             html.H2("Giorgos Valsamakis" , style = {"textAlign":"center" , "margin": "35px", "fontSize":"2.5rem" }),
                         html.H2("Data Analytics Graduation" , style = {"textAlign":"center" , "margin": "35px", "fontSize":"2.5rem" }),
                          html.H2("SPICED Academy" , style = {"textAlign":"center" , "margin": "35px", "fontSize":"2.5rem" }),
                           html.H2("Berlin, 21.06.2023" , style = {"textAlign":"center" , "margin": "35px", "fontSize":"2.5rem" })
                        ])
                        ] ,style={"height":"100vh" , "display":"flex" , "flexDirection":"column" , "justifyContent":"center"}),
                         html.H2("40 100 000" , style = {"display": "flex", "fontSize":"9rem" , "height":"100vh"  , "alignItems":"center" , "justifyContent":"center" , "color": "rgb(211,0,0)"}),
                        html.Div([html.Img(src=image_path1,  style={"margin" : "auto", "display": "block" , "width" : "60%"}),
                        html.P("San Francisco Gay Men's Chorus demonstrating impact of AIDS on the choir - May 1993. Picture: Getty" , style={"textAlign": "center" , "fontWeight":"600"})
                        ] , style = {"height":"100vh"}),
                        # html.Div(children=[
                        # html.H1("HIV-related deaths by country and year", style={"textAlign":"center"}),     
                        # html.Div(dcc.Graph(id='world-map', figure=fig1) , style={"margin-left" : "20%" , "width" : "80%"}) ]),
                        html.Div(children=[
                        html.H1("Distribution of HIV-related deaths over years by continent", style={"textAlign":"center"}),     
                        html.Div(dcc.Graph(id='continents', figure=fig2) , style={"margin" : "auto" , "width" : "80%"}) ], style={"height" : "100vh" , "marginTop" : "300px"}),
                        html.Div(children=[
                        html.H1("Incidence, deaths and ART-averted deaths by HIV in years (1990-2019)", style={"textAlign":"center"}),     
                        html.Div(dcc.Graph(id='first-line-graph', figure=fig3) , style={"margin" : "auto" , "width" : "80%"}) ] ,  style={"height" : "100vh"}),
                        html.Div(children=[
                            html.H2('ART: Anti-Retroviral Treatment' , style ={ "margin": "40px", "fontSize":"2.5rem" , "padding" : "3rem 5rem" }),
                            html.H2('PrEP: Pre-Exposure Prophylaxis' , style ={ "margin": "40px", "fontSize":"2.5rem"  , "padding" : "3rem 5rem"}),
                            html.H2('PEP: Post-Exposure Prophylaxis' , style ={ "margin": "40px", "fontSize":"2.5rem" , "padding" : "3rem 5rem"})
                        ] , style={"height":"100vh" , "display":"flex" , "flexDirection":"column" , "alignItems" : "center"}),
                        html.Div(children=[
                        html.H1("ART coverage among people living with HIV (%) by year (2000-2021)", style={"textAlign":"center"}),     
                        html.Div(dcc.Graph(id='second-line-graph', figure=fig4) , style={"margin" : "auto" , "width" : "80%"}) ] ,style={"height" : "100vh"}),
                        html.Div(children=[
                        html.H1("PrEP usage by year (2016-2022)", style={"textAlign":"center"}),     
                        html.Div(dcc.Graph(id='third-line-graph', figure=fig5) , style={"margin" : "auto" , "width" : "80%"}) ] , style={"height" : "100vh"}),
                        html.Div(children=[
                        html.H1("Country restrictions in 2023", style={"textAlign":"center"}),     
                        html.Div(dcc.Graph(id='100-stack-graph', figure=fig6) , style={"margin" : "auto" , "width" : "80%"}) ] , style={"height" : "100vh"}),
                         html.Div(children=[
                            html.H2("https://www.aidsmemorial.org/interactive-aids-quilt" , style ={ "margin": "35px", "fontSize":"2.5rem"})
                        ] , style={"height":"40vh" , "display":"flex" , "flexDirection":"column", "alignItems" : "center"}),
                        html.Div(children=[
                            html.H2('Data Sources' , style ={ "margin": "35px", "fontSize":"2.5rem"}),
                            html.H3('kaggle.com, link: https://www.kaggle.com/datasets/programmerrdai/hiv-aids' , style ={ "margin": "15px", "fontSize":"1.3rem"}),
                            html.H3('worldbank, link: https://data.worldbank.org/indicator/SH.HIV.ARTC.ZS' , style ={ "margin": "15px", "fontSize":"1.3rem"}),
                            html.H3('prepwatch. link: https://www.prepwatch.org/resources/global-prep-tracker' , style ={ "margin": "15px", "fontSize":"1.3rem"}),
                            html.H3('hivtravel, link: https://www.hivtravel.org' , style ={ "margin": "15px", "fontSize":"1.3rem"})
                            ] , style={"height":"60vh" , "display":"flex" , "flexDirection":"column" , "justifyContent":"center" , "alignItems" : "center"}),
                        html.Div(children=[    
                            html.H2('Libraries' , style ={ "height": "0px", "fontSize":"2.5rem"}),
                            html.Div(children=[
                            html.Img(src=image_path2, style={"width": "100px"}),
                            html.Img(src=image_path3, style={"width": "190px"}),
                            html.Img(src=image_path4, style={"width": "190px"}),
                            html.Img(src=image_path5, style={"width": "190px"}),
                            html.Img(src=image_path6, style={"width": "345px" , "height":"82px"}),
                            html.Img(src=image_path8, style={"width": "200px"})
                            ],  style={"display":"flex" , "justifyContent":"space-evenly", "alignItems":"center" , "width":"100vw"})
                            ], style={"display":"flex", "flexDirection":"column" , "justifyContent":"center", "alignItems":"center"}),
                        html.Div(children=[
                            #html.H3('pandas numpy seaborn matplotlib plotly dash' , style ={ "margin": "15px", "fontSize":"1rem"}),
                            html.H2('Acknowledgements' , style ={ "margin": "35px", "fontSize":"2.5rem"}),
                            html.H3('Mustard Deviations teachers and students' , style ={ "margin": "15px", "fontSize":"1.3rem"})
                        ] , style={"display":"flex" , "flexDirection":"column" , "alignItems":"center" , "margin":"4rem" })      
                        ], style = {"fontFamily" : "math" , "color" : "gray"})


if __name__ == '__main__':
    app.run_server()