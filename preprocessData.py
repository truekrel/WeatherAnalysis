import pandas as pd
#Read unprocessed data
dataInit = pd.read_csv("GlobalWeatherRepository.csv")

#Convert relevant time fields to DateTime
dataInit["sunrise"] = pd.to_datetime(dataInit["sunrise"])
dataInit["sunset"] = pd.to_datetime(dataInit["sunset"])

#Remap the data frame 
dataRemap = pd.DataFrame(data={"Date": dataInit["last_updated"],
                          "Location": dataInit["location_name"],
                          "lat": dataInit["latitude"],
                          "lon": dataInit["longitude"],
                          "Absolute temperature": dataInit["temperature_celsius"],
                          "Apparent temperature": dataInit["feels_like_celsius"],
                          "Precipitation": dataInit["precip_mm"],
                          "Pressure": dataInit["pressure_mb"],
                          "Wind speed": dataInit["wind_kph"],
                          "Wind direction": dataInit["wind_direction"],
                          "CO":dataInit["air_quality_Carbon_Monoxide"],
                          "O3":dataInit["air_quality_Ozone"],
                          "NO2":dataInit["air_quality_Nitrogen_dioxide"],
                          "SO2":dataInit["air_quality_Sulphur_dioxide"],
                          "PM2.5":dataInit["air_quality_PM2.5"],
                          "PM10":dataInit["air_quality_PM10"],
                          "EPA":dataInit["air_quality_us-epa-index"],
                          "DEFRA":dataInit["air_quality_gb-defra-index"],
                          "Sunrise":dataInit["sunrise"],
                          "Sunset":dataInit["sunset"],
                          "Day length": dataInit["sunset"] - dataInit["sunrise"],
                          "Weather condition":dataInit["condition_text"],
                          "UV index":dataInit["uv_index"]
                          })
#Rewrite day length as DateTime instead of TimeStamp64 since plotly does not support the latter
#This is done by adding a "throwaway" date such as 1970/01/01 to the TimeStamp
#This date is later truncated to HH:MM format directly in the plotly axis handler (see line 234 in app.py)
dataRemap["Day length"] = dataRemap["Day length"] + pd.to_datetime('1970/01/01')

#Save the preprocessed data
dataRemap.to_csv("GlobalWeatherRepositoryRemaped.csv")