from flask import Flask, request, render_template_string
import openai
import google.generativeai as genai
import os
import requests

genai.configure(api_key="AIzaSyB434P__wR_o_rr5Q3PjOULqyKhMANRtgk")
openai.api_key = "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"

app = Flask(__name__)
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)

# 🔧 Prompt optimisé selon format
def generate_extended_prompt(prompt, tone="conversationnel", format_type="texte"):
    base = (
        f"Tu es un expert en copywriting LinkedIn. Le sujet est : {prompt}. "
        f"Le ton est {tone}, humain, authentique, conversationnel.\n\n"
    )

    if format_type == "texte":
        format_prompt = (
            "Rédige un post LinkedIn optimisé pour l’algorithme 2025 :\n"
            "- Longueur entre 900 et 1200 caractères\n"
            "- Accroche forte dans les 2 premières lignes\n"
            "- Paragraphes courts + sauts de ligne\n"
            "- Contenu éducatif, inspirant ou professionnel\n"
            "- Pas de lien externe\n"
            "- Termine par une question engageante\n"
        )
    elif format_type == "texte+image":
        format_prompt = (
            "Rédige un post LinkedIn optimisé pour l’algorithme 2025, avec image :\n"
            "- Longueur entre 700 et 900 caractères\n"
            "- Accroche forte dans les 2 premières lignes\n"
            "- Paragraphes courts + sauts de ligne\n"
            "- Contenu storytelling, coulisses ou succès\n"
            "- Pas de lien externe\n"
            "- Termine par une question engageante\n"
            "- Ajoute une ligne à la fin du post exactement sous la forme : IMAGE_DESCRIPTION: Une photo verticale réaliste de [décris ici]."
        )
    else:
        format_prompt = "Format inconnu – rédige un post structuré et engageant."

    return base + format_prompt

# 🎨 Génération image via DALL·E
def generate_image_with_dalle(prompt_image):
    try:
        response = openai.Image.create(
            prompt=prompt_image,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        return None

# 💾 Téléchargement de l'image dans /static
def save_image_locally(image_url, filename="generated_image.jpg"):
    try:
        response = requests.get(image_url)
        path = os.path.join(STATIC_FOLDER, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        return f"/static/{filename}"
    except Exception as e:
        return None

# 🖥 Interface HTML
TEMPLATE = '''
<!doctype html>
<title>Générateur LinkedIn</title>
<h1>🚀 Génère ton post LinkedIn optimisé</h1>
<form method=post>
  Sujet du post :<br><input type=text name=prompt size=80 required><br><br>

  Ton :<br>
  <select name="tone">
    <option value="professionnel">Professionnel</option>
    <option value="inspirant">Inspirant</option>
    <option value="personnel">Personnel</option>
    <option value="conversationnel" selected>Conversationnel</option>
  </select><br><br>

  Format de publication :<br>
  <select name="format_type">
    <option value="texte">📄 Texte seul (optimisé)</option>
    <option value="texte+image">🖼️ Texte + Image (optimisé)</option>
  </select><br><br>

  <input type=submit value="Générer le post">
</form>

{% if post %}
<hr>
<h2>📝 Post généré :</h2>
<pre>{{ post }}</pre>
{% endif %}

{% if image_url %}
<hr>
<h2>🖼️ Image générée :</h2>
<img src="{{ image_url }}" width="300"><br>
<a href="{{ image_url }}" target="_blank">Voir en grand</a>
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    post = ""
    image_url = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        tone = request.form.get("tone")
        format_type = request.form.get("format_type")

        try:
            # Générer post Gemini
            full_prompt = generate_extended_prompt(prompt, tone, format_type)
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(full_prompt)
            post = response.text.strip()

            # Gérer image si besoin
            if format_type == "texte+image":
                lines = post.split("\n")
                image_description = ""
                for line in lines[::-1]:
                    if line.startswith("IMAGE_DESCRIPTION:"):
                        image_description = line.replace("IMAGE_DESCRIPTION:", "").strip()
                        break
                    
                if image_description:
                    print("🎨 Prompt image :", image_description)
                    dalle_url = generate_image_with_dalle(image_description)
                    if dalle_url:
                        image_url = save_image_locally(dalle_url)
                    else:
                        post += "\n\n⚠️ Erreur : DALL·E n’a pas pu générer d’image."
                else:
                    post += "\n\nℹ️ Aucune description d’image trouvée dans le texte."
            

        except Exception as e:
            post = f"Erreur : {e}"

    return render_template_string(TEMPLATE, post=post, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
