from browser import Browser

from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, mode, url) -> None:
        if not "https://www.nonograms.org" in url:
            raise ValueError("URL is not from nonograms.org")
        if not mode in ["page", "list"]:
            raise ValueError("Mode is not valid")
        
        self.browser = Browser(False)
        self.browser.maximize()
        self.mode = mode
        self.url = url
        self.html = self.get_html()
        self.soup = self.get_soup()
        
        try:
            if self.soup.find("div", {"class": "content"}).find("h1").find("span").text == "Error 404":
                raise ValueError("URL is not valid")
        except AttributeError:
            pass
    
    def get_html(self):
        return self.browser.get_html(self.url)

    def get_soup(self):
        try:
            html = self.html
        except AttributeError:
            html = self.get_html()
        return BeautifulSoup(html, "html.parser")
    
    def get_content(self):
        wrapper = self.soup.find_all("table")[0]
        document = wrapper.find("td", {"class": "document"})
        content = document.find("div", {"class": "content"})
        return content

    def get_information_table(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        content = self.get_content()
        table = content.find_all("table")
        for t in table:
            if "Size" in t.text:
                table = t
                break
        info_table = table.find("tr")
        
        return info_table
    
    def get_size(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        info_table = self.get_information_table()
        tds = info_table.find_all("td")
        size = tds[0].text
        size = size.split(" ")[1]
        width, height = size.split("x")
        return {"width": int(width), "height": int(height)}
    
    def get_picture(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        info_table = self.get_information_table()
        tds = info_table.find_all("td")
        picture = tds[1].find("img")["title"].split("/")[0]
        return {"picture": picture}
    
    def get_difficulty(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        info_table = self.get_information_table()
        tds = info_table.find_all("td")
        difficulty = tds[2].find("img")["title"].split("/")[0]
        return {"difficulty": difficulty}
    
    def get_date(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        info_table = self.get_information_table()
        tds = info_table.find_all("td")
        date = tds[4].text
        return {"date": date}
    
    def get_author(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        info_table = self.get_information_table()
        tds = info_table.find_all("td")
        author = tds[5].find("a").text
        return {"author": author}
    
    def get_information(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        return self.get_size() | self.get_picture() | self.get_difficulty() | self.get_date() | self.get_author()
    
    def get_nonogram_table(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        content = self.get_content()
        table = content.find("table", {"class": "nonogram_table"}).find("tbody")
        return table
    
    def get_columns(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        tr = self.get_nonogram_table().find_all("tr")[0]
        tbody = tr.find("td", {"class": "nmtt"}).find("table").find("tbody")
        trs = tbody.find_all("tr")
        columns = []
        for height in range(1, len(trs)+1):
            height = -height
            nums = trs[height].find_all("td")
            for i in range(len(nums)):
                if not 'num_empty' in nums[i]["class"]:
                    try:
                        columns[i].insert(0, int(nums[i].find("div").text))
                    except IndexError:
                        columns.append([int(nums[i].find("div").text)])
        return columns
    
    def get_rows(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        tbody = self.get_nonogram_table().find("td", {"class": "nmtl"}).find("table").find("tbody")
        trs = tbody.find_all("tr")
        rows = []
        for row in range(len(trs)):
            rows.append([])
            nums = trs[row].find_all("td")
            for i in range(len(nums)):
                if not 'num_empty' in nums[i]["class"]:
                    rows[row].append(int(nums[i].find("div").text))
        return rows
                    
    def convert_to_non(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        info = self.get_information()
        rows = " ".join([",".join([str(i) for i in row]) for row in self.get_rows()])
        columns = " ".join([",".join([str(i) for i in column]) for column in self.get_columns()])

        string = ""
        string += f"author:{info['author']}\n"
        string += f"date:{info['date']}\n"
        string += f"picture:{info['picture']}\n"
        string += f"difficulty:{info['difficulty']}\n"
        string += f"width:{info['width']}\n"
        string += f"height:{info['height']}\n"
        string += f"rows:{rows}\n"
        string += f"columns:{columns}\n"
        string += "solution:"
        
        return string
    
    def path_from_url(self):
        if self.mode != "page":
            raise ValueError("Invalid mode")
        code = self.url.split("/")[-1]
        return f"src/nonograms/{code}.non"
    
    def export(self, path):
        non = self.convert_to_non()
        if self.mode != "page":
            raise ValueError("Invalid mode")
        with open(path, "w") as f:
            f.write(non)
    
    def get_codes_from_list(self):
        if self.mode != "list":
            raise ValueError("Invalid mode")
        content = self.get_content()
        nonogram_list = content.find("table", {"class": "nonogram_list"}).find("tbody")
        trs = nonogram_list.find_all("tr")
        codes = []
        for tr in trs:
            if tr.find("td", {"class": "nonogram_list_separator"}) is None:
                td = tr.find("td", {"class": "nonogram_img"})
                if td is not None:
                    link = td.find("a")["href"]
                    code = link.split("/")[-1]
                    codes.append(code)
        return codes