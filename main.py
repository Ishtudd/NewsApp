from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


app = FastAPI()

class Url(BaseModel):
    url: str


@app.post("/url/")
def scrape_url(url: Url):
    response = requests.get(url.url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        exit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all paragraphs from the webpage
    paragraphs = soup.find_all('p')

    # Extract text from each paragraph and join them
    text = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
    return text



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)