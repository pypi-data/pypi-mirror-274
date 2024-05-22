from enum import Enum


class ExtensionValueType(str, Enum):
    XSANYURI = "xs:anyURI"
    XSBASE64BINARY = "xs:base64Binary"
    XSBOOLEAN = "xs:boolean"
    XSBYTE = "xs:byte"
    XSDATE = "xs:date"
    XSDATETIME = "xs:dateTime"
    XSDECIMAL = "xs:decimal"
    XSDOUBLE = "xs:double"
    XSDURATION = "xs:duration"
    XSFLOAT = "xs:float"
    XSGDAY = "xs:gDay"
    XSGMONTH = "xs:gMonth"
    XSGMONTHDAY = "xs:gMonthDay"
    XSGYEAR = "xs:gYear"
    XSGYEARMONTH = "xs:gYearMonth"
    XSHEXBINARY = "xs:hexBinary"
    XSINT = "xs:int"
    XSINTEGER = "xs:integer"
    XSLONG = "xs:long"
    XSNEGATIVEINTEGER = "xs:negativeInteger"
    XSNONNEGATIVEINTEGER = "xs:nonNegativeInteger"
    XSNONPOSITIVEINTEGER = "xs:nonPositiveInteger"
    XSPOSITIVEINTEGER = "xs:positiveInteger"
    XSSHORT = "xs:short"
    XSSTRING = "xs:string"
    XSTIME = "xs:time"
    XSUNSIGNEDBYTE = "xs:unsignedByte"
    XSUNSIGNEDINT = "xs:unsignedInt"
    XSUNSIGNEDLONG = "xs:unsignedLong"
    XSUNSIGNEDSHORT = "xs:unsignedShort"

    def __str__(self) -> str:
        return str(self.value)
