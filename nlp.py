import os
import spacy
spacy.cli.download("en_core_web_sm")
from flask import Flask, render_template, request

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()

def get_jurisdiction(contract_text):
    doc = nlp(contract_text)
    countries = []
    for ent in doc.ents:
        if ent.label_ == "GPE":
            countries.append(ent.text)
    if countries:
        return countries[0]
    else:
        return "Could not determine jurisdiction"

@app.route("/")
def index():
    return render_template("contract_form.html")

@app.route('/jurisdiction', methods=['POST'])
def contract_jurisdiction():
    contract_text = request.form['contract_text']
    jurisdiction = get_jurisdiction(contract_text)
    return jurisdiction

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
