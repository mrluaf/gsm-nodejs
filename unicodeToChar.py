__all__ = ['unicodeToChar']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([u'unicodeToChar'])
@Js
def PyJsHoisted_unicodeToChar_(text, this, arguments, var=var):
    var = Scope({u'this':this, u'text':text, u'arguments':arguments}, var)
    var.registers([u'text'])
    @Js
    def PyJs_anonymous_0_(match, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'match':match}, var)
        var.registers([u'match'])
        return var.get(u'String').callprop(u'fromCharCode', var.get(u'parseInt')(var.get(u'match').callprop(u'replace', JsRegExp(u'/\\\\u/g'), Js(u'')), Js(16.0)))
    PyJs_anonymous_0_._set_name(u'anonymous')
    return var.get(u'text').callprop(u'replace', JsRegExp(u'/\\\\u[\\dA-F]{4}/gi'), PyJs_anonymous_0_)
PyJsHoisted_unicodeToChar_.func_name = u'unicodeToChar'
var.put(u'unicodeToChar', PyJsHoisted_unicodeToChar_)
pass
pass


# Add lib to the module scope
unicodeToChar = var.to_python()