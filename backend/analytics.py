"""
Analytics Module for Hybrid Voice Chatbot
Provides analytics and reporting capabilities
"""
from datetime import datetime, timedelta
from collections import Counter


class Analytics:
    """Handles analytics and reporting"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_dashboard_stats(self):
        """Get main dashboard statistics"""
        try:
            global_stats = self.db_manager.get_global_analytics()
            feedback_summary = self._get_recent_feedback_summary(7)
            conversation_stats = self._get_conversation_stats(30)
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'global_stats': global_stats,
                'recent_feedback': feedback_summary,
                'conversation_stats': conversation_stats,
                'growth_metrics': self._calculate_growth_metrics()
            }
            
        except Exception as e:
            print(f"Error getting dashboard stats: {str(e)}")
            return {}
    
    def _get_recent_feedback_summary(self, days=7):
        """Get recent feedback summary"""
        try:
            all_feedback = self.db_manager.get_all_feedback(page=1, per_page=9999)
            
            since_date = datetime.utcnow() - timedelta(days=days)
            recent = [
                f for f in all_feedback.items
                if f.created_at >= since_date
            ]
            
            total = len(recent)
            good = sum(1 for f in recent if f.rating == 'good')
            bad = sum(1 for f in recent if f.rating == 'bad')
            
            return {
                'days': days,
                'total': total,
                'good': good,
                'bad': bad,
                'satisfaction_rate': (good / total * 100) if total > 0 else 0
            }
            
        except Exception as e:
            print(f"Error in feedback summary: {str(e)}")
            return {}
    
    def _get_conversation_stats(self, days=30):
        """Get conversation statistics"""
        try:
            # This is a simplified version - in production you'd use proper SQL queries
            all_convs = self.db_manager.get_recent_conversations(limit=1000)
            
            since_date = datetime.utcnow() - timedelta(days=days)
            recent = [c for c in all_convs if c.timestamp >= since_date]
            
            total = len(recent)
            voice = sum(1 for c in recent if c.message_type == 'voice')
            text = sum(1 for c in recent if c.message_type == 'text')
            
            # Sentiment breakdown
            positive = sum(1 for c in recent if c.sentiment == 'positive')
            negative = sum(1 for c in recent if c.sentiment == 'negative')
            neutral = sum(1 for c in recent if c.sentiment == 'neutral')
            
            return {
                'days': days,
                'total_conversations': total,
                'voice_interactions': voice,
                'text_interactions': text,
                'sentiment': {
                    'positive': positive,
                    'negative': negative,
                    'neutral': neutral
                },
                'avg_per_day': total / days if days > 0 else 0
            }
            
        except Exception as e:
            print(f"Error in conversation stats: {str(e)}")
            return {}
    
    def _calculate_growth_metrics(self):
        """Calculate growth metrics"""
        try:
            # Last 7 days vs previous 7 days
            now = datetime.utcnow()
            week_ago = now - timedelta(days=7)
            two_weeks_ago = now - timedelta(days=14)
            
            all_convs = self.db_manager.get_recent_conversations(limit=1000)
            
            this_week = [c for c in all_convs if c.timestamp >= week_ago]
            last_week = [c for c in all_convs if two_weeks_ago <= c.timestamp < week_ago]
            
            this_week_count = len(this_week)
            last_week_count = len(last_week)
            
            if last_week_count > 0:
                growth_rate = ((this_week_count - last_week_count) / last_week_count) * 100
            else:
                growth_rate = 100 if this_week_count > 0 else 0
            
            return {
                'this_week': this_week_count,
                'last_week': last_week_count,
                'growth_rate': round(growth_rate, 2),
                'trend': 'up' if growth_rate > 0 else 'down' if growth_rate < 0 else 'stable'
            }
            
        except Exception as e:
            print(f"Error calculating growth metrics: {str(e)}")
            return {}
    
    def get_user_engagement(self, user_id):
        """Get engagement metrics for a specific user"""
        try:
            analytics = self.db_manager.get_analytics(user_id)
            conversations = self.db_manager.get_user_conversations(user_id, page=1, per_page=9999)
            
            if not analytics:
                return None
            
            total_convs = conversations.total if hasattr(conversations, 'total') else 0
            
            # Calculate engagement score (0-100)
            engagement_score = min(100, (
                (analytics.total_questions * 2) +
                (analytics.positive_feedback * 5) +
                (total_convs * 1)
            ) / 2)
            
            return {
                'user_id': user_id,
                'total_questions': analytics.total_questions,
                'total_conversations': total_convs,
                'positive_feedback': analytics.positive_feedback,
                'negative_feedback': analytics.negative_feedback,
                'engagement_score': round(engagement_score, 2),
                'avg_response_time': analytics.avg_response_time,
                'last_updated': analytics.updated_at.isoformat() if analytics.updated_at else None
            }
            
        except Exception as e:
            print(f"Error getting user engagement: {str(e)}")
            return None
    
    def get_popular_topics(self, limit=10):
        """Get most popular topics based on conversations"""
        try:
            conversations = self.db_manager.get_recent_conversations(limit=1000)
            
            # Extract keywords from messages
            from textblob import TextBlob
            
            topic_count = Counter()
            for conv in conversations:
                try:
                    blob = TextBlob(conv.message)
                    # Get noun phrases as topics
                    for phrase in blob.noun_phrases:
                        if len(phrase) > 3:  # Filter short phrases
                            topic_count[phrase.lower()] += 1
                except:
                    continue
            
            # Get most common topics
            popular = topic_count.most_common(limit)
            
            return [
                {'topic': topic, 'count': count}
                for topic, count in popular
            ]
            
        except Exception as e:
            print(f"Error getting popular topics: {str(e)}")
            return []
    
    def get_response_time_stats(self):
        """Get response time statistics"""
        try:
            # This would require storing response times - simplified version
            all_analytics = []
            users = self.db_manager.get_all_users(page=1, per_page=9999)
            
            for user in users.items:
                analytics = self.db_manager.get_analytics(user.user_id)
                if analytics and analytics.avg_response_time > 0:
                    all_analytics.append(analytics.avg_response_time)
            
            if not all_analytics:
                return {
                    'avg_response_time': 0,
                    'min_response_time': 0,
                    'max_response_time': 0
                }
            
            return {
                'avg_response_time': sum(all_analytics) / len(all_analytics),
                'min_response_time': min(all_analytics),
                'max_response_time': max(all_analytics),
                'sample_size': len(all_analytics)
            }
            
        except Exception as e:
            print(f"Error getting response time stats: {str(e)}")
            return {}
    
    def get_hourly_activity(self, days=7):
        """Get hourly activity distribution"""
        try:
            all_convs = self.db_manager.get_recent_conversations(limit=1000)
            
            since_date = datetime.utcnow() - timedelta(days=days)
            recent = [c for c in all_convs if c.timestamp >= since_date]
            
            # Group by hour
            hourly = {hour: 0 for hour in range(24)}
            for conv in recent:
                hour = conv.timestamp.hour
                hourly[hour] += 1
            
            return {
                'days': days,
                'hourly_distribution': [
                    {'hour': hour, 'count': count}
                    for hour, count in sorted(hourly.items())
                ],
                'peak_hour': max(hourly, key=hourly.get) if hourly else 0
            }
            
        except Exception as e:
            print(f"Error getting hourly activity: {str(e)}")
            return {}
    
    def export_analytics_report(self, user_id=None):
        """Export comprehensive analytics report"""
        try:
            report = {
                'generated_at': datetime.utcnow().isoformat(),
                'dashboard_stats': self.get_dashboard_stats(),
                'popular_topics': self.get_popular_topics(),
                'response_time_stats': self.get_response_time_stats(),
                'hourly_activity': self.get_hourly_activity()
            }
            
            if user_id:
                report['user_engagement'] = self.get_user_engagement(user_id)
            
            return report
            
        except Exception as e:
            print(f"Error exporting analytics report: {str(e)}")
            return {}
