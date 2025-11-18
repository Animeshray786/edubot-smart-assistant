"""
Pattern Testing Sandbox
Test new patterns, A/B testing, preview changes, rollback capability
"""
import os
import tempfile
import shutil
from typing import Dict, List
from datetime import datetime
import xml.etree.ElementTree as ET


class PatternTestingSandbox:
    """Sandbox environment for testing AIML patterns safely"""
    
    def __init__(self, aiml_dir: str):
        self.aiml_dir = aiml_dir
        self.sandbox_dir = os.path.join(tempfile.gettempdir(), 'aiml_sandbox')
        self.test_results = {}
        os.makedirs(self.sandbox_dir, exist_ok=True)
    
    def create_sandbox(self, session_id: str = None) -> str:
        """
        Create isolated sandbox environment
        
        Args:
            session_id: Optional session identifier
            
        Returns:
            Sandbox session ID
        """
        if session_id is None:
            session_id = f"sandbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        os.makedirs(sandbox_path, exist_ok=True)
        
        # Copy all AIML files to sandbox
        for filename in os.listdir(self.aiml_dir):
            if filename.endswith('.xml') and not filename.startswith('_'):
                src = os.path.join(self.aiml_dir, filename)
                dst = os.path.join(sandbox_path, filename)
                shutil.copy2(src, dst)
        
        return session_id
    
    def add_test_pattern(self, session_id: str, pattern: str, 
                        template: str, category: str = None) -> Dict:
        """
        Add pattern to sandbox for testing
        
        Args:
            session_id: Sandbox session ID
            pattern: Pattern text
            template: Template response
            category: Category/topic
            
        Returns:
            Result dictionary
        """
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        
        if not os.path.exists(sandbox_path):
            return {'error': 'Sandbox session not found'}
        
        # Determine which file to add to
        if category:
            filename = f"{category}.xml"
        else:
            filename = "test_patterns.xml"
        
        filepath = os.path.join(sandbox_path, filename)
        
        try:
            # Load or create file
            if os.path.exists(filepath):
                tree = ET.parse(filepath)
                root = tree.getroot()
            else:
                root = ET.Element('aiml', version='2.0')
                tree = ET.ElementTree(root)
            
            # Add new category
            category_elem = ET.SubElement(root, 'category')
            pattern_elem = ET.SubElement(category_elem, 'pattern')
            pattern_elem.text = pattern.upper()
            template_elem = ET.SubElement(category_elem, 'template')
            template_elem.text = template
            
            # Save
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            
            return {
                'success': True,
                'file': filename,
                'pattern_id': f"{filename}_{len(root.findall('category')) - 1}"
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def test_pattern(self, session_id: str, test_input: str, 
                     aiml_engine=None) -> Dict:
        """
        Test a pattern with sample input
        
        Args:
            session_id: Sandbox session ID
            test_input: Test query
            aiml_engine: AIML engine instance
            
        Returns:
            Test result
        """
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        
        if not os.path.exists(sandbox_path):
            return {'error': 'Sandbox session not found'}
        
        # Simulate AIML engine response
        # In production, you would load sandbox patterns into engine
        result = {
            'input': test_input,
            'matched_pattern': None,
            'response': None,
            'confidence': 0.0,
            'file': None,
            'execution_time': 0.0
        }
        
        # Simple pattern matching (placeholder)
        # Real implementation would use actual AIML engine
        patterns = self._get_sandbox_patterns(session_id)
        
        for pattern_data in patterns:
            pattern = pattern_data['pattern']
            
            # Simple wildcard matching
            if self._pattern_matches(pattern, test_input):
                result['matched_pattern'] = pattern
                result['response'] = pattern_data['template']
                result['confidence'] = 0.95
                result['file'] = pattern_data['file']
                break
        
        # Log test
        if session_id not in self.test_results:
            self.test_results[session_id] = []
        
        self.test_results[session_id].append({
            'timestamp': datetime.now(),
            'test': result
        })
        
        return result
    
    def _get_sandbox_patterns(self, session_id: str) -> List[Dict]:
        """Get all patterns from sandbox"""
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        patterns = []
        
        for filename in os.listdir(sandbox_path):
            if filename.endswith('.xml'):
                filepath = os.path.join(sandbox_path, filename)
                
                try:
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    
                    for category in root.findall('.//category'):
                        pattern_elem = category.find('pattern')
                        template_elem = category.find('template')
                        
                        if pattern_elem is not None and template_elem is not None:
                            patterns.append({
                                'pattern': pattern_elem.text or '',
                                'template': template_elem.text or '',
                                'file': filename
                            })
                except:
                    pass
        
        return patterns
    
    def _pattern_matches(self, pattern: str, input_text: str) -> bool:
        """Simple pattern matching (placeholder)"""
        pattern_lower = pattern.lower()
        input_lower = input_text.lower()
        
        # Handle wildcards
        if '*' in pattern_lower:
            parts = pattern_lower.split('*')
            if all(part in input_lower for part in parts if part):
                return True
        
        # Exact match
        return pattern_lower == input_lower
    
    def run_ab_test(self, session_id: str, pattern_a: Dict, 
                    pattern_b: Dict, test_queries: List[str]) -> Dict:
        """
        Run A/B test between two patterns
        
        Args:
            session_id: Sandbox session ID
            pattern_a: First pattern variant
            pattern_b: Second pattern variant
            test_queries: List of test queries
            
        Returns:
            A/B test results
        """
        results = {
            'pattern_a': {
                'pattern': pattern_a,
                'matches': 0,
                'responses': []
            },
            'pattern_b': {
                'pattern': pattern_b,
                'matches': 0,
                'responses': []
            },
            'test_queries': test_queries,
            'timestamp': datetime.now().isoformat()
        }
        
        # Test pattern A
        session_a = self.create_sandbox(f"{session_id}_a")
        self.add_test_pattern(session_a, pattern_a['pattern'], pattern_a['template'])
        
        for query in test_queries:
            result = self.test_pattern(session_a, query)
            if result['matched_pattern']:
                results['pattern_a']['matches'] += 1
                results['pattern_a']['responses'].append({
                    'query': query,
                    'response': result['response']
                })
        
        # Test pattern B
        session_b = self.create_sandbox(f"{session_id}_b")
        self.add_test_pattern(session_b, pattern_b['pattern'], pattern_b['template'])
        
        for query in test_queries:
            result = self.test_pattern(session_b, query)
            if result['matched_pattern']:
                results['pattern_b']['matches'] += 1
                results['pattern_b']['responses'].append({
                    'query': query,
                    'response': result['response']
                })
        
        # Calculate winner
        if results['pattern_a']['matches'] > results['pattern_b']['matches']:
            results['winner'] = 'A'
        elif results['pattern_b']['matches'] > results['pattern_a']['matches']:
            results['winner'] = 'B'
        else:
            results['winner'] = 'tie'
        
        # Cleanup test sandboxes
        self.delete_sandbox(session_a)
        self.delete_sandbox(session_b)
        
        return results
    
    def preview_changes(self, session_id: str) -> Dict:
        """
        Preview changes made in sandbox vs production
        
        Args:
            session_id: Sandbox session ID
            
        Returns:
            Diff of changes
        """
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        
        if not os.path.exists(sandbox_path):
            return {'error': 'Sandbox session not found'}
        
        changes = {
            'added': [],
            'modified': [],
            'deleted': [],
            'unchanged': []
        }
        
        # Compare files
        sandbox_files = set(os.listdir(sandbox_path))
        prod_files = set(f for f in os.listdir(self.aiml_dir) if f.endswith('.xml'))
        
        changes['added'] = list(sandbox_files - prod_files)
        changes['deleted'] = list(prod_files - sandbox_files)
        
        # Check modifications
        for filename in sandbox_files & prod_files:
            sandbox_file = os.path.join(sandbox_path, filename)
            prod_file = os.path.join(self.aiml_dir, filename)
            
            with open(sandbox_file, 'r', encoding='utf-8') as f1:
                sandbox_content = f1.read()
            
            with open(prod_file, 'r', encoding='utf-8') as f2:
                prod_content = f2.read()
            
            if sandbox_content != prod_content:
                changes['modified'].append(filename)
            else:
                changes['unchanged'].append(filename)
        
        return changes
    
    def apply_to_production(self, session_id: str, create_backup: bool = True) -> Dict:
        """
        Apply sandbox changes to production
        
        Args:
            session_id: Sandbox session ID
            create_backup: Create backup before applying
            
        Returns:
            Result dictionary
        """
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        
        if not os.path.exists(sandbox_path):
            return {'error': 'Sandbox session not found'}
        
        try:
            # Create backup
            if create_backup:
                backup_dir = os.path.join(self.aiml_dir, '_backups')
                os.makedirs(backup_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = os.path.join(backup_dir, f'backup_{timestamp}')
                os.makedirs(backup_path, exist_ok=True)
                
                for filename in os.listdir(self.aiml_dir):
                    if filename.endswith('.xml') and not filename.startswith('_'):
                        shutil.copy2(
                            os.path.join(self.aiml_dir, filename),
                            os.path.join(backup_path, filename)
                        )
            
            # Apply changes
            for filename in os.listdir(sandbox_path):
                if filename.endswith('.xml'):
                    shutil.copy2(
                        os.path.join(sandbox_path, filename),
                        os.path.join(self.aiml_dir, filename)
                    )
            
            return {
                'success': True,
                'backup_id': timestamp if create_backup else None,
                'files_updated': len([f for f in os.listdir(sandbox_path) if f.endswith('.xml')])
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def delete_sandbox(self, session_id: str) -> bool:
        """Delete sandbox session"""
        sandbox_path = os.path.join(self.sandbox_dir, session_id)
        
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)
            return True
        
        return False
    
    def list_sandboxes(self) -> List[Dict]:
        """List all active sandboxes"""
        sandboxes = []
        
        for folder in os.listdir(self.sandbox_dir):
            folder_path = os.path.join(self.sandbox_dir, folder)
            
            if os.path.isdir(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
                
                sandboxes.append({
                    'session_id': folder,
                    'created': datetime.fromtimestamp(os.path.getctime(folder_path)),
                    'files_count': len(files),
                    'test_results': len(self.test_results.get(folder, []))
                })
        
        return sorted(sandboxes, key=lambda x: x['created'], reverse=True)
    
    def get_test_history(self, session_id: str) -> List[Dict]:
        """Get test history for a sandbox session"""
        return self.test_results.get(session_id, [])
