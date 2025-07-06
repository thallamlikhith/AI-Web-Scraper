# selenium gives us control our website browser like click butons , select ect..
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import streamlit as st

AUTH = 'brd-customer-hl_f85086ce-zone-smartscarper:lfe42y3ztalv'

SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

# Function it helps to gram the  information from the website
def scrape_website(website):
    print("Lanching chrome browser. . .")
    
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
        
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,"html.parser")
    body_content = soup.body
    if body_content :
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,"html.parser")
    
    for script_or_Style in soup("script","style"):
        script_or_Style.extract()
        
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
        ) # It removes the backshlash r unnessary n characters
    

    return cleaned_content 

def split_dom_content(dom_content,max_length =6000 ):
    return[
        dom_content[i: i+max_length] for i in range(0,len(dom_content),max_length)
    ]# it will convert into batchs of 6000 chars 
    
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")
    
    if st.button("Prase Content"):
        if parse_description:
                st.write("Prasing the content")
                dom_chunks = split_dom_content(st.session_state.dom_content) # We need to pass this to LLM
            
            