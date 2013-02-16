import re
import cssutils

class RtlParser(object):
    def __init__(self, source):
        self.source = source

    def parse(self):
        pass


class CSSRtlParser(RtlParser):
    def __init__(self, source):
        super(CSSRtlParser, self).__init__(source)
        self.resolvers = {"text-align": self._resolve_attribute,
                          "float": self._resolve_attribute,
                          "clear": self._resolve_attribute,
                          "left": self._resolve_positioning,
                          "right": self._resolve_positioning,
                          "margin": self._resolve_spacing,
                          "padding": self._resolve_spacing,
                          "background": self._resolve_background,
                          "background-position": self._resolve_background}


    def parse(self):
        """ parse a string containing css data and return an rtl fixing version """
        stylesheet = cssutils.parseString(self.source)
        rtlStylesheet = self._rtl_this(stylesheet)
        return rtlStylesheet.cssText

    def _rtl_this(self, stylesheet):
        rtlStylesheet = cssutils.css.CSSStyleSheet()
        rtlStylesheet.add("body{ direction: rtl; unicode-bidi: embed; }")
        for rule in stylesheet.cssRules:
            if rule.type == rule.STYLE_RULE:
                rtlRule = cssutils.css.CSSStyleRule()
                rtlRule.selectorText = rule.selectorText

                for key, resolver in self.resolvers.items():
                    rtlRule = resolver(rule, rtlRule, key)

                if "border" in rule.style.cssText:
                    rtlRule = self._reverse_border(rule, rtlRule)

                if rtlRule.style.length > 0:
                    rtlStylesheet.add(rtlRule)
        return rtlStylesheet

    def _resolve_attribute(self, rule, rtlRule, name):
        """ Reverse an attribute direction left/right and return the matching rtl css rule"""
        attribute = rule.style[name]
        if attribute:
            rtlValue = self._switch_direction(attribute)
            if rtlValue is not None:
                rtlRule.style.setProperty(name, rtlValue)
        return rtlRule

    def _resolve_positioning(self, rule, rtlRule, name):
        """ Reverse a positioning attribute direction left/right (and set previous one to auto) and return the matching rtl css rule"""
        attribute = rule.style[name]
        if attribute:
            rtlName = self._switch_direction(name)
            rtlRule.style.setProperty(name, "auto")
            rtlRule.style.setProperty(rtlName, attribute)
        return rtlRule

    def _resolve_spacing(self, rule, rtlRule, name):
        """ Reverse a spacing attribute (supporting full and shorthanded version) and return the matching rtl css rule"""
        value = rule.style[name]
        if value:
            splitValues = value.split()
            if len(splitValues) == 4 and splitValues[1] != splitValues[3]:
                splitValues[1], splitValues[3] = splitValues[3], splitValues[1]
                rtlRule.style.setProperty(name, " ".join(splitValues))
        nameLeft = name + "-left"
        nameRight = name + "-right"
        valueLeft = rule.style[nameLeft]
        valueRight = rule.style[nameRight]
        if valueRight and valueLeft:
            rtlRule.style.setProperty(nameLeft, valueRight)
            rtlRule.style.setProperty(nameRight, valueLeft)
        elif valueRight:
            rtlRule.style.setProperty(nameLeft, valueRight)
            rtlRule.style.setProperty(nameRight, "0px")
        elif valueLeft:
            rtlRule.style.setProperty(nameLeft, "0px")
            rtlRule.style.setProperty(nameRight, valueLeft)
        return rtlRule

    def _switch_direction(self, direction):
        """ Reverse right/left. for other values return null """
        if direction.lower() == "left":
            return "right"
        elif direction.lower() == "right":
            return "left"
        else:
            return None

    def _background_position_pattern(self, currValue):
        return re.search(r'\b(right|left|center|\d+%*)\s(top|center|bottom|\d+\w{0,2})*\b', currValue)

    def _resolve_background(self, rule, rtlRule, name):
        """ Reverse an background attribute direction left/right and return the matching rtl css rule"""
        value = rule.style[name]
        save = False
        if len(value) > 0:
            pattern = self._background_position_pattern(value)
            if pattern:
                splitValue = list(pattern.groups())
                if splitValue[0] == "right":
                    splitValue[0] = "left"
                    save = True
                elif splitValue[0] == "left":
                    splitValue[0] = "right"
                    save = True
                elif splitValue[0] == "0":
                    splitValue[0] = "100%"
                    save = True
                elif splitValue[0].find("%") > 0:
                    percent = splitValue[0].replace("%", "")
                    splitValue[0] = str(100 - int(percent)) + "%"
                    save = True

                if save:
                    rtlRule.style.setProperty(name, " ".join(splitValue))
        return rtlRule

    # TODO arikg: border-top-left-radius etc. border-bottom-left-radius, spacing, radius
    def _reverse_border(self, rule, rtlRule):
        """ Reverse a border attribute (supporting all kinds of border parameters) and return the matching rtl css rule"""
        border_suffixes = ("", "-style", "-width", "-color")
        for suffix in border_suffixes:
            name = "border" + suffix
            value = rule.style[name]
            if len(value) > 0:
                splitValues = value.split()
                if len(splitValues) == 4 and splitValues[1] != splitValues[3]:
                    splitValues[1], splitValues[3] = splitValues[3], splitValues[1]
                    rtlRule.style.setProperty(name, " ".join(splitValues))

            nameLeft = "border-" + "left" + suffix
            nameRight = "border-" + "right" + suffix
            valueLeft = rule.style[nameLeft]
            valueRight = rule.style[nameRight]
            if len(valueRight) > 0 and len(valueLeft) > 0:
                rtlRule.style.setProperty(nameLeft, valueRight)
                rtlRule.style.setProperty(nameRight, valueLeft)
            elif len(valueRight) > 0:
                rtlRule.style.setProperty(nameLeft, valueRight)
                rtlRule.style.setProperty(nameRight, "inherit")
            elif len(valueLeft) > 0:
                rtlRule.style.setProperty(nameLeft, "inherit")
                rtlRule.style.setProperty(nameRight, valueLeft)
        return rtlRule


if __name__ == '__main__':
    with open("example/elist.css", "r") as f:
        source = f.read()

    if source:
        parser = CSSRtlParser(source)
        result = parser.parse()
        for line in result.split('\n'):
            print line

