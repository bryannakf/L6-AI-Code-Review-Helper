from services.ai_service import analyse_code

# Test Python

python_code = """
def divide(a, b):
    password = "secret123"
    print(password)
    result = a / b
    return result
"""

python_result = analyse_code(
    python_code,
    "python"
)

print("PYTHON RESULT:")
print(python_result)


# Test JavaScript

javascript_code = """
function login(username, password) {
    const query = "SELECT * FROM users WHERE username = '" + username + "'";
    console.log(password);
    return query;
}
"""

javascript_result = analyse_code(
    javascript_code,
    "javascript"
)

print("\nJAVASCRIPT RESULT:")
print(javascript_result)
