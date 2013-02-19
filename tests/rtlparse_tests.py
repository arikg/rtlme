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
        rule.style.setProperty("left", "right")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule= parser._resolve_attribute_rtl(rule, rtlRule, "float")
        self.assertEqual("", rtlRule.style.cssText)
        self.assertEqual("", rtlRule.style["float"])

    def test_resolve_attribute_rtl_invalid(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("float", "center")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule= parser._resolve_attribute_rtl(rule, rtlRule, "float")
        self.assertEqual("", rtlRule.style.cssText)
        self.assertEqual("", rtlRule.style["float"])

    def test_resolve_attribute_rtl(self):
        parser = CSSRtlParser("")
        rule = cssutils.css.CSSStyleRule()
        rule.style.setProperty("float", "right")
        rtlRule = cssutils.css.CSSStyleRule()
        rtlRule= parser._resolve_attribute_rtl(rule, rtlRule, "float")
        self.assertEqual("left", rtlRule.style["float"])

if __name__ == '__main__':
    unittest.main()