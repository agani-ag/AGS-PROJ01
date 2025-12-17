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
    
    def calculate_global_analytics(self, all_data: pd.DataFrame) -> Dict:
        """
        Calculate analytics across ALL sessions (global view)
        
        Args:
            all_data: DataFrame with all evaluation data from all sessions
        
        Returns:
            Dictionary with global analytics
        """
        if len(all_data) == 0:
            return {
                'total_sessions': 0,
                'total_evaluations': 0,
                'total_questions': 0,
                'avg_first_score': 0,
                'avg_last_score': 0,
                'avg_improvement': 0,
                'avg_learning_gain_pct': 0,
                'avg_error_reduction': 0,
                'scores_by_attempt': {}
            }
        
        analytics_list = []
        scores_by_attempt = {}
        
        # Group by session and question to get first and last attempts
        for session_id in all_data['session_id'].unique():
            session_data = all_data[all_data['session_id'] == session_id]
            
            for question in session_data['question'].unique():
                question_data = session_data[session_data['question'] == question].sort_values('attempt_no')
                
                if len(question_data) == 0:
                    continue
                
                first_attempt = question_data.iloc[0]
                last_attempt = question_data.iloc[-1]
                
                # Count missing concepts
                first_errors = len([x for x in str(first_attempt['missing_concepts']).split(' | ') if x.strip()])
                last_errors = len([x for x in str(last_attempt['missing_concepts']).split(' | ') if x.strip()])
                
                first_score = first_attempt['score']
                last_score = last_attempt['score']
                improvement = last_score - first_score
                learning_gain_pct = (improvement / 10) * 100
                error_reduction = first_errors - last_errors
                
                analytics_list.append({
                    'first_score': first_score,
                    'last_score': last_score,
                    'improvement': improvement,
                    'learning_gain_pct': learning_gain_pct,
                    'error_reduction': error_reduction
                })
                
                # Collect scores by attempt number
                for _, row in question_data.iterrows():
                    attempt_no = row['attempt_no']
                    if attempt_no not in scores_by_attempt:
                        scores_by_attempt[attempt_no] = []
                    scores_by_attempt[attempt_no].append(row['score'])
        
        if not analytics_list:
            return {
                'total_sessions': len(all_data['session_id'].unique()),
                'total_evaluations': len(all_data),
                'total_questions': 0,
                'avg_first_score': 0,
                'avg_last_score': 0,
                'avg_improvement': 0,
                'avg_learning_gain_pct': 0,
                'avg_error_reduction': 0,
                'scores_by_attempt': {}
            }
        
        analytics_df = pd.DataFrame(analytics_list)
        
        # Calculate average scores by attempt
        avg_scores_by_attempt = {
            attempt: sum(scores) / len(scores) 
            for attempt, scores in scores_by_attempt.items()
        }
        
        return {
            'total_sessions': len(all_data['session_id'].unique()),
            'total_evaluations': len(all_data),
            'total_questions': len(analytics_list),
            'avg_first_score': round(analytics_df['first_score'].mean(), 2),
            'avg_last_score': round(analytics_df['last_score'].mean(), 2),
            'avg_improvement': round(analytics_df['improvement'].mean(), 2),
            'avg_learning_gain_pct': round(analytics_df['learning_gain_pct'].mean(), 2),
            'avg_error_reduction': round(analytics_df['error_reduction'].mean(), 2),
            'scores_by_attempt': avg_scores_by_attempt
        }
    
    def create_global_average_chart(self, global_analytics: Dict) -> plt.Figure:
        """
        Create a chart showing average scores by attempt number across ALL sessions
        
        Args:
            global_analytics: Dictionary with global analytics data
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scores_by_attempt = global_analytics.get('scores_by_attempt', {})
        
        if not scores_by_attempt:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return fig
        
        attempts = sorted(scores_by_attempt.keys())
        avg_scores = [scores_by_attempt[attempt] for attempt in attempts]
        
        # Line chart with markers
        ax.plot(attempts, avg_scores, marker='o', linewidth=2, markersize=10, 
                color='#4CAF50', label='Average Score')
        
        # Add value labels on points
        for attempt, score in zip(attempts, avg_scores):
            ax.annotate(f'{score:.2f}', 
                       xy=(attempt, score), 
                       xytext=(0, 10),
                       textcoords='offset points',
                       ha='center',
                       fontsize=10,
                       fontweight='bold')
        
        ax.set_xlabel('Attempt Number', fontsize=12)
        ax.set_ylabel('Average Score (out of 10)', fontsize=12)
        ax.set_title('Global Average Score by Attempt (All Sessions)', fontsize=14, fontweight='bold')
        ax.set_xticks(attempts)
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend()
        
        plt.tight_layout()
        return fig

