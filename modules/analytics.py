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
    
    def create_human_vs_ai_comparison_chart(self, session_data: pd.DataFrame) -> plt.Figure:
        """
        Create a chart comparing Human scores vs AI scores
        
        Args:
            session_data: DataFrame with evaluation data including human_score
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Filter data to only include rows with human scores
        data_with_human = session_data[session_data['human_score'].notna() & (session_data['human_score'] != '')]
        
        if len(data_with_human) == 0:
            ax.text(0.5, 0.5, 'No human evaluation data available\nAdd human scores to see comparison', 
                   ha='center', va='center', fontsize=12)
            return fig
        
        # Prepare data
        data_with_human = data_with_human.copy()
        data_with_human['human_score'] = pd.to_numeric(data_with_human['human_score'], errors='coerce')
        data_with_human = data_with_human.dropna(subset=['human_score'])
        
        # Group by question and get the latest attempt for each
        latest_attempts = data_with_human.sort_values('attempt_no').groupby('question').last().reset_index()
        
        if len(latest_attempts) == 0:
            ax.text(0.5, 0.5, 'No valid human scores available', ha='center', va='center')
            return fig
        
        # Create labels for questions
        question_labels = [f"Q{i+1}" for i in range(len(latest_attempts))]
        x_pos = range(len(latest_attempts))
        width = 0.35
        
        # Plot bars
        ai_bars = ax.bar([i - width/2 for i in x_pos], latest_attempts['score'], 
                         width, label='AI Score', color='#4CAF50', alpha=0.8)
        human_bars = ax.bar([i + width/2 for i in x_pos], latest_attempts['human_score'], 
                           width, label='Human Score', color='#2196F3', alpha=0.8)
        
        # Add value labels on bars
        for bars in [ai_bars, human_bars]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           fontsize=9)
        
        # Calculate and display correlation
        correlation = latest_attempts['score'].corr(latest_attempts['human_score'])
        ax.text(0.02, 0.98, f'Correlation: {correlation:.3f}', 
               transform=ax.transAxes, 
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               fontsize=10)
        
        ax.set_xlabel('Question', fontsize=12)
        ax.set_ylabel('Score (out of 10)', fontsize=12)
        ax.set_title('Human vs AI Evaluation Score Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(question_labels)
        ax.set_ylim(0, 10.5)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_global_human_vs_ai_chart(self, all_data: pd.DataFrame) -> plt.Figure:
        """
        Create a chart comparing Human scores vs AI scores globally (all sessions)
        
        Args:
            all_data: DataFrame with all evaluation data including human_score
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Filter data to only include rows with human scores
        data_with_human = all_data[all_data['human_score'].notna() & (all_data['human_score'] != '')]
        
        if len(data_with_human) == 0:
            ax.text(0.5, 0.5, 'No human evaluation data available\nAdd human scores to see global comparison', 
                   ha='center', va='center', fontsize=12)
            return fig
        
        # Prepare data
        data_with_human = data_with_human.copy()
        data_with_human['human_score'] = pd.to_numeric(data_with_human['human_score'], errors='coerce')
        data_with_human = data_with_human.dropna(subset=['human_score'])
        
        if len(data_with_human) == 0:
            ax.text(0.5, 0.5, 'No valid human scores available', ha='center', va='center')
            return fig
        
        # Calculate average AI score and average Human score across all attempts
        avg_ai_score = data_with_human['score'].mean()
        avg_human_score = data_with_human['human_score'].mean()
        
        # Group by attempt number and calculate averages
        attempt_stats = data_with_human.groupby('attempt_no').agg({
            'score': 'mean',
            'human_score': 'mean'
        }).reset_index()
        
        attempt_stats = attempt_stats.sort_values('attempt_no')
        
        # Create line plot
        attempts = attempt_stats['attempt_no']
        ai_scores = attempt_stats['score']
        human_scores = attempt_stats['human_score']
        
        ax.plot(attempts, ai_scores, marker='o', linewidth=2, markersize=10, 
                color='#4CAF50', label='AI Average Score', linestyle='-')
        ax.plot(attempts, human_scores, marker='s', linewidth=2, markersize=10, 
                color='#2196F3', label='Human Average Score', linestyle='--')
        
        # Add value labels on points
        for attempt, ai_score, human_score in zip(attempts, ai_scores, human_scores):
            ax.annotate(f'{ai_score:.2f}', 
                       xy=(attempt, ai_score), 
                       xytext=(0, 10),
                       textcoords='offset points',
                       ha='center',
                       fontsize=9,
                       color='#4CAF50',
                       fontweight='bold')
            ax.annotate(f'{human_score:.2f}', 
                       xy=(attempt, human_score), 
                       xytext=(0, -15),
                       textcoords='offset points',
                       ha='center',
                       fontsize=9,
                       color='#2196F3',
                       fontweight='bold')
        
        # Calculate and display overall statistics
        correlation = data_with_human['score'].corr(data_with_human['human_score'])
        mean_diff = avg_ai_score - avg_human_score
        
        stats_text = f'Correlation: {correlation:.3f}\n'
        stats_text += f'Avg AI: {avg_ai_score:.2f} | Avg Human: {avg_human_score:.2f}\n'
        stats_text += f'Difference: {mean_diff:+.2f}'
        
        ax.text(0.02, 0.98, stats_text, 
               transform=ax.transAxes, 
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               fontsize=10)
        
        ax.set_xlabel('Attempt Number', fontsize=12)
        ax.set_ylabel('Average Score (out of 10)', fontsize=12)
        ax.set_title('Global Human vs AI Score Comparison (All Sessions)', fontsize=14, fontweight='bold')
        ax.set_xticks(attempts)
        ax.set_ylim(0, 10.5)
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig

