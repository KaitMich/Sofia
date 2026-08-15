#!/usr/bin/env python3
"""
Script Relationship Auditor
Analyzes all Python scripts to find:
1. Consolidation patterns (unified files vs originals)
2. Duplicate/variant scripts
3. Import relationships
4. Orphaned scripts (not imported anywhere)
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
import re

def extract_imports(file_path):
    """Extract all imports from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))

        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        return imports
    except Exception as e:
        return set()

def extract_header_comment(file_path):
    """Extract docstring or header comment"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to parse and get module docstring
        try:
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            if docstring:
                return docstring.split('\n')[0:5]  # First 5 lines
        except:
            pass

        # Fallback: look for header comments
        lines = content.split('\n')
        header = []
        for line in lines[:20]:
            if line.strip().startswith('#') or '"""' in line or "'''" in line:
                header.append(line.strip())
            elif header and not line.strip():
                break
        return header
    except:
        return []

def find_consolidation_claims(file_path):
    """Check if file claims to consolidate other files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for consolidation patterns
        patterns = [
            r'consolidate[sd]?\s+([a-z_\.py\s,]+)',
            r'replaces?\s+([a-z_\.py\s,]+)',
            r'unified\s+([a-z_\s]+)',
            r'combines?\s+([a-z_\.py\s,]+)'
        ]

        claims = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            claims.extend(matches)

        return claims
    except:
        return []

def analyze_file(file_path):
    """Full analysis of a single file"""
    stat = os.stat(file_path)
    return {
        'name': file_path.name,
        'size': stat.st_size,
        'lines': sum(1 for _ in open(file_path, 'rb')),
        'imports': extract_imports(file_path),
        'header': extract_header_comment(file_path),
        'consolidation_claims': find_consolidation_claims(file_path)
    }

def main():
    project_dir = Path("/path/to/sofia")

    # Find all Python files in root
    py_files = list(project_dir.glob("*.py"))
    py_files = [f for f in py_files if not f.name.startswith('__') and not f.name.startswith('audit_')]

    print(f"📊 Analyzing {len(py_files)} Python files...\n")

    # Analyze all files
    analyses = {}
    for file_path in sorted(py_files):
        analyses[file_path.name] = analyze_file(file_path)

    # Build import graph
    import_graph = defaultdict(set)
    for filename, data in analyses.items():
        for imp in data['imports']:
            # Check if this import matches a file in our project
            if f"{imp}.py" in analyses:
                import_graph[f"{imp}.py"].add(filename)

    # Find groups
    print("=" * 80)
    print("1. CONSOLIDATION CLAIMS (Files that say they consolidate others)")
    print("=" * 80)

    consolidated_files = {}
    for filename, data in analyses.items():
        if data['consolidation_claims'] or 'unified' in filename.lower() or 'consolidate' in str(data['header']).lower():
            print(f"\n📦 {filename} ({data['size']/1024:.1f} KB, {data['lines']} lines)")
            if data['header']:
                print(f"   Header: {' '.join(data['header'][:2])[:120]}...")
            if data['consolidation_claims']:
                print(f"   Claims to consolidate: {data['consolidation_claims']}")
            consolidated_files[filename] = data

    print("\n" + "=" * 80)
    print("2. NAMING PATTERN GROUPS (Potential duplicates/variants)")
    print("=" * 80)

    # Group by base name
    groups = defaultdict(list)
    for filename in analyses.keys():
        # Extract base name (e.g., "memory" from "memory_optimizer.py")
        parts = filename.replace('.py', '').split('_')
        if len(parts) > 1:
            base = parts[0]
            groups[base].append(filename)

    for base, files in sorted(groups.items()):
        if len(files) >= 2:
            print(f"\n🔍 '{base}' group ({len(files)} files):")
            for f in sorted(files):
                data = analyses[f]
                imported_by = len(import_graph.get(f, set()))
                print(f"   - {f:40} {data['size']/1024:>6.1f} KB  {data['lines']:>5} lines  [{imported_by:>2} imports]")

    print("\n" + "=" * 80)
    print("3. ORPHANED SCRIPTS (Not imported by any file)")
    print("=" * 80)

    orphaned = []
    for filename in sorted(analyses.keys()):
        imported_by = import_graph.get(filename, set())
        if not imported_by and filename not in ['main.py', 'cli.py', 'run_system.py', 'talk_to_ai.py']:
            data = analyses[filename]
            orphaned.append((filename, data))

    for filename, data in orphaned:
        print(f"   - {filename:40} {data['size']/1024:>6.1f} KB  {data['lines']:>5} lines")

    print(f"\n   Total orphaned: {len(orphaned)}")

    print("\n" + "=" * 80)
    print("4. MOST IMPORTED FILES (Core dependencies)")
    print("=" * 80)

    most_imported = sorted(import_graph.items(), key=lambda x: len(x[1]), reverse=True)[:15]
    for filename, importers in most_imported:
        print(f"   - {filename:40} imported by {len(importers):>2} files")

    print("\n" + "=" * 80)
    print("5. SYMBOL/SYMBOLIC FILE ANALYSIS")
    print("=" * 80)

    symbol_files = {f: d for f, d in analyses.items() if 'symbol' in f.lower()}
    print(f"\n   Found {len(symbol_files)} symbol-related files:")
    for filename, data in sorted(symbol_files.items()):
        imported_by = len(import_graph.get(filename, set()))
        print(f"   - {filename:40} {data['size']/1024:>6.1f} KB  [{imported_by:>2} imports]")

    print("\n" + "=" * 80)
    print("6. MEMORY FILE ANALYSIS")
    print("=" * 80)

    memory_files = {f: d for f, d in analyses.items() if 'memory' in f.lower()}
    print(f"\n   Found {len(memory_files)} memory-related files:")
    for filename, data in sorted(memory_files.items()):
        imported_by = len(import_graph.get(filename, set()))
        print(f"   - {filename:40} {data['size']/1024:>6.1f} KB  [{imported_by:>2} imports]")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"   Total files analyzed: {len(analyses)}")
    print(f"   Files with consolidation claims: {len(consolidated_files)}")
    print(f"   Orphaned scripts: {len(orphaned)}")
    print(f"   Symbol-related files: {len(symbol_files)}")
    print(f"   Memory-related files: {len(memory_files)}")
    print()

if __name__ == "__main__":
    main()
