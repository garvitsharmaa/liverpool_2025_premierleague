import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Premier League Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .team-selector {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the Premier League data"""
    try:
        df = pd.read_csv('final_matches.csv')
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date'])
        
        # Create additional features
        df['goal_difference'] = df['gf'] - df['ga']
        df['points'] = np.where(df['result'] == 'W', 3, np.where(df['result'] == 'D', 1, 0))
        df['match_week'] = df['round'].str.extract(r'(\d+)').astype(int)
        df['season_week'] = df['season'].astype(str) + '_' + df['match_week'].astype(str)
        
        # Calculate rolling averages
        df = df.sort_values(['team', 'season', 'match_week'])
        df['rolling_xg_5'] = df.groupby('team')['xg'].rolling(5, min_periods=1).mean().reset_index(0, drop=True)
        df['rolling_xga_5'] = df.groupby('team')['xga'].rolling(5, min_periods=1).mean().reset_index(0, drop=True)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">⚽ Premier League Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Failed to load data. Please check if 'final_matches.csv' is in the current directory.")
        return
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    
    # Season selector
    seasons = sorted(df['season'].unique())
    selected_season = st.sidebar.selectbox("Select Season", seasons, index=len(seasons)-1)
    
    # Team selector
    teams = sorted(df[df['season'] == selected_season]['team'].unique())
    selected_team = st.sidebar.selectbox("Select Team", teams, index=teams.index('Arsenal') if 'Arsenal' in teams else 0)
    
    # Filter data
    season_data = df[df['season'] == selected_season]
    team_data = df[(df['team'] == selected_team) & (df['season'] == selected_season)]
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        wins = len(team_data[team_data['result'] == 'W'])
        st.metric("Wins", wins)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        draws = len(team_data[team_data['result'] == 'D'])
        st.metric("Draws", draws)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        losses = len(team_data[team_data['result'] == 'L'])
        st.metric("Losses", losses)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        points = team_data['points'].sum()
        st.metric("Points", points)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Team Performance Analysis
    st.header(f"📈 {selected_team} Performance Analysis - {selected_season}")
    
    # Performance over time
    col1, col2 = st.columns(2)
    
    with col1:
        # Points progression
        fig_points = go.Figure()
        fig_points.add_trace(go.Scatter(
            x=team_data['match_week'],
            y=team_data['points'].cumsum(),
            mode='lines+markers',
            name='Points',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        fig_points.update_layout(
            title=f'{selected_team} Points Progression',
            xaxis_title='Match Week',
            yaxis_title='Cumulative Points',
            height=400
        )
        st.plotly_chart(fig_points, use_container_width=True)
    
    with col2:
        # Goal difference progression
        fig_gd = go.Figure()
        fig_gd.add_trace(go.Scatter(
            x=team_data['match_week'],
            y=team_data['goal_difference'].cumsum(),
            mode='lines+markers',
            name='Goal Difference',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        ))
        fig_gd.update_layout(
            title=f'{selected_team} Goal Difference Progression',
            xaxis_title='Match Week',
            yaxis_title='Cumulative Goal Difference',
            height=400
        )
        st.plotly_chart(fig_gd, use_container_width=True)
    
    # Match Results and Performance Metrics
    st.subheader("🎯 Match Results and Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Results distribution
        results = team_data['result'].value_counts()
        fig_results = px.pie(
            values=results.values,
            names=results.index,
            title=f'{selected_team} Results Distribution',
            color_discrete_map={'W': '#2ca02c', 'D': '#ff7f0e', 'L': '#d62728'}
        )
        st.plotly_chart(fig_results, use_container_width=True)
    
    with col2:
        # xG vs xGA comparison
        fig_xg = go.Figure()
        fig_xg.add_trace(go.Scatter(
            x=team_data['match_week'],
            y=team_data['xg'],
            mode='lines+markers',
            name='xG',
            line=dict(color='#2ca02c', width=2)
        ))
        fig_xg.add_trace(go.Scatter(
            x=team_data['match_week'],
            y=team_data['xga'],
            mode='lines+markers',
            name='xGA',
            line=dict(color='#d62728', width=2)
        ))
        fig_xg.update_layout(
            title=f'{selected_team} xG vs xGA Over Time',
            xaxis_title='Match Week',
            yaxis_title='Expected Goals',
            height=400
        )
        st.plotly_chart(fig_xg, use_container_width=True)
    
    # Home vs Away Performance
    st.subheader("🏠 Home vs Away Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Home vs Away points
        venue_points = team_data.groupby('venue')['points'].sum()
        fig_venue = px.bar(
            x=venue_points.index,
            y=venue_points.values,
            title=f'{selected_team} Points by Venue',
            color=venue_points.index,
            color_discrete_map={'Home': '#1f77b4', 'Away': '#ff7f0e'}
        )
        st.plotly_chart(fig_venue, use_container_width=True)
    
    with col2:
        # Home vs Away goals
        venue_goals = team_data.groupby('venue')[['gf', 'ga']].sum()
        fig_goals = go.Figure()
        fig_goals.add_trace(go.Bar(
            x=venue_goals.index,
            y=venue_goals['gf'],
            name='Goals For',
            marker_color='#2ca02c'
        ))
        fig_goals.add_trace(go.Bar(
            x=venue_goals.index,
            y=venue_goals['ga'],
            name='Goals Against',
            marker_color='#d62728'
        ))
        fig_goals.update_layout(
            title=f'{selected_team} Goals by Venue',
            xaxis_title='Venue',
            yaxis_title='Goals',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_goals, use_container_width=True)
    
    # League Table and Comparisons
    st.header("🏆 League Analysis")
    
    # League table
    st.subheader("📊 League Table")
    
    # Calculate league table
    league_table = season_data.groupby('team').agg({
        'points': 'sum',
        'gf': 'sum',
        'ga': 'sum',
        'result': 'count'
    }).reset_index()
    
    league_table['goal_difference'] = league_table['gf'] - league_table['ga']
    league_table = league_table.sort_values(['points', 'goal_difference'], ascending=[False, False])
    league_table['position'] = range(1, len(league_table) + 1)
    
    # Highlight selected team
    def highlight_team(row):
        if row['team'] == selected_team:
            return ['background-color: #e8f4fd'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        league_table[['position', 'team', 'points', 'gf', 'ga', 'goal_difference']].style.apply(highlight_team, axis=1),
        use_container_width=True
    )
    
    # Team Comparisons
    st.subheader("🔍 Team Comparisons")
    
    # Select teams to compare
    teams_to_compare = st.multiselect(
        "Select teams to compare",
        teams,
        default=[selected_team, 'Manchester City', 'Liverpool'] if selected_team in ['Manchester City', 'Liverpool'] else [selected_team, 'Manchester City']
    )
    
    if teams_to_compare:
        comparison_data = season_data[season_data['team'].isin(teams_to_compare)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Points comparison
            team_points = comparison_data.groupby('team')['points'].sum().sort_values(ascending=False)
            fig_comp_points = px.bar(
                x=team_points.index,
                y=team_points.values,
                title='Points Comparison',
                color=team_points.index
            )
            st.plotly_chart(fig_comp_points, use_container_width=True)
        
        with col2:
            # xG comparison
            team_xg = comparison_data.groupby('team')['xg'].mean().sort_values(ascending=False)
            fig_comp_xg = px.bar(
                x=team_xg.index,
                y=team_xg.values,
                title='Average xG Comparison',
                color=team_xg.index
            )
            st.plotly_chart(fig_comp_xg, use_container_width=True)
    
    # Advanced Analytics
    st.header("🔬 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Possession vs Points correlation
        possession_points = season_data.groupby('team').agg({
            'poss': 'mean',
            'points': 'sum'
        }).reset_index()
        
        fig_corr = px.scatter(
            possession_points,
            x='poss',
            y='points',
            text='team',
            title='Possession vs Points Correlation',
            trendline="ols"
        )
        fig_corr.update_traces(textposition="top center")
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Formation analysis
        formation_performance = team_data.groupby('formation').agg({
            'points': 'mean',
            'xg': 'mean',
            'xga': 'mean'
        }).reset_index()
        
        if len(formation_performance) > 1:
            fig_formation = px.scatter(
                formation_performance,
                x='xg',
                y='xga',
                size='points',
                text='formation',
                title=f'{selected_team} Formation Performance',
                labels={'xg': 'Average xG', 'xga': 'Average xGA', 'points': 'Average Points'}
            )
            fig_formation.update_traces(textposition="top center")
            st.plotly_chart(fig_formation, use_container_width=True)
    
    # Match Details
    st.header("📋 Match Details")
    
    # Show recent matches
    st.subheader(f"Recent Matches - {selected_team}")
    
    recent_matches = team_data[['date', 'opponent', 'venue', 'result', 'gf', 'ga', 'xg', 'xga', 'poss']].tail(10)
    recent_matches['date'] = recent_matches['date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(recent_matches, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>📊 Premier League Analytics Dashboard | Data from 2021-2025</p>
            <p>Built with Streamlit and Plotly</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 