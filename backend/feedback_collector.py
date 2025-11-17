"""
Feedback Collector for Hybrid Voice Chatbot
Manages user feedback and rating system
"""
from datetime import datetime, timedelta


class FeedbackCollector:
    """Handles feedback collection and analysis"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def collect_feedback(self, conversation_id, rating, comments=None, helpful=True):
        """Collect feedback for a conversation"""
        try:
            # Validate rating
            valid_ratings = ['good', 'bad', 'improvement']
            if rating not in valid_ratings:
                return None, "Invalid rating. Must be: good, bad, or improvement"
            
            # Check if feedback already exists
            conversation = self.db_manager.get_conversation_by_id(conversation_id)
            if not conversation:
                return None, "Conversation not found"
            
            if conversation.feedback:
                return None, "Feedback already exists for this conversation"
            
            # Create feedback
            feedback = self.db_manager.create_feedback(
                conversation_id=conversation_id,
                rating=rating,
                comments=comments,
                helpful=helpful
            )
            
            print(f"✓ Feedback collected: {feedback.feedback_id} - {rating}")
            return feedback, "Feedback submitted successfully"
            
        except Exception as e:
            print(f"Error collecting feedback: {str(e)}")
            return None, f"Error: {str(e)}"
    
    def get_feedback_summary(self, days=30):
        """Get feedback summary for specified period"""
        try:
            # Get all feedback
            all_feedback = self.db_manager.get_all_feedback(page=1, per_page=9999)
            
            # Filter by date
            since_date = datetime.utcnow() - timedelta(days=days)
            recent_feedback = [
                f for f in all_feedback.items 
                if f.created_at >= since_date
            ]
            
            # Calculate statistics
            total = len(recent_feedback)
            good = sum(1 for f in recent_feedback if f.rating == 'good')
            bad = sum(1 for f in recent_feedback if f.rating == 'bad')
            improvement = sum(1 for f in recent_feedback if f.rating == 'improvement')
            
            with_comments = sum(1 for f in recent_feedback if f.comments)
            
            return {
                'period_days': days,
                'total_feedback': total,
                'good': good,
                'bad': bad,
                'improvement': improvement,
                'with_comments': with_comments,
                'satisfaction_rate': (good / total * 100) if total > 0 else 0,
                'dissatisfaction_rate': (bad / total * 100) if total > 0 else 0
            }
            
        except Exception as e:
            print(f"Error getting feedback summary: {str(e)}")
            return {}
    
    def get_top_issues(self, limit=10):
        """Get top issues based on negative feedback"""
        try:
            # Get all bad/improvement feedback with comments
            all_feedback = self.db_manager.get_all_feedback(page=1, per_page=9999)
            
            negative_feedback = [
                f for f in all_feedback.items
                if f.rating in ['bad', 'improvement'] and f.comments
            ]
            
            # Group by similar comments (simplified)
            issues = []
            for feedback in negative_feedback[:limit]:
                conversation = self.db_manager.get_conversation_by_id(feedback.conversation_id)
                if conversation:
                    issues.append({
                        'feedback_id': feedback.feedback_id,
                        'rating': feedback.rating,
                        'comments': feedback.comments,
                        'question': conversation.message,
                        'response': conversation.response,
                        'created_at': feedback.created_at.isoformat() if feedback.created_at else None
                    })
            
            return issues
            
        except Exception as e:
            print(f"Error getting top issues: {str(e)}")
            return []
    
    def get_positive_examples(self, limit=10):
        """Get examples of positive feedback"""
        try:
            all_feedback = self.db_manager.get_all_feedback(page=1, per_page=9999)
            
            positive_feedback = [
                f for f in all_feedback.items
                if f.rating == 'good'
            ]
            
            examples = []
            for feedback in positive_feedback[:limit]:
                conversation = self.db_manager.get_conversation_by_id(feedback.conversation_id)
                if conversation:
                    examples.append({
                        'feedback_id': feedback.feedback_id,
                        'question': conversation.message,
                        'response': conversation.response,
                        'comments': feedback.comments,
                        'created_at': feedback.created_at.isoformat() if feedback.created_at else None
                    })
            
            return examples
            
        except Exception as e:
            print(f"Error getting positive examples: {str(e)}")
            return []
    
    def analyze_feedback_trends(self, days=30):
        """Analyze feedback trends over time"""
        try:
            all_feedback = self.db_manager.get_all_feedback(page=1, per_page=9999)
            
            since_date = datetime.utcnow() - timedelta(days=days)
            recent_feedback = [
                f for f in all_feedback.items
                if f.created_at >= since_date
            ]
            
            # Group by date
            daily_stats = {}
            for feedback in recent_feedback:
                date_key = feedback.created_at.strftime('%Y-%m-%d')
                
                if date_key not in daily_stats:
                    daily_stats[date_key] = {
                        'good': 0,
                        'bad': 0,
                        'improvement': 0,
                        'total': 0
                    }
                
                daily_stats[date_key][feedback.rating] += 1
                daily_stats[date_key]['total'] += 1
            
            # Convert to sorted list
            trends = [
                {
                    'date': date,
                    **stats,
                    'satisfaction_rate': (stats['good'] / stats['total'] * 100) if stats['total'] > 0 else 0
                }
                for date, stats in sorted(daily_stats.items())
            ]
            
            return trends
            
        except Exception as e:
            print(f"Error analyzing feedback trends: {str(e)}")
            return []
    
    def get_feedback_by_user(self, user_id):
        """Get all feedback from a specific user"""
        try:
            conversations = self.db_manager.get_user_conversations(user_id, page=1, per_page=9999)
            
            user_feedback = []
            for conv in conversations.items:
                if conv.feedback:
                    user_feedback.append({
                        'feedback_id': conv.feedback.feedback_id,
                        'conversation_id': conv.conversation_id,
                        'rating': conv.feedback.rating,
                        'comments': conv.feedback.comments,
                        'question': conv.message,
                        'response': conv.response,
                        'created_at': conv.feedback.created_at.isoformat() if conv.feedback.created_at else None
                    })
            
            return user_feedback
            
        except Exception as e:
            print(f"Error getting user feedback: {str(e)}")
            return []
    
    def get_improvement_suggestions(self, min_occurrences=3):
        """Get suggestions for improvement based on feedback"""
        try:
            issues = self.get_top_issues(limit=50)
            
            # Analyze patterns in feedback
            suggestions = []
            
            # Look for common keywords in negative feedback
            keyword_count = {}
            for issue in issues:
                if issue['comments']:
                    words = issue['comments'].lower().split()
                    for word in words:
                        if len(word) > 4:  # Only consider words longer than 4 chars
                            keyword_count[word] = keyword_count.get(word, 0) + 1
            
            # Filter keywords that appear multiple times
            common_issues = {
                word: count 
                for word, count in keyword_count.items() 
                if count >= min_occurrences
            }
            
            # Create suggestions
            for keyword, count in sorted(common_issues.items(), key=lambda x: x[1], reverse=True):
                suggestions.append({
                    'issue': keyword,
                    'occurrences': count,
                    'priority': 'High' if count >= 5 else 'Medium',
                    'suggestion': f"Review and improve responses related to '{keyword}'"
                })
            
            return suggestions[:10]  # Top 10 suggestions
            
        except Exception as e:
            print(f"Error getting improvement suggestions: {str(e)}")
            return []
    
    def export_feedback_report(self, days=30):
        """Export comprehensive feedback report"""
        try:
            summary = self.get_feedback_summary(days)
            trends = self.analyze_feedback_trends(days)
            issues = self.get_top_issues()
            positive = self.get_positive_examples()
            suggestions = self.get_improvement_suggestions()
            
            report = {
                'generated_at': datetime.utcnow().isoformat(),
                'period_days': days,
                'summary': summary,
                'trends': trends,
                'top_issues': issues,
                'positive_examples': positive,
                'improvement_suggestions': suggestions
            }
            
            return report
            
        except Exception as e:
            print(f"Error exporting feedback report: {str(e)}")
            return {}
