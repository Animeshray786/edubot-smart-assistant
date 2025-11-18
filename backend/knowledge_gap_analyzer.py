"""
Smart Knowledge Gap Detection
Analyzes failed queries, suggests new patterns, and auto-generates AIML templates
"""
import re
from collections import Counter
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from database.models import Conversation


class KnowledgeGapAnalyzer:
    """Analyzes conversations to detect knowledge gaps and suggest improvements"""
    
    def __init__(self, db=None):
        self.db = db
        self.failed_indicators = [
            'i don\'t understand',
            'i\'m not sure',
            'i don\'t know',
            'sorry, i can\'t',
            'no information',
            'unable to help',
            'try rephrasing',
            'default response',
            'fallback'
        ]
        
        self.question_patterns = [
            r'\bwhat is\b',
            r'\bhow to\b',
            r'\bwhy\b',
            r'\bwhen\b',
            r'\bwhere\b',
            r'\bwho\b',
            r'\bcan you\b',
            r'\btell me about\b',
            r'\bexplain\b'
        ]
    
    def analyze_failed_queries(self, db_session, days=7) -> List[Dict]:
        """
        Analyze conversations to find failed queries
        
        Args:
            db_session: Database session
            days: Number of days to analyze
            
        Returns:
            List of failed query patterns with frequency
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get conversations from last N days
        conversations = db_session.query(Conversation).filter(
            Conversation.timestamp >= start_date
        ).all()
        
        failed_queries = []
        
        for conv in conversations:
            # Check if response indicates failure
            response_lower = conv.response.lower()
            if any(indicator in response_lower for indicator in self.failed_indicators):
                failed_queries.append({
                    'query': conv.message,
                    'response': conv.response,
                    'timestamp': conv.timestamp,
                    'user_id': conv.user_id
                })
        
        # Group and count similar queries
        grouped = self._group_similar_queries(failed_queries)
        
        # Sort by frequency
        sorted_gaps = sorted(grouped, key=lambda x: x['frequency'], reverse=True)
        
        return sorted_gaps[:50]  # Top 50 gaps
    
    def _group_similar_queries(self, queries: List[Dict]) -> List[Dict]:
        """Group similar queries together"""
        groups = {}
        
        for query_data in queries:
            query = query_data['query'].lower().strip()
            
            # Normalize query
            normalized = self._normalize_query(query)
            
            if normalized not in groups:
                groups[normalized] = {
                    'pattern': normalized,
                    'original_query': query_data['query'],
                    'examples': [],
                    'frequency': 0,
                    'users_affected': set(),
                    'category': self._categorize_query(query)
                }
            
            groups[normalized]['frequency'] += 1
            groups[normalized]['examples'].append(query_data['query'])
            groups[normalized]['users_affected'].add(query_data['user_id'])
        
        # Convert to list
        result = []
        for key, data in groups.items():
            data['users_affected'] = len(data['users_affected'])
            data['examples'] = list(set(data['examples']))[:5]  # Max 5 examples
            result.append(data)
        
        return result
    
    def _normalize_query(self, query: str) -> str:
        """Normalize query by removing specific details"""
        # Remove numbers
        query = re.sub(r'\d+', 'NUMBER', query)
        
        # Remove specific names (capitalized words)
        query = re.sub(r'\b[A-Z][a-z]+\b', 'NAME', query)
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        # Extract key patterns
        for pattern in self.question_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                match = re.search(pattern, query, re.IGNORECASE)
                return match.group()
        
        # Return first 5 words
        words = query.split()[:5]
        return ' '.join(words)
    
    def _categorize_query(self, query: str) -> str:
        """Categorize query into topic"""
        categories = {
            'academic': ['exam', 'syllabus', 'course', 'subject', 'study', 'assignment', 'grade'],
            'placement': ['job', 'company', 'interview', 'placement', 'career', 'salary', 'resume'],
            'college': ['admission', 'fee', 'campus', 'hostel', 'faculty', 'library'],
            'technical': ['coding', 'programming', 'software', 'algorithm', 'database'],
            'general': ['help', 'information', 'tell me', 'what is', 'how to']
        }
        
        query_lower = query.lower()
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def suggest_new_patterns(self, knowledge_gaps: List[Dict]) -> List[Dict]:
        """
        Suggest new AIML patterns based on knowledge gaps
        
        Args:
            knowledge_gaps: List of identified gaps
            
        Returns:
            List of pattern suggestions
        """
        suggestions = []
        
        for gap in knowledge_gaps:
            suggestion = {
                'pattern': self._generate_pattern(gap['original_query']),
                'category': gap['category'],
                'priority': self._calculate_priority(gap),
                'frequency': gap['frequency'],
                'examples': gap['examples'],
                'suggested_response': self._generate_response_template(gap),
                'aiml_template': self._generate_aiml_template(gap)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_pattern(self, query: str) -> str:
        """Generate AIML pattern from query"""
        # Convert to uppercase (AIML convention)
        pattern = query.upper()
        
        # Replace specific values with wildcards
        pattern = re.sub(r'\d+', '*', pattern)
        pattern = re.sub(r'\b[A-Z][a-z]+\b', '*', pattern)
        
        # Simplify
        pattern = ' '.join(pattern.split())
        
        return pattern
    
    def _calculate_priority(self, gap: Dict) -> str:
        """Calculate priority level"""
        frequency = gap['frequency']
        users = gap['users_affected']
        
        score = (frequency * 2) + users
        
        if score >= 20:
            return 'critical'
        elif score >= 10:
            return 'high'
        elif score >= 5:
            return 'medium'
        else:
            return 'low'
    
    def _generate_response_template(self, gap: Dict) -> str:
        """Generate suggested response template"""
        category = gap['category']
        
        templates = {
            'academic': "Based on our syllabus, {topic} covers {details}. Would you like to know more about specific topics?",
            'placement': "For {company} placements, {details}. I can also help with interview preparation.",
            'college': "Regarding {topic}, {details}. Contact the administration office for more specific information.",
            'technical': "For {topic}, here's what you need to know: {details}. Would you like examples or practice problems?",
            'general': "Regarding your question about {topic}, {details}."
        }
        
        return templates.get(category, "I can help you with {topic}. {details}")
    
    def _generate_aiml_template(self, gap: Dict) -> str:
        """Generate complete AIML pattern template"""
        pattern = self._generate_pattern(gap['original_query'])
        response = self._generate_response_template(gap)
        category = gap['category']
        
        template = f"""
