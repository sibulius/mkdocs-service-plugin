class Channel:
    def __init__(self, page):
        
        self.title = page.meta.get("title")
        self.slug = page.meta.get("slug")
        self.type = page.meta.get("type")
        self.url = page.meta.get("url")