"""
Advanced Admin Features Routes
Knowledge Gap Detection, Bulk AIML Editor, Pattern Testing, Performance Monitor, Rate Limiting
"""
from flask import Blueprint, render_template, request, session, jsonify, current_app
from backend.utils import login_required, admin_required, success_response, error_response
from backend.knowledge_gap_analyzer import KnowledgeGapAnalyzer
from backend.bulk_aiml_editor import BulkAIMLEditor
from backend.pattern_testing_sandbox import PatternTestingSandbox
from backend.performance_monitor import performance_monitor
from backend.rate_limiter import rate_limiter
from database import db
from datetime import datetime, timedelta
import os

admin_advanced_bp = Blueprint('admin_advanced', __name__)

# Initialize modules
aiml_dir = 'aiml'
knowledge_gap = KnowledgeGapAnalyzer(db)
bulk_editor = BulkAIMLEditor(aiml_dir)
sandbox = PatternTestingSandbox(aiml_dir)


# ==================== MAIN DASHBOARD ====================

@admin_advanced_bp.route('/')
@login_required
@admin_required
def advanced_dashboard():
    """Advanced features dashboard"""
    return render_template('admin/advanced_features.html')


# ==================== KNOWLEDGE GAP DETECTION ====================

@admin_advanced_bp.route('/gaps/list', methods=['GET'])
@login_required
@admin_required
def get_knowledge_gaps():
    """Get list of knowledge gaps"""
    try:
        min_frequency = request.args.get('min_frequency', 3, type=int)
        days = request.args.get('days', 30, type=int)
        
        gaps = knowledge_gap.get_knowledge_gaps(min_frequency, days)
        
        return success_response({
            'gaps': gaps,
            'count': len(gaps),
            'period_days': days
        })
    except Exception as e:
        return error_response(f"Failed to get knowledge gaps: {str(e)}", 500)


@admin_advanced_bp.route('/gaps/suggestions', methods=['POST'])
@login_required
@admin_required
def get_pattern_suggestions():
    """Get pattern suggestions for knowledge gaps"""
    try:
        data = request.get_json()
        gap_queries = data.get('queries', [])
        
        if not gap_queries:
            return error_response('No queries provided', 400)
        
        suggestions = knowledge_gap.suggest_new_patterns(gap_queries)
        
        return success_response({
            'suggestions': suggestions,
            'count': len(suggestions)
        })
    except Exception as e:
        return error_response(f"Failed to generate suggestions: {str(e)}", 500)


