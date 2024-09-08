# 출처 : https://velog.io/@a101201031/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-%EB%AC%B8%EC%A0%9C-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%B4%EC%84%9C-%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4%EC%9C%BC%EB%A1%9C-%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B01

import os
import sys
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter as MarkdownifyConverter


class MarkdownConverter:
    _module_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, url, parser):
        self.request_html(url)
        self.convert_html_bs4(parser)
        self.parse()

    def request_html(self, url):
        res = requests.get(url)
        self.html = res.text

    def convert_html_bs4(self, parser):
        self.soup = BeautifulSoup(self.html, "lxml")
        print(self.soup)

    def parse(self):
        category, title = self.find_category_title()
        categroy_path = os.path.join(MarkdownConverter._module_path, category)
        title_path = os.path.join(categroy_path, title)

        self.make_dir(categroy_path)
        self.make_dir(title_path)
        self.write_markdown(os.path.join(title_path, "readme.md"))

    def find_category_title(self):
        category_title_soup = self.soup.find("ol", "breadcrumb")
        _, category_soup, tilte_soup = category_title_soup.find_all("li")
        category = category_soup.get_text()
        title = tilte_soup.get_text()
        return category, title

    def make_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def md(self, soup, **options):
        return MarkdownifyConverter(**options).convert_soup(soup)
    
    def write_markdown(self, file_path):
        with open(file_path, "w", encoding='utf-8') as f:
            category, title = self.find_category_title()
            hyperlink = f"{url}"  # 해당 링크로 수정
            f.write(f"# [{title}]({hyperlink})\n\n")  # 제목과 하이퍼링크 추가
            description = self.soup.find("div", "guide-section-description")
            f.write(self.md(description))



def md(soup, **options):
    return MarkdownifyConverter(**options).convert_soup(soup)


if __name__ == "__main__":
    url = "https://school.programmers.co.kr/learn/courses/30/lessons/118666"
    if len(sys.argv) != 1:
        url = sys.argv[1]

    markdown_converter = MarkdownConverter(url, "lxml")