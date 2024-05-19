from playwright.sync_api import sync_playwright

class Book:
    def __init__(self, size=None, margins=None, media='screen'):
        self.size = size
        self.margins = margins
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        self.page.emulate_media(media=media)

    def __del__(self):
        self.browser.close()
        self.playwright.stop()

    def load_url(self, url):
        self.page.goto(url, wait_until='load')

    def load_html(self, content):
        self.page.set_content(content, wait_until='load')

    def write_to_pdf(self, path, page_ranges=None):
        kwargs = dict(path=path, print_background=True)
        if page_ranges is not None:
            kwargs['page_ranges'] = page_ranges
        if self.size is not None:
            kwargs['format'] = self.size
        if self.margins is not None:
            kwargs['margin'] = self.margins
        self.page.pdf(**kwargs)

    def write_to_png(self, path):
        self.page.screenshot(path=path, type='png', full_page=True)

    def write_to_jpg(self, path, quality=None):
        kwargs = dict(path=path, type='jpeg', full_page=True)
        if quality is not None:
            kwargs['quality'] = quality
        self.page.screenshot(**kwargs)

if __name__ == '__main__':
    book = Book()
    book.load_url('https://en.wikipedia.org/wiki/Robert_Fico')
    book.write_to_pdf('hello.pdf')
    book.write_to_png('hello.png')
    book.write_to_jpg('hello.jpg')
