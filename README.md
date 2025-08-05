# ⚽ Premier League Analytics Dashboard

A comprehensive analytics dashboard for Premier League match data from 2021-2025, built with Streamlit and Plotly.

## 🚀 Features

### 📊 Interactive Dashboard
- **Team Performance Analysis**: Detailed breakdown of wins, draws, losses, and points
- **Performance Progression**: Track points and goal difference over the season
- **Match Results Distribution**: Visual representation of team results
- **xG Analysis**: Expected goals vs expected goals against over time

### 🏠 Home vs Away Performance
- **Venue-based Analysis**: Compare home and away performance
- **Goals by Venue**: Breakdown of goals scored and conceded at home vs away
- **Points by Venue**: Performance metrics split by venue

### 🏆 League Analysis
- **Live League Table**: Current standings with team highlighting
- **Team Comparisons**: Compare multiple teams across various metrics
- **Advanced Analytics**: Possession vs points correlation, formation analysis

### 📋 Match Details
- **Recent Matches**: Detailed view of recent team performances
- **Match Statistics**: Goals, xG, possession, and other key metrics

## 📁 Project Structure

```
Liverpool_2025/
├── final_matches.csv          # Premier League match data (2021-2025)
├── premier_league_analytics.py # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── premier_league.ipynb      # Jupyter notebook with analysis
└── big_game_performance.png  # Generated visualization
```

## 🛠️ Installation

1. **Clone or download the project files**
   ```bash
   # Make sure you have the following files in your directory:
   # - final_matches.csv
   # - premier_league_analytics.py
   # - requirements.txt
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run premier_league_analytics.py
   ```

4. **Open your browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

## 📊 Data Overview

The `final_matches.csv` file contains comprehensive Premier League match data including:

- **Match Information**: Date, time, competition, round, venue
- **Results**: Goals for/against, match result (W/D/L)
- **Advanced Metrics**: Expected goals (xG), expected goals against (xGA), possession
- **Team Details**: Formation, captain, referee
- **Performance Stats**: Shots, shots on target, distance, free kicks, penalties

## 🎯 How to Use

### 1. **Select Season and Team**
   - Use the sidebar to choose a season (2021-2025)
   - Select your team of interest

### 2. **Explore Performance Metrics**
   - View key performance indicators in the metric cards
   - Analyze performance progression over time
   - Compare home vs away performance

### 3. **League Analysis**
   - Check current league standings
   - Compare teams across multiple metrics
   - Analyze correlations between different performance indicators

### 4. **Advanced Insights**
   - Explore formation effectiveness
   - Analyze possession vs points correlation
   - Review recent match details

## 📈 Key Analytics Features

### Performance Tracking
- **Points Progression**: Cumulative points over match weeks
- **Goal Difference**: Net goal difference progression
- **xG Trends**: Expected goals performance over time

### Comparative Analysis
- **Team Comparisons**: Side-by-side team performance
- **League Position**: Current standings with team highlighting
- **Statistical Correlations**: Advanced analytics insights

### Visual Analytics
- **Interactive Charts**: Plotly-powered visualizations
- **Real-time Updates**: Dynamic filtering and selection
- **Professional Styling**: Clean, modern dashboard design

## 🔧 Technical Details

### Built With
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Data Processing
- **Automatic Feature Engineering**: Goal difference, points calculation, rolling averages
- **Data Validation**: Error handling and data quality checks
- **Performance Optimization**: Cached data loading for faster interactions

## 📊 Sample Insights

The dashboard can reveal insights such as:
- Which teams perform better at home vs away
- Correlation between possession and points
- Formation effectiveness for different teams
- Performance trends over multiple seasons
- Key performance indicators for success

## 🚀 Future Enhancements

Potential improvements could include:
- **Player Analysis**: Individual player performance metrics
- **Predictive Modeling**: Match outcome predictions
- **Historical Comparisons**: Season-over-season analysis
- **Export Functionality**: Download reports and visualizations
- **Mobile Optimization**: Responsive design for mobile devices

## 📝 License

This project is for educational and analytical purposes. The data is sourced from publicly available Premier League statistics.

## 🤝 Contributing

Feel free to enhance the dashboard by:
- Adding new visualizations
- Improving the UI/UX
- Adding more analytical features
- Optimizing performance

## 📞 Support

If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Ensure `final_matches.csv` is in the same directory as the Python file
3. Verify you have Python 3.8+ installed

---

**Enjoy exploring Premier League data with this comprehensive analytics dashboard! ⚽📊** 