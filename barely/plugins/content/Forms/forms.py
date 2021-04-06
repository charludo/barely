"""
Generate forms from yaml shorthand.
Allow the easy creation of forms
by requiring the smallest possible
amount of information to generate
any HTML5 form.
"""
import re
from barely.plugins import PluginBase


class Forms(PluginBase):
    # generate an arbitrary amount of forms for any page, specified through yaml

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 5
            }
        try:
            self.plugin_config = standard_config | self.config["FORMS"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "Forms", self.plugin_config["PRIORITY"], self.config["PAGE_EXT"]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            try:
                form_list = item["meta"]["forms"]
            except KeyError:
                yield item
                return

            for key, value in form_list:
                item["form-" + key] = "\n".join(self.generate_form(key, value))
            yield item

    def generate_form(self, form_name, **form_config):
        form_config = self.form_defaults | form_config
        yield f"<form id=\"form-{form_name}\" class=\"{form_config['classes']}\" action=\"{form_config['action']}\">"
        for field, settings in form_config:
            if field in ["action", "classes"]:
                continue
            yield from self.render_fields(form_name, field, settings)
        yield "</form>"

    def render_fields(self, form_name, field_name, **field_config):
        id = "form-" + form_name + "-" + field_name

        if re.match(r"^group-.+", field_name):
            field_config = self.group_defaults | field_config
            yield f"<fieldset id=\"{id}\" class=\"{field_config['classes']}\">"

            if field_config["legend"]:
                yield f"<legend>{field_config['legend']}</legend>"

            for field, settings in field_config:
                if field in ["legend", "classes"]:
                    continue
                yield from self.render_fields(form_name, field, settings)

            yield "</fieldset>"

        else:
            field_config = self.field_defaults | field_config
            required = "required" if field_config["required"] else ""
            if field_config["label"]:
                yield f"<label for=\"{id}\">{field_config['label']}</label>"

            if field_config["type"] == "radio":
                for value, option in field_config["options"]:
                    checked = "checked" if value == field_config["default"] else ""
                    radio_id = id + "-" + value
                    yield f"<input type=\"radio\" id=\"{radio_id}\" value=\"{value}\" name=\"{field_name}\" {checked}>"
                    yield f"<label for=\"{radio_id}\">option</label>"

            elif field_config["type"] == "select":
                multiple = "multiple" if field_config["multiple"] else ""
                yield f"<select id=\"{id}\" class=\"{field_config['classes']}\" name=\"{field_name}\" {multiple} {required}>"

                for value, option in field_config["options"]:
                    selected = "selected" if value == field_config["default"] else ""
                    yield f"<option value=\"{value}\" {selected}>{option}</option>"
                yield "</select>"
            else:
                yield f"<input type=\"{field_config['type']} "
                + f"id=\"{id}\" class=\"{field_config['classes']}\" "
                + f"name=\"{field_name}\" value=\"{field_config['default']}\" placeholder=\"{field_config['placeholder']}\" {required}>"
