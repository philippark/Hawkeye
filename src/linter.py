import ast
import sys

class Linter(ast.NodeVisitor):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.scopes = [{
            "assigned": set(),
            "used": set(),
            "start_line": 0,
            "end_line": -1
        }]
        self.issues = []
        self.source_lines = []

    def _push_scope(self, node):
        """ Pushes a new scope onto the stack. """
        self.scopes.append({
            "assigned": set(),
            "used": set(),
            "start_line": node.lineno,
            "end_line": getattr(node, 'end_lineno', -1)
        })

    def _pop_scope(self):
        """ Pops a scope and checks for unused variables before doing so. """
        scope = self.scopes.pop()
        unused_variables = scope["assigned"] - scope["used"]
        for var_name in sorted(list(unused_variables)):
            self.issues.append(f"{self.filename}:{scope['start_line']} | Unused variable '{var_name}'")

    def visit_FunctionDef(self, node):
        self._push_scope(node)
        for arg in node.args.args:
            self.scopes[-1]["assigned"].add(arg.arg)
        self.generic_visit(node)
        self._pop_scope()

    def visit_ClassDef(self, node):
        self._push_scope(node)
        self.generic_visit(node)
        self._pop_scope()

    def visit_Name(self, node):
        """ Visits a variable name. Determines if the variable is being assigned or used. """
        if isinstance(node.ctx, ast.Store):
            self.scopes[-1]["assigned"].add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.scopes[-1]["used"].add(node.id)

    def check_line_formatting(self):
        """ Checks for line formatting issues such as trailing whitespace and line length. """
        for lineno, line in enumerate(self.source_lines, start=1):
            line = line.rstrip('\n\r')

            if len(line) > 80:
                self.issues.append(f"{self.filename}:{lineno} | Line exceeds 80 characters")

            if line != line.rstrip():
                self.issues.append(f"{self.filename}:{lineno} | Trailing whitespace detected")

    def run(self, source_code):
        self.source_lines = source_code.splitlines(keepends=True)

        # traverse AST to check for unused variables
        tree = ast.parse(source_code, filename=self.filename)
        self.visit(tree)
        self._pop_scope()

        self.check_line_formatting()

        # Sort issues by line number
        self.issues.sort(key=lambda x: int(x.split(':')[1].split(' ')[0]))

        return self.issues

def main():
    """Main function to parse the file and run the linter."""
    if len(sys.argv) < 2:
        print("Usage: python linter.py <file_to_lint.py>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        
        linter = Linter(file_path)
        issues = linter.run(source_code)
        
        if issues:
            print("Linter found the following issues:")
            for issue in issues:
                print(issue)
        else:
            print("No issues found! Great job!")

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()