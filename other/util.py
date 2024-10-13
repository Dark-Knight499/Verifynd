import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-pro")
def scrap(URL):
    try:
        url = URL  # Replace with your URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print("I am in url ")
        article = soup.find('article').get_text(strip=True)
        x = article.split(".")
        for k in x:
            k = k.strip()
        return article
    except:
        return "Unable to Load" ,False
    
def summarize(news:str):
    return model.generate_content(f"Precisly Summarize the context without folding of facts.Summarize it carefully{news}")

def analyze(news_summary:str):
    prompt = f"""
    You are a highly experienced fact-checker and news analyst with expertise in evaluating the authenticity, bias, and accuracy of news articles. Your task is to analyze the following news article and provide a detailed JSON report with scores and recommendations. Consider the following criteria:

- **Accuracy**: How factual and supported by evidence is the article? Check for misinformation or dubious claims.
- **Bias**: Identify any political, cultural, or ideological bias present in the article. Rate the bias on a scale from neutral to highly biased.
- **Source Credibility**: Evaluate the sources used in the article. Are they trustworthy and verifiable?
- **Tone**: Analyze the tone of the article (e.g., neutral, inflammatory, sensationalist).
- **Overall Reliability**: Provide a final score assessing the overall reliability of the article.

Return the analysis in JSON format with the following structure:

{
  "accuracy_score": <value between 1-10>,
  "bias_level": "<Neutral, Low Bias, Moderate Bias, High Bias>",
  "source_credibility": <value between 1-10>,
  "tone": "<Neutral, Inflammatory, Sensationalist>",
  "overall_reliability": <value between 1-10>,
  "recommendation": "<Short recommendation about the article's credibility>"
  "tags": <Tags Associated with it>
}
Analyze this news{news_summary}
RETURN ONLY JSON NO EXTRA THINGS FORMATS NO EXTRA WORDS GIVE THE OUTPUT JSON.
"""
    return model.generate_content(prompt)
