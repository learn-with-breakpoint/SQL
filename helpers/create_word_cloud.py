import requests
from bs4 import BeautifulSoup
import json
import re
from collections import Counter
from wordcloud import WordCloud
from tqdm import tqdm


# Step 1: Scrape the Links
base_url = "https://www.sqlitetutorial.net"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all links
all_links = soup.find_all("a", href=True)
print(f"len of all links {len(all_links)}")
internal_links = []

# Filter out external links
for link in all_links:
    href = link['href']
    if href.startswith('https://www.sqlitetutorial.net'):
        internal_links.append(href)

print(f"internal links {len(internal_links)}")


# Step 2: Extract Code Text
data = []
excluded_chars = ['\n', '\t', '\r']
count = 0
for url in tqdm(internal_links, desc="processing links",
                total=len(internal_links), unit="links"):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    code_tags = soup.find_all("span", recursive=True, class_="hljs-keyword",)
    code_texts = []

    for code in code_tags:
        # Get text and remove unwanted characters
        text = code.get_text()
        for ch in excluded_chars:
            text = text.replace(ch, '')

        code_texts.append(text)

    data.append({"url": url, "code": code_texts})


# Write to JSON
with open('code_data.json', 'w') as f:
    json.dump(data, f, indent=4)

# Step 3: Process JSON Data
with open('code_data.json', 'r') as f:
    data = json.load(f)

word_counts = Counter()

for item in data:
    for code in item["code"]:
        words = re.findall(r'\b\w+\b', code.lower())  # split into words
        word_counts.update(words)

# Create Word Map
wordcloud = WordCloud(
    width=800, height=400,
    background_color='white').generate_from_frequencies(word_counts)

# Save Word Map to file
wordcloud.to_file("wordcloud.png")
