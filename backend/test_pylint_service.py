from services.pylint_service import analyse_python

code = """
def add(a,b):
    return a+b
"""

result = analyse_python(code)

print(result)