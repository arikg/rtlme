import unittest
import cssutils
from rtlparse.rtlparse import CSSRtlParser

class CssRtlParseTest(unittest.TestCase):
    def test_switch_direction_left(self):
        parser = CSSRtlParser("")
        result = parser._switch_direction("left")
        self.assertEqual("right", result)

    def test_switch_direction_right(self):
        parser = CSSRtlParser("")
        result = parser._switch_direction("right")
        self.assertEqual("left", result)

    def test_switch_direction_other(self):
        parser = CSSRtlParser("")
        result = parser._switch_direction("center")
        self.assertIsNone(result)


    def create_test_objects(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rtl_rule = cssutils.css.CSSStyleRule()
        return parser, rule, rtl_rule

    def test_resolve_attribute_rule_rtl_empty(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("clear", "right")
        rtl_rule = parser._resolve_attribute_rule_rtl(rule, rtl_rule, "float")
        self.assertEqual("", rtl_rule.style.cssText)
        self.assertEqual("", rtl_rule.style["float"])

    def test_resolve_attribute_rule_rtl_invalid(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("float", "center")
        rtl_rule = parser._resolve_attribute_rule_rtl(rule, rtl_rule, "float")
        self.assertEqual("", rtl_rule.style.cssText)
        self.assertEqual("", rtl_rule.style["float"])

    def test_resolve_attribute_rule_rtl_valid(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("float", "right")
        rtl_rule = parser._resolve_attribute_rule_rtl(rule, rtl_rule, "float")
        self.assertEqual("left", rtl_rule.style["float"])


    def test_resolve_positioning_rule_rtl_empty(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("right", "5px")
        rtl_rule = parser._resolve_positioning_rule_rtl(rule, rtl_rule, "left")
        self.assertEqual("", rtl_rule.style["left"])
        self.assertEqual("", rtl_rule.style["right"])

    def test_resolve_positioning_rule_rtl_invalid(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("center", "5px")
        rtl_rule = parser._resolve_positioning_rule_rtl(rule, rtl_rule, "center")
        self.assertEqual("", rtl_rule.style["left"])
        self.assertEqual("", rtl_rule.style["right"])
        self.assertEqual("", rtl_rule.style["center"])

    def test_resolve_positioning_rule_rtl_valid(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("left", "5px")
        rtl_rule = parser._resolve_positioning_rule_rtl(rule, rtl_rule, "left")
        self.assertEqual("auto", rtl_rule.style["left"])
        self.assertEqual("5px", rtl_rule.style["right"])


    def test_resolve_spacing_shorthanded_rule_rtl_valid_4_values_different(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("padding", "25px 50px 75px 100px")
        rtl_rule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("25px 100px 75px 50px", rtl_rule.style["padding"])

    def test_resolve_spacing_shorthanded_rule_rtl_valid_4_values_same(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("padding", "25px 50px 75px 50px")
        rtl_rule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("", rtl_rule.style["padding"])

    def test_resolve_spacing_shorthanded_rule_rtl_valid_3_values_or_less(self):
        parser, rule, rtl_rule = self.create_test_objects()

        rule.style.setProperty("padding", "25px 50px 75px")
        rtl_rule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("", rtl_rule.style["padding"])

        rule.style.setProperty("padding", "25px 50px")
        rtl_rule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("", rtl_rule.style["padding"])

        rule.style.setProperty("padding", "25px ")
        rtl_rule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("", rtl_rule.style["padding"])

    def test_resolve_spacing_specific_rule_rtl_valid_left_and_right_different(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("padding-left", "25px")
        rule.style.setProperty("padding-right", "50px")
        rtl_rule = parser._resolve_spacing_specific_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("50px", rtl_rule.style["padding-left"])
        self.assertEqual("25px", rtl_rule.style["padding-right"])

    def test_resolve_spacing_specific_rule_rtl_valid_left_and_right_same(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("padding-left", "25px")
        rule.style.setProperty("padding-right", "25px ")
        rtl_rule = parser._resolve_spacing_specific_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("", rtl_rule.style["padding-left"])
        self.assertEqual("", rtl_rule.style["padding-right"])

    def test_resolve_spacing_specific_rule_rtl_valid_only_right(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("padding-right", "50px")
        rtl_rule = parser._resolve_spacing_specific_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("50px", rtl_rule.style["padding-left"])
        self.assertEqual("0", rtl_rule.style["padding-right"])

    def test_resolve_spacing_specific_rule_rtl_valid_only_left(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("padding-left", "25px")
        rtl_rule = parser._resolve_spacing_specific_rule_rtl(rule, rtl_rule, "padding")
        self.assertEqual("25px", rtl_rule.style["padding-right"])
        self.assertEqual("0", rtl_rule.style["padding-left"])


    def test_resolve_background_rule_rtl_empty(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rtl_rule = parser._resolve_background_rule_rtl(rule, rtl_rule, "background")
        self.assertEqual("", rtl_rule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_ignored(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("background", "center top")
        rtl_rule = parser._resolve_background_rule_rtl(rule, rtl_rule, "background")
        self.assertEqual("", rtl_rule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_set(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("background", "left top")
        rtl_rule = parser._resolve_background_rule_rtl(rule, rtl_rule, "background")
        self.assertEqual("right top", rtl_rule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_zero(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("background", "0 20")
        rtl_rule = parser._resolve_background_rule_rtl(rule, rtl_rule, "background")
        self.assertEqual("100% 20", rtl_rule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_percent(self):
        parser, rule, rtl_rule = self.create_test_objects()
        rule.style.setProperty("background", "70% 15%")
        rtl_rule = parser._resolve_background_rule_rtl(rule, rtl_rule, "background")
        self.assertEqual("30% 15%", rtl_rule.style["background"])

if __name__ == '__main__':
    unittest.main()