const input = document.getElementById("input");
const result = document.getElementById("result");
const suggestionsBox = document.getElementById("suggestions");
const decodeBtn = document.getElementById("decodeBtn");

const data = {
  "we'll get back to you": "Rejected politely.",
  "we are like a family": "No boundaries.",
  "exam will be easy": "We lied.",
  "i am busy": "You are not a priority.",
  "let's catch up soon": "Never happening.",
  "interesting idea": "No.",
  "work life balance": "Occasional Sundays off.",
  "deadline is flexible": "Due yesterday.",
  "not ready for a relationship": "Not with you."
};

const phrases = Object.keys(data);

// suggestions while typing
input.addEventListener("input", () => {
  const value = input.value.toLowerCase();
  suggestionsBox.innerHTML = "";

  if (!value) return;

  phrases.forEach(p => {
    if (p.includes(value)) {
      const div = document.createElement("div");
      div.className = "suggestion";
      div.innerText = p;
      div.onclick = () => {
        input.value = p;
        suggestionsBox.innerHTML = "";
      };
      suggestionsBox.appendChild(div);
    }
  });
});

// decode
function decode() {
  const text = input.value.toLowerCase();
  for (let key in data) {
    if (text.includes(key)) {
      result.innerText = data[key];
      return;
    }
  }
  result.innerText = "Too vague. Even we don’t know what they meant.";
}

decodeBtn.onclick = decode;

// Enter key support
input.addEventListener("keydown", e => {
  if (e.key === "Enter") decode();
});
