"""Templating engine for rendering Jinja templates."""

import logging

from decorators import monitor
from exceptions import TemplateNotFoundError
from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateNotFound
from metrics import HERMES_TEMPLATE_NAME


class TemplatingEngine:
    """Template engine."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern that allows arbitrary arguments."""
        if cls._instance is None:
            cls._instance = super(TemplatingEngine, cls).__new__(cls)
            # Initialize _instance's attributes
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger: logging.LoggerAdapter = None):
        """Initialize template engine."""
        if not self._initialized:
            self._default_template = None
            self._logger = logger if logger else logging.getLogger(__name__)
            self._initialized = True

    @monitor
    def render_template(
        self, context: dict = None, raw_template: str = None, template_name: str = None
    ):
        """Render the jinja template with the provided context data."""
        if context is None:
            context = {}

        if raw_template and template_name:
            raise ValueError("Cannot provide both raw_template and template_name.")

        # Template was provided at runtime.
        if raw_template:
            self._logger.info(
                f"### Hermes is using a runtime template: \n\n {raw_template=}"
            )

            tmp_template = self._load_template_from_string(raw_template)
            return tmp_template.render(context)

        # Load template from disk every time.
        if template_name:
            try:
                tmp_template = self._load_template(template_name=template_name)
                return tmp_template.render(context)
            except TemplateNotFound as ex:
                raise TemplateNotFoundError(
                    f"Template not found: {template_name}. {ex=}"
                )

        # If no template is provided or template could not be rendered, fallback to the default.
        if self._default_template is None:
            self._default_template = self._load_template()

        return self._default_template.render(context)

    def _load_template(self, template_name: str = "production.yml.j2") -> Template:
        """Load template from disk."""
        loader = FileSystemLoader(searchpath="./templates")
        env = Environment(loader=loader)
        # TODO: support dynamic routing to different templates.
        template = env.get_template(template_name)
        HERMES_TEMPLATE_NAME.labels(template_name=template_name).inc()
        return template

    def _load_template_from_string(self, raw_template: str):
        """Load template from raw string."""
        return Template(raw_template)
