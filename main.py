from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    search_results = google_search(keyword)
    filename = save_results(search_results, keyword)
    return send_file(filename, as_attachment=True)


def google_search(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(f'https://www.google.com/search?q={query}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all(class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else 'No title'
        link = g.find('a')['href'] if g.find('a') else 'No link'
        snippet = g.find(class_='IsZvec').text if g.find(class_='IsZvec') else 'No snippet'
        results.append({'title': title, 'link': link, 'snippet': snippet})
    return results


def save_results(results, keyword):
    df = pd.DataFrame(results)
    filename = f'results_{keyword}.csv'
    df.to_csv(filename, index=False)
    return filename


if __name__ == '__main__':
    app.run(debug=True)
