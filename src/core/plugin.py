from mkdocs.plugins import BasePlugin
from .config import ServiceConfig
from .registry import Registry

from .models.category import Category
from .models.service import Service
from .models.step import Step
from .models.process import Process
from .models.channel import Channel


class ServicePlugin(BasePlugin[ServiceConfig]):

    def classify_page(self, page):

            uri = page.file.src_uri

            if uri.startswith(self.config.categories_dir + "/"):
                return "category"
            elif uri.startswith(self.config.services_dir + "/"):
                return "service"
            elif uri.startswith(self.config.processes_dir + "/"):
                return "process"
            elif uri.startswith(self.config.channels_dir + "/"):
                return "channel"
            
            return "generic"

    # 
    # relations between categories, services, processes, and channels are built after all pages have been read and parsed
    #

    def build_relations(self):        

        # CATEGORY → SERVICES
        for service in self.registry.services.values():

            for category_slug in service.category:

                category = self.registry.categories.get(category_slug)

                if category:
                    category.services.append(service)

            for process_slug in service.processes:

                process = self.registry.processes.get(process_slug)

                if process:
                    process.service.append(service.slug)

        # SERVICE → PROCESSES
        for process in self.registry.processes.values():

            for service_slug in process.service:

                service = self.registry.services.get(service_slug)

                if service:
                    service.processes.append(process)

        # PROCESS → STEPS → CHANNEL
        for process in self.registry.processes.values():

            resolved_steps = []

            for step in process.steps:

                channel_slug = step.channel if hasattr(step, "channel") else step.get("channel")
                channel = self.registry.channels.get(channel_slug)

                resolved_steps.append(
                        {
                            "title": step.title if hasattr(step, "title") else step.get("title"),
                            "description": step.description if hasattr(step, "description") else step.get("description"),
                            "channel": channel_slug,
                            "channel_title": channel.title if channel else None,
                            "channel_url": channel.url if channel else None,
                        }
                )

            process.steps = resolved_steps            

    # MkDocs plugin hooks
    def on_env(self, env, config, files):

        if getattr(self, "_relations_built", False):
            return env
        
        self.build_relations()
        self._relations_built = True

        return env

    # MkDocs plugin hooks
    def on_config(self, config):

        self.registry = Registry()        

        return config
    
    # This hook is called for each page after it has been read and parsed, but before it is converted to HTML
    def on_page_markdown(self, markdown, page, config, files):

        uri = page.file.src_uri

        if uri.startswith(self.config.categories_dir + "/"):

            category = Category(page)
            self.registry.categories[category.slug] = category

        elif uri.startswith(self.config.services_dir + "/"):
            
            service = Service(page)
            self.registry.services[service.slug] = service

        elif uri.startswith(self.config.processes_dir + "/"):

            process = Process(page)
            self.registry.processes[process.slug] = process

        elif uri.startswith(self.config.channels_dir + "/"):

            channel = Channel(page)
            self.registry.channels[channel.slug] = channel

        return markdown        

    # This hook is called for each page after it has been converted to HTML, but before it is written to disk
    def on_page_context(self, context, page, config, nav):

        uri = page.file.src_uri
        view_type = self.classify_page(page)
        context["ptv_view"] = view_type

        if view_type == "service":

            slug = page.meta.get("slug")
            service = self.registry.services.get(slug)

            if service:

                context["ptv"] = {
                    "service": service
                }


        if view_type == "category":

            slug = page.meta.get("slug")
            category = self.registry.categories.get(slug)

            if category:

                context["ptv"] = {
                    "category": category
                }

        if view_type == "process":

            slug = page.meta.get("slug")
            process = self.registry.processes.get(slug)

            if process:

                context["ptv"] = {
                    "process": process
                }

        return context