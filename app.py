import os
import re
import pandas as pd
import requests
from flask import Flask, render_template, request, send_from_directory
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import nltk
from nltk.corpus import stopwords

# Last ned stopwords første gang
nltk.download('stopwords')
BASE_STOPWORDS = set(stopwords.words('norwegian') + stopwords.words('english'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['WORDCLOUD_FOLDER'] = 'static/wordclouds'

# Sørg for at mappene finnes
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['WORDCLOUD_FOLDER'], exist_ok=True)


def fetch_webpage_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    return soup.get_text(separator=' ', strip=True)


def clean_and_tokenize(text, extra_stopwords=None):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    stop_words = BASE_STOPWORDS.copy()
    custom_stops = set()

    if extra_stopwords:
        extra_stopwords_cleaned = {word.lower().strip() for word in extra_stopwords}
        stop_words.update(extra_stopwords_cleaned)
        custom_stops = extra_stopwords_cleaned

    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    removed_custom_words = sorted(custom_stops.intersection(set(words)))
    return filtered_words, removed_custom_words


def generate_wordcloud(word_list, output_path, colormap='viridis'):
    unique_string = " ".join(word_list)
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color='white',
        colormap=colormap
    ).generate(unique_string)

    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


def export_to_excel(words, excluded, url_used, output_path):
    word_freq = Counter(words)
    df_words = pd.DataFrame(word_freq.items(), columns=["Ord", "Frekvens"]).sort_values(by="Frekvens", ascending=False)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_meta = pd.DataFrame({
        "Ekskluderte ord": excluded + [""] * (max(1, len(df_words)) - len(excluded)),
        "Dato og tid": [timestamp] + [""] * (max(1, len(df_words)) - 1),
        "URL": [url_used] + [""] * (max(1, len(df_words)) - 1)
    })

    with pd.ExcelWriter(output_path) as writer:
        df_words.to_excel(writer, index=False, sheet_name="Ordfrekvens")
        df_meta.to_excel(writer, index=False, sheet_name="Metadata")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        raw_excludes = request.form.get("exclude_words", "")
        custom_excludes = [word.strip() for word in raw_excludes.split(",")] if raw_excludes else []

        # Hent valgt fargeskjema
        color_scheme = request.form.get("color_scheme", "viridis")
        print(f"[DEBUG] Valgt fargeskjema: {color_scheme}")  # Debug-utskrift

        try:
            text = fetch_webpage_text(url)
            tokens, removed_custom = clean_and_tokenize(text, custom_excludes)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            image_filename = f"wordcloud_{timestamp}.png"
            image_path = os.path.join(app.config['WORDCLOUD_FOLDER'], image_filename)

            generate_wordcloud(tokens, image_path, colormap=color_scheme)

            excel_filename = f"ordfrekvens_{timestamp}.xlsx"
            excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
            export_to_excel(tokens, removed_custom, url, excel_path)

            return render_template("result.html",
                                   image_filename=image_filename,
                                   excel_filename=excel_filename)

        except Exception as e:
            return f"Feil under prosessering: {str(e)}"

    return render_template("index.html")


@app.route("/download/<filename>")
def download_excel(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
