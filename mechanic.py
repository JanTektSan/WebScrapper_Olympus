import mechanicalsoup

browser = mechanicalsoup.Browser()
url = "https://ctc-associates.com/dental-practices-for-sale"
page = browser.get(url)
li_elements = page.soup.select("li.directory_link")

for li_element in li_elements:
    a_tag = li_element.select("a")[0]
    if a_tag:
        href = a_tag["href"]
        # print(href)
        sub_page = browser.get(href)
        ol = sub_page.soup.select("ol.breadcrumb")[0]
        sheet_name = ol.select("li")[-1].text
        print(f"{sheet_name}")

        detailDiv = sub_page.soup.select("ul.detailDiv")[0]
        
        ul_elements = detailDiv.select("li")[0].select("ul")

        for ul_element in ul_elements:
            print(f"{ul_element.select("li")[0].text} =======> {ul_element.select("li")[1].text}")


# url = "http://olympus.realpython.org/login"
# login_page = browser.get(url)
# login_html = login_page.soup

# form = login_html.select("form")[0]
# form.select("input")[0]["value"] = "zeus"
# form.select("input")[1]["value"] = "ThunderDude"

# profile_page = browser.submit(form, login_page.url)
