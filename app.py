import math
from flask import Flask, request, render_template_string

app = Flask(__name__)

def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    score = 0
    if length >= 8:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score <= 2:
        return "You're on Hacker's radar"
    elif score == 3 or score == 4:
        return "Not Out of Sight Yet"
    else:
        return "Password Hero"
    
def estimate_crack_time(password):
    length = len(password)
    char_space = 0
    if any(c.islower() for c in password):
        char_space += 26
    if any(c.isupper() for c in password):
        char_space += 26
    if any(c.isdigit() for c in password):
        char_space += 10
    if any(not c.isalnum() for c in password):
        char_space += 32  # Approx. common special chars
    
    if char_space == 0:
        return "Instantly cracked"
    
    entropy = length * math.log2(char_space)
    guesses_per_second = 10_000_000_000  # 10 billion guesses per second
    seconds = 2 ** entropy / guesses_per_second
    
    if seconds < 1:
        return "Less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days"
    else:
        years = seconds / 31536000
        return f"{years:.2f} years"

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    time_to_crack = ""
    password = ""
    if request.method == "POST":
        password = request.form.get("password", "")
        strength = check_password_strength(password)
        time_to_crack = estimate_crack_time(password)
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Password Strength Checker</title>
<style>
    body { font-family: Arial, sans-serif; padding: 20px; background: #2B2B2C; }
    .container { max-width: 400px; margin: auto; background: #E9825D; padding: 20px; border-radius: 8px; color:#491d2a;  }
    label { font-weight: bold; display: block; margin-bottom: 8px; }
    input[type="password"] { width: 80%; padding: 6px; margin-bottom: 15px; }
    button { padding: 10px 15px; background: #491D2A; color: white; border: none; border-radius: 5px; cursor: pointer; }
    .strength { font-weight: bold; font-size: 1.2em; color:#1C351D;}
    .time { margin-top: 10px; font-weight: bold; color: #491D2A; }                             
</style>
</head>
<body>
<div class="container">
    <h2>Password Strength Checker</h2>
    <form method="post">
        <label for="password">Enter Password:</label>
        <input type="password" id="password" name="password" value="{{ password }}" required />
        <button type="submit">Check Strength</button>
    </form>
    {% if strength %}
    <p>Password Strength: <span class="strength">{{ strength }}</span></p>
    <p class="time">Estimated Time to Crack: {{ time_to_crack }}</p>
    {% endif %}
</div>
</body>
</html>
""", strength=strength, time_to_crack=time_to_crack, password=password)


if __name__ == "__main__":
    app.run(debug=True)

