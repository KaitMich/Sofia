#!/usr/bin/env python3
"""
Comprehensive Dependency Analysis for AI System
Analyzes imports, dependencies, and neural pathways of the AI system.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
import ast
import traceback

class DependencyAnalyzer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.files = {}
        self.imports = defaultdict(list)
        self.dependency_graph = defaultdict(set)
        self.failed_imports = []
        self.missing_modules = set()
        self.interface_mismatches = []
        
    def scan_files(self):
        """Scan all Python files and extract import information"""
        print("🔍 Scanning Python files...")
        
        for py_file in self.project_dir.glob("**/*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            relative_path = py_file.relative_to(self.project_dir)
            print(f"  📄 Analyzing {relative_path}")
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                self.files[str(relative_path)] = {
                    'path': str(py_file),
                    'content': content,
                    'size': len(content),
                    'lines': len(content.splitlines())
                }
                
                # Extract imports using both regex and AST
                self._extract_imports(str(relative_path), content)
                
            except Exception as e:
                print(f"    ❌ Error reading {relative_path}: {e}")
                self.failed_imports.append({
                    'file': str(relative_path),
                    'error': str(e),
                    'type': 'file_read_error'
                })
    
    def _extract_imports(self, file_path, content):
        """Extract imports using multiple methods"""
        imports = []
        
        # Method 1: Regex patterns
        import_patterns = [
            r'^import\s+([^\s#]+)',
            r'^from\s+([^\s#]+)\s+import\s+([^#]+)',
        ]
        
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    if 'from' in pattern:
                        module = match.group(1)
                        items = match.group(2)
                        imports.append({
                            'type': 'from_import',
                            'module': module,
                            'items': [item.strip() for item in items.split(',')],
                            'line': line_num,
                            'raw': line
                        })
                    else:
                        module = match.group(1)
                        imports.append({
                            'type': 'import',
                            'module': module,
                            'line': line_num,
                            'raw': line
                        })
                    break
        
        # Method 2: AST parsing (more reliable)
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            'type': 'import',
                            'module': alias.name,
                            'alias': alias.asname,
                            'line': node.lineno,
                            'method': 'ast'
                        })
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    items = [alias.name for alias in node.names]
                    imports.append({
                        'type': 'from_import',
                        'module': module,
                        'items': items,
                        'line': node.lineno,
                        'method': 'ast'
                    })
        except SyntaxError as e:
            print(f"    ⚠️ Syntax error in {file_path}: {e}")
            self.failed_imports.append({
                'file': file_path,
                'error': str(e),
                'type': 'syntax_error'
            })
        
        self.imports[file_path] = imports
        
    def analyze_dependencies(self):
        """Analyze dependency relationships"""
        print("\n🔗 Analyzing dependency relationships...")
        
        # Build dependency graph
        for file_path, imports in self.imports.items():
            for import_info in imports:
                module = import_info['module']
                
                # Check if it's a local module
                local_module = self._resolve_local_module(module)
                if local_module:
                    self.dependency_graph[file_path].add(local_module)
                    print(f"  📎 {file_path} → {local_module}")
                else:
                    # External module
                    if not self._is_standard_library(module):
                        self.missing_modules.add(module)
    
    def _resolve_local_module(self, module_name):
        """Try to resolve a module name to a local file"""
        possible_files = [
            f"{module_name}.py",
            f"{module_name}/__init__.py"
        ]
        
        for possible in possible_files:
            if possible in self.files:
                return possible
                
        # Handle imports like 'path.to.module'
        parts = module_name.split('.')
        if len(parts) > 1:
            possible = f"{parts[0]}.py"
            if possible in self.files:
                return possible
                
        return None
    
    def _is_standard_library(self, module_name):
        """Check if module is part of standard library"""
        stdlib_modules = {
            'sys', 'os', 'json', 'pathlib', 'datetime', 'time', 'hashlib',
            'collections', 're', 'threading', 'typing', 'traceback', 'ast',
            'csv', 'argparse', 'unicodedata', 'tempfile', 'shutil'
        }
        
        return module_name.split('.')[0] in stdlib_modules
    
    def find_interface_mismatches(self):
        """Find potential interface mismatches"""
        print("\n🔍 Checking for interface mismatches...")
        
        for file_path, imports in self.imports.items():
            for import_info in imports:
                if import_info['type'] == 'from_import':
                    module = import_info['module']
                    items = import_info.get('items', [])
                    
                    local_module = self._resolve_local_module(module)
                    if local_module and local_module in self.files:
                        # Check if imported items exist in target module
                        self._check_imported_items(file_path, local_module, items, import_info)
    
    def _check_imported_items(self, importing_file, target_file, items, import_info):
        """Check if imported items exist in target file"""
        target_content = self.files[target_file]['content']
        
        # Look for function/class definitions
        for item in items:
            if item == '*':
                continue
                
            patterns = [
                rf'^def\s+{item}\s*\(',
                rf'^class\s+{item}\s*[\(:]',
                rf'^{item}\s*=',
                rf'^\s*{item}\s*=',
            ]
            
            found = False
            for pattern in patterns:
                if re.search(pattern, target_content, re.MULTILINE):
                    found = True
                    break
            
            if not found:
                self.interface_mismatches.append({
                    'importing_file': importing_file,
                    'target_file': target_file,
                    'missing_item': item,
                    'line': import_info.get('line', 'unknown'),
                    'import_statement': import_info.get('raw', 'unknown')
                })
                print(f"  ❌ {importing_file} imports '{item}' from {target_file} but it's not found")
    
    def find_circular_dependencies(self):
        """Find circular dependency chains"""
        print("\n🔄 Checking for circular dependencies...")
        
        visited = set()
        recursion_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in recursion_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
                
            if node in visited:
                return
                
            visited.add(node)
            recursion_stack.add(node)
            
            for dependency in self.dependency_graph.get(node, []):
                if dependency in self.files:  # Only consider local files
                    dfs(dependency, path + [node])
            
            recursion_stack.remove(node)
        
        for file_path in self.files:
            if file_path not in visited:
                dfs(file_path, [])
        
        if cycles:
            print(f"  🚨 Found {len(cycles)} circular dependency chains:")
            for i, cycle in enumerate(cycles, 1):
                print(f"    {i}. {' → '.join(cycle)}")
        else:
            print("  ✅ No circular dependencies found")
            
        return cycles
    
    def analyze_critical_files(self):
        """Analyze the critical files mentioned"""
        critical_files = [
            'memory_optimizer.py',
            'memory_analytics.py',
            'memory_evolution_engine.py',
            'unified_memory.py',
            'symbol_memory.py',
            'processing_nodes.py'
        ]
        
        print("\n🎯 Analyzing critical files...")
        
        critical_analysis = {}
        
        for critical in critical_files:
            if critical in self.files:
                print(f"\n📋 {critical}:")
                
                # Analyze imports
                imports = self.imports.get(critical, [])
                local_imports = []
                external_imports = []
                failed_imports = []
                
                for imp in imports:
                    module = imp['module']
                    local_module = self._resolve_local_module(module)
                    
                    if local_module:
                        local_imports.append({
                            'module': module,
                            'resolves_to': local_module,
                            'type': imp['type'],
                            'items': imp.get('items', [])
                        })
                    elif self._is_standard_library(module):
                        external_imports.append(module)
                    else:
                        failed_imports.append(module)
                
                print(f"  📦 Local imports: {len(local_imports)}")
                for imp in local_imports:
                    items_str = f" ({', '.join(imp['items'])})" if imp.get('items') else ""
                    print(f"    • {imp['module']} → {imp['resolves_to']}{items_str}")
                
                print(f"  🌐 External imports: {len(external_imports)}")
                for ext in external_imports:
                    print(f"    • {ext}")
                
                if failed_imports:
                    print(f"  ❌ Failed imports: {len(failed_imports)}")
                    for fail in failed_imports:
                        print(f"    • {fail}")
                
                # Check who imports this file
                dependents = []
                for file_path, deps in self.dependency_graph.items():
                    if critical in deps:
                        dependents.append(file_path)
                
                print(f"  ⬅️ Files that depend on this: {len(dependents)}")
                for dep in dependents:
                    print(f"    • {dep}")
                
                critical_analysis[critical] = {
                    'local_imports': local_imports,
                    'external_imports': external_imports,
                    'failed_imports': failed_imports,
                    'dependents': dependents,
                    'lines_of_code': self.files[critical]['lines'],
                    'file_size': self.files[critical]['size']
                }
            else:
                print(f"  ❌ {critical} not found!")
                critical_analysis[critical] = {'status': 'missing'}
        
        return critical_analysis
    
    def generate_dependency_map(self):
        """Generate a comprehensive dependency map"""
        print("\n📊 Generating dependency map...")
        
        # Find root nodes (files with no dependencies)
        root_nodes = []
        for file_path in self.files:
            if not self.dependency_graph.get(file_path):
                root_nodes.append(file_path)
        
        # Find leaf nodes (files nothing depends on)
        all_dependencies = set()
        for deps in self.dependency_graph.values():
            all_dependencies.update(deps)
        
        leaf_nodes = []
        for file_path in self.files:
            if file_path not in all_dependencies:
                leaf_nodes.append(file_path)
        
        # Calculate dependency depths
        dependency_depths = {}
        
        def calculate_depth(file_path, visited=None):
            if visited is None:
                visited = set()
                
            if file_path in visited:
                return float('inf')  # Circular dependency
                
            if file_path in dependency_depths:
                return dependency_depths[file_path]
            
            visited.add(file_path)
            
            deps = self.dependency_graph.get(file_path, set())
            if not deps:
                depth = 0
            else:
                depth = 1 + max(calculate_depth(dep, visited.copy()) for dep in deps)
            
            dependency_depths[file_path] = depth
            return depth
        
        for file_path in self.files:
            calculate_depth(file_path)
        
        # Create map
        dependency_map = {
            'total_files': len(self.files),
            'total_dependencies': sum(len(deps) for deps in self.dependency_graph.values()),
            'root_nodes': root_nodes,
            'leaf_nodes': leaf_nodes,
            'dependency_depths': dependency_depths,
            'circular_dependencies': self.find_circular_dependencies(),
            'missing_modules': list(self.missing_modules),
            'interface_mismatches': self.interface_mismatches,
            'failed_imports': self.failed_imports,
            'dependency_graph': {k: list(v) for k, v in self.dependency_graph.items()},
            'import_summary': self._generate_import_summary()
        }
        
        return dependency_map
    
    def _generate_import_summary(self):
        """Generate import summary statistics"""
        summary = {
            'total_import_statements': 0,
            'unique_modules_imported': set(),
            'most_imported_modules': Counter(),
            'files_by_import_count': [],
            'import_types': Counter()
        }
        
        for file_path, imports in self.imports.items():
            import_count = len(imports)
            summary['files_by_import_count'].append((file_path, import_count))
            summary['total_import_statements'] += import_count
            
            for imp in imports:
                module = imp['module']
                summary['unique_modules_imported'].add(module)
                summary['most_imported_modules'][module] += 1
                summary['import_types'][imp['type']] += 1
        
        # Convert sets to lists for JSON serialization
        summary['unique_modules_imported'] = list(summary['unique_modules_imported'])
        summary['files_by_import_count'].sort(key=lambda x: x[1], reverse=True)
        
        return summary
    
    def save_report(self, output_file):
        """Save comprehensive report to file"""
        print(f"\n💾 Saving comprehensive dependency report to {output_file}...")
        
        report = {
            'analysis_timestamp': str(Path.cwd()),
            'project_directory': str(self.project_dir),
            'critical_files_analysis': self.analyze_critical_files(),
            'dependency_map': self.generate_dependency_map(),
            'files_analyzed': {k: {'lines': v['lines'], 'size': v['size']} for k, v in self.files.items()},
            'neural_pathways': self._generate_neural_pathways()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✅ Report saved to {output_file}")
        return report
    
    def _generate_neural_pathways(self):
        """Generate neural pathway analysis (import chains)"""
        pathways = {}
        
        def trace_pathway(start_file, visited=None):
            if visited is None:
                visited = []
                
            if start_file in visited:
                return [visited + [start_file]]  # Circular path
            
            visited = visited + [start_file]
            
            if start_file not in self.dependency_graph or not self.dependency_graph[start_file]:
                return [visited]  # End of pathway
            
            pathways_from_here = []
            for dependency in self.dependency_graph[start_file]:
                pathways_from_here.extend(trace_pathway(dependency, visited))
            
            return pathways_from_here
        
        for file_path in self.files:
            pathways[file_path] = trace_pathway(file_path)
        
        return pathways
    
    def print_summary(self):
        """Print a summary of findings"""
        print("\n" + "="*60)
        print("🧠 AI SYSTEM DEPENDENCY ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Total Python files: {len(self.files)}")
        print(f"  Total import statements: {sum(len(imports) for imports in self.imports.values())}")
        print(f"  Unique modules imported: {len(set(imp['module'] for imports in self.imports.values() for imp in imports))}")
        print(f"  Local dependencies: {sum(len(deps) for deps in self.dependency_graph.values())}")
        
        print(f"\n🚨 Issues Found:")
        print(f"  Missing/broken imports: {len(self.missing_modules)}")
        print(f"  Interface mismatches: {len(self.interface_mismatches)}")
        print(f"  Failed file reads: {len([f for f in self.failed_imports if f['type'] == 'file_read_error'])}")
        print(f"  Syntax errors: {len([f for f in self.failed_imports if f['type'] == 'syntax_error'])}")
        
        if self.missing_modules:
            print(f"\n❌ Missing Modules:")
            for module in sorted(self.missing_modules):
                print(f"    • {module}")
        
        if self.interface_mismatches:
            print(f"\n🔧 Interface Mismatches:")
            for mismatch in self.interface_mismatches[:10]:  # Show first 10
                print(f"    • {mismatch['importing_file']} → {mismatch['target_file']}: missing '{mismatch['missing_item']}'")
        
        # Find most central files (most depended upon)
        dependency_counts = Counter()
        for deps in self.dependency_graph.values():
            for dep in deps:
                dependency_counts[dep] += 1
        
        print(f"\n🎯 Most Critical Files (by dependents):")
        for file_path, count in dependency_counts.most_common(10):
            print(f"    • {file_path}: {count} files depend on it")

def main():
    project_dir = Path.cwd()
    print(f"🔍 Analyzing AI system dependencies in: {project_dir}")
    
    analyzer = DependencyAnalyzer(project_dir)
    analyzer.scan_files()
    analyzer.analyze_dependencies()
    analyzer.find_interface_mismatches()
    
    # Generate and save report
    report = analyzer.save_report("ai_dependency_analysis.json")
    
    # Print summary
    analyzer.print_summary()
    
    print(f"\n✅ Analysis complete! Full report saved to ai_dependency_analysis.json")

if __name__ == "__main__":
    main()