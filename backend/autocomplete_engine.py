"""
Smart Autocomplete Engine
Provides intelligent question suggestions using AIML patterns and NLP
"""

from typing import List, Dict, Set
import re
from difflib import SequenceMatcher

class AutocompleteEngine:
    """Smart autocomplete engine with pattern matching and NLP"""
    
    def __init__(self, aiml_engine=None):
        """
        Initialize autocomplete engine
        
        Args:
            aiml_engine: AIML engine instance for pattern extraction
        """
        self.aiml_engine = aiml_engine
        self.patterns = set()
        self.popular_questions = []
        self.user_query_history = []
        self.max_history = 100
        self.min_similarity = 0.6
        
        # Pre-defined popular questions
        self.init_popular_questions()
        
        # Extract patterns from AIML if available
        if aiml_engine:
            self.extract_aiml_patterns()
    
    def init_popular_questions(self):
        """Initialize list of popular questions"""
        self.popular_questions = [
            # Academic queries
            "What is Newton's law of motion?",
            "Explain photosynthesis",
            "How do I calculate derivatives?",
            "What are the types of chemical bonds?",
            "Explain the water cycle",
            "What is machine learning?",
            "How does DNA replication work?",
            "Explain the theory of relativity",
            "What is Pythagorean theorem?",
            "How do I solve quadratic equations?",
            
            # Study help
            "How can I improve my study habits?",
            "What are effective note-taking methods?",
            "How do I prepare for exams?",
            "Can you explain this topic?",
            "I need help with homework",
            "How do I memorize formulas?",
            "What are good study techniques?",
            "How much time should I study daily?",
            
            # College information
            "What are the admission requirements?",
            "Tell me about the courses offered",
            "What is the fee structure?",
            "How do I apply for scholarships?",
            "What are the placement statistics?",
            "Tell me about campus facilities",
            "What extracurricular activities are available?",
            
            # Features
            "Show my lecture notes",
            "Create a study plan",
            "Summarize this lecture",
            "Generate practice questions",
            "Test my knowledge",
            "Translate to another language",
            "Read this aloud",
            "Export chat history"
        ]
    
    def extract_aiml_patterns(self):
        """Extract patterns from AIML engine"""
        try:
            if hasattr(self.aiml_engine, 'brain'):
                # Extract pattern texts
                patterns = []
                for pattern in self.aiml_engine.brain._patternsTemplate:
                    pattern_text = pattern.template
                    if pattern_text:
                        # Clean pattern text
                        clean_text = self.clean_pattern(pattern_text)
                        if clean_text:
                            patterns.append(clean_text)
                
                self.patterns = set(patterns)
                print(f"[Autocomplete] Extracted {len(self.patterns)} AIML patterns")
        except Exception as e:
            print(f"[Autocomplete] Could not extract AIML patterns: {e}")
    
    def clean_pattern(self, pattern: str) -> str:
        """
        Clean AIML pattern text
        
        Args:
            pattern: Raw pattern text
            
        Returns:
            str: Cleaned pattern
        """
        # Remove AIML wildcards and special chars
        pattern = re.sub(r'[*_#]', '', pattern)
        # Remove extra spaces
        pattern = ' '.join(pattern.split())
        # Capitalize first letter
        if pattern:
            pattern = pattern[0].upper() + pattern[1:]
        return pattern
    
    def get_suggestions(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Get autocomplete suggestions for a query
        
        Args:
            query: User's partial query
            limit: Maximum number of suggestions
            
        Returns:
            list: List of suggestion dictionaries with text, score, and source
        """
        if not query or len(query) < 2:
            return []
        
        query = query.lower().strip()
        suggestions = []
        
        # Search in popular questions
        for question in self.popular_questions:
            similarity = self.calculate_similarity(query, question.lower())
            if similarity > self.min_similarity or question.lower().startswith(query):
                suggestions.append({
                    'text': question,
                    'score': similarity,
                    'source': 'popular',
                    'icon': '⭐'
                })
        
        # Search in user history
        for past_query in reversed(self.user_query_history):
            similarity = self.calculate_similarity(query, past_query.lower())
            if similarity > self.min_similarity or past_query.lower().startswith(query):
                suggestions.append({
                    'text': past_query,
                    'score': similarity,
                    'source': 'history',
                    'icon': '🕒'
                })
        
        # Search in AIML patterns
        for pattern in self.patterns:
            similarity = self.calculate_similarity(query, pattern.lower())
            if similarity > self.min_similarity or pattern.lower().startswith(query):
                suggestions.append({
                    'text': pattern,
                    'score': similarity,
                    'source': 'aiml',
                    'icon': '🤖'
                })
        
        # Remove duplicates
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            text_lower = suggestion['text'].lower()
            if text_lower not in seen:
                seen.add(text_lower)
                unique_suggestions.append(suggestion)
        
        # Sort by score (highest first)
        unique_suggestions.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top suggestions
        return unique_suggestions[:limit]
    
    def calculate_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate similarity between two strings
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            float: Similarity score (0-1)
        """
        # Exact prefix match gets bonus
        if s2.startswith(s1):
            return 1.0
        
        # Use SequenceMatcher for similarity
        return SequenceMatcher(None, s1, s2).ratio()
    
    def add_to_history(self, query: str):
        """
        Add query to user history
        
        Args:
            query: User's query
        """
        if query and len(query.strip()) > 0:
            self.user_query_history.append(query.strip())
            
            # Limit history size
            if len(self.user_query_history) > self.max_history:
                self.user_query_history.pop(0)
    
    def get_category_suggestions(self, category: str, limit: int = 5) -> List[str]:
        """
        Get suggestions for a specific category
        
        Args:
            category: Category name (academic, study, college, features)
            limit: Maximum number of suggestions
            
        Returns:
            list: List of suggestion texts
        """
        category_questions = {
            'academic': [
                "What is Newton's law of motion?",
                "Explain photosynthesis",
                "How do I calculate derivatives?",
                "What are the types of chemical bonds?",
                "Explain the theory of relativity"
            ],
            'study': [
                "How can I improve my study habits?",
                "What are effective note-taking methods?",
                "How do I prepare for exams?",
                "How do I memorize formulas?",
                "What are good study techniques?"
            ],
            'college': [
                "What are the admission requirements?",
                "Tell me about the courses offered",
                "What is the fee structure?",
                "How do I apply for scholarships?",
                "What are the placement statistics?"
            ],
            'features': [
                "Show my lecture notes",
                "Create a study plan",
                "Summarize this lecture",
                "Generate practice questions",
                "Export chat history"
            ]
        }
        
        return category_questions.get(category, [])[:limit]
    
    def get_trending_queries(self, limit: int = 5) -> List[str]:
        """
        Get trending queries from recent history
        
        Args:
            limit: Maximum number of queries
            
        Returns:
            list: List of trending queries
        """
        # Count frequency in recent history
        recent_queries = self.user_query_history[-50:]  # Last 50 queries
        query_freq = {}
        
        for query in recent_queries:
            query_freq[query] = query_freq.get(query, 0) + 1
        
        # Sort by frequency
        sorted_queries = sorted(query_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [query for query, _ in sorted_queries[:limit]]
    
    def clear_history(self):
        """Clear user query history"""
        self.user_query_history = []
        print("[Autocomplete] User history cleared")
    
    def get_stats(self) -> Dict:
        """
        Get autocomplete engine statistics
        
        Returns:
            dict: Statistics dictionary
        """
        return {
            'total_patterns': len(self.patterns),
            'popular_questions': len(self.popular_questions),
            'user_history_size': len(self.user_query_history),
            'max_history': self.max_history,
            'min_similarity': self.min_similarity
        }


# Global instance
autocomplete_engine = None


def init_autocomplete(aiml_engine=None):
    """
    Initialize autocomplete engine
    
    Args:
        aiml_engine: AIML engine instance
        
    Returns:
        AutocompleteEngine: Initialized engine
    """
    global autocomplete_engine
    autocomplete_engine = AutocompleteEngine(aiml_engine)
    print(f"[OK] Autocomplete Engine initialized")
    return autocomplete_engine
