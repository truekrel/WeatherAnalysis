# WeatherAnalysis
interractive web application to analyse weather and climate data from capitals around the world
## Features
- Interractive data visualization for various weather parameters
- Includes data for most capital cities of the world for several years
- Responsive and easy-to-use UI
## Quick start

### Local installation
```bash
# Clone the github repository
git clone https://github.com/YourUserName/WeatherAnalysis.git
cd WeatherAnalysis

# Install dependencies 
pip install -r requirements.txt

# Preprocess initial dataset
python preprocessData.py

# Run the application
streamlit run app.py
```
Open in browser: http://0.0.0.0:8501

### Build localy in docker
```bash
# Build
docker build -t WeatherAnalysis .

# Run
docker run -p 8501:8501 WeatherAnalysis
```
## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── preprocessData.py        # Preprocess initial dataset
├── GlobalWeatherRepository.csv    # Initial dataset
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
└── .streamlit/
    └── config.toml        # Streamlit settings
```
## Technologies

- **Python 3.10+**
- **Streamlit** - Web interface
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts

## License

MIT License
