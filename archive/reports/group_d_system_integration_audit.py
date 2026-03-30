#!/usr/bin/env python3
"""
SYSTEM INTEGRATION AUDIT - GROUP D VALIDATION

Comprehensive verification of all claimed integrations for GROUP D: SYMBOL & CONCEPT PROCESSING

This audit will:
1. Import Analysis: Check actual imports vs claimed connections
2. Function Call Verification: Search for actual function calls between files
3. Data Flow Validation: Verify data flows between systems
4. API Compatibility: Check interface compatibility
5. Runtime Testing: Test actual execution of claimed connections
6. Error Analysis: Look for import errors contradicting claims
"""

import ast
import importlib
import inspect
import json
import os
import re
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple

class GroupDIntegrationAuditor:
    """Comprehensive auditor for GROUP D symbol processing integration claims."""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.audit_results = {
            "timestamp": "2025-06-25T00:00:00Z",
            "audit_type": "GROUP_D_SYSTEM_INTEGRATION_VALIDATION",
            "files_analyzed": [],
            "import_analysis": {},
            "function_verification": {},
            "data_flow_validation": {},
            "api_compatibility": {},
            "runtime_testing": {},
            "error_analysis": {},
            "claimed_vs_actual": {},
            "discrepancies": [],
            "overall_assessment": "unknown"
        }
        
        # Define the claimed GROUP D integrations
        self.claimed_integrations = {
            "symbol_chainer.py": {
                "status": "consolidated_into_creative_engine",
                "target": "creative_engine.py",
                "method": "build_concept_chains()",
                "claimed_connections": ["unified_memory", "vector_data", "cosine_similarity"]
            },
            "symbol_suggester.py": {
                "status": "consolidated_into_creative_engine", 
                "target": "creative_engine.py",
                "method": "suggest_symbols_from_clusters()",
                "claimed_connections": ["unified_memory", "DBSCAN", "sklearn"]
            },
            "symbol_cluster.py": {
                "status": "consolidated_into_memory_analytics",
                "target": "memory_analytics.py", 
                "method": "analyze_symbol_clusters()",
                "claimed_connections": ["sklearn", "matplotlib", "unified_memory"]
            },
            "symbolic_nourishment.py": {
                "status": "standalone_gold_standard",
                "target": "standalone",
                "claimed_connections": ["unified_memory", "memory_bridge", "emotion_handler", "processing_nodes"]
            },
            "expanded_symbolic_core.py": {
                "status": "standalone_foundational",
                "target": "standalone", 
                "claimed_connections": ["json", "datetime", "typing"]
            }
        }
        
        self.group_d_files = list(self.claimed_integrations.keys())
        self.target_files = ["creative_engine.py", "memory_analytics.py"]
    
    def run_comprehensive_audit(self) -> Dict[str, Any]:
        """Run the complete integration audit."""
        print("🔍 STARTING COMPREHENSIVE GROUP D INTEGRATION AUDIT")
        print("=" * 70)
        
        # 1. Import Analysis
        print("\n1️⃣ IMPORT ANALYSIS")
        self._analyze_imports()
        
        # 2. Function Call Verification  
        print("\n2️⃣ FUNCTION CALL VERIFICATION")
        self._verify_function_calls()
        
        # 3. Data Flow Validation
        print("\n3️⃣ DATA FLOW VALIDATION")
        self._validate_data_flow()
        
        # 4. API Compatibility
        print("\n4️⃣ API COMPATIBILITY CHECK")
        self._check_api_compatibility()
        
        # 5. Runtime Testing
        print("\n5️⃣ RUNTIME TESTING")
        self._test_runtime_connections()
        
        # 6. Error Analysis
        print("\n6️⃣ ERROR ANALYSIS")
        self._analyze_errors()
        
        # 7. Generate final assessment
        print("\n7️⃣ FINAL ASSESSMENT")
        self._generate_assessment()
        
        return self.audit_results
    
    def _analyze_imports(self):
        """Analyze actual import statements vs claimed connections."""
        print("   Analyzing import statements in all GROUP D files...")
        
        for file_name in self.group_d_files + self.target_files:
            file_path = self.project_dir / file_name
            
            if not file_path.exists():
                self.audit_results["import_analysis"][file_name] = {
                    "status": "file_not_found",
                    "error": f"File {file_name} does not exist"
                }
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse AST to get imports
                tree = ast.parse(content)
                imports = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ""
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}" if module else alias.name)
                
                # Also check for dynamic imports and string-based imports
                string_imports = re.findall(r'from\s+(\w+(?:\.\w+)*)\s+import\s+([^#\n]+)', content)
                direct_imports = re.findall(r'import\s+(\w+(?:\.\w+)*)', content)
                
                self.audit_results["import_analysis"][file_name] = {
                    "status": "analyzed",
                    "ast_imports": imports,
                    "string_imports": string_imports,
                    "direct_imports": direct_imports,
                    "total_imports": len(imports) + len(string_imports) + len(direct_imports)
                }
                
                print(f"      ✅ {file_name}: {len(imports)} AST imports found")
                
            except Exception as e:
                self.audit_results["import_analysis"][file_name] = {
                    "status": "parse_error",
                    "error": str(e)
                }
                print(f"      ❌ {file_name}: Parse error - {e}")
    
    def _verify_function_calls(self):
        """Verify actual function calls match claimed integrations."""
        print("   Verifying function calls and method existence...")
        
        # Check if consolidated methods actually exist in target files
        consolidation_checks = {
            "creative_engine.py": ["build_concept_chains", "suggest_symbols_from_clusters"],
            "memory_analytics.py": ["analyze_symbol_clusters"]
        }
        
        for target_file, expected_methods in consolidation_checks.items():
            file_path = self.project_dir / target_file
            
            if not file_path.exists():
                self.audit_results["function_verification"][target_file] = {
                    "status": "file_not_found"
                }
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                found_methods = []
                missing_methods = []
                
                for method in expected_methods:
                    if f"def {method}" in content:
                        found_methods.append(method)
                        print(f"      ✅ {target_file}: Found method {method}")
                    else:
                        missing_methods.append(method)
                        print(f"      ❌ {target_file}: Missing method {method}")
                
                # Check for function signatures and parameters
                method_signatures = {}
                for method in found_methods:
                    pattern = rf"def {method}\([^)]*\):"
                    match = re.search(pattern, content)
                    if match:
                        method_signatures[method] = match.group(0)
                
                self.audit_results["function_verification"][target_file] = {
                    "status": "verified",
                    "found_methods": found_methods,
                    "missing_methods": missing_methods,
                    "method_signatures": method_signatures,
                    "consolidation_success_rate": len(found_methods) / len(expected_methods) * 100
                }
                
            except Exception as e:
                self.audit_results["function_verification"][target_file] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"      ❌ {target_file}: Verification error - {e}")
    
    def _validate_data_flow(self):
        """Validate data flows between systems as claimed."""
        print("   Validating data flow patterns...")
        
        # Check for unified_memory usage patterns
        unified_memory_usage = {}
        
        for file_name in self.group_d_files + self.target_files:
            file_path = self.project_dir / file_name
            
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for unified memory usage patterns
                patterns = {
                    "unified_memory_import": "unified_memory" in content,
                    "get_unified_memory_call": "get_unified_memory()" in content,
                    "vector_data_access": "vector_data" in content,
                    "store_decision_call": "store_decision" in content,
                    "memory_counts_call": "get_memory_counts" in content,
                    "sklearn_usage": "sklearn" in content,
                    "numpy_usage": "numpy" in content or "np." in content
                }
                
                unified_memory_usage[file_name] = patterns
                active_patterns = sum(1 for v in patterns.values() if v)
                print(f"      📊 {file_name}: {active_patterns}/{len(patterns)} data flow patterns found")
                
            except Exception as e:
                print(f"      ❌ {file_name}: Data flow validation error - {e}")
        
        self.audit_results["data_flow_validation"] = unified_memory_usage
    
    def _check_api_compatibility(self):
        """Check API compatibility between connected systems."""
        print("   Checking API compatibility...")
        
        compatibility_results = {}
        
        # Test key API interfaces
        try:
            # Check if we can import and inspect key modules
            sys.path.insert(0, str(self.project_dir))
            
            # Test unified_memory API
            try:
                import unified_memory
                unified_mem = unified_memory.get_unified_memory()
                
                api_methods = [method for method in dir(unified_mem) if not method.startswith('_')]
                compatibility_results["unified_memory"] = {
                    "status": "available",
                    "api_methods": api_methods,
                    "has_store_method": hasattr(unified_mem, 'store_decision'),
                    "has_counts_method": hasattr(unified_mem, 'get_memory_counts'),
                    "has_vector_data": hasattr(unified_mem, 'vector_data')
                }
                print(f"      ✅ unified_memory: {len(api_methods)} API methods available")
                
            except Exception as e:
                compatibility_results["unified_memory"] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"      ❌ unified_memory: Import/API error - {e}")
            
            # Test creative_engine API
            try:
                import creative_engine
                engine = creative_engine.CreativeEngine()
                
                expected_methods = ["build_concept_chains", "suggest_symbols_from_clusters"]
                method_availability = {method: hasattr(engine, method) for method in expected_methods}
                
                compatibility_results["creative_engine"] = {
                    "status": "available",
                    "method_availability": method_availability,
                    "consolidation_success": all(method_availability.values())
                }
                
                success_count = sum(1 for v in method_availability.values() if v)
                print(f"      ✅ creative_engine: {success_count}/{len(expected_methods)} consolidated methods available")
                
            except Exception as e:
                compatibility_results["creative_engine"] = {
                    "status": "error", 
                    "error": str(e)
                }
                print(f"      ❌ creative_engine: Import/API error - {e}")
            
            # Test memory_analytics API
            try:
                import memory_analytics
                # Note: MemoryAnalyzer needs memory parameter
                
                expected_methods = ["analyze_symbol_clusters"]
                # Check if class exists and method is defined
                has_class = hasattr(memory_analytics, 'MemoryAnalyzer')
                method_exists = False
                
                if has_class:
                    method_exists = hasattr(memory_analytics.MemoryAnalyzer, 'analyze_symbol_clusters')
                
                compatibility_results["memory_analytics"] = {
                    "status": "available" if has_class else "missing_class",
                    "has_analyzer_class": has_class,
                    "has_symbol_clustering": method_exists,
                    "consolidation_success": method_exists
                }
                
                print(f"      ✅ memory_analytics: Class exists: {has_class}, Method exists: {method_exists}")
                
            except Exception as e:
                compatibility_results["memory_analytics"] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"      ❌ memory_analytics: Import/API error - {e}")
                
        except Exception as e:
            print(f"      ❌ General API compatibility error: {e}")
        
        self.audit_results["api_compatibility"] = compatibility_results
    
    def _test_runtime_connections(self):
        """Test runtime execution of claimed connections."""
        print("   Testing runtime connections...")
        
        runtime_results = {}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                sys.path.insert(0, str(self.project_dir))
                
                # Test 1: Unified Memory Integration
                print("      🧪 Testing unified memory integration...")
                try:
                    from unified_memory import get_unified_memory
                    unified_memory = get_unified_memory()
                    
                    # Test basic operations
                    test_item = {"text": "test symbol", "symbol": "🧪", "vector": [0.1, 0.2, 0.3]}
                    unified_memory.store_decision(test_item, "FOLLOW_SYMBOLIC")
                    
                    counts = unified_memory.get_memory_counts()
                    
                    runtime_results["unified_memory_integration"] = {
                        "status": "success",
                        "store_test": "passed",
                        "counts_test": "passed",
                        "memory_counts": counts
                    }
                    print("         ✅ Unified memory integration working")
                    
                except Exception as e:
                    runtime_results["unified_memory_integration"] = {
                        "status": "error",
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    }
                    print(f"         ❌ Unified memory integration failed: {e}")
                
                # Test 2: Creative Engine Consolidation
                print("      🧪 Testing creative engine consolidation...")
                try:
                    from creative_engine import CreativeEngine
                    engine = CreativeEngine(tmpdir)
                    
                    # Test consolidated methods
                    consolidation_tests = {}
                    
                    if hasattr(engine, 'build_concept_chains'):
                        try:
                            chains = engine.build_concept_chains(min_similarity=0.5)
                            consolidation_tests["build_concept_chains"] = "success"
                        except Exception as e:
                            consolidation_tests["build_concept_chains"] = f"error: {e}"
                    else:
                        consolidation_tests["build_concept_chains"] = "method_missing"
                    
                    if hasattr(engine, 'suggest_symbols_from_clusters'):
                        try:
                            suggestions = engine.suggest_symbols_from_clusters(min_cluster_size=2)
                            consolidation_tests["suggest_symbols_from_clusters"] = "success"
                        except Exception as e:
                            consolidation_tests["suggest_symbols_from_clusters"] = f"error: {e}"
                    else:
                        consolidation_tests["suggest_symbols_from_clusters"] = "method_missing"
                    
                    runtime_results["creative_engine_consolidation"] = {
                        "status": "tested",
                        "consolidation_tests": consolidation_tests,
                        "success_rate": sum(1 for v in consolidation_tests.values() if v == "success") / len(consolidation_tests) * 100
                    }
                    
                    success_count = sum(1 for v in consolidation_tests.values() if v == "success")
                    print(f"         ✅ Creative engine: {success_count}/{len(consolidation_tests)} consolidated methods working")
                    
                except Exception as e:
                    runtime_results["creative_engine_consolidation"] = {
                        "status": "error",
                        "error": str(e)
                    }
                    print(f"         ❌ Creative engine consolidation failed: {e}")
                
                # Test 3: Memory Analytics Consolidation
                print("      🧪 Testing memory analytics consolidation...")
                try:
                    from memory_analytics import MemoryAnalyzer
                    from unified_memory import get_unified_memory
                    
                    unified_memory = get_unified_memory()
                    analyzer = MemoryAnalyzer(unified_memory, tmpdir)
                    
                    if hasattr(analyzer, 'analyze_symbol_clusters'):
                        try:
                            cluster_analysis = analyzer.analyze_symbol_clusters(max_features=50, show_visualization=False)
                            runtime_results["memory_analytics_consolidation"] = {
                                "status": "success",
                                "method_exists": True,
                                "execution_result": "success" if "error" not in cluster_analysis else "error",
                                "analysis_keys": list(cluster_analysis.keys()) if isinstance(cluster_analysis, dict) else "non_dict_result"
                            }
                            print("         ✅ Memory analytics consolidation working")
                        except Exception as e:
                            runtime_results["memory_analytics_consolidation"] = {
                                "status": "method_error",
                                "error": str(e)
                            }
                            print(f"         ❌ Memory analytics method error: {e}")
                    else:
                        runtime_results["memory_analytics_consolidation"] = {
                            "status": "method_missing",
                            "error": "analyze_symbol_clusters method not found"
                        }
                        print("         ❌ Memory analytics method missing")
                        
                except Exception as e:
                    runtime_results["memory_analytics_consolidation"] = {
                        "status": "error",
                        "error": str(e)
                    }
                    print(f"         ❌ Memory analytics consolidation failed: {e}")
                
                # Test 4: Standalone Components
                print("      🧪 Testing standalone components...")
                standalone_tests = {}
                
                # Test symbolic_nourishment
                try:
                    from symbolic_nourishment import SymbolicNourishment
                    nourishment = SymbolicNourishment()
                    balance = nourishment.assess_current_balance()
                    standalone_tests["symbolic_nourishment"] = "success"
                    print("         ✅ Symbolic nourishment working")
                except Exception as e:
                    standalone_tests["symbolic_nourishment"] = f"error: {e}"
                    print(f"         ❌ Symbolic nourishment failed: {e}")
                
                # Test expanded_symbolic_core
                try:
                    from expanded_symbolic_core import create_expanded_symbolic_core
                    core_symbols = create_expanded_symbolic_core()
                    standalone_tests["expanded_symbolic_core"] = "success"
                    print("         ✅ Expanded symbolic core working")
                except Exception as e:
                    standalone_tests["expanded_symbolic_core"] = f"error: {e}"
                    print(f"         ❌ Expanded symbolic core failed: {e}")
                
                runtime_results["standalone_components"] = {
                    "status": "tested",
                    "component_tests": standalone_tests,
                    "success_rate": sum(1 for v in standalone_tests.values() if v == "success") / len(standalone_tests) * 100
                }
                
            except Exception as e:
                runtime_results["general_error"] = {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                print(f"      ❌ General runtime testing error: {e}")
        
        self.audit_results["runtime_testing"] = runtime_results
    
    def _analyze_errors(self):
        """Analyze errors that contradict integration claims."""
        print("   Analyzing integration errors...")
        
        error_analysis = {
            "import_errors": [],
            "missing_dependencies": [],
            "api_mismatches": [],
            "runtime_failures": [],
            "consolidation_gaps": []
        }
        
        # Check import analysis for errors
        for file_name, analysis in self.audit_results["import_analysis"].items():
            if analysis.get("status") == "parse_error":
                error_analysis["import_errors"].append({
                    "file": file_name,
                    "error": analysis.get("error")
                })
        
        # Check function verification for missing methods
        for file_name, verification in self.audit_results["function_verification"].items():
            missing_methods = verification.get("missing_methods", [])
            if missing_methods:
                error_analysis["consolidation_gaps"].extend([
                    {"file": file_name, "missing_method": method} for method in missing_methods
                ])
        
        # Check API compatibility for errors
        for component, compatibility in self.audit_results["api_compatibility"].items():
            if compatibility.get("status") == "error":
                error_analysis["api_mismatches"].append({
                    "component": component,
                    "error": compatibility.get("error")
                })
        
        # Check runtime testing for failures
        for test_name, results in self.audit_results["runtime_testing"].items():
            if results.get("status") == "error":
                error_analysis["runtime_failures"].append({
                    "test": test_name,
                    "error": results.get("error")
                })
        
        self.audit_results["error_analysis"] = error_analysis
        
        total_errors = sum(len(errors) for errors in error_analysis.values())
        print(f"      📊 Total integration errors found: {total_errors}")
        
        for error_type, errors in error_analysis.items():
            if errors:
                print(f"         ❌ {error_type}: {len(errors)} issues")
    
    def _generate_assessment(self):
        """Generate final assessment comparing claims vs reality."""
        print("   Generating final assessment...")
        
        assessment = {
            "consolidation_claims_vs_reality": {},
            "integration_accuracy": {},
            "critical_discrepancies": [],
            "validation_score": 0.0
        }
        
        # Analyze consolidation claims
        for file_name, claimed in self.claimed_integrations.items():
            reality_check = {
                "claimed_status": claimed["status"],
                "actual_status": "unknown",
                "verification_results": {}
            }
            
            if claimed["status"] == "consolidated_into_creative_engine":
                # Check if method exists in creative_engine.py
                ce_verification = self.audit_results["function_verification"].get("creative_engine.py", {})
                found_methods = ce_verification.get("found_methods", [])
                expected_method = claimed["method"].replace("()", "")
                
                if expected_method in found_methods:
                    reality_check["actual_status"] = "successfully_consolidated"
                    reality_check["verification_results"]["method_exists"] = True
                else:
                    reality_check["actual_status"] = "consolidation_failed"
                    reality_check["verification_results"]["method_exists"] = False
                    assessment["critical_discrepancies"].append(
                        f"CLAIM: {file_name} consolidated into creative_engine.py - REALITY: Method {expected_method} not found"
                    )
            
            elif claimed["status"] == "consolidated_into_memory_analytics":
                # Check if method exists in memory_analytics.py
                ma_verification = self.audit_results["function_verification"].get("memory_analytics.py", {})
                found_methods = ma_verification.get("found_methods", [])
                expected_method = claimed["method"].replace("()", "")
                
                if expected_method in found_methods:
                    reality_check["actual_status"] = "successfully_consolidated"
                    reality_check["verification_results"]["method_exists"] = True
                else:
                    reality_check["actual_status"] = "consolidation_failed"
                    reality_check["verification_results"]["method_exists"] = False
                    assessment["critical_discrepancies"].append(
                        f"CLAIM: {file_name} consolidated into memory_analytics.py - REALITY: Method {expected_method} not found"
                    )
            
            elif claimed["status"] in ["standalone_gold_standard", "standalone_foundational"]:
                # Check if standalone component works
                runtime_results = self.audit_results["runtime_testing"].get("standalone_components", {})
                component_tests = runtime_results.get("component_tests", {})
                component_key = file_name.replace(".py", "")
                
                if component_tests.get(component_key) == "success":
                    reality_check["actual_status"] = "standalone_working"
                    reality_check["verification_results"]["runtime_success"] = True
                else:
                    reality_check["actual_status"] = "standalone_failed"
                    reality_check["verification_results"]["runtime_success"] = False
                    assessment["critical_discrepancies"].append(
                        f"CLAIM: {file_name} is working standalone - REALITY: Runtime test failed"
                    )
            
            assessment["consolidation_claims_vs_reality"][file_name] = reality_check
        
        # Calculate validation score
        total_claims = len(self.claimed_integrations)
        successful_validations = sum(
            1 for check in assessment["consolidation_claims_vs_reality"].values()
            if "successfully_consolidated" in check["actual_status"] or "standalone_working" in check["actual_status"]
        )
        
        assessment["validation_score"] = (successful_validations / total_claims) * 100
        
        # Determine overall assessment
        if assessment["validation_score"] >= 80:
            assessment["overall_validation"] = "CLAIMS_MOSTLY_ACCURATE"
        elif assessment["validation_score"] >= 60:
            assessment["overall_validation"] = "CLAIMS_PARTIALLY_ACCURATE" 
        else:
            assessment["overall_validation"] = "CLAIMS_SIGNIFICANTLY_INACCURATE"
        
        self.audit_results["claimed_vs_actual"] = assessment
        self.audit_results["overall_assessment"] = assessment["overall_validation"]
        
        print(f"      📊 Validation Score: {assessment['validation_score']:.1f}%")
        print(f"      🎯 Overall Assessment: {assessment['overall_validation']}")
        print(f"      ⚠️ Critical Discrepancies: {len(assessment['critical_discrepancies'])}")

def main():
    """Run the comprehensive GROUP D integration audit."""
    project_dir = "/mnt/c/Users/kaitl/Documents/Core-Project - Copy"
    
    auditor = GroupDIntegrationAuditor(project_dir)
    results = auditor.run_comprehensive_audit()
    
    # Save detailed audit results
    audit_file = Path(project_dir) / "data" / "group_d_integration_audit_results.json"
    audit_file.parent.mkdir(exist_ok=True)
    
    with open(audit_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Detailed audit results saved to: {audit_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("🔍 GROUP D INTEGRATION AUDIT SUMMARY")
    print("=" * 70)
    
    assessment = results["claimed_vs_actual"]
    print(f"📊 Validation Score: {assessment['validation_score']:.1f}%")
    print(f"🎯 Overall Assessment: {assessment['overall_validation']}")
    
    if assessment["critical_discrepancies"]:
        print(f"\n❌ CRITICAL DISCREPANCIES FOUND:")
        for i, discrepancy in enumerate(assessment["critical_discrepancies"], 1):
            print(f"   {i}. {discrepancy}")
    
    print(f"\n📋 CONSOLIDATION VERIFICATION:")
    for file_name, verification in assessment["consolidation_claims_vs_reality"].items():
        status_icon = "✅" if "successfully" in verification["actual_status"] or "working" in verification["actual_status"] else "❌"
        print(f"   {status_icon} {file_name}: {verification['actual_status']}")
    
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    audit_results = main()