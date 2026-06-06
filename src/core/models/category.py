class Category:
    def __init__(self, page):
        
        self.title = page.meta.get("title")
        self.slug = page.meta.get("slug")
        self.services = []