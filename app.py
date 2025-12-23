from flask import Flask, request, jsonify

app = Flask(__name__)

# ===================== DATA =====================
data = {
    "exam will be easy": "We lied.",
    "notes will be shared": "You’ll never see them.",
    "syllabus is small": "Surprise incoming.",
    "important questions only": "Everything is important.",
    "attendance is mandatory": "Marks depend on mood.",

    "we'll get back to you": "Rejected politely.",
    "fast paced environment": "Overworked.",
    "competitive salary": "Lower than market.",
    "learning opportunity": "More work, less pay.",
    "we are like a family": "No boundaries.",
    "deadline is flexible": "Due yesterday.",

    "i'm busy": "You are not priority.",
    "let's plan": "Never happening.",
    "will call you": "Won’t.",
    "on the way": "Just woke up.",

    "i need space": "I am distancing.",
    "let's just be friends": "End of story.",

    "trust the process": "No clear plan.",
    "it is what it is": "I gave up.",
    "no offense but": "Offense incoming."
}

suggestions = list(data.keys())

# ===================== HOME =====================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Nice Words</title>
<style>
*{box-sizing:border-box}

body{
    margin:0;
    height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#fff9d6;
    font-family:system-ui,sans-serif;
}

.card{
    background:#161616;
    width:360px;
    padding:24px;
    border-radius:20px;
    box-shadow:0 30px 60px rgba(0,0,0,.35);
    text-align:center;
}

h2{
    margin:0;
    color:#ffe600;
    font-size:22px;
}

.sub{
    font-size:13px;
    color:#bbb;
    margin-top:6px;
}

.input-wrap{
    margin-top:20px;
    position:relative;
}

input{
    width:100%;
    padding:14px;
    border-radius:14px;
    border:none;
    background:#0f0f0f;
    color:#fff;
    font-size:14px;
    outline:none;
    box-shadow:0 6px 0 #000;
}

input:focus{
    box-shadow:0 10px 0 #000;
}

#suggestions{
    position:absolute;
    top:58px;
    left:0;
    width:100%;
    background:#1e1e1e;
    border-radius:12px;
    overflow:hidden;
    z-index:100;
}

.suggestion{
    padding:8px 12px;
    font-size:13px;
    cursor:pointer;
    color:#ddd;
}

.suggestion:hover{
    background:#333;
}

button{
    margin-top:16px;
    padding:10px 20px;
    border-radius:999px;
    border:none;
    background:#ffe600;
    color:#000;
    font-weight:bold;
    cursor:pointer;
}

#out{
    margin-top:16px;
    color:#fff;
    font-weight:600;
}

.footer{
    font-size:11px;
    color:#666;
    margin-top:12px;
}
</style>
</head>

<body>
<div class="card">
    <h2>Nice Words</h2>
    <div class="sub">What They Say Vs What They Actually Mean</div>

    <div class="input-wrap">
        <input id="text" placeholder="type the lie here…" oninput="getSuggestions()">
        <div id="suggestions"></div>
    </div>

    <button onclick="go()">decode</button>
    <div id="out"></div>

    <div class="footer">Use at your own emotional risk.</div>
</div>

<script>
const text = document.getElementById("text");
const suggestions = document.getElementById("suggestions");
const out = document.getElementById("out");

function getSuggestions(){
    if(!text.value.trim()){
        suggestions.innerHTML="";
        return;
    }

    fetch("/suggest?q=" + text.value)
    .then(r => r.json())
    .then(d => {
        suggestions.innerHTML = d.map(
            s => `<div class="suggestion" onclick="selectSuggestion(this)">${s}</div>`
        ).join("");
    });
}

function selectSuggestion(el){
    text.value = el.innerText;
    suggestions.innerHTML = "";
    text.focus();
    text.setSelectionRange(text.value.length, text.value.length);
}

function go(){
    fetch("/translate",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({text:text.value})
    })
    .then(r => r.json())
    .then(d => out.innerText = d.result);
}

text.addEventListener("keydown", e=>{
    if(e.key === "Enter"){
        e.preventDefault();
        go();
    }
});
</script>
</body>
</html>
"""

# ===================== SUGGEST =====================
@app.route("/suggest")
def suggest():
    q = request.args.get("q","").lower()
    return jsonify([s for s in suggestions if q in s.lower()][:10])

# ===================== TRANSLATE =====================
@app.route("/translate", methods=["POST"])
def translate():
    t = request.json.get("text","").lower()
    for k,v in data.items():
        if all(w in t for w in k.split()):
            return jsonify({"result": v})
    return jsonify({"result":"Too vague. Even we don't know what they meant."})

# ===================== RUN =====================
if __name__ == "__main__":
    app.run(debug=True)