<category>
    <pattern>{pattern}</pattern>
    <template>
        {response}
    </template>
</category>

<!-- Examples that match this pattern:
{chr(10).join(f'  - {ex}' for ex in gap['examples'][:3])}
-->

<!-- Category: {category} -->
<!-- Priority: {self._calculate_priority(gap)} -->
<!-- Frequency: {gap['frequency']} times -->
<!-- Users affected: {gap['users_affected']} -->
"""
        
        return template
    
    def get_statistics(self, knowledge_gaps: List[Dict]) -> Dict:
        """Get statistics about knowledge gaps"""
        if not knowledge_gaps:
            return {
                'total_gaps': 0,
                'total_frequency': 0,
                'users_affected': 0,
                'categories': {},
                'priorities': {}
            }
        
        categories = Counter(gap['category'] for gap in knowledge_gaps)
        
        suggestions = self.suggest_new_patterns(knowledge_gaps)
        priorities = Counter(s['priority'] for s in suggestions)
        
        return {
            'total_gaps': len(knowledge_gaps),
            'total_frequency': sum(gap['frequency'] for gap in knowledge_gaps),
            'users_affected': sum(gap['users_affected'] for gap in knowledge_gaps),
            'categories': dict(categories),
            'priorities': dict(priorities),
            'top_categories': categories.most_common(5),
            'critical_gaps': len([s for s in suggestions if s['priority'] == 'critical']),
            'high_priority_gaps': len([s for s in suggestions if s['priority'] == 'high'])
        }
    
    def export_patterns_file(self, suggestions: List[Dict], filename: str = None) -> str:
        """Export suggested patterns as AIML file"""
        if filename is None:
            filename = f"suggested_patterns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        
        header = """<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
<!-- Auto-generated AIML patterns based on knowledge gap analysis -->
<!-- Generated: {datetime} -->
<!-- Total patterns: {count} -->

"""
        
        content = header.format(
            datetime=datetime.now().isoformat(),
            count=len(suggestions)
        )
        
        for suggestion in suggestions:
            content += suggestion['aiml_template']
            content += "\n"
        
        content += "</aiml>"
        
        return content
