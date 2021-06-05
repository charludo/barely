import unittest
from barely.plugins.content.ReadingTime.readingtime import ReadingTime


class TestReadingTime(unittest.TestCase):

    def test___init__(self):
        golden = {
            "PRIORITY": 850,
            "WPM_FAST": 265,
            "WPM_SLOW": 90,
            "SEPARATOR": " - "
        }
        rt = ReadingTime()
        self.assertDictEqual(golden, rt.plugin_config)

        rt.config["READING_TIME"] = {"PRIORITY": -1}
        rt.__init__()

        golden["PRIORITY"] = -1
        self.assertDictEqual(golden, rt.plugin_config)

        # reset
        del rt.config["READING_TIME"]
        rt.__init__()

    def test_register(self):
        rt = ReadingTime()
        name, prio, ext = rt.register()

        self.assertEqual(name, "ReadingTime")
        self.assertEqual(prio, 850)
        self.assertEqual(ext, ["md"])

    def test_action(self):
        item = {
            "content_raw": """
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
            voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
            amet.
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
            voluptua.
            At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
            voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet

            Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et
            accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit ame,
            consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.

            Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum
            iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto
            odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.

            Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer
            """,
            "meta": {}
        }

        rt = ReadingTime()
        result = list(rt.action(item=item))[0]

        self.assertEqual(result["meta"]["reading_time"], "1 - 3")
