import json
from typing import Dict, List, Tuple, Optional
from collections import Counter
import re

class SelfHealingTextClassifier:
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialize the text classifier with sentiment dictionaries.
        
        Args:
            confidence_threshold: Minimum confidence score to accept a prediction
        """
        self.confidence_threshold = confidence_threshold
        self.positive_words = {
            'good': 1.0, 'great': 1.0, 'amazing': 1.0, 'love': 1.0,
            'excellent': 1.0, 'best': 1.0, 'wonderful': 1.0, 'fantastic': 1.0,
            'happy': 0.8, 'nice': 0.8, 'enjoy': 0.8, 'like': 0.8,
            'positive': 0.8, 'pleased': 0.8, 'satisfied': 0.8,
            'impressed': 0.9, 'excited': 0.9, 'thrilled': 0.9,
            'delighted': 0.9, 'incredible': 0.9
        }
        
        self.negative_words = {
            'bad': 1.0, 'terrible': 1.0, 'awful': 1.0, 'hate': 1.0,
            'horrible': 1.0, 'disappoint': 1.0, 'worst': 1.0, 'poor': 1.0,
            'sad': 0.8, 'unhappy': 0.8, 'dislike': 0.8, 'negative': 0.8,
            'frustrated': 0.8, 'dissatisfied': 0.8, 'annoyed': 0.8,
            'angry': 0.9, 'terrible': 0.9, 'horrible': 0.9,
            'disgusted': 0.9, 'appalled': 0.9
        }
        
    def classify_text(self, text: str) -> Dict:
        """
        Classify text using a rule-based approach with sentiment scores.
        
        Args:
            text: Input text to classify
            
        Returns:
            Dictionary containing prediction and confidence
        """
        # Preprocess text
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation and numbers
        words = text.split()
        
        # Calculate sentiment scores
        pos_score = sum(self.positive_words.get(word, 0) for word in words)
        neg_score = sum(self.negative_words.get(word, 0) for word in words)
        
        # Calculate confidence based on relative strength of scores
        total_score = pos_score + neg_score
        if total_score == 0:
            confidence = 0.5
        else:
            confidence = pos_score / total_score if pos_score > neg_score else 1 - (neg_score / total_score)
        
        prediction = 'Positive' if pos_score > neg_score else 'Negative'
        
        return {
            'label': prediction,
            'confidence': confidence
        }
    
    def needs_human_verification(self, prediction: Dict) -> bool:
        """
        Check if the prediction needs human verification based on confidence.
        
        Args:
            prediction: Prediction dictionary containing label and confidence
            
        Returns:
            True if prediction needs verification, False otherwise
        """
        return prediction['confidence'] < self.confidence_threshold
    
    def get_backup_prediction(self, text: str) -> Dict:
        """
        Get a backup prediction using a more sophisticated rule-based approach.
        This serves as a fallback when the model is uncertain.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary containing prediction and confidence
        """
        # Enhanced rule-based backup with context analysis
        text_lower = text.lower()
        
        # Check for strong sentiment indicators
        strong_pos = any(word in text_lower for word in ['love', 'amazing', 'fantastic'])
        strong_neg = any(word in text_lower for word in ['hate', 'terrible', 'awful'])
        
        # Check for negations
        negations = ['not', 'never', 'no', 'without']
        has_negation = any(word in text_lower for word in negations)
        
        # Calculate word counts
        pos_count = sum(word in text_lower for word in self.positive_words)
        neg_count = sum(word in text_lower for word in self.negative_words)
        
        # Adjust confidence based on context
        confidence = 0.5
        if strong_pos or strong_neg:
            confidence = 0.7
        if has_negation:
            confidence = 0.6
        
        # Make final prediction
        final_prediction = 'Positive' if pos_count > neg_count else 'Negative'
        
        return {
            'prediction': final_prediction,
            'confidence': confidence * 100,  # Convert to percentage
            'used_fallback': True
        }
    
    def classify_with_fallback(self, text: str) -> Dict:
        """
        Classify text with fallback strategy and return JSON response.
        
        Args:
            text: Input text
            
        Returns:
            JSON response with prediction, confidence, and fallback status
        """
        # Get initial prediction
        prediction = self.classify_text(text)
        
        # Check if we need to use fallback
        if self.needs_human_verification(prediction):
            # Use backup prediction
            return self.get_backup_prediction(text)
        else:
            return {
                'prediction': prediction['label'],
                'confidence': prediction['confidence'] * 100,  # Convert to percentage
                'used_fallback': False
            }
