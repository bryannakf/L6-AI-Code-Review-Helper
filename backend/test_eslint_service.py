from services.eslint_service import analyse_javascript

code = """
function add(a,b) {
    return a+b;
}
"""

result = analyse_javascript(code)

print(result)