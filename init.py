from flask import Flask, request, render_template_string
import google.generativeai as genai

# Clé API Gemini
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
10. Tu conclueras par 3/4 hashtags en rapport

Objectif : générer du **temps de lecture élevé**, **des commentaires** et **des sauvegardes**.

Rédige un post complet, sans aucun titre, ni signature, ni lien. Commence directement par l’accroche.
"""

# 🖥 Interface HTML modifiée avec champ <textarea>
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
<h1>✨ Générateur de Post LinkedIn optimisé (2025)</h1>
<form method=post>
  Sujet du post :<br>
  <input type=text name=subject size=80 required value="{{ subject or '' }}"><br><br>

  Ton :<br>
  <select name="tone">
    <option value="professionnel" {% if tone == 'professionnel' %}selected{% endif %}>Professionnel</option>
    <option value="inspirant" {% if tone == 'inspirant' %}selected{% endif %}>Inspirant</option>
    <option value="personnel" {% if tone == 'personnel' %}selected{% endif %}>Personnel</option>
    <option value="conversationnel" {% if tone == 'conversationnel' %}selected{% endif %}>Conversationnel</option>
  </select><br><br>

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

    if request.method == "POST":
        # Si l'utilisateur modifie le texte à la main (sans regénération)
        if request.form.get("edited_post"):
            post = request.form.get("edited_post", "")
            subject = request.form.get("subject", "")
            tone = request.form.get("tone", "inspirant")
        else:
            subject = request.form.get("subject", "")
            tone = request.form.get("tone", "inspirant")
            try:
                prompt = generate_performance_prompt(subject, tone)
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(prompt)
                post = response.text.strip()
            except Exception as e:
                post = f"Erreur lors de la génération : {e}"

    return render_template_string(TEMPLATE, post=post, subject=subject, tone=tone)

if __name__ == "__main__":
    app.run(debug=True)
