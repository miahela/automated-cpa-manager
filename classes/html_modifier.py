from bs4 import BeautifulSoup


class HTMLModifier:
    def __init__(self):
        self.soup = None

    def load_html(self, filepath):
        with open(filepath, "r") as f:
            content = f.read()
            self.soup = BeautifulSoup(content, "html.parser")

    def change_name(self, new_name):
        if self.soup is None:
            self.load_html()
        heading = self.soup.find("h1", {"class": "heading"})
        if heading:
            heading.string = new_name
        return str(self.soup)

    def save_html(self, filepath):
        with open(filepath, "w") as f:
            f.write(str(self.soup))
