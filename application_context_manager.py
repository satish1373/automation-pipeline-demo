import os
import ast
import json
import re
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

class ApplicationContextAnalyzer:
    """Analyzes existing application and builds comprehensive context"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def analyze_application(self) -> Dict[str, Any]:
        """Perform comprehensive application analysis"""
        print("Starting comprehensive application context analysis...")
        
        context = {
            "project_name": self.project_path.name,
            "framework": self._detect_framework(),
            "language": "TypeScript",
            "last_analyzed": datetime.now().isoformat(),
            "file_analyses": self._analyze_all_files(),
            "components": self._analyze_components(),
            "dependencies": self._analyze_dependencies(),
            "file_tree": self._build_file_tree(),
            "api_endpoints": self._find_api_endpoints(),
            "state_management": self._analyze_state_management()
        }
        
        print(f"Analysis complete! Found {len(context['components'])} components")
        return context
    
    def _detect_framework(self) -> str:
        """Detect the application framework"""
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            with open(package_json_path, "r") as f:
                package_data = json.load(f)
                dependencies = package_data.get("dependencies", {})
                if "react" in dependencies:
                    return "React"
        return "Unknown"
    
    def _get_source_files(self) -> List[Path]:
        """Get all source files to analyze"""
        source_extensions = {".js", ".jsx", ".ts", ".tsx"}
        source_files = []
        
        src_dir = self.project_path / "src"
        if src_dir.exists():
            for file_path in src_dir.rglob("*"):
                if file_path.suffix in source_extensions:
                    source_files.append(file_path)
        
        return source_files
    
    def _analyze_all_files(self) -> Dict[str, Dict]:
        """Analyze all relevant files in the project"""
        file_analyses = {}
        
        for file_path in self._get_source_files():
            try:
                analysis = self._analyze_single_file(file_path)
                if analysis:
                    relative_path = str(file_path.relative_to(self.project_path))
                    file_analyses[relative_path] = analysis
            except Exception as e:
                print(f"Warning: Could not analyze {file_path}: {e}")
        
        return file_analyses
    
    def _analyze_single_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a single source file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return None
        
        analysis = {
            "path": str(file_path.relative_to(self.project_path)),
            "type": self._determine_file_type(file_path, content),
            "lines_of_code": len([line for line in content.split("\n") if line.strip()]),
            "functions": self._extract_functions(content),
            "imports": self._extract_imports(content),
            "hooks_used": self._extract_hooks(content),
            "components_used": self._extract_component_usage(content)
        }
        
        return analysis
    
    def _determine_file_type(self, file_path: Path, content: str) -> str:
        """Determine the type/purpose of a file"""
        file_name = file_path.name.lower()
        
        if "test" in file_name or "spec" in file_name:
            return "test"
        elif file_path.suffix in [".jsx", ".tsx"] or "component" in file_name:
            return "component"
        elif "service" in file_name or "api" in file_name:
            return "service"
        elif "util" in file_name or "helper" in file_name:
            return "utility"
        else:
            return "module"
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from content"""
        functions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('function '):
                func_match = re.search(r'function\s+(\w+)', line)
                if func_match:
                    functions.append(func_match.group(1))
            elif 'const ' in line and '=>' in line:
                const_match = re.search(r'const\s+(\w+)\s*=', line)
                if const_match:
                    functions.append(const_match.group(1))
        
        return list(set(functions))
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []
        for line in content.split("\n"):
            if line.strip().startswith("import "):
                imports.append(line.strip())
        return imports
    
    def _extract_hooks(self, content: str) -> List[str]:
        """Extract React hooks used"""
        hooks = []
        hook_names = ['useState', 'useEffect', 'useContext', 'useReducer', 'useMemo', 'useCallback']
        
        for hook in hook_names:
            if hook in content:
                hooks.append(hook)
        
        return hooks
    
    def _extract_component_usage(self, content: str) -> List[str]:
        """Extract components used in JSX"""
        components = []
        lines = content.split('\n')
        
        for line in lines:
            # Simple component detection for JSX tags starting with capital letter
            import_matches = re.findall(r'<([A-Z]\w+)', line)
            components.extend(import_matches)
        
        return list(set(components))
    
    def _analyze_components(self) -> Dict[str, Dict]:
        """Analyze React components and their relationships"""
        components = {}
        
        component_files = [f for f in self._get_source_files() 
                          if f.suffix in [".jsx", ".tsx"] and "test" not in f.name.lower()]
        
        for file_path in component_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                component_name = file_path.stem
                components[component_name] = {
                    "name": component_name,
                    "file_path": str(file_path.relative_to(self.project_path)),
                    "hooks_used": self._extract_hooks(content),
                    "children_components": self._extract_component_usage(content),
                    "has_state": "useState" in content,
                    "has_effects": "useEffect" in content
                }
                
            except Exception as e:
                print(f"Warning: Could not analyze component {file_path}: {e}")
        
        return components
    
    def _analyze_dependencies(self) -> Dict[str, str]:
        """Analyze package dependencies"""
        deps = {}
        
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, "r") as f:
                    package_data = json.load(f)
                    deps = package_data.get("dependencies", {})
            except Exception as e:
                print(f"Warning: Could not parse package.json: {e}")
        
        return deps
    
    def _build_file_tree(self) -> Dict[str, Any]:
        """Build hierarchical file tree structure"""
        def build_tree(path: Path) -> Dict[str, Any]:
            tree = {"type": "directory", "children": {}}
            
            try:
                for child in path.iterdir():
                    if child.name.startswith(".") and child.name not in [".env.example"]:
                        continue
                    if child.name in ["node_modules", "dist", "build", "coverage"]:
                        continue
                    
                    if child.is_file():
                        tree["children"][child.name] = {
                            "type": "file",
                            "size": child.stat().st_size,
                            "extension": child.suffix
                        }
                    elif child.is_dir():
                        tree["children"][child.name] = build_tree(child)
            except:
                pass
            
            return tree
        
        return build_tree(self.project_path)
    
    def _find_api_endpoints(self) -> List[str]:
        """Find API endpoints in the code"""
        endpoints = []
        
        for file_path in self._get_source_files():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Simple API endpoint detection
                if 'fetch(' in content:
                    endpoints.append('fetch_api_detected')
                if 'axios' in content:
                    endpoints.append('axios_api_detected')
                    
            except:
                continue
        
        return list(set(endpoints))
    
    def _analyze_state_management(self) -> List[str]:
        """Analyze state management patterns used"""
        patterns = set()
        
        for file_path in self._get_source_files():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if "useState" in content or "useReducer" in content:
                    patterns.add("React Hooks")
                if "redux" in content.lower():
                    patterns.add("Redux")
                if "context" in content.lower() and "provider" in content.lower():
                    patterns.add("React Context")
                    
            except:
                continue
        
        return list(patterns)

if __name__ == "__main__":
    analyzer = ApplicationContextAnalyzer(".")
    context = analyzer.analyze_application()
    
    # Save context to file
    with open("application_context.json", "w") as f:
        json.dump(context, f, indent=2, default=str)
    
    print(f"Context saved to application_context.json")
    print(f"Found {len(context['components'])} components")
    print(f"Dependencies: {len(context['dependencies'])}")
    print(f"State management: {context['state_management']}")
