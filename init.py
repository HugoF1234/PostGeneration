from flask import Flask, request, render_template_string
import google.generativeai as genai
import os
import requests

genai.configure(api_key="AIzaSyB434P__wR_o_rr5Q3PjOULqyKhMANRtgk")

app = Flask(__name__)

# 📌 PROMPT ULTRA OPTIMISÉ
def generate_performance_prompt(subject, tone):
    return f"""
Tu es un expert de LinkedIn, spécialisé dans les posts viraux qui performent avec l’algorithme 2025.

Rédige un post LinkedIn optimisé sur : "{subject}"

Respecte strictement ces consignes :

1. Accroche percutante dans les **2 premières lignes** (positive, négative ou personnelle)
2. Rédige en **paragraphes courts**, avec **sauts de ligne** fréquents
3. Longueur : entre **900 et 1200 caractères** (pas plus)
4. Ton : {tone}, authentique, conversationnel, humain
5. **Aucune mention de lien externe**
6. Termine par une **question engageante** simple qui pousse à commenter
7. Le contenu doit être **éducatif**, **inspirant**, **personnel**, ou **utile**
8. Index de lisibilité entre 0 et 4 (accessible à tous)
9. Tu peux utiliser **puces ou émojis**, mais avec modération

Objectif : générer du **temps de lecture élevé**, **des commentaires** et **des sauvegardes**.

Rédige un post complet, sans aucun titre, ni signature, ni lien. Commence directement par l’accroche.
"""

# 🖥 Interface HTML
TEMPLATE = '''
<!doctype html>
<title>Générateur de Post LinkedIn Parfait</title>
<h1>✨ Générateur de Post LinkedIn optimisé (2025)</h1>
<form method=post>
  Sujet du post :<br><input type=text name=subject size=80 required><br><br>
  Ton :<br>
  <select name="tone">
    <option value="professionnel">Professionnel</option>
    <option value="inspirant" selected>Inspirant</option>
    <option value="personnel">Personnel</option>
    <option value="conversationnel">Conversationnel</option>
  </select><br><br>
  <input type=submit value="Générer le post">
</form>

{% if post %}
<hr>
<h2>💬 Post généré :</h2>
<pre style="white-space: pre-wrap;">{{ post }}</pre>
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    post = ""

    if request.method == "POST":
        subject = request.form.get("subject", "")
        tone = request.form.get("tone", "inspirant")

        try:
            prompt = generate_performance_prompt(subject, tone)
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            post = response.text.strip()
        except Exception as e:
            post = f"Erreur lors de la génération : {e}"

    return render_template_string(TEMPLATE, post=post)

if __name__ == "__main__":
    app.run(debug=True)

