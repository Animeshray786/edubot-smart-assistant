"""
Lecture Note Summarizer
Upload lecture recordings/transcripts and get AI-generated summaries
"""
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class LectureSummarizer:
    """AI-powered lecture note summarizer with key concepts and study questions"""
    
    def __init__(self):
        self.keywords = {
            'definition': ['is defined as', 'refers to', 'means', 'is called', 'known as'],
            'important': ['important', 'crucial', 'essential', 'key', 'critical', 'vital'],
            'process': ['process', 'steps', 'procedure', 'method', 'approach'],
            'example': ['example', 'for instance', 'such as', 'like'],
            'comparison': ['whereas', 'however', 'on the other hand', 'in contrast', 'compared to'],
            'result': ['therefore', 'thus', 'hence', 'as a result', 'consequently'],
            'formula': ['formula', 'equation', 'calculate', '=', 'equals']
        }
    
    def summarize_lecture(self, content: str, title: str = "Lecture Notes") -> Dict:
        """
        Summarize lecture content with bullets, concepts, and questions
        
        Args:
            content: Full lecture transcript/notes
            title: Title of the lecture
            
        Returns:
            Dictionary with summary, key concepts, and study questions
        """
        if not content or len(content.strip()) < 50:
            return {
                'error': 'Content too short. Please provide at least 50 characters.',
                'success': False
            }
        
        # Clean and preprocess content
        clean_content = self._preprocess_content(content)
        
        # Extract key sentences
        key_sentences = self._extract_key_sentences(clean_content)
        
        # Generate bullet points
        bullet_points = self._generate_bullet_points(key_sentences)
        
        # Extract key concepts
        key_concepts = self._extract_key_concepts(clean_content)
        
        # Generate study questions
        study_questions = self._generate_study_questions(clean_content, key_concepts)
        
        # Calculate statistics
        stats = self._calculate_stats(content, bullet_points, key_concepts)
        
        return {
            'success': True,
            'title': title,
            'summary': {
                'bullet_points': bullet_points,
                'word_count': stats['original_words'],
                'compressed_words': stats['summary_words'],
                'compression_ratio': stats['compression_ratio']
            },
            'key_concepts': key_concepts,
            'study_questions': study_questions,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def _preprocess_content(self, content: str) -> str:
        """Clean and preprocess the content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove URLs
        content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
        
        # Remove special characters but keep punctuation
        content = re.sub(r'[^\w\s.,;:?!()\-\'\"=+*/]', '', content)
        
        return content.strip()
    
    def _extract_key_sentences(self, content: str, max_sentences: int = 10) -> List[str]:
        """Extract key sentences using keyword scoring"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Score each sentence
        scored_sentences = []
        for sentence in sentences:
            score = self._score_sentence(sentence)
            if score > 0:
                scored_sentences.append((sentence, score))
        
        # Sort by score and return top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_sentences[:max_sentences]]
    
    def _score_sentence(self, sentence: str) -> float:
        """Score sentence based on keyword presence"""
        score = 0.0
        sentence_lower = sentence.lower()
        
        # Check for each keyword category
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in sentence_lower:
                    # Different weights for different categories
                    if category == 'definition':
                        score += 3.0
                    elif category == 'important':
                        score += 2.5
                    elif category == 'formula':
                        score += 2.0
                    else:
                        score += 1.5
        
        # Bonus for longer, informative sentences
        words = sentence.split()
        if 10 <= len(words) <= 30:
            score += 1.0
        
        # Bonus for sentences with numbers (likely to be facts)
        if re.search(r'\d+', sentence):
            score += 0.5
        
        return score
    
    def _generate_bullet_points(self, key_sentences: List[str]) -> List[str]:
        """Convert key sentences to bullet points"""
        bullet_points = []
        
        for sentence in key_sentences:
            # Clean up the sentence
            bullet = sentence.strip()
            
            # Ensure it ends with proper punctuation
            if not bullet.endswith(('.', '!', '?')):
                bullet += '.'
            
            # Capitalize first letter
            if bullet:
                bullet = bullet[0].upper() + bullet[1:]
            
            bullet_points.append(bullet)
        
        return bullet_points
    
    def _extract_key_concepts(self, content: str, max_concepts: int = 8) -> List[Dict]:
        """Extract key concepts with definitions"""
        concepts = []
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            # Look for definition patterns
            for pattern in self.keywords['definition']:
                if pattern in sentence.lower():
                    # Try to extract the term being defined
                    parts = sentence.lower().split(pattern)
                    if len(parts) >= 2:
                        term = parts[0].strip().split()[-3:]  # Last few words before definition
                        term = ' '.join(term).title()
                        definition = parts[1].strip()
                        
                        # Clean up
                        term = re.sub(r'^(the|a|an)\s+', '', term, flags=re.IGNORECASE)
                        
                        if term and definition and len(term) < 50:
                            concepts.append({
                                'term': term,
                                'definition': definition[:150] + ('...' if len(definition) > 150 else ''),
                                'importance': 'high'
                            })
                            break
        
        # Also extract capitalized terms that appear multiple times
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        term_counts = {}
        for term in capitalized_terms:
            if len(term) > 3 and term.lower() not in ['the', 'this', 'that', 'these', 'those']:
                term_counts[term] = term_counts.get(term, 0) + 1
        
        # Add frequently mentioned terms
        for term, count in sorted(term_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            if count >= 2 and term not in [c['term'] for c in concepts]:
                concepts.append({
                    'term': term,
                    'definition': f'Mentioned {count} times - key concept in this lecture',
                    'importance': 'medium' if count < 4 else 'high'
                })
        
        return concepts[:max_concepts]
    
    def _generate_study_questions(self, content: str, key_concepts: List[Dict]) -> List[Dict]:
        """Generate study questions based on content"""
        questions = []
        
        # Question templates
        templates = [
            "What is {term}?",
            "Explain the concept of {term}.",
            "How does {term} work?",
            "What are the key characteristics of {term}?",
            "Why is {term} important?",
            "Compare and contrast {term1} with {term2}.",
            "What is the difference between {term1} and {term2}?",
            "Describe the process of {term}.",
            "What are the applications of {term}?",
            "List the main points about {term}."
        ]
        
        # Generate questions from key concepts
        for i, concept in enumerate(key_concepts[:6]):
            term = concept['term']
            
            # Choose template based on concept type
            if i < len(templates):
                if i == 5 and len(key_concepts) >= 2:
                    question_text = templates[5].format(
                        term1=key_concepts[0]['term'],
                        term2=key_concepts[1]['term']
                    )
                elif i == 6 and len(key_concepts) >= 2:
                    question_text = templates[6].format(
                        term1=key_concepts[0]['term'],
                        term2=key_concepts[1]['term']
                    )
                else:
                    question_text = templates[i % len(templates)].format(term=term)
            else:
                question_text = f"Explain {term} in your own words."
            
            # Determine difficulty
            difficulty = 'easy' if i < 2 else 'medium' if i < 4 else 'hard'
            
            questions.append({
                'id': i + 1,
                'question': question_text,
                'type': 'short_answer',
                'difficulty': difficulty,
                'related_concept': term
            })
        
        # Add general comprehension questions
        general_questions = [
            {
                'id': len(questions) + 1,
                'question': 'Summarize the main topic of this lecture in 2-3 sentences.',
                'type': 'essay',
                'difficulty': 'medium',
                'related_concept': 'Overall Understanding'
            },
            {
                'id': len(questions) + 2,
                'question': 'What are the 3 most important takeaways from this lecture?',
                'type': 'list',
                'difficulty': 'easy',
                'related_concept': 'Key Takeaways'
            }
        ]
        
        questions.extend(general_questions)
        
        return questions[:10]  # Return max 10 questions
    
    def _calculate_stats(self, original: str, bullet_points: List[str], concepts: List[Dict]) -> Dict:
        """Calculate summary statistics"""
        original_words = len(original.split())
        summary_words = sum(len(bp.split()) for bp in bullet_points)
        
        compression_ratio = round((1 - summary_words / original_words) * 100, 1) if original_words > 0 else 0
        
        return {
            'original_words': original_words,
            'summary_words': summary_words,
            'compression_ratio': f'{compression_ratio}%',
            'key_concepts_count': len(concepts),
            'bullet_points_count': len(bullet_points),
            'estimated_read_time': f'{original_words // 200} min',
            'estimated_review_time': f'{summary_words // 200 + 1} min'
        }
    
    def format_summary_html(self, summary_data: Dict) -> str:
        """Format summary as beautiful HTML"""
        if not summary_data.get('success'):
            return f"<div class='error'>{summary_data.get('error', 'Unknown error')}</div>"
        
        html = f"""
        <div style="max-width: 900px; margin: 20px auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 30px; border-radius: 12px 12px 0 0; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="margin: 0; font-size: 2em;">📚 {summary_data['title']}</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">
                    Generated on {datetime.fromisoformat(summary_data['timestamp']).strftime('%B %d, %Y at %I:%M %p')}
                </p>
            </div>
            
            <!-- Statistics Bar -->
            <div style="background: #f7fafc; padding: 20px; display: flex; justify-content: space-around; 
                        border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0;">
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">
                        {summary_data['statistics']['original_words']}
                    </div>
                    <div style="color: #718096; font-size: 0.9em;">Original Words</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #48bb78;">
                        {summary_data['statistics']['compression_ratio']}
                    </div>
                    <div style="color: #718096; font-size: 0.9em;">Compressed</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #ed8936;">
                        {summary_data['statistics']['key_concepts_count']}
                    </div>
                    <div style="color: #718096; font-size: 0.9em;">Key Concepts</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #4299e1;">
                        {len(summary_data['study_questions'])}
                    </div>
                    <div style="color: #718096; font-size: 0.9em;">Study Questions</div>
                </div>
            </div>
            
            <!-- Summary Bullet Points -->
            <div style="background: white; padding: 30px; border-left: 1px solid #e2e8f0; 
                        border-right: 1px solid #e2e8f0;">
                <h2 style="color: #2d3748; margin-top: 0; display: flex; align-items: center;">
                    <span style="font-size: 1.5em; margin-right: 10px;">✨</span>
                    Summary Highlights
                </h2>
                <ul style="list-style: none; padding: 0;">
"""
        
        # Add bullet points
        for i, point in enumerate(summary_data['summary']['bullet_points'], 1):
            html += f"""
                    <li style="margin: 15px 0; padding: 15px; background: #f7fafc; 
                               border-left: 4px solid #667eea; border-radius: 6px;">
                        <span style="font-weight: bold; color: #667eea; margin-right: 8px;">{i}.</span>
                        {point}
                    </li>
"""
        
        html += """
                </ul>
            </div>
            
            <!-- Key Concepts -->
            <div style="background: white; padding: 30px; border-left: 1px solid #e2e8f0; 
                        border-right: 1px solid #e2e8f0; border-top: 1px solid #e2e8f0;">
                <h2 style="color: #2d3748; margin-top: 0; display: flex; align-items: center;">
                    <span style="font-size: 1.5em; margin-right: 10px;">🎯</span>
                    Key Concepts
                </h2>
                <div style="display: grid; gap: 15px;">
"""
        
        # Add key concepts
        for concept in summary_data['key_concepts']:
            importance_color = '#48bb78' if concept['importance'] == 'high' else '#ed8936'
            html += f"""
                    <div style="padding: 15px; background: #f7fafc; border-radius: 8px; 
                                border: 2px solid {importance_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; color: #2d3748; font-size: 1.1em;">{concept['term']}</h3>
                            <span style="background: {importance_color}; color: white; padding: 4px 12px; 
                                         border-radius: 12px; font-size: 0.8em; text-transform: uppercase;">
                                {concept['importance']}
                            </span>
                        </div>
                        <p style="margin: 10px 0 0 0; color: #4a5568; line-height: 1.6;">
                            {concept['definition']}
                        </p>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <!-- Study Questions -->
            <div style="background: white; padding: 30px; border: 1px solid #e2e8f0; 
                        border-radius: 0 0 12px 12px;">
                <h2 style="color: #2d3748; margin-top: 0; display: flex; align-items: center;">
                    <span style="font-size: 1.5em; margin-right: 10px;">❓</span>
                    Study Questions
                </h2>
                <div style="display: grid; gap: 15px;">
"""
        
        # Add study questions
        for q in summary_data['study_questions']:
            difficulty_colors = {
                'easy': '#48bb78',
                'medium': '#ed8936',
                'hard': '#f56565'
            }
            color = difficulty_colors.get(q['difficulty'], '#4299e1')
            
            html += f"""
                    <div style="padding: 15px; background: #f7fafc; border-radius: 8px; 
                                border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: start; 
                                    margin-bottom: 8px;">
                            <span style="font-weight: bold; color: {color};">Q{q['id']}.</span>
                            <span style="background: {color}; color: white; padding: 2px 8px; 
                                         border-radius: 10px; font-size: 0.75em; text-transform: uppercase;">
                                {q['difficulty']}
                            </span>
                        </div>
                        <p style="margin: 0; color: #2d3748; font-size: 1em; line-height: 1.6;">
                            {q['question']}
                        </p>
                        <p style="margin: 8px 0 0 0; color: #718096; font-size: 0.85em;">
                            Type: {q['type'].replace('_', ' ').title()} | 
                            Related: {q['related_concept']}
                        </p>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; padding: 20px; color: #718096; font-size: 0.9em;">
                <p>💡 Review Time: {review_time} | Original Read Time: {read_time}</p>
                <p style="margin: 5px 0 0 0;">Generated by EduBot Lecture Summarizer</p>
            </div>
            
        </div>
        """.format(
            review_time=summary_data['statistics']['estimated_review_time'],
            read_time=summary_data['statistics']['estimated_read_time']
        )
        
        return html
