import mechanicalsoup
import gspread
import concurrent
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor

# Function to process each li_element
def process_li_element(li_element):
    with mechanicalsoup.StatefulBrowser() as browser:
        a_tag = li_element.select_one("a")
        if a_tag:
            href = a_tag["href"]
            # print(href)
            sub_page = browser.open(href)
            ol = sub_page.soup.select_one("ol.breadcrumb")
            sheet_name = ol.select("li")[-1].text
            print(f"{sheet_name}")
            # Add a new sheet
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            detailDiv = sub_page.soup.select_one("ul.detailDiv")
            ul_elements = detailDiv.select("li > ul")

            for ul_element in ul_elements:
                li_items = ul_element.select("li")
                if len(li_items) >= 2:
                    key, value = li_items[0].text, li_items[1].text
                    print(f"{key} =======> {value}")
                    worksheet.append_row([key, value])

# Initialize browser and get page
browser = mechanicalsoup.StatefulBrowser()
url = "https://ctc-associates.com/dental-practices-for-sale"
page = browser.open(url)
li_elements = page.soup.select("li.directory_link")

# Set up Google Sheets credentials and client
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scopes)
client = gspread.authorize(creds)

# Open the spreadsheet and clear existing worksheets
spreadsheet = client.open('ctc spreadsheet')
worksheets = spreadsheet.worksheets()
reqs = [{"repeatCell": {"range": {"sheetId": s.id}, "fields": "*"}} if i == 0 else {"deleteSheet": {"sheetId": s.id}} for i, s in enumerate(worksheets)]
spreadsheet.batch_update({"requests": reqs})
print(f"all worksheets removed and first sheet cleared")

# Use ThreadPoolExecutor to process li_elements concurrently
with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks to the executor
    futures = [executor.submit(process_li_element, li) for li in li_elements]

    # Wait for all futures to complete
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()  # If needed, you can use the result of each future here
        except Exception as e:
            print(f"An error occurred: {e}")

print("All tasks completed.")