# OrdskyGenerator
# 🔤 Ordsky-generator for nettsider

En interaktiv webapplikasjon som lar deg generere en ordsky basert på innholdet fra en hvilken som helst nettside – perfekt for innsikt, undervisning, eller ren nysgjerrighet!



## 🎯 Funksjonalitet

- 📥 Hent tekst fra en offentlig nettside
- 🧹 Fjern små og irrelevante ord (stoppord)
- 🧠 Egendefinerte ekskluderinger (f.eks. institusjonsnavn)
- 🎨 Velg mellom flere moderne fargetemaer
- 📊 Last ned Excel-fil med ordfrekvenser + metadata (URL, tidspunkt, ekskluderte ord)
- 🌐 Responsivt webgrensesnitt med Bootstrap

---

## 🧰 Teknologi

- [Python](https://www.python.org/) + [Flask](https://flask.palletsprojects.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – nettskraping
- [WordCloud](https://github.com/amueller/word_cloud) – generering av ordsky
- [Matplotlib](https://matplotlib.org/) – bildebehandling
- [pandas](https://pandas.pydata.org/) – Excel-håndtering
- [Bootstrap](https://getbootstrap.com/) – frontend-styling

---

## 🛠 Installasjon

```bash
# 1. Klon repoet
git clone https://github.com/dittbrukernavn/ordsky-generator.git
cd ordsky-generator

# 2. Installer avhengigheter
pip install -r requirements.txt

# 3. Start appen
python app.py
