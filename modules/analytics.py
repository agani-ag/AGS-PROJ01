"""
Analytics Module
Handles data analysis and visualization for evaluation results
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List, Tuple
import streamlit as st

# Set matplotlib to use a non-interactive backend
matplotlib.use('Agg')


class AnalyticsEngine:
    """
    Class to handle analytics and visualization
    """
    
    def __init__(self):
        """Initialize the analytics engine"""
        pass
    
    def calculate_session_analytics(self, session_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate analytics for all questions in a session
        
        Args:
            session_data: DataFrame with session evaluation data
        
        Returns:
            DataFrame with analytics per question
        """
        if len(session_data) == 0:
            return pd.DataFrame()
        
        analytics = []
        
        # Group by question
        for question in session_data['question'].unique():
            question_data = session_data[session_data['question'] == question].sort_values('attempt_no')
            
            if len(question_data) == 0:
                continue
            
            # Get first and last attempts
            first_attempt = question_data.iloc[0]
            last_attempt = question_data.iloc[-1]
            
            # Count missing concepts
            first_errors = len([x for x in str(first_attempt['missing_concepts']).split(' | ') if x.strip()])
            last_errors = len([x for x in str(last_attempt['missing_concepts']).split(' | ') if x.strip()])
            
            # Calculate metrics
            first_score = first_attempt['score']
            last_score = last_attempt['score']
            improvement = last_score - first_score
            learning_gain_pct = (improvement / 10) * 100
            error_reduction = first_errors - last_errors
            
            analytics.append({
                'question': question[:50] + '...' if len(question) > 50 else question,
                'first_score': first_score,
                'last_score': last_score,
                'improvement': improvement,
                'learning_gain_%': round(learning_gain_pct, 2),
                'first_errors': first_errors,
                'last_errors': last_errors,
                'error_reduction': error_reduction,
                'total_attempts': len(question_data)
            })
        
        return pd.DataFrame(analytics)
    
    def calculate_overall_metrics(self, analytics_df: pd.DataFrame) -> Dict:
        """
        Calculate overall metrics across all questions
        
        Args:
            analytics_df: DataFrame with per-question analytics
        
        Returns:
            Dictionary with overall metrics
        """
        if len(analytics_df) == 0:
            return {
                'avg_improvement_points': 0,
                'avg_improvement_pct': 0,
                'avg_learning_gain_pct': 0,
                'avg_error_reduction': 0,
                'total_questions': 0
            }
        
        return {
            'avg_improvement_points': round(analytics_df['improvement'].mean(), 2),
            'avg_improvement_pct': round((analytics_df['improvement'].mean() / 10) * 100, 2),
            'avg_learning_gain_pct': round(analytics_df['learning_gain_%'].mean(), 2),
            'avg_error_reduction': round(analytics_df['error_reduction'].mean(), 2),
            'total_questions': len(analytics_df)
        }
    
    def create_score_comparison_chart(self, analytics_df: pd.DataFrame) -> plt.Figure:
        """
        Create a bar chart comparing first and last scores
        
        Args:
            analytics_df: DataFrame with analytics data
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(analytics_df) == 0:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return fig
        
        x = range(len(analytics_df))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], analytics_df['first_score'], 
               width, label='First Attempt', color='#ff6b6b')
        ax.bar([i + width/2 for i in x], analytics_df['last_score'], 
               width, label='Last Attempt', color='#51cf66')
        
        ax.set_xlabel('Question')
        ax.set_ylabel('Score (out of 10)')
        ax.set_title('Before vs After Score Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels([f'Q{i+1}' for i in x])
        ax.legend()
        ax.set_ylim(0, 10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_learning_gain_chart(self, analytics_df: pd.DataFrame) -> plt.Figure:
        """
        Create a bar chart showing learning gain per question
        
        Args:
            analytics_df: DataFrame with analytics data
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(analytics_df) == 0:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return fig
        
        colors = ['#51cf66' if x >= 0 else '#ff6b6b' for x in analytics_df['improvement']]
        
        ax.bar(range(len(analytics_df)), analytics_df['improvement'], color=colors)
        
        ax.set_xlabel('Question')
        ax.set_ylabel('Score Improvement (points)')
        ax.set_title('Learning Gain per Question')
        ax.set_xticks(range(len(analytics_df)))
        ax.set_xticklabels([f'Q{i+1}' for i in range(len(analytics_df))])
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_error_reduction_chart(self, analytics_df: pd.DataFrame) -> plt.Figure:
        """
        Create a bar chart showing error reduction per question
        
        Args:
            analytics_df: DataFrame with analytics data
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(analytics_df) == 0:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return fig
        
        colors = ['#51cf66' if x >= 0 else '#ff6b6b' for x in analytics_df['error_reduction']]
        
        ax.bar(range(len(analytics_df)), analytics_df['error_reduction'], color=colors)
        
        ax.set_xlabel('Question')
        ax.set_ylabel('Missing Concepts Reduced')
        ax.set_title('Error Reduction per Question')
        ax.set_xticks(range(len(analytics_df)))
        ax.set_xticklabels([f'Q{i+1}' for i in range(len(analytics_df))])
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
