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


    def test_resolve_attribute_rtl_empty(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("clear", "right")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_attribute_rtl(rule, rtlRule, "float")
        self.assertEqual("", rtlRule.style.cssText)
        self.assertEqual("", rtlRule.style["float"])

    def test_resolve_attribute_rtl_invalid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("float", "center")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_attribute_rtl(rule, rtlRule, "float")
        self.assertEqual("", rtlRule.style.cssText)
        self.assertEqual("", rtlRule.style["float"])

    def test_resolve_attribute_rtl_valid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("float", "right")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_attribute_rtl(rule, rtlRule, "float")
        self.assertEqual("left", rtlRule.style["float"])


    def test_resolve_positioning_rtl_empty(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("right", "5px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_positioning_rtl(rule, rtlRule, "left")
        self.assertEqual("", rtlRule.style["left"])
        self.assertEqual("", rtlRule.style["right"])

    def test_resolve_positioning_rtl_invalid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("center", "5px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_positioning_rtl(rule, rtlRule, "center")
        self.assertEqual("", rtlRule.style["left"])
        self.assertEqual("", rtlRule.style["right"])
        self.assertEqual("", rtlRule.style["center"])

    def test_resolve_positioning_rtl_valid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("left", "5px")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule = parser._resolve_positioning_rtl(rule, rtlRule, "left")
        self.assertEqual("auto", rtlRule.style["left"])
        self.assertEqual("5px", rtlRule.style["right"])

if __name__ == '__main__':
    unittest.main()