from core.models.step import Step

class Process:
    def __init__(self, page):
        
        self.title = page.meta.get("title")
        self.slug = page.meta.get("slug")
        self.service = page.meta.get("service", [])
        
        self.steps = []

        raw_steps = page.meta.get("steps", [])
        
        for raw_step in raw_steps:
            self.steps.append(Step(raw_step))