@admin_advanced_bp.route('/gaps/generate-aiml', methods=['POST'])
@login_required
@admin_required
def generate_aiml_template():
    """Auto-generate AIML template from query"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        category = data.get('category', 'general')
        
        if not query:
            return error_response('Query required', 400)
        
        aiml_template = knowledge_gap.auto_generate_aiml_template(query, category)
        
        return success_response({
            'aiml': aiml_template,
            'query': query,
            'category': category
        })
    except Exception as e:
        return error_response(f"Failed to generate AIML: {str(e)}", 500)


@admin_advanced_bp.route('/gaps/clusters', methods=['GET'])
@login_required
@admin_required
def get_topic_clusters():
    """Get topic clusters from failed queries"""
    try:
        days = request.args.get('days', 30, type=int)
        
        # Get recent gaps
        gaps = knowledge_gap.get_knowledge_gaps(min_frequency=1, days=days)
        queries = [gap['query'] for gap in gaps]
        
        if not queries:
            return success_response({'clusters': [], 'message': 'No failed queries found'})
        
        clusters = knowledge_gap.detect_topic_clusters(queries)
        
        return success_response({
            'clusters': clusters,
            'total_queries': len(queries)
        })
    except Exception as e:
        return error_response(f"Failed to cluster topics: {str(e)}", 500)


@admin_advanced_bp.route('/gaps/prioritized', methods=['GET'])
@login_required
@admin_required
def get_prioritized_gaps():
    """Get prioritized knowledge gaps"""
    try:
        days = request.args.get('days', 30, type=int)
        
        gaps = knowledge_gap.get_knowledge_gaps(min_frequency=1, days=days)
        prioritized = knowledge_gap.prioritize_gaps(gaps)
        
        return success_response({
            'gaps': prioritized,
            'count': len(prioritized)
        })
    except Exception as e:
        return error_response(f"Failed to prioritize gaps: {str(e)}", 500)


# ==================== BULK AIML EDITOR ====================

@admin_advanced_bp.route('/aiml/search', methods=['POST'])
@login_required
@admin_required
def search_in_aiml_files():
    """Search across all AIML files"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '').strip()
        case_sensitive = data.get('case_sensitive', False)
        
        if not search_term:
            return error_response('Search term required', 400)
        
        results = bulk_editor.find_in_files(search_term, case_sensitive=case_sensitive)
        
        return success_response({
            'results': results,
            'count': len(results),
            'search_term': search_term
        })
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/replace', methods=['POST'])
@login_required
@admin_required
def replace_in_aiml_files():
    """Find and replace across AIML files"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '').strip()
        replace_term = data.get('replace_term', '').strip()
        preview = data.get('preview', True)
        case_sensitive = data.get('case_sensitive', False)
        
        if not search_term:
            return error_response('Search term required', 400)
        
        result = bulk_editor.replace_in_files(
            search_term, 
            replace_term, 
            preview=preview,
            case_sensitive=case_sensitive
        )
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Replace failed: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/batch-edit', methods=['POST'])
@login_required
@admin_required
def batch_edit_patterns():
    """Batch edit multiple patterns"""
    try:
        data = request.get_json()
        pattern_updates = data.get('updates', [])
        
        if not pattern_updates:
            return error_response('No updates provided', 400)
        
        result = bulk_editor.batch_edit_patterns(pattern_updates)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Batch edit failed: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/add-category', methods=['POST'])
@login_required
@admin_required
def add_aiml_category():
    """Add new AIML category file"""
    try:
        data = request.get_json()
        category_name = data.get('category_name', '').strip()
        patterns = data.get('patterns', [])
        description = data.get('description', '')
        
        if not category_name:
            return error_response('Category name required', 400)
        
        if not patterns:
            return error_response('At least one pattern required', 400)
        
        result = bulk_editor.add_new_category(category_name, patterns, description)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Failed to add category: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/backup', methods=['POST'])
@login_required
@admin_required
def create_aiml_backup():
    """Create backup of AIML files"""
    try:
        data = request.get_json() or {}
        description = data.get('description', 'Manual backup')
        
        backup_id = bulk_editor.create_backup(description=description)
        
        return success_response({
            'backup_id': backup_id,
            'message': 'Backup created successfully',
            'description': description
        })
    except Exception as e:
        return error_response(f"Backup failed: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/restore', methods=['POST'])
@login_required
@admin_required
def restore_aiml_backup():
    """Restore from backup"""
    try:
        data = request.get_json()
        backup_id = data.get('backup_id', '').strip()
        preview = data.get('preview', True)
        
        if not backup_id:
            return error_response('Backup ID required', 400)
        
        result = bulk_editor.restore_from_backup(backup_id, preview=preview)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Restore failed: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/backups', methods=['GET'])
@login_required
@admin_required
def get_backup_history():
    """Get backup history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        backups = bulk_editor.get_backup_history(limit)
        
        return success_response({
            'backups': backups,
            'count': len(backups)
        })
    except Exception as e:
        return error_response(f"Failed to get backups: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/validate', methods=['POST'])
@login_required
@admin_required
def validate_aiml_file():
    """Validate AIML file syntax"""
    try:
        data = request.get_json()
        filename = data.get('filename', '').strip()
        
        if not filename:
            return error_response('Filename required', 400)
        
        # Security check
        if '..' in filename or '/' in filename or '\\' in filename:
            return error_response('Invalid filename', 400)
        
        filepath = os.path.join(aiml_dir, filename)
        
        if not os.path.exists(filepath):
            return error_response('File not found', 404)
        
        result = bulk_editor.validate_aiml_syntax(filepath)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Validation failed: {str(e)}", 500)


@admin_advanced_bp.route('/aiml/stats', methods=['GET'])
@login_required
@admin_required
def get_pattern_statistics():
    """Get pattern statistics"""
    try:
        stats = bulk_editor.get_pattern_statistics()
        
        return success_response(stats)
    except Exception as e:
        return error_response(f"Failed to get statistics: {str(e)}", 500)


# ==================== PATTERN TESTING SANDBOX ====================

@admin_advanced_bp.route('/test/create-sandbox', methods=['POST'])
@login_required
@admin_required
def create_test_sandbox():
    """Create new testing sandbox"""
    try:
        data = request.get_json() or {}
        copy_production = data.get('copy_production', False)
        
        sandbox_id = sandbox.create_sandbox_environment(copy_production)
        
        return success_response({
            'sandbox_id': sandbox_id,
            'message': 'Sandbox created successfully'
        })
    except Exception as e:
        return error_response(f"Failed to create sandbox: {str(e)}", 500)


@admin_advanced_bp.route('/test/load-patterns', methods=['POST'])
@login_required
@admin_required
def load_test_patterns():
    """Load patterns into sandbox"""
    try:
        data = request.get_json()
        sandbox_id = data.get('sandbox_id', '').strip()
        patterns = data.get('patterns', [])
        
        if not sandbox_id:
            return error_response('Sandbox ID required', 400)
        
        if not patterns:
            return error_response('Patterns required', 400)
        
        result = sandbox.load_test_patterns(patterns, sandbox_id)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Failed to load patterns: {str(e)}", 500)


@admin_advanced_bp.route('/test/run', methods=['POST'])
@login_required
@admin_required
def run_pattern_test():
    """Test pattern in sandbox"""
    try:
        data = request.get_json()
        input_text = data.get('input', '').strip()
        sandbox_id = data.get('sandbox_id')
        
        if not input_text:
            return error_response('Input text required', 400)
        
        result = sandbox.test_pattern(input_text, sandbox_id)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Test failed: {str(e)}", 500)


@admin_advanced_bp.route('/test/batch', methods=['POST'])
@login_required
@admin_required
def batch_test_patterns():
    """Run batch tests"""
    try:
        data = request.get_json()
        test_cases = data.get('test_cases', [])
        sandbox_id = data.get('sandbox_id')
        
        if not test_cases:
            return error_response('Test cases required', 400)
        
        result = sandbox.batch_test_patterns(test_cases, sandbox_id)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Batch test failed: {str(e)}", 500)


@admin_advanced_bp.route('/test/ab-create', methods=['POST'])
@login_required
@admin_required
def create_ab_test():
    """Create A/B test"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        variant_a = data.get('variant_a', [])
        variant_b = data.get('variant_b', [])
        metric = data.get('metric', 'satisfaction')
        duration_days = data.get('duration_days', 7)
        
        if not name:
            return error_response('Test name required', 400)
        
        if not variant_a or not variant_b:
            return error_response('Both variants required', 400)
        
        test_id = sandbox.create_ab_test(name, variant_a, variant_b, metric, duration_days)
        
        return success_response({
            'test_id': test_id,
            'message': 'A/B test created successfully',
            'name': name
        })
    except Exception as e:
        return error_response(f"Failed to create A/B test: {str(e)}", 500)


@admin_advanced_bp.route('/test/ab-results/<test_id>', methods=['GET'])
@login_required
@admin_required
def get_ab_test_results(test_id):
    """Get A/B test results"""
    try:
        results = sandbox.get_ab_test_results(test_id)
        
        return success_response(results)
    except Exception as e:
        return error_response(f"Failed to get results: {str(e)}", 500)


@admin_advanced_bp.route('/test/preview', methods=['POST'])
@login_required
@admin_required
def preview_pattern_changes():
    """Preview changes before deployment"""
    try:
        data = request.get_json()
        old_patterns = data.get('old_patterns', [])
        new_patterns = data.get('new_patterns', [])
        test_inputs = data.get('test_inputs', [])
        
        result = sandbox.preview_changes(old_patterns, new_patterns, test_inputs)
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Preview failed: {str(e)}", 500)


@admin_advanced_bp.route('/test/deploy', methods=['POST'])
@login_required
@admin_required
def deploy_from_sandbox():
    """Deploy patterns from sandbox to production"""
    try:
        data = request.get_json()
        sandbox_id = data.get('sandbox_id', '').strip()
        patterns = data.get('patterns', [])
        
        if not sandbox_id:
            return error_response('Sandbox ID required', 400)
        
        result = sandbox.deploy_from_sandbox(sandbox_id, patterns)
        
        # Reload AIML engine
        current_app.aiml_engine.reload_patterns()
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Deployment failed: {str(e)}", 500)


# ==================== PERFORMANCE MONITORING ====================

@admin_advanced_bp.route('/performance/metrics', methods=['GET'])
@login_required
@admin_required
def get_performance_metrics():
    """Get current system performance metrics"""
    try:
        system_metrics = performance_monitor.get_system_metrics()
        process_metrics = performance_monitor.get_process_metrics()
        uptime = performance_monitor.get_uptime()
        
        return success_response({
            'system': system_metrics,
            'process': process_metrics,
            'uptime': uptime
        })
    except Exception as e:
        return error_response(f"Failed to get metrics: {str(e)}", 500)


@admin_advanced_bp.route('/performance/requests', methods=['GET'])
@login_required
@admin_required
def get_request_analytics():
    """Get request analytics"""
    try:
        minutes = request.args.get('minutes', 60, type=int)
        
        analytics = performance_monitor.get_request_analytics(minutes)
        
        return success_response(analytics)
    except Exception as e:
        return error_response(f"Failed to get analytics: {str(e)}", 500)


@admin_advanced_bp.route('/performance/slow-endpoints', methods=['GET'])
@login_required
@admin_required
def get_slow_endpoints():
    """Get slowest endpoints"""
    try:
        threshold_ms = request.args.get('threshold', 1000, type=float)
        limit = request.args.get('limit', 10, type=int)
        
        slow_endpoints = performance_monitor.get_slow_endpoints(threshold_ms, limit)
        
        return success_response({
            'endpoints': slow_endpoints,
            'count': len(slow_endpoints),
            'threshold_ms': threshold_ms
        })
    except Exception as e:
        return error_response(f"Failed to get slow endpoints: {str(e)}", 500)


@admin_advanced_bp.route('/performance/slow-queries', methods=['GET'])
@login_required
@admin_required
def get_slow_queries():
    """Get slowest database queries"""
    try:
        threshold_ms = request.args.get('threshold', 100, type=float)
        limit = request.args.get('limit', 10, type=int)
        
        slow_queries = performance_monitor.get_slow_queries(threshold_ms, limit)
        
        return success_response({
            'queries': slow_queries,
            'count': len(slow_queries),
            'threshold_ms': threshold_ms
        })
    except Exception as e:
        return error_response(f"Failed to get slow queries: {str(e)}", 500)


@admin_advanced_bp.route('/performance/errors', methods=['GET'])
@login_required
@admin_required
def get_error_summary():
    """Get error summary"""
    try:
        hours = request.args.get('hours', 24, type=int)
        
        summary = performance_monitor.get_error_summary(hours)
        
        return success_response(summary)
    except Exception as e:
        return error_response(f"Failed to get errors: {str(e)}", 500)


@admin_advanced_bp.route('/performance/bottlenecks', methods=['GET'])
@login_required
@admin_required
def identify_bottlenecks():
    """Identify performance bottlenecks"""
    try:
        bottlenecks = performance_monitor.get_bottlenecks()
        
        return success_response(bottlenecks)
    except Exception as e:
        return error_response(f"Failed to identify bottlenecks: {str(e)}", 500)


# ==================== RATE LIMITING ====================

@admin_advanced_bp.route('/rate-limit/stats', methods=['GET'])
@login_required
@admin_required
def get_rate_limit_stats():
    """Get rate limiting statistics"""
    try:
        hours = request.args.get('hours', 24, type=int)
        identifier = request.args.get('identifier')
        
        stats = rate_limiter.get_usage_stats(identifier, hours)
        
        return success_response(stats)
    except Exception as e:
        return error_response(f"Failed to get stats: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/violations', methods=['GET'])
@login_required
@admin_required
def get_rate_violations():
    """Get rate limit violations"""
    try:
        hours = request.args.get('hours', 24, type=int)
        identifier = request.args.get('identifier')
        
        violations = rate_limiter.get_violations(hours, identifier)
        
        return success_response({
            'violations': violations,
            'count': len(violations)
        })
    except Exception as e:
        return error_response(f"Failed to get violations: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/set-limit', methods=['POST'])
@login_required
@admin_required
def set_custom_rate_limit():
    """Set custom rate limit for user/IP"""
    try:
        data = request.get_json()
        identifier = data.get('identifier', '').strip()
        limit_type = data.get('type', 'ip')  # 'ip' or 'user'
        limits = data.get('limits', {})
        
        if not identifier:
            return error_response('Identifier required', 400)
        
        if limit_type not in ['ip', 'user']:
            return error_response('Invalid limit type', 400)
        
        required_keys = ['requests_per_minute', 'requests_per_hour', 'requests_per_day']
        if not all(key in limits for key in required_keys):
            return error_response('All limit values required', 400)
        
        rate_limiter.set_custom_limit(identifier, limit_type, limits)
        
        return success_response({
            'message': 'Custom limit set successfully',
            'identifier': identifier,
            'limits': limits
        })
    except Exception as e:
        return error_response(f"Failed to set limit: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/block', methods=['POST'])
@login_required
@admin_required
def block_ip_address():
    """Block an IP address"""
    try:
        data = request.get_json()
        ip_address = data.get('ip', '').strip()
        reason = data.get('reason', 'Manual block by admin')
        
        if not ip_address:
            return error_response('IP address required', 400)
        
        rate_limiter.block_ip(ip_address, reason)
        
        return success_response({
            'message': 'IP blocked successfully',
            'ip': ip_address,
            'reason': reason
        })
    except Exception as e:
        return error_response(f"Failed to block IP: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/unblock', methods=['POST'])
@login_required
@admin_required
def unblock_ip_address():
    """Unblock an IP address"""
    try:
        data = request.get_json()
        ip_address = data.get('ip', '').strip()
        
        if not ip_address:
            return error_response('IP address required', 400)
        
        rate_limiter.unblock_ip(ip_address)
        
        return success_response({
            'message': 'IP unblocked successfully',
            'ip': ip_address
        })
    except Exception as e:
        return error_response(f"Failed to unblock IP: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/abuse-suspects', methods=['GET'])
@login_required
@admin_required
def get_abuse_suspects():
    """Get suspected abusive users"""
    try:
        threshold = request.args.get('threshold', 2.0, type=float)
        
        suspects = rate_limiter.get_abuse_suspects(threshold)
        
        return success_response({
            'suspects': suspects,
            'count': len(suspects),
            'threshold': threshold
        })
    except Exception as e:
        return error_response(f"Failed to get suspects: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/auto-block', methods=['POST'])
@login_required
@admin_required
def auto_block_abusers():
    """Automatically block abusive users"""
    try:
        data = request.get_json() or {}
        threshold_score = data.get('threshold_score', 5)
        
        blocked = rate_limiter.auto_block_abusers(threshold_score)
        
        return success_response({
            'message': f'Blocked {len(blocked)} abusive identifiers',
            'blocked': blocked,
            'count': len(blocked)
        })
    except Exception as e:
        return error_response(f"Auto-block failed: {str(e)}", 500)


@admin_advanced_bp.route('/rate-limit/analytics', methods=['GET'])
@login_required
@admin_required
def get_rate_limit_analytics():
    """Get comprehensive rate limiting analytics"""
    try:
        hours = request.args.get('hours', 24, type=int)
        
        analytics = rate_limiter.get_analytics(hours)
        
        return success_response(analytics)
    except Exception as e:
        return error_response(f"Failed to get analytics: {str(e)}", 500)
