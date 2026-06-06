from mkdocs.config import base
from mkdocs.config import config_options as c

class ServiceConfig(base.Config):

    categories_dir = c.Type(str, default="categories")
    services_dir = c.Type(str, default="services")
    processes_dir = c.Type(str, default="processes")
    channels_dir = c.Type(str, default="channels")

    generate_indexes = c.Type(bool, default=True)
    show_related_content = c.Type(bool, default=True)