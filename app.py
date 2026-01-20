import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Weather Analysis",
    layout="wide"
)
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
#read data
data = pd.read_csv("GlobalWeatherRepositoryRemaped.csv")

#convert relevant time fields to DateTime and TimeDelta
data["Date"] = pd.to_datetime(data["Date"])
data["Sunrise"] = pd.to_datetime(data["Sunrise"])
data["Sunset"] = pd.to_datetime(data["Sunset"])
data["Day length"] = pd.to_datetime(data["Day length"])

#isolate the unique locations
locs = data["Location"].unique()

#configure layot of select fields
locSel, yearSel = st.columns(2)

#create a masked dataset based on selected location and year
LocSelect = locSel.selectbox("Select the location",(locs),placeholder="Select Location")
YearSelect = yearSel.selectbox("Select the year",(2024,2025,2026))
dataMasked = data[(data["Location"]==LocSelect) & (data["Date"].dt.year==YearSelect)]

#Configure the map based on coordinates of selected location
lat = dataMasked["lat"].mean()
lon = dataMasked["lon"].mean()
cords = pd.DataFrame({"lat":[lat],"lon":[lon]})
st.map(cords,zoom=13)

#main tabs
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["Tempearature",
                                         "Precipitation",
                                         "Pressure",
                                         "Wind speed",
                                         "Air quality",
                                         "Other statisitcs"]) 

#temperature
with tab1:
    ##configure the tab layout
    st.title("Temperatrue statistic",text_alignment="center")    
    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)

    ##calculate max/min temperature metric
    Tmin = dataMasked["Absolute temperature"].min()
    Tmax = dataMasked["Absolute temperature"].max()
    col1.metric(label="Highest recorded temperature",value=f"{Tmax}°C",border=True,width="stretch")
    col2.metric(label="Lowest recorded temperature",value=f"{Tmin}°C",border=True,width="stretch")
    
    ##draw daily temperature chart
    col3.title("Daily temperature graph",text_alignment="center")    
    col3.line_chart(dataMasked,x="Date",y=["Absolute temperature","Apparent temperature"],x_label="Date",y_label="Temperature, °C",height=600)

    
    ##average monthly temperature
    #get the months within selected year
    monthsNum = dataMasked["Date"].dt.month.unique()
    #create temporary series to handle mean temperature statistics
    avgTemp = pd.Series(index=monthsNum,dtype=float)
    #iterate over the months and calculate mean temperature within specific month
    for num in monthsNum:
        avgTemp[num] = dataMasked.loc[dataMasked["Date"].dt.month==num,"Absolute temperature"].mean()
    #convert month number to DateTime object by adding selected year
    avgTemp.index = pd.to_datetime(str(YearSelect) +"-"+ avgTemp.index.astype(str),format="%Y-%m")
    #draw the chart
    col4.title("Average monthly temperature graph",text_alignment="center")
    col4.bar_chart(avgTemp,x_label="Month",y_label="Average temperature, °C",height=600)

#precipitation
with tab2:
    ##configure the tab layout
    st.title("Precipitation statistic",text_alignment="center")    
    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)
    ##calculate min/max precipitation metric
    Precipmin = dataMasked["Precipitation"].min()
    Precipmax = dataMasked["Precipitation"].max()
    col1.metric(label="Highest recorded precipitation",value=f"{Precipmax} mm",border=True,width="stretch")
    col2.metric(label="Lowest recorded precipitation",value=f"{Precipmin} mm",border=True,width="stretch")
    ##draw daily precipitation chart
    col3.title("Daily precipitation graph",text_alignment="center")
    col3.line_chart(dataMasked,x="Date",y="Precipitation",x_label="Date",y_label="Precipitation, mm",height=600)
    
    ##average monthly precipitation
    #get the months within selected year
    monthsNum = dataMasked["Date"].dt.month.unique()
    #create temporary series to handle mean precipitation statistics
    avgPrecip = pd.Series(index=monthsNum,dtype=float)
    #iterate over the months and calculate mean precipitation within specific month
    for num in monthsNum:
        avgPrecip[num] = dataMasked.loc[dataMasked["Date"].dt.month==num,"Precipitation"].mean()
    #convert month number to DateTime object by adding selected year
    avgPrecip.index = pd.to_datetime(str(YearSelect) +"-"+ avgPrecip.index.astype(str),format="%Y-%m")
    #draw the chart
    col4.title("Average monthly precipitation graph",text_alignment="center")
    col4.bar_chart(avgPrecip,x_label="Month",y_label="Average precipitation, mm",height=600)

