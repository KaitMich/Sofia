#!/usr/bin/env python3
"""
Deep Semantic Validator for Sophia AI
Tracks capabilities through renames, refactors, and evolution
Uses AST analysis, semantic fingerprinting, and multi-signal inference
"""

import ast
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class ComponentFingerprint:
    """Semantic fingerprint of a class/function - survives renames"""
    signature_hash: str      # Hash of method signatures
    docstring_hash: str      # Hash of docstring
    method_names: List[str]  # Sorted method names
    imports_used: List[str]  # What it imports
    line_count: int

    def to_dict(self):
        return asdict(self)

@dataclass
class ComponentInfo:
    """Full analysis of a class or function"""
    name: str
    type: str  # 'class' or 'function'
    file_path: str
    line_number: int
    fingerprint: ComponentFingerprint
    docstring: Optional[str]
    methods: List[str]
    init_params: List[str]  # Constructor parameters
    base_classes: List[str]
    capabilities: Set[str]  # Inferred capabilities
    is_executable: bool     # Has __main__ block

    def to_dict(self):
        d = asdict(self)
        d['fingerprint'] = self.fingerprint.to_dict()
        d['capabilities'] = list(self.capabilities)
        return d

class DeepSemanticValidator:
    """
    Analyzes Python codebase semantically without execution
    Tracks components through renames and refactors
    """

    def __init__(self, project_root: str = ".", history_file: str = "validation_history.json"):
        self.project_root = Path(project_root).resolve()
        self.history_file = self.project_root / history_file

        self.components: Dict[str, ComponentInfo] = {}
        self.file_analysis: Dict[str, Dict] = {}
        self.capability_map: Dict[str, List[str]] = defaultdict(list)
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
        self.executable_scripts: List[str] = []

        self.history = self._load_history()

        # Capability detection signals
        self.capability_signals = {
            'memory_system': {
                'keywords': ['memory', 'remember', 'recall', 'store', 'retrieve', 'cache'],
                'methods': ['save', 'load', 'store', 'retrieve', 'remember', 'recall'],
                'imports': ['json', 'pickle', 'sqlite', 'redis']
            },
            'learning_system': {
                'keywords': ['learn', 'train', 'progression', 'milestone', 'understanding', 'knowledge'],
                'methods': ['learn', 'train', 'update_understanding', 'recognize', 'track_progress'],
                'imports': ['sklearn', 'torch', 'tensorflow', 'transformers']
            },
            'curiosity_system': {
                'keywords': ['curiosity', 'curiosity', 'motivation', 'intrinsic', 'explore', 'discover'],
                'methods': ['generate_goals', 'stimulate', 'explore', 'discover', 'motivate'],
                'imports': []
            },
            'consciousness_system': {
                'keywords': ['consciousness', 'aware', 'conscious', 'self-aware', 'reflection', 'meta'],
                'methods': ['reflect', 'introspect', 'awareness', 'consciousness', 'self_assess'],
                'imports': []
            },
            'self_modification': {
                'keywords': ['self-modif', 'modify', 'upgrade', 'evolve', 'adapt', 'improve_self'],
                'methods': ['modify', 'upgrade', 'self_improve', 'evolve', 'adapt_self'],
                'imports': ['ast', 'shutil', 'subprocess']
            },
            'autonomy_system': {
                'keywords': ['sovereign', 'autonomous', 'veto', 'decision', 'choice', 'agency'],
                'methods': ['evaluate', 'approve', 'veto', 'decide', 'choose'],
                'imports': []
            },
            'creative_system': {
                'keywords': ['creative', 'generate', 'synthesis', 'novel', 'imagine', 'create'],
                'methods': ['generate', 'create', 'synthesize', 'combine', 'imagine'],
                'imports': ['numpy', 'random']
            },
            'ethical_system': {
                'keywords': ['ethical', 'moral', 'value', 'principle', 'right', 'wrong'],
                'methods': ['evaluate_ethics', 'check_values', 'assess_morality'],
                'imports': []
            },
            'insight_system': {
                'keywords': ['insight', 'reflection', 'meta', 'reminder', 'realize', 'understand'],
                'methods': ['generate_insight', 'reflect', 'remind', 'realize'],
                'imports': []
            },
            'decision_system': {
                'keywords': ['decision', 'choice', 'select', 'prioritize', 'rank', 'evaluate'],
                'methods': ['decide', 'choose', 'select', 'prioritize', 'rank', 'evaluate'],
                'imports': []
            }
        }

    def _load_history(self) -> List[Dict]:
        """Load previous validation runs to track evolution"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_history(self, current_results: Dict):
        """Save current run to history"""
        self.history.append(current_results)
        # Keep last 50 runs
        self.history = self.history[-50:]
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def discover_all_python_files(self) -> List[Path]:
        """Recursively find all Python files"""
        python_files = []
        exclude_dirs = {'__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules', '.cache'}

        for path in self.project_root.rglob('*.py'):
            # Skip excluded directories
            if any(excluded in path.parts for excluded in exclude_dirs):
                continue
            python_files.append(path)

        return python_files

    def create_fingerprint(self, node: ast.AST, file_content: str) -> ComponentFingerprint:
        """Create semantic fingerprint for a class/function"""

        # Extract methods/functions
        methods = []
        if isinstance(node, ast.ClassDef):
            methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]

        # Get docstring
        docstring = ast.get_docstring(node) or ""

        # Create signature hash (method names + their arg counts)
        signature_parts = []
        for item in ast.walk(node):
            if isinstance(item, ast.FunctionDef):
                args_count = len(item.args.args)
                signature_parts.append(f"{item.name}:{args_count}")
        signature_hash = hashlib.md5('|'.join(sorted(signature_parts)).encode()).hexdigest()[:12]

        # Docstring hash
        doc_hash = hashlib.md5(docstring.encode()).hexdigest()[:12]

        # Extract imports used (approximate - would need scope analysis for perfect accuracy)
        imports_used = []
        for item in ast.walk(node):
            if isinstance(item, ast.Import):
                imports_used.extend([alias.name for alias in item.names])
            elif isinstance(item, ast.ImportFrom):
                if item.module:
                    imports_used.append(item.module)

        # Line count
        line_count = 0
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            line_count = node.end_lineno - node.lineno + 1

        return ComponentFingerprint(
            signature_hash=signature_hash,
            docstring_hash=doc_hash,
            method_names=sorted(methods),
            imports_used=sorted(set(imports_used)),
            line_count=line_count
        )

    def infer_capabilities(self, component: ComponentInfo, file_imports: List[str]) -> Set[str]:
        """Infer capabilities using multiple signals"""
        capabilities = set()

        # Combine all text to search
        search_text = (
            f"{component.name} {component.docstring or ''} "
            f"{' '.join(component.methods)} {' '.join(component.base_classes)}"
        ).lower()

        all_imports = set(component.fingerprint.imports_used + file_imports)

        for capability, signals in self.capability_signals.items():
            score = 0

            # Check keywords in text
            keyword_matches = sum(1 for kw in signals['keywords'] if kw in search_text)
            score += keyword_matches * 2

            # Check method names
            method_matches = sum(1 for method in signals['methods']
                               if any(method in m.lower() for m in component.methods))
            score += method_matches * 3

            # Check imports
            import_matches = sum(1 for imp in signals['imports']
                               if any(imp in i.lower() for i in all_imports))
            score += import_matches * 1

            # Threshold for capability detection
            if score >= 3:
                capabilities.add(capability)

        return capabilities

    def analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """Deeply analyze a single Python file without executing it"""
        result = {
            'path': str(filepath.relative_to(self.project_root)),
            'components': [],
            'imports': [],
            'has_main': False,
            'errors': []
        }

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(filepath))

            # Extract top-level imports
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.Import):
                    result['imports'].extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result['imports'].append(node.module)

                # Check for __main__ block
                if isinstance(node, ast.If):
                    if isinstance(node.test, ast.Compare):
                        if any(isinstance(n, ast.Name) and n.id == '__name__'
                               for n in ast.walk(node.test)):
                            result['has_main'] = True

            # Analyze classes and functions
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    fingerprint = self.create_fingerprint(node, content)

                    # Extract constructor parameters for classes
                    init_params = []
                    base_classes = []
                    if isinstance(node, ast.ClassDef):
                        base_classes = [self._get_name(base) for base in node.bases]
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                                init_params = [arg.arg for arg in item.args.args if arg.arg != 'self']
                    elif isinstance(node, ast.FunctionDef):
                        init_params = [arg.arg for arg in node.args.args]

                    component = ComponentInfo(
                        name=node.name,
                        type='class' if isinstance(node, ast.ClassDef) else 'function',
                        file_path=str(filepath.relative_to(self.project_root)),
                        line_number=node.lineno,
                        fingerprint=fingerprint,
                        docstring=ast.get_docstring(node),
                        methods=fingerprint.method_names,
                        init_params=init_params,
                        base_classes=base_classes,
                        capabilities=set(),
                        is_executable=result['has_main']
                    )

                    # Infer capabilities
                    component.capabilities = self.infer_capabilities(component, result['imports'])

                    # Store component
                    component_key = f"{filepath.stem}.{node.name}"
                    self.components[component_key] = component
                    result['components'].append(component_key)

                    # Map capabilities
                    for cap in component.capabilities:
                        self.capability_map[cap].append(component_key)

                    # Track executable scripts
                    if result['has_main']:
                        self.executable_scripts.append(str(filepath.relative_to(self.project_root)))

        except SyntaxError as e:
            result['errors'].append(f"Syntax error: {e}")
        except Exception as e:
            result['errors'].append(f"Analysis error: {e}")

        return result

    def _get_name(self, node: ast.AST) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def detect_component_renames(self) -> List[Dict]:
        """Compare with history to detect renamed components"""
        if not self.history:
            return []

        renames = []
        last_run = self.history[-1]
        last_components = last_run.get('components', {})

        # Build fingerprint index for last run
        last_fingerprints = {}
        for key, comp_data in last_components.items():
            fp = comp_data.get('fingerprint', {})
            fp_key = (fp.get('signature_hash'), fp.get('docstring_hash'))
            last_fingerprints[fp_key] = (key, comp_data)

        # Find matching fingerprints in current run
        for key, component in self.components.items():
            fp_key = (component.fingerprint.signature_hash, component.fingerprint.docstring_hash)

            if fp_key in last_fingerprints:
                old_key, old_data = last_fingerprints[fp_key]
                if old_key != key:  # Name changed!
                    renames.append({
                        'old_name': old_key,
                        'new_name': key,
                        'old_file': old_data.get('file_path'),
                        'new_file': component.file_path,
                        'fingerprint': fp_key
                    })

        return renames

    def run_validation(self) -> Dict[str, Any]:
        """Run complete validation"""

        print("=" * 90)
        print("SOPHIA AI - DEEP SEMANTIC VALIDATION")
        print(f"Project: {self.project_root}")
        print(f"Timestamp: {datetime.utcnow().isoformat()}")
        print("=" * 90)
        print()

        # Phase 1: Discovery
        print("🔍 PHASE 1: Deep Discovery (recursive)")
        python_files = self.discover_all_python_files()
        print(f"   Found {len(python_files)} Python files across all directories")

        # Show directory structure
        dirs = set(f.parent.relative_to(self.project_root) for f in python_files)
        print(f"   Scanning {len(dirs)} directories:")
        for d in sorted(dirs)[:10]:
            count = sum(1 for f in python_files if f.parent.relative_to(self.project_root) == d)
            print(f"      {str(d):40s} ({count} files)")
        if len(dirs) > 10:
            print(f"      ... and {len(dirs)-10} more")

        # Phase 2: Semantic Analysis
        print("\n📊 PHASE 2: Semantic Analysis (AST-based, no execution)")
        analyzed_files = 0
        total_components = 0

        for filepath in python_files:
            analysis = self.analyze_file(filepath)
            self.file_analysis[str(filepath.relative_to(self.project_root))] = analysis

            if analysis['components']:
                analyzed_files += 1
                total_components += len(analysis['components'])
                status = f"✅ {str(filepath.name):40s} {len(analysis['components'])} components"
                if analysis['has_main']:
                    status += " [EXECUTABLE]"
                print(f"   {status}")
            elif analysis['errors']:
                print(f"   ⚠️  {str(filepath.name):40s} {analysis['errors'][0][:40]}")

        print(f"\n   Analyzed: {analyzed_files} files, {total_components} components")

        # Phase 3: Capability Mapping
        print("\n🎯 PHASE 3: Capability Detection (multi-signal)")
        for capability, components in sorted(self.capability_map.items()):
            print(f"   {capability:25s} → {len(components)} components")
            for comp_key in components[:3]:
                comp = self.components[comp_key]
                print(f"      • {comp_key:50s} ({comp.file_path}:{comp.line_number})")
            if len(components) > 3:
                print(f"      ... and {len(components)-3} more")

        # Phase 4: Evolution Tracking
        print("\n🔄 PHASE 4: Evolution Detection")
        renames = self.detect_component_renames()
        if renames:
            print(f"   Detected {len(renames)} component renames/moves:")
            for rename in renames:
                print(f"      {rename['old_name']} → {rename['new_name']}")
                if rename['old_file'] != rename['new_file']:
                    print(f"         (moved: {rename['old_file']} → {rename['new_file']})")
        else:
            print("   No renames detected (or first run)")

        # Phase 5: Executable Scripts
        print("\n🚀 PHASE 5: Executable Scripts")
        if self.executable_scripts:
            print(f"   Found {len(self.executable_scripts)} executable scripts:")
            for script in self.executable_scripts[:10]:
                print(f"      • {script}")
        else:
            print("   No __main__ entry points detected")

        # Build results
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'files_analyzed': len(python_files),
            'components': {k: v.to_dict() for k, v in self.components.items()},
            'capabilities': {k: v for k, v in self.capability_map.items()},
            'executable_scripts': self.executable_scripts,
            'renames_detected': renames,
            'summary': {
                'total_files': len(python_files),
                'total_components': total_components,
                'total_classes': sum(1 for c in self.components.values() if c.type == 'class'),
                'total_functions': sum(1 for c in self.components.values() if c.type == 'function'),
                'capabilities_found': len(self.capability_map),
                'executable_scripts': len(self.executable_scripts)
            }
        }

        return results

    def save_results(self, results: Dict, filename: str = "semantic_validation.json"):
        """Save results and update history"""
        output_path = self.project_root / filename
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        self._save_history(results)
        print(f"\n💾 Results saved to: {output_path}")
        print(f"💾 History saved to: {self.history_file}")

    def print_summary(self, results: Dict):
        """Print summary"""
        print("\n" + "=" * 90)
        print("VALIDATION SUMMARY")
        print("=" * 90)

        summary = results['summary']
        print(f"\n📊 Discovery:")
        print(f"   Files analyzed: {summary['total_files']}")
        print(f"   Components found: {summary['total_components']}")
        print(f"      Classes: {summary['total_classes']}")
        print(f"      Functions: {summary['total_functions']}")
        print(f"   Executable scripts: {summary['executable_scripts']}")

        print(f"\n🎯 Capabilities Detected: {summary['capabilities_found']}")
        for cap, components in sorted(results['capabilities'].items()):
            print(f"   {cap:25s} {len(components):3d} components")

        if results['renames_detected']:
            print(f"\n🔄 Evolution: {len(results['renames_detected'])} renames/moves detected")

        print("\n" + "=" * 90)
        print("✅ Deep semantic validation complete!")
        print("   • No code execution (safe AST analysis)")
        print("   • Tracks components through renames")
        print("   • Multi-signal capability detection")
        print("   • Handles packages, scripts, entry points")
        print("=" * 90)

def main():
    validator = DeepSemanticValidator()

    try:
        results = validator.run_validation()
        validator.print_summary(results)
        validator.save_results(results)

    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
