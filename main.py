import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import urllib3
import time
import os
from crawl_url_pdf import download_pdf
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://congbobanan.toaan.gov.vn/0tat1cvn/ban-an-quyet-dinh"

def get_hidden_fields(response):
    try:
        soup = BeautifulSoup(response, "html.parser")
        
        hidden = {}
        
        for input_tag in soup.find_all("input", type="hidden"):
            if input_tag.get("name") and input_tag.get("value"):
                hidden[input_tag["name"]] = input_tag["value"]
        
        return hidden
    except RequestException as e:
        print(f"Error fetching hidden fields: {e}")
        return {}
    

session = requests.Session()
response = session.get(BASE_URL, verify=False)
response.raise_for_status()
hidden_fields = get_hidden_fields(response.text)

all_links = []
pair_list = []
checkpoint_dict = {}
BATCH_SIZE = 1
# for i in range(1, 10):
#     start = (i - 1) * BATCH_SIZE + 1
#     end = i * BATCH_SIZE
#     pair_list.append((start, end))

#     checkpoint_dict[i] = 0
# pair_list[-1] = (9001, 9136) 

# import json
# if os.path.exists("checkpoint.json"):
#     with open("checkpoint.json", "r") as f:
#         checkpoint_dict = json.load(f)
#         print("Loaded checkpoint:", checkpoint_dict)
# else:
#     with open("checkpoint.json", "w") as f:
#         json.dump(checkpoint_dict, f)

# for i in range(1, 10):
#     if checkpoint_dict[str(i)] != 0:
#         print(f"Batch {i} already completed up to page {checkpoint_dict[str(i)]}. Skipping.")
#     else:
#         print(f"Batch {i} not started yet.")
        
# input_str = input(f"Chọn số tiếp tục batch: " )
# input_str = int(input_str)
data = []


for page in range(1, 150):
    if page == 1:
        # Lần đầu: bấm nút "Tìm kiếm"
        payload = {
            **hidden_fields,
            "ctl00$Content_home_Public$ctl00$txtKeyword": "Nhập tên vụ/việc hoặc số bản án, quyết định", 
            "ctl00$Content_home_Public$ctl00$Drop_Levels": "T",
            "ctl00$Content_home_Public$ctl00$Ra_Drop_Courts": "787",
            "ctl00$Content_home_Public$ctl00$Rad_DATE_FROM": "01/01/2024",
            "ctl00$Content_home_Public$ctl00$cmd_search_banner": "Tìm kiếm"
        }
    else:
        payload = {
            **hidden_fields,
            "ctl00$Content_home_Public$ctl00$txtKeyword": "Nhập tên vụ/việc hoặc số bản án, quyết định",
            "ctl00$Content_home_Public$ctl00$Drop_Levels": "T",
            "ctl00$Content_home_Public$ctl00$Ra_Drop_Courts": "787",
            "ctl00$Content_home_Public$ctl00$Rad_DATE_FROM": "01/01/2024",
            "ctl00$Content_home_Public$ctl00$DropPages": str(page),
            "__EVENTTARGET": "ctl00$Content_home_Public$ctl00$DropPages",
            "__EVENTARGUMENT": ""
        }


    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = session.post(BASE_URL, data=payload, headers=headers, verify=False)
        response.raise_for_status()
        
        print(f"Page {page} fetched successfully.")
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        links = [a["href"] for a in soup.find_all("a", href=True)]
        
        cases = soup.find_all("div", class_="list-group-item")
        for case in cases:
            # Link chi tiết
            link_tag = case.find("a", class_="echo_id_pub")
            full_link = "https://congbobanan.toaan.gov.vn" + link_tag["href"] if link_tag else None

            # Tiêu đề
            title = case.find("h4", class_="list-group-item-heading")
            title = title.get_text(strip=True) if title else None

            # Nội dung tóm tắt
            first_p = case.find("p")
            description = first_p.get_text(strip=True) if first_p else None

            # Cấp xét xử
            cap_tag = case.find("label", string="Cấp xét xử: ")
            cap = cap_tag.find_next("span").get_text(strip=True) if cap_tag else None

            # Áp dụng án lệ
            anle_tag = case.find("label", string="Áp dụng án lệ: ")
            an_le = anle_tag.find_next("span").get_text(strip=True) if anle_tag else None

            # Loại án / Loại vụ việc
            loai = None
            loai_an_tag = case.find("label", string="Loại án:")
            loai_vu_tag = case.find("label", string="Loại vụ/việc:")
            if loai_an_tag:
                loai = loai_an_tag.find_next("span").get_text(strip=True)
            elif loai_vu_tag:
                loai = loai_vu_tag.find_next("span").get_text(strip=True)

            # Đính chính
            dinhchinh_tag = case.find("label", string="Đính chính: ")
            dinh_chinh = dinhchinh_tag.find_next("span").get_text(strip=True) if dinhchinh_tag else None

            # Thông tin chi tiết
            info_tag = case.find("p", class_="Description_pub")
            info = info_tag.get_text(strip=True) if info_tag else None
            
            response_link = session.get(full_link, verify=False)
            response_link.raise_for_status()
            soup_link = BeautifulSoup(response_link.text, "html.parser")
            pdf_links = [a for a in soup_link.find_all("a", href=True) if a["href"].lower().endswith(".pdf")]
            # print(pdf_links)
            final_link = pdf_links[0]["href"] if pdf_links else None
            if final_link and not final_link.startswith("http"):
                final_link = "https://congbobanan.toaan.gov.vn" + final_link
            # print(final_link)
            data.append({
                "title": title,
                "link": full_link,
                "description": description,
                "cap_xet_xu": cap,
                "ap_dung_an_le": an_le,
                "loai": loai,
                "dinh_chinh": dinh_chinh,
                "thong_tin": info,
                "pdf_link": final_link
            })
        
        # print(links[0])
        # for link in links: 
        #     text_split = link.split("/")
        #     if len(text_split) > 2 and text_split[2] == "chi-tiet-ban-an":
        #         full_link = "https://congbobanan.toaan.gov.vn" + link
        #         all_links.append(full_link)
        
        hidden_fields = get_hidden_fields(response.text)
        # time.sleep(1)  
        
    except RequestException as e:
        print(f"Error on page {page}: {e}")
        break

df = pd.DataFrame(data)

# Xuất ra CSV
df.to_csv("final_ban_an_full.csv", index=False, encoding="utf-8-sig")
print("Đã lưu vào final_ban_an_full.csv")


# set_all_links = set(all_links)
# list_all_links = list(set_all_links)
# print(f"Total unique links collected: {len(list_all_links)}")

# if not os.path.exists("./dataset"):
#     os.makedirs("./dataset")

# for i, link in enumerate(list_all_links):
#     print(f"{i+1}: {link}")
#     download_pdf(link, session)
    
# checkpoint_dict[str(input_str)] = 1
# with open("checkpoint.json", "w") as f:
#     json.dump(checkpoint_dict, f)