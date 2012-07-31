"""
Created on Jul 27, 2012

@author: arikg
"""

import cssutils

def reverseDirection(direction, ignoredValues=()):
    if direction in ignoredValues:
        return None
    elif direction.lower() == "left":
        return "right"
    elif direction.lower() == "right":
        return "left"
    else:
        raise ValueError("can't reverse string " + direction)


def reverseAttribute(rtlRule, name, ignoredValues=()):
    attribute = rule.style[name]
    if len(attribute) > 0:
        rtlValue = reverseDirection(attribute, ignoredValues)
        if rtlValue != None:
            rtlRule.style.setProperty(name, rtlValue)
    return rtlRule


def reversePositioning(rtlRule, name):
    attribute = rule.style[name]
    if len(attribute) > 0:
        rtlName = reverseDirection(name)
        rtlRule.style.setProperty(name, "auto")
        rtlRule.style.setProperty(rtlName, attribute)
    return rtlRule


def reverseShorthandVersion(rtlRule, name):
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

if __name__ == '__main__':
    stylesheet = cssutils.parseFile("example/elist.css", "utf-8")
    rtlStylesheet = cssutils.css.CSSStyleSheet()
    rtlStylesheet.add("body{ direction: rtl; unicode-bidi: embed; }")
    for rule in stylesheet.cssRules:
        if rule.type == rule.STYLE_RULE:
            rtlRule = cssutils.css.CSSStyleRule()
            rtlRule.selectorText = rule.selectorText

            rtlRule = reverseAttribute(rtlRule, "text-align", ("center"))
            rtlRule = reverseAttribute(rtlRule, "float", ("none"))
            rtlRule = reverseAttribute(rtlRule, "clear", ("both"))

            rtlRule = reversePositioning(rtlRule, "left")
            rtlRule = reversePositioning(rtlRule, "right")
            rtlRule = reverseShorthandVersion(rtlRule, "margin")
            rtlRule = reverseShorthandVersion(rtlRule, "padding")

            if rtlRule.style.length > 0:
                rtlStylesheet.add(rtlRule)

    for rule in rtlStylesheet.cssRules:
        print(rule.cssText)