import mechanicalsoup

browser = mechanicalsoup.Browser()
url = "https://ctc-associates.com/dental-practices-for-sale"
page = browser.get(url)
li_elements = page.soup.select("li.directory_link")

for li_element in li_elements:
    a_tag = li_element.select("a")[0]
    if a_tag:
        href = a_tag["href"]
        print(href)

# url = "http://olympus.realpython.org/login"
# login_page = browser.get(url)
# login_html = login_page.soup

# form = login_html.select("form")[0]
# form.select("input")[0]["value"] = "zeus"
# form.select("input")[1]["value"] = "ThunderDude"

# profile_page = browser.submit(form, login_page.url)
