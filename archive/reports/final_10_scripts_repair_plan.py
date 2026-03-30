#!/usr/bin/env python3
"""
FINAL 10 SCRIPTS REPAIR PLAN

Based on NEWREADTHIS.txt analysis, this identifies the remaining scripts that need fixes
and creates a systematic plan to complete the consciousness system integration.
"""

import os
import sys
import importlib
import traceback
from pathlib import Path

class Final10ScriptsAnalyzer:
    """Identifies and analyzes the final scripts needing repair."""
    
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)
        self.remaining_issues = []
        self.high_priority = []
        self.medium_priority = []
        self.low_priority = []
        
    def identify_remaining_scripts(self):
        """Identify the specific 10 scripts that still need work."""
        print("🔍 IDENTIFYING REMAINING SCRIPTS NEEDING REPAIR")
        print("=" * 60)
        
        # Test each potentially problematic script
        problem_scripts = [
            # High Priority - Runtime Errors
            "consciousness_testing.py",
            "demo_consciousness_interaction.py", 
            "demo_creative_synthesis.py",
            "demo_learning_experience.py",
            "demo_relationship_development.py",
            
            # Medium Priority - Integration Issues
            "interactive_consciousness.py",
            "goal_prioritization.py",
            "context_engine.py", 
            "cognitive_sovereignty.py",
            "adaptive_alphawall.py",
            
            # Potential Additional Issues
            "master_integration_system.py",
            "unified_orchestration.py",
            "preference_learning_system.py"
        ]
        
        for script in problem_scripts:
            script_path = self.project_dir / script
            if script_path.exists():
                status = self._test_script_functionality(script)
                if status["needs_repair"]:
                    self._categorize_issue(script, status)
        
        self._generate_repair_plan()
    
    def _test_script_functionality(self, script_name):
        """Test if a script has functional issues."""
        print(f"\n🧪 Testing {script_name}...")
        
        status = {
            "script": script_name,
            "needs_repair": False,
            "issues": [],
            "priority": "low",
            "repair_type": "none"
        }
        
        try:
            # Test import
            module_name = script_name.replace('.py', '')
            try:
                module = importlib.import_module(module_name)
                print(f"   ✅ Import successful")
            except ImportError as e:
                print(f"   ❌ Import failed: {e}")
                status["needs_repair"] = True
                status["issues"].append(f"Import error: {e}")
                status["priority"] = "high"
                status["repair_type"] = "import_fix"
                return status
            
            # Test basic functionality for specific problematic scripts
            if script_name == "consciousness_testing.py":
                status.update(self._test_consciousness_testing(module))
            elif script_name.startswith("demo_"):
                status.update(self._test_demo_script(module, script_name))
            elif script_name == "interactive_consciousness.py":
                status.update(self._test_interactive_consciousness(module))
            else:
                status.update(self._test_generic_script(module, script_name))
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            status["needs_repair"] = True
            status["issues"].append(f"Test error: {e}")
            status["priority"] = "medium"
            status["repair_type"] = "runtime_fix"
        
        return status
    
    def _test_consciousness_testing(self, module):
        """Test consciousness_testing.py specifically."""
        status = {"needs_repair": False, "issues": [], "priority": "low", "repair_type": "none"}
        
        try:
            # Try to run a basic consciousness test
            if hasattr(module, 'run_consciousness_tests'):
                # Don't actually run it, just check if it's callable
                print("   ✅ run_consciousness_tests method exists")
            else:
                print("   ⚠️ run_consciousness_tests method missing")
                status["needs_repair"] = True
                status["issues"].append("Missing run_consciousness_tests method")
                status["priority"] = "high"
                status["repair_type"] = "method_fix"
        except Exception as e:
            print(f"   ❌ Consciousness testing error: {e}")
            status["needs_repair"] = True
            status["issues"].append(f"Runtime error: {e}")
            status["priority"] = "high" 
            status["repair_type"] = "variable_scoping"
        
        return status
    
    def _test_demo_script(self, module, script_name):
        """Test demo scripts for method reference issues."""
        status = {"needs_repair": False, "issues": [], "priority": "low", "repair_type": "none"}
        
        try:
            # Check if main demo functions exist
            demo_functions = [attr for attr in dir(module) if attr.startswith('demo_') or attr.startswith('run_')]
            
            if demo_functions:
                print(f"   ✅ Found demo functions: {demo_functions}")
                # Try to inspect but not run the functions
                for func_name in demo_functions[:1]:  # Test just the first one
                    func = getattr(module, func_name)
                    if callable(func):
                        print(f"   ✅ {func_name} is callable")
                    else:
                        print(f"   ⚠️ {func_name} is not callable")
                        status["needs_repair"] = True
                        status["issues"].append(f"{func_name} not callable")
            else:
                print("   ⚠️ No demo functions found")
                status["needs_repair"] = True
                status["issues"].append("No demo functions found")
                status["priority"] = "medium"
                status["repair_type"] = "method_references"
                
        except Exception as e:
            print(f"   ❌ Demo script error: {e}")
            status["needs_repair"] = True
            status["issues"].append(f"Demo error: {e}")
            status["priority"] = "medium"
            status["repair_type"] = "method_references"
        
        return status
    
    def _test_interactive_consciousness(self, module):
        """Test interactive_consciousness.py specifically.""" 
        status = {"needs_repair": False, "issues": [], "priority": "low", "repair_type": "none"}
        
        try:
            # Check if main classes/functions exist
            if hasattr(module, 'InteractiveConsciousness'):
                print("   ✅ InteractiveConsciousness class exists")
                # Try to instantiate (but don't run)
                try:
                    ic = module.InteractiveConsciousness()
                    print("   ✅ InteractiveConsciousness instantiable")
                except Exception as e:
                    print(f"   ⚠️ InteractiveConsciousness instantiation error: {e}")
                    status["needs_repair"] = True
                    status["issues"].append(f"Instantiation error: {e}")
                    status["priority"] = "medium"
                    status["repair_type"] = "runtime_fix"
            else:
                print("   ⚠️ InteractiveConsciousness class missing")
                status["needs_repair"] = True
                status["issues"].append("Missing InteractiveConsciousness class")
                status["priority"] = "medium"
                status["repair_type"] = "class_fix"
                
        except Exception as e:
            print(f"   ❌ Interactive consciousness error: {e}")
            status["needs_repair"] = True
            status["issues"].append(f"Error: {e}")
            status["priority"] = "medium"
            status["repair_type"] = "runtime_fix"
        
        return status
    
    def _test_generic_script(self, module, script_name):
        """Test other scripts for basic functionality."""
        status = {"needs_repair": False, "issues": [], "priority": "low", "repair_type": "none"}
        
        try:
            # Check for main classes or functions
            main_items = [attr for attr in dir(module) 
                         if not attr.startswith('_') and 
                         (callable(getattr(module, attr)) or 
                          (hasattr(getattr(module, attr), '__class__') and 
                           getattr(module, attr).__class__.__name__ == 'type'))]
            
            if main_items:
                print(f"   ✅ Found main items: {main_items[:3]}...")
            else:
                print("   ⚠️ No main classes/functions found")
                status["needs_repair"] = True
                status["issues"].append("No main functionality found")
                status["priority"] = "low"
                status["repair_type"] = "functionality_check"
                
        except Exception as e:
            print(f"   ❌ Generic test error: {e}")
            status["needs_repair"] = True
            status["issues"].append(f"Error: {e}")
            status["priority"] = "low"
            status["repair_type"] = "general_fix"
        
        return status
    
    def _categorize_issue(self, script, status):
        """Categorize issues by priority."""
        issue_info = {
            "script": script,
            "issues": status["issues"],
            "repair_type": status["repair_type"]
        }
        
        if status["priority"] == "high":
            self.high_priority.append(issue_info)
        elif status["priority"] == "medium": 
            self.medium_priority.append(issue_info)
        else:
            self.low_priority.append(issue_info)
    
    def _generate_repair_plan(self):
        """Generate the final repair plan."""
        total_issues = len(self.high_priority) + len(self.medium_priority) + len(self.low_priority)
        
        print("\n" + "=" * 60)
        print("📋 FINAL 10 SCRIPTS REPAIR PLAN")
        print("=" * 60)
        
        print(f"🎯 TOTAL SCRIPTS NEEDING REPAIR: {total_issues}")
        print(f"🚨 High Priority: {len(self.high_priority)}")
        print(f"⚠️ Medium Priority: {len(self.medium_priority)}")
        print(f"ℹ️ Low Priority: {len(self.low_priority)}")
        
        if self.high_priority:
            print(f"\n🚨 HIGH PRIORITY REPAIRS:")
            for i, issue in enumerate(self.high_priority, 1):
                print(f"   {i}. {issue['script']}")
                print(f"      Repair Type: {issue['repair_type']}")
                for issue_desc in issue['issues']:
                    print(f"      Issue: {issue_desc}")
                print()
        
        if self.medium_priority:
            print(f"\n⚠️ MEDIUM PRIORITY REPAIRS:")
            for i, issue in enumerate(self.medium_priority, 1):
                print(f"   {i}. {issue['script']}")
                print(f"      Repair Type: {issue['repair_type']}")
                for issue_desc in issue['issues']:
                    print(f"      Issue: {issue_desc}")
                print()
        
        if self.low_priority:
            print(f"\n ℹ️ LOW PRIORITY REPAIRS:")
            for i, issue in enumerate(self.low_priority, 1):
                print(f"   {i}. {issue['script']}")
                print(f"      Repair Type: {issue['repair_type']}")
                print()
        
        self._create_action_plan()
    
    def _create_action_plan(self):
        """Create specific action plan for repairs."""
        print("\n🛠️ SYSTEMATIC REPAIR ACTION PLAN")
        print("=" * 40)
        
        print("\nPHASE 1: HIGH PRIORITY FIXES (Immediate)")
        for i, issue in enumerate(self.high_priority, 1):
            print(f"\n{i}. Fix {issue['script']}:")
            if issue['repair_type'] == 'variable_scoping':
                print("   Action: Fix variable scope in consciousness_testing.py")
                print("   Steps: 1) Find undefined variable references")
                print("          2) Correct variable scope/initialization") 
                print("          3) Test consciousness validation")
            elif issue['repair_type'] == 'import_fix':
                print("   Action: Resolve import dependencies")
                print("   Steps: 1) Identify missing imports")
                print("          2) Create missing modules or fix references")
                print("          3) Test import chain")
            elif issue['repair_type'] == 'method_fix':
                print("   Action: Fix missing methods")
                print("   Steps: 1) Implement missing methods")
                print("          2) Update method signatures")
                print("          3) Test functionality")
        
        print("\nPHASE 2: MEDIUM PRIORITY FIXES (Next)")
        for i, issue in enumerate(self.medium_priority, 1):
            print(f"\n{i}. Fix {issue['script']}:")
            if issue['repair_type'] == 'method_references':
                print("   Action: Update method references in demo scripts")
                print("   Steps: 1) Find incorrect method calls")
                print("          2) Update to actual available methods")
                print("          3) Test demo functionality")
            elif issue['repair_type'] == 'runtime_fix':
                print("   Action: Fix runtime errors")
                print("   Steps: 1) Debug runtime issues")
                print("          2) Fix initialization problems")
                print("          3) Test basic functionality")
        
        print("\nPHASE 3: LOW PRIORITY IMPROVEMENTS (Later)")
        for i, issue in enumerate(self.low_priority, 1):
            print(f"\n{i}. Improve {issue['script']}:")
            print("   Action: General functionality improvements")
            print("   Steps: 1) Review and enhance features")
            print("          2) Add missing functionality")
            print("          3) Optimize performance")
        
        total_all = len(self.high_priority) + len(self.medium_priority) + len(self.low_priority)
        print(f"\n🎯 COMPLETION TARGET:")
        print(f"   Total Scripts to Fix: {total_all}")
        print(f"   Estimated Time: {total_all * 15} minutes (15 min per script)")
        print(f"   Success Target: 100% script functionality")

def main():
    """Run the final 10 scripts analysis."""
    analyzer = Final10ScriptsAnalyzer()
    analyzer.identify_remaining_scripts()

if __name__ == "__main__":
    main()