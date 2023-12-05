import mechanicalsoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

browser = mechanicalsoup.Browser()
url = "https://ctc-associates.com/dental-practices-for-sale"
page = browser.get(url)
li_elements = page.soup.select("li.directory_link")

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scopes)
client = gspread.authorize(creds)

spreadsheet = client.open('ctc spreadsheet')

worksheets = spreadsheet.worksheets()
reqs = [{"repeatCell": {"range": {"sheetId": s.id}, "fields": "*"}} if i == 0 else {"deleteSheet": {"sheetId": s.id}} for i, s in enumerate(worksheets)]
spreadsheet.batch_update({"requests": reqs})
print(f"all worksheets removed and first sheet cleared")

for li_element in li_elements:
    a_tag = li_element.select("a")[0]
    if a_tag:
        href = a_tag["href"]
        # print(href)
        sub_page = browser.get(href)
        ol = sub_page.soup.select("ol.breadcrumb")[0]
        sheet_name = ol.select("li")[-1].text
        print(f"{sheet_name}")
        # Add a new sheet
        worksheet = spreadsheet.add_worksheet(sheet_name, rows=100, cols=20)
        detailDiv = sub_page.soup.select("ul.detailDiv")[0]
        ul_elements = detailDiv.select("li")[0].select("ul")

        for ul_element in ul_elements:
            print(f"{ul_element.select("li")[0].text} =======> {ul_element.select("li")[1].text}")
            worksheet.append_row([ul_element.select("li")[0].text, ul_element.select("li")[1].text])


# url = "http://olympus.realpython.org/login"
# login_page = browser.get(url)
# login_html = login_page.soup

# form = login_html.select("form")[0]
# form.select("input")[0]["value"] = "zeus"
# form.select("input")[1]["value"] = "ThunderDude"

# profile_page = browser.submit(form, login_page.url)
