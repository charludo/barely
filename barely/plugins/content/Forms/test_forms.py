import re
import unittest
from barely.plugins.content.Forms.forms import Forms


class TestForms(unittest.TestCase):

    def test___init__(self):
        f = Forms()
        self.assertDictEqual({"PRIORITY": 5}, f.plugin_config)

        golden = {
            "PRIORITY": 2
        }
        f.config["FORMS"] = {"PRIORITY": 2}
        f.__init__()

        self.assertDictEqual(golden, f.plugin_config)

        # reset
        del f.config["FORMS"]
        f.__init__()

    def test_register(self):
        f = Forms()
        name, prio, ext = f.register()

        self.assertEqual(name, "Forms")
        self.assertEqual(prio, 5)
        self.assertEqual(ext, ["md"])

    def test_action(self):
        item = {
            "meta": {
                "forms": {
                    "sample": {
                        "action": "test.php",
                        "classes": "large",
                        "group-basic": {
                            "legend": "Basic Data",
                            "name": {
                                "type": "text",
                                "required": True,
                                "placeholder": "Name"
                            },
                            "mmail": {
                                "type": "email",
                                "required": True,
                                "placeholder": "E-Mail"
                            }
                        },
                        "topic": {
                            "type": "select",
                            "multiple": False,
                            "default": "standard",
                            "options": {
                                "n1": "something",
                                "n2": "standard",
                                "n3": "something else"
                            }
                        },
                        "group-radios": {
                            "rating": {
                                "type": "radio",
                                "label": "Please rate us!",
                                "options": {
                                    1: "1",
                                    2: "2",
                                    3: "3"
                                }
                            }
                        },
                        "message": {
                            "type": "textarea",
                            "required": True,
                            "classes": "extra",
                            "value": "Pre-filled"
                        },
                        "grpd": {
                            "type": "checkbox",
                            "value": "agreed",
                            "label": "Agree to GDPR",
                            "name": "gdpr-checkbox"
                        },
                        "send": {
                            "type": "button",
                            "value": "Send Now",
                            "action": "submit"
                        }
                    }
                }
            }
        }

        golden_form = """
        <form id="form-sample" class="large" action="test.php">
        <fieldset id="form-sample-group-basic" class="">
        <legend>Basic Data</legend>
        <input type="text" id="form-sample-name" class="" name="name" value="" placeholder="Name" required>
        <input type="email" id="form-sample-mmail" class="" name="mmail" value="" placeholder="E-Mail" required>
        </fieldset>
        <select id="form-sample-topic" class="" name="topic"  >
        <option value="n1" >something</option>
        <option value="n2" >standard</option>
        <option value="n3" >something else</option>
        </select>
        <fieldset id="form-sample-group-radios" class="">
        <label for="form-sample-rating">Please rate us!</label>
        <input type="radio" id="form-sample-rating-1" value="1" name="rating" >
        <label for="form-sample-rating-1">1</label>
        <input type="radio" id="form-sample-rating-2" value="2" name="rating" >
        <label for="form-sample-rating-2">2</label>
        <input type="radio" id="form-sample-rating-3" value="3" name="rating" >
        <label for="form-sample-rating-3">3</label>
        </fieldset>
        <textarea id="form-sample-message" class="extra" rows="" cols="" name="message" placeholder="" required>Pre-filled</textarea>
        <label for="form-sample-grpd">Agree to GDPR</label>
        <input type="checkbox" id="form-sample-grpd" class="" name="grpd" value="agreed" placeholder="" >
        <button type="submit" id="form-sample-send" class="" name="send">Send Now</button>
        </form>
        """

        f = Forms()
        result = list(f.action(item=item))[0]
        self.assertEqual(re.sub(r'[\s+]', '', golden_form), re.sub(r'[\s+]', '', result["meta"]["form_sample"]))
