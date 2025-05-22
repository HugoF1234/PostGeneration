from flask import Flask, request, render_template_string
import google.generativeai as genai

# Clé API Gemini
genai.configure(api_key="AIzaSyB434P__wR_o_rr5Q3PjOULqyKhMANRtgk")

app = Flask(__name__)

# 📌 PROMPT ULTRA OPTIMISÉ avec interêts + secteur
def generate_performance_prompt(subject, tone, interets, secteur):
    return f"""
Tu es un expert de LinkedIn, spécialisé dans les posts viraux qui performent avec l’algorithme 2025.

Rédige un post LinkedIn optimisé sur : "{subject}"

Respecte strictement ces consignes :

1. Accroche percutante dans les **2 premières lignes** (positive, négative ou personnelle)
2. Rédige en **paragraphes courts**, avec **sauts de ligne** fréquents
3. Longueur : entre **900 et 1200 caractères** (pas plus)
4. Ton : {tone}, authentique, humain. 
   - Pour le ton professionnel, utilise un vocabulaire technique et adapté au domaine.
   - Pour le ton inspirant, vise à motiver et à inspirer ton audience.
   - Pour le ton personnel, base-toi sur les centres d’intérêt suivants : {interets}, et sur le secteur suivant : {secteur}
   - Pour le ton conversationnel, adopte un langage courant, accessible et amical.
5. **Aucune mention de lien externe**
6. Termine par une **question engageante** simple qui pousse à commenter
7. Le contenu doit être **éducatif**, **inspirant**, **personnel**, ou **utile**
8. Index de lisibilité entre 0 et 4 (accessible à tous)
9. Tu peux utiliser **puces ou émojis**, mais avec modération
10. Tu conclueras par 3/4 hashtags en rapport

Objectif : générer du **temps de lecture élevé**, **des commentaires** et **des sauvegardes**.

Rédige un post complet, sans aucun titre, ni signature, ni lien. Commence directement par l’accroche.
"""

# 🖥 Interface HTML mise à jour avec intérêt + secteur
TEMPLATE = '''
<!doctype html>
<html>
<head>
  <title>Post LinkedIn Optimisé</title>
  <style>
    textarea { width: 100%; height: 300px; font-size: 16px; line-height: 1.5; }
    input[type="submit"] { font-size: 18px; padding: 6px 12px; }
  </style>
</head>
<body>
<h1>Générateur de Post LinkedIn optimisé </h1>
<form method=post>
  De quoi voudriez-vous parler ?<br>
  <input type=text name=subject size=80 required value="{{ subject or '' }}"><br><br>

  Ton :<br>
  <select name="tone">
    <option value="professionnel" {% if tone == 'professionnel' %}selected{% endif %}>Professionnel</option>
    <option value="inspirant" {% if tone == 'inspirant' %}selected{% endif %}>Inspirant</option>
    <option value="personnel" {% if tone == 'personnel' %}selected{% endif %}>Personnel</option>
    <option value="conversationnel" {% if tone == 'conversationnel' %}selected{% endif %}>Conversationnel</option>
  </select><br><br>

  Secteur :<br>
  <select name="secteur">
    <option value="tech">Tech</option>
    <option value="santé">Santé</option>
    <option value="finance">Finance</option>
    <option value="éducation">Éducation</option>
    <option value="marketing">Marketing</option>
    <option value="autre">Autre</option>
  </select><br><br>

  Centres d’intérêt (ex : IA, entrepreneuriat, sport) :<br>
  <input type=text name=interets size=80 value="{{ interets or '' }}"><br><br>

  <input type=submit value="Générer le post">
</form>

{% if post %}
<hr>
<h2>💬 Post généré :</h2>
<form method="post">
  <textarea name="edited_post">{{ post }}</textarea><br><br>
  <input type="submit" value="Modifier manuellement uniquement">
</form>
{% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    post = ""
    subject = ""
    tone = "inspirant"
    interets = ""
    secteur = "tech"

    if request.method == "POST":
        if request.form.get("edited_post"):
            post = request.form.get("edited_post", "")
            subject = request.form.get("subject", "")
            tone = request.form.get("tone", "inspirant")
            interets = request.form.get("interets", "")
            secteur = request.form.get("secteur", "tech")
        else:
            subject = request.form.get("subject", "")
            tone = request.form.get("tone", "inspirant")
            interets = request.form.get("interets", "")
            secteur = request.form.get("secteur", "tech")
            try:
                prompt = generate_performance_prompt(subject, tone, interets, secteur)
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(prompt)
                post = response.text.strip()
            except Exception as e:
                post = f"Erreur lors de la génération : {e}"

    return render_template_string(TEMPLATE, post=post, subject=subject, tone=tone, interets=interets, secteur=secteur)

if __name__ == "__main__":
    app.run(debug=True)
