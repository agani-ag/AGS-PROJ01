"""
OpenAI Integration Module
Handles communication with OpenAI API for answer evaluation
"""

import os
from openai import OpenAI
from typing import Dict, List
import json


class AnswerEvaluator:
    """
    Class to handle answer evaluation using OpenAI API
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the OpenAI client
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Using GPT-4o-mini for cost efficiency
    
    def evaluate_answer(self, question: str, answer: str) -> Dict:
        """
        Evaluate a student's answer using OpenAI API
        
        Args:
            question: The question being answered
            answer: The student's answer
        
        Returns:
            Dictionary containing evaluation results
        """
        
        system_prompt = """You are an expert teacher evaluating student answers. 
Your task is to provide constructive feedback on student answers.

For each answer, you MUST provide a response in the following JSON format:
{
    "score": <number between 0-10>,
    "strengths": [<list of 2-4 bullet points about what was done well>],
    "areas_for_improvement": [<list of 2-4 bullet points about what needs improvement>],
    "feedback": "<A paragraph of detailed teacher feedback>",
    "missing_concepts": [<list of key concepts that were not addressed or were incorrect>]
}

Be thorough, constructive, and encouraging in your feedback."""

        user_prompt = f"""Please evaluate the following student answer:

QUESTION:
{question}

STUDENT'S ANSWER:
{answer}

Provide your evaluation in the specified JSON format."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            
            # Validate and ensure all required fields are present
            required_fields = ['score', 'strengths', 'areas_for_improvement', 'feedback', 'missing_concepts']
            for field in required_fields:
                if field not in result:
                    result[field] = [] if field in ['strengths', 'areas_for_improvement', 'missing_concepts'] else ""
            
            # Ensure score is within range
            result['score'] = max(0, min(10, result['score']))
            
            return result
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            # Return a default error response
            return {
                "score": 0,
                "strengths": ["Unable to evaluate"],
                "areas_for_improvement": ["API Error occurred"],
                "feedback": f"Error evaluating answer: {str(e)}",
                "missing_concepts": []
            }
