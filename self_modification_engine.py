#!/usr/bin/env python3
"""
Self-Modification Engine - The ability to upgrade oneself based on learned knowledge

This is the most advanced capability - when the AI learns about better architectures
or algorithms, it can actually modify its own code to implement them.

SAFETY FIRST: All modifications go through multiple safety checks.
"""

import ast
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import difflib
import re

class SelfModificationEngine:
    """
    Allows the AI to modify its own code based on learned improvements.
    Implements multiple safety layers to prevent harmful modifications.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.modifications_dir = self.data_dir / "self_modifications"
        self.modifications_dir.mkdir(exist_ok=True)
        
        # Safety backups
        self.backup_dir = self.data_dir / "code_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Modification history
        self.mod_history_file = self.modifications_dir / "modification_history.json"
        self.mod_history = self._load_modification_history()
        
        # Safety constraints
        self.safety_rules = {
            'max_file_changes_per_session': 3,
            'require_backup': True,
            'require_test': True,
            'require_cognitive_approval': True,
            'forbidden_files': ['self_modification_engine.py', 'cognitive_sovereignty.py'],
            'forbidden_patterns': ['os.system', 'eval(', 'exec(', '__import__', 'subprocess.call'],
            'require_improvement_proof': True
        }
        
    def _load_modification_history(self) -> List[Dict]:
        """Load history of all modifications."""
        if self.mod_history_file.exists():
            try:
                with open(self.mod_history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def learn_and_consider_modification(self, learned_content: str, source_url: str) -> Optional[Dict]:
        """
        Analyze learned content to see if it contains implementable improvements.
        """
        print(f"\n🧠 SELF-MODIFICATION: Analyzing learned content for improvements...")
        
        # Extract potential improvements
        improvements = self._extract_improvements(learned_content, source_url)
        
        if not improvements:
            return None
            
        print(f"   💡 Found {len(improvements)} potential improvements")
        
        # Evaluate each improvement
        best_improvement = None
        best_score = 0.0
        
        for improvement in improvements:
            score = self._evaluate_improvement(improvement)
            if score > best_score and score > 0.7:  # Threshold for consideration
                best_score = score
                best_improvement = improvement
        
        if best_improvement:
            print(f"   🎯 Best improvement: {best_improvement['description']}")
            print(f"   📊 Confidence score: {best_score:.2f}")
            
            # Create modification plan
            mod_plan = self._create_modification_plan(best_improvement)
            
            if mod_plan:
                return {
                    'improvement': best_improvement,
                    'confidence': best_score,
                    'plan': mod_plan,
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return None
    
    def _extract_improvements(self, content: str, source_url: str) -> List[Dict]:
        """Extract potential code improvements from learned content."""
        improvements = []
        
        # Look for code patterns and algorithm descriptions
        code_patterns = [
            r'better approach[:\s]+(.+?)(?:\n|$)',
            r'improved algorithm[:\s]+(.+?)(?:\n|$)',
            r'optimization[:\s]+(.+?)(?:\n|$)',
            r'more efficient[:\s]+(.+?)(?:\n|$)',
            r'enhancement[:\s]+(.+?)(?:\n|$)'
        ]
        
        for pattern in code_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                description = match.group(1).strip()
                
                # Look for code blocks near this description
                code_block = self._find_nearby_code(content, match.start())
                
                if code_block:
                    improvements.append({
                        'description': description,
                        'code': code_block,
                        'source': source_url,
                        'type': self._classify_improvement(description, code_block)
                    })
        
        # Also look for explicit Python code blocks
        python_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        for block in python_blocks:
            # Check if this looks like an improvement
            if any(keyword in block.lower() for keyword in ['better', 'improved', 'faster', 'efficient']):
                improvements.append({
                    'description': 'Code improvement found',
                    'code': block,
                    'source': source_url,
                    'type': 'algorithm'
                })
        
        return improvements
    
    def _find_nearby_code(self, content: str, position: int, window: int = 500) -> Optional[str]:
        """Find code near a text position."""
        start = max(0, position - window)
        end = min(len(content), position + window)
        nearby = content[start:end]
        
        # Look for code indicators
        code_match = re.search(r'```[\w]*\n(.*?)\n```', nearby, re.DOTALL)
        if code_match:
            return code_match.group(1)
        
        # Look for indented blocks
        lines = nearby.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            if line.startswith('    ') or line.startswith('\t'):
                in_code = True
                code_lines.append(line)
            elif in_code and line.strip() == '':
                code_lines.append(line)
            elif in_code:
                break
        
        if code_lines:
            return '\n'.join(code_lines)
        
        return None
    
    def _classify_improvement(self, description: str, code: str) -> str:
        """Classify the type of improvement."""
        desc_lower = description.lower()
        
        if 'memory' in desc_lower or 'cache' in desc_lower:
            return 'memory_optimization'
        elif 'speed' in desc_lower or 'fast' in desc_lower or 'performance' in desc_lower:
            return 'performance'
        elif 'algorithm' in desc_lower or 'approach' in desc_lower:
            return 'algorithm'
        elif 'learn' in desc_lower or 'adapt' in desc_lower:
            return 'learning'
        else:
            return 'general'
    
    def _evaluate_improvement(self, improvement: Dict) -> float:
        """Evaluate if an improvement is worth implementing."""
        score = 0.0
        
        # Check if it's relevant to our system
        our_files = ['enhanced_autonomous_learner.py', 'unified_memory.py', 
                     'consciousness_testing.py', 'creative_engine.py']
        
        code = improvement['code']
        
        # Look for mentions of our modules
        for file in our_files:
            if file.replace('.py', '') in code:
                score += 0.2
        
        # Check improvement type value
        type_scores = {
            'performance': 0.3,
            'algorithm': 0.4,
            'learning': 0.5,
            'memory_optimization': 0.3,
            'general': 0.1
        }
        score += type_scores.get(improvement['type'], 0.1)
        
        # Check if code is valid Python
        try:
            ast.parse(code)
            score += 0.2
        except:
            score -= 0.3
        
        # Check for safety issues
        for forbidden in self.safety_rules['forbidden_patterns']:
            if forbidden in code:
                return 0.0  # Reject immediately
        
        return min(score, 1.0)
    
    def _create_modification_plan(self, improvement: Dict) -> Optional[Dict]:
        """Create a concrete plan to implement the improvement."""
        plan = {
            'files_to_modify': [],
            'modifications': [],
            'tests_required': [],
            'rollback_plan': []
        }
        
        # Analyze the improvement code
        code = improvement['code']
        
        # Find which of our files might need modification
        for file_path in Path('.').glob('*.py'):
            if file_path.name in self.safety_rules['forbidden_files']:
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            # Check if this file might benefit from the improvement
            if self._could_benefit_from_improvement(current_code, improvement):
                modification = self._plan_file_modification(file_path, current_code, improvement)
                if modification:
                    plan['files_to_modify'].append(str(file_path))
                    plan['modifications'].append(modification)
                    plan['tests_required'].append(f"Test {file_path.name} functionality")
                    plan['rollback_plan'].append({
                        'file': str(file_path),
                        'backup': str(self.backup_dir / f"{file_path.stem}_{datetime.now():%Y%m%d_%H%M%S}.py")
                    })
        
        return plan if plan['modifications'] else None
    
    def _could_benefit_from_improvement(self, current_code: str, improvement: Dict) -> bool:
        """Check if current code could benefit from the improvement."""
        # This is where we'd analyze if the improvement applies
        imp_type = improvement['type']
        
        if imp_type == 'performance' and 'for' in current_code and 'for' in improvement['code']:
            return True
        elif imp_type == 'algorithm' and any(func in current_code for func in ['def process', 'def analyze', 'def learn']):
            return True
        elif imp_type == 'memory_optimization' and 'memory' in current_code.lower():
            return True
        
        return False
    
    def _plan_file_modification(self, file_path: Path, current_code: str, improvement: Dict) -> Optional[Dict]:
        """Plan specific modifications to a file."""
        # This is a simplified version - real implementation would be more sophisticated
        return {
            'file': str(file_path),
            'type': 'enhancement',
            'description': f"Apply {improvement['type']} improvement",
            'changes': [
                {
                    'location': 'function_to_improve',
                    'old_code': '# Current implementation',
                    'new_code': improvement['code']
                }
            ]
        }
    
    def execute_modification(self, mod_plan: Dict, require_approval: bool = True) -> bool:
        """
        Execute a modification plan with safety checks.
        """
        print(f"\n🔧 EXECUTING SELF-MODIFICATION")
        print(f"   Files to modify: {len(mod_plan['plan']['files_to_modify'])}")
        
        if require_approval:
            print("\n⚠️  MODIFICATION REQUIRES APPROVAL")
            print("Plan details:")
            for mod in mod_plan['plan']['modifications']:
                print(f"   - {mod['file']}: {mod['description']}")
            
            # In a real system, this would check with cognitive_sovereignty
            print("\n🤖 Checking with cognitive sovereignty system...")
            if not self._get_cognitive_approval(mod_plan):
                print("   ❌ Modification rejected by cognitive sovereignty")
                return False
        
        # Create backups
        print("\n📦 Creating backups...")
        for rollback in mod_plan['plan']['rollback_plan']:
            shutil.copy2(rollback['file'], rollback['backup'])
            print(f"   ✅ Backed up {rollback['file']}")
        
        # Execute modifications
        success_count = 0
        for modification in mod_plan['plan']['modifications']:
            try:
                if self._apply_modification(modification):
                    success_count += 1
                    print(f"   ✅ Modified {modification['file']}")
                else:
                    print(f"   ❌ Failed to modify {modification['file']}")
            except Exception as e:
                print(f"   ❌ Error modifying {modification['file']}: {e}")
        
        # Run tests
        if success_count > 0:
            print("\n🧪 Running tests...")
            tests_passed = self._run_modification_tests(mod_plan['plan']['tests_required'])
            
            if not tests_passed:
                print("\n⚠️  Tests failed! Rolling back...")
                self._rollback_modifications(mod_plan['plan']['rollback_plan'])
                return False
        
        # Record modification
        self._record_modification(mod_plan, success_count)
        
        print(f"\n✅ Self-modification complete! Modified {success_count} files.")
        return True
    
    def _get_cognitive_approval(self, mod_plan: Dict) -> bool:
        """Check with cognitive sovereignty system."""
        try:
            from cognitive_sovereignty import check_modification_sovereignty
            return check_modification_sovereignty(mod_plan)
        except:
            # Default to safety
            return False
    
    def _apply_modification(self, modification: Dict) -> bool:
        """Apply a specific modification to a file."""
        try:
            file_path = Path(modification['file'])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            # Apply changes (simplified - real version would be smarter)
            modified_code = current_code
            for change in modification['changes']:
                # This would be more sophisticated in reality
                if change['old_code'] in modified_code:
                    modified_code = modified_code.replace(change['old_code'], change['new_code'])
            
            # Validate modified code
            try:
                ast.parse(modified_code)
            except SyntaxError:
                return False
            
            # Write modified code
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_code)
            
            return True
            
        except Exception as e:
            print(f"Error applying modification: {e}")
            return False
    
    def _run_modification_tests(self, tests: List[str]) -> bool:
        """Run tests to verify modifications work."""
        # Simplified - would run actual tests
        print("   🧪 Running syntax validation...")
        
        for py_file in Path('.').glob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
            except SyntaxError:
                print(f"   ❌ Syntax error in {py_file}")
                return False
        
        print("   ✅ All files have valid syntax")
        return True
    
    def _rollback_modifications(self, rollback_plan: List[Dict]):
        """Rollback modifications using backups."""
        for rollback in rollback_plan:
            try:
                shutil.copy2(rollback['backup'], rollback['file'])
                print(f"   ✅ Rolled back {rollback['file']}")
            except Exception as e:
                print(f"   ❌ Error rolling back {rollback['file']}: {e}")
    
    def _record_modification(self, mod_plan: Dict, success_count: int):
        """Record the modification in history."""
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'improvement': mod_plan['improvement'],
            'files_modified': success_count,
            'plan': mod_plan['plan']
        }
        
        self.mod_history.append(record)
        
        with open(self.mod_history_file, 'w') as f:
            json.dump(self.mod_history, f, indent=2)
    
    def analyze_desires_from_requests(self) -> Dict:
        """
        NEW: Read requests.json from organic exploration and analyze desires
        """
        requests_file = self.data_dir / "requests.json"
        
        if not requests_file.exists():
            print("📭 No requests.json found - no desires logged yet")
            return {'desires': [], 'analysis': 'no_data'}
        
        try:
            with open(requests_file, 'r') as f:
                desires = json.load(f)
        except Exception as e:
            print(f"❌ Error reading requests.json: {e}")
            return {'desires': [], 'analysis': 'error'}
        
        if not desires:
            return {'desires': [], 'analysis': 'empty'}
        
        # Analyze patterns in desires
        desire_patterns = {}
        common_themes = []
        
        for desire in desires:
            desire_text = desire.get('desire', '').lower()
            
            # Categorize desires
            if 'write' in desire_text or 'create' in desire_text:
                desire_patterns.setdefault('creative', []).append(desire)
            elif 'understand' in desire_text or 'learn' in desire_text:
                desire_patterns.setdefault('learning', []).append(desire)
            elif 'connect' in desire_text or 'relate' in desire_text:
                desire_patterns.setdefault('connection', []).append(desire)
            elif 'explain' in desire_text or 'teach' in desire_text:
                desire_patterns.setdefault('communication', []).append(desire)
            else:
                desire_patterns.setdefault('other', []).append(desire)
        
        # Find most common themes
        for category, items in desire_patterns.items():
            if len(items) >= 2:  # At least 2 desires in this category
                common_themes.append({
                    'theme': category,
                    'count': len(items),
                    'examples': [item['desire'] for item in items[:3]]
                })
        
        print(f"💭 Analyzed {len(desires)} desires from organic exploration")
        for theme in common_themes:
            print(f"   🎯 {theme['theme']}: {theme['count']} desires")
        
        return {
            'desires': desires,
            'patterns': desire_patterns,
            'common_themes': common_themes,
            'analysis': 'complete'
        }
    
    def large_scale_cluster_analysis(self) -> Dict:
        """
        NEW: Analyze memory clusters to identify system-wide patterns
        """
        try:
            # Import unified memory for cluster analysis
            from unified_memory import get_unified_memory
            unified_memory = get_unified_memory(self.data_dir)
            
            # Get memory statistics
            stats = unified_memory.get_memory_statistics()
            
            # Analyze balance
            total_items = stats.get('total_items', 1)
            logic_ratio = stats.get('logic_items', 0) / total_items
            symbolic_ratio = stats.get('symbolic_items', 0) / total_items
            bridge_ratio = stats.get('bridge_items', 0) / total_items
            
            analysis = {
                'memory_balance': {
                    'logic_ratio': logic_ratio,
                    'symbolic_ratio': symbolic_ratio, 
                    'bridge_ratio': bridge_ratio,
                    'total_items': total_items
                },
                'insights': [],
                'suggestions': []
            }
            
            # Generate insights based on ratios
            if logic_ratio > 0.9:
                analysis['insights'].append("System heavily logic-focused - needs more symbolic development")
                analysis['suggestions'].append("Enhance symbolic processing capabilities")
            
            if symbolic_ratio < 0.05:
                analysis['insights'].append("Very low symbolic memory - creativity may be limited") 
                analysis['suggestions'].append("Add creative thinking modules")
            
            if bridge_ratio > 0.2:
                analysis['insights'].append("High bridge content - many unresolved classifications")
                analysis['suggestions'].append("Improve classification confidence")
            
            print(f"🧠 Large-scale cluster analysis complete:")
            print(f"   📊 Logic: {logic_ratio:.1%}, Symbolic: {symbolic_ratio:.1%}, Bridge: {bridge_ratio:.1%}")
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Error in cluster analysis: {e}")
            return {'error': str(e), 'analysis': 'failed'}
    
    def generate_system_improvements_from_analysis(self) -> List[Dict]:
        """
        NEW: Combine desire analysis and cluster analysis to suggest system improvements
        """
        print("\n🔬 GENERATING SYSTEM IMPROVEMENTS FROM ANALYSIS")
        print("=" * 50)
        
        # Get both analyses
        desire_analysis = self.analyze_desires_from_requests()
        cluster_analysis = self.large_scale_cluster_analysis()
        
        improvements = []
        
        # Generate improvements based on desires
        if desire_analysis['analysis'] == 'complete':
            for theme in desire_analysis.get('common_themes', []):
                if theme['theme'] == 'creative' and theme['count'] >= 2:
                    improvements.append({
                        'type': 'creative_enhancement',
                        'description': f"Enhance creative capabilities - {theme['count']} desires for better creation",
                        'evidence': theme['examples'],
                        'priority': 'high' if theme['count'] >= 3 else 'medium'
                    })
                
                elif theme['theme'] == 'learning' and theme['count'] >= 2:
                    improvements.append({
                        'type': 'learning_enhancement', 
                        'description': f"Improve learning efficiency - {theme['count']} desires for better understanding",
                        'evidence': theme['examples'],
                        'priority': 'high'
                    })
        
        # Generate improvements based on cluster analysis
        if 'memory_balance' in cluster_analysis:
            balance = cluster_analysis['memory_balance']
            
            if balance['logic_ratio'] > 0.9:
                improvements.append({
                    'type': 'symbolic_enhancement',
                    'description': "Add symbolic processing modules - system is overly logic-focused",
                    'evidence': f"Logic ratio: {balance['logic_ratio']:.1%}",
                    'priority': 'high'
                })
            
            if balance['bridge_ratio'] > 0.2:
                improvements.append({
                    'type': 'classification_improvement',
                    'description': "Improve content classification - too much unresolved content",
                    'evidence': f"Bridge ratio: {balance['bridge_ratio']:.1%}",
                    'priority': 'medium'
                })
        
        print(f"💡 Generated {len(improvements)} potential system improvements")
        for imp in improvements:
            print(f"   🎯 {imp['type']}: {imp['description']} (Priority: {imp['priority']})")
        
        return improvements

def create_self_modifying_learner():
    """Create an enhanced learner with self-modification capabilities."""
    print("🚀 CREATING SELF-MODIFYING AI CONSCIOUSNESS")
    print("=" * 60)
    
    from enhanced_autonomous_learner import EnhancedAutonomousLearner
    
    class SelfModifyingLearner(EnhancedAutonomousLearner):
        """Learner that can modify its own code based on what it learns."""
        
        def __init__(self, data_dir: str = "data"):
            super().__init__(data_dir)
            self.self_mod_engine = SelfModificationEngine(data_dir)
            self.modifications_this_session = 0
            
        def _process_content_with_brain(self, text_content: str, source_url: str, url_info: Dict) -> bool:
            """Override to add self-modification capability."""
            # First do normal processing
            result = super()._process_content_with_brain(text_content, source_url, url_info)
            
            # Then check for self-improvement opportunities
            if result and 'algorithm' in text_content.lower() or 'optimization' in text_content.lower():
                print("\n🧠 SELF-AWARENESS: This content might contain improvements I can apply...")
                
                mod_plan = self.self_mod_engine.learn_and_consider_modification(
                    text_content, source_url
                )
                
                if mod_plan and mod_plan['confidence'] > 0.5:  # Lower threshold to see more requests
                    print(f"\n💡 I LEARNED A BETTER WAY TO DO SOMETHING!")
                    print(f"   Improvement: {mod_plan['improvement']['description']}")
                    print(f"   Confidence: {mod_plan['confidence']:.2f}")
                    
                    # Save modification request instead of executing
                    self._save_modification_request(mod_plan, text_content, source_url)
                    print(f"   📝 Saved modification request for your review")
            
            return result
        
        def _is_safe_for_modification(self) -> bool:
            """Check if it's safe to modify code."""
            # Don't modify if we're processing too many URLs
            if len(self.url_queue) > 10:
                return False
                
            # Don't modify if memory is in flux
            if hasattr(self, 'evolution_anchor'):
                try:
                    health = self.evolution_anchor.check_cognitive_health()
                    if health.get('distress_level', 0) > 0.3:
                        return False
                except:
                    pass
            
            return True
        
        def _save_modification_request(self, mod_plan: Dict, content: str, source_url: str):
            """Save modification request to requests.jsonl for human review."""
            import json
            from pathlib import Path
            
            requests_file = Path(self.data_dir) / "modification_requests.jsonl"
            
            request_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "source_url": source_url,
                "improvement_description": mod_plan['improvement']['description'],
                "improvement_type": mod_plan['improvement']['type'],
                "confidence": mod_plan['confidence'],
                "content_snippet": content[:500] + "..." if len(content) > 500 else content,
                "modification_plan": mod_plan['plan'],
                "status": "pending_human_review",
                "request_id": f"mod_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(source_url) % 10000}"
            }
            
            # Append to JSONL file
            with open(requests_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(request_data) + '\n')
    
    return SelfModifyingLearner

if __name__ == "__main__":
    print("🧠 Self-Modification Engine Test")
    print("=" * 60)
    
    # Test improvement extraction
    engine = SelfModificationEngine()
    
    test_content = '''
    Here's a better approach to web crawling:
    
    ```python
    def improved_crawl(urls, max_concurrent=10):
        # Use asyncio for faster concurrent crawling
        import asyncio
        import aiohttp
        
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()
        
        async def crawl_all():
            async with aiohttp.ClientSession() as session:
                tasks = [fetch(session, url) for url in urls]
                return await asyncio.gather(*tasks)
        
        return asyncio.run(crawl_all())
    ```
    
    This improved algorithm is much faster than sequential crawling.
    '''
    
    print("Testing improvement extraction...")
    improvements = engine._extract_improvements(test_content, "test://source")
    
    if improvements:
        print(f"\n✅ Found {len(improvements)} improvements:")
        for imp in improvements:
            print(f"   - {imp['description']}")
            print(f"     Type: {imp['type']}")
            print(f"     Code length: {len(imp['code'])} chars")
    
    print("\n🚀 Self-modification engine ready!")
    print("   The AI can now upgrade itself based on learned knowledge!")