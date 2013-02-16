"""
Created on Jul 27, 2012

@author: arikg
"""

import cssutils
import re

def reverse_direction(direction, ignoredValues=()):
    if direction in ignoredValues:
        return None
    elif direction.lower() == "left":
        return "right"
    elif direction.lower() == "right":
        return "left"
    else:
        raise ValueError("can't reverse string " + direction)


def reverse_attribute(rule, rtlRule, name, ignoredValues=()):
    attribute = rule.style[name]
    if len(attribute) > 0:
        rtlValue = reverse_direction(attribute, ignoredValues)
        if rtlValue is not None:
            rtlRule.style.setProperty(name, rtlValue)
    return rtlRule


def reverse_positioning(rule, rtlRule, name):
    attribute = rule.style[name]
    if len(attribute) > 0:
        rtlName = reverse_direction(name)
        rtlRule.style.setProperty(name, "auto")
        rtlRule.style.setProperty(rtlName, attribute)
    return rtlRule


def reverse_shorthand_version(rule, rtlRule, name):
    value = rule.style[name]
    if len(value) > 0:
        splitValues = value.split()
        if len(splitValues) == 4 and splitValues[1] != splitValues[3]:
            splitValues[1], splitValues[3] = splitValues[3], splitValues[1]
            rtlRule.style.setProperty(name, " ".join(splitValues))
    nameLeft = name + "-left"
    nameRight = name + "-right"
    valueLeft = rule.style[nameLeft]
    valueRight = rule.style[nameRight]
    if len(valueRight) > 0 and len(valueLeft) > 0:
        rtlRule.style.setProperty(nameLeft, valueRight)
        rtlRule.style.setProperty(nameRight, valueLeft)
    elif len(valueRight) > 0:
        rtlRule.style.setProperty(nameLeft, valueRight)
        rtlRule.style.setProperty(nameRight, "0px")
    elif len(valueLeft) > 0:
        rtlRule.style.setProperty(nameLeft, "0px")
        rtlRule.style.setProperty(nameRight, valueLeft)
    return rtlRule


def background_position_pattern(currValue):
    return re.search(r'\b(right|left|center|\d+%*)\s(top|center|bottom|\d+\w{0,2})*\b', currValue)


def reverse_background_position(rule, rtlRule, name):
    value = rule.style[name]
    save = False
    if len(value) > 0:
        pattern = background_position_pattern(value)
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
def reverse_border(rule, rtlRule):
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


def rtl_stylesheet(stylesheet):
    rtlStylesheet = cssutils.css.CSSStyleSheet()
    rtlStylesheet.add("body{ direction: rtl; unicode-bidi: embed; }")
    for rule in stylesheet.cssRules:
        if rule.type == rule.STYLE_RULE:
            rtlRule = cssutils.css.CSSStyleRule()
            rtlRule.selectorText = rule.selectorText

            rtlRule = reverse_attribute(rule, rtlRule, "text-align", "center")
            rtlRule = reverse_attribute(rule, rtlRule, "float", "none")
            rtlRule = reverse_attribute(rule, rtlRule, "clear", "both")

            rtlRule = reverse_positioning(rule, rtlRule, "left")
            rtlRule = reverse_positioning(rule, rtlRule, "right")

            rtlRule = reverse_shorthand_version(rule, rtlRule, "margin")
            rtlRule = reverse_shorthand_version(rule, rtlRule, "padding")

            rtlRule = reverse_background_position(rule, rtlRule, "background-position")
            rtlRule = reverse_background_position(rule, rtlRule, "background")

            rtlRule = reverse_border(rule, rtlRule)

            if rtlRule.style.length > 0:
                rtlStylesheet.add(rtlRule)
    return rtlStylesheet

if __name__ == '__main__':
    stylesheet = cssutils.parseFile("example/elist.css", "utf-8")
    rtlStylesheet = rtl_stylesheet(stylesheet)

    for rule in rtlStylesheet.cssRules:
        print(rule.cssText)