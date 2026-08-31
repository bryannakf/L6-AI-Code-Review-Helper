import time
from services.ai_service import analyse_code

# Test Python

python_code = """
def divide(a, b):
    password = "secret123"
    print(password)
    result = a / b
    return result
"""

python_start = time.perf_counter()

python_result = analyse_code(
    python_code,
    "python"
)

python_end = time.perf_counter()

python_time = python_end - python_start

print("PYTHON RESULT:")
print(python_result)

print(f"Python AI analysis time: {python_time:.2f} seconds")

# Test JavaScript

javascript_code = """
function login(username, password) {
    const query = "SELECT * FROM users WHERE username = '" + username + "'";
    console.log(password);
    return query;
}
"""

javascript_start = time.perf_counter()

javascript_result = analyse_code(
    javascript_code,
    "javascript"
)

javascript_end = time.perf_counter()

javascript_time = javascript_end - javascript_start

print("\nJAVASCRIPT RESULT:")
print(javascript_result)

print(f"JavaScript AI analysis time: {javascript_time:.2f} seconds")