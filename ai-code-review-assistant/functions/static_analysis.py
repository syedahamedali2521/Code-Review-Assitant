import ast
import re
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def analyze_python_code(code):
    """
    Perform static analysis on Python code.
    Returns dict with unused vars, imports, complexity, maintainability index.
    """
    try:
        tree = ast.parse(code)
        analyzer = PythonAnalyzer()
        analyzer.visit(tree)

        complexity = sum(f.complexity for f in cc_visit(code))
        mi = mi_visit(code, multi=True)

        return {
            'unused_variables': analyzer.unused_vars,
            'unused_imports': analyzer.unused_imports,
            'complexity': complexity,
            'maintainability_index': mi
        }
    except SyntaxError as e:
        return {'error': f'Syntax error: {e}'}

class PythonAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.unused_vars = []
        self.unused_imports = []
        self.defined_vars = set()
        self.used_vars = set()
        self.imports = {}

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = node.lineno
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.defined_vars.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.defined_vars.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.defined_vars.add(node.name)
        self.generic_visit(node)

    def finalize(self):
        self.unused_vars = list(self.defined_vars - self.used_vars)
        self.unused_imports = [imp for imp in self.imports if imp not in self.used_vars]

def analyze_js_code(code):
    """
    Perform basic static analysis on JS code using regex.
    Returns dict with issues found.
    """
    issues = []

    # Check for console.log
    if re.search(r'console\.log', code):
        issues.append('console.log found - remove for production')

    # Check for var usage (prefer let/const)
    var_matches = re.findall(r'\bvar\s+\w+', code)
    if var_matches:
        issues.append(f'Use of var: {len(var_matches)} instances - prefer let/const')

    # Check for missing semicolons (basic)
    lines = code.split('\n')
    missing_semi = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith('//') and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
            if re.search(r'[a-zA-Z_]\w*\s*=', line) or re.search(r'return\s', line):
                missing_semi += 1
    if missing_semi > 0:
        issues.append(f'Possible missing semicolons: {missing_semi}')

    # Basic complexity: count functions
    func_count = len(re.findall(r'function\s+\w+', code)) + len(re.findall(r'=>\s*\{', code))
    issues.append(f'Function count: {func_count}')

    return {'issues': issues}
