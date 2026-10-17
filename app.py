from flask import Flask, render_template_string, request, redirect
import os

app = Flask(__name__)

BUDGET_FILE = "budget.txt"
EXPENSE_FILE = "expenses.txt"

def get_budget():
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r") as f:
                return int(f.read())
        except:
            return 800
    return 800

def get_expenses():
    if not os.path.exists(EXPENSE_FILE):
        return [], 0
    try:
        with open(EXPENSE_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        lines = []
    total = 0
    for line in lines:
        if "جنيه" in line:
            try:
                total += int(line.split("-")[-1].replace("جنيه","").strip())
            except:
                pass
    return lines, total

HTML_PAGE = """
<html dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ahmed yones Live</title>
<style>
body { font-family: Arial; background: linear-gradient(135deg, #0f0f0f, #1a1a2e); color: white; text-align: center; padding: 15px; min-height: 100vh; }
.card { background: rgba(255,255,255,0.08); backdrop-filter: blur(10px); padding: 20px; border-radius: 20px; margin: 15px auto; max-width: 550px; border: 1px solid #333; box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
input, button { padding: 12px 15px; border-radius: 10px; border: none; margin: 5px; font-size: 16px; }
input { background: #222; color: white; border: 1px solid #444; width: 40%; }
button { cursor: pointer; font-weight: bold; transition: 0.2s; }
.btn-green { background: #00ff88; color: #000; }
.btn-red { background: #ff4444; color: white; }
.btn-blue { background: #44aaff; color: white; }
.btn-green:hover { transform: scale(1.05); }
.red { color: #ff5555; text-shadow: 0 0 10px #ff000055; } 
.green { color: #00ff88; text-shadow: 0 0 10px #00ff8855; }
table { width: 100%; background: #1e1e1e; border-radius: 12px; margin-top: 15px; overflow: hidden; }
td { padding: 12px; border-bottom: 1px solid #333; }
h1 { background: linear-gradient(90deg, #00ff88, #44aaff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 28px; }
</style></head>
<body>
<h1>💎 ahmed yones Live Dashboard</h1>
<p>أول موقع ليك يا بطل!</p>

<div class="card">
<h2>الميزانية: {{budget}} جنيه</h2>
<h2>صرفت: {{total}} جنيه</h2>
<h2 class="{{'red' if left < 200 else 'green'}}">فاضل: {{left}} جنيه</h2>
<div style="background: #333; border-radius: 10px; height: 20px; overflow:hidden; margin-top:10px;">
<div style="width: {{percent}}%; background: {{'#ff4444' if left < 200 else '#00ff88'}}; height:100%; transition: 0.5s;"></div>
</div>
</div>

<div class="card">
<h3>⚙️ غير ميزانيتك</h3>
<form method="POST" action="/set_budget">
<input name="new_budget" type="number" placeholder="مثلا 1000" required>
<button class="btn-blue" type="submit">حدث الميزانية</button>
</form>
</div>

<div class="card">
<h3>➕ أضف مصروف جديد</h3>
<form method="POST" action="/add">
<input name="reason" placeholder="صرفت في ايه؟" required>
<input name="price" type="number" placeholder="كام؟" required>
<button class="btn-green" type="submit">أضف</button>
</form>

<table>
{% for line in lines %}
<tr><td>{{line}}</td></tr>
{% endfor %}
{% if not lines %}
<tr><td style="color:#888;">لسه مفيش مصاريف... ابدأ دلوقتي!</td></tr>
{% endif %}
</table>

<form method="POST" action="/clear" style="margin-top:15px;">
<button class="btn-red" type="submit" onclick="return confirm('متأكد تمسح كله؟')">🗑️ امسح كل المصاريف</button>
</form>
</div>

<p style="color:#666; margin-top:30px;">Made with ❤️ by Ahmed Yones - V5</p>
</body></html>
"""

@app.route("/", methods=["GET"])
def home():
    lines, total = get_expenses()
    budget = get_budget()
    left = budget - total
    percent = int((total / budget * 100) if budget > 0 else 0)
    if percent > 100: percent = 100
    return render_template_string(HTML_PAGE, lines=lines, total=total, left=left, budget=budget, percent=percent)

@app.route("/add", methods=["POST"])
def add():
    reason = request.form["reason"]
    price = request.form["price"]
    with open(EXPENSE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{reason} - {price} جنيه\n")
    return redirect("/")

@app.route("/set_budget", methods=["POST"])
def set_budget():
    new_budget = request.form["new_budget"]
    with open(BUDGET_FILE, "w") as f:
        f.write(new_budget)
    return redirect("/")

@app.route("/clear", methods=["POST"])
def clear():
    if os.path.exists(EXPENSE_FILE):
        os.remove(EXPENSE_FILE)
    return redirect("/")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)