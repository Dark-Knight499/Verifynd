import streamlit as st
import json
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def score_color(value):
    if isinstance(value, (int, float)):
        score = int(value)
        if score <= 3:
            return "🔴"
        elif score <= 6:
            return "🟠"
        else:
            return "🟢"
    elif isinstance(value, str):
        lower_value = value.lower()
        if any(word in lower_value for word in ['low', 'neutral', 'mild']):
            return "🟢"
        elif any(word in lower_value for word in ['moderate', 'medium']):
            return "🟠"
        else:
            return "🔴"
    return "🔵"  # default color

def parse_analysis_output(output: str):
    try:
        data = json.loads(output.text)
        formatted_output = f"""
        ## 📊 Analysis Results

        ### Accuracy
        {score_color(data.get('accuracy_score', 'N/A'))} **Score:** {data.get('accuracy_score', 'N/A')}/10
        _{data.get('accuracy_description', 'No description provided.')}_

        ### Bias
        {score_color(data.get('bias_level', 'N/A'))} **Level:** {data.get('bias_level', 'N/A')}
        _{data.get('bias_description', 'No description provided.')}_

        ### Source Credibility
        {score_color(data.get('source_credibility', 'N/A'))} **Score:** {data.get('source_credibility', 'N/A')}/10
        _{data.get('source_description', 'No description provided.')}_

        ### Tone
        {score_color(data.get('tone', 'N/A'))} **Tone:** {data.get('tone', 'N/A')}
        _{data.get('tone_description', 'No description provided.')}_

        ### Overall Reliability
        {score_color(data.get('overall_reliability', 'N/A'))} **Score:** {data.get('overall_reliability', 'N/A')}/10
        _{data.get('reliability_description', 'No description provided.')}_

        ### 💡 Recommendation
        _{data.get('recommendation', 'No recommendation provided.')}_

        ### 🏷️ Tags
        {', '.join([f'`{tag}`' for tag in data.get('tags', ['N/A'])])}
        """
        return formatted_output
    except json.JSONDecodeError:
        return "Error: Unable to parse the output."
    except Exception as e:
        return f"Error: {str(e)}"

def get_news_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_content = " ".join([p.text for p in soup.find_all('p')])
        return news_content
    except Exception as e:
        return f"Error fetching news from the URL: {e}"

def summarize(news: str):
    response = model.generate_content(f"Precisely summarize the context without folding of facts. Summarize it carefully: {news}")
    return response.text

def analyze_news(news_summary: str,url:str):
    prompt = f"""
    You are a highly experienced fact-checker and news analyst with expertise in evaluating the authenticity, bias, and accuracy of news articles. Your task is to analyze the following news article and provide a detailed JSON report with scores, descriptions, and recommendations. Consider the following criteria:

- Accuracy: How factual and supported by evidence is the article? Check for misinformation or dubious claims.
- Bias: Identify any political, cultural, or ideological bias present in the article. Rate the bias on a scale from neutral to highly biased.
- Source Credibility: Evaluate the sources used in the article. Are they trustworthy and verifiable?
- Tone: Analyze the tone of the article (e.g., neutral, inflammatory, sensationalist).
- Overall Reliability: Provide a final score assessing the overall reliability of the article.

Return the analysis in JSON format with the following structure:

{{
  "accuracy_score": <value between 1-10>,
  "accuracy_description": "<Brief explanation of the accuracy score>",
  "bias_level": "<Neutral, Low Bias, Moderate Bias, High Bias>",
  "bias_description": "<Brief explanation of the bias assessment>",
  "source_credibility": <value between 1-10>,
  "source_description": "<Brief explanation of the source credibility>",
  "tone": "<Neutral, Inflammatory, Sensationalist>",
  "tone_description": "<Brief explanation of the tone assessment>",
  "overall_reliability": <value between 1-10>,
  "reliability_description": "<Brief explanation of the overall reliability>",
  "recommendation": "<Short recommendation about the article's credibility>",
  "tags": ["tag1", "tag2", "tag3"]
}}

Analyze this news: {news_summary}
source : {url}
RETURN ONLY JSON NO EXTRA THINGS FORMATS NO EXTRA WORDS GIVE THE OUTPUT JSON.
"""
    return model.generate_content(prompt)

st.title("Verifynd: Analyze News Authenticity")

tab1, tab2 = st.tabs(["Text Input", "URL Input"])

with tab1:
    st.header("Input News Text")
    news_text = st.text_area("Paste the news article text here:")
    if st.button("Analyze Text", key="text_analyze"):
        if news_text:
            analysis_result = analyze_news(news_text,"Through text")
            parsed_output = parse_analysis_output(analysis_result)
            st.markdown(parsed_output, unsafe_allow_html=True)
        else:
            st.error("Please input news text to analyze.")

with tab2:
    st.header("Input News URL")
    news_url = st.text_input("Enter the URL of the news article:")
    
    if st.button("Analyze URL", key="url_analyze"):
        if news_url:
            news_content = get_news_from_url(news_url)
            if "Error" in news_content:
                st.error(news_content)
            else:
                summarized_content = summarize(news_content)
                analysis_result = analyze_news(summarized_content,news_url)
                parsed_output = parse_analysis_output(analysis_result)
                st.markdown(parsed_output, unsafe_allow_html=True)
        else:
            st.error("Please input a valid URL.")
