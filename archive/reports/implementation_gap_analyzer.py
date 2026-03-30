#!/usr/bin/env python3
"""
Implementation Gap Analyzer
Finds features that are documented/defined but not actually implemented
Similar to the fear_patterns case - exists in data but never used in logic
"""

import ast
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any

class ImplementationGapAnalyzer:
    """Finds the gap between aspiration (documentation) and reality (implementation)"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.findings = {
            "unused_constants": [],
            "unused_class_attributes": [],
            "uncalled_methods": [],
            "empty_data_files": [],
            "documented_but_missing": [],
            "loaded_never_written": [],
            "defined_never_accessed": [],
            "integration_claims_unverified": []
        }

        # Track all definitions and usages
        self.defined_attributes = defaultdict(list)  # {attr_name: [file locations]}
        self.attribute_usage = defaultdict(list)     # {attr_name: [usage locations]}
        self.method_definitions = defaultdict(list)   # {method_name: [file locations]}
        self.method_calls = defaultdict(list)         # {method_name: [call locations]}

    def analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """Analyze a single Python file for implementation gaps"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=str(filepath))
        except Exception as e:
            return {"error": str(e)}

        file_findings = {
            "unused_in_file": [],
            "suspicious_patterns": []
        }

        # Find class definitions with their attributes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node, filepath, content)

        return file_findings

    def _analyze_class(self, class_node: ast.ClassDef, filepath: Path, content: str):
        """Analyze a class for unused attributes and methods"""
        class_name = class_node.name

        # Find attributes defined in __init__ or class body
        defined_attrs = set()
        methods_defined = set()

        # Scan class body
        for item in class_node.body:
            # Track method definitions
            if isinstance(item, ast.FunctionDef):
                method_name = item.name
                methods_defined.add(method_name)

                # Track as definition
                self.method_definitions[f"{class_name}.{method_name}"].append({
                    "file": str(filepath.name),
                    "line": item.lineno,
                    "class": class_name
                })

                # Look for self.attribute assignments in methods
                for node in ast.walk(item):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Attribute):
                                if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                    attr_name = target.attr
                                    defined_attrs.add(attr_name)
                                    self.defined_attributes[f"{class_name}.{attr_name}"].append({
                                        "file": str(filepath.name),
                                        "line": node.lineno,
                                        "class": class_name
                                    })

            # Track class-level attribute assignments
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attr_name = target.value if hasattr(target, 'value') else str(target.id)
                        # This is a class constant
                        self.defined_attributes[f"{class_name}.{attr_name}"].append({
                            "file": str(filepath.name),
                            "line": item.lineno,
                            "class": class_name,
                            "type": "class_constant"
                        })

        # Now scan for usages within the class
        used_attrs = set()
        called_methods = set()

        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                for node in ast.walk(item):
                    # Track attribute access (self.something)
                    if isinstance(node, ast.Attribute):
                        if isinstance(node.value, ast.Name) and node.value.id == 'self':
                            attr_name = node.attr
                            used_attrs.add(attr_name)
                            self.attribute_usage[f"{class_name}.{attr_name}"].append({
                                "file": str(filepath.name),
                                "line": node.lineno,
                                "context": "attribute_access"
                            })

                    # Track method calls (self.method())
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'self':
                                method_name = node.func.attr
                                called_methods.add(method_name)
                                self.method_calls[f"{class_name}.{method_name}"].append({
                                    "file": str(filepath.name),
                                    "line": node.lineno
                                })

        # Find unused attributes (defined but never accessed)
        unused_attrs = defined_attrs - used_attrs
        if unused_attrs:
            for attr in unused_attrs:
                # Skip private methods and special cases
                if not attr.startswith('_') and attr not in ['data_dir', 'lock']:
                    self.findings["unused_class_attributes"].append({
                        "class": class_name,
                        "attribute": attr,
                        "file": str(filepath.name),
                        "type": "defined_never_used"
                    })

        # Find uncalled methods (defined but never called)
        uncalled = methods_defined - called_methods
        if uncalled:
            for method in uncalled:
                # Skip special methods, private methods, and common public API methods
                if not method.startswith('_') and method not in [
                    'run', 'start', 'stop', 'execute', 'main', 'process',
                    'get', 'set', 'load', 'save', 'update', 'delete'
                ]:
                    self.findings["uncalled_methods"].append({
                        "class": class_name,
                        "method": method,
                        "file": str(filepath.name),
                        "note": "Method defined but never called within class"
                    })

    def find_empty_data_files(self):
        """Find data files that are created but remain empty or near-empty"""
        data_dir = self.project_root / "data"
        if not data_dir.exists():
            return

        for json_file in data_dir.glob("*.json"):
            try:
                size = json_file.stat().st_size

                # Check if file is very small (< 50 bytes) or empty
                if size < 50:
                    self.findings["empty_data_files"].append({
                        "file": str(json_file.name),
                        "size": size,
                        "status": "empty_or_minimal"
                    })
                    continue

                # Check if file has only default/empty structure
                with open(json_file, 'r') as f:
                    data = json.load(f)

                    # Empty list/dict or only 1 test entry
                    if isinstance(data, list) and len(data) == 0:
                        self.findings["empty_data_files"].append({
                            "file": str(json_file.name),
                            "size": size,
                            "status": "empty_list"
                        })
                    elif isinstance(data, dict) and len(data) <= 1:
                        self.findings["empty_data_files"].append({
                            "file": str(json_file.name),
                            "size": size,
                            "status": "minimal_data",
                            "entries": len(data)
                        })
            except Exception as e:
                pass

    def find_loaded_never_written(self):
        """Find data structures that are loaded but never written to"""

        for filepath in self.project_root.glob("*.py"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Pattern: self.something = self._load_something()
                load_pattern = r'self\.(\w+)\s*=\s*self\._load_(\w+)\('
                loads = re.findall(load_pattern, content)

                for attr_name, load_method in loads:
                    # Check if there's a corresponding save
                    save_pattern = rf'self\._save_{load_method}\('
                    if not re.search(save_pattern, content):
                        # Check if the attribute is ever assigned to after load
                        assign_pattern = rf'self\.{attr_name}\s*[=\.]'
                        assignments = len(re.findall(assign_pattern, content))

                        # If only 1 assignment (the load itself), it's never written
                        if assignments <= 1:
                            self.findings["loaded_never_written"].append({
                                "file": str(filepath.name),
                                "attribute": attr_name,
                                "load_method": f"_load_{load_method}",
                                "issue": "Loaded but never modified or saved"
                            })
            except Exception:
                pass

    def find_integration_claims(self):
        """Find claimed integrations that might not be real"""

        for filepath in self.project_root.glob("*.py"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for imports that claim integration
                # Pattern: from X import Y  where X suggests integration
                integration_keywords = [
                    'consciousness', 'curiosity', 'identity', 'sovereignty',
                    'insight', 'creativity', 'ethical', 'choice'
                ]

                for keyword in integration_keywords:
                    # Find imports
                    import_pattern = rf'from (\w*{keyword}\w*) import (\w+)'
                    imports = re.findall(import_pattern, content, re.IGNORECASE)

                    for module, imported in imports:
                        # Check if the imported item is actually used
                        usage_count = len(re.findall(rf'\b{imported}\b', content))

                        # If used only once (the import itself), it's unused
                        if usage_count <= 1:
                            self.findings["integration_claims_unverified"].append({
                                "file": str(filepath.name),
                                "claimed_integration": module,
                                "imported_but_unused": imported,
                                "issue": "Imported to claim integration but never used"
                            })
            except Exception:
                pass

    def analyze_docstring_claims(self, filepath: Path):
        """Find capabilities mentioned in docstrings but not in code"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=str(filepath))
        except Exception:
            return

        # Capability keywords to look for in docstrings
        capability_keywords = {
            'fear': ['fear', 'threat', 'anxiety', 'avoidance'],
            'emotion': ['emotion', 'feeling', 'mood', 'affect'],
            'narrative': ['narrative', 'story', 'autobiography'],
            'consciousness': ['conscious', 'aware', 'meta-cognitive'],
            'learning': ['learn', 'train', 'adapt', 'improve'],
            'autonomy': ['autonomous', 'independent', 'self-directed'],
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if not docstring:
                    continue

                docstring_lower = docstring.lower()

                # Check each capability
                for capability, keywords in capability_keywords.items():
                    for keyword in keywords:
                        if keyword in docstring_lower:
                            # Now check if the keyword appears in actual code
                            # Get the source of just this node
                            try:
                                node_source = ast.get_source_segment(content, node)
                                if node_source:
                                    # Remove docstring and comments
                                    code_only = re.sub(r'""".*?"""', '', node_source, flags=re.DOTALL)
                                    code_only = re.sub(r"'''.*?'''", '', code_only, flags=re.DOTALL)
                                    code_only = re.sub(r'#.*$', '', code_only, flags=re.MULTILINE)

                                    # Check if keyword appears in actual logic
                                    if keyword not in code_only.lower():
                                        self.findings["documented_but_missing"].append({
                                            "file": str(filepath.name),
                                            "function_or_class": node.name,
                                            "claimed_capability": capability,
                                            "keyword_in_doc": keyword,
                                            "issue": "Mentioned in docstring but not in code"
                                        })
                            except Exception:
                                pass

    def run_full_analysis(self) -> Dict[str, Any]:
        """Run complete analysis"""

        print("=" * 80)
        print("IMPLEMENTATION GAP ANALYZER")
        print("Finding features that are documented but not implemented")
        print("=" * 80)
        print()

        # Phase 1: Analyze all Python files
        print("📊 Phase 1: Analyzing code structure...")
        python_files = list(self.project_root.glob("*.py"))

        for filepath in python_files:
            self.analyze_file(filepath)
            self.analyze_docstring_claims(filepath)

        print(f"   Analyzed {len(python_files)} files")

        # Phase 2: Find empty/minimal data files
        print("\n📂 Phase 2: Checking data files...")
        self.find_empty_data_files()
        print(f"   Found {len(self.findings['empty_data_files'])} minimal data files")

        # Phase 3: Find loaded-never-written patterns
        print("\n🔄 Phase 3: Finding loaded-but-never-modified structures...")
        self.find_loaded_never_written()
        print(f"   Found {len(self.findings['loaded_never_written'])} cases")

        # Phase 4: Find fake integrations
        print("\n🔗 Phase 4: Verifying integration claims...")
        self.find_integration_claims()
        print(f"   Found {len(self.findings['integration_claims_unverified'])} suspicious imports")

        # Phase 5: Cross-reference to find truly unused
        print("\n🎯 Phase 5: Cross-referencing usage patterns...")
        self._cross_reference_usage()

        return self.findings

    def _cross_reference_usage(self):
        """Cross-reference definitions with usage to find true gaps"""

        # Check each defined attribute
        for attr_key, definitions in self.defined_attributes.items():
            if attr_key not in self.attribute_usage:
                # Never used anywhere
                for defn in definitions:
                    if defn.get('type') == 'class_constant':
                        self.findings["defined_never_accessed"].append({
                            "attribute": attr_key,
                            "file": defn['file'],
                            "line": defn['line'],
                            "type": "constant_never_referenced",
                            "similar_to": "fear_patterns case"
                        })

    def print_report(self):
        """Print comprehensive report"""

        print("\n" + "=" * 80)
        print("IMPLEMENTATION GAP REPORT")
        print("=" * 80)

        # 1. Unused constants (like fear_patterns)
        if self.findings["defined_never_accessed"]:
            print(f"\n❌ DEFINED BUT NEVER ACCESSED ({len(self.findings['defined_never_accessed'])})")
            print("   (Similar to 'fear_patterns' - exists but never used in logic)")
            print("   " + "-" * 76)
            for item in self.findings["defined_never_accessed"][:10]:
                print(f"   • {item['attribute']:50s} ({item['file']}:{item['line']})")
            if len(self.findings["defined_never_accessed"]) > 10:
                print(f"   ... and {len(self.findings['defined_never_accessed']) - 10} more")

        # 2. Uncalled methods
        if self.findings["uncalled_methods"]:
            print(f"\n⚠️  UNCALLED METHODS ({len(self.findings['uncalled_methods'])})")
            print("   (Defined but never invoked - may be aspirational)")
            print("   " + "-" * 76)
            for item in self.findings["uncalled_methods"][:10]:
                print(f"   • {item['class']}.{item['method']:50s} ({item['file']})")
            if len(self.findings["uncalled_methods"]) > 10:
                print(f"   ... and {len(self.findings['uncalled_methods']) - 10} more")

        # 3. Empty data files
        if self.findings["empty_data_files"]:
            print(f"\n📁 EMPTY/MINIMAL DATA FILES ({len(self.findings['empty_data_files'])})")
            print("   (Created but never populated - planned features?)")
            print("   " + "-" * 76)
            for item in self.findings["empty_data_files"][:10]:
                print(f"   • {item['file']:50s} ({item.get('entries', 0)} entries, {item['size']} bytes)")
            if len(self.findings["empty_data_files"]) > 10:
                print(f"   ... and {len(self.findings['empty_data_files']) - 10} more")

        # 4. Loaded never written
        if self.findings["loaded_never_written"]:
            print(f"\n🔄 LOADED BUT NEVER MODIFIED ({len(self.findings['loaded_never_written'])})")
            print("   (Loaded at startup but never changes - static data?)")
            print("   " + "-" * 76)
            for item in self.findings["loaded_never_written"][:10]:
                print(f"   • {item['attribute']:50s} in {item['file']}")
            if len(self.findings["loaded_never_written"]) > 10:
                print(f"   ... and {len(self.findings['loaded_never_written']) - 10} more")

        # 5. Documented but missing
        if self.findings["documented_but_missing"]:
            print(f"\n📝 DOCUMENTED BUT NOT IMPLEMENTED ({len(self.findings['documented_but_missing'])})")
            print("   (Mentioned in docstrings but not in actual code)")
            print("   " + "-" * 76)
            for item in self.findings["documented_but_missing"][:10]:
                print(f"   • {item['function_or_class']}: claims '{item['claimed_capability']}' but missing '{item['keyword_in_doc']}'")
            if len(self.findings["documented_but_missing"]) > 10:
                print(f"   ... and {len(self.findings['documented_but_missing']) - 10} more")

        # 6. Fake integrations
        if self.findings["integration_claims_unverified"]:
            print(f"\n🔗 CLAIMED INTEGRATIONS (UNUSED IMPORTS) ({len(self.findings['integration_claims_unverified'])})")
            print("   (Imports suggest integration but never actually used)")
            print("   " + "-" * 76)
            for item in self.findings["integration_claims_unverified"][:10]:
                print(f"   • {item['file']}: imports {item['imported_but_unused']} from {item['claimed_integration']} but never uses it")
            if len(self.findings["integration_claims_unverified"]) > 10:
                print(f"   ... and {len(self.findings['integration_claims_unverified']) - 10} more")

        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        total_gaps = sum(len(v) for v in self.findings.values() if isinstance(v, list))
        print(f"Total implementation gaps found: {total_gaps}")
        print()

        for category, items in self.findings.items():
            if isinstance(items, list) and items:
                print(f"   {category:40s} {len(items):4d}")

        print("\n" + "=" * 80)

    def save_detailed_report(self, filename: str = "implementation_gaps_report.json"):
        """Save detailed findings to JSON"""
        output_path = self.project_root / filename
        with open(output_path, 'w') as f:
            json.dump(self.findings, f, indent=2)
        print(f"\n💾 Detailed report saved to: {output_path}")


def main():
    analyzer = ImplementationGapAnalyzer()
    analyzer.run_full_analysis()
    analyzer.print_report()
    analyzer.save_detailed_report()

    print("\n✅ Gap analysis complete!")
    print("   This report shows the difference between Sophia's vision and reality.")

if __name__ == "__main__":
    main()
