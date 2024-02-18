from flask import Flask, request, render_template
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

def calculate_perplexity(text):
    """Calculate the perplexity of a given text using GPT-2."""
    tokenize_input = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad(): 
        outputs = model(tokenize_input, labels=tokenize_input)
    loss = outputs[0]
    perplexity = torch.exp(loss).item()
    return perplexity

def analyze_text(text):
    """Analyze the text to separate AI-generated and human-written sentences."""
    sentences = [s.strip() for s in text.split(".") if s.strip()] 
    ai_sentences, human_sentences = [], []

    for i, sentence in enumerate(sentences):
        perplexity = calculate_perplexity(sentence)
        if perplexity < 20: 
            ai_sentences.append(f"<span class='highlight'>{sentence}.</span>")
            human_sentences.append(f"<span class='highlight'>{sentence}.</span>")
        else:
            human_sentences.append(f"{sentence}.")
            

    return ai_sentences, human_sentences

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle the index route."""
    if request.method == "POST":
        text = ""
        if "file" in request.files and request.files["file"]:
            text = request.files["file"].read().decode("utf-8")
        elif "text" in request.form:
            text = request.form["text"]

        if text:
            ai_sentences, human_sentences = analyze_text(text)
            total_sentences = len(ai_sentences) + len(human_sentences)
            ai_percentage = (
                (len(ai_sentences) / total_sentences) * 100
                if total_sentences > 0
                else 0
            )
            human_percentage = (
                (len(human_sentences) / total_sentences) * 100
                if total_sentences > 0
                else 0
            )

            highlighted_text = human_sentences
            return render_template(
                "index.html",
                ai_percentage=ai_percentage,
                human_percentage=human_percentage,
                highlighted_text=highlighted_text,
                original_text=None,
            )

    return render_template(
        "index.html", ai_percentage=None, human_percentage=None, highlighted_text=None
    )

if __name__ == "__main__":
       app.run(debug=True, threaded=True)