#pressure
with tab3:
    ##configure the tab layout
    st.title("Armospheric pressure statistic",text_alignment="center")    
    #create a toggle to switch between different units of pressure
    unit_toggle = st.toggle("Pressure in kPa")
    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)
    #handle unit switch toggle logic 
    if unit_toggle:
        unit = "kPa"
        pfac = 100
    else:
        unit = "mmHg"
        pfac = 0.75
    #convert pressure from mbar to desired unit of measure
    dataMasked["Pressure"] = dataMasked["Pressure"]*pfac
    ##calculate min/max pressure metric
    Pressmin = dataMasked["Pressure"].min()
    Pressmax = dataMasked["Pressure"].max()
    col1.metric(label="Highest recorded pressure",value=f"{Pressmax} {unit}",border=True,width="stretch")
    col2.metric(label="Lowest recorded pressure",value=f"{Pressmin} {unit}",border=True,width="stretch")
    ##draw daily pressure chart
    col3.title("Daily pressure graph",text_alignment="center")
    col3.line_chart(dataMasked,x="Date",y="Pressure",x_label="Date",y_label=f"Pressure, {unit}",height=600)
    
    ##average monthly pressure
    #get the months within selected year
    monthsNum = dataMasked["Date"].dt.month.unique()
    #create temporary series to handle mean pressure statistics
    avgPress = pd.Series(index=monthsNum,dtype=float)
    #iterate over the months and calculate mean pressure within specific month
    for num in monthsNum:
        avgPress[num] = dataMasked.loc[dataMasked["Date"].dt.month==num,"Pressure"].mean()
    #convert month number to DateTime object by adding selected year
    avgPress.index = pd.to_datetime(str(YearSelect) +"-"+ avgPress.index.astype(str),format="%Y-%m")
    #draw the chart
    col4.title("Average monthly pressure graph",text_alignment="center")
    col4.bar_chart(avgPress,x_label="Month",y_label=f"Average pressure, {unit}",height=600)
#wind speed
with tab4:
    ##configure the tab layout
    st.title("Wind speed statistic",text_alignment="center")    
    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)
    ##calculate min/max wind speed metric
    Windmin = dataMasked["Wind speed"].min()
    Windmax = dataMasked["Wind speed"].max()
    col1.metric(label="Highest recorded wind speed",value=f"{Windmax} km/h",border=True,width="stretch")
    col2.metric(label="Lowest recorded wind speed",value=f"{Windmin} km/h",border=True,width="stretch")
    ##draw daily wind speed chart
    col3.title("Daily wind speed graph",text_alignment="center")
    col3.line_chart(dataMasked,x="Date",y="Wind speed",x_label="Date",y_label="Wind speed, km/h",height=600)
    
    ##average monthly wind speed
    #get the months within selected year
    monthsNum = dataMasked["Date"].dt.month.unique()
    #create temporary series to handle mean pressure statistics
    avgWindV = pd.Series(index=monthsNum,dtype=float)
    #iterate over the months and calculate mean wind speed within specific month
    for num in monthsNum:
        avgWindV[num] = dataMasked.loc[dataMasked["Date"].dt.month==num,"Wind speed"].mean()
    #convert month number to DateTime object by adding selected year
    avgWindV.index = pd.to_datetime(str(YearSelect) +"-"+ avgWindV.index.astype(str),format="%Y-%m")
    #draw the chart
    col4.title("Average monthly wind speed graph",text_alignment="center")
    col4.bar_chart(avgWindV,x_label="Month",y_label="Average wind speed, km/h",height=600)

