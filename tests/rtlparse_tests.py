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


    def test_resolve_attribute_rule_rtl_empty(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("clear", "right")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_attribute_rule_rtl(rule, rtlRule, "float")
        self.assertEqual("", rtlRule.style.cssText)
        self.assertEqual("", rtlRule.style["float"])

    def test_resolve_attribute_rule_rtl_invalid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("float", "center")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_attribute_rule_rtl(rule, rtlRule, "float")
        self.assertEqual("", rtlRule.style.cssText)
        self.assertEqual("", rtlRule.style["float"])

    def test_resolve_attribute_rule_rtl_valid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("float", "right")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_attribute_rule_rtl(rule, rtlRule, "float")
        self.assertEqual("left", rtlRule.style["float"])


    def test_resolve_positioning_rule_rtl_empty(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("right", "5px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_positioning_rule_rtl(rule, rtlRule, "left")
        self.assertEqual("", rtlRule.style["left"])
        self.assertEqual("", rtlRule.style["right"])

    def test_resolve_positioning_rule_rtl_invalid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("center", "5px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_positioning_rule_rtl(rule, rtlRule, "center")
        self.assertEqual("", rtlRule.style["left"])
        self.assertEqual("", rtlRule.style["right"])
        self.assertEqual("", rtlRule.style["center"])

    def test_resolve_positioning_rule_rtl_valid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("left", "5px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_positioning_rule_rtl(rule, rtlRule, "left")
        self.assertEqual("auto", rtlRule.style["left"])
        self.assertEqual("5px", rtlRule.style["right"])


    def test_resolve_spacing_shorthanded_rule_rtl_valid_4_values_different(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("padding", "25px 50px 75px 100px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("25px 100px 75px 50px", rtlRule.style["padding"])

    def test_resolve_spacing_shorthanded_rule_rtl_valid_4_values_same(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("padding", "25px 50px 75px 50px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("", rtlRule.style["padding"])

    def test_resolve_spacing_shorthanded_rule_rtl_valid_3_values_or_less(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rtlRule = cssutils.css.CSSStyleRule()

        rule.style.setProperty("padding", "25px 50px 75px")
        rtlRule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("", rtlRule.style["padding"])

        rule.style.setProperty("padding", "25px 50px")
        rtlRule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("", rtlRule.style["padding"])

        rule.style.setProperty("padding", "25px ")
        rtlRule = parser._resolve_spacing_shorthanded_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("", rtlRule.style["padding"])

    def test_resolve_spacing_specific_rule_rtl_valid_left_and_right_different(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("padding-left", "25px")
        rule.style.setProperty("padding-right", "50px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_spacing_specific_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("50px", rtlRule.style["padding-left"])
        self.assertEqual("25px", rtlRule.style["padding-right"])

    def test_resolve_spacing_specific_rule_rtl_valid_left_and_right_same(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("padding-left", "25px")
        rule.style.setProperty("padding-right", "25px ")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_spacing_specific_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("", rtlRule.style["padding-left"])
        self.assertEqual("", rtlRule.style["padding-right"])

    def test_resolve_spacing_specific_rule_rtl_valid_only_right(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("padding-right", "50px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_spacing_specific_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("50px", rtlRule.style["padding-left"])
        self.assertEqual("0", rtlRule.style["padding-right"])

    def test_resolve_spacing_specific_rule_rtl_valid_only_left(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("padding-left", "25px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_spacing_specific_rule_rtl(rule, rtlRule, "padding")
        self.assertEqual("25px", rtlRule.style["padding-right"])
        self.assertEqual("0", rtlRule.style["padding-left"])


    def test_resolve_background_rule_rtl_empty(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_background_rule_rtl(rule, rtlRule, "background")
        self.assertEqual("", rtlRule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_ignored(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("background", "center top")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_background_rule_rtl(rule, rtlRule, "background")
        self.assertEqual("", rtlRule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_set(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("background", "left top")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_background_rule_rtl(rule, rtlRule, "background")
        self.assertEqual("right top", rtlRule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_zero(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("background", "0 20")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_background_rule_rtl(rule, rtlRule, "background")
        self.assertEqual("100% 20", rtlRule.style["background"])

    def test_resolve_background_rule_rtl_valid_position_percent(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("background", "70% 15%")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_background_rule_rtl(rule, rtlRule, "background")
        self.assertEqual("30% 15%", rtlRule.style["background"])

if __name__ == '__main__':
    unittest.main()