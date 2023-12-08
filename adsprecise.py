import mechanicalsoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scopes)
client = gspread.authorize(creds)

spreadsheet = client.open('adsprecise spreadsheet')

worksheets = spreadsheet.worksheets()
reqs = [{"repeatCell": {"range": {"sheetId": s.id}, "fields": "*"}} if i == 0 else {"deleteSheet": {"sheetId": s.id}} for i, s in enumerate(worksheets)]
spreadsheet.batch_update({"requests": reqs})

# worksheet = spreadsheet.get_worksheet(0)
# worksheet.update_title('colorado')

# # Reset the worksheet to its original state
# worksheet.clear()

# # Unmerge all cells in column A
# worksheet.unmerge_cells(1, 1, worksheet.row_count, 1)

current_row = 1
index = 0

colors = [(1, 0.8, 0.7), (0.2, 1, 0.9), (0.3, 0.8, 1)]

browser = mechanicalsoup.Browser()
baseUrl = "https://adsprecise.com/listings/"
page = browser.get(baseUrl)

nav_element = page.soup.select(".fusion-tabs-1 > .nav")[0]

tab_links = nav_element.select("a.tab-link")

for tab_link in tab_links:
    print(f"{tab_link["href"]}  =============> {tab_link.text}")
    page = browser.get(f"{baseUrl}{tab_link["href"]}")

    worksheet = spreadsheet.add_worksheet(tab_link.text, rows="1000", cols="26")

    li_elements = page.soup.select(".tab-content .tab-pane.active .es-listing > .properties")

    for li_element in li_elements:
        a_tag = li_element.select(".es-read-wrap a")[0]
        if a_tag:
            href = a_tag["href"]
            print(href)
            sub_page = browser.get(href)
            h1_element = sub_page.soup.select("h1.entry-title")[0]
            ul_element = sub_page.soup.select(".es-property-fields ul")[0]
            sub_li_elements = ul_element.select("li")

            data_to_write = []

            for sub_li_element in sub_li_elements:
                strong_element = sub_li_element.select("strong")[0]
                print(f"{strong_element.contents[0]} ==========> {sub_li_element.contents[1]}")
                data_to_write.append([strong_element.contents[0], sub_li_element.contents[1]])

            description_element = sub_page.soup.select("#es-description p")[0]
            print(f"description ===========> {description_element.text}")
            data_to_write.append(["Description", description_element.text])

            end_row = current_row + len(data_to_write) - 1
            worksheet.update(f'B{current_row}:C{end_row}', data_to_write)
            # Merge cells in column A for current property
            worksheet.merge_cells(current_row, 1, end_row, 1)
            # Set the property title in the merged cells
            worksheet.update_acell(f'A{current_row}', h1_element.text)

            # Apply vertical alignment to the merged cells
            worksheet.format(f'A{current_row}:A{end_row}', {
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
                "textFormat": {
                    "bold": True
                }
            })

            # Apply background color to the range of the current li_element
            color = colors[index % len(colors)]  # Alternate between colors defined
            index = index + 1
            worksheet.format(f'A{current_row}:Z{end_row}', {
                "backgroundColor": {
                    "red": color[0],
                    "green": color[1],
                    "blue": color[2],
                    "alpha": 0.2
                }
            })

            # Update current_row for the next property
            current_row = end_row + 1

    while True:
        pagination_lies = page.soup.select("nav.pagination ul.page-numbers li")
        if len(pagination_lies) == 0:
            break
        next_a_elements = pagination_lies[-1].select("a")
        if len(next_a_elements) == 0:
            break
        
        time.sleep(30)
        url = next_a_elements[0]["href"]
        page = browser.get(url)
        li_elements = page.soup.select(".tab-content .tab-pane.active .es-listing .es_category-colorado")

        print("length:",  len(li_elements))

        for li_element in li_elements:
            a_tag = li_element.select(".es-read-wrap a")[0]
            if a_tag:
                href = a_tag["href"]
                print(href)
                sub_page = browser.get(href)
                h1_element = sub_page.soup.select("h1.entry-title")[0]
                ul_element = sub_page.soup.select(".es-property-fields ul")[0]
                sub_li_elements = ul_element.select("li")

                data_to_write = []

                for sub_li_element in sub_li_elements:
                    strong_element = sub_li_element.select("strong")[0]
                    print(f"{strong_element.contents[0]} ==========> {sub_li_element.contents[1]}")
                    data_to_write.append([strong_element.contents[0], sub_li_element.contents[1]])

                description_element = sub_page.soup.select("#es-description p")[0]
                print(f"description ===========> {description_element.text}")
                data_to_write.append(["Description", description_element.text])

                end_row = current_row + len(data_to_write) - 1
                worksheet.update(f'B{current_row}:C{end_row}', data_to_write)
                # Merge cells in column A for current property
                worksheet.merge_cells(current_row, 1, end_row, 1)
                # Set the property title in the merged cells
                worksheet.update_acell(f'A{current_row}', h1_element.text)

                # Apply vertical alignment to the merged cells
                worksheet.format(f'A{current_row}:A{end_row}', {
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE",
                    "textFormat": {
                        "bold": True
                    }
                })

                # Apply background color to the range of the current li_element
                color = colors[index % len(colors)]  # Alternate between colors defined
                index = index + 1
                worksheet.format(f'A{current_row}:Z{end_row}', {
                    "backgroundColor": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2],
                        "alpha": 0.2
                    }
                })

                # Update current_row for the next property
                current_row = end_row + 1


print("length:",  len(li_elements))


print("Data entry complete.")