#air quality index (AQI)
with tab5:
    ##configure the tab layout
    st.title("Air quality statistic",text_alignment="center")    
    #create selection of AQI
    AQindex = st.pills("Select the air quality index",["CO","O3","NO2","SO2","PM2.5","PM10","EPA","DEFRA"],selection_mode="single",default="CO") 
    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)
    #change units of measure based on the selected AQI
    if((AQindex=="EPA") or (AQindex=="DEFRA")):
        AQunit = " "
    else:
        AQunit = " µg/m³"
    
    ##calculate min/max AQI metric
    AQmin = dataMasked[AQindex].min()
    AQmax = dataMasked[AQindex].max()
    col1.metric(label=f"Highest recorded {AQindex} value",value=f"{AQmax}{AQunit}",border=True,width="stretch")
    col2.metric(label=f"Lowest recorded {AQindex} value",value=f"{AQmin}{AQunit}",border=True,width="stretch")
    
    ##draw daily AQI chart
    col3.title("Daily air quality graph",text_alignment="center")
    col3.line_chart(dataMasked,x="Date",y=AQindex,x_label="Date",y_label=f"{AQindex}{AQunit}",height=600)
    
    ##average air quality
    #get the months within selected year
    monthsNum = dataMasked["Date"].dt.month.unique()
    #create temporary series to handle mean pressure statistics
    avgAQ = pd.Series(index=monthsNum,dtype=float)
    #iterate over the months and calculate mean AQI within specific month
    for num in monthsNum:
        avgAQ[num] = dataMasked.loc[dataMasked["Date"].dt.month==num,AQindex].mean()
    #convert month number to DateTime object by adding selected year
    avgAQ.index = pd.to_datetime(str(YearSelect) +"-"+ avgAQ.index.astype(str),format="%Y-%m")
    #draw the chart
    col4.title("Average monthly air quality",text_alignment="center")
    col4.bar_chart(avgAQ,x_label="Month",y_label=f"Average {AQindex}{unit}",height=600)

with tab6:
    ##configure the tablayout
    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)
    
    ##weather condition statistic
    #calculate the distribution of wether conditions via histogramm and draw the chart
    fig1 = px.histogram(dataMasked,x="Weather condition")
    col1.title("Weather conditions",text_alignment="center")
    col1.plotly_chart(fig1,height=600,theme="streamlit")
    
    ##daylegnth
    fig2 = px.line(dataMasked,x="Date",y="Day length",labels={"x":"Date","y":"Day length"})
    #truncate the DateTime to desireble format (HH:MM) and add subticks every 30 minutes
    fig2.update_yaxes(dtick=1000*60*30,tickformat="%H:%M")
    col2.title("Day length",text_alignment="center")
    col2.plotly_chart(fig2,height=600,theme="streamlit")

    ##average wind speed vs direction
    #create a list of the directions
    wDirs = ["N","NNW","NW","WNW","W","WSW","SW","SSW","S","SSE","SE","ESE","E","ENE","NE","NNE"]
    #create temporary dataframe to handle the wind speed statistics
    windStat = pd.DataFrame(columns=["Direction","Count","Mean Speed, km/h"])
    windStat["Direction"] = wDirs
    #iterate over the wind directions and calculate the number of entries within particular direction and corresponidng mean speed
    for wDir in wDirs:
        windStat.loc[windStat["Direction"]==wDir,"Count"] = len(dataMasked[dataMasked["Wind direction"]==wDir])
        windStat.loc[windStat["Direction"]==wDir,"Mean speed, km/h"] = dataMasked.loc[dataMasked["Wind direction"]==wDir,"Wind speed"].mean()
    fig3 = px.bar_polar(windStat,r="Count",theta="Direction",color="Mean speed, km/h",template="plotly_dark",color_discrete_sequence=px.colors.sequential.Plasma_r)
    col3.title("Average wind speed vs wind direction",text_alignment="center")
    col3.plotly_chart(fig3,height=600,theme="streamlit")

    ##UV index
    fig4 = px.line(dataMasked,x="Date",y="UV index")
    col4.title("UV index")
    col4.plotly_chart(fig4,height=600,theme="streamlit")