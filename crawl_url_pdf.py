import requests
from requests.exceptions import RequestException, ChunkedEncodingError
from bs4 import BeautifulSoup
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_pdf(url, session):
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        pdf_links = [a for a in soup.find_all("a", href=True) if a["href"].lower().endswith(".pdf")]

        if pdf_links:
            for pdf_link in pdf_links:
                pdf_url = pdf_link["href"]
                if not pdf_url.startswith("http"):
                    pdf_url = "https://congbobanan.toaan.gov.vn" + pdf_url
            
            pdf_response = session.get(pdf_url, verify=False)
            pdf_response.raise_for_status()
            
            filename = pdf_url.split("/")[-1]
            with open(f"./dataset/{filename}", "wb") as f:
                f.write(pdf_response.content)
            print(f"Downloaded: {filename}")
        else:
            print("No PDF link found on the page.")
    except RequestException as e:
        print(f"Error downloading PDF from {url}: {e}")
        

# session = requests.Session()

# with open("all_links.txt", "r", encoding="utf-8") as f:
#     all_links = [line.strip() for line in f.readlines() if line.strip()]
    
# for i, link in enumerate(all_links):
#         print(f"Processing {i+1}/{len(all_links)}: {link}")
#         download_pdf(link, session)
#     # time.sleep(1)  # Thêm độ trễ để tránh quá tải server