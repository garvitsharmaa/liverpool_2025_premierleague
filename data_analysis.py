#!/usr/bin/env python3
"""
Premier League Data Analysis Script
Quick analysis and insights from final_matches.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_and_clean_data():
    """Load and preprocess the Premier League data"""
    print("Loading Premier League data...")
    df = pd.read_csv('final_matches.csv')
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Create additional features
    df['goal_difference'] = df['gf'] - df['ga']
    df['points'] = np.where(df['result'] == 'W', 3, np.where(df['result'] == 'D', 1, 0))
    df['match_week'] = df['round'].str.extract(r'(\d+)').astype(int)
    
    print(f"Data loaded successfully! Shape: {df.shape}")
    print(f"Seasons: {sorted(df['season'].unique())}")
    print(f"Teams: {len(df['team'].unique())} teams")
    
    return df

def season_summary(df, season=2025):
    """Generate season summary statistics"""
    print(f"\n{'='*50}")
    print(f"SEASON {season} SUMMARY")
    print(f"{'='*50}")
    
    season_data = df[df['season'] == season]
    
    # League table
    league_table = season_data.groupby('team').agg({
        'points': 'sum',
        'gf': 'sum',
        'ga': 'sum',
        'result': 'count'
    }).reset_index()
    
    league_table['goal_difference'] = league_table['gf'] - league_table['ga']
    league_table = league_table.sort_values(['points', 'goal_difference'], ascending=[False, False])
    league_table['position'] = range(1, len(league_table) + 1)
    
    print("\nTOP 5 TEAMS:")
    print(league_table[['position', 'team', 'points', 'gf', 'ga', 'goal_difference']].head())
    
    print("\nBOTTOM 5 TEAMS:")
    print(league_table[['position', 'team', 'points', 'gf', 'ga', 'goal_difference']].tail())
    
    return league_table

def team_analysis(df, team_name, season=2025):
    """Analyze specific team performance"""
    print(f"\n{'='*50}")
    print(f"{team_name.upper()} ANALYSIS - SEASON {season}")
    print(f"{'='*50}")
    
    team_data = df[(df['team'] == team_name) & (df['season'] == season)]
    
    if len(team_data) == 0:
        print(f"No data found for {team_name} in season {season}")
        return None
    
    # Basic stats
    wins = len(team_data[team_data['result'] == 'W'])
    draws = len(team_data[team_data['result'] == 'D'])
    losses = len(team_data[team_data['result'] == 'L'])
    points = team_data['points'].sum()
    goals_for = team_data['gf'].sum()
    goals_against = team_data['ga'].sum()
    
    print(f"Matches played: {len(team_data)}")
    print(f"Wins: {wins}, Draws: {draws}, Losses: {losses}")
    print(f"Points: {points}")
    print(f"Goals: {goals_for} for, {goals_against} against")
    print(f"Goal difference: {goals_for - goals_against}")
    
    # Home vs Away
    home_data = team_data[team_data['venue'] == 'Home']
    away_data = team_data[team_data['venue'] == 'Away']
    
    print(f"\nHOME PERFORMANCE:")
    print(f"Matches: {len(home_data)}")
    print(f"Points: {home_data['points'].sum()}")
    print(f"Goals: {home_data['gf'].sum()} for, {home_data['ga'].sum()} against")
    
    print(f"\nAWAY PERFORMANCE:")
    print(f"Matches: {len(away_data)}")
    print(f"Points: {away_data['points'].sum()}")
    print(f"Goals: {away_data['gf'].sum()} for, {away_data['ga'].sum()} against")
    
    # xG analysis
    avg_xg = team_data['xg'].mean()
    avg_xga = team_data['xga'].mean()
    print(f"\nEXPECTED GOALS:")
    print(f"Average xG: {avg_xg:.2f}")
    print(f"Average xGA: {avg_xga:.2f}")
    print(f"xG difference: {avg_xg - avg_xga:.2f}")
    
    return team_data

def performance_trends(df, team_name, season=2025):
    """Analyze performance trends over the season"""
    print(f"\n{'='*50}")
    print(f"{team_name.upper()} PERFORMANCE TRENDS - SEASON {season}")
    print(f"{'='*50}")
    
    team_data = df[(df['team'] == team_name) & (df['season'] == season)].sort_values('match_week')
    
    if len(team_data) == 0:
        print(f"No data found for {team_name} in season {season}")
        return
    
    # Points progression
    cumulative_points = team_data['points'].cumsum()
    print("\nPOINTS PROGRESSION:")
    for i, (week, points) in enumerate(zip(team_data['match_week'], cumulative_points)):
        print(f"Week {week}: {points} points")
    
    # Recent form (last 5 matches)
    recent_matches = team_data.tail(5)
    recent_results = recent_matches['result'].tolist()
    recent_points = recent_matches['points'].sum()
    
    print(f"\nRECENT FORM (Last 5 matches):")
    print(f"Results: {' - '.join(recent_results)}")
    print(f"Points: {recent_points}/15")
    
    # Best and worst performances
    best_match = team_data.loc[team_data['goal_difference'].idxmax()]
    worst_match = team_data.loc[team_data['goal_difference'].idxmin()]
    
    print(f"\nBEST PERFORMANCE:")
    print(f"Week {best_match['match_week']}: {best_match['team']} {best_match['gf']}-{best_match['ga']} {best_match['opponent']} ({best_match['venue']})")
    
    print(f"\nWORST PERFORMANCE:")
    print(f"Week {worst_match['match_week']}: {worst_match['team']} {worst_match['gf']}-{worst_match['ga']} {worst_match['opponent']} ({worst_match['venue']})")

def head_to_head_analysis(df, team1, team2, season=2025):
    """Analyze head-to-head performance between two teams"""
    print(f"\n{'='*50}")
    print(f"HEAD-TO-HEAD: {team1.upper()} vs {team2.upper()} - SEASON {season}")
    print(f"{'='*50}")
    
    # Find matches between these teams
    matches = df[
        ((df['team'] == team1) & (df['opponent'] == team2)) |
        ((df['team'] == team2) & (df['opponent'] == team1))
    ]
    
    matches = matches[matches['season'] == season]
    
    if len(matches) == 0:
        print(f"No matches found between {team1} and {team2} in season {season}")
        return
    
    print(f"Matches found: {len(matches)}")
    
    for _, match in matches.iterrows():
        if match['team'] == team1:
            print(f"{match['date'].strftime('%Y-%m-%d')}: {team1} {match['gf']}-{match['ga']} {team2} ({match['venue']})")
        else:
            print(f"{match['date'].strftime('%Y-%m-%d')}: {team2} {match['gf']}-{match['ga']} {team1} ({match['venue']})")

def generate_insights(df):
    """Generate general insights from the data"""
    print(f"\n{'='*50}")
    print("GENERAL INSIGHTS")
    print(f"{'='*50}")
    
    # Most recent season
    latest_season = df['season'].max()
    season_data = df[df['season'] == latest_season]
    
    # Highest scoring team
    highest_scoring = season_data.groupby('team')['gf'].sum().idxmax()
    highest_goals = season_data.groupby('team')['gf'].sum().max()
    
    # Best defensive team
    best_defense = season_data.groupby('team')['ga'].sum().idxmin()
    fewest_goals = season_data.groupby('team')['ga'].sum().min()
    
    # Most possession
    highest_possession = season_data.groupby('team')['poss'].mean().idxmax()
    avg_possession = season_data.groupby('team')['poss'].mean().max()
    
    print(f"Season {latest_season} Insights:")
    print(f"Highest scoring team: {highest_scoring} ({highest_goals} goals)")
    print(f"Best defensive team: {best_defense} ({fewest_goals} goals conceded)")
    print(f"Highest average possession: {highest_possession} ({avg_possession:.1f}%)")
    
    # Home advantage analysis
    home_points = season_data[season_data['venue'] == 'Home']['points'].sum()
    away_points = season_data[season_data['venue'] == 'Away']['points'].sum()
    total_matches = len(season_data)
    
    print(f"\nHome advantage:")
    print(f"Home points: {home_points} ({home_points/total_matches:.1f} per match)")
    print(f"Away points: {away_points} ({away_points/total_matches:.1f} per match)")

def main():
    """Main analysis function"""
    print("⚽ PREMIER LEAGUE DATA ANALYSIS")
    print("="*50)
    
    # Load data
    df = load_and_clean_data()
    
    # Generate insights
    generate_insights(df)
    
    # Season summary
    season_summary(df, 2025)
    
    # Team analysis (example with Arsenal)
    team_analysis(df, 'Arsenal', 2025)
    performance_trends(df, 'Arsenal', 2025)
    
    # Head-to-head analysis
    head_to_head_analysis(df, 'Arsenal', 'Manchester City', 2025)
    
    print(f"\n{'='*50}")
    print("ANALYSIS COMPLETE!")
    print("For interactive dashboard, run: streamlit run premier_league_analytics.py")
    print(f"{'='*50}")

if __name__ == "__main__":
    main() 