"""
Data Storage Module
Handles CSV file operations for storing and retrieving evaluation data
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, List
import uuid


class DataStorage:
    """
    Class to handle data storage operations with CSV
    """
    
    def __init__(self, csv_path: str = "data/evaluations.csv"):
        """
        Initialize the data storage
        
        Args:
            csv_path: Path to the CSV file
        """
        self.csv_path = csv_path
        self.ensure_csv_exists()
    
    def ensure_csv_exists(self):
        """
        Create the CSV file with headers if it doesn't exist
        """
        if not os.path.exists(self.csv_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
            
            # Create empty DataFrame with required columns
            df = pd.DataFrame(columns=[
                'session_id',
                'question',
                'attempt_no',
                'score',
                'human_score',
                'strengths',
                'areas_for_improvement',
                'feedback',
                'missing_concepts',
                'answer_text',
                'timestamp'
            ])
            df.to_csv(self.csv_path, index=False)
    
    def save_evaluation(self, session_id: str, question: str, attempt_no: int,
                       evaluation_result: Dict, answer_text: str, human_score: float = None):
        """
        Save an evaluation result to CSV
        
        Args:
            session_id: Unique session identifier
            question: The question being answered
            attempt_no: Attempt number for this question
            evaluation_result: Dictionary containing evaluation results
            answer_text: The student's answer text
            human_score: Optional human-provided score (0-10)
        """
        # Convert lists to strings for CSV storage
        strengths_str = " | ".join(evaluation_result.get('strengths', []))
        areas_str = " | ".join(evaluation_result.get('areas_for_improvement', []))
        missing_str = " | ".join(evaluation_result.get('missing_concepts', []))
        
        # Create new row
        new_row = {
            'session_id': session_id,
            'question': question,
            'attempt_no': attempt_no,
            'score': evaluation_result.get('score', 0),
            'human_score': human_score if human_score is not None else '',
            'strengths': strengths_str,
            'areas_for_improvement': areas_str,
            'feedback': evaluation_result.get('feedback', ''),
            'missing_concepts': missing_str,
            'answer_text': answer_text,
            'timestamp': datetime.now().isoformat()
        }
        
        # Read existing data
        df = pd.read_csv(self.csv_path, encoding='utf-8', encoding_errors='replace')
        
        # Append new row
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Save back to CSV
        df.to_csv(self.csv_path, index=False, encoding='utf-8')
    
    def get_session_data(self, session_id: str) -> pd.DataFrame:
        """
        Get all evaluations for a specific session
        
        Args:
            session_id: Session identifier
        
        Returns:
            DataFrame with session data
        """
        df = pd.read_csv(self.csv_path, encoding='utf-8', encoding_errors='replace')
        return df[df['session_id'] == session_id]
    
    def get_question_attempts(self, session_id: str, question: str) -> pd.DataFrame:
        """
        Get all attempts for a specific question in a session
        
        Args:
            session_id: Session identifier
            question: The question text
        
        Returns:
            DataFrame with attempts for the question
        """
        df = pd.read_csv(self.csv_path, encoding='utf-8', encoding_errors='replace')
        return df[(df['session_id'] == session_id) & (df['question'] == question)].sort_values('attempt_no')
    
    def get_next_attempt_number(self, session_id: str, question: str) -> int:
        """
        Get the next attempt number for a question
        
        Args:
            session_id: Session identifier
            question: The question text
        
        Returns:
            Next attempt number
        """
        attempts = self.get_question_attempts(session_id, question)
        if len(attempts) == 0:
            return 1
        return attempts['attempt_no'].max() + 1
    
    def get_all_data(self) -> pd.DataFrame:
        """
        Get all stored evaluation data
        
        Returns:
            Complete DataFrame
        """
        return pd.read_csv(self.csv_path, encoding='utf-8', encoding_errors='replace')
