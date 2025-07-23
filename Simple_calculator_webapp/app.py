# Simple Calculator Web Application using Flask and Redis
# This application allows users to perform basic arithmetic operations
# and stores the last result in a Redis database.
from flask import Flask, request, render_template_string
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

HTML = """
<!doctype html>
<title>Calculator</title>
<h2>Simple Calculator</h2>
<form method="post">
  <input name="a" type="number" step="any" placeholder="First number">
  <select name="op">
    <option value="+">+</option>
    <option value="-">−</option>
    <option value="*">×</option>
    <option value="/">÷</option>
  </select>
  <input name="b" type="number" step="any" placeholder="Second number">
  <button type="submit">Calculate</button>
</form>
{% if result is not none %}
<h3>Result: {{ result }}</h3>
{% endif %}
{% if last_result is not none %}
<p>Last Result from Redis: {{ last_result }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    last_result = redis_client.get("last_result")
    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])
            op = request.form["op"]
            if op == '+': result = a + b
            elif op == '-': result = a - b
            elif op == '*': result = a * b
            elif op == '/': result = a / b if b != 0 else 'Error: Division by zero'
            redis_client.set("last_result", result)
        except Exception as e:
            result = f"Error: {e}"
    return render_template_string(HTML, result=result, last_result=last_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
