"""
Bulk AIML Editor
Edit multiple patterns at once, find & replace, batch operations
"""
import os
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple
from datetime import datetime
import shutil


class BulkAIMLEditor:
    """Bulk operations for AIML pattern files"""
    
    def __init__(self, aiml_dir: str):
        self.aiml_dir = aiml_dir
        self.backup_dir = os.path.join(aiml_dir, '_backups')
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def get_all_patterns(self) -> List[Dict]:
        """
        Get all patterns from all AIML files
        
        Returns:
            List of pattern dictionaries
        """
        all_patterns = []
        
        for filename in os.listdir(self.aiml_dir):
            if filename.endswith('.xml') and not filename.startswith('_'):
                filepath = os.path.join(self.aiml_dir, filename)
                patterns = self._extract_patterns_from_file(filepath)
                
                for pattern in patterns:
                    pattern['file'] = filename
                    pattern['filepath'] = filepath
                    all_patterns.append(pattern)
        
        return all_patterns
    
    def _extract_patterns_from_file(self, filepath: str) -> List[Dict]:
        """Extract all patterns from a single file"""
        patterns = []
        
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            for idx, category in enumerate(root.findall('.//category')):
                pattern_elem = category.find('pattern')
                template_elem = category.find('template')
                
                if pattern_elem is not None and template_elem is not None:
                    patterns.append({
                        'id': f"{os.path.basename(filepath)}_{idx}",
                        'pattern': pattern_elem.text or '',
                        'template': ET.tostring(template_elem, encoding='unicode', method='text').strip(),
                        'template_xml': ET.tostring(template_elem, encoding='unicode'),
                        'index': idx
                    })
        
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
        
        return patterns
    
    def search_patterns(self, query: str, search_in: str = 'both') -> List[Dict]:
        """
        Search patterns by text
        
        Args:
            query: Search query
            search_in: 'pattern', 'template', or 'both'
            
        Returns:
            Matching patterns
        """
        all_patterns = self.get_all_patterns()
        results = []
        
        query_lower = query.lower()
        
        for pattern in all_patterns:
            match = False
            
            if search_in in ['pattern', 'both']:
                if query_lower in pattern['pattern'].lower():
                    match = True
            
            if search_in in ['template', 'both']:
                if query_lower in pattern['template'].lower():
                    match = True
            
            if match:
                results.append(pattern)
        
        return results
    
    def find_and_replace(self, find_text: str, replace_text: str, 
                        files: List[str] = None, search_in: str = 'template',
                        case_sensitive: bool = False) -> Dict:
        """
        Find and replace text across AIML files
        
        Args:
            find_text: Text to find
            replace_text: Text to replace with
            files: Specific files to search (None = all files)
            search_in: 'pattern', 'template', or 'both'
            case_sensitive: Case sensitive search
            
        Returns:
            Dictionary with results
        """
        # Create backup first
        backup_id = self._create_backup()
        
        replacements = []
        errors = []
        
        files_to_process = files or [
            f for f in os.listdir(self.aiml_dir) 
            if f.endswith('.xml') and not f.startswith('_')
        ]
        
        for filename in files_to_process:
            filepath = os.path.join(self.aiml_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                modified = False
                
                if search_in in ['pattern', 'both']:
                    pattern = find_text if case_sensitive else f'(?i){re.escape(find_text)}'
                    if re.search(pattern, content):
                        content = re.sub(pattern, replace_text, content)
                        modified = True
                
                if search_in in ['template', 'both']:
                    # Replace in template tags
                    pattern = find_text if case_sensitive else f'(?i){re.escape(find_text)}'
                    if re.search(pattern, content):
                        content = re.sub(pattern, replace_text, content)
                        modified = True
                
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    replacements.append({
                        'file': filename,
                        'count': content.count(replace_text) - original_content.count(replace_text)
                    })
            
            except Exception as e:
                errors.append({
                    'file': filename,
                    'error': str(e)
                })
        
        return {
            'success': len(errors) == 0,
            'backup_id': backup_id,
            'replacements': replacements,
            'errors': errors,
            'total_replacements': sum(r['count'] for r in replacements),
            'files_modified': len(replacements)
        }
    
    def batch_update_patterns(self, updates: List[Dict]) -> Dict:
        """
        Update multiple patterns at once
        
        Args:
            updates: List of {pattern_id, new_pattern, new_template}
            
        Returns:
            Results dictionary
        """
        backup_id = self._create_backup()
        
        successful = []
        failed = []
        
        # Group updates by file
        file_updates = {}
        for update in updates:
            pattern_id = update['pattern_id']
            file = pattern_id.split('_')[0]
            
            if file not in file_updates:
                file_updates[file] = []
            
            file_updates[file].append(update)
        
        # Process each file
        for filename, updates_list in file_updates.items():
            filepath = os.path.join(self.aiml_dir, filename)
            
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                for update in updates_list:
                    idx = int(update['pattern_id'].split('_')[1])
                    category = root.findall('.//category')[idx]
                    
                    if 'new_pattern' in update:
                        pattern_elem = category.find('pattern')
                        pattern_elem.text = update['new_pattern']
                    
                    if 'new_template' in update:
                        template_elem = category.find('template')
                        template_elem.text = update['new_template']
                    
                    successful.append(update['pattern_id'])
                
                tree.write(filepath, encoding='utf-8', xml_declaration=True)
            
            except Exception as e:
                failed.append({
                    'file': filename,
                    'error': str(e)
                })
        
        return {
            'success': len(failed) == 0,
            'backup_id': backup_id,
            'updated': len(successful),
            'failed': len(failed),
            'errors': failed
        }
    
    def _create_backup(self) -> str:
        """Create backup of all AIML files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_folder = os.path.join(self.backup_dir, f'backup_{timestamp}')
        os.makedirs(backup_folder, exist_ok=True)
        
        for filename in os.listdir(self.aiml_dir):
            if filename.endswith('.xml') and not filename.startswith('_'):
                src = os.path.join(self.aiml_dir, filename)
                dst = os.path.join(backup_folder, filename)
                shutil.copy2(src, dst)
        
        return timestamp
    
    def restore_backup(self, backup_id: str) -> bool:
        """Restore from backup"""
        backup_folder = os.path.join(self.backup_dir, f'backup_{backup_id}')
        
        if not os.path.exists(backup_folder):
            return False
        
        try:
            for filename in os.listdir(backup_folder):
                src = os.path.join(backup_folder, filename)
                dst = os.path.join(self.aiml_dir, filename)
                shutil.copy2(src, dst)
            
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        
        for folder in os.listdir(self.backup_dir):
            if folder.startswith('backup_'):
                backup_id = folder.replace('backup_', '')
                folder_path = os.path.join(self.backup_dir, folder)
                
                files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
                
                backups.append({
                    'id': backup_id,
                    'timestamp': datetime.strptime(backup_id, '%Y%m%d_%H%M%S'),
                    'files_count': len(files),
                    'size': sum(
                        os.path.getsize(os.path.join(folder_path, f)) 
                        for f in files
                    )
                })
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)
    
    def validate_aiml_syntax(self, filename: str = None) -> Dict:
        """
        Validate AIML syntax
        
        Args:
            filename: Specific file to validate (None = all files)
            
        Returns:
            Validation results
        """
        files_to_check = [filename] if filename else [
            f for f in os.listdir(self.aiml_dir) 
            if f.endswith('.xml') and not f.startswith('_')
        ]
        
        results = {
            'valid': [],
            'invalid': [],
            'warnings': []
        }
        
        for file in files_to_check:
            filepath = os.path.join(self.aiml_dir, file)
            
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                # Check for basic structure
                categories = root.findall('.//category')
                
                if len(categories) == 0:
                    results['warnings'].append({
                        'file': file,
                        'message': 'No categories found'
                    })
                
                for idx, category in enumerate(categories):
                    if category.find('pattern') is None:
                        results['invalid'].append({
                            'file': file,
                            'line': idx,
                            'error': 'Missing pattern element'
                        })
                    
                    if category.find('template') is None:
                        results['invalid'].append({
                            'file': file,
                            'line': idx,
                            'error': 'Missing template element'
                        })
                
                if file not in [r['file'] for r in results['invalid']]:
                    results['valid'].append(file)
            
            except ET.ParseError as e:
                results['invalid'].append({
                    'file': file,
                    'error': str(e)
                })
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics about AIML files"""
        all_patterns = self.get_all_patterns()
        
        files_stats = {}
        for pattern in all_patterns:
            file = pattern['file']
            if file not in files_stats:
                files_stats[file] = {
                    'pattern_count': 0,
                    'avg_pattern_length': 0,
                    'avg_template_length': 0,
                    'patterns': []
                }
            
            files_stats[file]['pattern_count'] += 1
            files_stats[file]['patterns'].append(pattern)
        
        # Calculate averages
        for file, stats in files_stats.items():
            patterns = stats['patterns']
            stats['avg_pattern_length'] = sum(len(p['pattern']) for p in patterns) / len(patterns)
            stats['avg_template_length'] = sum(len(p['template']) for p in patterns) / len(patterns)
            del stats['patterns']  # Remove to reduce size
        
        return {
            'total_files': len(files_stats),
            'total_patterns': len(all_patterns),
            'files': files_stats,
            'backups_available': len(self.list_backups())
        }
