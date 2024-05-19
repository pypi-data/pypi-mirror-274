__all__ = ['handlebars_js']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# mustache.js uses a 'hack' to specify globalThis -> not supported by js2py
# see: https://mathiasbynens.be/notes/globalthis
# see: https://github.com/PiotrDabkowski/Js2Py/issues?q=is%3Aissue+__defineGetter__
# workaround: define the missing variables
@Js
def __defineGetter__(key, func):
    print(key)
    var.get('Object').get('prototype').put(str(key), func)
__defineGetter__._set_name('__defineGetter__')
var.get('Object').get('prototype').put('__defineGetter__', __defineGetter__)
var.put('__magic__', var.get(u"this"))


# Code follows:
var.registers([])
@Js
def PyJs_anonymous_0_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    def PyJs_LONG_423_(var=var):
        @Js
        def PyJs_anonymous_1_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_handlebarsRuntime2', 'module', '_interopRequireDefault', '_handlebarsCompilerAst2', '_handlebarsCompilerJavascriptCompiler2', '_handlebarsCompilerBase', '_handlebarsRuntime', '_handlebarsCompilerVisitor2', '_handlebarsNoConflict', '__webpack_require__', '_create', '_handlebarsNoConflict2', 'exports', 'create', '_handlebarsCompilerVisitor', 'inst', '_handlebarsCompilerAst', '_handlebarsCompilerCompiler', '_handlebarsCompilerJavascriptCompiler'])
            @Js
            def PyJsHoisted_create_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['hb'])
                var.put('hb', var.get('_create')())
                @Js
                def PyJs_anonymous_2_(input, options, this, arguments, var=var):
                    var = Scope({'input':input, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['options', 'input'])
                    return var.get('_handlebarsCompilerCompiler').callprop('compile', var.get('input'), var.get('options'), var.get('hb'))
                PyJs_anonymous_2_._set_name('anonymous')
                var.get('hb').put('compile', PyJs_anonymous_2_)
                @Js
                def PyJs_anonymous_3_(input, options, this, arguments, var=var):
                    var = Scope({'input':input, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['options', 'input'])
                    return var.get('_handlebarsCompilerCompiler').callprop('precompile', var.get('input'), var.get('options'), var.get('hb'))
                PyJs_anonymous_3_._set_name('anonymous')
                var.get('hb').put('precompile', PyJs_anonymous_3_)
                var.get('hb').put('AST', var.get('_handlebarsCompilerAst2').get('default'))
                var.get('hb').put('Compiler', var.get('_handlebarsCompilerCompiler').get('Compiler'))
                var.get('hb').put('JavaScriptCompiler', var.get('_handlebarsCompilerJavascriptCompiler2').get('default'))
                var.get('hb').put('Parser', var.get('_handlebarsCompilerBase').get('parser'))
                var.get('hb').put('parse', var.get('_handlebarsCompilerBase').get('parse'))
                var.get('hb').put('parseWithoutProcessing', var.get('_handlebarsCompilerBase').get('parseWithoutProcessing'))
                return var.get('hb')
            PyJsHoisted_create_.func_name = 'create'
            var.put('create', PyJsHoisted_create_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_handlebarsRuntime', var.get('__webpack_require__')(Js(2.0)))
            var.put('_handlebarsRuntime2', var.get('_interopRequireDefault')(var.get('_handlebarsRuntime')))
            var.put('_handlebarsCompilerAst', var.get('__webpack_require__')(Js(84.0)))
            var.put('_handlebarsCompilerAst2', var.get('_interopRequireDefault')(var.get('_handlebarsCompilerAst')))
            var.put('_handlebarsCompilerBase', var.get('__webpack_require__')(Js(85.0)))
            var.put('_handlebarsCompilerCompiler', var.get('__webpack_require__')(Js(90.0)))
            var.put('_handlebarsCompilerJavascriptCompiler', var.get('__webpack_require__')(Js(91.0)))
            var.put('_handlebarsCompilerJavascriptCompiler2', var.get('_interopRequireDefault')(var.get('_handlebarsCompilerJavascriptCompiler')))
            var.put('_handlebarsCompilerVisitor', var.get('__webpack_require__')(Js(88.0)))
            var.put('_handlebarsCompilerVisitor2', var.get('_interopRequireDefault')(var.get('_handlebarsCompilerVisitor')))
            var.put('_handlebarsNoConflict', var.get('__webpack_require__')(Js(83.0)))
            var.put('_handlebarsNoConflict2', var.get('_interopRequireDefault')(var.get('_handlebarsNoConflict')))
            var.put('_create', var.get('_handlebarsRuntime2').get('default').get('create'))
            pass
            var.put('inst', var.get('create')())
            var.get('inst').put('create', var.get('create'))
            var.get('_handlebarsNoConflict2').callprop('default', var.get('inst'))
            var.get('inst').put('Visitor', var.get('_handlebarsCompilerVisitor2').get('default'))
            var.get('inst').put('default', var.get('inst'))
            var.get('exports').put('default', var.get('inst'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_1_._set_name('anonymous')
        @Js
        def PyJs_anonymous_4_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            Js('use strict')
            @Js
            def PyJs_anonymous_5_(obj, this, arguments, var=var):
                var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
                var.registers(['obj'])
                return (var.get('obj') if (var.get('obj') and var.get('obj').get('__esModule')) else Js({'default':var.get('obj')}))
            PyJs_anonymous_5_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_5_)
            var.get('exports').put('__esModule', Js(True))
        PyJs_anonymous_4_._set_name('anonymous')
        @Js
        def PyJs_anonymous_6_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_handlebarsSafeString', 'module', 'Utils', 'runtime', '_handlebarsBase', '_interopRequireDefault', '_handlebarsException', '_handlebarsSafeString2', '_handlebarsRuntime', '_handlebarsException2', '_interopRequireWildcard', '_handlebarsNoConflict', '__webpack_require__', '_handlebarsUtils', '_handlebarsNoConflict2', 'exports', 'create', 'inst', 'base'])
            @Js
            def PyJsHoisted_create_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['hb'])
                var.put('hb', var.get('base').get('HandlebarsEnvironment').create())
                var.get('Utils').callprop('extend', var.get('hb'), var.get('base'))
                var.get('hb').put('SafeString', var.get('_handlebarsSafeString2').get('default'))
                var.get('hb').put('Exception', var.get('_handlebarsException2').get('default'))
                var.get('hb').put('Utils', var.get('Utils'))
                var.get('hb').put('escapeExpression', var.get('Utils').get('escapeExpression'))
                var.get('hb').put('VM', var.get('runtime'))
                @Js
                def PyJs_anonymous_7_(spec, this, arguments, var=var):
                    var = Scope({'spec':spec, 'this':this, 'arguments':arguments}, var)
                    var.registers(['spec'])
                    return var.get('runtime').callprop('template', var.get('spec'), var.get('hb'))
                PyJs_anonymous_7_._set_name('anonymous')
                var.get('hb').put('template', PyJs_anonymous_7_)
                return var.get('hb')
            PyJsHoisted_create_.func_name = 'create'
            var.put('create', PyJsHoisted_create_)
            Js('use strict')
            var.put('_interopRequireWildcard', var.get('__webpack_require__')(Js(3.0)).get('default'))
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_handlebarsBase', var.get('__webpack_require__')(Js(4.0)))
            var.put('base', var.get('_interopRequireWildcard')(var.get('_handlebarsBase')))
            var.put('_handlebarsSafeString', var.get('__webpack_require__')(Js(77.0)))
            var.put('_handlebarsSafeString2', var.get('_interopRequireDefault')(var.get('_handlebarsSafeString')))
            var.put('_handlebarsException', var.get('__webpack_require__')(Js(6.0)))
            var.put('_handlebarsException2', var.get('_interopRequireDefault')(var.get('_handlebarsException')))
            var.put('_handlebarsUtils', var.get('__webpack_require__')(Js(5.0)))
            var.put('Utils', var.get('_interopRequireWildcard')(var.get('_handlebarsUtils')))
            var.put('_handlebarsRuntime', var.get('__webpack_require__')(Js(78.0)))
            var.put('runtime', var.get('_interopRequireWildcard')(var.get('_handlebarsRuntime')))
            var.put('_handlebarsNoConflict', var.get('__webpack_require__')(Js(83.0)))
            var.put('_handlebarsNoConflict2', var.get('_interopRequireDefault')(var.get('_handlebarsNoConflict')))
            pass
            var.put('inst', var.get('create')())
            var.get('inst').put('create', var.get('create'))
            var.get('_handlebarsNoConflict2').callprop('default', var.get('inst'))
            var.get('inst').put('default', var.get('inst'))
            var.get('exports').put('default', var.get('inst'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_6_._set_name('anonymous')
        @Js
        def PyJs_anonymous_8_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            Js('use strict')
            @Js
            def PyJs_anonymous_9_(obj, this, arguments, var=var):
                var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
                var.registers(['obj', 'key', 'newObj'])
                if (var.get('obj') and var.get('obj').get('__esModule')):
                    return var.get('obj')
                else:
                    var.put('newObj', Js({}))
                    if (var.get('obj')!=var.get(u"null")):
                        for PyJsTemp in var.get('obj'):
                            var.put('key', PyJsTemp)
                            if var.get('Object').get('prototype').get('hasOwnProperty').callprop('call', var.get('obj'), var.get('key')):
                                var.get('newObj').put(var.get('key'), var.get('obj').get(var.get('key')))
                    var.get('newObj').put('default', var.get('obj'))
                    return var.get('newObj')
            PyJs_anonymous_9_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_9_)
            var.get('exports').put('__esModule', Js(True))
        PyJs_anonymous_8_._set_name('anonymous')
        @Js
        def PyJs_anonymous_10_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_logger', '_internalProtoAccess', 'LAST_COMPATIBLE_COMPILER_REVISION', 'module', 'HandlebarsEnvironment', '_interopRequireDefault', '_exception2', '_helpers', 'objectType', '_utils', 'log', '__webpack_require__', 'REVISION_CHANGES', '_decorators', 'exports', 'VERSION', '_logger2', '_exception', 'COMPILER_REVISION'])
            @Js
            def PyJsHoisted_HandlebarsEnvironment_(helpers, partials, decorators, this, arguments, var=var):
                var = Scope({'helpers':helpers, 'partials':partials, 'decorators':decorators, 'this':this, 'arguments':arguments}, var)
                var.registers(['decorators', 'helpers', 'partials'])
                var.get(u"this").put('helpers', (var.get('helpers') or Js({})))
                var.get(u"this").put('partials', (var.get('partials') or Js({})))
                var.get(u"this").put('decorators', (var.get('decorators') or Js({})))
                var.get('_helpers').callprop('registerDefaultHelpers', var.get(u"this"))
                var.get('_decorators').callprop('registerDefaultDecorators', var.get(u"this"))
            PyJsHoisted_HandlebarsEnvironment_.func_name = 'HandlebarsEnvironment'
            var.put('HandlebarsEnvironment', PyJsHoisted_HandlebarsEnvironment_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('HandlebarsEnvironment', var.get('HandlebarsEnvironment'))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            var.put('_helpers', var.get('__webpack_require__')(Js(10.0)))
            var.put('_decorators', var.get('__webpack_require__')(Js(70.0)))
            var.put('_logger', var.get('__webpack_require__')(Js(72.0)))
            var.put('_logger2', var.get('_interopRequireDefault')(var.get('_logger')))
            var.put('_internalProtoAccess', var.get('__webpack_require__')(Js(73.0)))
            var.put('VERSION', Js('4.7.8'))
            var.get('exports').put('VERSION', var.get('VERSION'))
            var.put('COMPILER_REVISION', Js(8.0))
            var.get('exports').put('COMPILER_REVISION', var.get('COMPILER_REVISION'))
            var.put('LAST_COMPATIBLE_COMPILER_REVISION', Js(7.0))
            var.get('exports').put('LAST_COMPATIBLE_COMPILER_REVISION', var.get('LAST_COMPATIBLE_COMPILER_REVISION'))
            var.put('REVISION_CHANGES', Js({'1':Js('<= 1.0.rc.2'),'2':Js('== 1.0.0-rc.3'),'3':Js('== 1.0.0-rc.4'),'4':Js('== 1.x.x'),'5':Js('== 2.0.0-alpha.x'),'6':Js('>= 2.0.0-beta.1'),'7':Js('>= 4.0.0 <4.3.0'),'8':Js('>= 4.3.0')}))
            var.get('exports').put('REVISION_CHANGES', var.get('REVISION_CHANGES'))
            var.put('objectType', Js('[object Object]'))
            pass
            def PyJs_LONG_18_(var=var):
                @Js
                def PyJs_registerHelper_11_(name, fn, this, arguments, var=var):
                    var = Scope({'name':name, 'fn':fn, 'this':this, 'arguments':arguments, 'registerHelper':PyJs_registerHelper_11_}, var)
                    var.registers(['name', 'fn'])
                    if PyJsStrictEq(var.get('_utils').get('toString').callprop('call', var.get('name')),var.get('objectType')):
                        if var.get('fn'):
                            PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('Arg not supported with multiple helpers')))
                            raise PyJsTempException
                        var.get('_utils').callprop('extend', var.get(u"this").get('helpers'), var.get('name'))
                    else:
                        var.get(u"this").get('helpers').put(var.get('name'), var.get('fn'))
                PyJs_registerHelper_11_._set_name('registerHelper')
                @Js
                def PyJs_unregisterHelper_12_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'unregisterHelper':PyJs_unregisterHelper_12_}, var)
                    var.registers(['name'])
                    var.get(u"this").get('helpers').delete(var.get('name'))
                PyJs_unregisterHelper_12_._set_name('unregisterHelper')
                @Js
                def PyJs_registerPartial_13_(name, partial, this, arguments, var=var):
                    var = Scope({'name':name, 'partial':partial, 'this':this, 'arguments':arguments, 'registerPartial':PyJs_registerPartial_13_}, var)
                    var.registers(['partial', 'name'])
                    if PyJsStrictEq(var.get('_utils').get('toString').callprop('call', var.get('name')),var.get('objectType')):
                        var.get('_utils').callprop('extend', var.get(u"this").get('partials'), var.get('name'))
                    else:
                        if PyJsStrictEq(var.get('partial',throw=False).typeof(),Js('undefined')):
                            PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(((Js('Attempting to register a partial called "')+var.get('name'))+Js('" as undefined'))))
                            raise PyJsTempException
                        var.get(u"this").get('partials').put(var.get('name'), var.get('partial'))
                PyJs_registerPartial_13_._set_name('registerPartial')
                @Js
                def PyJs_unregisterPartial_14_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'unregisterPartial':PyJs_unregisterPartial_14_}, var)
                    var.registers(['name'])
                    var.get(u"this").get('partials').delete(var.get('name'))
                PyJs_unregisterPartial_14_._set_name('unregisterPartial')
                @Js
                def PyJs_registerDecorator_15_(name, fn, this, arguments, var=var):
                    var = Scope({'name':name, 'fn':fn, 'this':this, 'arguments':arguments, 'registerDecorator':PyJs_registerDecorator_15_}, var)
                    var.registers(['name', 'fn'])
                    if PyJsStrictEq(var.get('_utils').get('toString').callprop('call', var.get('name')),var.get('objectType')):
                        if var.get('fn'):
                            PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('Arg not supported with multiple decorators')))
                            raise PyJsTempException
                        var.get('_utils').callprop('extend', var.get(u"this").get('decorators'), var.get('name'))
                    else:
                        var.get(u"this").get('decorators').put(var.get('name'), var.get('fn'))
                PyJs_registerDecorator_15_._set_name('registerDecorator')
                @Js
                def PyJs_unregisterDecorator_16_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'unregisterDecorator':PyJs_unregisterDecorator_16_}, var)
                    var.registers(['name'])
                    var.get(u"this").get('decorators').delete(var.get('name'))
                PyJs_unregisterDecorator_16_._set_name('unregisterDecorator')
                @Js
                def PyJs_resetLoggedPropertyAccesses_17_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'resetLoggedPropertyAccesses':PyJs_resetLoggedPropertyAccesses_17_}, var)
                    var.registers([])
                    var.get('_internalProtoAccess').callprop('resetLoggedProperties')
                PyJs_resetLoggedPropertyAccesses_17_._set_name('resetLoggedPropertyAccesses')
                return var.get('HandlebarsEnvironment').put('prototype', Js({'constructor':var.get('HandlebarsEnvironment'),'logger':var.get('_logger2').get('default'),'log':var.get('_logger2').get('default').get('log'),'registerHelper':PyJs_registerHelper_11_,'unregisterHelper':PyJs_unregisterHelper_12_,'registerPartial':PyJs_registerPartial_13_,'unregisterPartial':PyJs_unregisterPartial_14_,'registerDecorator':PyJs_registerDecorator_15_,'unregisterDecorator':PyJs_unregisterDecorator_16_,'resetLoggedPropertyAccesses':PyJs_resetLoggedPropertyAccesses_17_}))
            PyJs_LONG_18_()
            var.put('log', var.get('_logger2').get('default').get('log'))
            var.get('exports').put('log', var.get('log'))
            var.get('exports').put('createFrame', var.get('_utils').get('createFrame'))
            var.get('exports').put('logger', var.get('_logger2').get('default'))
        PyJs_anonymous_10_._set_name('anonymous')
        @Js
        def PyJs_anonymous_19_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['escapeExpression', 'appendContextPath', 'escape', 'exports', 'badChars', 'escapeChar', 'isEmpty', 'toString', 'indexOf', 'isFunction', 'isArray', 'module', 'extend', 'possible', 'blockParams', 'createFrame'])
            @Js
            def PyJsHoisted_escapeChar_(chr, this, arguments, var=var):
                var = Scope({'chr':chr, 'this':this, 'arguments':arguments}, var)
                var.registers(['chr'])
                return var.get('escape').get(var.get('chr'))
            PyJsHoisted_escapeChar_.func_name = 'escapeChar'
            var.put('escapeChar', PyJsHoisted_escapeChar_)
            @Js
            def PyJsHoisted_extend_(obj, this, arguments, var=var):
                var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
                var.registers(['obj', 'key', 'i'])
                #for JS loop
                var.put('i', Js(1.0))
                while (var.get('i')<var.get('arguments').get('length')):
                    for PyJsTemp in var.get('arguments').get(var.get('i')):
                        var.put('key', PyJsTemp)
                        if var.get('Object').get('prototype').get('hasOwnProperty').callprop('call', var.get('arguments').get(var.get('i')), var.get('key')):
                            var.get('obj').put(var.get('key'), var.get('arguments').get(var.get('i')).get(var.get('key')))
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                return var.get('obj')
            PyJsHoisted_extend_.func_name = 'extend'
            var.put('extend', PyJsHoisted_extend_)
            @Js
            def PyJsHoisted_indexOf_(array, value, this, arguments, var=var):
                var = Scope({'array':array, 'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['len', 'array', 'i', 'value'])
                #for JS loop
                var.put('i', Js(0.0))
                var.put('len', var.get('array').get('length'))
                while (var.get('i')<var.get('len')):
                    if PyJsStrictEq(var.get('array').get(var.get('i')),var.get('value')):
                        return var.get('i')
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                return (-Js(1.0))
            PyJsHoisted_indexOf_.func_name = 'indexOf'
            var.put('indexOf', PyJsHoisted_indexOf_)
            @Js
            def PyJsHoisted_escapeExpression_(string, this, arguments, var=var):
                var = Scope({'string':string, 'this':this, 'arguments':arguments}, var)
                var.registers(['string'])
                if PyJsStrictNeq(var.get('string',throw=False).typeof(),Js('string')):
                    if (var.get('string') and var.get('string').get('toHTML')):
                        return var.get('string').callprop('toHTML')
                    else:
                        if (var.get('string')==var.get(u"null")):
                            return Js('')
                        else:
                            if var.get('string').neg():
                                return (var.get('string')+Js(''))
                    var.put('string', (Js('')+var.get('string')))
                if var.get('possible').callprop('test', var.get('string')).neg():
                    return var.get('string')
                return var.get('string').callprop('replace', var.get('badChars'), var.get('escapeChar'))
            PyJsHoisted_escapeExpression_.func_name = 'escapeExpression'
            var.put('escapeExpression', PyJsHoisted_escapeExpression_)
            @Js
            def PyJsHoisted_isEmpty_(value, this, arguments, var=var):
                var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['value'])
                if (var.get('value').neg() and PyJsStrictNeq(var.get('value'),Js(0.0))):
                    return Js(True)
                else:
                    if (var.get('isArray')(var.get('value')) and PyJsStrictEq(var.get('value').get('length'),Js(0.0))):
                        return Js(True)
                    else:
                        return Js(False)
            PyJsHoisted_isEmpty_.func_name = 'isEmpty'
            var.put('isEmpty', PyJsHoisted_isEmpty_)
            @Js
            def PyJsHoisted_createFrame_(object, this, arguments, var=var):
                var = Scope({'object':object, 'this':this, 'arguments':arguments}, var)
                var.registers(['frame', 'object'])
                var.put('frame', var.get('extend')(Js({}), var.get('object')))
                var.get('frame').put('_parent', var.get('object'))
                return var.get('frame')
            PyJsHoisted_createFrame_.func_name = 'createFrame'
            var.put('createFrame', PyJsHoisted_createFrame_)
            @Js
            def PyJsHoisted_blockParams_(params, ids, this, arguments, var=var):
                var = Scope({'params':params, 'ids':ids, 'this':this, 'arguments':arguments}, var)
                var.registers(['ids', 'params'])
                var.get('params').put('path', var.get('ids'))
                return var.get('params')
            PyJsHoisted_blockParams_.func_name = 'blockParams'
            var.put('blockParams', PyJsHoisted_blockParams_)
            @Js
            def PyJsHoisted_appendContextPath_(contextPath, id, this, arguments, var=var):
                var = Scope({'contextPath':contextPath, 'id':id, 'this':this, 'arguments':arguments}, var)
                var.registers(['contextPath', 'id'])
                return (((var.get('contextPath')+Js('.')) if var.get('contextPath') else Js(''))+var.get('id'))
            PyJsHoisted_appendContextPath_.func_name = 'appendContextPath'
            var.put('appendContextPath', PyJsHoisted_appendContextPath_)
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('extend', var.get('extend'))
            var.get('exports').put('indexOf', var.get('indexOf'))
            var.get('exports').put('escapeExpression', var.get('escapeExpression'))
            var.get('exports').put('isEmpty', var.get('isEmpty'))
            var.get('exports').put('createFrame', var.get('createFrame'))
            var.get('exports').put('blockParams', var.get('blockParams'))
            var.get('exports').put('appendContextPath', var.get('appendContextPath'))
            var.put('escape', Js({'&':Js('&amp;'),'<':Js('&lt;'),'>':Js('&gt;'),'"':Js('&quot;'),"'":Js('&#x27;'),'`':Js('&#x60;'),'=':Js('&#x3D;')}))
            var.put('badChars', JsRegExp('/[&<>"\'`=]/g'))
            var.put('possible', JsRegExp('/[&<>"\'`=]/'))
            pass
            pass
            var.put('toString', var.get('Object').get('prototype').get('toString'))
            var.get('exports').put('toString', var.get('toString'))
            @Js
            def PyJs_isFunction_20_(value, this, arguments, var=var):
                var = Scope({'value':value, 'this':this, 'arguments':arguments, 'isFunction':PyJs_isFunction_20_}, var)
                var.registers(['value'])
                return PyJsStrictEq(var.get('value',throw=False).typeof(),Js('function'))
            PyJs_isFunction_20_._set_name('isFunction')
            var.put('isFunction', PyJs_isFunction_20_)
            if var.get('isFunction')(JsRegExp('/x/')):
                @Js
                def PyJs_anonymous_21_(value, this, arguments, var=var):
                    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
                    var.registers(['value'])
                    return (PyJsStrictEq(var.get('value',throw=False).typeof(),Js('function')) and PyJsStrictEq(var.get('toString').callprop('call', var.get('value')),Js('[object Function]')))
                PyJs_anonymous_21_._set_name('anonymous')
                var.get('exports').put('isFunction', var.put('isFunction', PyJs_anonymous_21_))
            var.get('exports').put('isFunction', var.get('isFunction'))
            @Js
            def PyJs_anonymous_22_(value, this, arguments, var=var):
                var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['value'])
                return (PyJsStrictEq(var.get('toString').callprop('call', var.get('value')),Js('[object Array]')) if (var.get('value') and PyJsStrictEq(var.get('value',throw=False).typeof(),Js('object'))) else Js(False))
            PyJs_anonymous_22_._set_name('anonymous')
            var.put('isArray', (var.get('Array').get('isArray') or PyJs_anonymous_22_))
            var.get('exports').put('isArray', var.get('isArray'))
            pass
            pass
            pass
            pass
            pass
            pass
        PyJs_anonymous_19_._set_name('anonymous')
        @Js
        def PyJs_anonymous_23_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'Exception', 'module', '_Object$defineProperty', 'errorProps', '__webpack_require__'])
            @Js
            def PyJsHoisted_Exception_(message, node, this, arguments, var=var):
                var = Scope({'message':message, 'node':node, 'this':this, 'arguments':arguments}, var)
                var.registers(['endLineNumber', 'tmp', 'loc', 'idx', 'column', 'endColumn', 'message', 'line', 'node'])
                var.put('loc', (var.get('node') and var.get('node').get('loc')))
                var.put('line', var.get('undefined'))
                var.put('endLineNumber', var.get('undefined'))
                var.put('column', var.get('undefined'))
                var.put('endColumn', var.get('undefined'))
                if var.get('loc'):
                    var.put('line', var.get('loc').get('start').get('line'))
                    var.put('endLineNumber', var.get('loc').get('end').get('line'))
                    var.put('column', var.get('loc').get('start').get('column'))
                    var.put('endColumn', var.get('loc').get('end').get('column'))
                    var.put('message', (((Js(' - ')+var.get('line'))+Js(':'))+var.get('column')), '+')
                var.put('tmp', var.get('Error').get('prototype').get('constructor').callprop('call', var.get(u"this"), var.get('message')))
                #for JS loop
                var.put('idx', Js(0.0))
                while (var.get('idx')<var.get('errorProps').get('length')):
                    var.get(u"this").put(var.get('errorProps').get(var.get('idx')), var.get('tmp').get(var.get('errorProps').get(var.get('idx'))))
                    # update
                    (var.put('idx',Js(var.get('idx').to_number())+Js(1))-Js(1))
                if var.get('Error').get('captureStackTrace'):
                    var.get('Error').callprop('captureStackTrace', var.get(u"this"), var.get('Exception'))
                try:
                    if var.get('loc'):
                        var.get(u"this").put('lineNumber', var.get('line'))
                        var.get(u"this").put('endLineNumber', var.get('endLineNumber'))
                        if var.get('_Object$defineProperty'):
                            var.get('Object').callprop('defineProperty', var.get(u"this"), Js('column'), Js({'value':var.get('column'),'enumerable':Js(True)}))
                            var.get('Object').callprop('defineProperty', var.get(u"this"), Js('endColumn'), Js({'value':var.get('endColumn'),'enumerable':Js(True)}))
                        else:
                            var.get(u"this").put('column', var.get('column'))
                            var.get(u"this").put('endColumn', var.get('endColumn'))
                except PyJsException as PyJsTempException:
                    PyJsHolder_6e6f70_26757802 = var.own.get('nop')
                    var.force_own_put('nop', PyExceptionToJs(PyJsTempException))
                    try:
                        pass
                    finally:
                        if PyJsHolder_6e6f70_26757802 is not None:
                            var.own['nop'] = PyJsHolder_6e6f70_26757802
                        else:
                            del var.own['nop']
                        del PyJsHolder_6e6f70_26757802
            PyJsHoisted_Exception_.func_name = 'Exception'
            var.put('Exception', PyJsHoisted_Exception_)
            Js('use strict')
            var.put('_Object$defineProperty', var.get('__webpack_require__')(Js(7.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('errorProps', Js([Js('description'), Js('fileName'), Js('lineNumber'), Js('endLineNumber'), Js('message'), Js('name'), Js('number'), Js('stack')]))
            pass
            var.get('Exception').put('prototype', var.get('Error').create())
            var.get('exports').put('default', var.get('Exception'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_23_._set_name('anonymous')
        @Js
        def PyJs_anonymous_24_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(8.0)),'__esModule':Js(True)}))
        PyJs_anonymous_24_._set_name('anonymous')
        @Js
        def PyJs_anonymous_25_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', '$', 'exports'])
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            @Js
            def PyJs_defineProperty_26_(it, key, desc, this, arguments, var=var):
                var = Scope({'it':it, 'key':key, 'desc':desc, 'this':this, 'arguments':arguments, 'defineProperty':PyJs_defineProperty_26_}, var)
                var.registers(['key', 'it', 'desc'])
                return var.get('$').callprop('setDesc', var.get('it'), var.get('key'), var.get('desc'))
            PyJs_defineProperty_26_._set_name('defineProperty')
            var.get('module').put('exports', PyJs_defineProperty_26_)
        PyJs_anonymous_25_._set_name('anonymous')
        @Js
        def PyJs_anonymous_27_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '$Object', 'exports'])
            var.put('$Object', var.get('Object'))
            def PyJs_LONG_28_(var=var):
                return var.get('module').put('exports', Js({'create':var.get('$Object').get('create'),'getProto':var.get('$Object').get('getPrototypeOf'),'isEnum':Js({}).get('propertyIsEnumerable'),'getDesc':var.get('$Object').get('getOwnPropertyDescriptor'),'setDesc':var.get('$Object').get('defineProperty'),'setDescs':var.get('$Object').get('defineProperties'),'getKeys':var.get('$Object').get('keys'),'getNames':var.get('$Object').get('getOwnPropertyNames'),'getSymbols':var.get('$Object').get('getOwnPropertySymbols'),'each':Js([]).get('forEach')}))
            PyJs_LONG_28_()
        PyJs_anonymous_27_._set_name('anonymous')
        @Js
        def PyJs_anonymous_29_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['moveHelperToHooks', '_helpersLog2', 'module', '_helpersEach2', '_helpersHelperMissing', '_interopRequireDefault', '_helpersLog', '_helpersWith2', '_helpersIf2', 'registerDefaultHelpers', '_helpersHelperMissing2', '_helpersIf', '_helpersLookup', '_helpersEach', '__webpack_require__', '_helpersWith', '_helpersLookup2', 'exports', '_helpersBlockHelperMissing2', '_helpersBlockHelperMissing'])
            @Js
            def PyJsHoisted_registerDefaultHelpers_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                var.get('_helpersBlockHelperMissing2').callprop('default', var.get('instance'))
                var.get('_helpersEach2').callprop('default', var.get('instance'))
                var.get('_helpersHelperMissing2').callprop('default', var.get('instance'))
                var.get('_helpersIf2').callprop('default', var.get('instance'))
                var.get('_helpersLog2').callprop('default', var.get('instance'))
                var.get('_helpersLookup2').callprop('default', var.get('instance'))
                var.get('_helpersWith2').callprop('default', var.get('instance'))
            PyJsHoisted_registerDefaultHelpers_.func_name = 'registerDefaultHelpers'
            var.put('registerDefaultHelpers', PyJsHoisted_registerDefaultHelpers_)
            @Js
            def PyJsHoisted_moveHelperToHooks_(instance, helperName, keepHelper, this, arguments, var=var):
                var = Scope({'instance':instance, 'helperName':helperName, 'keepHelper':keepHelper, 'this':this, 'arguments':arguments}, var)
                var.registers(['keepHelper', 'helperName', 'instance'])
                if var.get('instance').get('helpers').get(var.get('helperName')):
                    var.get('instance').get('hooks').put(var.get('helperName'), var.get('instance').get('helpers').get(var.get('helperName')))
                    if var.get('keepHelper').neg():
                        var.get('instance').get('helpers').delete(var.get('helperName'))
            PyJsHoisted_moveHelperToHooks_.func_name = 'moveHelperToHooks'
            var.put('moveHelperToHooks', PyJsHoisted_moveHelperToHooks_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('registerDefaultHelpers', var.get('registerDefaultHelpers'))
            var.get('exports').put('moveHelperToHooks', var.get('moveHelperToHooks'))
            var.put('_helpersBlockHelperMissing', var.get('__webpack_require__')(Js(11.0)))
            var.put('_helpersBlockHelperMissing2', var.get('_interopRequireDefault')(var.get('_helpersBlockHelperMissing')))
            var.put('_helpersEach', var.get('__webpack_require__')(Js(12.0)))
            var.put('_helpersEach2', var.get('_interopRequireDefault')(var.get('_helpersEach')))
            var.put('_helpersHelperMissing', var.get('__webpack_require__')(Js(65.0)))
            var.put('_helpersHelperMissing2', var.get('_interopRequireDefault')(var.get('_helpersHelperMissing')))
            var.put('_helpersIf', var.get('__webpack_require__')(Js(66.0)))
            var.put('_helpersIf2', var.get('_interopRequireDefault')(var.get('_helpersIf')))
            var.put('_helpersLog', var.get('__webpack_require__')(Js(67.0)))
            var.put('_helpersLog2', var.get('_interopRequireDefault')(var.get('_helpersLog')))
            var.put('_helpersLookup', var.get('__webpack_require__')(Js(68.0)))
            var.put('_helpersLookup2', var.get('_interopRequireDefault')(var.get('_helpersLookup')))
            var.put('_helpersWith', var.get('__webpack_require__')(Js(69.0)))
            var.put('_helpersWith2', var.get('_interopRequireDefault')(var.get('_helpersWith')))
            pass
            pass
        PyJs_anonymous_29_._set_name('anonymous')
        @Js
        def PyJs_anonymous_30_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports', '__webpack_require__', '_utils'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            @Js
            def PyJs_anonymous_31_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_32_(context, options, this, arguments, var=var):
                    var = Scope({'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['context', 'fn', 'data', 'inverse', 'options'])
                    var.put('inverse', var.get('options').get('inverse'))
                    var.put('fn', var.get('options').get('fn'))
                    if PyJsStrictEq(var.get('context'),Js(True)):
                        return var.get('fn')(var.get(u"this"))
                    else:
                        if (PyJsStrictEq(var.get('context'),Js(False)) or (var.get('context')==var.get(u"null"))):
                            return var.get('inverse')(var.get(u"this"))
                        else:
                            if var.get('_utils').callprop('isArray', var.get('context')):
                                if (var.get('context').get('length')>Js(0.0)):
                                    if var.get('options').get('ids'):
                                        var.get('options').put('ids', Js([var.get('options').get('name')]))
                                    return var.get('instance').get('helpers').callprop('each', var.get('context'), var.get('options'))
                                else:
                                    return var.get('inverse')(var.get(u"this"))
                            else:
                                if (var.get('options').get('data') and var.get('options').get('ids')):
                                    var.put('data', var.get('_utils').callprop('createFrame', var.get('options').get('data')))
                                    var.get('data').put('contextPath', var.get('_utils').callprop('appendContextPath', var.get('options').get('data').get('contextPath'), var.get('options').get('name')))
                                    var.put('options', Js({'data':var.get('data')}))
                                return var.get('fn')(var.get('context'), var.get('options'))
                PyJs_anonymous_32_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('blockHelperMissing'), PyJs_anonymous_32_)
            PyJs_anonymous_31_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_31_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_30_._set_name('anonymous')
        @Js
        def PyJs_anonymous_33_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_interopRequireDefault', '_Symbol$iterator', 'exports', '_exception2', '_getIterator', 'module', '_exception', '_Object$keys', '_utils', '_Symbol', '__webpack_require__'])
            Js('use strict')
            var.put('_Symbol', var.get('__webpack_require__')(Js(13.0)).get('default'))
            var.put('_Symbol$iterator', var.get('__webpack_require__')(Js(43.0)).get('default'))
            var.put('_getIterator', var.get('__webpack_require__')(Js(55.0)).get('default'))
            var.put('_Object$keys', var.get('__webpack_require__')(Js(60.0)).get('default'))
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            @Js
            def PyJs_anonymous_34_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_35_(context, options, this, arguments, var=var):
                    var = Scope({'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['context', 'execIteration', 'j', 'i', 'contextPath', 'fn', 'iterator', 'inverse', 'newContext', 'it', 'options', 'ret', 'data'])
                    @Js
                    def PyJsHoisted_execIteration_(field, index, last, this, arguments, var=var):
                        var = Scope({'field':field, 'index':index, 'last':last, 'this':this, 'arguments':arguments}, var)
                        var.registers(['last', 'field', 'index'])
                        if var.get('data'):
                            var.get('data').put('key', var.get('field'))
                            var.get('data').put('index', var.get('index'))
                            var.get('data').put('first', PyJsStrictEq(var.get('index'),Js(0.0)))
                            var.get('data').put('last', var.get('last').neg().neg())
                            if var.get('contextPath'):
                                var.get('data').put('contextPath', (var.get('contextPath')+var.get('field')))
                        var.put('ret', (var.get('ret')+var.get('fn')(var.get('context').get(var.get('field')), Js({'data':var.get('data'),'blockParams':var.get('_utils').callprop('blockParams', Js([var.get('context').get(var.get('field')), var.get('field')]), Js([(var.get('contextPath')+var.get('field')), var.get(u"null")]))}))))
                    PyJsHoisted_execIteration_.func_name = 'execIteration'
                    var.put('execIteration', PyJsHoisted_execIteration_)
                    if var.get('options').neg():
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('Must pass iterator to #each')))
                        raise PyJsTempException
                    var.put('fn', var.get('options').get('fn'))
                    var.put('inverse', var.get('options').get('inverse'))
                    var.put('i', Js(0.0))
                    var.put('ret', Js(''))
                    var.put('data', var.get('undefined'))
                    var.put('contextPath', var.get('undefined'))
                    if (var.get('options').get('data') and var.get('options').get('ids')):
                        var.put('contextPath', (var.get('_utils').callprop('appendContextPath', var.get('options').get('data').get('contextPath'), var.get('options').get('ids').get('0'))+Js('.')))
                    if var.get('_utils').callprop('isFunction', var.get('context')):
                        var.put('context', var.get('context').callprop('call', var.get(u"this")))
                    if var.get('options').get('data'):
                        var.put('data', var.get('_utils').callprop('createFrame', var.get('options').get('data')))
                    pass
                    if (var.get('context') and PyJsStrictEq(var.get('context',throw=False).typeof(),Js('object'))):
                        if var.get('_utils').callprop('isArray', var.get('context')):
                            #for JS loop
                            var.put('j', var.get('context').get('length'))
                            while (var.get('i')<var.get('j')):
                                if var.get('context').contains(var.get('i')):
                                    var.get('execIteration')(var.get('i'), var.get('i'), PyJsStrictEq(var.get('i'),(var.get('context').get('length')-Js(1.0))))
                                # update
                                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                        else:
                            if (PyJsStrictEq(var.get('_Symbol',throw=False).typeof(),Js('function')) and var.get('context').get(var.get('_Symbol$iterator'))):
                                var.put('newContext', Js([]))
                                var.put('iterator', var.get('_getIterator')(var.get('context')))
                                #for JS loop
                                var.put('it', var.get('iterator').callprop('next'))
                                while var.get('it').get('done').neg():
                                    var.get('newContext').callprop('push', var.get('it').get('value'))
                                    # update
                                    var.put('it', var.get('iterator').callprop('next'))
                                var.put('context', var.get('newContext'))
                                #for JS loop
                                var.put('j', var.get('context').get('length'))
                                while (var.get('i')<var.get('j')):
                                    var.get('execIteration')(var.get('i'), var.get('i'), PyJsStrictEq(var.get('i'),(var.get('context').get('length')-Js(1.0))))
                                    # update
                                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                            else:
                                @Js
                                def PyJs_anonymous_36_(this, arguments, var=var):
                                    var = Scope({'this':this, 'arguments':arguments}, var)
                                    var.registers(['priorKey'])
                                    var.put('priorKey', var.get('undefined'))
                                    @Js
                                    def PyJs_anonymous_37_(key, this, arguments, var=var):
                                        var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
                                        var.registers(['key'])
                                        if PyJsStrictNeq(var.get('priorKey'),var.get('undefined')):
                                            var.get('execIteration')(var.get('priorKey'), (var.get('i')-Js(1.0)))
                                        var.put('priorKey', var.get('key'))
                                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                                    PyJs_anonymous_37_._set_name('anonymous')
                                    var.get('_Object$keys')(var.get('context')).callprop('forEach', PyJs_anonymous_37_)
                                    if PyJsStrictNeq(var.get('priorKey'),var.get('undefined')):
                                        var.get('execIteration')(var.get('priorKey'), (var.get('i')-Js(1.0)), Js(True))
                                PyJs_anonymous_36_._set_name('anonymous')
                                PyJs_anonymous_36_()
                    if PyJsStrictEq(var.get('i'),Js(0.0)):
                        var.put('ret', var.get('inverse')(var.get(u"this")))
                    return var.get('ret')
                PyJs_anonymous_35_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('each'), PyJs_anonymous_35_)
            PyJs_anonymous_34_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_34_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_33_._set_name('anonymous')
        @Js
        def PyJs_anonymous_38_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(14.0)),'__esModule':Js(True)}))
        PyJs_anonymous_38_._set_name('anonymous')
        @Js
        def PyJs_anonymous_39_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('__webpack_require__')(Js(15.0))
            var.get('__webpack_require__')(Js(42.0))
            var.get('module').put('exports', var.get('__webpack_require__')(Js(21.0)).get('Symbol'))
        PyJs_anonymous_39_._set_name('anonymous')
        @Js
        def PyJs_anonymous_40_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['shared', 'global', 'keyOf', 'symbolStatics', '$defineProperties', 'HIDDEN', '$getOwnPropertyDescriptor', '$export', 'DESCRIPTORS', 'module', 'anObject', 'getNames', 'SymbolRegistry', '$stringify', 'AllSymbols', '$getOwnPropertySymbols', 'setToStringTag', '$defineProperty', '$create', '$Symbol', '$names', 'uid', 'isArray', 'toIObject', 'redefine', 'wrap', 'has', '$propertyIsEnumerable', '__webpack_require__', '$', '_create', 'setSymbolDesc', 'setDesc', 'getDesc', 'setter', '$getOwnPropertyNames', 'enumKeys', '$fails', 'isSymbol', 'exports', '$JSON', 'createDesc', 'buggyJSON', 'isEnum', 'ObjectProto', 'wks', '_stringify', 'useNative'])
            Js('use strict')
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            var.put('global', var.get('__webpack_require__')(Js(16.0)))
            var.put('has', var.get('__webpack_require__')(Js(17.0)))
            var.put('DESCRIPTORS', var.get('__webpack_require__')(Js(18.0)))
            var.put('$export', var.get('__webpack_require__')(Js(20.0)))
            var.put('redefine', var.get('__webpack_require__')(Js(24.0)))
            var.put('$fails', var.get('__webpack_require__')(Js(19.0)))
            var.put('shared', var.get('__webpack_require__')(Js(27.0)))
            var.put('setToStringTag', var.get('__webpack_require__')(Js(28.0)))
            var.put('uid', var.get('__webpack_require__')(Js(30.0)))
            var.put('wks', var.get('__webpack_require__')(Js(29.0)))
            var.put('keyOf', var.get('__webpack_require__')(Js(31.0)))
            var.put('$names', var.get('__webpack_require__')(Js(36.0)))
            var.put('enumKeys', var.get('__webpack_require__')(Js(37.0)))
            var.put('isArray', var.get('__webpack_require__')(Js(38.0)))
            var.put('anObject', var.get('__webpack_require__')(Js(39.0)))
            var.put('toIObject', var.get('__webpack_require__')(Js(32.0)))
            var.put('createDesc', var.get('__webpack_require__')(Js(26.0)))
            var.put('getDesc', var.get('$').get('getDesc'))
            var.put('setDesc', var.get('$').get('setDesc'))
            var.put('_create', var.get('$').get('create'))
            var.put('getNames', var.get('$names').get('get'))
            var.put('$Symbol', var.get('global').get('Symbol'))
            var.put('$JSON', var.get('global').get('JSON'))
            var.put('_stringify', (var.get('$JSON') and var.get('$JSON').get('stringify')))
            var.put('setter', Js(False))
            var.put('HIDDEN', var.get('wks')(Js('_hidden')))
            var.put('isEnum', var.get('$').get('isEnum'))
            var.put('SymbolRegistry', var.get('shared')(Js('symbol-registry')))
            var.put('AllSymbols', var.get('shared')(Js('symbols')))
            var.put('useNative', (var.get('$Symbol',throw=False).typeof()==Js('function')))
            var.put('ObjectProto', var.get('Object').get('prototype'))
            @Js
            def PyJs_anonymous_41_(it, key, D, this, arguments, var=var):
                var = Scope({'it':it, 'key':key, 'D':D, 'this':this, 'arguments':arguments}, var)
                var.registers(['protoDesc', 'it', 'D', 'key'])
                var.put('protoDesc', var.get('getDesc')(var.get('ObjectProto'), var.get('key')))
                if var.get('protoDesc'):
                    var.get('ObjectProto').delete(var.get('key'))
                var.get('setDesc')(var.get('it'), var.get('key'), var.get('D'))
                if (var.get('protoDesc') and PyJsStrictNeq(var.get('it'),var.get('ObjectProto'))):
                    var.get('setDesc')(var.get('ObjectProto'), var.get('key'), var.get('protoDesc'))
            PyJs_anonymous_41_._set_name('anonymous')
            @Js
            def PyJs_anonymous_42_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                @Js
                def PyJs_anonymous_43_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    return var.get('setDesc')(var.get(u"this"), Js('a'), Js({'value':Js(7.0)})).get('a')
                PyJs_anonymous_43_._set_name('anonymous')
                return (var.get('_create')(var.get('setDesc')(Js({}), Js('a'), Js({'get':PyJs_anonymous_43_}))).get('a')!=Js(7.0))
            PyJs_anonymous_42_._set_name('anonymous')
            var.put('setSymbolDesc', (PyJs_anonymous_41_ if (var.get('DESCRIPTORS') and var.get('$fails')(PyJs_anonymous_42_)) else var.get('setDesc')))
            @Js
            def PyJs_anonymous_44_(tag, this, arguments, var=var):
                var = Scope({'tag':tag, 'this':this, 'arguments':arguments}, var)
                var.registers(['tag', 'sym'])
                var.put('sym', var.get('AllSymbols').put(var.get('tag'), var.get('_create')(var.get('$Symbol').get('prototype'))))
                var.get('sym').put('_k', var.get('tag'))
                @Js
                def PyJs_anonymous_45_(value, this, arguments, var=var):
                    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
                    var.registers(['value'])
                    if (var.get('has')(var.get(u"this"), var.get('HIDDEN')) and var.get('has')(var.get(u"this").get(var.get('HIDDEN')), var.get('tag'))):
                        var.get(u"this").get(var.get('HIDDEN')).put(var.get('tag'), Js(False))
                    var.get('setSymbolDesc')(var.get(u"this"), var.get('tag'), var.get('createDesc')(Js(1.0), var.get('value')))
                PyJs_anonymous_45_._set_name('anonymous')
                ((var.get('DESCRIPTORS') and var.get('setter')) and var.get('setSymbolDesc')(var.get('ObjectProto'), var.get('tag'), Js({'configurable':Js(True),'set':PyJs_anonymous_45_})))
                return var.get('sym')
            PyJs_anonymous_44_._set_name('anonymous')
            var.put('wrap', PyJs_anonymous_44_)
            @Js
            def PyJs_anonymous_46_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return (var.get('it',throw=False).typeof()==Js('symbol'))
            PyJs_anonymous_46_._set_name('anonymous')
            var.put('isSymbol', PyJs_anonymous_46_)
            @Js
            def PyJs_defineProperty_47_(it, key, D, this, arguments, var=var):
                var = Scope({'it':it, 'key':key, 'D':D, 'this':this, 'arguments':arguments, 'defineProperty':PyJs_defineProperty_47_}, var)
                var.registers(['key', 'it', 'D'])
                if (var.get('D') and var.get('has')(var.get('AllSymbols'), var.get('key'))):
                    if var.get('D').get('enumerable').neg():
                        if var.get('has')(var.get('it'), var.get('HIDDEN')).neg():
                            var.get('setDesc')(var.get('it'), var.get('HIDDEN'), var.get('createDesc')(Js(1.0), Js({})))
                        var.get('it').get(var.get('HIDDEN')).put(var.get('key'), Js(True))
                    else:
                        if (var.get('has')(var.get('it'), var.get('HIDDEN')) and var.get('it').get(var.get('HIDDEN')).get(var.get('key'))):
                            var.get('it').get(var.get('HIDDEN')).put(var.get('key'), Js(False))
                        var.put('D', var.get('_create')(var.get('D'), Js({'enumerable':var.get('createDesc')(Js(0.0), Js(False))})))
                    return var.get('setSymbolDesc')(var.get('it'), var.get('key'), var.get('D'))
                return var.get('setDesc')(var.get('it'), var.get('key'), var.get('D'))
            PyJs_defineProperty_47_._set_name('defineProperty')
            var.put('$defineProperty', PyJs_defineProperty_47_)
            @Js
            def PyJs_defineProperties_48_(it, P, this, arguments, var=var):
                var = Scope({'it':it, 'P':P, 'this':this, 'arguments':arguments, 'defineProperties':PyJs_defineProperties_48_}, var)
                var.registers(['keys', 'l', 'i', 'P', 'key', 'it'])
                var.get('anObject')(var.get('it'))
                var.put('keys', var.get('enumKeys')(var.put('P', var.get('toIObject')(var.get('P')))))
                var.put('i', Js(0.0))
                var.put('l', var.get('keys').get('length'))
                while (var.get('l')>var.get('i')):
                    var.get('$defineProperty')(var.get('it'), var.put('key', var.get('keys').get((var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1)))), var.get('P').get(var.get('key')))
                return var.get('it')
            PyJs_defineProperties_48_._set_name('defineProperties')
            var.put('$defineProperties', PyJs_defineProperties_48_)
            @Js
            def PyJs_create_49_(it, P, this, arguments, var=var):
                var = Scope({'it':it, 'P':P, 'this':this, 'arguments':arguments, 'create':PyJs_create_49_}, var)
                var.registers(['it', 'P'])
                return (var.get('_create')(var.get('it')) if PyJsStrictEq(var.get('P'),var.get('undefined')) else var.get('$defineProperties')(var.get('_create')(var.get('it')), var.get('P')))
            PyJs_create_49_._set_name('create')
            var.put('$create', PyJs_create_49_)
            @Js
            def PyJs_propertyIsEnumerable_50_(key, this, arguments, var=var):
                var = Scope({'key':key, 'this':this, 'arguments':arguments, 'propertyIsEnumerable':PyJs_propertyIsEnumerable_50_}, var)
                var.registers(['key', 'E'])
                var.put('E', var.get('isEnum').callprop('call', var.get(u"this"), var.get('key')))
                return (var.get('E') if (((var.get('E') or var.get('has')(var.get(u"this"), var.get('key')).neg()) or var.get('has')(var.get('AllSymbols'), var.get('key')).neg()) or (var.get('has')(var.get(u"this"), var.get('HIDDEN')) and var.get(u"this").get(var.get('HIDDEN')).get(var.get('key')))) else Js(True))
            PyJs_propertyIsEnumerable_50_._set_name('propertyIsEnumerable')
            var.put('$propertyIsEnumerable', PyJs_propertyIsEnumerable_50_)
            @Js
            def PyJs_getOwnPropertyDescriptor_51_(it, key, this, arguments, var=var):
                var = Scope({'it':it, 'key':key, 'this':this, 'arguments':arguments, 'getOwnPropertyDescriptor':PyJs_getOwnPropertyDescriptor_51_}, var)
                var.registers(['key', 'it', 'D'])
                var.put('D', var.get('getDesc')(var.put('it', var.get('toIObject')(var.get('it'))), var.get('key')))
                if ((var.get('D') and var.get('has')(var.get('AllSymbols'), var.get('key'))) and (var.get('has')(var.get('it'), var.get('HIDDEN')) and var.get('it').get(var.get('HIDDEN')).get(var.get('key'))).neg()):
                    var.get('D').put('enumerable', Js(True))
                return var.get('D')
            PyJs_getOwnPropertyDescriptor_51_._set_name('getOwnPropertyDescriptor')
            var.put('$getOwnPropertyDescriptor', PyJs_getOwnPropertyDescriptor_51_)
            @Js
            def PyJs_getOwnPropertyNames_52_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments, 'getOwnPropertyNames':PyJs_getOwnPropertyNames_52_}, var)
                var.registers(['i', 'key', 'it', 'names', 'result'])
                var.put('names', var.get('getNames')(var.get('toIObject')(var.get('it'))))
                var.put('result', Js([]))
                var.put('i', Js(0.0))
                while (var.get('names').get('length')>var.get('i')):
                    if (var.get('has')(var.get('AllSymbols'), var.put('key', var.get('names').get((var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))))).neg() and (var.get('key')!=var.get('HIDDEN'))):
                        var.get('result').callprop('push', var.get('key'))
                return var.get('result')
            PyJs_getOwnPropertyNames_52_._set_name('getOwnPropertyNames')
            var.put('$getOwnPropertyNames', PyJs_getOwnPropertyNames_52_)
            @Js
            def PyJs_getOwnPropertySymbols_53_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments, 'getOwnPropertySymbols':PyJs_getOwnPropertySymbols_53_}, var)
                var.registers(['i', 'key', 'it', 'names', 'result'])
                var.put('names', var.get('getNames')(var.get('toIObject')(var.get('it'))))
                var.put('result', Js([]))
                var.put('i', Js(0.0))
                while (var.get('names').get('length')>var.get('i')):
                    if var.get('has')(var.get('AllSymbols'), var.put('key', var.get('names').get((var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))))):
                        var.get('result').callprop('push', var.get('AllSymbols').get(var.get('key')))
                return var.get('result')
            PyJs_getOwnPropertySymbols_53_._set_name('getOwnPropertySymbols')
            var.put('$getOwnPropertySymbols', PyJs_getOwnPropertySymbols_53_)
            @Js
            def PyJs_stringify_54_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments, 'stringify':PyJs_stringify_54_}, var)
                var.registers(['$$', 'replacer', 'args', 'i', 'it', '$replacer'])
                if (PyJsStrictEq(var.get('it'),var.get('undefined')) or var.get('isSymbol')(var.get('it'))):
                    return var.get('undefined')
                var.put('args', Js([var.get('it')]))
                var.put('i', Js(1.0))
                var.put('$$', var.get('arguments'))
                while (var.get('$$').get('length')>var.get('i')):
                    var.get('args').callprop('push', var.get('$$').get((var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))))
                var.put('replacer', var.get('args').get('1'))
                if (var.get('replacer',throw=False).typeof()==Js('function')):
                    var.put('$replacer', var.get('replacer'))
                if (var.get('$replacer') or var.get('isArray')(var.get('replacer')).neg()):
                    @Js
                    def PyJs_anonymous_55_(key, value, this, arguments, var=var):
                        var = Scope({'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
                        var.registers(['key', 'value'])
                        if var.get('$replacer'):
                            var.put('value', var.get('$replacer').callprop('call', var.get(u"this"), var.get('key'), var.get('value')))
                        if var.get('isSymbol')(var.get('value')).neg():
                            return var.get('value')
                    PyJs_anonymous_55_._set_name('anonymous')
                    var.put('replacer', PyJs_anonymous_55_)
                var.get('args').put('1', var.get('replacer'))
                return var.get('_stringify').callprop('apply', var.get('$JSON'), var.get('args'))
            PyJs_stringify_54_._set_name('stringify')
            var.put('$stringify', PyJs_stringify_54_)
            @Js
            def PyJs_anonymous_56_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['S'])
                var.put('S', var.get('$Symbol')())
                return (((var.get('_stringify')(Js([var.get('S')]))!=Js('[null]')) or (var.get('_stringify')(Js({'a':var.get('S')}))!=Js('{}'))) or (var.get('_stringify')(var.get('Object')(var.get('S')))!=Js('{}')))
            PyJs_anonymous_56_._set_name('anonymous')
            var.put('buggyJSON', var.get('$fails')(PyJs_anonymous_56_))
            if var.get('useNative').neg():
                @Js
                def PyJs_Symbol_57_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'Symbol':PyJs_Symbol_57_}, var)
                    var.registers([])
                    if var.get('isSymbol')(var.get(u"this")):
                        PyJsTempException = JsToPyException(var.get('TypeError')(Js('Symbol is not a constructor')))
                        raise PyJsTempException
                    return var.get('wrap')(var.get('uid')((var.get('arguments').get('0') if (var.get('arguments').get('length')>Js(0.0)) else var.get('undefined'))))
                PyJs_Symbol_57_._set_name('Symbol')
                var.put('$Symbol', PyJs_Symbol_57_)
                @Js
                def PyJs_toString_58_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_58_}, var)
                    var.registers([])
                    return var.get(u"this").get('_k')
                PyJs_toString_58_._set_name('toString')
                var.get('redefine')(var.get('$Symbol').get('prototype'), Js('toString'), PyJs_toString_58_)
                @Js
                def PyJs_anonymous_59_(it, this, arguments, var=var):
                    var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                    var.registers(['it'])
                    return var.get('it').instanceof(var.get('$Symbol'))
                PyJs_anonymous_59_._set_name('anonymous')
                var.put('isSymbol', PyJs_anonymous_59_)
                var.get('$').put('create', var.get('$create'))
                var.get('$').put('isEnum', var.get('$propertyIsEnumerable'))
                var.get('$').put('getDesc', var.get('$getOwnPropertyDescriptor'))
                var.get('$').put('setDesc', var.get('$defineProperty'))
                var.get('$').put('setDescs', var.get('$defineProperties'))
                var.get('$').put('getNames', var.get('$names').put('get', var.get('$getOwnPropertyNames')))
                var.get('$').put('getSymbols', var.get('$getOwnPropertySymbols'))
                if (var.get('DESCRIPTORS') and var.get('__webpack_require__')(Js(41.0)).neg()):
                    var.get('redefine')(var.get('ObjectProto'), Js('propertyIsEnumerable'), var.get('$propertyIsEnumerable'), Js(True))
            @Js
            def PyJs_anonymous_60_(key, this, arguments, var=var):
                var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
                var.registers(['key'])
                return (var.get('SymbolRegistry').get(var.get('key')) if var.get('has')(var.get('SymbolRegistry'), var.put('key', Js(''), '+')) else var.get('SymbolRegistry').put(var.get('key'), var.get('$Symbol')(var.get('key'))))
            PyJs_anonymous_60_._set_name('anonymous')
            @Js
            def PyJs_keyFor_61_(key, this, arguments, var=var):
                var = Scope({'key':key, 'this':this, 'arguments':arguments, 'keyFor':PyJs_keyFor_61_}, var)
                var.registers(['key'])
                return var.get('keyOf')(var.get('SymbolRegistry'), var.get('key'))
            PyJs_keyFor_61_._set_name('keyFor')
            @Js
            def PyJs_anonymous_62_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.put('setter', Js(True))
            PyJs_anonymous_62_._set_name('anonymous')
            @Js
            def PyJs_anonymous_63_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.put('setter', Js(False))
            PyJs_anonymous_63_._set_name('anonymous')
            var.put('symbolStatics', Js({'for':PyJs_anonymous_60_,'keyFor':PyJs_keyFor_61_,'useSetter':PyJs_anonymous_62_,'useSimple':PyJs_anonymous_63_}))
            @Js
            def PyJs_anonymous_64_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it', 'sym'])
                var.put('sym', var.get('wks')(var.get('it')))
                var.get('symbolStatics').put(var.get('it'), (var.get('sym') if var.get('useNative') else var.get('wrap')(var.get('sym'))))
            PyJs_anonymous_64_._set_name('anonymous')
            var.get('$').get('each').callprop('call', (Js('hasInstance,isConcatSpreadable,iterator,match,replace,search,')+Js('species,split,toPrimitive,toStringTag,unscopables')).callprop('split', Js(',')), PyJs_anonymous_64_)
            var.put('setter', Js(True))
            var.get('$export')((var.get('$export').get('G')+var.get('$export').get('W')), Js({'Symbol':var.get('$Symbol')}))
            var.get('$export')(var.get('$export').get('S'), Js('Symbol'), var.get('symbolStatics'))
            def PyJs_LONG_65_(var=var):
                return var.get('$export')((var.get('$export').get('S')+(var.get('$export').get('F')*var.get('useNative').neg())), Js('Object'), Js({'create':var.get('$create'),'defineProperty':var.get('$defineProperty'),'defineProperties':var.get('$defineProperties'),'getOwnPropertyDescriptor':var.get('$getOwnPropertyDescriptor'),'getOwnPropertyNames':var.get('$getOwnPropertyNames'),'getOwnPropertySymbols':var.get('$getOwnPropertySymbols')}))
            PyJs_LONG_65_()
            (var.get('$JSON') and var.get('$export')((var.get('$export').get('S')+(var.get('$export').get('F')*(var.get('useNative').neg() or var.get('buggyJSON')))), Js('JSON'), Js({'stringify':var.get('$stringify')})))
            var.get('setToStringTag')(var.get('$Symbol'), Js('Symbol'))
            var.get('setToStringTag')(var.get('Math'), Js('Math'), Js(True))
            var.get('setToStringTag')(var.get('global').get('JSON'), Js('JSON'), Js(True))
        PyJs_anonymous_40_._set_name('anonymous')
        @Js
        def PyJs_anonymous_66_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'global', 'exports'])
            var.put('global', var.get('module').put('exports', (var.get('window') if ((var.get('window',throw=False).typeof()!=Js('undefined')) and (var.get('window').get('Math')==var.get('Math'))) else (var.get('self') if ((var.get('self',throw=False).typeof()!=Js('undefined')) and (var.get('self').get('Math')==var.get('Math'))) else var.get('Function')(Js('return this'))()))))
            if (var.get('__g',throw=False).typeof()==Js('number')):
                var.put('__g', var.get('global'))
        PyJs_anonymous_66_._set_name('anonymous')
        @Js
        def PyJs_anonymous_67_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'hasOwnProperty', 'exports'])
            var.put('hasOwnProperty', Js({}).get('hasOwnProperty'))
            @Js
            def PyJs_anonymous_68_(it, key, this, arguments, var=var):
                var = Scope({'it':it, 'key':key, 'this':this, 'arguments':arguments}, var)
                var.registers(['key', 'it'])
                return var.get('hasOwnProperty').callprop('call', var.get('it'), var.get('key'))
            PyJs_anonymous_68_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_68_)
        PyJs_anonymous_67_._set_name('anonymous')
        @Js
        def PyJs_anonymous_69_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            @Js
            def PyJs_anonymous_70_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                @Js
                def PyJs_anonymous_71_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    return Js(7.0)
                PyJs_anonymous_71_._set_name('anonymous')
                return (var.get('Object').callprop('defineProperty', Js({}), Js('a'), Js({'get':PyJs_anonymous_71_})).get('a')!=Js(7.0))
            PyJs_anonymous_70_._set_name('anonymous')
            var.get('module').put('exports', var.get('__webpack_require__')(Js(19.0))(PyJs_anonymous_70_).neg())
        PyJs_anonymous_69_._set_name('anonymous')
        @Js
        def PyJs_anonymous_72_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_73_(exec, this, arguments, var=var):
                var = Scope({'exec':exec, 'this':this, 'arguments':arguments}, var)
                var.registers(['exec'])
                try:
                    return var.get('exec')().neg().neg()
                except PyJsException as PyJsTempException:
                    PyJsHolder_65_70830041 = var.own.get('e')
                    var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                    try:
                        return Js(True)
                    finally:
                        if PyJsHolder_65_70830041 is not None:
                            var.own['e'] = PyJsHolder_65_70830041
                        else:
                            del var.own['e']
                        del PyJsHolder_65_70830041
            PyJs_anonymous_73_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_73_)
        PyJs_anonymous_72_._set_name('anonymous')
        @Js
        def PyJs_anonymous_74_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['PROTOTYPE', 'global', 'ctx', 'exports', 'core', '$export', 'module', '__webpack_require__'])
            var.put('global', var.get('__webpack_require__')(Js(16.0)))
            var.put('core', var.get('__webpack_require__')(Js(21.0)))
            var.put('ctx', var.get('__webpack_require__')(Js(22.0)))
            var.put('PROTOTYPE', Js('prototype'))
            @Js
            def PyJs_anonymous_75_(type, name, source, this, arguments, var=var):
                var = Scope({'type':type, 'name':name, 'source':source, 'this':this, 'arguments':arguments}, var)
                var.registers(['key', 'IS_PROTO', 'exports', 'IS_BIND', 'out', 'type', 'IS_WRAP', 'IS_FORCED', 'name', 'IS_STATIC', 'IS_GLOBAL', 'own', 'target', 'source'])
                var.put('IS_FORCED', (var.get('type')&var.get('$export').get('F')))
                var.put('IS_GLOBAL', (var.get('type')&var.get('$export').get('G')))
                var.put('IS_STATIC', (var.get('type')&var.get('$export').get('S')))
                var.put('IS_PROTO', (var.get('type')&var.get('$export').get('P')))
                var.put('IS_BIND', (var.get('type')&var.get('$export').get('B')))
                var.put('IS_WRAP', (var.get('type')&var.get('$export').get('W')))
                var.put('exports', (var.get('core') if var.get('IS_GLOBAL') else (var.get('core').get(var.get('name')) or var.get('core').put(var.get('name'), Js({})))))
                var.put('target', (var.get('global') if var.get('IS_GLOBAL') else (var.get('global').get(var.get('name')) if var.get('IS_STATIC') else (var.get('global').get(var.get('name')) or Js({})).get(var.get('PROTOTYPE')))))
                if var.get('IS_GLOBAL'):
                    var.put('source', var.get('name'))
                for PyJsTemp in var.get('source'):
                    var.put('key', PyJsTemp)
                    var.put('own', ((var.get('IS_FORCED').neg() and var.get('target')) and var.get('target').contains(var.get('key'))))
                    if (var.get('own') and var.get('exports').contains(var.get('key'))):
                        continue
                    var.put('out', (var.get('target').get(var.get('key')) if var.get('own') else var.get('source').get(var.get('key'))))
                    def PyJs_LONG_78_(var=var):
                        @Js
                        def PyJs_anonymous_76_(C, this, arguments, var=var):
                            var = Scope({'C':C, 'this':this, 'arguments':arguments}, var)
                            var.registers(['C', 'F'])
                            @Js
                            def PyJs_anonymous_77_(param, this, arguments, var=var):
                                var = Scope({'param':param, 'this':this, 'arguments':arguments}, var)
                                var.registers(['param'])
                                return (var.get('C').create(var.get('param')) if var.get(u"this").instanceof(var.get('C')) else var.get('C')(var.get('param')))
                            PyJs_anonymous_77_._set_name('anonymous')
                            var.put('F', PyJs_anonymous_77_)
                            var.get('F').put(var.get('PROTOTYPE'), var.get('C').get(var.get('PROTOTYPE')))
                            return var.get('F')
                        PyJs_anonymous_76_._set_name('anonymous')
                        return (var.get('source').get(var.get('key')) if (var.get('IS_GLOBAL') and (var.get('target').get(var.get('key')).typeof()!=Js('function'))) else (var.get('ctx')(var.get('out'), var.get('global')) if (var.get('IS_BIND') and var.get('own')) else (PyJs_anonymous_76_(var.get('out')) if (var.get('IS_WRAP') and (var.get('target').get(var.get('key'))==var.get('out'))) else (var.get('ctx')(var.get('Function').get('call'), var.get('out')) if (var.get('IS_PROTO') and (var.get('out',throw=False).typeof()==Js('function'))) else var.get('out')))))
                    var.get('exports').put(var.get('key'), PyJs_LONG_78_())
                    if var.get('IS_PROTO'):
                        (var.get('exports').get(var.get('PROTOTYPE')) or var.get('exports').put(var.get('PROTOTYPE'), Js({}))).put(var.get('key'), var.get('out'))
            PyJs_anonymous_75_._set_name('anonymous')
            var.put('$export', PyJs_anonymous_75_)
            var.get('$export').put('F', Js(1.0))
            var.get('$export').put('G', Js(2.0))
            var.get('$export').put('S', Js(4.0))
            var.get('$export').put('P', Js(8.0))
            var.get('$export').put('B', Js(16.0))
            var.get('$export').put('W', Js(32.0))
            var.get('module').put('exports', var.get('$export'))
        PyJs_anonymous_74_._set_name('anonymous')
        @Js
        def PyJs_anonymous_79_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'core', 'exports'])
            var.put('core', var.get('module').put('exports', Js({'version':Js('1.2.6')})))
            if (var.get('__e',throw=False).typeof()==Js('number')):
                var.put('__e', var.get('core'))
        PyJs_anonymous_79_._set_name('anonymous')
        @Js
        def PyJs_anonymous_80_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'aFunction', 'exports'])
            var.put('aFunction', var.get('__webpack_require__')(Js(23.0)))
            @Js
            def PyJs_anonymous_81_(fn, that, length, this, arguments, var=var):
                var = Scope({'fn':fn, 'that':that, 'length':length, 'this':this, 'arguments':arguments}, var)
                var.registers(['length', 'that', 'fn'])
                var.get('aFunction')(var.get('fn'))
                if PyJsStrictEq(var.get('that'),var.get('undefined')):
                    return var.get('fn')
                while 1:
                    SWITCHED = False
                    CONDITION = (var.get('length'))
                    if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
                        SWITCHED = True
                        @Js
                        def PyJs_anonymous_82_(a, this, arguments, var=var):
                            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
                            var.registers(['a'])
                            return var.get('fn').callprop('call', var.get('that'), var.get('a'))
                        PyJs_anonymous_82_._set_name('anonymous')
                        return PyJs_anonymous_82_
                    if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
                        SWITCHED = True
                        @Js
                        def PyJs_anonymous_83_(a, b, this, arguments, var=var):
                            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
                            var.registers(['a', 'b'])
                            return var.get('fn').callprop('call', var.get('that'), var.get('a'), var.get('b'))
                        PyJs_anonymous_83_._set_name('anonymous')
                        return PyJs_anonymous_83_
                    if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
                        SWITCHED = True
                        @Js
                        def PyJs_anonymous_84_(a, b, c, this, arguments, var=var):
                            var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
                            var.registers(['c', 'a', 'b'])
                            return var.get('fn').callprop('call', var.get('that'), var.get('a'), var.get('b'), var.get('c'))
                        PyJs_anonymous_84_._set_name('anonymous')
                        return PyJs_anonymous_84_
                    SWITCHED = True
                    break
                @Js
                def PyJs_anonymous_85_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    return var.get('fn').callprop('apply', var.get('that'), var.get('arguments'))
                PyJs_anonymous_85_._set_name('anonymous')
                return PyJs_anonymous_85_
            PyJs_anonymous_81_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_81_)
        PyJs_anonymous_80_._set_name('anonymous')
        @Js
        def PyJs_anonymous_86_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_87_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                if (var.get('it',throw=False).typeof()!=Js('function')):
                    PyJsTempException = JsToPyException(var.get('TypeError')((var.get('it')+Js(' is not a function!'))))
                    raise PyJsTempException
                return var.get('it')
            PyJs_anonymous_87_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_87_)
        PyJs_anonymous_86_._set_name('anonymous')
        @Js
        def PyJs_anonymous_88_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', var.get('__webpack_require__')(Js(25.0)))
        PyJs_anonymous_88_._set_name('anonymous')
        @Js
        def PyJs_anonymous_89_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'module', 'createDesc', '__webpack_require__', '$'])
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            var.put('createDesc', var.get('__webpack_require__')(Js(26.0)))
            @Js
            def PyJs_anonymous_90_(object, key, value, this, arguments, var=var):
                var = Scope({'object':object, 'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['key', 'object', 'value'])
                return var.get('$').callprop('setDesc', var.get('object'), var.get('key'), var.get('createDesc')(Js(1.0), var.get('value')))
            PyJs_anonymous_90_._set_name('anonymous')
            @Js
            def PyJs_anonymous_91_(object, key, value, this, arguments, var=var):
                var = Scope({'object':object, 'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['key', 'object', 'value'])
                var.get('object').put(var.get('key'), var.get('value'))
                return var.get('object')
            PyJs_anonymous_91_._set_name('anonymous')
            var.get('module').put('exports', (PyJs_anonymous_90_ if var.get('__webpack_require__')(Js(18.0)) else PyJs_anonymous_91_))
        PyJs_anonymous_89_._set_name('anonymous')
        @Js
        def PyJs_anonymous_92_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_93_(bitmap, value, this, arguments, var=var):
                var = Scope({'bitmap':bitmap, 'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['bitmap', 'value'])
                return Js({'enumerable':(var.get('bitmap')&Js(1.0)).neg(),'configurable':(var.get('bitmap')&Js(2.0)).neg(),'writable':(var.get('bitmap')&Js(4.0)).neg(),'value':var.get('value')})
            PyJs_anonymous_93_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_93_)
        PyJs_anonymous_92_._set_name('anonymous')
        @Js
        def PyJs_anonymous_94_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['global', 'exports', 'store', 'module', '__webpack_require__', 'SHARED'])
            var.put('global', var.get('__webpack_require__')(Js(16.0)))
            var.put('SHARED', Js('__core-js_shared__'))
            var.put('store', (var.get('global').get(var.get('SHARED')) or var.get('global').put(var.get('SHARED'), Js({}))))
            @Js
            def PyJs_anonymous_95_(key, this, arguments, var=var):
                var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
                var.registers(['key'])
                return (var.get('store').get(var.get('key')) or var.get('store').put(var.get('key'), Js({})))
            PyJs_anonymous_95_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_95_)
        PyJs_anonymous_94_._set_name('anonymous')
        @Js
        def PyJs_anonymous_96_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'module', 'def', 'has', '__webpack_require__', 'TAG'])
            var.put('def', var.get('__webpack_require__')(Js(9.0)).get('setDesc'))
            var.put('has', var.get('__webpack_require__')(Js(17.0)))
            var.put('TAG', var.get('__webpack_require__')(Js(29.0))(Js('toStringTag')))
            @Js
            def PyJs_anonymous_97_(it, tag, stat, this, arguments, var=var):
                var = Scope({'it':it, 'tag':tag, 'stat':stat, 'this':this, 'arguments':arguments}, var)
                var.registers(['tag', 'it', 'stat'])
                if (var.get('it') and var.get('has')(var.put('it', (var.get('it') if var.get('stat') else var.get('it').get('prototype'))), var.get('TAG')).neg()):
                    var.get('def')(var.get('it'), var.get('TAG'), Js({'configurable':Js(True),'value':var.get('tag')}))
            PyJs_anonymous_97_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_97_)
        PyJs_anonymous_96_._set_name('anonymous')
        @Js
        def PyJs_anonymous_98_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['uid', 'exports', 'Symbol', 'store', 'module', '__webpack_require__'])
            var.put('store', var.get('__webpack_require__')(Js(27.0))(Js('wks')))
            var.put('uid', var.get('__webpack_require__')(Js(30.0)))
            var.put('Symbol', var.get('__webpack_require__')(Js(16.0)).get('Symbol'))
            @Js
            def PyJs_anonymous_99_(name, this, arguments, var=var):
                var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
                var.registers(['name'])
                return (var.get('store').get(var.get('name')) or var.get('store').put(var.get('name'), ((var.get('Symbol') and var.get('Symbol').get(var.get('name'))) or (var.get('Symbol') or var.get('uid'))((Js('Symbol.')+var.get('name'))))))
            PyJs_anonymous_99_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_99_)
        PyJs_anonymous_98_._set_name('anonymous')
        @Js
        def PyJs_anonymous_100_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['px', 'exports', 'id', 'module'])
            var.put('id', Js(0.0))
            var.put('px', var.get('Math').callprop('random'))
            @Js
            def PyJs_anonymous_101_(key, this, arguments, var=var):
                var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
                var.registers(['key'])
                return Js('Symbol(').callprop('concat', (Js('') if PyJsStrictEq(var.get('key'),var.get('undefined')) else var.get('key')), Js(')_'), (var.put('id',Js(var.get('id').to_number())+Js(1))+var.get('px')).callprop('toString', Js(36.0)))
            PyJs_anonymous_101_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_101_)
        PyJs_anonymous_100_._set_name('anonymous')
        @Js
        def PyJs_anonymous_102_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'module', 'toIObject', '__webpack_require__', '$'])
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            var.put('toIObject', var.get('__webpack_require__')(Js(32.0)))
            @Js
            def PyJs_anonymous_103_(object, el, this, arguments, var=var):
                var = Scope({'object':object, 'el':el, 'this':this, 'arguments':arguments}, var)
                var.registers(['keys', 'key', 'object', 'length', 'index', 'O', 'el'])
                var.put('O', var.get('toIObject')(var.get('object')))
                var.put('keys', var.get('$').callprop('getKeys', var.get('O')))
                var.put('length', var.get('keys').get('length'))
                var.put('index', Js(0.0))
                while (var.get('length')>var.get('index')):
                    if PyJsStrictEq(var.get('O').get(var.put('key', var.get('keys').get((var.put('index',Js(var.get('index').to_number())+Js(1))-Js(1))))),var.get('el')):
                        return var.get('key')
            PyJs_anonymous_103_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_103_)
        PyJs_anonymous_102_._set_name('anonymous')
        @Js
        def PyJs_anonymous_104_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'defined', 'module', 'IObject', '__webpack_require__'])
            var.put('IObject', var.get('__webpack_require__')(Js(33.0)))
            var.put('defined', var.get('__webpack_require__')(Js(35.0)))
            @Js
            def PyJs_anonymous_105_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return var.get('IObject')(var.get('defined')(var.get('it')))
            PyJs_anonymous_105_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_105_)
        PyJs_anonymous_104_._set_name('anonymous')
        @Js
        def PyJs_anonymous_106_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['cof', 'module', '__webpack_require__', 'exports'])
            var.put('cof', var.get('__webpack_require__')(Js(34.0)))
            @Js
            def PyJs_anonymous_107_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return (var.get('it').callprop('split', Js('')) if (var.get('cof')(var.get('it'))==Js('String')) else var.get('Object')(var.get('it')))
            PyJs_anonymous_107_._set_name('anonymous')
            var.get('module').put('exports', (var.get('Object') if var.get('Object')(Js('z')).callprop('propertyIsEnumerable', Js(0.0)) else PyJs_anonymous_107_))
        PyJs_anonymous_106_._set_name('anonymous')
        @Js
        def PyJs_anonymous_108_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['toString', 'module', 'exports'])
            var.put('toString', Js({}).get('toString'))
            @Js
            def PyJs_anonymous_109_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return var.get('toString').callprop('call', var.get('it')).callprop('slice', Js(8.0), (-Js(1.0)))
            PyJs_anonymous_109_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_109_)
        PyJs_anonymous_108_._set_name('anonymous')
        @Js
        def PyJs_anonymous_110_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_111_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                if (var.get('it')==var.get('undefined')):
                    PyJsTempException = JsToPyException(var.get('TypeError')((Js("Can't call method on  ")+var.get('it'))))
                    raise PyJsTempException
                return var.get('it')
            PyJs_anonymous_111_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_111_)
        PyJs_anonymous_110_._set_name('anonymous')
        @Js
        def PyJs_anonymous_112_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'getWindowNames', 'toString', 'windowNames', 'toIObject', 'getNames', 'module', '__webpack_require__'])
            var.put('toIObject', var.get('__webpack_require__')(Js(32.0)))
            var.put('getNames', var.get('__webpack_require__')(Js(9.0)).get('getNames'))
            var.put('toString', Js({}).get('toString'))
            var.put('windowNames', (var.get('Object').callprop('getOwnPropertyNames', var.get('window')) if ((var.get('window',throw=False).typeof()==Js('object')) and var.get('Object').get('getOwnPropertyNames')) else Js([])))
            @Js
            def PyJs_anonymous_113_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                try:
                    return var.get('getNames')(var.get('it'))
                except PyJsException as PyJsTempException:
                    PyJsHolder_65_33827338 = var.own.get('e')
                    var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                    try:
                        return var.get('windowNames').callprop('slice')
                    finally:
                        if PyJsHolder_65_33827338 is not None:
                            var.own['e'] = PyJsHolder_65_33827338
                        else:
                            del var.own['e']
                        del PyJsHolder_65_33827338
            PyJs_anonymous_113_._set_name('anonymous')
            var.put('getWindowNames', PyJs_anonymous_113_)
            @Js
            def PyJs_getOwnPropertyNames_114_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments, 'getOwnPropertyNames':PyJs_getOwnPropertyNames_114_}, var)
                var.registers(['it'])
                if (var.get('windowNames') and (var.get('toString').callprop('call', var.get('it'))==Js('[object Window]'))):
                    return var.get('getWindowNames')(var.get('it'))
                return var.get('getNames')(var.get('toIObject')(var.get('it')))
            PyJs_getOwnPropertyNames_114_._set_name('getOwnPropertyNames')
            var.get('module').get('exports').put('get', PyJs_getOwnPropertyNames_114_)
        PyJs_anonymous_112_._set_name('anonymous')
        @Js
        def PyJs_anonymous_115_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', '$', 'exports'])
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            @Js
            def PyJs_anonymous_116_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['keys', 'symbols', 'i', 'key', 'it', 'isEnum', 'getSymbols'])
                var.put('keys', var.get('$').callprop('getKeys', var.get('it')))
                var.put('getSymbols', var.get('$').get('getSymbols'))
                if var.get('getSymbols'):
                    var.put('symbols', var.get('getSymbols')(var.get('it')))
                    var.put('isEnum', var.get('$').get('isEnum'))
                    var.put('i', Js(0.0))
                    while (var.get('symbols').get('length')>var.get('i')):
                        if var.get('isEnum').callprop('call', var.get('it'), var.put('key', var.get('symbols').get((var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))))):
                            var.get('keys').callprop('push', var.get('key'))
                return var.get('keys')
            PyJs_anonymous_116_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_116_)
        PyJs_anonymous_115_._set_name('anonymous')
        @Js
        def PyJs_anonymous_117_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['cof', 'module', '__webpack_require__', 'exports'])
            var.put('cof', var.get('__webpack_require__')(Js(34.0)))
            @Js
            def PyJs_anonymous_118_(arg, this, arguments, var=var):
                var = Scope({'arg':arg, 'this':this, 'arguments':arguments}, var)
                var.registers(['arg'])
                return (var.get('cof')(var.get('arg'))==Js('Array'))
            PyJs_anonymous_118_._set_name('anonymous')
            var.get('module').put('exports', (var.get('Array').get('isArray') or PyJs_anonymous_118_))
        PyJs_anonymous_117_._set_name('anonymous')
        @Js
        def PyJs_anonymous_119_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports', '__webpack_require__', 'isObject'])
            var.put('isObject', var.get('__webpack_require__')(Js(40.0)))
            @Js
            def PyJs_anonymous_120_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                if var.get('isObject')(var.get('it')).neg():
                    PyJsTempException = JsToPyException(var.get('TypeError')((var.get('it')+Js(' is not an object!'))))
                    raise PyJsTempException
                return var.get('it')
            PyJs_anonymous_120_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_120_)
        PyJs_anonymous_119_._set_name('anonymous')
        @Js
        def PyJs_anonymous_121_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_122_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return (PyJsStrictNeq(var.get('it'),var.get(u"null")) if PyJsStrictEq(var.get('it',throw=False).typeof(),Js('object')) else PyJsStrictEq(var.get('it',throw=False).typeof(),Js('function')))
            PyJs_anonymous_122_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_122_)
        PyJs_anonymous_121_._set_name('anonymous')
        @Js
        def PyJs_anonymous_123_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            var.get('module').put('exports', Js(True))
        PyJs_anonymous_123_._set_name('anonymous')
        @Js
        def PyJs_anonymous_124_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            pass
        PyJs_anonymous_124_._set_name('anonymous')
        @Js
        def PyJs_anonymous_125_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(44.0)),'__esModule':Js(True)}))
        PyJs_anonymous_125_._set_name('anonymous')
        @Js
        def PyJs_anonymous_126_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('__webpack_require__')(Js(45.0))
            var.get('__webpack_require__')(Js(51.0))
            var.get('module').put('exports', var.get('__webpack_require__')(Js(29.0))(Js('iterator')))
        PyJs_anonymous_126_._set_name('anonymous')
        @Js
        def PyJs_anonymous_127_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['$at', 'module', '__webpack_require__', 'exports'])
            Js('use strict')
            var.put('$at', var.get('__webpack_require__')(Js(46.0))(Js(True)))
            @Js
            def PyJs_anonymous_128_(iterated, this, arguments, var=var):
                var = Scope({'iterated':iterated, 'this':this, 'arguments':arguments}, var)
                var.registers(['iterated'])
                var.get(u"this").put('_t', var.get('String')(var.get('iterated')))
                var.get(u"this").put('_i', Js(0.0))
            PyJs_anonymous_128_._set_name('anonymous')
            @Js
            def PyJs_anonymous_129_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['point', 'O', 'index'])
                var.put('O', var.get(u"this").get('_t'))
                var.put('index', var.get(u"this").get('_i'))
                if (var.get('index')>=var.get('O').get('length')):
                    return Js({'value':var.get('undefined'),'done':Js(True)})
                var.put('point', var.get('$at')(var.get('O'), var.get('index')))
                var.get(u"this").put('_i', var.get('point').get('length'), '+')
                return Js({'value':var.get('point'),'done':Js(False)})
            PyJs_anonymous_129_._set_name('anonymous')
            var.get('__webpack_require__')(Js(48.0))(var.get('String'), Js('String'), PyJs_anonymous_128_, PyJs_anonymous_129_)
        PyJs_anonymous_127_._set_name('anonymous')
        @Js
        def PyJs_anonymous_130_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'defined', 'module', '__webpack_require__', 'toInteger'])
            var.put('toInteger', var.get('__webpack_require__')(Js(47.0)))
            var.put('defined', var.get('__webpack_require__')(Js(35.0)))
            @Js
            def PyJs_anonymous_131_(TO_STRING, this, arguments, var=var):
                var = Scope({'TO_STRING':TO_STRING, 'this':this, 'arguments':arguments}, var)
                var.registers(['TO_STRING'])
                @Js
                def PyJs_anonymous_132_(that, pos, this, arguments, var=var):
                    var = Scope({'that':that, 'pos':pos, 'this':this, 'arguments':arguments}, var)
                    var.registers(['l', 'a', 'i', 'pos', 'that', 'b', 's'])
                    var.put('s', var.get('String')(var.get('defined')(var.get('that'))))
                    var.put('i', var.get('toInteger')(var.get('pos')))
                    var.put('l', var.get('s').get('length'))
                    if ((var.get('i')<Js(0.0)) or (var.get('i')>=var.get('l'))):
                        return (Js('') if var.get('TO_STRING') else var.get('undefined'))
                    var.put('a', var.get('s').callprop('charCodeAt', var.get('i')))
                    def PyJs_LONG_133_(var=var):
                        return ((var.get('s').callprop('charAt', var.get('i')) if var.get('TO_STRING') else var.get('a')) if (((((var.get('a')<Js(55296)) or (var.get('a')>Js(56319))) or PyJsStrictEq((var.get('i')+Js(1.0)),var.get('l'))) or (var.put('b', var.get('s').callprop('charCodeAt', (var.get('i')+Js(1.0))))<Js(56320))) or (var.get('b')>Js(57343))) else (var.get('s').callprop('slice', var.get('i'), (var.get('i')+Js(2.0))) if var.get('TO_STRING') else ((((var.get('a')-Js(55296))<<Js(10.0))+(var.get('b')-Js(56320)))+Js(65536))))
                    return PyJs_LONG_133_()
                PyJs_anonymous_132_._set_name('anonymous')
                return PyJs_anonymous_132_
            PyJs_anonymous_131_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_131_)
        PyJs_anonymous_130_._set_name('anonymous')
        @Js
        def PyJs_anonymous_134_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'ceil', 'floor', 'exports'])
            var.put('ceil', var.get('Math').get('ceil'))
            var.put('floor', var.get('Math').get('floor'))
            @Js
            def PyJs_anonymous_135_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return (Js(0.0) if var.get('isNaN')(var.put('it', (+var.get('it')))) else (var.get('floor') if (var.get('it')>Js(0.0)) else var.get('ceil'))(var.get('it')))
            PyJs_anonymous_135_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_135_)
        PyJs_anonymous_134_._set_name('anonymous')
        @Js
        def PyJs_anonymous_136_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['getProto', '$iterCreate', 'returnThis', 'ITERATOR', 'BUGGY', 'exports', 'hide', 'setToStringTag', '$export', 'KEYS', 'module', 'redefine', 'Iterators', 'VALUES', 'has', '__webpack_require__', 'FF_ITERATOR', 'LIBRARY'])
            Js('use strict')
            var.put('LIBRARY', var.get('__webpack_require__')(Js(41.0)))
            var.put('$export', var.get('__webpack_require__')(Js(20.0)))
            var.put('redefine', var.get('__webpack_require__')(Js(24.0)))
            var.put('hide', var.get('__webpack_require__')(Js(25.0)))
            var.put('has', var.get('__webpack_require__')(Js(17.0)))
            var.put('Iterators', var.get('__webpack_require__')(Js(49.0)))
            var.put('$iterCreate', var.get('__webpack_require__')(Js(50.0)))
            var.put('setToStringTag', var.get('__webpack_require__')(Js(28.0)))
            var.put('getProto', var.get('__webpack_require__')(Js(9.0)).get('getProto'))
            var.put('ITERATOR', var.get('__webpack_require__')(Js(29.0))(Js('iterator')))
            var.put('BUGGY', (Js([]).get('keys') and Js([]).callprop('keys').contains(Js('next'))).neg())
            var.put('FF_ITERATOR', Js('@@iterator'))
            var.put('KEYS', Js('keys'))
            var.put('VALUES', Js('values'))
            @Js
            def PyJs_anonymous_137_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return var.get(u"this")
            PyJs_anonymous_137_._set_name('anonymous')
            var.put('returnThis', PyJs_anonymous_137_)
            @Js
            def PyJs_anonymous_138_(Base, NAME, Constructor, next, DEFAULT, IS_SET, FORCED, this, arguments, var=var):
                var = Scope({'Base':Base, 'NAME':NAME, 'Constructor':Constructor, 'next':next, 'DEFAULT':DEFAULT, 'IS_SET':IS_SET, 'FORCED':FORCED, 'this':this, 'arguments':arguments}, var)
                var.registers(['IS_SET', 'DEFAULT', 'getMethod', 'methods', 'key', 'proto', 'IteratorPrototype', 'NAME', 'Base', 'Constructor', 'next', 'FORCED', '$default', 'DEF_VALUES', 'VALUES_BUG', 'TAG', '$native'])
                var.get('$iterCreate')(var.get('Constructor'), var.get('NAME'), var.get('next'))
                @Js
                def PyJs_anonymous_139_(kind, this, arguments, var=var):
                    var = Scope({'kind':kind, 'this':this, 'arguments':arguments}, var)
                    var.registers(['kind'])
                    if (var.get('BUGGY').neg() and var.get('proto').contains(var.get('kind'))):
                        return var.get('proto').get(var.get('kind'))
                    while 1:
                        SWITCHED = False
                        CONDITION = (var.get('kind'))
                        if SWITCHED or PyJsStrictEq(CONDITION, var.get('KEYS')):
                            SWITCHED = True
                            @Js
                            def PyJs_keys_140_(this, arguments, var=var):
                                var = Scope({'this':this, 'arguments':arguments, 'keys':PyJs_keys_140_}, var)
                                var.registers([])
                                return var.get('Constructor').create(var.get(u"this"), var.get('kind'))
                            PyJs_keys_140_._set_name('keys')
                            return PyJs_keys_140_
                        if SWITCHED or PyJsStrictEq(CONDITION, var.get('VALUES')):
                            SWITCHED = True
                            @Js
                            def PyJs_values_141_(this, arguments, var=var):
                                var = Scope({'this':this, 'arguments':arguments, 'values':PyJs_values_141_}, var)
                                var.registers([])
                                return var.get('Constructor').create(var.get(u"this"), var.get('kind'))
                            PyJs_values_141_._set_name('values')
                            return PyJs_values_141_
                        SWITCHED = True
                        break
                    @Js
                    def PyJs_entries_142_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'entries':PyJs_entries_142_}, var)
                        var.registers([])
                        return var.get('Constructor').create(var.get(u"this"), var.get('kind'))
                    PyJs_entries_142_._set_name('entries')
                    return PyJs_entries_142_
                PyJs_anonymous_139_._set_name('anonymous')
                var.put('getMethod', PyJs_anonymous_139_)
                var.put('TAG', (var.get('NAME')+Js(' Iterator')))
                var.put('DEF_VALUES', (var.get('DEFAULT')==var.get('VALUES')))
                var.put('VALUES_BUG', Js(False))
                var.put('proto', var.get('Base').get('prototype'))
                var.put('$native', ((var.get('proto').get(var.get('ITERATOR')) or var.get('proto').get(var.get('FF_ITERATOR'))) or (var.get('DEFAULT') and var.get('proto').get(var.get('DEFAULT')))))
                var.put('$default', (var.get('$native') or var.get('getMethod')(var.get('DEFAULT'))))
                if var.get('$native'):
                    var.put('IteratorPrototype', var.get('getProto')(var.get('$default').callprop('call', var.get('Base').create())))
                    var.get('setToStringTag')(var.get('IteratorPrototype'), var.get('TAG'), Js(True))
                    if (var.get('LIBRARY').neg() and var.get('has')(var.get('proto'), var.get('FF_ITERATOR'))):
                        var.get('hide')(var.get('IteratorPrototype'), var.get('ITERATOR'), var.get('returnThis'))
                    if (var.get('DEF_VALUES') and PyJsStrictNeq(var.get('$native').get('name'),var.get('VALUES'))):
                        var.put('VALUES_BUG', Js(True))
                        @Js
                        def PyJs_values_143_(this, arguments, var=var):
                            var = Scope({'this':this, 'arguments':arguments, 'values':PyJs_values_143_}, var)
                            var.registers([])
                            return var.get('$native').callprop('call', var.get(u"this"))
                        PyJs_values_143_._set_name('values')
                        var.put('$default', PyJs_values_143_)
                if ((var.get('LIBRARY').neg() or var.get('FORCED')) and ((var.get('BUGGY') or var.get('VALUES_BUG')) or var.get('proto').get(var.get('ITERATOR')).neg())):
                    var.get('hide')(var.get('proto'), var.get('ITERATOR'), var.get('$default'))
                var.get('Iterators').put(var.get('NAME'), var.get('$default'))
                var.get('Iterators').put(var.get('TAG'), var.get('returnThis'))
                if var.get('DEFAULT'):
                    var.put('methods', Js({'values':(var.get('$default') if var.get('DEF_VALUES') else var.get('getMethod')(var.get('VALUES'))),'keys':(var.get('$default') if var.get('IS_SET') else var.get('getMethod')(var.get('KEYS'))),'entries':(var.get('$default') if var.get('DEF_VALUES').neg() else var.get('getMethod')(Js('entries')))}))
                    if var.get('FORCED'):
                        for PyJsTemp in var.get('methods'):
                            var.put('key', PyJsTemp)
                            if var.get('proto').contains(var.get('key')).neg():
                                var.get('redefine')(var.get('proto'), var.get('key'), var.get('methods').get(var.get('key')))
                    else:
                        var.get('$export')((var.get('$export').get('P')+(var.get('$export').get('F')*(var.get('BUGGY') or var.get('VALUES_BUG')))), var.get('NAME'), var.get('methods'))
                return var.get('methods')
            PyJs_anonymous_138_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_138_)
        PyJs_anonymous_136_._set_name('anonymous')
        @Js
        def PyJs_anonymous_144_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            var.get('module').put('exports', Js({}))
        PyJs_anonymous_144_._set_name('anonymous')
        @Js
        def PyJs_anonymous_145_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'IteratorPrototype', 'descriptor', 'module', '__webpack_require__', '$', 'setToStringTag'])
            Js('use strict')
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            var.put('descriptor', var.get('__webpack_require__')(Js(26.0)))
            var.put('setToStringTag', var.get('__webpack_require__')(Js(28.0)))
            var.put('IteratorPrototype', Js({}))
            @Js
            def PyJs_anonymous_146_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return var.get(u"this")
            PyJs_anonymous_146_._set_name('anonymous')
            var.get('__webpack_require__')(Js(25.0))(var.get('IteratorPrototype'), var.get('__webpack_require__')(Js(29.0))(Js('iterator')), PyJs_anonymous_146_)
            @Js
            def PyJs_anonymous_147_(Constructor, NAME, next, this, arguments, var=var):
                var = Scope({'Constructor':Constructor, 'NAME':NAME, 'next':next, 'this':this, 'arguments':arguments}, var)
                var.registers(['Constructor', 'NAME', 'next'])
                var.get('Constructor').put('prototype', var.get('$').callprop('create', var.get('IteratorPrototype'), Js({'next':var.get('descriptor')(Js(1.0), var.get('next'))})))
                var.get('setToStringTag')(var.get('Constructor'), (var.get('NAME')+Js(' Iterator')))
            PyJs_anonymous_147_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_147_)
        PyJs_anonymous_145_._set_name('anonymous')
        @Js
        def PyJs_anonymous_148_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'Iterators', 'exports'])
            var.get('__webpack_require__')(Js(52.0))
            var.put('Iterators', var.get('__webpack_require__')(Js(49.0)))
            var.get('Iterators').put('NodeList', var.get('Iterators').put('HTMLCollection', var.get('Iterators').get('Array')))
        PyJs_anonymous_148_._set_name('anonymous')
        @Js
        def PyJs_anonymous_149_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['step', 'addToUnscopables', 'exports', 'module', 'toIObject', 'Iterators', '__webpack_require__'])
            Js('use strict')
            var.put('addToUnscopables', var.get('__webpack_require__')(Js(53.0)))
            var.put('step', var.get('__webpack_require__')(Js(54.0)))
            var.put('Iterators', var.get('__webpack_require__')(Js(49.0)))
            var.put('toIObject', var.get('__webpack_require__')(Js(32.0)))
            @Js
            def PyJs_anonymous_150_(iterated, kind, this, arguments, var=var):
                var = Scope({'iterated':iterated, 'kind':kind, 'this':this, 'arguments':arguments}, var)
                var.registers(['kind', 'iterated'])
                var.get(u"this").put('_t', var.get('toIObject')(var.get('iterated')))
                var.get(u"this").put('_i', Js(0.0))
                var.get(u"this").put('_k', var.get('kind'))
            PyJs_anonymous_150_._set_name('anonymous')
            @Js
            def PyJs_anonymous_151_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['kind', 'O', 'index'])
                var.put('O', var.get(u"this").get('_t'))
                var.put('kind', var.get(u"this").get('_k'))
                var.put('index', (var.get(u"this").put('_i',Js(var.get(u"this").get('_i').to_number())+Js(1))-Js(1)))
                if (var.get('O').neg() or (var.get('index')>=var.get('O').get('length'))):
                    var.get(u"this").put('_t', var.get('undefined'))
                    return var.get('step')(Js(1.0))
                if (var.get('kind')==Js('keys')):
                    return var.get('step')(Js(0.0), var.get('index'))
                if (var.get('kind')==Js('values')):
                    return var.get('step')(Js(0.0), var.get('O').get(var.get('index')))
                return var.get('step')(Js(0.0), Js([var.get('index'), var.get('O').get(var.get('index'))]))
            PyJs_anonymous_151_._set_name('anonymous')
            var.get('module').put('exports', var.get('__webpack_require__')(Js(48.0))(var.get('Array'), Js('Array'), PyJs_anonymous_150_, PyJs_anonymous_151_, Js('values')))
            var.get('Iterators').put('Arguments', var.get('Iterators').get('Array'))
            var.get('addToUnscopables')(Js('keys'))
            var.get('addToUnscopables')(Js('values'))
            var.get('addToUnscopables')(Js('entries'))
        PyJs_anonymous_149_._set_name('anonymous')
        @Js
        def PyJs_anonymous_152_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_153_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                pass
            PyJs_anonymous_153_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_153_)
        PyJs_anonymous_152_._set_name('anonymous')
        @Js
        def PyJs_anonymous_154_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            @Js
            def PyJs_anonymous_155_(done, value, this, arguments, var=var):
                var = Scope({'done':done, 'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['value', 'done'])
                return Js({'value':var.get('value'),'done':var.get('done').neg().neg()})
            PyJs_anonymous_155_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_155_)
        PyJs_anonymous_154_._set_name('anonymous')
        @Js
        def PyJs_anonymous_156_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(56.0)),'__esModule':Js(True)}))
        PyJs_anonymous_156_._set_name('anonymous')
        @Js
        def PyJs_anonymous_157_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('__webpack_require__')(Js(51.0))
            var.get('__webpack_require__')(Js(45.0))
            var.get('module').put('exports', var.get('__webpack_require__')(Js(57.0)))
        PyJs_anonymous_157_._set_name('anonymous')
        @Js
        def PyJs_anonymous_158_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'module', 'anObject', '__webpack_require__', 'get'])
            var.put('anObject', var.get('__webpack_require__')(Js(39.0)))
            var.put('get', var.get('__webpack_require__')(Js(58.0)))
            @Js
            def PyJs_anonymous_159_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it', 'iterFn'])
                var.put('iterFn', var.get('get')(var.get('it')))
                if (var.get('iterFn',throw=False).typeof()!=Js('function')):
                    PyJsTempException = JsToPyException(var.get('TypeError')((var.get('it')+Js(' is not iterable!'))))
                    raise PyJsTempException
                return var.get('anObject')(var.get('iterFn').callprop('call', var.get('it')))
            PyJs_anonymous_159_._set_name('anonymous')
            var.get('module').put('exports', var.get('__webpack_require__')(Js(21.0)).put('getIterator', PyJs_anonymous_159_))
        PyJs_anonymous_158_._set_name('anonymous')
        @Js
        def PyJs_anonymous_160_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['ITERATOR', 'exports', 'module', 'Iterators', '__webpack_require__', 'classof'])
            var.put('classof', var.get('__webpack_require__')(Js(59.0)))
            var.put('ITERATOR', var.get('__webpack_require__')(Js(29.0))(Js('iterator')))
            var.put('Iterators', var.get('__webpack_require__')(Js(49.0)))
            @Js
            def PyJs_anonymous_161_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                if (var.get('it')!=var.get('undefined')):
                    return ((var.get('it').get(var.get('ITERATOR')) or var.get('it').get('@@iterator')) or var.get('Iterators').get(var.get('classof')(var.get('it'))))
            PyJs_anonymous_161_._set_name('anonymous')
            var.get('module').put('exports', var.get('__webpack_require__')(Js(21.0)).put('getIteratorMethod', PyJs_anonymous_161_))
        PyJs_anonymous_160_._set_name('anonymous')
        @Js
        def PyJs_anonymous_162_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'cof', 'module', '__webpack_require__', 'ARG', 'TAG'])
            var.put('cof', var.get('__webpack_require__')(Js(34.0)))
            var.put('TAG', var.get('__webpack_require__')(Js(29.0))(Js('toStringTag')))
            @Js
            def PyJs_anonymous_163_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return var.get('arguments')
            PyJs_anonymous_163_._set_name('anonymous')
            var.put('ARG', (var.get('cof')(PyJs_anonymous_163_())==Js('Arguments')))
            @Js
            def PyJs_anonymous_164_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it', 'B', 'O', 'T'])
                pass
                def PyJs_LONG_165_(var=var):
                    return (Js('Null') if PyJsStrictEq(var.get('it'),var.get(u"null")) else (var.get('T') if (var.put('T', var.put('O', var.get('Object')(var.get('it'))).get(var.get('TAG'))).typeof()==Js('string')) else (var.get('cof')(var.get('O')) if var.get('ARG') else (Js('Arguments') if ((var.put('B', var.get('cof')(var.get('O')))==Js('Object')) and (var.get('O').get('callee').typeof()==Js('function'))) else var.get('B')))))
                return (Js('Undefined') if PyJsStrictEq(var.get('it'),var.get('undefined')) else PyJs_LONG_165_())
            PyJs_anonymous_164_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_164_)
        PyJs_anonymous_162_._set_name('anonymous')
        @Js
        def PyJs_anonymous_166_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(61.0)),'__esModule':Js(True)}))
        PyJs_anonymous_166_._set_name('anonymous')
        @Js
        def PyJs_anonymous_167_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('__webpack_require__')(Js(62.0))
            var.get('module').put('exports', var.get('__webpack_require__')(Js(21.0)).get('Object').get('keys'))
        PyJs_anonymous_167_._set_name('anonymous')
        @Js
        def PyJs_anonymous_168_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['toObject', 'module', '__webpack_require__', 'exports'])
            var.put('toObject', var.get('__webpack_require__')(Js(63.0)))
            @Js
            def PyJs_anonymous_169_(PyJsArg_246b657973_, this, arguments, var=var):
                var = Scope({'$keys':PyJsArg_246b657973_, 'this':this, 'arguments':arguments}, var)
                var.registers(['$keys'])
                @Js
                def PyJs_keys_170_(it, this, arguments, var=var):
                    var = Scope({'it':it, 'this':this, 'arguments':arguments, 'keys':PyJs_keys_170_}, var)
                    var.registers(['it'])
                    return var.get('$keys')(var.get('toObject')(var.get('it')))
                PyJs_keys_170_._set_name('keys')
                return PyJs_keys_170_
            PyJs_anonymous_169_._set_name('anonymous')
            var.get('__webpack_require__')(Js(64.0))(Js('keys'), PyJs_anonymous_169_)
        PyJs_anonymous_168_._set_name('anonymous')
        @Js
        def PyJs_anonymous_171_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'defined', 'exports'])
            var.put('defined', var.get('__webpack_require__')(Js(35.0)))
            @Js
            def PyJs_anonymous_172_(it, this, arguments, var=var):
                var = Scope({'it':it, 'this':this, 'arguments':arguments}, var)
                var.registers(['it'])
                return var.get('Object')(var.get('defined')(var.get('it')))
            PyJs_anonymous_172_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_172_)
        PyJs_anonymous_171_._set_name('anonymous')
        @Js
        def PyJs_anonymous_173_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['fails', 'exports', 'core', '$export', 'module', '__webpack_require__'])
            var.put('$export', var.get('__webpack_require__')(Js(20.0)))
            var.put('core', var.get('__webpack_require__')(Js(21.0)))
            var.put('fails', var.get('__webpack_require__')(Js(19.0)))
            @Js
            def PyJs_anonymous_174_(KEY, exec, this, arguments, var=var):
                var = Scope({'KEY':KEY, 'exec':exec, 'this':this, 'arguments':arguments}, var)
                var.registers(['exp', 'KEY', 'exec', 'fn'])
                var.put('fn', ((var.get('core').get('Object') or Js({})).get(var.get('KEY')) or var.get('Object').get(var.get('KEY'))))
                var.put('exp', Js({}))
                var.get('exp').put(var.get('KEY'), var.get('exec')(var.get('fn')))
                @Js
                def PyJs_anonymous_175_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    var.get('fn')(Js(1.0))
                PyJs_anonymous_175_._set_name('anonymous')
                var.get('$export')((var.get('$export').get('S')+(var.get('$export').get('F')*var.get('fails')(PyJs_anonymous_175_))), Js('Object'), var.get('exp'))
            PyJs_anonymous_174_._set_name('anonymous')
            var.get('module').put('exports', PyJs_anonymous_174_)
        PyJs_anonymous_173_._set_name('anonymous')
        @Js
        def PyJs_anonymous_176_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_interopRequireDefault', 'exports', '_exception2', 'module', '_exception', '__webpack_require__'])
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            @Js
            def PyJs_anonymous_177_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_178_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    if PyJsStrictEq(var.get('arguments').get('length'),Js(1.0)):
                        return var.get('undefined')
                    else:
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(((Js('Missing helper: "')+var.get('arguments').get((var.get('arguments').get('length')-Js(1.0))).get('name'))+Js('"'))))
                        raise PyJsTempException
                PyJs_anonymous_178_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('helperMissing'), PyJs_anonymous_178_)
            PyJs_anonymous_177_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_177_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_176_._set_name('anonymous')
        @Js
        def PyJs_anonymous_179_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_interopRequireDefault', 'exports', '_exception2', 'module', '_exception', '_utils', '__webpack_require__'])
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            @Js
            def PyJs_anonymous_180_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_181_(conditional, options, this, arguments, var=var):
                    var = Scope({'conditional':conditional, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['options', 'conditional'])
                    if (var.get('arguments').get('length')!=Js(2.0)):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('#if requires exactly one argument')))
                        raise PyJsTempException
                    if var.get('_utils').callprop('isFunction', var.get('conditional')):
                        var.put('conditional', var.get('conditional').callprop('call', var.get(u"this")))
                    if ((var.get('options').get('hash').get('includeZero').neg() and var.get('conditional').neg()) or var.get('_utils').callprop('isEmpty', var.get('conditional'))):
                        return var.get('options').callprop('inverse', var.get(u"this"))
                    else:
                        return var.get('options').callprop('fn', var.get(u"this"))
                PyJs_anonymous_181_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('if'), PyJs_anonymous_181_)
                @Js
                def PyJs_anonymous_182_(conditional, options, this, arguments, var=var):
                    var = Scope({'conditional':conditional, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['options', 'conditional'])
                    if (var.get('arguments').get('length')!=Js(2.0)):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('#unless requires exactly one argument')))
                        raise PyJsTempException
                    return var.get('instance').get('helpers').get('if').callprop('call', var.get(u"this"), var.get('conditional'), Js({'fn':var.get('options').get('inverse'),'inverse':var.get('options').get('fn'),'hash':var.get('options').get('hash')}))
                PyJs_anonymous_182_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('unless'), PyJs_anonymous_182_)
            PyJs_anonymous_180_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_180_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_179_._set_name('anonymous')
        @Js
        def PyJs_anonymous_183_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            @Js
            def PyJs_anonymous_184_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_185_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers(['level', 'options', 'args', 'i'])
                    var.put('args', Js([var.get('undefined')]))
                    var.put('options', var.get('arguments').get((var.get('arguments').get('length')-Js(1.0))))
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<(var.get('arguments').get('length')-Js(1.0))):
                        var.get('args').callprop('push', var.get('arguments').get(var.get('i')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    var.put('level', Js(1.0))
                    if (var.get('options').get('hash').get('level')!=var.get(u"null")):
                        var.put('level', var.get('options').get('hash').get('level'))
                    else:
                        if (var.get('options').get('data') and (var.get('options').get('data').get('level')!=var.get(u"null"))):
                            var.put('level', var.get('options').get('data').get('level'))
                    var.get('args').put('0', var.get('level'))
                    var.get('instance').get('log').callprop('apply', var.get('instance'), var.get('args'))
                PyJs_anonymous_185_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('log'), PyJs_anonymous_185_)
            PyJs_anonymous_184_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_184_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_183_._set_name('anonymous')
        @Js
        def PyJs_anonymous_186_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            @Js
            def PyJs_anonymous_187_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_188_(obj, field, options, this, arguments, var=var):
                    var = Scope({'obj':obj, 'field':field, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['obj', 'options', 'field'])
                    if var.get('obj').neg():
                        return var.get('obj')
                    return var.get('options').callprop('lookupProperty', var.get('obj'), var.get('field'))
                PyJs_anonymous_188_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('lookup'), PyJs_anonymous_188_)
            PyJs_anonymous_187_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_187_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_186_._set_name('anonymous')
        @Js
        def PyJs_anonymous_189_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_interopRequireDefault', 'exports', '_exception2', 'module', '_exception', '_utils', '__webpack_require__'])
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            @Js
            def PyJs_anonymous_190_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_191_(context, options, this, arguments, var=var):
                    var = Scope({'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['options', 'context', 'data', 'fn'])
                    if (var.get('arguments').get('length')!=Js(2.0)):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('#with requires exactly one argument')))
                        raise PyJsTempException
                    if var.get('_utils').callprop('isFunction', var.get('context')):
                        var.put('context', var.get('context').callprop('call', var.get(u"this")))
                    var.put('fn', var.get('options').get('fn'))
                    if var.get('_utils').callprop('isEmpty', var.get('context')).neg():
                        var.put('data', var.get('options').get('data'))
                        if (var.get('options').get('data') and var.get('options').get('ids')):
                            var.put('data', var.get('_utils').callprop('createFrame', var.get('options').get('data')))
                            var.get('data').put('contextPath', var.get('_utils').callprop('appendContextPath', var.get('options').get('data').get('contextPath'), var.get('options').get('ids').get('0')))
                        return var.get('fn')(var.get('context'), Js({'data':var.get('data'),'blockParams':var.get('_utils').callprop('blockParams', Js([var.get('context')]), Js([(var.get('data') and var.get('data').get('contextPath'))]))}))
                    else:
                        return var.get('options').callprop('inverse', var.get(u"this"))
                PyJs_anonymous_191_._set_name('anonymous')
                var.get('instance').callprop('registerHelper', Js('with'), PyJs_anonymous_191_)
            PyJs_anonymous_190_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_190_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_189_._set_name('anonymous')
        @Js
        def PyJs_anonymous_192_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['registerDefaultDecorators', '_interopRequireDefault', 'exports', '_decoratorsInline', 'module', '_decoratorsInline2', '__webpack_require__'])
            @Js
            def PyJsHoisted_registerDefaultDecorators_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                var.get('_decoratorsInline2').callprop('default', var.get('instance'))
            PyJsHoisted_registerDefaultDecorators_.func_name = 'registerDefaultDecorators'
            var.put('registerDefaultDecorators', PyJsHoisted_registerDefaultDecorators_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('registerDefaultDecorators', var.get('registerDefaultDecorators'))
            var.put('_decoratorsInline', var.get('__webpack_require__')(Js(71.0)))
            var.put('_decoratorsInline2', var.get('_interopRequireDefault')(var.get('_decoratorsInline')))
            pass
        PyJs_anonymous_192_._set_name('anonymous')
        @Js
        def PyJs_anonymous_193_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports', '__webpack_require__', '_utils'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            @Js
            def PyJs_anonymous_194_(instance, this, arguments, var=var):
                var = Scope({'instance':instance, 'this':this, 'arguments':arguments}, var)
                var.registers(['instance'])
                @Js
                def PyJs_anonymous_195_(fn, props, container, options, this, arguments, var=var):
                    var = Scope({'fn':fn, 'props':props, 'container':container, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['container', 'fn', 'props', 'ret', 'options'])
                    var.put('ret', var.get('fn'))
                    if var.get('props').get('partials').neg():
                        var.get('props').put('partials', Js({}))
                        @Js
                        def PyJs_anonymous_196_(context, options, this, arguments, var=var):
                            var = Scope({'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                            var.registers(['options', 'context', 'ret', 'original'])
                            var.put('original', var.get('container').get('partials'))
                            var.get('container').put('partials', var.get('_utils').callprop('extend', Js({}), var.get('original'), var.get('props').get('partials')))
                            var.put('ret', var.get('fn')(var.get('context'), var.get('options')))
                            var.get('container').put('partials', var.get('original'))
                            return var.get('ret')
                        PyJs_anonymous_196_._set_name('anonymous')
                        var.put('ret', PyJs_anonymous_196_)
                    var.get('props').get('partials').put(var.get('options').get('args').get('0'), var.get('options').get('fn'))
                    return var.get('ret')
                PyJs_anonymous_195_._set_name('anonymous')
                var.get('instance').callprop('registerDecorator', Js('inline'), PyJs_anonymous_195_)
            PyJs_anonymous_194_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_194_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_193_._set_name('anonymous')
        @Js
        def PyJs_anonymous_197_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'module', '_utils', '__webpack_require__', 'logger'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            @Js
            def PyJs_lookupLevel_198_(level, this, arguments, var=var):
                var = Scope({'level':level, 'this':this, 'arguments':arguments, 'lookupLevel':PyJs_lookupLevel_198_}, var)
                var.registers(['levelMap', 'level'])
                if PyJsStrictEq(var.get('level',throw=False).typeof(),Js('string')):
                    var.put('levelMap', var.get('_utils').callprop('indexOf', var.get('logger').get('methodMap'), var.get('level').callprop('toLowerCase')))
                    if (var.get('levelMap')>=Js(0.0)):
                        var.put('level', var.get('levelMap'))
                    else:
                        var.put('level', var.get('parseInt')(var.get('level'), Js(10.0)))
                return var.get('level')
            PyJs_lookupLevel_198_._set_name('lookupLevel')
            @Js
            def PyJs_log_199_(level, this, arguments, var=var):
                var = Scope({'level':level, 'this':this, 'arguments':arguments, 'log':PyJs_log_199_}, var)
                var.registers(['_len', 'level', '_key', 'message', 'method'])
                var.put('level', var.get('logger').callprop('lookupLevel', var.get('level')))
                if (PyJsStrictNeq(var.get('console',throw=False).typeof(),Js('undefined')) and (var.get('logger').callprop('lookupLevel', var.get('logger').get('level'))<=var.get('level'))):
                    var.put('method', var.get('logger').get('methodMap').get(var.get('level')))
                    if var.get('console').get(var.get('method')).neg():
                        var.put('method', Js('log'))
                    #for JS loop
                    var.put('_len', var.get('arguments').get('length'))
                    var.put('message', var.get('Array')(((var.get('_len')-Js(1.0)) if (var.get('_len')>Js(1.0)) else Js(0.0))))
                    var.put('_key', Js(1.0))
                    while (var.get('_key')<var.get('_len')):
                        var.get('message').put((var.get('_key')-Js(1.0)), var.get('arguments').get(var.get('_key')))
                        # update
                        (var.put('_key',Js(var.get('_key').to_number())+Js(1))-Js(1))
                    var.get('console').get(var.get('method')).callprop('apply', var.get('console'), var.get('message'))
            PyJs_log_199_._set_name('log')
            var.put('logger', Js({'methodMap':Js([Js('debug'), Js('info'), Js('warn'), Js('error')]),'level':Js('info'),'lookupLevel':PyJs_lookupLevel_198_,'log':PyJs_log_199_}))
            var.get('exports').put('default', var.get('logger'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_197_._set_name('anonymous')
        @Js
        def PyJs_anonymous_200_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['loggedProperties', 'logUnexpecedPropertyAccessOnce', '_logger', '_interopRequireDefault', 'checkWhiteList', 'exports', 'resultIsAllowed', 'resetLoggedProperties', '_createNewLookupObject', 'createProtoAccessControl', '_logger2', 'module', '_Object$keys', '_Object$create', '__webpack_require__'])
            @Js
            def PyJsHoisted_createProtoAccessControl_(runtimeOptions, this, arguments, var=var):
                var = Scope({'runtimeOptions':runtimeOptions, 'this':this, 'arguments':arguments}, var)
                var.registers(['runtimeOptions', 'defaultPropertyWhiteList', 'defaultMethodWhiteList'])
                var.put('defaultMethodWhiteList', var.get('_Object$create')(var.get(u"null")))
                var.get('defaultMethodWhiteList').put('constructor', Js(False))
                var.get('defaultMethodWhiteList').put('__defineGetter__', Js(False))
                var.get('defaultMethodWhiteList').put('__defineSetter__', Js(False))
                var.get('defaultMethodWhiteList').put('__lookupGetter__', Js(False))
                var.put('defaultPropertyWhiteList', var.get('_Object$create')(var.get(u"null")))
                var.get('defaultPropertyWhiteList').put('__proto__', Js(False))
                return Js({'properties':Js({'whitelist':var.get('_createNewLookupObject').callprop('createNewLookupObject', var.get('defaultPropertyWhiteList'), var.get('runtimeOptions').get('allowedProtoProperties')),'defaultValue':var.get('runtimeOptions').get('allowProtoPropertiesByDefault')}),'methods':Js({'whitelist':var.get('_createNewLookupObject').callprop('createNewLookupObject', var.get('defaultMethodWhiteList'), var.get('runtimeOptions').get('allowedProtoMethods')),'defaultValue':var.get('runtimeOptions').get('allowProtoMethodsByDefault')})})
            PyJsHoisted_createProtoAccessControl_.func_name = 'createProtoAccessControl'
            var.put('createProtoAccessControl', PyJsHoisted_createProtoAccessControl_)
            @Js
            def PyJsHoisted_resultIsAllowed_(result, protoAccessControl, propertyName, this, arguments, var=var):
                var = Scope({'result':result, 'protoAccessControl':protoAccessControl, 'propertyName':propertyName, 'this':this, 'arguments':arguments}, var)
                var.registers(['result', 'protoAccessControl', 'propertyName'])
                if PyJsStrictEq(var.get('result',throw=False).typeof(),Js('function')):
                    return var.get('checkWhiteList')(var.get('protoAccessControl').get('methods'), var.get('propertyName'))
                else:
                    return var.get('checkWhiteList')(var.get('protoAccessControl').get('properties'), var.get('propertyName'))
            PyJsHoisted_resultIsAllowed_.func_name = 'resultIsAllowed'
            var.put('resultIsAllowed', PyJsHoisted_resultIsAllowed_)
            @Js
            def PyJsHoisted_checkWhiteList_(protoAccessControlForType, propertyName, this, arguments, var=var):
                var = Scope({'protoAccessControlForType':protoAccessControlForType, 'propertyName':propertyName, 'this':this, 'arguments':arguments}, var)
                var.registers(['protoAccessControlForType', 'propertyName'])
                if PyJsStrictNeq(var.get('protoAccessControlForType').get('whitelist').get(var.get('propertyName')),var.get('undefined')):
                    return PyJsStrictEq(var.get('protoAccessControlForType').get('whitelist').get(var.get('propertyName')),Js(True))
                if PyJsStrictNeq(var.get('protoAccessControlForType').get('defaultValue'),var.get('undefined')):
                    return var.get('protoAccessControlForType').get('defaultValue')
                var.get('logUnexpecedPropertyAccessOnce')(var.get('propertyName'))
                return Js(False)
            PyJsHoisted_checkWhiteList_.func_name = 'checkWhiteList'
            var.put('checkWhiteList', PyJsHoisted_checkWhiteList_)
            @Js
            def PyJsHoisted_logUnexpecedPropertyAccessOnce_(propertyName, this, arguments, var=var):
                var = Scope({'propertyName':propertyName, 'this':this, 'arguments':arguments}, var)
                var.registers(['propertyName'])
                if PyJsStrictNeq(var.get('loggedProperties').get(var.get('propertyName')),Js(True)):
                    var.get('loggedProperties').put(var.get('propertyName'), Js(True))
                    def PyJs_LONG_201_(var=var):
                        return var.get('_logger2').get('default').callprop('log', Js('error'), ((((Js('Handlebars: Access has been denied to resolve the property "')+var.get('propertyName'))+Js('" because it is not an "own property" of its parent.\n'))+Js('You can add a runtime option to disable the check or this warning:\n'))+Js('See https://handlebarsjs.com/api-reference/runtime-options.html#options-to-control-prototype-access for details')))
                    PyJs_LONG_201_()
            PyJsHoisted_logUnexpecedPropertyAccessOnce_.func_name = 'logUnexpecedPropertyAccessOnce'
            var.put('logUnexpecedPropertyAccessOnce', PyJsHoisted_logUnexpecedPropertyAccessOnce_)
            @Js
            def PyJsHoisted_resetLoggedProperties_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                @Js
                def PyJs_anonymous_202_(propertyName, this, arguments, var=var):
                    var = Scope({'propertyName':propertyName, 'this':this, 'arguments':arguments}, var)
                    var.registers(['propertyName'])
                    var.get('loggedProperties').delete(var.get('propertyName'))
                PyJs_anonymous_202_._set_name('anonymous')
                var.get('_Object$keys')(var.get('loggedProperties')).callprop('forEach', PyJs_anonymous_202_)
            PyJsHoisted_resetLoggedProperties_.func_name = 'resetLoggedProperties'
            var.put('resetLoggedProperties', PyJsHoisted_resetLoggedProperties_)
            Js('use strict')
            var.put('_Object$create', var.get('__webpack_require__')(Js(74.0)).get('default'))
            var.put('_Object$keys', var.get('__webpack_require__')(Js(60.0)).get('default'))
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('createProtoAccessControl', var.get('createProtoAccessControl'))
            var.get('exports').put('resultIsAllowed', var.get('resultIsAllowed'))
            var.get('exports').put('resetLoggedProperties', var.get('resetLoggedProperties'))
            var.put('_createNewLookupObject', var.get('__webpack_require__')(Js(76.0)))
            var.put('_logger', var.get('__webpack_require__')(Js(72.0)))
            var.put('_logger2', var.get('_interopRequireDefault')(var.get('_logger')))
            var.put('loggedProperties', var.get('_Object$create')(var.get(u"null")))
            pass
            pass
            pass
            pass
            pass
        PyJs_anonymous_200_._set_name('anonymous')
        @Js
        def PyJs_anonymous_203_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(75.0)),'__esModule':Js(True)}))
        PyJs_anonymous_203_._set_name('anonymous')
        @Js
        def PyJs_anonymous_204_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', '$', 'exports'])
            var.put('$', var.get('__webpack_require__')(Js(9.0)))
            @Js
            def PyJs_create_205_(P, D, this, arguments, var=var):
                var = Scope({'P':P, 'D':D, 'this':this, 'arguments':arguments, 'create':PyJs_create_205_}, var)
                var.registers(['D', 'P'])
                return var.get('$').callprop('create', var.get('P'), var.get('D'))
            PyJs_create_205_._set_name('create')
            var.get('module').put('exports', PyJs_create_205_)
        PyJs_anonymous_204_._set_name('anonymous')
        @Js
        def PyJs_anonymous_206_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['exports', 'createNewLookupObject', 'module', '_utils', '_Object$create', '__webpack_require__'])
            @Js
            def PyJsHoisted_createNewLookupObject_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['_len', 'sources', '_key'])
                #for JS loop
                var.put('_len', var.get('arguments').get('length'))
                var.put('sources', var.get('Array')(var.get('_len')))
                var.put('_key', Js(0.0))
                while (var.get('_key')<var.get('_len')):
                    var.get('sources').put(var.get('_key'), var.get('arguments').get(var.get('_key')))
                    # update
                    (var.put('_key',Js(var.get('_key').to_number())+Js(1))-Js(1))
                return var.get('_utils').get('extend').callprop('apply', var.get('undefined'), Js([var.get('_Object$create')(var.get(u"null"))]).callprop('concat', var.get('sources')))
            PyJsHoisted_createNewLookupObject_.func_name = 'createNewLookupObject'
            var.put('createNewLookupObject', PyJsHoisted_createNewLookupObject_)
            Js('use strict')
            var.put('_Object$create', var.get('__webpack_require__')(Js(74.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('createNewLookupObject', var.get('createNewLookupObject'))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            pass
        PyJs_anonymous_206_._set_name('anonymous')
        @Js
        def PyJs_anonymous_207_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'SafeString', 'exports'])
            @Js
            def PyJsHoisted_SafeString_(string, this, arguments, var=var):
                var = Scope({'string':string, 'this':this, 'arguments':arguments}, var)
                var.registers(['string'])
                var.get(u"this").put('string', var.get('string'))
            PyJsHoisted_SafeString_.func_name = 'SafeString'
            var.put('SafeString', PyJsHoisted_SafeString_)
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            pass
            @Js
            def PyJs_anonymous_208_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return (Js('')+var.get(u"this").get('string'))
            PyJs_anonymous_208_._set_name('anonymous')
            var.get('SafeString').get('prototype').put('toString', var.get('SafeString').get('prototype').put('toHTML', PyJs_anonymous_208_))
            var.get('exports').put('default', var.get('SafeString'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_207_._set_name('anonymous')
        @Js
        def PyJs_anonymous_209_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_internalProtoAccess', 'invokePartial', 'initData', 'module', 'Utils', '_interopRequireDefault', '_exception2', '_helpers', 'executeDecorators', '_Object$seal', 'noop', 'checkRevision', 'passLookupPropertyOption', '_interopRequireWildcard', '_Object$keys', '_utils', '__webpack_require__', '_base', 'wrapHelpersToPassLookupProperty', 'exports', 'template', '_internalWrapHelper', '_exception', 'wrapProgram', 'resolvePartial'])
            @Js
            def PyJsHoisted_checkRevision_(compilerInfo, this, arguments, var=var):
                var = Scope({'compilerInfo':compilerInfo, 'this':this, 'arguments':arguments}, var)
                var.registers(['runtimeVersions', 'currentRevision', 'compilerRevision', 'compilerVersions', 'compilerInfo'])
                var.put('compilerRevision', ((var.get('compilerInfo') and var.get('compilerInfo').get('0')) or Js(1.0)))
                var.put('currentRevision', var.get('_base').get('COMPILER_REVISION'))
                if ((var.get('compilerRevision')>=var.get('_base').get('LAST_COMPATIBLE_COMPILER_REVISION')) and (var.get('compilerRevision')<=var.get('_base').get('COMPILER_REVISION'))):
                    return var.get('undefined')
                if (var.get('compilerRevision')<var.get('_base').get('LAST_COMPATIBLE_COMPILER_REVISION')):
                    var.put('runtimeVersions', var.get('_base').get('REVISION_CHANGES').get(var.get('currentRevision')))
                    var.put('compilerVersions', var.get('_base').get('REVISION_CHANGES').get(var.get('compilerRevision')))
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((((((Js('Template was precompiled with an older version of Handlebars than the current runtime. ')+Js('Please update your precompiler to a newer version ('))+var.get('runtimeVersions'))+Js(') or downgrade your runtime to an older version ('))+var.get('compilerVersions'))+Js(').'))))
                    raise PyJsTempException
                else:
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((((Js('Template was precompiled with a newer version of Handlebars than the current runtime. ')+Js('Please update your runtime to a newer version ('))+var.get('compilerInfo').get('1'))+Js(').'))))
                    raise PyJsTempException
            PyJsHoisted_checkRevision_.func_name = 'checkRevision'
            var.put('checkRevision', PyJsHoisted_checkRevision_)
            @Js
            def PyJsHoisted_template_(templateSpec, env, this, arguments, var=var):
                var = Scope({'templateSpec':templateSpec, 'env':env, 'this':this, 'arguments':arguments}, var)
                var.registers(['templateSpec', 'invokePartialWrapper', 'container', 'templateWasPrecompiledWithCompilerV7', 'env', 'ret'])
                @Js
                def PyJsHoisted_invokePartialWrapper_(partial, context, options, this, arguments, var=var):
                    var = Scope({'partial':partial, 'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['context', 'l', 'i', 'lines', 'result', 'options', 'partial', 'extendedOptions'])
                    if var.get('options').get('hash'):
                        var.put('context', var.get('Utils').callprop('extend', Js({}), var.get('context'), var.get('options').get('hash')))
                        if var.get('options').get('ids'):
                            var.get('options').get('ids').put('0', Js(True))
                    var.put('partial', var.get('env').get('VM').get('resolvePartial').callprop('call', var.get(u"this"), var.get('partial'), var.get('context'), var.get('options')))
                    var.put('extendedOptions', var.get('Utils').callprop('extend', Js({}), var.get('options'), Js({'hooks':var.get(u"this").get('hooks'),'protoAccessControl':var.get(u"this").get('protoAccessControl')})))
                    var.put('result', var.get('env').get('VM').get('invokePartial').callprop('call', var.get(u"this"), var.get('partial'), var.get('context'), var.get('extendedOptions')))
                    if ((var.get('result')==var.get(u"null")) and var.get('env').get('compile')):
                        var.get('options').get('partials').put(var.get('options').get('name'), var.get('env').callprop('compile', var.get('partial'), var.get('templateSpec').get('compilerOptions'), var.get('env')))
                        var.put('result', var.get('options').get('partials').callprop(var.get('options').get('name'), var.get('context'), var.get('extendedOptions')))
                    if (var.get('result')!=var.get(u"null")):
                        if var.get('options').get('indent'):
                            var.put('lines', var.get('result').callprop('split', Js('\n')))
                            #for JS loop
                            var.put('i', Js(0.0))
                            var.put('l', var.get('lines').get('length'))
                            while (var.get('i')<var.get('l')):
                                if (var.get('lines').get(var.get('i')).neg() and PyJsStrictEq((var.get('i')+Js(1.0)),var.get('l'))):
                                    break
                                var.get('lines').put(var.get('i'), (var.get('options').get('indent')+var.get('lines').get(var.get('i'))))
                                # update
                                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                            var.put('result', var.get('lines').callprop('join', Js('\n')))
                        return var.get('result')
                    else:
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(((Js('The partial ')+var.get('options').get('name'))+Js(' could not be compiled when running in runtime-only mode'))))
                        raise PyJsTempException
                PyJsHoisted_invokePartialWrapper_.func_name = 'invokePartialWrapper'
                var.put('invokePartialWrapper', PyJsHoisted_invokePartialWrapper_)
                @Js
                def PyJsHoisted_ret_(context, this, arguments, var=var):
                    var = Scope({'context':context, 'this':this, 'arguments':arguments}, var)
                    var.registers(['context', 'depths', 'main', 'options', 'data', 'blockParams'])
                    @Js
                    def PyJsHoisted_main_(context, this, arguments, var=var):
                        var = Scope({'context':context, 'this':this, 'arguments':arguments}, var)
                        var.registers(['context'])
                        return (Js('')+var.get('templateSpec').callprop('main', var.get('container'), var.get('context'), var.get('container').get('helpers'), var.get('container').get('partials'), var.get('data'), var.get('blockParams'), var.get('depths')))
                    PyJsHoisted_main_.func_name = 'main'
                    var.put('main', PyJsHoisted_main_)
                    var.put('options', (Js({}) if ((var.get('arguments').get('length')<=Js(1.0)) or PyJsStrictEq(var.get('arguments').get('1'),var.get('undefined'))) else var.get('arguments').get('1')))
                    var.put('data', var.get('options').get('data'))
                    var.get('ret').callprop('_setup', var.get('options'))
                    if (var.get('options').get('partial').neg() and var.get('templateSpec').get('useData')):
                        var.put('data', var.get('initData')(var.get('context'), var.get('data')))
                    var.put('depths', var.get('undefined'))
                    var.put('blockParams', (Js([]) if var.get('templateSpec').get('useBlockParams') else var.get('undefined')))
                    if var.get('templateSpec').get('useDepths'):
                        if var.get('options').get('depths'):
                            var.put('depths', (Js([var.get('context')]).callprop('concat', var.get('options').get('depths')) if (var.get('context')!=var.get('options').get('depths').get('0')) else var.get('options').get('depths')))
                        else:
                            var.put('depths', Js([var.get('context')]))
                    pass
                    var.put('main', var.get('executeDecorators')(var.get('templateSpec').get('main'), var.get('main'), var.get('container'), (var.get('options').get('depths') or Js([])), var.get('data'), var.get('blockParams')))
                    return var.get('main')(var.get('context'), var.get('options'))
                PyJsHoisted_ret_.func_name = 'ret'
                var.put('ret', PyJsHoisted_ret_)
                if var.get('env').neg():
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('No environment passed to template')))
                    raise PyJsTempException
                if (var.get('templateSpec').neg() or var.get('templateSpec').get('main').neg()):
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('Unknown template object: ')+var.get('templateSpec',throw=False).typeof())))
                    raise PyJsTempException
                var.get('templateSpec').get('main').put('decorator', var.get('templateSpec').get('main_d'))
                var.get('env').get('VM').callprop('checkRevision', var.get('templateSpec').get('compiler'))
                var.put('templateWasPrecompiledWithCompilerV7', (var.get('templateSpec').get('compiler') and PyJsStrictEq(var.get('templateSpec').get('compiler').get('0'),Js(7.0))))
                pass
                @Js
                def PyJs_strict_210_(obj, name, loc, this, arguments, var=var):
                    var = Scope({'obj':obj, 'name':name, 'loc':loc, 'this':this, 'arguments':arguments, 'strict':PyJs_strict_210_}, var)
                    var.registers(['obj', 'name', 'loc'])
                    if (var.get('obj').neg() or var.get('obj').contains(var.get('name')).neg()):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((((Js('"')+var.get('name'))+Js('" not defined in '))+var.get('obj')), Js({'loc':var.get('loc')})))
                        raise PyJsTempException
                    return var.get('container').callprop('lookupProperty', var.get('obj'), var.get('name'))
                PyJs_strict_210_._set_name('strict')
                @Js
                def PyJs_lookupProperty_211_(parent, propertyName, this, arguments, var=var):
                    var = Scope({'parent':parent, 'propertyName':propertyName, 'this':this, 'arguments':arguments, 'lookupProperty':PyJs_lookupProperty_211_}, var)
                    var.registers(['result', 'parent', 'propertyName'])
                    var.put('result', var.get('parent').get(var.get('propertyName')))
                    if (var.get('result')==var.get(u"null")):
                        return var.get('result')
                    if var.get('Object').get('prototype').get('hasOwnProperty').callprop('call', var.get('parent'), var.get('propertyName')):
                        return var.get('result')
                    if var.get('_internalProtoAccess').callprop('resultIsAllowed', var.get('result'), var.get('container').get('protoAccessControl'), var.get('propertyName')):
                        return var.get('result')
                    return var.get('undefined')
                PyJs_lookupProperty_211_._set_name('lookupProperty')
                @Js
                def PyJs_lookup_212_(depths, name, this, arguments, var=var):
                    var = Scope({'depths':depths, 'name':name, 'this':this, 'arguments':arguments, 'lookup':PyJs_lookup_212_}, var)
                    var.registers(['i', 'len', 'depths', 'name', 'result'])
                    var.put('len', var.get('depths').get('length'))
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('len')):
                        var.put('result', (var.get('depths').get(var.get('i')) and var.get('container').callprop('lookupProperty', var.get('depths').get(var.get('i')), var.get('name'))))
                        if (var.get('result')!=var.get(u"null")):
                            return var.get('depths').get(var.get('i')).get(var.get('name'))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_lookup_212_._set_name('lookup')
                @Js
                def PyJs_InlineNonPyName_213_(current, context, this, arguments, var=var):
                    var = Scope({'current':current, 'context':context, 'this':this, 'arguments':arguments, 'lambda':PyJs_InlineNonPyName_213_}, var)
                    var.registers(['context', 'current'])
                    return (var.get('current').callprop('call', var.get('context')) if PyJsStrictEq(var.get('current',throw=False).typeof(),Js('function')) else var.get('current'))
                PyJs_InlineNonPyName_213_._set_name('lambda')
                @Js
                def PyJs_fn_214_(i, this, arguments, var=var):
                    var = Scope({'i':i, 'this':this, 'arguments':arguments, 'fn':PyJs_fn_214_}, var)
                    var.registers(['ret', 'i'])
                    var.put('ret', var.get('templateSpec').get(var.get('i')))
                    var.get('ret').put('decorator', var.get('templateSpec').get((var.get('i')+Js('_d'))))
                    return var.get('ret')
                PyJs_fn_214_._set_name('fn')
                @Js
                def PyJs_program_215_(i, data, declaredBlockParams, blockParams, depths, this, arguments, var=var):
                    var = Scope({'i':i, 'data':data, 'declaredBlockParams':declaredBlockParams, 'blockParams':blockParams, 'depths':depths, 'this':this, 'arguments':arguments, 'program':PyJs_program_215_}, var)
                    var.registers(['i', 'depths', 'fn', 'data', 'blockParams', 'declaredBlockParams', 'programWrapper'])
                    var.put('programWrapper', var.get(u"this").get('programs').get(var.get('i')))
                    var.put('fn', var.get(u"this").callprop('fn', var.get('i')))
                    if (((var.get('data') or var.get('depths')) or var.get('blockParams')) or var.get('declaredBlockParams')):
                        var.put('programWrapper', var.get('wrapProgram')(var.get(u"this"), var.get('i'), var.get('fn'), var.get('data'), var.get('declaredBlockParams'), var.get('blockParams'), var.get('depths')))
                    else:
                        if var.get('programWrapper').neg():
                            var.put('programWrapper', var.get(u"this").get('programs').put(var.get('i'), var.get('wrapProgram')(var.get(u"this"), var.get('i'), var.get('fn'))))
                    return var.get('programWrapper')
                PyJs_program_215_._set_name('program')
                @Js
                def PyJs_data_216_(value, depth, this, arguments, var=var):
                    var = Scope({'value':value, 'depth':depth, 'this':this, 'arguments':arguments, 'data':PyJs_data_216_}, var)
                    var.registers(['depth', 'value'])
                    while (var.get('value') and (var.put('depth',Js(var.get('depth').to_number())-Js(1))+Js(1))):
                        var.put('value', var.get('value').get('_parent'))
                    return var.get('value')
                PyJs_data_216_._set_name('data')
                @Js
                def PyJs_mergeIfNeeded_217_(param, common, this, arguments, var=var):
                    var = Scope({'param':param, 'common':common, 'this':this, 'arguments':arguments, 'mergeIfNeeded':PyJs_mergeIfNeeded_217_}, var)
                    var.registers(['obj', 'param', 'common'])
                    var.put('obj', (var.get('param') or var.get('common')))
                    if ((var.get('param') and var.get('common')) and PyJsStrictNeq(var.get('param'),var.get('common'))):
                        var.put('obj', var.get('Utils').callprop('extend', Js({}), var.get('common'), var.get('param')))
                    return var.get('obj')
                PyJs_mergeIfNeeded_217_._set_name('mergeIfNeeded')
                var.put('container', Js({'strict':PyJs_strict_210_,'lookupProperty':PyJs_lookupProperty_211_,'lookup':PyJs_lookup_212_,'lambda':PyJs_InlineNonPyName_213_,'escapeExpression':var.get('Utils').get('escapeExpression'),'invokePartial':var.get('invokePartialWrapper'),'fn':PyJs_fn_214_,'programs':Js([]),'program':PyJs_program_215_,'data':PyJs_data_216_,'mergeIfNeeded':PyJs_mergeIfNeeded_217_,'nullContext':var.get('_Object$seal')(Js({})),'noop':var.get('env').get('VM').get('noop'),'compilerInfo':var.get('templateSpec').get('compiler')}))
                pass
                var.get('ret').put('isTop', Js(True))
                @Js
                def PyJs_anonymous_218_(options, this, arguments, var=var):
                    var = Scope({'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['mergedHelpers', 'options', 'keepHelperInHelpers'])
                    if var.get('options').get('partial').neg():
                        var.put('mergedHelpers', var.get('Utils').callprop('extend', Js({}), var.get('env').get('helpers'), var.get('options').get('helpers')))
                        var.get('wrapHelpersToPassLookupProperty')(var.get('mergedHelpers'), var.get('container'))
                        var.get('container').put('helpers', var.get('mergedHelpers'))
                        if var.get('templateSpec').get('usePartial'):
                            var.get('container').put('partials', var.get('container').callprop('mergeIfNeeded', var.get('options').get('partials'), var.get('env').get('partials')))
                        if (var.get('templateSpec').get('usePartial') or var.get('templateSpec').get('useDecorators')):
                            var.get('container').put('decorators', var.get('Utils').callprop('extend', Js({}), var.get('env').get('decorators'), var.get('options').get('decorators')))
                        var.get('container').put('hooks', Js({}))
                        var.get('container').put('protoAccessControl', var.get('_internalProtoAccess').callprop('createProtoAccessControl', var.get('options')))
                        var.put('keepHelperInHelpers', (var.get('options').get('allowCallsToHelperMissing') or var.get('templateWasPrecompiledWithCompilerV7')))
                        var.get('_helpers').callprop('moveHelperToHooks', var.get('container'), Js('helperMissing'), var.get('keepHelperInHelpers'))
                        var.get('_helpers').callprop('moveHelperToHooks', var.get('container'), Js('blockHelperMissing'), var.get('keepHelperInHelpers'))
                    else:
                        var.get('container').put('protoAccessControl', var.get('options').get('protoAccessControl'))
                        var.get('container').put('helpers', var.get('options').get('helpers'))
                        var.get('container').put('partials', var.get('options').get('partials'))
                        var.get('container').put('decorators', var.get('options').get('decorators'))
                        var.get('container').put('hooks', var.get('options').get('hooks'))
                PyJs_anonymous_218_._set_name('anonymous')
                var.get('ret').put('_setup', PyJs_anonymous_218_)
                @Js
                def PyJs_anonymous_219_(i, data, blockParams, depths, this, arguments, var=var):
                    var = Scope({'i':i, 'data':data, 'blockParams':blockParams, 'depths':depths, 'this':this, 'arguments':arguments}, var)
                    var.registers(['depths', 'data', 'blockParams', 'i'])
                    if (var.get('templateSpec').get('useBlockParams') and var.get('blockParams').neg()):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('must pass block params')))
                        raise PyJsTempException
                    if (var.get('templateSpec').get('useDepths') and var.get('depths').neg()):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('must pass parent depths')))
                        raise PyJsTempException
                    return var.get('wrapProgram')(var.get('container'), var.get('i'), var.get('templateSpec').get(var.get('i')), var.get('data'), Js(0.0), var.get('blockParams'), var.get('depths'))
                PyJs_anonymous_219_._set_name('anonymous')
                var.get('ret').put('_child', PyJs_anonymous_219_)
                return var.get('ret')
            PyJsHoisted_template_.func_name = 'template'
            var.put('template', PyJsHoisted_template_)
            @Js
            def PyJsHoisted_wrapProgram_(container, i, fn, data, declaredBlockParams, blockParams, depths, this, arguments, var=var):
                var = Scope({'container':container, 'i':i, 'fn':fn, 'data':data, 'declaredBlockParams':declaredBlockParams, 'blockParams':blockParams, 'depths':depths, 'this':this, 'arguments':arguments}, var)
                var.registers(['i', 'container', 'depths', 'prog', 'fn', 'data', 'blockParams', 'declaredBlockParams'])
                @Js
                def PyJsHoisted_prog_(context, this, arguments, var=var):
                    var = Scope({'context':context, 'this':this, 'arguments':arguments}, var)
                    var.registers(['currentDepths', 'options', 'context'])
                    var.put('options', (Js({}) if ((var.get('arguments').get('length')<=Js(1.0)) or PyJsStrictEq(var.get('arguments').get('1'),var.get('undefined'))) else var.get('arguments').get('1')))
                    var.put('currentDepths', var.get('depths'))
                    if ((var.get('depths') and (var.get('context')!=var.get('depths').get('0'))) and (PyJsStrictEq(var.get('context'),var.get('container').get('nullContext')) and PyJsStrictEq(var.get('depths').get('0'),var.get(u"null"))).neg()):
                        var.put('currentDepths', Js([var.get('context')]).callprop('concat', var.get('depths')))
                    return var.get('fn')(var.get('container'), var.get('context'), var.get('container').get('helpers'), var.get('container').get('partials'), (var.get('options').get('data') or var.get('data')), (var.get('blockParams') and Js([var.get('options').get('blockParams')]).callprop('concat', var.get('blockParams'))), var.get('currentDepths'))
                PyJsHoisted_prog_.func_name = 'prog'
                var.put('prog', PyJsHoisted_prog_)
                pass
                var.put('prog', var.get('executeDecorators')(var.get('fn'), var.get('prog'), var.get('container'), var.get('depths'), var.get('data'), var.get('blockParams')))
                var.get('prog').put('program', var.get('i'))
                var.get('prog').put('depth', (var.get('depths').get('length') if var.get('depths') else Js(0.0)))
                var.get('prog').put('blockParams', (var.get('declaredBlockParams') or Js(0.0)))
                return var.get('prog')
            PyJsHoisted_wrapProgram_.func_name = 'wrapProgram'
            var.put('wrapProgram', PyJsHoisted_wrapProgram_)
            @Js
            def PyJsHoisted_resolvePartial_(partial, context, options, this, arguments, var=var):
                var = Scope({'partial':partial, 'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                var.registers(['context', 'options', 'partial'])
                if var.get('partial').neg():
                    if PyJsStrictEq(var.get('options').get('name'),Js('@partial-block')):
                        var.put('partial', var.get('options').get('data').get('partial-block'))
                    else:
                        var.put('partial', var.get('options').get('partials').get(var.get('options').get('name')))
                else:
                    if (var.get('partial').get('call').neg() and var.get('options').get('name').neg()):
                        var.get('options').put('name', var.get('partial'))
                        var.put('partial', var.get('options').get('partials').get(var.get('partial')))
                return var.get('partial')
            PyJsHoisted_resolvePartial_.func_name = 'resolvePartial'
            var.put('resolvePartial', PyJsHoisted_resolvePartial_)
            @Js
            def PyJsHoisted_invokePartial_(partial, context, options, this, arguments, var=var):
                var = Scope({'partial':partial, 'context':context, 'options':options, 'this':this, 'arguments':arguments}, var)
                var.registers(['context', 'currentPartialBlock', 'partialBlock', 'options', 'partial'])
                var.put('currentPartialBlock', (var.get('options').get('data') and var.get('options').get('data').get('partial-block')))
                var.get('options').put('partial', Js(True))
                if var.get('options').get('ids'):
                    var.get('options').get('data').put('contextPath', (var.get('options').get('ids').get('0') or var.get('options').get('data').get('contextPath')))
                var.put('partialBlock', var.get('undefined'))
                if (var.get('options').get('fn') and PyJsStrictNeq(var.get('options').get('fn'),var.get('noop'))):
                    @Js
                    def PyJs_anonymous_220_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments}, var)
                        var.registers(['fn'])
                        var.get('options').put('data', var.get('_base').callprop('createFrame', var.get('options').get('data')))
                        var.put('fn', var.get('options').get('fn'))
                        @Js
                        def PyJs_partialBlockWrapper_221_(context, this, arguments, var=var):
                            var = Scope({'context':context, 'this':this, 'arguments':arguments, 'partialBlockWrapper':PyJs_partialBlockWrapper_221_}, var)
                            var.registers(['context', 'options'])
                            var.put('options', (Js({}) if ((var.get('arguments').get('length')<=Js(1.0)) or PyJsStrictEq(var.get('arguments').get('1'),var.get('undefined'))) else var.get('arguments').get('1')))
                            var.get('options').put('data', var.get('_base').callprop('createFrame', var.get('options').get('data')))
                            var.get('options').get('data').put('partial-block', var.get('currentPartialBlock'))
                            return var.get('fn')(var.get('context'), var.get('options'))
                        PyJs_partialBlockWrapper_221_._set_name('partialBlockWrapper')
                        var.put('partialBlock', var.get('options').get('data').put('partial-block', PyJs_partialBlockWrapper_221_))
                        if var.get('fn').get('partials'):
                            var.get('options').put('partials', var.get('Utils').callprop('extend', Js({}), var.get('options').get('partials'), var.get('fn').get('partials')))
                    PyJs_anonymous_220_._set_name('anonymous')
                    PyJs_anonymous_220_()
                if (PyJsStrictEq(var.get('partial'),var.get('undefined')) and var.get('partialBlock')):
                    var.put('partial', var.get('partialBlock'))
                if PyJsStrictEq(var.get('partial'),var.get('undefined')):
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(((Js('The partial ')+var.get('options').get('name'))+Js(' could not be found'))))
                    raise PyJsTempException
                else:
                    if var.get('partial').instanceof(var.get('Function')):
                        return var.get('partial')(var.get('context'), var.get('options'))
            PyJsHoisted_invokePartial_.func_name = 'invokePartial'
            var.put('invokePartial', PyJsHoisted_invokePartial_)
            @Js
            def PyJsHoisted_noop_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return Js('')
            PyJsHoisted_noop_.func_name = 'noop'
            var.put('noop', PyJsHoisted_noop_)
            @Js
            def PyJsHoisted_initData_(context, data, this, arguments, var=var):
                var = Scope({'context':context, 'data':data, 'this':this, 'arguments':arguments}, var)
                var.registers(['context', 'data'])
                if (var.get('data').neg() or var.get('data').contains(Js('root')).neg()):
                    var.put('data', (var.get('_base').callprop('createFrame', var.get('data')) if var.get('data') else Js({})))
                    var.get('data').put('root', var.get('context'))
                return var.get('data')
            PyJsHoisted_initData_.func_name = 'initData'
            var.put('initData', PyJsHoisted_initData_)
            @Js
            def PyJsHoisted_executeDecorators_(fn, prog, container, depths, data, blockParams, this, arguments, var=var):
                var = Scope({'fn':fn, 'prog':prog, 'container':container, 'depths':depths, 'data':data, 'blockParams':blockParams, 'this':this, 'arguments':arguments}, var)
                var.registers(['container', 'depths', 'prog', 'fn', 'props', 'data', 'blockParams'])
                if var.get('fn').get('decorator'):
                    var.put('props', Js({}))
                    var.put('prog', var.get('fn').callprop('decorator', var.get('prog'), var.get('props'), var.get('container'), (var.get('depths') and var.get('depths').get('0')), var.get('data'), var.get('blockParams'), var.get('depths')))
                    var.get('Utils').callprop('extend', var.get('prog'), var.get('props'))
                return var.get('prog')
            PyJsHoisted_executeDecorators_.func_name = 'executeDecorators'
            var.put('executeDecorators', PyJsHoisted_executeDecorators_)
            @Js
            def PyJsHoisted_wrapHelpersToPassLookupProperty_(mergedHelpers, container, this, arguments, var=var):
                var = Scope({'mergedHelpers':mergedHelpers, 'container':container, 'this':this, 'arguments':arguments}, var)
                var.registers(['mergedHelpers', 'container'])
                @Js
                def PyJs_anonymous_222_(helperName, this, arguments, var=var):
                    var = Scope({'helperName':helperName, 'this':this, 'arguments':arguments}, var)
                    var.registers(['helper', 'helperName'])
                    var.put('helper', var.get('mergedHelpers').get(var.get('helperName')))
                    var.get('mergedHelpers').put(var.get('helperName'), var.get('passLookupPropertyOption')(var.get('helper'), var.get('container')))
                PyJs_anonymous_222_._set_name('anonymous')
                var.get('_Object$keys')(var.get('mergedHelpers')).callprop('forEach', PyJs_anonymous_222_)
            PyJsHoisted_wrapHelpersToPassLookupProperty_.func_name = 'wrapHelpersToPassLookupProperty'
            var.put('wrapHelpersToPassLookupProperty', PyJsHoisted_wrapHelpersToPassLookupProperty_)
            @Js
            def PyJsHoisted_passLookupPropertyOption_(helper, container, this, arguments, var=var):
                var = Scope({'helper':helper, 'container':container, 'this':this, 'arguments':arguments}, var)
                var.registers(['lookupProperty', 'container', 'helper'])
                var.put('lookupProperty', var.get('container').get('lookupProperty'))
                @Js
                def PyJs_anonymous_223_(options, this, arguments, var=var):
                    var = Scope({'options':options, 'this':this, 'arguments':arguments}, var)
                    var.registers(['options'])
                    return var.get('Utils').callprop('extend', Js({'lookupProperty':var.get('lookupProperty')}), var.get('options'))
                PyJs_anonymous_223_._set_name('anonymous')
                return var.get('_internalWrapHelper').callprop('wrapHelper', var.get('helper'), PyJs_anonymous_223_)
            PyJsHoisted_passLookupPropertyOption_.func_name = 'passLookupPropertyOption'
            var.put('passLookupPropertyOption', PyJsHoisted_passLookupPropertyOption_)
            Js('use strict')
            var.put('_Object$seal', var.get('__webpack_require__')(Js(79.0)).get('default'))
            var.put('_Object$keys', var.get('__webpack_require__')(Js(60.0)).get('default'))
            var.put('_interopRequireWildcard', var.get('__webpack_require__')(Js(3.0)).get('default'))
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('checkRevision', var.get('checkRevision'))
            var.get('exports').put('template', var.get('template'))
            var.get('exports').put('wrapProgram', var.get('wrapProgram'))
            var.get('exports').put('resolvePartial', var.get('resolvePartial'))
            var.get('exports').put('invokePartial', var.get('invokePartial'))
            var.get('exports').put('noop', var.get('noop'))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('Utils', var.get('_interopRequireWildcard')(var.get('_utils')))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            var.put('_base', var.get('__webpack_require__')(Js(4.0)))
            var.put('_helpers', var.get('__webpack_require__')(Js(10.0)))
            var.put('_internalWrapHelper', var.get('__webpack_require__')(Js(82.0)))
            var.put('_internalProtoAccess', var.get('__webpack_require__')(Js(73.0)))
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
        PyJs_anonymous_209_._set_name('anonymous')
        @Js
        def PyJs_anonymous_224_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('module').put('exports', Js({'default':var.get('__webpack_require__')(Js(80.0)),'__esModule':Js(True)}))
        PyJs_anonymous_224_._set_name('anonymous')
        @Js
        def PyJs_anonymous_225_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', '__webpack_require__', 'exports'])
            var.get('__webpack_require__')(Js(81.0))
            var.get('module').put('exports', var.get('__webpack_require__')(Js(21.0)).get('Object').get('seal'))
        PyJs_anonymous_225_._set_name('anonymous')
        @Js
        def PyJs_anonymous_226_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports', '__webpack_require__', 'isObject'])
            var.put('isObject', var.get('__webpack_require__')(Js(40.0)))
            @Js
            def PyJs_anonymous_227_(PyJsArg_247365616c_, this, arguments, var=var):
                var = Scope({'$seal':PyJsArg_247365616c_, 'this':this, 'arguments':arguments}, var)
                var.registers(['$seal'])
                @Js
                def PyJs_seal_228_(it, this, arguments, var=var):
                    var = Scope({'it':it, 'this':this, 'arguments':arguments, 'seal':PyJs_seal_228_}, var)
                    var.registers(['it'])
                    return (var.get('$seal')(var.get('it')) if (var.get('$seal') and var.get('isObject')(var.get('it'))) else var.get('it'))
                PyJs_seal_228_._set_name('seal')
                return PyJs_seal_228_
            PyJs_anonymous_227_._set_name('anonymous')
            var.get('__webpack_require__')(Js(64.0))(Js('seal'), PyJs_anonymous_227_)
        PyJs_anonymous_226_._set_name('anonymous')
        @Js
        def PyJs_anonymous_229_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['wrapHelper', 'module', 'exports'])
            @Js
            def PyJsHoisted_wrapHelper_(helper, transformOptionsFn, this, arguments, var=var):
                var = Scope({'helper':helper, 'transformOptionsFn':transformOptionsFn, 'this':this, 'arguments':arguments}, var)
                var.registers(['wrapper', 'helper', 'transformOptionsFn'])
                if PyJsStrictNeq(var.get('helper',throw=False).typeof(),Js('function')):
                    return var.get('helper')
                @Js
                def PyJs_wrapper_230_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'wrapper':PyJs_wrapper_230_}, var)
                    var.registers(['options'])
                    var.put('options', var.get('arguments').get((var.get('arguments').get('length')-Js(1.0))))
                    var.get('arguments').put((var.get('arguments').get('length')-Js(1.0)), var.get('transformOptionsFn')(var.get('options')))
                    return var.get('helper').callprop('apply', var.get(u"this"), var.get('arguments'))
                PyJs_wrapper_230_._set_name('wrapper')
                var.put('wrapper', PyJs_wrapper_230_)
                return var.get('wrapper')
            PyJsHoisted_wrapHelper_.func_name = 'wrapHelper'
            var.put('wrapHelper', PyJsHoisted_wrapHelper_)
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('wrapHelper', var.get('wrapHelper'))
            pass
        PyJs_anonymous_229_._set_name('anonymous')
        @Js
        def PyJs_anonymous_231_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'exports'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            @Js
            def PyJs_anonymous_232_(Handlebars, this, arguments, var=var):
                var = Scope({'Handlebars':Handlebars, 'this':this, 'arguments':arguments}, var)
                var.registers(['Handlebars', '$Handlebars'])
                @Js
                def PyJs_anonymous_233_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    if PyJsStrictEq(var.get('globalThis',throw=False).typeof(),Js('object')):
                        return var.get('undefined')
                    @Js
                    def PyJs_anonymous_234_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments}, var)
                        var.registers([])
                        return var.get(u"this")
                    PyJs_anonymous_234_._set_name('anonymous')
                    var.get('Object').get('prototype').callprop('__defineGetter__', Js('__magic__'), PyJs_anonymous_234_)
                    var.get('__magic__').put('globalThis', var.get('__magic__'))
                    var.get('Object').get('prototype').delete('__magic__')
                PyJs_anonymous_233_._set_name('anonymous')
                PyJs_anonymous_233_()
                var.put('$Handlebars', var.get('globalThis').get('Handlebars'))
                @Js
                def PyJs_anonymous_235_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    if PyJsStrictEq(var.get('globalThis').get('Handlebars'),var.get('Handlebars')):
                        var.get('globalThis').put('Handlebars', var.get('$Handlebars'))
                    return var.get('Handlebars')
                PyJs_anonymous_235_._set_name('anonymous')
                var.get('Handlebars').put('noConflict', PyJs_anonymous_235_)
            PyJs_anonymous_232_._set_name('anonymous')
            var.get('exports').put('default', PyJs_anonymous_232_)
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_231_._set_name('anonymous')
        @Js
        def PyJs_anonymous_236_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['AST', 'exports', 'module'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            @Js
            def PyJs_helperExpression_237_(node, this, arguments, var=var):
                var = Scope({'node':node, 'this':this, 'arguments':arguments, 'helperExpression':PyJs_helperExpression_237_}, var)
                var.registers(['node'])
                return (PyJsStrictEq(var.get('node').get('type'),Js('SubExpression')) or ((PyJsStrictEq(var.get('node').get('type'),Js('MustacheStatement')) or PyJsStrictEq(var.get('node').get('type'),Js('BlockStatement'))) and ((var.get('node').get('params') and var.get('node').get('params').get('length')) or var.get('node').get('hash')).neg().neg()))
            PyJs_helperExpression_237_._set_name('helperExpression')
            @Js
            def PyJs_scopedId_238_(path, this, arguments, var=var):
                var = Scope({'path':path, 'this':this, 'arguments':arguments, 'scopedId':PyJs_scopedId_238_}, var)
                var.registers(['path'])
                return JsRegExp('/^\\.|this\\b/').callprop('test', var.get('path').get('original'))
            PyJs_scopedId_238_._set_name('scopedId')
            @Js
            def PyJs_simpleId_239_(path, this, arguments, var=var):
                var = Scope({'path':path, 'this':this, 'arguments':arguments, 'simpleId':PyJs_simpleId_239_}, var)
                var.registers(['path'])
                return ((PyJsStrictEq(var.get('path').get('parts').get('length'),Js(1.0)) and var.get('AST').get('helpers').callprop('scopedId', var.get('path')).neg()) and var.get('path').get('depth').neg())
            PyJs_simpleId_239_._set_name('simpleId')
            var.put('AST', Js({'helpers':Js({'helperExpression':PyJs_helperExpression_237_,'scopedId':PyJs_scopedId_238_,'simpleId':PyJs_simpleId_239_})}))
            var.get('exports').put('default', var.get('AST'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_236_._set_name('anonymous')
        @Js
        def PyJs_anonymous_240_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_parser2', '_interopRequireDefault', 'exports', '_helpers', '_whitespaceControl', 'parseWithoutProcessing', '_whitespaceControl2', 'Helpers', 'module', '_interopRequireWildcard', '__webpack_require__', '_utils', '_parser', 'yy', 'parse'])
            @Js
            def PyJsHoisted_parseWithoutProcessing_(input, options, this, arguments, var=var):
                var = Scope({'input':input, 'options':options, 'this':this, 'arguments':arguments}, var)
                var.registers(['options', 'ast', 'input'])
                if PyJsStrictEq(var.get('input').get('type'),Js('Program')):
                    return var.get('input')
                var.get('_parser2').get('default').put('yy', var.get('yy'))
                @Js
                def PyJs_anonymous_241_(locInfo, this, arguments, var=var):
                    var = Scope({'locInfo':locInfo, 'this':this, 'arguments':arguments}, var)
                    var.registers(['locInfo'])
                    return var.get('yy').get('SourceLocation').create((var.get('options') and var.get('options').get('srcName')), var.get('locInfo'))
                PyJs_anonymous_241_._set_name('anonymous')
                var.get('yy').put('locInfo', PyJs_anonymous_241_)
                var.put('ast', var.get('_parser2').get('default').callprop('parse', var.get('input')))
                return var.get('ast')
            PyJsHoisted_parseWithoutProcessing_.func_name = 'parseWithoutProcessing'
            var.put('parseWithoutProcessing', PyJsHoisted_parseWithoutProcessing_)
            @Js
            def PyJsHoisted_parse_(input, options, this, arguments, var=var):
                var = Scope({'input':input, 'options':options, 'this':this, 'arguments':arguments}, var)
                var.registers(['options', 'strip', 'ast', 'input'])
                var.put('ast', var.get('parseWithoutProcessing')(var.get('input'), var.get('options')))
                var.put('strip', var.get('_whitespaceControl2').get('default').create(var.get('options')))
                return var.get('strip').callprop('accept', var.get('ast'))
            PyJsHoisted_parse_.func_name = 'parse'
            var.put('parse', PyJsHoisted_parse_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.put('_interopRequireWildcard', var.get('__webpack_require__')(Js(3.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('parseWithoutProcessing', var.get('parseWithoutProcessing'))
            var.get('exports').put('parse', var.get('parse'))
            var.put('_parser', var.get('__webpack_require__')(Js(86.0)))
            var.put('_parser2', var.get('_interopRequireDefault')(var.get('_parser')))
            var.put('_whitespaceControl', var.get('__webpack_require__')(Js(87.0)))
            var.put('_whitespaceControl2', var.get('_interopRequireDefault')(var.get('_whitespaceControl')))
            var.put('_helpers', var.get('__webpack_require__')(Js(89.0)))
            var.put('Helpers', var.get('_interopRequireWildcard')(var.get('_helpers')))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.get('exports').put('parser', var.get('_parser2').get('default'))
            var.put('yy', Js({}))
            var.get('_utils').callprop('extend', var.get('yy'), var.get('Helpers'))
            pass
            pass
        PyJs_anonymous_240_._set_name('anonymous')
        @Js
        def PyJs_anonymous_242_(module, exports, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
            var.registers(['module', 'handlebars', 'exports'])
            Js('use strict')
            var.get('exports').put('__esModule', Js(True))
            @Js
            def PyJs_anonymous_243_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['Parser', 'lexer', 'parser'])
                @Js
                def PyJsHoisted_Parser_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    var.get(u"this").put('yy', Js({}))
                PyJsHoisted_Parser_.func_name = 'Parser'
                var.put('Parser', PyJsHoisted_Parser_)
                @Js
                def PyJs_trace_244_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'trace':PyJs_trace_244_}, var)
                    var.registers([])
                    pass
                PyJs_trace_244_._set_name('trace')
                @Js
                def PyJs_anonymous_245_(yytext, yyleng, yylineno, yy, yystate, PyJsArg_2424_, PyJsArg_5f24_, this, arguments, var=var):
                    var = Scope({'yytext':yytext, 'yyleng':yyleng, 'yylineno':yylineno, 'yy':yy, 'yystate':yystate, '$$':PyJsArg_2424_, '_$':PyJsArg_5f24_, 'this':this, 'arguments':arguments, 'anonymous':PyJs_anonymous_245_}, var)
                    var.registers(['program', '$$', 'yyleng', '$0', '_$', 'yytext', 'inverse', 'yylineno', 'yy', 'yystate'])
                    var.put('$0', (var.get('$$').get('length')-Js(1.0)))
                    while 1:
                        SWITCHED = False
                        CONDITION = (var.get('yystate'))
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
                            SWITCHED = True
                            return var.get('$$').get((var.get('$0')-Js(1.0)))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('prepareProgram', var.get('$$').get(var.get('$0'))))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(4.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(5.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(6.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(7.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(8.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(9.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('CommentStatement'),'value':var.get('yy').callprop('stripComment', var.get('$$').get(var.get('$0'))),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get(var.get('$0')), var.get('$$').get(var.get('$0'))),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(10.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('ContentStatement'),'original':var.get('$$').get(var.get('$0')),'value':var.get('$$').get(var.get('$0')),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(11.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('prepareRawBlock', var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get(var.get('$0')), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(12.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'path':var.get('$$').get((var.get('$0')-Js(3.0))),'params':var.get('$$').get((var.get('$0')-Js(2.0))),'hash':var.get('$$').get((var.get('$0')-Js(1.0)))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(13.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('prepareBlock', var.get('$$').get((var.get('$0')-Js(3.0))), var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get(var.get('$0')), Js(False), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(14.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('prepareBlock', var.get('$$').get((var.get('$0')-Js(3.0))), var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get(var.get('$0')), Js(True), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(15.0)):
                            SWITCHED = True
                            def PyJs_LONG_246_(var=var):
                                return var.get(u"this").put('$', Js({'open':var.get('$$').get((var.get('$0')-Js(5.0))),'path':var.get('$$').get((var.get('$0')-Js(4.0))),'params':var.get('$$').get((var.get('$0')-Js(3.0))),'hash':var.get('$$').get((var.get('$0')-Js(2.0))),'blockParams':var.get('$$').get((var.get('$0')-Js(1.0))),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(5.0))), var.get('$$').get(var.get('$0')))}))
                            PyJs_LONG_246_()
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(16.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'path':var.get('$$').get((var.get('$0')-Js(4.0))),'params':var.get('$$').get((var.get('$0')-Js(3.0))),'hash':var.get('$$').get((var.get('$0')-Js(2.0))),'blockParams':var.get('$$').get((var.get('$0')-Js(1.0))),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(5.0))), var.get('$$').get(var.get('$0')))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(17.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'path':var.get('$$').get((var.get('$0')-Js(4.0))),'params':var.get('$$').get((var.get('$0')-Js(3.0))),'hash':var.get('$$').get((var.get('$0')-Js(2.0))),'blockParams':var.get('$$').get((var.get('$0')-Js(1.0))),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(5.0))), var.get('$$').get(var.get('$0')))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(18.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get((var.get('$0')-Js(1.0)))),'program':var.get('$$').get(var.get('$0'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(19.0)):
                            SWITCHED = True
                            var.put('inverse', var.get('yy').callprop('prepareBlock', var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get(var.get('$0')), var.get('$$').get(var.get('$0')), Js(False), var.get(u"this").get('_$')))
                            var.put('program', var.get('yy').callprop('prepareProgram', Js([var.get('inverse')]), var.get('$$').get((var.get('$0')-Js(1.0))).get('loc')))
                            var.get('program').put('chained', Js(True))
                            var.get(u"this").put('$', Js({'strip':var.get('$$').get((var.get('$0')-Js(2.0))).get('strip'),'program':var.get('program'),'chain':Js(True)}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(20.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(21.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'path':var.get('$$').get((var.get('$0')-Js(1.0))),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get(var.get('$0')))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(22.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('prepareMustache', var.get('$$').get((var.get('$0')-Js(3.0))), var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get((var.get('$0')-Js(4.0))), var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(4.0))), var.get('$$').get(var.get('$0'))), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(23.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('prepareMustache', var.get('$$').get((var.get('$0')-Js(3.0))), var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get((var.get('$0')-Js(4.0))), var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(4.0))), var.get('$$').get(var.get('$0'))), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(24.0)):
                            SWITCHED = True
                            def PyJs_LONG_247_(var=var):
                                return var.get(u"this").put('$', Js({'type':Js('PartialStatement'),'name':var.get('$$').get((var.get('$0')-Js(3.0))),'params':var.get('$$').get((var.get('$0')-Js(2.0))),'hash':var.get('$$').get((var.get('$0')-Js(1.0))),'indent':Js(''),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(4.0))), var.get('$$').get(var.get('$0'))),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            PyJs_LONG_247_()
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(25.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('preparePartialBlock', var.get('$$').get((var.get('$0')-Js(2.0))), var.get('$$').get((var.get('$0')-Js(1.0))), var.get('$$').get(var.get('$0')), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(26.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'path':var.get('$$').get((var.get('$0')-Js(3.0))),'params':var.get('$$').get((var.get('$0')-Js(2.0))),'hash':var.get('$$').get((var.get('$0')-Js(1.0))),'strip':var.get('yy').callprop('stripFlags', var.get('$$').get((var.get('$0')-Js(4.0))), var.get('$$').get(var.get('$0')))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(27.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(28.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(29.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('SubExpression'),'path':var.get('$$').get((var.get('$0')-Js(3.0))),'params':var.get('$$').get((var.get('$0')-Js(2.0))),'hash':var.get('$$').get((var.get('$0')-Js(1.0))),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(30.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('Hash'),'pairs':var.get('$$').get(var.get('$0')),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(31.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('HashPair'),'key':var.get('yy').callprop('id', var.get('$$').get((var.get('$0')-Js(2.0)))),'value':var.get('$$').get(var.get('$0')),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(32.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('id', var.get('$$').get((var.get('$0')-Js(1.0)))))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(33.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(34.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(35.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('StringLiteral'),'value':var.get('$$').get(var.get('$0')),'original':var.get('$$').get(var.get('$0')),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(36.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('NumberLiteral'),'value':var.get('Number')(var.get('$$').get(var.get('$0'))),'original':var.get('Number')(var.get('$$').get(var.get('$0'))),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(37.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('BooleanLiteral'),'value':PyJsStrictEq(var.get('$$').get(var.get('$0')),Js('true')),'original':PyJsStrictEq(var.get('$$').get(var.get('$0')),Js('true')),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(38.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('UndefinedLiteral'),'original':var.get('undefined'),'value':var.get('undefined'),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(39.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js({'type':Js('NullLiteral'),'original':var.get(u"null"),'value':var.get(u"null"),'loc':var.get('yy').callprop('locInfo', var.get(u"this").get('_$'))}))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(40.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(41.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(42.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('preparePath', Js(True), var.get('$$').get(var.get('$0')), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(43.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', var.get('yy').callprop('preparePath', Js(False), var.get('$$').get(var.get('$0')), var.get(u"this").get('_$')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(44.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(2.0))).callprop('push', Js({'part':var.get('yy').callprop('id', var.get('$$').get(var.get('$0'))),'original':var.get('$$').get(var.get('$0')),'separator':var.get('$$').get((var.get('$0')-Js(1.0)))}))
                            var.get(u"this").put('$', var.get('$$').get((var.get('$0')-Js(2.0))))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(45.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([Js({'part':var.get('yy').callprop('id', var.get('$$').get(var.get('$0'))),'original':var.get('$$').get(var.get('$0'))})]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(46.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(47.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(48.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(49.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(50.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(51.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(58.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(59.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(64.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(65.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(70.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(71.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(78.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(79.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(82.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(83.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(86.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(87.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(90.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(91.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(94.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(95.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(98.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([var.get('$$').get(var.get('$0'))]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(99.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(100.0)):
                            SWITCHED = True
                            var.get(u"this").put('$', Js([var.get('$$').get(var.get('$0'))]))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js(101.0)):
                            SWITCHED = True
                            var.get('$$').get((var.get('$0')-Js(1.0))).callprop('push', var.get('$$').get(var.get('$0')))
                            break
                        SWITCHED = True
                        break
                PyJs_anonymous_245_._set_name('anonymous')
                @Js
                def PyJs_parseError_248_(str, hash, this, arguments, var=var):
                    var = Scope({'str':str, 'hash':hash, 'this':this, 'arguments':arguments, 'parseError':PyJs_parseError_248_}, var)
                    var.registers(['str', 'hash'])
                    PyJsTempException = JsToPyException(var.get('Error').create(var.get('str')))
                    raise PyJsTempException
                PyJs_parseError_248_._set_name('parseError')
                @Js
                def PyJs_parse_249_(input, this, arguments, var=var):
                    var = Scope({'input':input, 'this':this, 'arguments':arguments, 'parse':PyJs_parse_249_}, var)
                    var.registers(['stack', 'EOF', 'lstack', 'vstack', 'r', 'input', 'newState', 'a', 'yyleng', 'ranges', 'len', 'lex', 'preErrorSymbol', 'yyval', 'yyloc', 'errStr', 'recovering', 'yylineno', 'action', 'table', 'TERROR', 'popStack', 'state', 'expected', 'symbol', 'p', 'self', 'yytext'])
                    @Js
                    def PyJsHoisted_popStack_(n, this, arguments, var=var):
                        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
                        var.registers(['n'])
                        var.get('stack').put('length', (var.get('stack').get('length')-(Js(2.0)*var.get('n'))))
                        var.get('vstack').put('length', (var.get('vstack').get('length')-var.get('n')))
                        var.get('lstack').put('length', (var.get('lstack').get('length')-var.get('n')))
                    PyJsHoisted_popStack_.func_name = 'popStack'
                    var.put('popStack', PyJsHoisted_popStack_)
                    @Js
                    def PyJsHoisted_lex_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments}, var)
                        var.registers(['token'])
                        pass
                        var.put('token', (var.get('self').get('lexer').callprop('lex') or Js(1.0)))
                        if PyJsStrictNeq(var.get('token',throw=False).typeof(),Js('number')):
                            var.put('token', (var.get('self').get('symbols_').get(var.get('token')) or var.get('token')))
                        return var.get('token')
                    PyJsHoisted_lex_.func_name = 'lex'
                    var.put('lex', PyJsHoisted_lex_)
                    var.put('self', var.get(u"this"))
                    var.put('stack', Js([Js(0.0)]))
                    var.put('vstack', Js([var.get(u"null")]))
                    var.put('lstack', Js([]))
                    var.put('table', var.get(u"this").get('table'))
                    var.put('yytext', Js(''))
                    var.put('yylineno', Js(0.0))
                    var.put('yyleng', Js(0.0))
                    var.put('recovering', Js(0.0))
                    var.put('TERROR', Js(2.0))
                    var.put('EOF', Js(1.0))
                    var.get(u"this").get('lexer').callprop('setInput', var.get('input'))
                    var.get(u"this").get('lexer').put('yy', var.get(u"this").get('yy'))
                    var.get(u"this").get('yy').put('lexer', var.get(u"this").get('lexer'))
                    var.get(u"this").get('yy').put('parser', var.get(u"this"))
                    if (var.get(u"this").get('lexer').get('yylloc').typeof()==Js('undefined')):
                        var.get(u"this").get('lexer').put('yylloc', Js({}))
                    var.put('yyloc', var.get(u"this").get('lexer').get('yylloc'))
                    var.get('lstack').callprop('push', var.get('yyloc'))
                    var.put('ranges', (var.get(u"this").get('lexer').get('options') and var.get(u"this").get('lexer').get('options').get('ranges')))
                    if PyJsStrictEq(var.get(u"this").get('yy').get('parseError').typeof(),Js('function')):
                        var.get(u"this").put('parseError', var.get(u"this").get('yy').get('parseError'))
                    pass
                    pass
                    var.put('yyval', Js({}))
                    while Js(True):
                        var.put('state', var.get('stack').get((var.get('stack').get('length')-Js(1.0))))
                        if var.get(u"this").get('defaultActions').get(var.get('state')):
                            var.put('action', var.get(u"this").get('defaultActions').get(var.get('state')))
                        else:
                            if (PyJsStrictEq(var.get('symbol'),var.get(u"null")) or (var.get('symbol',throw=False).typeof()==Js('undefined'))):
                                var.put('symbol', var.get('lex')())
                            var.put('action', (var.get('table').get(var.get('state')) and var.get('table').get(var.get('state')).get(var.get('symbol'))))
                        if ((PyJsStrictEq(var.get('action',throw=False).typeof(),Js('undefined')) or var.get('action').get('length').neg()) or var.get('action').get('0').neg()):
                            var.put('errStr', Js(''))
                            if var.get('recovering').neg():
                                var.put('expected', Js([]))
                                for PyJsTemp in var.get('table').get(var.get('state')):
                                    var.put('p', PyJsTemp)
                                    if (var.get(u"this").get('terminals_').get(var.get('p')) and (var.get('p')>Js(2.0))):
                                        var.get('expected').callprop('push', ((Js("'")+var.get(u"this").get('terminals_').get(var.get('p')))+Js("'")))
                                if var.get(u"this").get('lexer').get('showPosition'):
                                    var.put('errStr', ((((((((Js('Parse error on line ')+(var.get('yylineno')+Js(1.0)))+Js(':\n'))+var.get(u"this").get('lexer').callprop('showPosition'))+Js('\nExpecting '))+var.get('expected').callprop('join', Js(', ')))+Js(", got '"))+(var.get(u"this").get('terminals_').get(var.get('symbol')) or var.get('symbol')))+Js("'")))
                                else:
                                    var.put('errStr', (((Js('Parse error on line ')+(var.get('yylineno')+Js(1.0)))+Js(': Unexpected '))+(Js('end of input') if (var.get('symbol')==Js(1.0)) else ((Js("'")+(var.get(u"this").get('terminals_').get(var.get('symbol')) or var.get('symbol')))+Js("'")))))
                                var.get(u"this").callprop('parseError', var.get('errStr'), Js({'text':var.get(u"this").get('lexer').get('match'),'token':(var.get(u"this").get('terminals_').get(var.get('symbol')) or var.get('symbol')),'line':var.get(u"this").get('lexer').get('yylineno'),'loc':var.get('yyloc'),'expected':var.get('expected')}))
                        if (var.get('action').get('0').instanceof(var.get('Array')) and (var.get('action').get('length')>Js(1.0))):
                            PyJsTempException = JsToPyException(var.get('Error').create((((Js('Parse Error: multiple actions possible at state: ')+var.get('state'))+Js(', token: '))+var.get('symbol'))))
                            raise PyJsTempException
                        while 1:
                            SWITCHED = False
                            CONDITION = (var.get('action').get('0'))
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
                                SWITCHED = True
                                var.get('stack').callprop('push', var.get('symbol'))
                                var.get('vstack').callprop('push', var.get(u"this").get('lexer').get('yytext'))
                                var.get('lstack').callprop('push', var.get(u"this").get('lexer').get('yylloc'))
                                var.get('stack').callprop('push', var.get('action').get('1'))
                                var.put('symbol', var.get(u"null"))
                                if var.get('preErrorSymbol').neg():
                                    var.put('yyleng', var.get(u"this").get('lexer').get('yyleng'))
                                    var.put('yytext', var.get(u"this").get('lexer').get('yytext'))
                                    var.put('yylineno', var.get(u"this").get('lexer').get('yylineno'))
                                    var.put('yyloc', var.get(u"this").get('lexer').get('yylloc'))
                                    if (var.get('recovering')>Js(0.0)):
                                        (var.put('recovering',Js(var.get('recovering').to_number())-Js(1))+Js(1))
                                else:
                                    var.put('symbol', var.get('preErrorSymbol'))
                                    var.put('preErrorSymbol', var.get(u"null"))
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
                                SWITCHED = True
                                var.put('len', var.get(u"this").get('productions_').get(var.get('action').get('1')).get('1'))
                                var.get('yyval').put('$', var.get('vstack').get((var.get('vstack').get('length')-var.get('len'))))
                                def PyJs_LONG_250_(var=var):
                                    return var.get('yyval').put('_$', Js({'first_line':var.get('lstack').get((var.get('lstack').get('length')-(var.get('len') or Js(1.0)))).get('first_line'),'last_line':var.get('lstack').get((var.get('lstack').get('length')-Js(1.0))).get('last_line'),'first_column':var.get('lstack').get((var.get('lstack').get('length')-(var.get('len') or Js(1.0)))).get('first_column'),'last_column':var.get('lstack').get((var.get('lstack').get('length')-Js(1.0))).get('last_column')}))
                                PyJs_LONG_250_()
                                if var.get('ranges'):
                                    var.get('yyval').get('_$').put('range', Js([var.get('lstack').get((var.get('lstack').get('length')-(var.get('len') or Js(1.0)))).get('range').get('0'), var.get('lstack').get((var.get('lstack').get('length')-Js(1.0))).get('range').get('1')]))
                                var.put('r', var.get(u"this").get('performAction').callprop('call', var.get('yyval'), var.get('yytext'), var.get('yyleng'), var.get('yylineno'), var.get(u"this").get('yy'), var.get('action').get('1'), var.get('vstack'), var.get('lstack')))
                                if PyJsStrictNeq(var.get('r',throw=False).typeof(),Js('undefined')):
                                    return var.get('r')
                                if var.get('len'):
                                    var.put('stack', var.get('stack').callprop('slice', Js(0.0), (((-Js(1.0))*var.get('len'))*Js(2.0))))
                                    var.put('vstack', var.get('vstack').callprop('slice', Js(0.0), ((-Js(1.0))*var.get('len'))))
                                    var.put('lstack', var.get('lstack').callprop('slice', Js(0.0), ((-Js(1.0))*var.get('len'))))
                                var.get('stack').callprop('push', var.get(u"this").get('productions_').get(var.get('action').get('1')).get('0'))
                                var.get('vstack').callprop('push', var.get('yyval').get('$'))
                                var.get('lstack').callprop('push', var.get('yyval').get('_$'))
                                var.put('newState', var.get('table').get(var.get('stack').get((var.get('stack').get('length')-Js(2.0)))).get(var.get('stack').get((var.get('stack').get('length')-Js(1.0)))))
                                var.get('stack').callprop('push', var.get('newState'))
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
                                SWITCHED = True
                                return Js(True)
                            SWITCHED = True
                            break
                    return Js(True)
                PyJs_parse_249_._set_name('parse')
                var.put('parser', Js({'trace':PyJs_trace_244_,'yy':Js({}),'symbols_':Js({'error':Js(2.0),'root':Js(3.0),'program':Js(4.0),'EOF':Js(5.0),'program_repetition0':Js(6.0),'statement':Js(7.0),'mustache':Js(8.0),'block':Js(9.0),'rawBlock':Js(10.0),'partial':Js(11.0),'partialBlock':Js(12.0),'content':Js(13.0),'COMMENT':Js(14.0),'CONTENT':Js(15.0),'openRawBlock':Js(16.0),'rawBlock_repetition0':Js(17.0),'END_RAW_BLOCK':Js(18.0),'OPEN_RAW_BLOCK':Js(19.0),'helperName':Js(20.0),'openRawBlock_repetition0':Js(21.0),'openRawBlock_option0':Js(22.0),'CLOSE_RAW_BLOCK':Js(23.0),'openBlock':Js(24.0),'block_option0':Js(25.0),'closeBlock':Js(26.0),'openInverse':Js(27.0),'block_option1':Js(28.0),'OPEN_BLOCK':Js(29.0),'openBlock_repetition0':Js(30.0),'openBlock_option0':Js(31.0),'openBlock_option1':Js(32.0),'CLOSE':Js(33.0),'OPEN_INVERSE':Js(34.0),'openInverse_repetition0':Js(35.0),'openInverse_option0':Js(36.0),'openInverse_option1':Js(37.0),'openInverseChain':Js(38.0),'OPEN_INVERSE_CHAIN':Js(39.0),'openInverseChain_repetition0':Js(40.0),'openInverseChain_option0':Js(41.0),'openInverseChain_option1':Js(42.0),'inverseAndProgram':Js(43.0),'INVERSE':Js(44.0),'inverseChain':Js(45.0),'inverseChain_option0':Js(46.0),'OPEN_ENDBLOCK':Js(47.0),'OPEN':Js(48.0),'mustache_repetition0':Js(49.0),'mustache_option0':Js(50.0),'OPEN_UNESCAPED':Js(51.0),'mustache_repetition1':Js(52.0),'mustache_option1':Js(53.0),'CLOSE_UNESCAPED':Js(54.0),'OPEN_PARTIAL':Js(55.0),'partialName':Js(56.0),'partial_repetition0':Js(57.0),'partial_option0':Js(58.0),'openPartialBlock':Js(59.0),'OPEN_PARTIAL_BLOCK':Js(60.0),'openPartialBlock_repetition0':Js(61.0),'openPartialBlock_option0':Js(62.0),'param':Js(63.0),'sexpr':Js(64.0),'OPEN_SEXPR':Js(65.0),'sexpr_repetition0':Js(66.0),'sexpr_option0':Js(67.0),'CLOSE_SEXPR':Js(68.0),'hash':Js(69.0),'hash_repetition_plus0':Js(70.0),'hashSegment':Js(71.0),'ID':Js(72.0),'EQUALS':Js(73.0),'blockParams':Js(74.0),'OPEN_BLOCK_PARAMS':Js(75.0),'blockParams_repetition_plus0':Js(76.0),'CLOSE_BLOCK_PARAMS':Js(77.0),'path':Js(78.0),'dataName':Js(79.0),'STRING':Js(80.0),'NUMBER':Js(81.0),'BOOLEAN':Js(82.0),'UNDEFINED':Js(83.0),'NULL':Js(84.0),'DATA':Js(85.0),'pathSegments':Js(86.0),'SEP':Js(87.0),'$accept':Js(0.0),'$end':Js(1.0)}),'terminals_':Js({'2':Js('error'),'5':Js('EOF'),'14':Js('COMMENT'),'15':Js('CONTENT'),'18':Js('END_RAW_BLOCK'),'19':Js('OPEN_RAW_BLOCK'),'23':Js('CLOSE_RAW_BLOCK'),'29':Js('OPEN_BLOCK'),'33':Js('CLOSE'),'34':Js('OPEN_INVERSE'),'39':Js('OPEN_INVERSE_CHAIN'),'44':Js('INVERSE'),'47':Js('OPEN_ENDBLOCK'),'48':Js('OPEN'),'51':Js('OPEN_UNESCAPED'),'54':Js('CLOSE_UNESCAPED'),'55':Js('OPEN_PARTIAL'),'60':Js('OPEN_PARTIAL_BLOCK'),'65':Js('OPEN_SEXPR'),'68':Js('CLOSE_SEXPR'),'72':Js('ID'),'73':Js('EQUALS'),'75':Js('OPEN_BLOCK_PARAMS'),'77':Js('CLOSE_BLOCK_PARAMS'),'80':Js('STRING'),'81':Js('NUMBER'),'82':Js('BOOLEAN'),'83':Js('UNDEFINED'),'84':Js('NULL'),'85':Js('DATA'),'87':Js('SEP')}),'productions_':Js([Js(0.0), Js([Js(3.0), Js(2.0)]), Js([Js(4.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(7.0), Js(1.0)]), Js([Js(13.0), Js(1.0)]), Js([Js(10.0), Js(3.0)]), Js([Js(16.0), Js(5.0)]), Js([Js(9.0), Js(4.0)]), Js([Js(9.0), Js(4.0)]), Js([Js(24.0), Js(6.0)]), Js([Js(27.0), Js(6.0)]), Js([Js(38.0), Js(6.0)]), Js([Js(43.0), Js(2.0)]), Js([Js(45.0), Js(3.0)]), Js([Js(45.0), Js(1.0)]), Js([Js(26.0), Js(3.0)]), Js([Js(8.0), Js(5.0)]), Js([Js(8.0), Js(5.0)]), Js([Js(11.0), Js(5.0)]), Js([Js(12.0), Js(3.0)]), Js([Js(59.0), Js(5.0)]), Js([Js(63.0), Js(1.0)]), Js([Js(63.0), Js(1.0)]), Js([Js(64.0), Js(5.0)]), Js([Js(69.0), Js(1.0)]), Js([Js(71.0), Js(3.0)]), Js([Js(74.0), Js(3.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(20.0), Js(1.0)]), Js([Js(56.0), Js(1.0)]), Js([Js(56.0), Js(1.0)]), Js([Js(79.0), Js(2.0)]), Js([Js(78.0), Js(1.0)]), Js([Js(86.0), Js(3.0)]), Js([Js(86.0), Js(1.0)]), Js([Js(6.0), Js(0.0)]), Js([Js(6.0), Js(2.0)]), Js([Js(17.0), Js(0.0)]), Js([Js(17.0), Js(2.0)]), Js([Js(21.0), Js(0.0)]), Js([Js(21.0), Js(2.0)]), Js([Js(22.0), Js(0.0)]), Js([Js(22.0), Js(1.0)]), Js([Js(25.0), Js(0.0)]), Js([Js(25.0), Js(1.0)]), Js([Js(28.0), Js(0.0)]), Js([Js(28.0), Js(1.0)]), Js([Js(30.0), Js(0.0)]), Js([Js(30.0), Js(2.0)]), Js([Js(31.0), Js(0.0)]), Js([Js(31.0), Js(1.0)]), Js([Js(32.0), Js(0.0)]), Js([Js(32.0), Js(1.0)]), Js([Js(35.0), Js(0.0)]), Js([Js(35.0), Js(2.0)]), Js([Js(36.0), Js(0.0)]), Js([Js(36.0), Js(1.0)]), Js([Js(37.0), Js(0.0)]), Js([Js(37.0), Js(1.0)]), Js([Js(40.0), Js(0.0)]), Js([Js(40.0), Js(2.0)]), Js([Js(41.0), Js(0.0)]), Js([Js(41.0), Js(1.0)]), Js([Js(42.0), Js(0.0)]), Js([Js(42.0), Js(1.0)]), Js([Js(46.0), Js(0.0)]), Js([Js(46.0), Js(1.0)]), Js([Js(49.0), Js(0.0)]), Js([Js(49.0), Js(2.0)]), Js([Js(50.0), Js(0.0)]), Js([Js(50.0), Js(1.0)]), Js([Js(52.0), Js(0.0)]), Js([Js(52.0), Js(2.0)]), Js([Js(53.0), Js(0.0)]), Js([Js(53.0), Js(1.0)]), Js([Js(57.0), Js(0.0)]), Js([Js(57.0), Js(2.0)]), Js([Js(58.0), Js(0.0)]), Js([Js(58.0), Js(1.0)]), Js([Js(61.0), Js(0.0)]), Js([Js(61.0), Js(2.0)]), Js([Js(62.0), Js(0.0)]), Js([Js(62.0), Js(1.0)]), Js([Js(66.0), Js(0.0)]), Js([Js(66.0), Js(2.0)]), Js([Js(67.0), Js(0.0)]), Js([Js(67.0), Js(1.0)]), Js([Js(70.0), Js(1.0)]), Js([Js(70.0), Js(2.0)]), Js([Js(76.0), Js(1.0)]), Js([Js(76.0), Js(2.0)])]),'performAction':PyJs_anonymous_245_,'table':Js([Js({'3':Js(1.0),'4':Js(2.0),'5':Js([Js(2.0), Js(46.0)]),'6':Js(3.0),'14':Js([Js(2.0), Js(46.0)]),'15':Js([Js(2.0), Js(46.0)]),'19':Js([Js(2.0), Js(46.0)]),'29':Js([Js(2.0), Js(46.0)]),'34':Js([Js(2.0), Js(46.0)]),'48':Js([Js(2.0), Js(46.0)]),'51':Js([Js(2.0), Js(46.0)]),'55':Js([Js(2.0), Js(46.0)]),'60':Js([Js(2.0), Js(46.0)])}), Js({'1':Js([Js(3.0)])}), Js({'5':Js([Js(1.0), Js(4.0)])}), Js({'5':Js([Js(2.0), Js(2.0)]),'7':Js(5.0),'8':Js(6.0),'9':Js(7.0),'10':Js(8.0),'11':Js(9.0),'12':Js(10.0),'13':Js(11.0),'14':Js([Js(1.0), Js(12.0)]),'15':Js([Js(1.0), Js(20.0)]),'16':Js(17.0),'19':Js([Js(1.0), Js(23.0)]),'24':Js(15.0),'27':Js(16.0),'29':Js([Js(1.0), Js(21.0)]),'34':Js([Js(1.0), Js(22.0)]),'39':Js([Js(2.0), Js(2.0)]),'44':Js([Js(2.0), Js(2.0)]),'47':Js([Js(2.0), Js(2.0)]),'48':Js([Js(1.0), Js(13.0)]),'51':Js([Js(1.0), Js(14.0)]),'55':Js([Js(1.0), Js(18.0)]),'59':Js(19.0),'60':Js([Js(1.0), Js(24.0)])}), Js({'1':Js([Js(2.0), Js(1.0)])}), Js({'5':Js([Js(2.0), Js(47.0)]),'14':Js([Js(2.0), Js(47.0)]),'15':Js([Js(2.0), Js(47.0)]),'19':Js([Js(2.0), Js(47.0)]),'29':Js([Js(2.0), Js(47.0)]),'34':Js([Js(2.0), Js(47.0)]),'39':Js([Js(2.0), Js(47.0)]),'44':Js([Js(2.0), Js(47.0)]),'47':Js([Js(2.0), Js(47.0)]),'48':Js([Js(2.0), Js(47.0)]),'51':Js([Js(2.0), Js(47.0)]),'55':Js([Js(2.0), Js(47.0)]),'60':Js([Js(2.0), Js(47.0)])}), Js({'5':Js([Js(2.0), Js(3.0)]),'14':Js([Js(2.0), Js(3.0)]),'15':Js([Js(2.0), Js(3.0)]),'19':Js([Js(2.0), Js(3.0)]),'29':Js([Js(2.0), Js(3.0)]),'34':Js([Js(2.0), Js(3.0)]),'39':Js([Js(2.0), Js(3.0)]),'44':Js([Js(2.0), Js(3.0)]),'47':Js([Js(2.0), Js(3.0)]),'48':Js([Js(2.0), Js(3.0)]),'51':Js([Js(2.0), Js(3.0)]),'55':Js([Js(2.0), Js(3.0)]),'60':Js([Js(2.0), Js(3.0)])}), Js({'5':Js([Js(2.0), Js(4.0)]),'14':Js([Js(2.0), Js(4.0)]),'15':Js([Js(2.0), Js(4.0)]),'19':Js([Js(2.0), Js(4.0)]),'29':Js([Js(2.0), Js(4.0)]),'34':Js([Js(2.0), Js(4.0)]),'39':Js([Js(2.0), Js(4.0)]),'44':Js([Js(2.0), Js(4.0)]),'47':Js([Js(2.0), Js(4.0)]),'48':Js([Js(2.0), Js(4.0)]),'51':Js([Js(2.0), Js(4.0)]),'55':Js([Js(2.0), Js(4.0)]),'60':Js([Js(2.0), Js(4.0)])}), Js({'5':Js([Js(2.0), Js(5.0)]),'14':Js([Js(2.0), Js(5.0)]),'15':Js([Js(2.0), Js(5.0)]),'19':Js([Js(2.0), Js(5.0)]),'29':Js([Js(2.0), Js(5.0)]),'34':Js([Js(2.0), Js(5.0)]),'39':Js([Js(2.0), Js(5.0)]),'44':Js([Js(2.0), Js(5.0)]),'47':Js([Js(2.0), Js(5.0)]),'48':Js([Js(2.0), Js(5.0)]),'51':Js([Js(2.0), Js(5.0)]),'55':Js([Js(2.0), Js(5.0)]),'60':Js([Js(2.0), Js(5.0)])}), Js({'5':Js([Js(2.0), Js(6.0)]),'14':Js([Js(2.0), Js(6.0)]),'15':Js([Js(2.0), Js(6.0)]),'19':Js([Js(2.0), Js(6.0)]),'29':Js([Js(2.0), Js(6.0)]),'34':Js([Js(2.0), Js(6.0)]),'39':Js([Js(2.0), Js(6.0)]),'44':Js([Js(2.0), Js(6.0)]),'47':Js([Js(2.0), Js(6.0)]),'48':Js([Js(2.0), Js(6.0)]),'51':Js([Js(2.0), Js(6.0)]),'55':Js([Js(2.0), Js(6.0)]),'60':Js([Js(2.0), Js(6.0)])}), Js({'5':Js([Js(2.0), Js(7.0)]),'14':Js([Js(2.0), Js(7.0)]),'15':Js([Js(2.0), Js(7.0)]),'19':Js([Js(2.0), Js(7.0)]),'29':Js([Js(2.0), Js(7.0)]),'34':Js([Js(2.0), Js(7.0)]),'39':Js([Js(2.0), Js(7.0)]),'44':Js([Js(2.0), Js(7.0)]),'47':Js([Js(2.0), Js(7.0)]),'48':Js([Js(2.0), Js(7.0)]),'51':Js([Js(2.0), Js(7.0)]),'55':Js([Js(2.0), Js(7.0)]),'60':Js([Js(2.0), Js(7.0)])}), Js({'5':Js([Js(2.0), Js(8.0)]),'14':Js([Js(2.0), Js(8.0)]),'15':Js([Js(2.0), Js(8.0)]),'19':Js([Js(2.0), Js(8.0)]),'29':Js([Js(2.0), Js(8.0)]),'34':Js([Js(2.0), Js(8.0)]),'39':Js([Js(2.0), Js(8.0)]),'44':Js([Js(2.0), Js(8.0)]),'47':Js([Js(2.0), Js(8.0)]),'48':Js([Js(2.0), Js(8.0)]),'51':Js([Js(2.0), Js(8.0)]),'55':Js([Js(2.0), Js(8.0)]),'60':Js([Js(2.0), Js(8.0)])}), Js({'5':Js([Js(2.0), Js(9.0)]),'14':Js([Js(2.0), Js(9.0)]),'15':Js([Js(2.0), Js(9.0)]),'19':Js([Js(2.0), Js(9.0)]),'29':Js([Js(2.0), Js(9.0)]),'34':Js([Js(2.0), Js(9.0)]),'39':Js([Js(2.0), Js(9.0)]),'44':Js([Js(2.0), Js(9.0)]),'47':Js([Js(2.0), Js(9.0)]),'48':Js([Js(2.0), Js(9.0)]),'51':Js([Js(2.0), Js(9.0)]),'55':Js([Js(2.0), Js(9.0)]),'60':Js([Js(2.0), Js(9.0)])}), Js({'20':Js(25.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(36.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'4':Js(37.0),'6':Js(3.0),'14':Js([Js(2.0), Js(46.0)]),'15':Js([Js(2.0), Js(46.0)]),'19':Js([Js(2.0), Js(46.0)]),'29':Js([Js(2.0), Js(46.0)]),'34':Js([Js(2.0), Js(46.0)]),'39':Js([Js(2.0), Js(46.0)]),'44':Js([Js(2.0), Js(46.0)]),'47':Js([Js(2.0), Js(46.0)]),'48':Js([Js(2.0), Js(46.0)]),'51':Js([Js(2.0), Js(46.0)]),'55':Js([Js(2.0), Js(46.0)]),'60':Js([Js(2.0), Js(46.0)])}), Js({'4':Js(38.0),'6':Js(3.0),'14':Js([Js(2.0), Js(46.0)]),'15':Js([Js(2.0), Js(46.0)]),'19':Js([Js(2.0), Js(46.0)]),'29':Js([Js(2.0), Js(46.0)]),'34':Js([Js(2.0), Js(46.0)]),'44':Js([Js(2.0), Js(46.0)]),'47':Js([Js(2.0), Js(46.0)]),'48':Js([Js(2.0), Js(46.0)]),'51':Js([Js(2.0), Js(46.0)]),'55':Js([Js(2.0), Js(46.0)]),'60':Js([Js(2.0), Js(46.0)])}), Js({'15':Js([Js(2.0), Js(48.0)]),'17':Js(39.0),'18':Js([Js(2.0), Js(48.0)])}), Js({'20':Js(41.0),'56':Js(40.0),'64':Js(42.0),'65':Js([Js(1.0), Js(43.0)]),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'4':Js(44.0),'6':Js(3.0),'14':Js([Js(2.0), Js(46.0)]),'15':Js([Js(2.0), Js(46.0)]),'19':Js([Js(2.0), Js(46.0)]),'29':Js([Js(2.0), Js(46.0)]),'34':Js([Js(2.0), Js(46.0)]),'47':Js([Js(2.0), Js(46.0)]),'48':Js([Js(2.0), Js(46.0)]),'51':Js([Js(2.0), Js(46.0)]),'55':Js([Js(2.0), Js(46.0)]),'60':Js([Js(2.0), Js(46.0)])}), Js({'5':Js([Js(2.0), Js(10.0)]),'14':Js([Js(2.0), Js(10.0)]),'15':Js([Js(2.0), Js(10.0)]),'18':Js([Js(2.0), Js(10.0)]),'19':Js([Js(2.0), Js(10.0)]),'29':Js([Js(2.0), Js(10.0)]),'34':Js([Js(2.0), Js(10.0)]),'39':Js([Js(2.0), Js(10.0)]),'44':Js([Js(2.0), Js(10.0)]),'47':Js([Js(2.0), Js(10.0)]),'48':Js([Js(2.0), Js(10.0)]),'51':Js([Js(2.0), Js(10.0)]),'55':Js([Js(2.0), Js(10.0)]),'60':Js([Js(2.0), Js(10.0)])}), Js({'20':Js(45.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(46.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(47.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(41.0),'56':Js(48.0),'64':Js(42.0),'65':Js([Js(1.0), Js(43.0)]),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'33':Js([Js(2.0), Js(78.0)]),'49':Js(49.0),'65':Js([Js(2.0), Js(78.0)]),'72':Js([Js(2.0), Js(78.0)]),'80':Js([Js(2.0), Js(78.0)]),'81':Js([Js(2.0), Js(78.0)]),'82':Js([Js(2.0), Js(78.0)]),'83':Js([Js(2.0), Js(78.0)]),'84':Js([Js(2.0), Js(78.0)]),'85':Js([Js(2.0), Js(78.0)])}), Js({'23':Js([Js(2.0), Js(33.0)]),'33':Js([Js(2.0), Js(33.0)]),'54':Js([Js(2.0), Js(33.0)]),'65':Js([Js(2.0), Js(33.0)]),'68':Js([Js(2.0), Js(33.0)]),'72':Js([Js(2.0), Js(33.0)]),'75':Js([Js(2.0), Js(33.0)]),'80':Js([Js(2.0), Js(33.0)]),'81':Js([Js(2.0), Js(33.0)]),'82':Js([Js(2.0), Js(33.0)]),'83':Js([Js(2.0), Js(33.0)]),'84':Js([Js(2.0), Js(33.0)]),'85':Js([Js(2.0), Js(33.0)])}), Js({'23':Js([Js(2.0), Js(34.0)]),'33':Js([Js(2.0), Js(34.0)]),'54':Js([Js(2.0), Js(34.0)]),'65':Js([Js(2.0), Js(34.0)]),'68':Js([Js(2.0), Js(34.0)]),'72':Js([Js(2.0), Js(34.0)]),'75':Js([Js(2.0), Js(34.0)]),'80':Js([Js(2.0), Js(34.0)]),'81':Js([Js(2.0), Js(34.0)]),'82':Js([Js(2.0), Js(34.0)]),'83':Js([Js(2.0), Js(34.0)]),'84':Js([Js(2.0), Js(34.0)]),'85':Js([Js(2.0), Js(34.0)])}), Js({'23':Js([Js(2.0), Js(35.0)]),'33':Js([Js(2.0), Js(35.0)]),'54':Js([Js(2.0), Js(35.0)]),'65':Js([Js(2.0), Js(35.0)]),'68':Js([Js(2.0), Js(35.0)]),'72':Js([Js(2.0), Js(35.0)]),'75':Js([Js(2.0), Js(35.0)]),'80':Js([Js(2.0), Js(35.0)]),'81':Js([Js(2.0), Js(35.0)]),'82':Js([Js(2.0), Js(35.0)]),'83':Js([Js(2.0), Js(35.0)]),'84':Js([Js(2.0), Js(35.0)]),'85':Js([Js(2.0), Js(35.0)])}), Js({'23':Js([Js(2.0), Js(36.0)]),'33':Js([Js(2.0), Js(36.0)]),'54':Js([Js(2.0), Js(36.0)]),'65':Js([Js(2.0), Js(36.0)]),'68':Js([Js(2.0), Js(36.0)]),'72':Js([Js(2.0), Js(36.0)]),'75':Js([Js(2.0), Js(36.0)]),'80':Js([Js(2.0), Js(36.0)]),'81':Js([Js(2.0), Js(36.0)]),'82':Js([Js(2.0), Js(36.0)]),'83':Js([Js(2.0), Js(36.0)]),'84':Js([Js(2.0), Js(36.0)]),'85':Js([Js(2.0), Js(36.0)])}), Js({'23':Js([Js(2.0), Js(37.0)]),'33':Js([Js(2.0), Js(37.0)]),'54':Js([Js(2.0), Js(37.0)]),'65':Js([Js(2.0), Js(37.0)]),'68':Js([Js(2.0), Js(37.0)]),'72':Js([Js(2.0), Js(37.0)]),'75':Js([Js(2.0), Js(37.0)]),'80':Js([Js(2.0), Js(37.0)]),'81':Js([Js(2.0), Js(37.0)]),'82':Js([Js(2.0), Js(37.0)]),'83':Js([Js(2.0), Js(37.0)]),'84':Js([Js(2.0), Js(37.0)]),'85':Js([Js(2.0), Js(37.0)])}), Js({'23':Js([Js(2.0), Js(38.0)]),'33':Js([Js(2.0), Js(38.0)]),'54':Js([Js(2.0), Js(38.0)]),'65':Js([Js(2.0), Js(38.0)]),'68':Js([Js(2.0), Js(38.0)]),'72':Js([Js(2.0), Js(38.0)]),'75':Js([Js(2.0), Js(38.0)]),'80':Js([Js(2.0), Js(38.0)]),'81':Js([Js(2.0), Js(38.0)]),'82':Js([Js(2.0), Js(38.0)]),'83':Js([Js(2.0), Js(38.0)]),'84':Js([Js(2.0), Js(38.0)]),'85':Js([Js(2.0), Js(38.0)])}), Js({'23':Js([Js(2.0), Js(39.0)]),'33':Js([Js(2.0), Js(39.0)]),'54':Js([Js(2.0), Js(39.0)]),'65':Js([Js(2.0), Js(39.0)]),'68':Js([Js(2.0), Js(39.0)]),'72':Js([Js(2.0), Js(39.0)]),'75':Js([Js(2.0), Js(39.0)]),'80':Js([Js(2.0), Js(39.0)]),'81':Js([Js(2.0), Js(39.0)]),'82':Js([Js(2.0), Js(39.0)]),'83':Js([Js(2.0), Js(39.0)]),'84':Js([Js(2.0), Js(39.0)]),'85':Js([Js(2.0), Js(39.0)])}), Js({'23':Js([Js(2.0), Js(43.0)]),'33':Js([Js(2.0), Js(43.0)]),'54':Js([Js(2.0), Js(43.0)]),'65':Js([Js(2.0), Js(43.0)]),'68':Js([Js(2.0), Js(43.0)]),'72':Js([Js(2.0), Js(43.0)]),'75':Js([Js(2.0), Js(43.0)]),'80':Js([Js(2.0), Js(43.0)]),'81':Js([Js(2.0), Js(43.0)]),'82':Js([Js(2.0), Js(43.0)]),'83':Js([Js(2.0), Js(43.0)]),'84':Js([Js(2.0), Js(43.0)]),'85':Js([Js(2.0), Js(43.0)]),'87':Js([Js(1.0), Js(50.0)])}), Js({'72':Js([Js(1.0), Js(35.0)]),'86':Js(51.0)}), Js({'23':Js([Js(2.0), Js(45.0)]),'33':Js([Js(2.0), Js(45.0)]),'54':Js([Js(2.0), Js(45.0)]),'65':Js([Js(2.0), Js(45.0)]),'68':Js([Js(2.0), Js(45.0)]),'72':Js([Js(2.0), Js(45.0)]),'75':Js([Js(2.0), Js(45.0)]),'80':Js([Js(2.0), Js(45.0)]),'81':Js([Js(2.0), Js(45.0)]),'82':Js([Js(2.0), Js(45.0)]),'83':Js([Js(2.0), Js(45.0)]),'84':Js([Js(2.0), Js(45.0)]),'85':Js([Js(2.0), Js(45.0)]),'87':Js([Js(2.0), Js(45.0)])}), Js({'52':Js(52.0),'54':Js([Js(2.0), Js(82.0)]),'65':Js([Js(2.0), Js(82.0)]),'72':Js([Js(2.0), Js(82.0)]),'80':Js([Js(2.0), Js(82.0)]),'81':Js([Js(2.0), Js(82.0)]),'82':Js([Js(2.0), Js(82.0)]),'83':Js([Js(2.0), Js(82.0)]),'84':Js([Js(2.0), Js(82.0)]),'85':Js([Js(2.0), Js(82.0)])}), Js({'25':Js(53.0),'38':Js(55.0),'39':Js([Js(1.0), Js(57.0)]),'43':Js(56.0),'44':Js([Js(1.0), Js(58.0)]),'45':Js(54.0),'47':Js([Js(2.0), Js(54.0)])}), Js({'28':Js(59.0),'43':Js(60.0),'44':Js([Js(1.0), Js(58.0)]),'47':Js([Js(2.0), Js(56.0)])}), Js({'13':Js(62.0),'15':Js([Js(1.0), Js(20.0)]),'18':Js([Js(1.0), Js(61.0)])}), Js({'33':Js([Js(2.0), Js(86.0)]),'57':Js(63.0),'65':Js([Js(2.0), Js(86.0)]),'72':Js([Js(2.0), Js(86.0)]),'80':Js([Js(2.0), Js(86.0)]),'81':Js([Js(2.0), Js(86.0)]),'82':Js([Js(2.0), Js(86.0)]),'83':Js([Js(2.0), Js(86.0)]),'84':Js([Js(2.0), Js(86.0)]),'85':Js([Js(2.0), Js(86.0)])}), Js({'33':Js([Js(2.0), Js(40.0)]),'65':Js([Js(2.0), Js(40.0)]),'72':Js([Js(2.0), Js(40.0)]),'80':Js([Js(2.0), Js(40.0)]),'81':Js([Js(2.0), Js(40.0)]),'82':Js([Js(2.0), Js(40.0)]),'83':Js([Js(2.0), Js(40.0)]),'84':Js([Js(2.0), Js(40.0)]),'85':Js([Js(2.0), Js(40.0)])}), Js({'33':Js([Js(2.0), Js(41.0)]),'65':Js([Js(2.0), Js(41.0)]),'72':Js([Js(2.0), Js(41.0)]),'80':Js([Js(2.0), Js(41.0)]),'81':Js([Js(2.0), Js(41.0)]),'82':Js([Js(2.0), Js(41.0)]),'83':Js([Js(2.0), Js(41.0)]),'84':Js([Js(2.0), Js(41.0)]),'85':Js([Js(2.0), Js(41.0)])}), Js({'20':Js(64.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'26':Js(65.0),'47':Js([Js(1.0), Js(66.0)])}), Js({'30':Js(67.0),'33':Js([Js(2.0), Js(58.0)]),'65':Js([Js(2.0), Js(58.0)]),'72':Js([Js(2.0), Js(58.0)]),'75':Js([Js(2.0), Js(58.0)]),'80':Js([Js(2.0), Js(58.0)]),'81':Js([Js(2.0), Js(58.0)]),'82':Js([Js(2.0), Js(58.0)]),'83':Js([Js(2.0), Js(58.0)]),'84':Js([Js(2.0), Js(58.0)]),'85':Js([Js(2.0), Js(58.0)])}), Js({'33':Js([Js(2.0), Js(64.0)]),'35':Js(68.0),'65':Js([Js(2.0), Js(64.0)]),'72':Js([Js(2.0), Js(64.0)]),'75':Js([Js(2.0), Js(64.0)]),'80':Js([Js(2.0), Js(64.0)]),'81':Js([Js(2.0), Js(64.0)]),'82':Js([Js(2.0), Js(64.0)]),'83':Js([Js(2.0), Js(64.0)]),'84':Js([Js(2.0), Js(64.0)]),'85':Js([Js(2.0), Js(64.0)])}), Js({'21':Js(69.0),'23':Js([Js(2.0), Js(50.0)]),'65':Js([Js(2.0), Js(50.0)]),'72':Js([Js(2.0), Js(50.0)]),'80':Js([Js(2.0), Js(50.0)]),'81':Js([Js(2.0), Js(50.0)]),'82':Js([Js(2.0), Js(50.0)]),'83':Js([Js(2.0), Js(50.0)]),'84':Js([Js(2.0), Js(50.0)]),'85':Js([Js(2.0), Js(50.0)])}), Js({'33':Js([Js(2.0), Js(90.0)]),'61':Js(70.0),'65':Js([Js(2.0), Js(90.0)]),'72':Js([Js(2.0), Js(90.0)]),'80':Js([Js(2.0), Js(90.0)]),'81':Js([Js(2.0), Js(90.0)]),'82':Js([Js(2.0), Js(90.0)]),'83':Js([Js(2.0), Js(90.0)]),'84':Js([Js(2.0), Js(90.0)]),'85':Js([Js(2.0), Js(90.0)])}), Js({'20':Js(74.0),'33':Js([Js(2.0), Js(80.0)]),'50':Js(71.0),'63':Js(72.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(73.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'72':Js([Js(1.0), Js(79.0)])}), Js({'23':Js([Js(2.0), Js(42.0)]),'33':Js([Js(2.0), Js(42.0)]),'54':Js([Js(2.0), Js(42.0)]),'65':Js([Js(2.0), Js(42.0)]),'68':Js([Js(2.0), Js(42.0)]),'72':Js([Js(2.0), Js(42.0)]),'75':Js([Js(2.0), Js(42.0)]),'80':Js([Js(2.0), Js(42.0)]),'81':Js([Js(2.0), Js(42.0)]),'82':Js([Js(2.0), Js(42.0)]),'83':Js([Js(2.0), Js(42.0)]),'84':Js([Js(2.0), Js(42.0)]),'85':Js([Js(2.0), Js(42.0)]),'87':Js([Js(1.0), Js(50.0)])}), Js({'20':Js(74.0),'53':Js(80.0),'54':Js([Js(2.0), Js(84.0)]),'63':Js(81.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(82.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'26':Js(83.0),'47':Js([Js(1.0), Js(66.0)])}), Js({'47':Js([Js(2.0), Js(55.0)])}), Js({'4':Js(84.0),'6':Js(3.0),'14':Js([Js(2.0), Js(46.0)]),'15':Js([Js(2.0), Js(46.0)]),'19':Js([Js(2.0), Js(46.0)]),'29':Js([Js(2.0), Js(46.0)]),'34':Js([Js(2.0), Js(46.0)]),'39':Js([Js(2.0), Js(46.0)]),'44':Js([Js(2.0), Js(46.0)]),'47':Js([Js(2.0), Js(46.0)]),'48':Js([Js(2.0), Js(46.0)]),'51':Js([Js(2.0), Js(46.0)]),'55':Js([Js(2.0), Js(46.0)]),'60':Js([Js(2.0), Js(46.0)])}), Js({'47':Js([Js(2.0), Js(20.0)])}), Js({'20':Js(85.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'4':Js(86.0),'6':Js(3.0),'14':Js([Js(2.0), Js(46.0)]),'15':Js([Js(2.0), Js(46.0)]),'19':Js([Js(2.0), Js(46.0)]),'29':Js([Js(2.0), Js(46.0)]),'34':Js([Js(2.0), Js(46.0)]),'47':Js([Js(2.0), Js(46.0)]),'48':Js([Js(2.0), Js(46.0)]),'51':Js([Js(2.0), Js(46.0)]),'55':Js([Js(2.0), Js(46.0)]),'60':Js([Js(2.0), Js(46.0)])}), Js({'26':Js(87.0),'47':Js([Js(1.0), Js(66.0)])}), Js({'47':Js([Js(2.0), Js(57.0)])}), Js({'5':Js([Js(2.0), Js(11.0)]),'14':Js([Js(2.0), Js(11.0)]),'15':Js([Js(2.0), Js(11.0)]),'19':Js([Js(2.0), Js(11.0)]),'29':Js([Js(2.0), Js(11.0)]),'34':Js([Js(2.0), Js(11.0)]),'39':Js([Js(2.0), Js(11.0)]),'44':Js([Js(2.0), Js(11.0)]),'47':Js([Js(2.0), Js(11.0)]),'48':Js([Js(2.0), Js(11.0)]),'51':Js([Js(2.0), Js(11.0)]),'55':Js([Js(2.0), Js(11.0)]),'60':Js([Js(2.0), Js(11.0)])}), Js({'15':Js([Js(2.0), Js(49.0)]),'18':Js([Js(2.0), Js(49.0)])}), Js({'20':Js(74.0),'33':Js([Js(2.0), Js(88.0)]),'58':Js(88.0),'63':Js(89.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(90.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'65':Js([Js(2.0), Js(94.0)]),'66':Js(91.0),'68':Js([Js(2.0), Js(94.0)]),'72':Js([Js(2.0), Js(94.0)]),'80':Js([Js(2.0), Js(94.0)]),'81':Js([Js(2.0), Js(94.0)]),'82':Js([Js(2.0), Js(94.0)]),'83':Js([Js(2.0), Js(94.0)]),'84':Js([Js(2.0), Js(94.0)]),'85':Js([Js(2.0), Js(94.0)])}), Js({'5':Js([Js(2.0), Js(25.0)]),'14':Js([Js(2.0), Js(25.0)]),'15':Js([Js(2.0), Js(25.0)]),'19':Js([Js(2.0), Js(25.0)]),'29':Js([Js(2.0), Js(25.0)]),'34':Js([Js(2.0), Js(25.0)]),'39':Js([Js(2.0), Js(25.0)]),'44':Js([Js(2.0), Js(25.0)]),'47':Js([Js(2.0), Js(25.0)]),'48':Js([Js(2.0), Js(25.0)]),'51':Js([Js(2.0), Js(25.0)]),'55':Js([Js(2.0), Js(25.0)]),'60':Js([Js(2.0), Js(25.0)])}), Js({'20':Js(92.0),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(74.0),'31':Js(93.0),'33':Js([Js(2.0), Js(60.0)]),'63':Js(94.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(95.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'75':Js([Js(2.0), Js(60.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(74.0),'33':Js([Js(2.0), Js(66.0)]),'36':Js(96.0),'63':Js(97.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(98.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'75':Js([Js(2.0), Js(66.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(74.0),'22':Js(99.0),'23':Js([Js(2.0), Js(52.0)]),'63':Js(100.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(101.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'20':Js(74.0),'33':Js([Js(2.0), Js(92.0)]),'62':Js(102.0),'63':Js(103.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(104.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'33':Js([Js(1.0), Js(105.0)])}), Js({'33':Js([Js(2.0), Js(79.0)]),'65':Js([Js(2.0), Js(79.0)]),'72':Js([Js(2.0), Js(79.0)]),'80':Js([Js(2.0), Js(79.0)]),'81':Js([Js(2.0), Js(79.0)]),'82':Js([Js(2.0), Js(79.0)]),'83':Js([Js(2.0), Js(79.0)]),'84':Js([Js(2.0), Js(79.0)]),'85':Js([Js(2.0), Js(79.0)])}), Js({'33':Js([Js(2.0), Js(81.0)])}), Js({'23':Js([Js(2.0), Js(27.0)]),'33':Js([Js(2.0), Js(27.0)]),'54':Js([Js(2.0), Js(27.0)]),'65':Js([Js(2.0), Js(27.0)]),'68':Js([Js(2.0), Js(27.0)]),'72':Js([Js(2.0), Js(27.0)]),'75':Js([Js(2.0), Js(27.0)]),'80':Js([Js(2.0), Js(27.0)]),'81':Js([Js(2.0), Js(27.0)]),'82':Js([Js(2.0), Js(27.0)]),'83':Js([Js(2.0), Js(27.0)]),'84':Js([Js(2.0), Js(27.0)]),'85':Js([Js(2.0), Js(27.0)])}), Js({'23':Js([Js(2.0), Js(28.0)]),'33':Js([Js(2.0), Js(28.0)]),'54':Js([Js(2.0), Js(28.0)]),'65':Js([Js(2.0), Js(28.0)]),'68':Js([Js(2.0), Js(28.0)]),'72':Js([Js(2.0), Js(28.0)]),'75':Js([Js(2.0), Js(28.0)]),'80':Js([Js(2.0), Js(28.0)]),'81':Js([Js(2.0), Js(28.0)]),'82':Js([Js(2.0), Js(28.0)]),'83':Js([Js(2.0), Js(28.0)]),'84':Js([Js(2.0), Js(28.0)]),'85':Js([Js(2.0), Js(28.0)])}), Js({'23':Js([Js(2.0), Js(30.0)]),'33':Js([Js(2.0), Js(30.0)]),'54':Js([Js(2.0), Js(30.0)]),'68':Js([Js(2.0), Js(30.0)]),'71':Js(106.0),'72':Js([Js(1.0), Js(107.0)]),'75':Js([Js(2.0), Js(30.0)])}), Js({'23':Js([Js(2.0), Js(98.0)]),'33':Js([Js(2.0), Js(98.0)]),'54':Js([Js(2.0), Js(98.0)]),'68':Js([Js(2.0), Js(98.0)]),'72':Js([Js(2.0), Js(98.0)]),'75':Js([Js(2.0), Js(98.0)])}), Js({'23':Js([Js(2.0), Js(45.0)]),'33':Js([Js(2.0), Js(45.0)]),'54':Js([Js(2.0), Js(45.0)]),'65':Js([Js(2.0), Js(45.0)]),'68':Js([Js(2.0), Js(45.0)]),'72':Js([Js(2.0), Js(45.0)]),'73':Js([Js(1.0), Js(108.0)]),'75':Js([Js(2.0), Js(45.0)]),'80':Js([Js(2.0), Js(45.0)]),'81':Js([Js(2.0), Js(45.0)]),'82':Js([Js(2.0), Js(45.0)]),'83':Js([Js(2.0), Js(45.0)]),'84':Js([Js(2.0), Js(45.0)]),'85':Js([Js(2.0), Js(45.0)]),'87':Js([Js(2.0), Js(45.0)])}), Js({'23':Js([Js(2.0), Js(44.0)]),'33':Js([Js(2.0), Js(44.0)]),'54':Js([Js(2.0), Js(44.0)]),'65':Js([Js(2.0), Js(44.0)]),'68':Js([Js(2.0), Js(44.0)]),'72':Js([Js(2.0), Js(44.0)]),'75':Js([Js(2.0), Js(44.0)]),'80':Js([Js(2.0), Js(44.0)]),'81':Js([Js(2.0), Js(44.0)]),'82':Js([Js(2.0), Js(44.0)]),'83':Js([Js(2.0), Js(44.0)]),'84':Js([Js(2.0), Js(44.0)]),'85':Js([Js(2.0), Js(44.0)]),'87':Js([Js(2.0), Js(44.0)])}), Js({'54':Js([Js(1.0), Js(109.0)])}), Js({'54':Js([Js(2.0), Js(83.0)]),'65':Js([Js(2.0), Js(83.0)]),'72':Js([Js(2.0), Js(83.0)]),'80':Js([Js(2.0), Js(83.0)]),'81':Js([Js(2.0), Js(83.0)]),'82':Js([Js(2.0), Js(83.0)]),'83':Js([Js(2.0), Js(83.0)]),'84':Js([Js(2.0), Js(83.0)]),'85':Js([Js(2.0), Js(83.0)])}), Js({'54':Js([Js(2.0), Js(85.0)])}), Js({'5':Js([Js(2.0), Js(13.0)]),'14':Js([Js(2.0), Js(13.0)]),'15':Js([Js(2.0), Js(13.0)]),'19':Js([Js(2.0), Js(13.0)]),'29':Js([Js(2.0), Js(13.0)]),'34':Js([Js(2.0), Js(13.0)]),'39':Js([Js(2.0), Js(13.0)]),'44':Js([Js(2.0), Js(13.0)]),'47':Js([Js(2.0), Js(13.0)]),'48':Js([Js(2.0), Js(13.0)]),'51':Js([Js(2.0), Js(13.0)]),'55':Js([Js(2.0), Js(13.0)]),'60':Js([Js(2.0), Js(13.0)])}), Js({'38':Js(55.0),'39':Js([Js(1.0), Js(57.0)]),'43':Js(56.0),'44':Js([Js(1.0), Js(58.0)]),'45':Js(111.0),'46':Js(110.0),'47':Js([Js(2.0), Js(76.0)])}), Js({'33':Js([Js(2.0), Js(70.0)]),'40':Js(112.0),'65':Js([Js(2.0), Js(70.0)]),'72':Js([Js(2.0), Js(70.0)]),'75':Js([Js(2.0), Js(70.0)]),'80':Js([Js(2.0), Js(70.0)]),'81':Js([Js(2.0), Js(70.0)]),'82':Js([Js(2.0), Js(70.0)]),'83':Js([Js(2.0), Js(70.0)]),'84':Js([Js(2.0), Js(70.0)]),'85':Js([Js(2.0), Js(70.0)])}), Js({'47':Js([Js(2.0), Js(18.0)])}), Js({'5':Js([Js(2.0), Js(14.0)]),'14':Js([Js(2.0), Js(14.0)]),'15':Js([Js(2.0), Js(14.0)]),'19':Js([Js(2.0), Js(14.0)]),'29':Js([Js(2.0), Js(14.0)]),'34':Js([Js(2.0), Js(14.0)]),'39':Js([Js(2.0), Js(14.0)]),'44':Js([Js(2.0), Js(14.0)]),'47':Js([Js(2.0), Js(14.0)]),'48':Js([Js(2.0), Js(14.0)]),'51':Js([Js(2.0), Js(14.0)]),'55':Js([Js(2.0), Js(14.0)]),'60':Js([Js(2.0), Js(14.0)])}), Js({'33':Js([Js(1.0), Js(113.0)])}), Js({'33':Js([Js(2.0), Js(87.0)]),'65':Js([Js(2.0), Js(87.0)]),'72':Js([Js(2.0), Js(87.0)]),'80':Js([Js(2.0), Js(87.0)]),'81':Js([Js(2.0), Js(87.0)]),'82':Js([Js(2.0), Js(87.0)]),'83':Js([Js(2.0), Js(87.0)]),'84':Js([Js(2.0), Js(87.0)]),'85':Js([Js(2.0), Js(87.0)])}), Js({'33':Js([Js(2.0), Js(89.0)])}), Js({'20':Js(74.0),'63':Js(115.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'67':Js(114.0),'68':Js([Js(2.0), Js(96.0)]),'69':Js(116.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'33':Js([Js(1.0), Js(117.0)])}), Js({'32':Js(118.0),'33':Js([Js(2.0), Js(62.0)]),'74':Js(119.0),'75':Js([Js(1.0), Js(120.0)])}), Js({'33':Js([Js(2.0), Js(59.0)]),'65':Js([Js(2.0), Js(59.0)]),'72':Js([Js(2.0), Js(59.0)]),'75':Js([Js(2.0), Js(59.0)]),'80':Js([Js(2.0), Js(59.0)]),'81':Js([Js(2.0), Js(59.0)]),'82':Js([Js(2.0), Js(59.0)]),'83':Js([Js(2.0), Js(59.0)]),'84':Js([Js(2.0), Js(59.0)]),'85':Js([Js(2.0), Js(59.0)])}), Js({'33':Js([Js(2.0), Js(61.0)]),'75':Js([Js(2.0), Js(61.0)])}), Js({'33':Js([Js(2.0), Js(68.0)]),'37':Js(121.0),'74':Js(122.0),'75':Js([Js(1.0), Js(120.0)])}), Js({'33':Js([Js(2.0), Js(65.0)]),'65':Js([Js(2.0), Js(65.0)]),'72':Js([Js(2.0), Js(65.0)]),'75':Js([Js(2.0), Js(65.0)]),'80':Js([Js(2.0), Js(65.0)]),'81':Js([Js(2.0), Js(65.0)]),'82':Js([Js(2.0), Js(65.0)]),'83':Js([Js(2.0), Js(65.0)]),'84':Js([Js(2.0), Js(65.0)]),'85':Js([Js(2.0), Js(65.0)])}), Js({'33':Js([Js(2.0), Js(67.0)]),'75':Js([Js(2.0), Js(67.0)])}), Js({'23':Js([Js(1.0), Js(123.0)])}), Js({'23':Js([Js(2.0), Js(51.0)]),'65':Js([Js(2.0), Js(51.0)]),'72':Js([Js(2.0), Js(51.0)]),'80':Js([Js(2.0), Js(51.0)]),'81':Js([Js(2.0), Js(51.0)]),'82':Js([Js(2.0), Js(51.0)]),'83':Js([Js(2.0), Js(51.0)]),'84':Js([Js(2.0), Js(51.0)]),'85':Js([Js(2.0), Js(51.0)])}), Js({'23':Js([Js(2.0), Js(53.0)])}), Js({'33':Js([Js(1.0), Js(124.0)])}), Js({'33':Js([Js(2.0), Js(91.0)]),'65':Js([Js(2.0), Js(91.0)]),'72':Js([Js(2.0), Js(91.0)]),'80':Js([Js(2.0), Js(91.0)]),'81':Js([Js(2.0), Js(91.0)]),'82':Js([Js(2.0), Js(91.0)]),'83':Js([Js(2.0), Js(91.0)]),'84':Js([Js(2.0), Js(91.0)]),'85':Js([Js(2.0), Js(91.0)])}), Js({'33':Js([Js(2.0), Js(93.0)])}), Js({'5':Js([Js(2.0), Js(22.0)]),'14':Js([Js(2.0), Js(22.0)]),'15':Js([Js(2.0), Js(22.0)]),'19':Js([Js(2.0), Js(22.0)]),'29':Js([Js(2.0), Js(22.0)]),'34':Js([Js(2.0), Js(22.0)]),'39':Js([Js(2.0), Js(22.0)]),'44':Js([Js(2.0), Js(22.0)]),'47':Js([Js(2.0), Js(22.0)]),'48':Js([Js(2.0), Js(22.0)]),'51':Js([Js(2.0), Js(22.0)]),'55':Js([Js(2.0), Js(22.0)]),'60':Js([Js(2.0), Js(22.0)])}), Js({'23':Js([Js(2.0), Js(99.0)]),'33':Js([Js(2.0), Js(99.0)]),'54':Js([Js(2.0), Js(99.0)]),'68':Js([Js(2.0), Js(99.0)]),'72':Js([Js(2.0), Js(99.0)]),'75':Js([Js(2.0), Js(99.0)])}), Js({'73':Js([Js(1.0), Js(108.0)])}), Js({'20':Js(74.0),'63':Js(125.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'72':Js([Js(1.0), Js(35.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'5':Js([Js(2.0), Js(23.0)]),'14':Js([Js(2.0), Js(23.0)]),'15':Js([Js(2.0), Js(23.0)]),'19':Js([Js(2.0), Js(23.0)]),'29':Js([Js(2.0), Js(23.0)]),'34':Js([Js(2.0), Js(23.0)]),'39':Js([Js(2.0), Js(23.0)]),'44':Js([Js(2.0), Js(23.0)]),'47':Js([Js(2.0), Js(23.0)]),'48':Js([Js(2.0), Js(23.0)]),'51':Js([Js(2.0), Js(23.0)]),'55':Js([Js(2.0), Js(23.0)]),'60':Js([Js(2.0), Js(23.0)])}), Js({'47':Js([Js(2.0), Js(19.0)])}), Js({'47':Js([Js(2.0), Js(77.0)])}), Js({'20':Js(74.0),'33':Js([Js(2.0), Js(72.0)]),'41':Js(126.0),'63':Js(127.0),'64':Js(75.0),'65':Js([Js(1.0), Js(43.0)]),'69':Js(128.0),'70':Js(76.0),'71':Js(77.0),'72':Js([Js(1.0), Js(78.0)]),'75':Js([Js(2.0), Js(72.0)]),'78':Js(26.0),'79':Js(27.0),'80':Js([Js(1.0), Js(28.0)]),'81':Js([Js(1.0), Js(29.0)]),'82':Js([Js(1.0), Js(30.0)]),'83':Js([Js(1.0), Js(31.0)]),'84':Js([Js(1.0), Js(32.0)]),'85':Js([Js(1.0), Js(34.0)]),'86':Js(33.0)}), Js({'5':Js([Js(2.0), Js(24.0)]),'14':Js([Js(2.0), Js(24.0)]),'15':Js([Js(2.0), Js(24.0)]),'19':Js([Js(2.0), Js(24.0)]),'29':Js([Js(2.0), Js(24.0)]),'34':Js([Js(2.0), Js(24.0)]),'39':Js([Js(2.0), Js(24.0)]),'44':Js([Js(2.0), Js(24.0)]),'47':Js([Js(2.0), Js(24.0)]),'48':Js([Js(2.0), Js(24.0)]),'51':Js([Js(2.0), Js(24.0)]),'55':Js([Js(2.0), Js(24.0)]),'60':Js([Js(2.0), Js(24.0)])}), Js({'68':Js([Js(1.0), Js(129.0)])}), Js({'65':Js([Js(2.0), Js(95.0)]),'68':Js([Js(2.0), Js(95.0)]),'72':Js([Js(2.0), Js(95.0)]),'80':Js([Js(2.0), Js(95.0)]),'81':Js([Js(2.0), Js(95.0)]),'82':Js([Js(2.0), Js(95.0)]),'83':Js([Js(2.0), Js(95.0)]),'84':Js([Js(2.0), Js(95.0)]),'85':Js([Js(2.0), Js(95.0)])}), Js({'68':Js([Js(2.0), Js(97.0)])}), Js({'5':Js([Js(2.0), Js(21.0)]),'14':Js([Js(2.0), Js(21.0)]),'15':Js([Js(2.0), Js(21.0)]),'19':Js([Js(2.0), Js(21.0)]),'29':Js([Js(2.0), Js(21.0)]),'34':Js([Js(2.0), Js(21.0)]),'39':Js([Js(2.0), Js(21.0)]),'44':Js([Js(2.0), Js(21.0)]),'47':Js([Js(2.0), Js(21.0)]),'48':Js([Js(2.0), Js(21.0)]),'51':Js([Js(2.0), Js(21.0)]),'55':Js([Js(2.0), Js(21.0)]),'60':Js([Js(2.0), Js(21.0)])}), Js({'33':Js([Js(1.0), Js(130.0)])}), Js({'33':Js([Js(2.0), Js(63.0)])}), Js({'72':Js([Js(1.0), Js(132.0)]),'76':Js(131.0)}), Js({'33':Js([Js(1.0), Js(133.0)])}), Js({'33':Js([Js(2.0), Js(69.0)])}), Js({'15':Js([Js(2.0), Js(12.0)]),'18':Js([Js(2.0), Js(12.0)])}), Js({'14':Js([Js(2.0), Js(26.0)]),'15':Js([Js(2.0), Js(26.0)]),'19':Js([Js(2.0), Js(26.0)]),'29':Js([Js(2.0), Js(26.0)]),'34':Js([Js(2.0), Js(26.0)]),'47':Js([Js(2.0), Js(26.0)]),'48':Js([Js(2.0), Js(26.0)]),'51':Js([Js(2.0), Js(26.0)]),'55':Js([Js(2.0), Js(26.0)]),'60':Js([Js(2.0), Js(26.0)])}), Js({'23':Js([Js(2.0), Js(31.0)]),'33':Js([Js(2.0), Js(31.0)]),'54':Js([Js(2.0), Js(31.0)]),'68':Js([Js(2.0), Js(31.0)]),'72':Js([Js(2.0), Js(31.0)]),'75':Js([Js(2.0), Js(31.0)])}), Js({'33':Js([Js(2.0), Js(74.0)]),'42':Js(134.0),'74':Js(135.0),'75':Js([Js(1.0), Js(120.0)])}), Js({'33':Js([Js(2.0), Js(71.0)]),'65':Js([Js(2.0), Js(71.0)]),'72':Js([Js(2.0), Js(71.0)]),'75':Js([Js(2.0), Js(71.0)]),'80':Js([Js(2.0), Js(71.0)]),'81':Js([Js(2.0), Js(71.0)]),'82':Js([Js(2.0), Js(71.0)]),'83':Js([Js(2.0), Js(71.0)]),'84':Js([Js(2.0), Js(71.0)]),'85':Js([Js(2.0), Js(71.0)])}), Js({'33':Js([Js(2.0), Js(73.0)]),'75':Js([Js(2.0), Js(73.0)])}), Js({'23':Js([Js(2.0), Js(29.0)]),'33':Js([Js(2.0), Js(29.0)]),'54':Js([Js(2.0), Js(29.0)]),'65':Js([Js(2.0), Js(29.0)]),'68':Js([Js(2.0), Js(29.0)]),'72':Js([Js(2.0), Js(29.0)]),'75':Js([Js(2.0), Js(29.0)]),'80':Js([Js(2.0), Js(29.0)]),'81':Js([Js(2.0), Js(29.0)]),'82':Js([Js(2.0), Js(29.0)]),'83':Js([Js(2.0), Js(29.0)]),'84':Js([Js(2.0), Js(29.0)]),'85':Js([Js(2.0), Js(29.0)])}), Js({'14':Js([Js(2.0), Js(15.0)]),'15':Js([Js(2.0), Js(15.0)]),'19':Js([Js(2.0), Js(15.0)]),'29':Js([Js(2.0), Js(15.0)]),'34':Js([Js(2.0), Js(15.0)]),'39':Js([Js(2.0), Js(15.0)]),'44':Js([Js(2.0), Js(15.0)]),'47':Js([Js(2.0), Js(15.0)]),'48':Js([Js(2.0), Js(15.0)]),'51':Js([Js(2.0), Js(15.0)]),'55':Js([Js(2.0), Js(15.0)]),'60':Js([Js(2.0), Js(15.0)])}), Js({'72':Js([Js(1.0), Js(137.0)]),'77':Js([Js(1.0), Js(136.0)])}), Js({'72':Js([Js(2.0), Js(100.0)]),'77':Js([Js(2.0), Js(100.0)])}), Js({'14':Js([Js(2.0), Js(16.0)]),'15':Js([Js(2.0), Js(16.0)]),'19':Js([Js(2.0), Js(16.0)]),'29':Js([Js(2.0), Js(16.0)]),'34':Js([Js(2.0), Js(16.0)]),'44':Js([Js(2.0), Js(16.0)]),'47':Js([Js(2.0), Js(16.0)]),'48':Js([Js(2.0), Js(16.0)]),'51':Js([Js(2.0), Js(16.0)]),'55':Js([Js(2.0), Js(16.0)]),'60':Js([Js(2.0), Js(16.0)])}), Js({'33':Js([Js(1.0), Js(138.0)])}), Js({'33':Js([Js(2.0), Js(75.0)])}), Js({'33':Js([Js(2.0), Js(32.0)])}), Js({'72':Js([Js(2.0), Js(101.0)]),'77':Js([Js(2.0), Js(101.0)])}), Js({'14':Js([Js(2.0), Js(17.0)]),'15':Js([Js(2.0), Js(17.0)]),'19':Js([Js(2.0), Js(17.0)]),'29':Js([Js(2.0), Js(17.0)]),'34':Js([Js(2.0), Js(17.0)]),'39':Js([Js(2.0), Js(17.0)]),'44':Js([Js(2.0), Js(17.0)]),'47':Js([Js(2.0), Js(17.0)]),'48':Js([Js(2.0), Js(17.0)]),'51':Js([Js(2.0), Js(17.0)]),'55':Js([Js(2.0), Js(17.0)]),'60':Js([Js(2.0), Js(17.0)])})]),'defaultActions':Js({'4':Js([Js(2.0), Js(1.0)]),'54':Js([Js(2.0), Js(55.0)]),'56':Js([Js(2.0), Js(20.0)]),'60':Js([Js(2.0), Js(57.0)]),'73':Js([Js(2.0), Js(81.0)]),'82':Js([Js(2.0), Js(85.0)]),'86':Js([Js(2.0), Js(18.0)]),'90':Js([Js(2.0), Js(89.0)]),'101':Js([Js(2.0), Js(53.0)]),'104':Js([Js(2.0), Js(93.0)]),'110':Js([Js(2.0), Js(19.0)]),'111':Js([Js(2.0), Js(77.0)]),'116':Js([Js(2.0), Js(97.0)]),'119':Js([Js(2.0), Js(63.0)]),'122':Js([Js(2.0), Js(69.0)]),'135':Js([Js(2.0), Js(75.0)]),'136':Js([Js(2.0), Js(32.0)])}),'parseError':PyJs_parseError_248_,'parse':PyJs_parse_249_}))
                @Js
                def PyJs_anonymous_251_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers(['lexer'])
                    @Js
                    def PyJs_parseError_252_(str, hash, this, arguments, var=var):
                        var = Scope({'str':str, 'hash':hash, 'this':this, 'arguments':arguments, 'parseError':PyJs_parseError_252_}, var)
                        var.registers(['str', 'hash'])
                        if var.get(u"this").get('yy').get('parser'):
                            var.get(u"this").get('yy').get('parser').callprop('parseError', var.get('str'), var.get('hash'))
                        else:
                            PyJsTempException = JsToPyException(var.get('Error').create(var.get('str')))
                            raise PyJsTempException
                    PyJs_parseError_252_._set_name('parseError')
                    @Js
                    def PyJs_setInput_253_(input, this, arguments, var=var):
                        var = Scope({'input':input, 'this':this, 'arguments':arguments, 'setInput':PyJs_setInput_253_}, var)
                        var.registers(['input'])
                        var.get(u"this").put('_input', var.get('input'))
                        var.get(u"this").put('_more', var.get(u"this").put('_less', var.get(u"this").put('done', Js(False))))
                        var.get(u"this").put('yylineno', var.get(u"this").put('yyleng', Js(0.0)))
                        var.get(u"this").put('yytext', var.get(u"this").put('matched', var.get(u"this").put('match', Js(''))))
                        var.get(u"this").put('conditionStack', Js([Js('INITIAL')]))
                        var.get(u"this").put('yylloc', Js({'first_line':Js(1.0),'first_column':Js(0.0),'last_line':Js(1.0),'last_column':Js(0.0)}))
                        if var.get(u"this").get('options').get('ranges'):
                            var.get(u"this").get('yylloc').put('range', Js([Js(0.0), Js(0.0)]))
                        var.get(u"this").put('offset', Js(0.0))
                        return var.get(u"this")
                    PyJs_setInput_253_._set_name('setInput')
                    @Js
                    def PyJs_input_254_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'input':PyJs_input_254_}, var)
                        var.registers(['lines', 'ch'])
                        var.put('ch', var.get(u"this").get('_input').get('0'))
                        var.get(u"this").put('yytext', var.get('ch'), '+')
                        (var.get(u"this").put('yyleng',Js(var.get(u"this").get('yyleng').to_number())+Js(1))-Js(1))
                        (var.get(u"this").put('offset',Js(var.get(u"this").get('offset').to_number())+Js(1))-Js(1))
                        var.get(u"this").put('match', var.get('ch'), '+')
                        var.get(u"this").put('matched', var.get('ch'), '+')
                        var.put('lines', var.get('ch').callprop('match', JsRegExp('/(?:\\r\\n?|\\n).*/g')))
                        if var.get('lines'):
                            (var.get(u"this").put('yylineno',Js(var.get(u"this").get('yylineno').to_number())+Js(1))-Js(1))
                            (var.get(u"this").get('yylloc').put('last_line',Js(var.get(u"this").get('yylloc').get('last_line').to_number())+Js(1))-Js(1))
                        else:
                            (var.get(u"this").get('yylloc').put('last_column',Js(var.get(u"this").get('yylloc').get('last_column').to_number())+Js(1))-Js(1))
                        if var.get(u"this").get('options').get('ranges'):
                            (var.get(u"this").get('yylloc').get('range').put('1',Js(var.get(u"this").get('yylloc').get('range').get('1').to_number())+Js(1))-Js(1))
                        var.get(u"this").put('_input', var.get(u"this").get('_input').callprop('slice', Js(1.0)))
                        return var.get('ch')
                    PyJs_input_254_._set_name('input')
                    @Js
                    def PyJs_unput_255_(ch, this, arguments, var=var):
                        var = Scope({'ch':ch, 'this':this, 'arguments':arguments, 'unput':PyJs_unput_255_}, var)
                        var.registers(['ch', 'oldLines', 'len', 'r', 'lines'])
                        var.put('len', var.get('ch').get('length'))
                        var.put('lines', var.get('ch').callprop('split', JsRegExp('/(?:\\r\\n?|\\n)/g')))
                        var.get(u"this").put('_input', (var.get('ch')+var.get(u"this").get('_input')))
                        var.get(u"this").put('yytext', var.get(u"this").get('yytext').callprop('substr', Js(0.0), ((var.get(u"this").get('yytext').get('length')-var.get('len'))-Js(1.0))))
                        var.get(u"this").put('offset', var.get('len'), '-')
                        var.put('oldLines', var.get(u"this").get('match').callprop('split', JsRegExp('/(?:\\r\\n?|\\n)/g')))
                        var.get(u"this").put('match', var.get(u"this").get('match').callprop('substr', Js(0.0), (var.get(u"this").get('match').get('length')-Js(1.0))))
                        var.get(u"this").put('matched', var.get(u"this").get('matched').callprop('substr', Js(0.0), (var.get(u"this").get('matched').get('length')-Js(1.0))))
                        if (var.get('lines').get('length')-Js(1.0)):
                            var.get(u"this").put('yylineno', (var.get('lines').get('length')-Js(1.0)), '-')
                        var.put('r', var.get(u"this").get('yylloc').get('range'))
                        def PyJs_LONG_256_(var=var):
                            return var.get(u"this").put('yylloc', Js({'first_line':var.get(u"this").get('yylloc').get('first_line'),'last_line':(var.get(u"this").get('yylineno')+Js(1.0)),'first_column':var.get(u"this").get('yylloc').get('first_column'),'last_column':((((var.get(u"this").get('yylloc').get('first_column') if PyJsStrictEq(var.get('lines').get('length'),var.get('oldLines').get('length')) else Js(0.0))+var.get('oldLines').get((var.get('oldLines').get('length')-var.get('lines').get('length'))).get('length'))-var.get('lines').get('0').get('length')) if var.get('lines') else (var.get(u"this").get('yylloc').get('first_column')-var.get('len')))}))
                        PyJs_LONG_256_()
                        if var.get(u"this").get('options').get('ranges'):
                            var.get(u"this").get('yylloc').put('range', Js([var.get('r').get('0'), ((var.get('r').get('0')+var.get(u"this").get('yyleng'))-var.get('len'))]))
                        return var.get(u"this")
                    PyJs_unput_255_._set_name('unput')
                    @Js
                    def PyJs_more_257_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'more':PyJs_more_257_}, var)
                        var.registers([])
                        var.get(u"this").put('_more', Js(True))
                        return var.get(u"this")
                    PyJs_more_257_._set_name('more')
                    @Js
                    def PyJs_less_258_(n, this, arguments, var=var):
                        var = Scope({'n':n, 'this':this, 'arguments':arguments, 'less':PyJs_less_258_}, var)
                        var.registers(['n'])
                        var.get(u"this").callprop('unput', var.get(u"this").get('match').callprop('slice', var.get('n')))
                    PyJs_less_258_._set_name('less')
                    @Js
                    def PyJs_pastInput_259_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'pastInput':PyJs_pastInput_259_}, var)
                        var.registers(['past'])
                        var.put('past', var.get(u"this").get('matched').callprop('substr', Js(0.0), (var.get(u"this").get('matched').get('length')-var.get(u"this").get('match').get('length'))))
                        return ((Js('...') if (var.get('past').get('length')>Js(20.0)) else Js(''))+var.get('past').callprop('substr', (-Js(20.0))).callprop('replace', JsRegExp('/\\n/g'), Js('')))
                    PyJs_pastInput_259_._set_name('pastInput')
                    @Js
                    def PyJs_upcomingInput_260_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'upcomingInput':PyJs_upcomingInput_260_}, var)
                        var.registers(['next'])
                        var.put('next', var.get(u"this").get('match'))
                        if (var.get('next').get('length')<Js(20.0)):
                            var.put('next', var.get(u"this").get('_input').callprop('substr', Js(0.0), (Js(20.0)-var.get('next').get('length'))), '+')
                        return (var.get('next').callprop('substr', Js(0.0), Js(20.0))+(Js('...') if (var.get('next').get('length')>Js(20.0)) else Js(''))).callprop('replace', JsRegExp('/\\n/g'), Js(''))
                    PyJs_upcomingInput_260_._set_name('upcomingInput')
                    @Js
                    def PyJs_showPosition_261_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'showPosition':PyJs_showPosition_261_}, var)
                        var.registers(['c', 'pre'])
                        var.put('pre', var.get(u"this").callprop('pastInput'))
                        var.put('c', var.get('Array').create((var.get('pre').get('length')+Js(1.0))).callprop('join', Js('-')))
                        return ((((var.get('pre')+var.get(u"this").callprop('upcomingInput'))+Js('\n'))+var.get('c'))+Js('^'))
                    PyJs_showPosition_261_._set_name('showPosition')
                    @Js
                    def PyJs_next_262_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'next':PyJs_next_262_}, var)
                        var.registers(['token', 'i', 'tempMatch', 'index', 'match', 'rules', 'lines', 'col'])
                        if var.get(u"this").get('done'):
                            return var.get(u"this").get('EOF')
                        if var.get(u"this").get('_input').neg():
                            var.get(u"this").put('done', Js(True))
                        pass
                        if var.get(u"this").get('_more').neg():
                            var.get(u"this").put('yytext', Js(''))
                            var.get(u"this").put('match', Js(''))
                        var.put('rules', var.get(u"this").callprop('_currentRules'))
                        #for JS loop
                        var.put('i', Js(0.0))
                        while (var.get('i')<var.get('rules').get('length')):
                            var.put('tempMatch', var.get(u"this").get('_input').callprop('match', var.get(u"this").get('rules').get(var.get('rules').get(var.get('i')))))
                            if (var.get('tempMatch') and (var.get('match').neg() or (var.get('tempMatch').get('0').get('length')>var.get('match').get('0').get('length')))):
                                var.put('match', var.get('tempMatch'))
                                var.put('index', var.get('i'))
                                if var.get(u"this").get('options').get('flex').neg():
                                    break
                            # update
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                        if var.get('match'):
                            var.put('lines', var.get('match').get('0').callprop('match', JsRegExp('/(?:\\r\\n?|\\n).*/g')))
                            if var.get('lines'):
                                var.get(u"this").put('yylineno', var.get('lines').get('length'), '+')
                            def PyJs_LONG_263_(var=var):
                                return var.get(u"this").put('yylloc', Js({'first_line':var.get(u"this").get('yylloc').get('last_line'),'last_line':(var.get(u"this").get('yylineno')+Js(1.0)),'first_column':var.get(u"this").get('yylloc').get('last_column'),'last_column':((var.get('lines').get((var.get('lines').get('length')-Js(1.0))).get('length')-var.get('lines').get((var.get('lines').get('length')-Js(1.0))).callprop('match', JsRegExp('/\\r?\\n?/')).get('0').get('length')) if var.get('lines') else (var.get(u"this").get('yylloc').get('last_column')+var.get('match').get('0').get('length')))}))
                            PyJs_LONG_263_()
                            var.get(u"this").put('yytext', var.get('match').get('0'), '+')
                            var.get(u"this").put('match', var.get('match').get('0'), '+')
                            var.get(u"this").put('matches', var.get('match'))
                            var.get(u"this").put('yyleng', var.get(u"this").get('yytext').get('length'))
                            if var.get(u"this").get('options').get('ranges'):
                                var.get(u"this").get('yylloc').put('range', Js([var.get(u"this").get('offset'), var.get(u"this").put('offset', var.get(u"this").get('yyleng'), '+')]))
                            var.get(u"this").put('_more', Js(False))
                            var.get(u"this").put('_input', var.get(u"this").get('_input').callprop('slice', var.get('match').get('0').get('length')))
                            var.get(u"this").put('matched', var.get('match').get('0'), '+')
                            var.put('token', var.get(u"this").get('performAction').callprop('call', var.get(u"this"), var.get(u"this").get('yy'), var.get(u"this"), var.get('rules').get(var.get('index')), var.get(u"this").get('conditionStack').get((var.get(u"this").get('conditionStack').get('length')-Js(1.0)))))
                            if (var.get(u"this").get('done') and var.get(u"this").get('_input')):
                                var.get(u"this").put('done', Js(False))
                            if var.get('token'):
                                return var.get('token')
                            else:
                                return var.get('undefined')
                        if PyJsStrictEq(var.get(u"this").get('_input'),Js('')):
                            return var.get(u"this").get('EOF')
                        else:
                            return var.get(u"this").callprop('parseError', (((Js('Lexical error on line ')+(var.get(u"this").get('yylineno')+Js(1.0)))+Js('. Unrecognized text.\n'))+var.get(u"this").callprop('showPosition')), Js({'text':Js(''),'token':var.get(u"null"),'line':var.get(u"this").get('yylineno')}))
                    PyJs_next_262_._set_name('next')
                    @Js
                    def PyJs_lex_264_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'lex':PyJs_lex_264_}, var)
                        var.registers(['r'])
                        var.put('r', var.get(u"this").callprop('next'))
                        if PyJsStrictNeq(var.get('r',throw=False).typeof(),Js('undefined')):
                            return var.get('r')
                        else:
                            return var.get(u"this").callprop('lex')
                    PyJs_lex_264_._set_name('lex')
                    @Js
                    def PyJs_begin_265_(condition, this, arguments, var=var):
                        var = Scope({'condition':condition, 'this':this, 'arguments':arguments, 'begin':PyJs_begin_265_}, var)
                        var.registers(['condition'])
                        var.get(u"this").get('conditionStack').callprop('push', var.get('condition'))
                    PyJs_begin_265_._set_name('begin')
                    @Js
                    def PyJs_popState_266_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'popState':PyJs_popState_266_}, var)
                        var.registers([])
                        return var.get(u"this").get('conditionStack').callprop('pop')
                    PyJs_popState_266_._set_name('popState')
                    @Js
                    def PyJs__currentRules_267_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, '_currentRules':PyJs__currentRules_267_}, var)
                        var.registers([])
                        return var.get(u"this").get('conditions').get(var.get(u"this").get('conditionStack').get((var.get(u"this").get('conditionStack').get('length')-Js(1.0)))).get('rules')
                    PyJs__currentRules_267_._set_name('_currentRules')
                    @Js
                    def PyJs_topState_268_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments, 'topState':PyJs_topState_268_}, var)
                        var.registers([])
                        return var.get(u"this").get('conditionStack').get((var.get(u"this").get('conditionStack').get('length')-Js(2.0)))
                    PyJs_topState_268_._set_name('topState')
                    @Js
                    def PyJs_begin_269_(condition, this, arguments, var=var):
                        var = Scope({'condition':condition, 'this':this, 'arguments':arguments, 'begin':PyJs_begin_269_}, var)
                        var.registers(['condition'])
                        var.get(u"this").callprop('begin', var.get('condition'))
                    PyJs_begin_269_._set_name('begin')
                    var.put('lexer', Js({'EOF':Js(1.0),'parseError':PyJs_parseError_252_,'setInput':PyJs_setInput_253_,'input':PyJs_input_254_,'unput':PyJs_unput_255_,'more':PyJs_more_257_,'less':PyJs_less_258_,'pastInput':PyJs_pastInput_259_,'upcomingInput':PyJs_upcomingInput_260_,'showPosition':PyJs_showPosition_261_,'next':PyJs_next_262_,'lex':PyJs_lex_264_,'begin':PyJs_begin_265_,'popState':PyJs_popState_266_,'_currentRules':PyJs__currentRules_267_,'topState':PyJs_topState_268_,'pushState':PyJs_begin_269_}))
                    var.get('lexer').put('options', Js({}))
                    @Js
                    def PyJs_anonymous_270_(yy, yy_, PyJsArg_2461766f6964696e675f6e616d655f636f6c6c6973696f6e73_, YY_START, this, arguments, var=var):
                        var = Scope({'yy':yy, 'yy_':yy_, '$avoiding_name_collisions':PyJsArg_2461766f6964696e675f6e616d655f636f6c6c6973696f6e73_, 'YY_START':YY_START, 'this':this, 'arguments':arguments, 'anonymous':PyJs_anonymous_270_}, var)
                        var.registers(['YY_START', 'strip', '$avoiding_name_collisions', 'yy_', 'yy', 'YYSTATE'])
                        @Js
                        def PyJsHoisted_strip_(start, end, this, arguments, var=var):
                            var = Scope({'start':start, 'end':end, 'this':this, 'arguments':arguments}, var)
                            var.registers(['end', 'start'])
                            return var.get('yy_').put('yytext', var.get('yy_').get('yytext').callprop('substring', var.get('start'), ((var.get('yy_').get('yyleng')-var.get('end'))+var.get('start'))))
                        PyJsHoisted_strip_.func_name = 'strip'
                        var.put('strip', PyJsHoisted_strip_)
                        pass
                        var.put('YYSTATE', var.get('YY_START'))
                        while 1:
                            SWITCHED = False
                            CONDITION = (var.get('$avoiding_name_collisions'))
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(0.0)):
                                SWITCHED = True
                                if PyJsStrictEq(var.get('yy_').get('yytext').callprop('slice', (-Js(2.0))),Js('\\\\')):
                                    var.get('strip')(Js(0.0), Js(1.0))
                                    var.get(u"this").callprop('begin', Js('mu'))
                                else:
                                    if PyJsStrictEq(var.get('yy_').get('yytext').callprop('slice', (-Js(1.0))),Js('\\')):
                                        var.get('strip')(Js(0.0), Js(1.0))
                                        var.get(u"this").callprop('begin', Js('emu'))
                                    else:
                                        var.get(u"this").callprop('begin', Js('mu'))
                                if var.get('yy_').get('yytext'):
                                    return Js(15.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
                                SWITCHED = True
                                return Js(15.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(15.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('begin', Js('raw'))
                                return Js(15.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(4.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                if PyJsStrictEq(var.get(u"this").get('conditionStack').get((var.get(u"this").get('conditionStack').get('length')-Js(1.0))),Js('raw')):
                                    return Js(15.0)
                                else:
                                    var.get('strip')(Js(5.0), Js(9.0))
                                    return Js('END_RAW_BLOCK')
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(5.0)):
                                SWITCHED = True
                                return Js(15.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(6.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(14.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(7.0)):
                                SWITCHED = True
                                return Js(65.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(8.0)):
                                SWITCHED = True
                                return Js(68.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(9.0)):
                                SWITCHED = True
                                return Js(19.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(10.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                var.get(u"this").callprop('begin', Js('raw'))
                                return Js(23.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(11.0)):
                                SWITCHED = True
                                return Js(55.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(12.0)):
                                SWITCHED = True
                                return Js(60.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(13.0)):
                                SWITCHED = True
                                return Js(29.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(14.0)):
                                SWITCHED = True
                                return Js(47.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(15.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(44.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(16.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(44.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(17.0)):
                                SWITCHED = True
                                return Js(34.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(18.0)):
                                SWITCHED = True
                                return Js(39.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(19.0)):
                                SWITCHED = True
                                return Js(51.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(20.0)):
                                SWITCHED = True
                                return Js(48.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(21.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('unput', var.get('yy_').get('yytext'))
                                var.get(u"this").callprop('popState')
                                var.get(u"this").callprop('begin', Js('com'))
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(22.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(14.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(23.0)):
                                SWITCHED = True
                                return Js(48.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(24.0)):
                                SWITCHED = True
                                return Js(73.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(25.0)):
                                SWITCHED = True
                                return Js(72.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(26.0)):
                                SWITCHED = True
                                return Js(72.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(27.0)):
                                SWITCHED = True
                                return Js(87.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(28.0)):
                                SWITCHED = True
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(29.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(54.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(30.0)):
                                SWITCHED = True
                                var.get(u"this").callprop('popState')
                                return Js(33.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(31.0)):
                                SWITCHED = True
                                var.get('yy_').put('yytext', var.get('strip')(Js(1.0), Js(2.0)).callprop('replace', JsRegExp('/\\\\"/g'), Js('"')))
                                return Js(80.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(32.0)):
                                SWITCHED = True
                                var.get('yy_').put('yytext', var.get('strip')(Js(1.0), Js(2.0)).callprop('replace', JsRegExp("/\\\\'/g"), Js("'")))
                                return Js(80.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(33.0)):
                                SWITCHED = True
                                return Js(85.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(34.0)):
                                SWITCHED = True
                                return Js(82.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(35.0)):
                                SWITCHED = True
                                return Js(82.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(36.0)):
                                SWITCHED = True
                                return Js(83.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(37.0)):
                                SWITCHED = True
                                return Js(84.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(38.0)):
                                SWITCHED = True
                                return Js(81.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(39.0)):
                                SWITCHED = True
                                return Js(75.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(40.0)):
                                SWITCHED = True
                                return Js(77.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(41.0)):
                                SWITCHED = True
                                return Js(72.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(42.0)):
                                SWITCHED = True
                                var.get('yy_').put('yytext', var.get('yy_').get('yytext').callprop('replace', JsRegExp('/\\\\([\\\\\\]])/g'), Js('$1')))
                                return Js(72.0)
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(43.0)):
                                SWITCHED = True
                                return Js('INVALID')
                                break
                            if SWITCHED or PyJsStrictEq(CONDITION, Js(44.0)):
                                SWITCHED = True
                                return Js(5.0)
                                break
                            SWITCHED = True
                            break
                    PyJs_anonymous_270_._set_name('anonymous')
                    var.get('lexer').put('performAction', PyJs_anonymous_270_)
                    def PyJs_LONG_271_(var=var):
                        return var.get('lexer').put('rules', Js([JsRegExp('/^(?:[^\\x00]*?(?=(\\{\\{)))/'), JsRegExp('/^(?:[^\\x00]+)/'), JsRegExp('/^(?:[^\\x00]{2,}?(?=(\\{\\{|\\\\\\{\\{|\\\\\\\\\\{\\{|$)))/'), JsRegExp('/^(?:\\{\\{\\{\\{(?=[^/]))/'), JsRegExp('/^(?:\\{\\{\\{\\{\\/[^\\s!"#%-,\\.\\/;->@\\[-\\^`\\{-~]+(?=[=}\\s\\/.])\\}\\}\\}\\})/'), JsRegExp('/^(?:[^\\x00]+?(?=(\\{\\{\\{\\{)))/'), JsRegExp('/^(?:[\\s\\S]*?--(~)?\\}\\})/'), JsRegExp('/^(?:\\()/'), JsRegExp('/^(?:\\))/'), JsRegExp('/^(?:\\{\\{\\{\\{)/'), JsRegExp('/^(?:\\}\\}\\}\\})/'), JsRegExp('/^(?:\\{\\{(~)?>)/'), JsRegExp('/^(?:\\{\\{(~)?#>)/'), JsRegExp('/^(?:\\{\\{(~)?#\\*?)/'), JsRegExp('/^(?:\\{\\{(~)?\\/)/'), JsRegExp('/^(?:\\{\\{(~)?\\^\\s*(~)?\\}\\})/'), JsRegExp('/^(?:\\{\\{(~)?\\s*else\\s*(~)?\\}\\})/'), JsRegExp('/^(?:\\{\\{(~)?\\^)/'), JsRegExp('/^(?:\\{\\{(~)?\\s*else\\b)/'), JsRegExp('/^(?:\\{\\{(~)?\\{)/'), JsRegExp('/^(?:\\{\\{(~)?&)/'), JsRegExp('/^(?:\\{\\{(~)?!--)/'), JsRegExp('/^(?:\\{\\{(~)?![\\s\\S]*?\\}\\})/'), JsRegExp('/^(?:\\{\\{(~)?\\*?)/'), JsRegExp('/^(?:=)/'), JsRegExp('/^(?:\\.\\.)/'), JsRegExp('/^(?:\\.(?=([=~}\\s\\/.)|])))/'), JsRegExp('/^(?:[\\/.])/'), JsRegExp('/^(?:\\s+)/'), JsRegExp('/^(?:\\}(~)?\\}\\})/'), JsRegExp('/^(?:(~)?\\}\\})/'), JsRegExp('/^(?:"(\\\\["]|[^"])*")/'), JsRegExp("/^(?:'(\\\\[']|[^'])*')/"), JsRegExp('/^(?:@)/'), JsRegExp('/^(?:true(?=([~}\\s)])))/'), JsRegExp('/^(?:false(?=([~}\\s)])))/'), JsRegExp('/^(?:undefined(?=([~}\\s)])))/'), JsRegExp('/^(?:null(?=([~}\\s)])))/'), JsRegExp('/^(?:-?[0-9]+(?:\\.[0-9]+)?(?=([~}\\s)])))/'), JsRegExp('/^(?:as\\s+\\|)/'), JsRegExp('/^(?:\\|)/'), JsRegExp('/^(?:([^\\s!"#%-,\\.\\/;->@\\[-\\^`\\{-~]+(?=([=~}\\s\\/.)|]))))/'), JsRegExp('/^(?:\\[(\\\\\\]|[^\\]])*\\])/'), JsRegExp('/^(?:.)/'), JsRegExp('/^(?:$)/')]))
                    PyJs_LONG_271_()
                    def PyJs_LONG_272_(var=var):
                        return var.get('lexer').put('conditions', Js({'mu':Js({'rules':Js([Js(7.0), Js(8.0), Js(9.0), Js(10.0), Js(11.0), Js(12.0), Js(13.0), Js(14.0), Js(15.0), Js(16.0), Js(17.0), Js(18.0), Js(19.0), Js(20.0), Js(21.0), Js(22.0), Js(23.0), Js(24.0), Js(25.0), Js(26.0), Js(27.0), Js(28.0), Js(29.0), Js(30.0), Js(31.0), Js(32.0), Js(33.0), Js(34.0), Js(35.0), Js(36.0), Js(37.0), Js(38.0), Js(39.0), Js(40.0), Js(41.0), Js(42.0), Js(43.0), Js(44.0)]),'inclusive':Js(False)}),'emu':Js({'rules':Js([Js(2.0)]),'inclusive':Js(False)}),'com':Js({'rules':Js([Js(6.0)]),'inclusive':Js(False)}),'raw':Js({'rules':Js([Js(3.0), Js(4.0), Js(5.0)]),'inclusive':Js(False)}),'INITIAL':Js({'rules':Js([Js(0.0), Js(1.0), Js(44.0)]),'inclusive':Js(True)})}))
                    PyJs_LONG_272_()
                    return var.get('lexer')
                PyJs_anonymous_251_._set_name('anonymous')
                var.put('lexer', PyJs_anonymous_251_())
                var.get('parser').put('lexer', var.get('lexer'))
                pass
                var.get('Parser').put('prototype', var.get('parser'))
                var.get('parser').put('Parser', var.get('Parser'))
                return var.get('Parser').create()
            PyJs_anonymous_243_._set_name('anonymous')
            var.put('handlebars', PyJs_anonymous_243_())
            var.get('exports').put('default', var.get('handlebars'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_242_._set_name('anonymous')
        @Js
        def PyJs_anonymous_273_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_interopRequireDefault', 'omitLeft', 'exports', 'isNextWhitespace', 'WhitespaceControl', 'module', 'isPrevWhitespace', '_visitor', '__webpack_require__', '_visitor2', 'omitRight'])
            @Js
            def PyJsHoisted_WhitespaceControl_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['options'])
                var.put('options', (Js({}) if ((var.get('arguments').get('length')<=Js(0.0)) or PyJsStrictEq(var.get('arguments').get('0'),var.get('undefined'))) else var.get('arguments').get('0')))
                var.get(u"this").put('options', var.get('options'))
            PyJsHoisted_WhitespaceControl_.func_name = 'WhitespaceControl'
            var.put('WhitespaceControl', PyJsHoisted_WhitespaceControl_)
            @Js
            def PyJsHoisted_isPrevWhitespace_(body, i, isRoot, this, arguments, var=var):
                var = Scope({'body':body, 'i':i, 'isRoot':isRoot, 'this':this, 'arguments':arguments}, var)
                var.registers(['prev', 'i', 'body', 'sibling', 'isRoot'])
                if PyJsStrictEq(var.get('i'),var.get('undefined')):
                    var.put('i', var.get('body').get('length'))
                var.put('prev', var.get('body').get((var.get('i')-Js(1.0))))
                var.put('sibling', var.get('body').get((var.get('i')-Js(2.0))))
                if var.get('prev').neg():
                    return var.get('isRoot')
                if PyJsStrictEq(var.get('prev').get('type'),Js('ContentStatement')):
                    return (JsRegExp('/\\r?\\n\\s*?$/') if (var.get('sibling') or var.get('isRoot').neg()) else JsRegExp('/(^|\\r?\\n)\\s*?$/')).callprop('test', var.get('prev').get('original'))
            PyJsHoisted_isPrevWhitespace_.func_name = 'isPrevWhitespace'
            var.put('isPrevWhitespace', PyJsHoisted_isPrevWhitespace_)
            @Js
            def PyJsHoisted_isNextWhitespace_(body, i, isRoot, this, arguments, var=var):
                var = Scope({'body':body, 'i':i, 'isRoot':isRoot, 'this':this, 'arguments':arguments}, var)
                var.registers(['i', 'body', 'next', 'sibling', 'isRoot'])
                if PyJsStrictEq(var.get('i'),var.get('undefined')):
                    var.put('i', (-Js(1.0)))
                var.put('next', var.get('body').get((var.get('i')+Js(1.0))))
                var.put('sibling', var.get('body').get((var.get('i')+Js(2.0))))
                if var.get('next').neg():
                    return var.get('isRoot')
                if PyJsStrictEq(var.get('next').get('type'),Js('ContentStatement')):
                    return (JsRegExp('/^\\s*?\\r?\\n/') if (var.get('sibling') or var.get('isRoot').neg()) else JsRegExp('/^\\s*?(\\r?\\n|$)/')).callprop('test', var.get('next').get('original'))
            PyJsHoisted_isNextWhitespace_.func_name = 'isNextWhitespace'
            var.put('isNextWhitespace', PyJsHoisted_isNextWhitespace_)
            @Js
            def PyJsHoisted_omitRight_(body, i, multiple, this, arguments, var=var):
                var = Scope({'body':body, 'i':i, 'multiple':multiple, 'this':this, 'arguments':arguments}, var)
                var.registers(['i', 'body', 'current', 'original', 'multiple'])
                var.put('current', var.get('body').get((Js(0.0) if (var.get('i')==var.get(u"null")) else (var.get('i')+Js(1.0)))))
                if ((var.get('current').neg() or PyJsStrictNeq(var.get('current').get('type'),Js('ContentStatement'))) or (var.get('multiple').neg() and var.get('current').get('rightStripped'))):
                    return var.get('undefined')
                var.put('original', var.get('current').get('value'))
                var.get('current').put('value', var.get('current').get('value').callprop('replace', (JsRegExp('/^\\s+/') if var.get('multiple') else JsRegExp('/^[ \\t]*\\r?\\n?/')), Js('')))
                var.get('current').put('rightStripped', PyJsStrictNeq(var.get('current').get('value'),var.get('original')))
            PyJsHoisted_omitRight_.func_name = 'omitRight'
            var.put('omitRight', PyJsHoisted_omitRight_)
            @Js
            def PyJsHoisted_omitLeft_(body, i, multiple, this, arguments, var=var):
                var = Scope({'body':body, 'i':i, 'multiple':multiple, 'this':this, 'arguments':arguments}, var)
                var.registers(['i', 'body', 'current', 'original', 'multiple'])
                var.put('current', var.get('body').get(((var.get('body').get('length')-Js(1.0)) if (var.get('i')==var.get(u"null")) else (var.get('i')-Js(1.0)))))
                if ((var.get('current').neg() or PyJsStrictNeq(var.get('current').get('type'),Js('ContentStatement'))) or (var.get('multiple').neg() and var.get('current').get('leftStripped'))):
                    return var.get('undefined')
                var.put('original', var.get('current').get('value'))
                var.get('current').put('value', var.get('current').get('value').callprop('replace', (JsRegExp('/\\s+$/') if var.get('multiple') else JsRegExp('/[ \\t]+$/')), Js('')))
                var.get('current').put('leftStripped', PyJsStrictNeq(var.get('current').get('value'),var.get('original')))
                return var.get('current').get('leftStripped')
            PyJsHoisted_omitLeft_.func_name = 'omitLeft'
            var.put('omitLeft', PyJsHoisted_omitLeft_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_visitor', var.get('__webpack_require__')(Js(88.0)))
            var.put('_visitor2', var.get('_interopRequireDefault')(var.get('_visitor')))
            pass
            var.get('WhitespaceControl').put('prototype', var.get('_visitor2').get('default').create())
            @Js
            def PyJs_anonymous_274_(program, this, arguments, var=var):
                var = Scope({'program':program, 'this':this, 'arguments':arguments}, var)
                var.registers(['program', 'l', 'closeStandalone', 'i', '_isPrevWhitespace', 'body', 'current', 'openStandalone', 'inlineStandalone', 'doStandalone', 'strip', 'isRoot', '_isNextWhitespace'])
                var.put('doStandalone', var.get(u"this").get('options').get('ignoreStandalone').neg())
                var.put('isRoot', var.get(u"this").get('isRootSeen').neg())
                var.get(u"this").put('isRootSeen', Js(True))
                var.put('body', var.get('program').get('body'))
                #for JS loop
                var.put('i', Js(0.0))
                var.put('l', var.get('body').get('length'))
                while (var.get('i')<var.get('l')):
                    var.put('current', var.get('body').get(var.get('i')))
                    var.put('strip', var.get(u"this").callprop('accept', var.get('current')))
                    if var.get('strip').neg():
                        # continue update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                        continue
                    var.put('_isPrevWhitespace', var.get('isPrevWhitespace')(var.get('body'), var.get('i'), var.get('isRoot')))
                    var.put('_isNextWhitespace', var.get('isNextWhitespace')(var.get('body'), var.get('i'), var.get('isRoot')))
                    var.put('openStandalone', (var.get('strip').get('openStandalone') and var.get('_isPrevWhitespace')))
                    var.put('closeStandalone', (var.get('strip').get('closeStandalone') and var.get('_isNextWhitespace')))
                    var.put('inlineStandalone', ((var.get('strip').get('inlineStandalone') and var.get('_isPrevWhitespace')) and var.get('_isNextWhitespace')))
                    if var.get('strip').get('close'):
                        var.get('omitRight')(var.get('body'), var.get('i'), Js(True))
                    if var.get('strip').get('open'):
                        var.get('omitLeft')(var.get('body'), var.get('i'), Js(True))
                    if (var.get('doStandalone') and var.get('inlineStandalone')):
                        var.get('omitRight')(var.get('body'), var.get('i'))
                        if var.get('omitLeft')(var.get('body'), var.get('i')):
                            if PyJsStrictEq(var.get('current').get('type'),Js('PartialStatement')):
                                var.get('current').put('indent', JsRegExp('/([ \\t]+$)/').callprop('exec', var.get('body').get((var.get('i')-Js(1.0))).get('original')).get('1'))
                    if (var.get('doStandalone') and var.get('openStandalone')):
                        var.get('omitRight')((var.get('current').get('program') or var.get('current').get('inverse')).get('body'))
                        var.get('omitLeft')(var.get('body'), var.get('i'))
                    if (var.get('doStandalone') and var.get('closeStandalone')):
                        var.get('omitRight')(var.get('body'), var.get('i'))
                        var.get('omitLeft')((var.get('current').get('inverse') or var.get('current').get('program')).get('body'))
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                return var.get('program')
            PyJs_anonymous_274_._set_name('anonymous')
            var.get('WhitespaceControl').get('prototype').put('Program', PyJs_anonymous_274_)
            @Js
            def PyJs_anonymous_275_(block, this, arguments, var=var):
                var = Scope({'block':block, 'this':this, 'arguments':arguments}, var)
                var.registers(['program', 'lastInverse', 'inverseStrip', 'firstInverse', 'inverse', 'strip', 'block'])
                var.get(u"this").callprop('accept', var.get('block').get('program'))
                var.get(u"this").callprop('accept', var.get('block').get('inverse'))
                var.put('program', (var.get('block').get('program') or var.get('block').get('inverse')))
                var.put('inverse', (var.get('block').get('program') and var.get('block').get('inverse')))
                var.put('firstInverse', var.get('inverse'))
                var.put('lastInverse', var.get('inverse'))
                if (var.get('inverse') and var.get('inverse').get('chained')):
                    var.put('firstInverse', var.get('inverse').get('body').get('0').get('program'))
                    while var.get('lastInverse').get('chained'):
                        var.put('lastInverse', var.get('lastInverse').get('body').get((var.get('lastInverse').get('body').get('length')-Js(1.0))).get('program'))
                var.put('strip', Js({'open':var.get('block').get('openStrip').get('open'),'close':var.get('block').get('closeStrip').get('close'),'openStandalone':var.get('isNextWhitespace')(var.get('program').get('body')),'closeStandalone':var.get('isPrevWhitespace')((var.get('firstInverse') or var.get('program')).get('body'))}))
                if var.get('block').get('openStrip').get('close'):
                    var.get('omitRight')(var.get('program').get('body'), var.get(u"null"), Js(True))
                if var.get('inverse'):
                    var.put('inverseStrip', var.get('block').get('inverseStrip'))
                    if var.get('inverseStrip').get('open'):
                        var.get('omitLeft')(var.get('program').get('body'), var.get(u"null"), Js(True))
                    if var.get('inverseStrip').get('close'):
                        var.get('omitRight')(var.get('firstInverse').get('body'), var.get(u"null"), Js(True))
                    if var.get('block').get('closeStrip').get('open'):
                        var.get('omitLeft')(var.get('lastInverse').get('body'), var.get(u"null"), Js(True))
                    if ((var.get(u"this").get('options').get('ignoreStandalone').neg() and var.get('isPrevWhitespace')(var.get('program').get('body'))) and var.get('isNextWhitespace')(var.get('firstInverse').get('body'))):
                        var.get('omitLeft')(var.get('program').get('body'))
                        var.get('omitRight')(var.get('firstInverse').get('body'))
                else:
                    if var.get('block').get('closeStrip').get('open'):
                        var.get('omitLeft')(var.get('program').get('body'), var.get(u"null"), Js(True))
                return var.get('strip')
            PyJs_anonymous_275_._set_name('anonymous')
            var.get('WhitespaceControl').get('prototype').put('BlockStatement', var.get('WhitespaceControl').get('prototype').put('DecoratorBlock', var.get('WhitespaceControl').get('prototype').put('PartialBlockStatement', PyJs_anonymous_275_)))
            @Js
            def PyJs_anonymous_276_(mustache, this, arguments, var=var):
                var = Scope({'mustache':mustache, 'this':this, 'arguments':arguments}, var)
                var.registers(['mustache'])
                return var.get('mustache').get('strip')
            PyJs_anonymous_276_._set_name('anonymous')
            var.get('WhitespaceControl').get('prototype').put('Decorator', var.get('WhitespaceControl').get('prototype').put('MustacheStatement', PyJs_anonymous_276_))
            @Js
            def PyJs_anonymous_277_(node, this, arguments, var=var):
                var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                var.registers(['strip', 'node'])
                var.put('strip', (var.get('node').get('strip') or Js({})))
                return Js({'inlineStandalone':Js(True),'open':var.get('strip').get('open'),'close':var.get('strip').get('close')})
            PyJs_anonymous_277_._set_name('anonymous')
            var.get('WhitespaceControl').get('prototype').put('PartialStatement', var.get('WhitespaceControl').get('prototype').put('CommentStatement', PyJs_anonymous_277_))
            pass
            pass
            pass
            pass
            var.get('exports').put('default', var.get('WhitespaceControl'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_273_._set_name('anonymous')
        @Js
        def PyJs_anonymous_278_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['Visitor', '_interopRequireDefault', 'exports', '_exception2', 'visitBlock', 'module', '_exception', '__webpack_require__', 'visitSubExpression', 'visitPartial'])
            @Js
            def PyJsHoisted_Visitor_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get(u"this").put('parents', Js([]))
            PyJsHoisted_Visitor_.func_name = 'Visitor'
            var.put('Visitor', PyJsHoisted_Visitor_)
            @Js
            def PyJsHoisted_visitSubExpression_(mustache, this, arguments, var=var):
                var = Scope({'mustache':mustache, 'this':this, 'arguments':arguments}, var)
                var.registers(['mustache'])
                var.get(u"this").callprop('acceptRequired', var.get('mustache'), Js('path'))
                var.get(u"this").callprop('acceptArray', var.get('mustache').get('params'))
                var.get(u"this").callprop('acceptKey', var.get('mustache'), Js('hash'))
            PyJsHoisted_visitSubExpression_.func_name = 'visitSubExpression'
            var.put('visitSubExpression', PyJsHoisted_visitSubExpression_)
            @Js
            def PyJsHoisted_visitBlock_(block, this, arguments, var=var):
                var = Scope({'block':block, 'this':this, 'arguments':arguments}, var)
                var.registers(['block'])
                var.get('visitSubExpression').callprop('call', var.get(u"this"), var.get('block'))
                var.get(u"this").callprop('acceptKey', var.get('block'), Js('program'))
                var.get(u"this").callprop('acceptKey', var.get('block'), Js('inverse'))
            PyJsHoisted_visitBlock_.func_name = 'visitBlock'
            var.put('visitBlock', PyJsHoisted_visitBlock_)
            @Js
            def PyJsHoisted_visitPartial_(partial, this, arguments, var=var):
                var = Scope({'partial':partial, 'this':this, 'arguments':arguments}, var)
                var.registers(['partial'])
                var.get(u"this").callprop('acceptRequired', var.get('partial'), Js('name'))
                var.get(u"this").callprop('acceptArray', var.get('partial').get('params'))
                var.get(u"this").callprop('acceptKey', var.get('partial'), Js('hash'))
            PyJsHoisted_visitPartial_.func_name = 'visitPartial'
            var.put('visitPartial', PyJsHoisted_visitPartial_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            pass
            def PyJs_LONG_295_(var=var):
                @Js
                def PyJs_acceptKey_279_(node, name, this, arguments, var=var):
                    var = Scope({'node':node, 'name':name, 'this':this, 'arguments':arguments, 'acceptKey':PyJs_acceptKey_279_}, var)
                    var.registers(['name', 'node', 'value'])
                    var.put('value', var.get(u"this").callprop('accept', var.get('node').get(var.get('name'))))
                    if var.get(u"this").get('mutating'):
                        if (var.get('value') and var.get('Visitor').get('prototype').get(var.get('value').get('type')).neg()):
                            PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((((((Js('Unexpected node type "')+var.get('value').get('type'))+Js('" found when accepting '))+var.get('name'))+Js(' on '))+var.get('node').get('type'))))
                            raise PyJsTempException
                        var.get('node').put(var.get('name'), var.get('value'))
                PyJs_acceptKey_279_._set_name('acceptKey')
                @Js
                def PyJs_acceptRequired_280_(node, name, this, arguments, var=var):
                    var = Scope({'node':node, 'name':name, 'this':this, 'arguments':arguments, 'acceptRequired':PyJs_acceptRequired_280_}, var)
                    var.registers(['name', 'node'])
                    var.get(u"this").callprop('acceptKey', var.get('node'), var.get('name'))
                    if var.get('node').get(var.get('name')).neg():
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(((var.get('node').get('type')+Js(' requires '))+var.get('name'))))
                        raise PyJsTempException
                PyJs_acceptRequired_280_._set_name('acceptRequired')
                @Js
                def PyJs_acceptArray_281_(array, this, arguments, var=var):
                    var = Scope({'array':array, 'this':this, 'arguments':arguments, 'acceptArray':PyJs_acceptArray_281_}, var)
                    var.registers(['array', 'l', 'i'])
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('l', var.get('array').get('length'))
                    while (var.get('i')<var.get('l')):
                        var.get(u"this").callprop('acceptKey', var.get('array'), var.get('i'))
                        if var.get('array').get(var.get('i')).neg():
                            var.get('array').callprop('splice', var.get('i'), Js(1.0))
                            (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
                            (var.put('l',Js(var.get('l').to_number())-Js(1))+Js(1))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_acceptArray_281_._set_name('acceptArray')
                @Js
                def PyJs_accept_282_(object, this, arguments, var=var):
                    var = Scope({'object':object, 'this':this, 'arguments':arguments, 'accept':PyJs_accept_282_}, var)
                    var.registers(['ret', 'object'])
                    if var.get('object').neg():
                        return var.get('undefined')
                    if var.get(u"this").get(var.get('object').get('type')).neg():
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('Unknown type: ')+var.get('object').get('type')), var.get('object')))
                        raise PyJsTempException
                    if var.get(u"this").get('current'):
                        var.get(u"this").get('parents').callprop('unshift', var.get(u"this").get('current'))
                    var.get(u"this").put('current', var.get('object'))
                    var.put('ret', var.get(u"this").callprop(var.get('object').get('type'), var.get('object')))
                    var.get(u"this").put('current', var.get(u"this").get('parents').callprop('shift'))
                    if (var.get(u"this").get('mutating').neg() or var.get('ret')):
                        return var.get('ret')
                    else:
                        if PyJsStrictNeq(var.get('ret'),Js(False)):
                            return var.get('object')
                PyJs_accept_282_._set_name('accept')
                @Js
                def PyJs_Program_283_(program, this, arguments, var=var):
                    var = Scope({'program':program, 'this':this, 'arguments':arguments, 'Program':PyJs_Program_283_}, var)
                    var.registers(['program'])
                    var.get(u"this").callprop('acceptArray', var.get('program').get('body'))
                PyJs_Program_283_._set_name('Program')
                @Js
                def PyJs_PartialBlockStatement_284_(partial, this, arguments, var=var):
                    var = Scope({'partial':partial, 'this':this, 'arguments':arguments, 'PartialBlockStatement':PyJs_PartialBlockStatement_284_}, var)
                    var.registers(['partial'])
                    var.get('visitPartial').callprop('call', var.get(u"this"), var.get('partial'))
                    var.get(u"this").callprop('acceptKey', var.get('partial'), Js('program'))
                PyJs_PartialBlockStatement_284_._set_name('PartialBlockStatement')
                @Js
                def PyJs_ContentStatement_285_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'ContentStatement':PyJs_ContentStatement_285_}, var)
                    var.registers([])
                    pass
                PyJs_ContentStatement_285_._set_name('ContentStatement')
                @Js
                def PyJs_CommentStatement_286_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'CommentStatement':PyJs_CommentStatement_286_}, var)
                    var.registers([])
                    pass
                PyJs_CommentStatement_286_._set_name('CommentStatement')
                @Js
                def PyJs_PathExpression_287_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'PathExpression':PyJs_PathExpression_287_}, var)
                    var.registers([])
                    pass
                PyJs_PathExpression_287_._set_name('PathExpression')
                @Js
                def PyJs_StringLiteral_288_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'StringLiteral':PyJs_StringLiteral_288_}, var)
                    var.registers([])
                    pass
                PyJs_StringLiteral_288_._set_name('StringLiteral')
                @Js
                def PyJs_NumberLiteral_289_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'NumberLiteral':PyJs_NumberLiteral_289_}, var)
                    var.registers([])
                    pass
                PyJs_NumberLiteral_289_._set_name('NumberLiteral')
                @Js
                def PyJs_BooleanLiteral_290_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'BooleanLiteral':PyJs_BooleanLiteral_290_}, var)
                    var.registers([])
                    pass
                PyJs_BooleanLiteral_290_._set_name('BooleanLiteral')
                @Js
                def PyJs_UndefinedLiteral_291_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'UndefinedLiteral':PyJs_UndefinedLiteral_291_}, var)
                    var.registers([])
                    pass
                PyJs_UndefinedLiteral_291_._set_name('UndefinedLiteral')
                @Js
                def PyJs_NullLiteral_292_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'NullLiteral':PyJs_NullLiteral_292_}, var)
                    var.registers([])
                    pass
                PyJs_NullLiteral_292_._set_name('NullLiteral')
                @Js
                def PyJs_Hash_293_(hash, this, arguments, var=var):
                    var = Scope({'hash':hash, 'this':this, 'arguments':arguments, 'Hash':PyJs_Hash_293_}, var)
                    var.registers(['hash'])
                    var.get(u"this").callprop('acceptArray', var.get('hash').get('pairs'))
                PyJs_Hash_293_._set_name('Hash')
                @Js
                def PyJs_HashPair_294_(pair, this, arguments, var=var):
                    var = Scope({'pair':pair, 'this':this, 'arguments':arguments, 'HashPair':PyJs_HashPair_294_}, var)
                    var.registers(['pair'])
                    var.get(u"this").callprop('acceptRequired', var.get('pair'), Js('value'))
                PyJs_HashPair_294_._set_name('HashPair')
                return var.get('Visitor').put('prototype', Js({'constructor':var.get('Visitor'),'mutating':Js(False),'acceptKey':PyJs_acceptKey_279_,'acceptRequired':PyJs_acceptRequired_280_,'acceptArray':PyJs_acceptArray_281_,'accept':PyJs_accept_282_,'Program':PyJs_Program_283_,'MustacheStatement':var.get('visitSubExpression'),'Decorator':var.get('visitSubExpression'),'BlockStatement':var.get('visitBlock'),'DecoratorBlock':var.get('visitBlock'),'PartialStatement':var.get('visitPartial'),'PartialBlockStatement':PyJs_PartialBlockStatement_284_,'ContentStatement':PyJs_ContentStatement_285_,'CommentStatement':PyJs_CommentStatement_286_,'SubExpression':var.get('visitSubExpression'),'PathExpression':PyJs_PathExpression_287_,'StringLiteral':PyJs_StringLiteral_288_,'NumberLiteral':PyJs_NumberLiteral_289_,'BooleanLiteral':PyJs_BooleanLiteral_290_,'UndefinedLiteral':PyJs_UndefinedLiteral_291_,'NullLiteral':PyJs_NullLiteral_292_,'Hash':PyJs_Hash_293_,'HashPair':PyJs_HashPair_294_}))
            PyJs_LONG_295_()
            pass
            pass
            pass
            var.get('exports').put('default', var.get('Visitor'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_278_._set_name('anonymous')
        @Js
        def PyJs_anonymous_296_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['validateClose', 'stripComment', 'prepareBlock', '_interopRequireDefault', 'preparePath', 'exports', '_exception2', 'stripFlags', 'module', '_exception', 'prepareRawBlock', 'prepareProgram', 'prepareMustache', 'SourceLocation', '__webpack_require__', 'id', 'preparePartialBlock'])
            @Js
            def PyJsHoisted_validateClose_(open, close, this, arguments, var=var):
                var = Scope({'open':open, 'close':close, 'this':this, 'arguments':arguments}, var)
                var.registers(['close', 'errorNode', 'open'])
                var.put('close', (var.get('close').get('path').get('original') if var.get('close').get('path') else var.get('close')))
                if PyJsStrictNeq(var.get('open').get('path').get('original'),var.get('close')):
                    var.put('errorNode', Js({'loc':var.get('open').get('path').get('loc')}))
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(((var.get('open').get('path').get('original')+Js(" doesn't match "))+var.get('close')), var.get('errorNode')))
                    raise PyJsTempException
            PyJsHoisted_validateClose_.func_name = 'validateClose'
            var.put('validateClose', PyJsHoisted_validateClose_)
            @Js
            def PyJsHoisted_SourceLocation_(source, locInfo, this, arguments, var=var):
                var = Scope({'source':source, 'locInfo':locInfo, 'this':this, 'arguments':arguments}, var)
                var.registers(['locInfo', 'source'])
                var.get(u"this").put('source', var.get('source'))
                var.get(u"this").put('start', Js({'line':var.get('locInfo').get('first_line'),'column':var.get('locInfo').get('first_column')}))
                var.get(u"this").put('end', Js({'line':var.get('locInfo').get('last_line'),'column':var.get('locInfo').get('last_column')}))
            PyJsHoisted_SourceLocation_.func_name = 'SourceLocation'
            var.put('SourceLocation', PyJsHoisted_SourceLocation_)
            @Js
            def PyJsHoisted_id_(token, this, arguments, var=var):
                var = Scope({'token':token, 'this':this, 'arguments':arguments}, var)
                var.registers(['token'])
                if JsRegExp('/^\\[.*\\]$/').callprop('test', var.get('token')):
                    return var.get('token').callprop('substring', Js(1.0), (var.get('token').get('length')-Js(1.0)))
                else:
                    return var.get('token')
            PyJsHoisted_id_.func_name = 'id'
            var.put('id', PyJsHoisted_id_)
            @Js
            def PyJsHoisted_stripFlags_(open, close, this, arguments, var=var):
                var = Scope({'open':open, 'close':close, 'this':this, 'arguments':arguments}, var)
                var.registers(['close', 'open'])
                return Js({'open':PyJsStrictEq(var.get('open').callprop('charAt', Js(2.0)),Js('~')),'close':PyJsStrictEq(var.get('close').callprop('charAt', (var.get('close').get('length')-Js(3.0))),Js('~'))})
            PyJsHoisted_stripFlags_.func_name = 'stripFlags'
            var.put('stripFlags', PyJsHoisted_stripFlags_)
            @Js
            def PyJsHoisted_stripComment_(comment, this, arguments, var=var):
                var = Scope({'comment':comment, 'this':this, 'arguments':arguments}, var)
                var.registers(['comment'])
                return var.get('comment').callprop('replace', JsRegExp('/^\\{\\{~?!-?-?/'), Js('')).callprop('replace', JsRegExp('/-?-?~?\\}\\}$/'), Js(''))
            PyJsHoisted_stripComment_.func_name = 'stripComment'
            var.put('stripComment', PyJsHoisted_stripComment_)
            @Js
            def PyJsHoisted_preparePath_(data, parts, loc, this, arguments, var=var):
                var = Scope({'data':data, 'parts':parts, 'loc':loc, 'this':this, 'arguments':arguments}, var)
                var.registers(['l', 'i', 'dig', 'loc', 'data', 'depth', 'part', 'isLiteral', 'parts', 'original'])
                var.put('loc', var.get(u"this").callprop('locInfo', var.get('loc')))
                var.put('original', (Js('@') if var.get('data') else Js('')))
                var.put('dig', Js([]))
                var.put('depth', Js(0.0))
                #for JS loop
                var.put('i', Js(0.0))
                var.put('l', var.get('parts').get('length'))
                while (var.get('i')<var.get('l')):
                    var.put('part', var.get('parts').get(var.get('i')).get('part'))
                    var.put('isLiteral', PyJsStrictNeq(var.get('parts').get(var.get('i')).get('original'),var.get('part')))
                    var.put('original', ((var.get('parts').get(var.get('i')).get('separator') or Js(''))+var.get('part')), '+')
                    if (var.get('isLiteral').neg() and ((PyJsStrictEq(var.get('part'),Js('..')) or PyJsStrictEq(var.get('part'),Js('.'))) or PyJsStrictEq(var.get('part'),Js('this')))):
                        if (var.get('dig').get('length')>Js(0.0)):
                            PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('Invalid path: ')+var.get('original')), Js({'loc':var.get('loc')})))
                            raise PyJsTempException
                        else:
                            if PyJsStrictEq(var.get('part'),Js('..')):
                                (var.put('depth',Js(var.get('depth').to_number())+Js(1))-Js(1))
                    else:
                        var.get('dig').callprop('push', var.get('part'))
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                return Js({'type':Js('PathExpression'),'data':var.get('data'),'depth':var.get('depth'),'parts':var.get('dig'),'original':var.get('original'),'loc':var.get('loc')})
            PyJsHoisted_preparePath_.func_name = 'preparePath'
            var.put('preparePath', PyJsHoisted_preparePath_)
            @Js
            def PyJsHoisted_prepareMustache_(path, params, hash, open, strip, locInfo, this, arguments, var=var):
                var = Scope({'path':path, 'params':params, 'hash':hash, 'open':open, 'strip':strip, 'locInfo':locInfo, 'this':this, 'arguments':arguments}, var)
                var.registers(['params', 'escaped', 'locInfo', 'escapeFlag', 'hash', 'strip', 'open', 'path', 'decorator'])
                var.put('escapeFlag', (var.get('open').callprop('charAt', Js(3.0)) or var.get('open').callprop('charAt', Js(2.0))))
                var.put('escaped', (PyJsStrictNeq(var.get('escapeFlag'),Js('{')) and PyJsStrictNeq(var.get('escapeFlag'),Js('&'))))
                var.put('decorator', JsRegExp('/\\*/').callprop('test', var.get('open')))
                return Js({'type':(Js('Decorator') if var.get('decorator') else Js('MustacheStatement')),'path':var.get('path'),'params':var.get('params'),'hash':var.get('hash'),'escaped':var.get('escaped'),'strip':var.get('strip'),'loc':var.get(u"this").callprop('locInfo', var.get('locInfo'))})
            PyJsHoisted_prepareMustache_.func_name = 'prepareMustache'
            var.put('prepareMustache', PyJsHoisted_prepareMustache_)
            @Js
            def PyJsHoisted_prepareRawBlock_(openRawBlock, contents, close, locInfo, this, arguments, var=var):
                var = Scope({'openRawBlock':openRawBlock, 'contents':contents, 'close':close, 'locInfo':locInfo, 'this':this, 'arguments':arguments}, var)
                var.registers(['close', 'program', 'contents', 'openRawBlock', 'locInfo'])
                var.get('validateClose')(var.get('openRawBlock'), var.get('close'))
                var.put('locInfo', var.get(u"this").callprop('locInfo', var.get('locInfo')))
                var.put('program', Js({'type':Js('Program'),'body':var.get('contents'),'strip':Js({}),'loc':var.get('locInfo')}))
                return Js({'type':Js('BlockStatement'),'path':var.get('openRawBlock').get('path'),'params':var.get('openRawBlock').get('params'),'hash':var.get('openRawBlock').get('hash'),'program':var.get('program'),'openStrip':Js({}),'inverseStrip':Js({}),'closeStrip':Js({}),'loc':var.get('locInfo')})
            PyJsHoisted_prepareRawBlock_.func_name = 'prepareRawBlock'
            var.put('prepareRawBlock', PyJsHoisted_prepareRawBlock_)
            @Js
            def PyJsHoisted_prepareBlock_(openBlock, program, inverseAndProgram, close, inverted, locInfo, this, arguments, var=var):
                var = Scope({'openBlock':openBlock, 'program':program, 'inverseAndProgram':inverseAndProgram, 'close':close, 'inverted':inverted, 'locInfo':locInfo, 'this':this, 'arguments':arguments}, var)
                var.registers(['close', 'program', 'inverseStrip', 'locInfo', 'openBlock', 'inverted', 'inverse', 'inverseAndProgram', 'decorator'])
                if (var.get('close') and var.get('close').get('path')):
                    var.get('validateClose')(var.get('openBlock'), var.get('close'))
                var.put('decorator', JsRegExp('/\\*/').callprop('test', var.get('openBlock').get('open')))
                var.get('program').put('blockParams', var.get('openBlock').get('blockParams'))
                var.put('inverse', var.get('undefined'))
                var.put('inverseStrip', var.get('undefined'))
                if var.get('inverseAndProgram'):
                    if var.get('decorator'):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('Unexpected inverse block on decorator'), var.get('inverseAndProgram')))
                        raise PyJsTempException
                    if var.get('inverseAndProgram').get('chain'):
                        var.get('inverseAndProgram').get('program').get('body').get('0').put('closeStrip', var.get('close').get('strip'))
                    var.put('inverseStrip', var.get('inverseAndProgram').get('strip'))
                    var.put('inverse', var.get('inverseAndProgram').get('program'))
                if var.get('inverted'):
                    var.put('inverted', var.get('inverse'))
                    var.put('inverse', var.get('program'))
                    var.put('program', var.get('inverted'))
                return Js({'type':(Js('DecoratorBlock') if var.get('decorator') else Js('BlockStatement')),'path':var.get('openBlock').get('path'),'params':var.get('openBlock').get('params'),'hash':var.get('openBlock').get('hash'),'program':var.get('program'),'inverse':var.get('inverse'),'openStrip':var.get('openBlock').get('strip'),'inverseStrip':var.get('inverseStrip'),'closeStrip':(var.get('close') and var.get('close').get('strip')),'loc':var.get(u"this").callprop('locInfo', var.get('locInfo'))})
            PyJsHoisted_prepareBlock_.func_name = 'prepareBlock'
            var.put('prepareBlock', PyJsHoisted_prepareBlock_)
            @Js
            def PyJsHoisted_prepareProgram_(statements, loc, this, arguments, var=var):
                var = Scope({'statements':statements, 'loc':loc, 'this':this, 'arguments':arguments}, var)
                var.registers(['loc', 'statements', 'lastLoc', 'firstLoc'])
                if (var.get('loc').neg() and var.get('statements').get('length')):
                    var.put('firstLoc', var.get('statements').get('0').get('loc'))
                    var.put('lastLoc', var.get('statements').get((var.get('statements').get('length')-Js(1.0))).get('loc'))
                    if (var.get('firstLoc') and var.get('lastLoc')):
                        var.put('loc', Js({'source':var.get('firstLoc').get('source'),'start':Js({'line':var.get('firstLoc').get('start').get('line'),'column':var.get('firstLoc').get('start').get('column')}),'end':Js({'line':var.get('lastLoc').get('end').get('line'),'column':var.get('lastLoc').get('end').get('column')})}))
                return Js({'type':Js('Program'),'body':var.get('statements'),'strip':Js({}),'loc':var.get('loc')})
            PyJsHoisted_prepareProgram_.func_name = 'prepareProgram'
            var.put('prepareProgram', PyJsHoisted_prepareProgram_)
            @Js
            def PyJsHoisted_preparePartialBlock_(open, program, close, locInfo, this, arguments, var=var):
                var = Scope({'open':open, 'program':program, 'close':close, 'locInfo':locInfo, 'this':this, 'arguments':arguments}, var)
                var.registers(['close', 'program', 'locInfo', 'open'])
                var.get('validateClose')(var.get('open'), var.get('close'))
                return Js({'type':Js('PartialBlockStatement'),'name':var.get('open').get('path'),'params':var.get('open').get('params'),'hash':var.get('open').get('hash'),'program':var.get('program'),'openStrip':var.get('open').get('strip'),'closeStrip':(var.get('close') and var.get('close').get('strip')),'loc':var.get(u"this").callprop('locInfo', var.get('locInfo'))})
            PyJsHoisted_preparePartialBlock_.func_name = 'preparePartialBlock'
            var.put('preparePartialBlock', PyJsHoisted_preparePartialBlock_)
            Js('use strict')
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('SourceLocation', var.get('SourceLocation'))
            var.get('exports').put('id', var.get('id'))
            var.get('exports').put('stripFlags', var.get('stripFlags'))
            var.get('exports').put('stripComment', var.get('stripComment'))
            var.get('exports').put('preparePath', var.get('preparePath'))
            var.get('exports').put('prepareMustache', var.get('prepareMustache'))
            var.get('exports').put('prepareRawBlock', var.get('prepareRawBlock'))
            var.get('exports').put('prepareBlock', var.get('prepareBlock'))
            var.get('exports').put('prepareProgram', var.get('prepareProgram'))
            var.get('exports').put('preparePartialBlock', var.get('preparePartialBlock'))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
            pass
        PyJs_anonymous_296_._set_name('anonymous')
        @Js
        def PyJs_anonymous_297_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['transformLiteralToPath', 'argEquals', '_interopRequireDefault', 'exports', '_exception2', 'precompile', '_ast2', 'slice', '_ast', 'compile', 'module', '_exception', '_utils', '_Object$create', '__webpack_require__', 'Compiler'])
            @Js
            def PyJsHoisted_Compiler_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                pass
            PyJsHoisted_Compiler_.func_name = 'Compiler'
            var.put('Compiler', PyJsHoisted_Compiler_)
            @Js
            def PyJsHoisted_precompile_(input, options, env, this, arguments, var=var):
                var = Scope({'input':input, 'options':options, 'env':env, 'this':this, 'arguments':arguments}, var)
                var.registers(['ast', 'env', 'environment', 'input', 'options'])
                if ((var.get('input')==var.get(u"null")) or (PyJsStrictNeq(var.get('input',throw=False).typeof(),Js('string')) and PyJsStrictNeq(var.get('input').get('type'),Js('Program')))):
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('You must pass a string or Handlebars AST to Handlebars.precompile. You passed ')+var.get('input'))))
                    raise PyJsTempException
                var.put('options', (var.get('options') or Js({})))
                if var.get('options').contains(Js('data')).neg():
                    var.get('options').put('data', Js(True))
                if var.get('options').get('compat'):
                    var.get('options').put('useDepths', Js(True))
                var.put('ast', var.get('env').callprop('parse', var.get('input'), var.get('options')))
                var.put('environment', var.get('env').get('Compiler').create().callprop('compile', var.get('ast'), var.get('options')))
                return var.get('env').get('JavaScriptCompiler').create().callprop('compile', var.get('environment'), var.get('options'))
            PyJsHoisted_precompile_.func_name = 'precompile'
            var.put('precompile', PyJsHoisted_precompile_)
            @Js
            def PyJsHoisted_compile_(input, options, env, this, arguments, var=var):
                var = Scope({'input':input, 'options':options, 'env':env, 'this':this, 'arguments':arguments}, var)
                var.registers(['env', 'compileInput', 'input', 'compiled', 'ret', 'options'])
                @Js
                def PyJsHoisted_compileInput_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers(['templateSpec', 'environment', 'ast'])
                    var.put('ast', var.get('env').callprop('parse', var.get('input'), var.get('options')))
                    var.put('environment', var.get('env').get('Compiler').create().callprop('compile', var.get('ast'), var.get('options')))
                    var.put('templateSpec', var.get('env').get('JavaScriptCompiler').create().callprop('compile', var.get('environment'), var.get('options'), var.get('undefined'), Js(True)))
                    return var.get('env').callprop('template', var.get('templateSpec'))
                PyJsHoisted_compileInput_.func_name = 'compileInput'
                var.put('compileInput', PyJsHoisted_compileInput_)
                @Js
                def PyJsHoisted_ret_(context, execOptions, this, arguments, var=var):
                    var = Scope({'context':context, 'execOptions':execOptions, 'this':this, 'arguments':arguments}, var)
                    var.registers(['context', 'execOptions'])
                    if var.get('compiled').neg():
                        var.put('compiled', var.get('compileInput')())
                    return var.get('compiled').callprop('call', var.get(u"this"), var.get('context'), var.get('execOptions'))
                PyJsHoisted_ret_.func_name = 'ret'
                var.put('ret', PyJsHoisted_ret_)
                if PyJsStrictEq(var.get('options'),var.get('undefined')):
                    var.put('options', Js({}))
                if ((var.get('input')==var.get(u"null")) or (PyJsStrictNeq(var.get('input',throw=False).typeof(),Js('string')) and PyJsStrictNeq(var.get('input').get('type'),Js('Program')))):
                    PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('You must pass a string or Handlebars AST to Handlebars.compile. You passed ')+var.get('input'))))
                    raise PyJsTempException
                var.put('options', var.get('_utils').callprop('extend', Js({}), var.get('options')))
                if var.get('options').contains(Js('data')).neg():
                    var.get('options').put('data', Js(True))
                if var.get('options').get('compat'):
                    var.get('options').put('useDepths', Js(True))
                var.put('compiled', var.get('undefined'))
                pass
                pass
                @Js
                def PyJs_anonymous_330_(setupOptions, this, arguments, var=var):
                    var = Scope({'setupOptions':setupOptions, 'this':this, 'arguments':arguments}, var)
                    var.registers(['setupOptions'])
                    if var.get('compiled').neg():
                        var.put('compiled', var.get('compileInput')())
                    return var.get('compiled').callprop('_setup', var.get('setupOptions'))
                PyJs_anonymous_330_._set_name('anonymous')
                var.get('ret').put('_setup', PyJs_anonymous_330_)
                @Js
                def PyJs_anonymous_331_(i, data, blockParams, depths, this, arguments, var=var):
                    var = Scope({'i':i, 'data':data, 'blockParams':blockParams, 'depths':depths, 'this':this, 'arguments':arguments}, var)
                    var.registers(['depths', 'data', 'blockParams', 'i'])
                    if var.get('compiled').neg():
                        var.put('compiled', var.get('compileInput')())
                    return var.get('compiled').callprop('_child', var.get('i'), var.get('data'), var.get('blockParams'), var.get('depths'))
                PyJs_anonymous_331_._set_name('anonymous')
                var.get('ret').put('_child', PyJs_anonymous_331_)
                return var.get('ret')
            PyJsHoisted_compile_.func_name = 'compile'
            var.put('compile', PyJsHoisted_compile_)
            @Js
            def PyJsHoisted_argEquals_(a, b, this, arguments, var=var):
                var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
                var.registers(['a', 'i', 'b'])
                if PyJsStrictEq(var.get('a'),var.get('b')):
                    return Js(True)
                if ((var.get('_utils').callprop('isArray', var.get('a')) and var.get('_utils').callprop('isArray', var.get('b'))) and PyJsStrictEq(var.get('a').get('length'),var.get('b').get('length'))):
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('a').get('length')):
                        if var.get('argEquals')(var.get('a').get(var.get('i')), var.get('b').get(var.get('i'))).neg():
                            return Js(False)
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    return Js(True)
            PyJsHoisted_argEquals_.func_name = 'argEquals'
            var.put('argEquals', PyJsHoisted_argEquals_)
            @Js
            def PyJsHoisted_transformLiteralToPath_(sexpr, this, arguments, var=var):
                var = Scope({'sexpr':sexpr, 'this':this, 'arguments':arguments}, var)
                var.registers(['literal', 'sexpr'])
                if var.get('sexpr').get('path').get('parts').neg():
                    var.put('literal', var.get('sexpr').get('path'))
                    var.get('sexpr').put('path', Js({'type':Js('PathExpression'),'data':Js(False),'depth':Js(0.0),'parts':Js([(var.get('literal').get('original')+Js(''))]),'original':(var.get('literal').get('original')+Js('')),'loc':var.get('literal').get('loc')}))
            PyJsHoisted_transformLiteralToPath_.func_name = 'transformLiteralToPath'
            var.put('transformLiteralToPath', PyJsHoisted_transformLiteralToPath_)
            Js('use strict')
            var.put('_Object$create', var.get('__webpack_require__')(Js(74.0)).get('default'))
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.get('exports').put('Compiler', var.get('Compiler'))
            var.get('exports').put('precompile', var.get('precompile'))
            var.get('exports').put('compile', var.get('compile'))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('_ast', var.get('__webpack_require__')(Js(84.0)))
            var.put('_ast2', var.get('_interopRequireDefault')(var.get('_ast')))
            var.put('slice', Js([]).get('slice'))
            pass
            def PyJs_LONG_329_(var=var):
                @Js
                def PyJs_equals_298_(other, this, arguments, var=var):
                    var = Scope({'other':other, 'this':this, 'arguments':arguments, 'equals':PyJs_equals_298_}, var)
                    var.registers(['opcode', 'other', 'otherOpcode', 'i', 'len'])
                    var.put('len', var.get(u"this").get('opcodes').get('length'))
                    if PyJsStrictNeq(var.get('other').get('opcodes').get('length'),var.get('len')):
                        return Js(False)
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('len')):
                        var.put('opcode', var.get(u"this").get('opcodes').get(var.get('i')))
                        var.put('otherOpcode', var.get('other').get('opcodes').get(var.get('i')))
                        if (PyJsStrictNeq(var.get('opcode').get('opcode'),var.get('otherOpcode').get('opcode')) or var.get('argEquals')(var.get('opcode').get('args'), var.get('otherOpcode').get('args')).neg()):
                            return Js(False)
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    var.put('len', var.get(u"this").get('children').get('length'))
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('len')):
                        if var.get(u"this").get('children').get(var.get('i')).callprop('equals', var.get('other').get('children').get(var.get('i'))).neg():
                            return Js(False)
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    return Js(True)
                PyJs_equals_298_._set_name('equals')
                @Js
                def PyJs_compile_299_(program, options, this, arguments, var=var):
                    var = Scope({'program':program, 'options':options, 'this':this, 'arguments':arguments, 'compile':PyJs_compile_299_}, var)
                    var.registers(['program', 'options'])
                    var.get(u"this").put('sourceNode', Js([]))
                    var.get(u"this").put('opcodes', Js([]))
                    var.get(u"this").put('children', Js([]))
                    var.get(u"this").put('options', var.get('options'))
                    var.get(u"this").put('stringParams', var.get('options').get('stringParams'))
                    var.get(u"this").put('trackIds', var.get('options').get('trackIds'))
                    var.get('options').put('blockParams', (var.get('options').get('blockParams') or Js([])))
                    var.get('options').put('knownHelpers', var.get('_utils').callprop('extend', var.get('_Object$create')(var.get(u"null")), Js({'helperMissing':Js(True),'blockHelperMissing':Js(True),'each':Js(True),'if':Js(True),'unless':Js(True),'with':Js(True),'log':Js(True),'lookup':Js(True)}), var.get('options').get('knownHelpers')))
                    return var.get(u"this").callprop('accept', var.get('program'))
                PyJs_compile_299_._set_name('compile')
                @Js
                def PyJs_compileProgram_300_(program, this, arguments, var=var):
                    var = Scope({'program':program, 'this':this, 'arguments':arguments, 'compileProgram':PyJs_compileProgram_300_}, var)
                    var.registers(['result', 'program', 'guid', 'childCompiler'])
                    var.put('childCompiler', var.get(u"this").get('compiler').create())
                    var.put('result', var.get('childCompiler').callprop('compile', var.get('program'), var.get(u"this").get('options')))
                    var.put('guid', (var.get(u"this").put('guid',Js(var.get(u"this").get('guid').to_number())+Js(1))-Js(1)))
                    var.get(u"this").put('usePartial', (var.get(u"this").get('usePartial') or var.get('result').get('usePartial')))
                    var.get(u"this").get('children').put(var.get('guid'), var.get('result'))
                    var.get(u"this").put('useDepths', (var.get(u"this").get('useDepths') or var.get('result').get('useDepths')))
                    return var.get('guid')
                PyJs_compileProgram_300_._set_name('compileProgram')
                @Js
                def PyJs_accept_301_(node, this, arguments, var=var):
                    var = Scope({'node':node, 'this':this, 'arguments':arguments, 'accept':PyJs_accept_301_}, var)
                    var.registers(['ret', 'node'])
                    if var.get(u"this").get(var.get('node').get('type')).neg():
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('Unknown type: ')+var.get('node').get('type')), var.get('node')))
                        raise PyJsTempException
                    var.get(u"this").get('sourceNode').callprop('unshift', var.get('node'))
                    var.put('ret', var.get(u"this").callprop(var.get('node').get('type'), var.get('node')))
                    var.get(u"this").get('sourceNode').callprop('shift')
                    return var.get('ret')
                PyJs_accept_301_._set_name('accept')
                @Js
                def PyJs_Program_302_(program, this, arguments, var=var):
                    var = Scope({'program':program, 'this':this, 'arguments':arguments, 'Program':PyJs_Program_302_}, var)
                    var.registers(['bodyLength', 'program', 'i', 'body'])
                    var.get(u"this").get('options').get('blockParams').callprop('unshift', var.get('program').get('blockParams'))
                    var.put('body', var.get('program').get('body'))
                    var.put('bodyLength', var.get('body').get('length'))
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('bodyLength')):
                        var.get(u"this").callprop('accept', var.get('body').get(var.get('i')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    var.get(u"this").get('options').get('blockParams').callprop('shift')
                    var.get(u"this").put('isSimple', PyJsStrictEq(var.get('bodyLength'),Js(1.0)))
                    var.get(u"this").put('blockParams', (var.get('program').get('blockParams').get('length') if var.get('program').get('blockParams') else Js(0.0)))
                    return var.get(u"this")
                PyJs_Program_302_._set_name('Program')
                @Js
                def PyJs_BlockStatement_303_(block, this, arguments, var=var):
                    var = Scope({'block':block, 'this':this, 'arguments':arguments, 'BlockStatement':PyJs_BlockStatement_303_}, var)
                    var.registers(['block', 'program', 'inverse', 'type'])
                    var.get('transformLiteralToPath')(var.get('block'))
                    var.put('program', var.get('block').get('program'))
                    var.put('inverse', var.get('block').get('inverse'))
                    var.put('program', (var.get('program') and var.get(u"this").callprop('compileProgram', var.get('program'))))
                    var.put('inverse', (var.get('inverse') and var.get(u"this").callprop('compileProgram', var.get('inverse'))))
                    var.put('type', var.get(u"this").callprop('classifySexpr', var.get('block')))
                    if PyJsStrictEq(var.get('type'),Js('helper')):
                        var.get(u"this").callprop('helperSexpr', var.get('block'), var.get('program'), var.get('inverse'))
                    else:
                        if PyJsStrictEq(var.get('type'),Js('simple')):
                            var.get(u"this").callprop('simpleSexpr', var.get('block'))
                            var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('program'))
                            var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('inverse'))
                            var.get(u"this").callprop('opcode', Js('emptyHash'))
                            var.get(u"this").callprop('opcode', Js('blockValue'), var.get('block').get('path').get('original'))
                        else:
                            var.get(u"this").callprop('ambiguousSexpr', var.get('block'), var.get('program'), var.get('inverse'))
                            var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('program'))
                            var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('inverse'))
                            var.get(u"this").callprop('opcode', Js('emptyHash'))
                            var.get(u"this").callprop('opcode', Js('ambiguousBlockValue'))
                    var.get(u"this").callprop('opcode', Js('append'))
                PyJs_BlockStatement_303_._set_name('BlockStatement')
                @Js
                def PyJs_DecoratorBlock_304_(decorator, this, arguments, var=var):
                    var = Scope({'decorator':decorator, 'this':this, 'arguments':arguments, 'DecoratorBlock':PyJs_DecoratorBlock_304_}, var)
                    var.registers(['program', 'path', 'decorator', 'params'])
                    var.put('program', (var.get('decorator').get('program') and var.get(u"this").callprop('compileProgram', var.get('decorator').get('program'))))
                    var.put('params', var.get(u"this").callprop('setupFullMustacheParams', var.get('decorator'), var.get('program'), var.get('undefined')))
                    var.put('path', var.get('decorator').get('path'))
                    var.get(u"this").put('useDecorators', Js(True))
                    var.get(u"this").callprop('opcode', Js('registerDecorator'), var.get('params').get('length'), var.get('path').get('original'))
                PyJs_DecoratorBlock_304_._set_name('DecoratorBlock')
                @Js
                def PyJs_PartialStatement_305_(partial, this, arguments, var=var):
                    var = Scope({'partial':partial, 'this':this, 'arguments':arguments, 'PartialStatement':PyJs_PartialStatement_305_}, var)
                    var.registers(['program', 'indent', 'params', 'partialName', 'isDynamic', 'partial'])
                    var.get(u"this").put('usePartial', Js(True))
                    var.put('program', var.get('partial').get('program'))
                    if var.get('program'):
                        var.put('program', var.get(u"this").callprop('compileProgram', var.get('partial').get('program')))
                    var.put('params', var.get('partial').get('params'))
                    if (var.get('params').get('length')>Js(1.0)):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('Unsupported number of partial arguments: ')+var.get('params').get('length')), var.get('partial')))
                        raise PyJsTempException
                    else:
                        if var.get('params').get('length').neg():
                            if var.get(u"this").get('options').get('explicitPartialContext'):
                                var.get(u"this").callprop('opcode', Js('pushLiteral'), Js('undefined'))
                            else:
                                var.get('params').callprop('push', Js({'type':Js('PathExpression'),'parts':Js([]),'depth':Js(0.0)}))
                    var.put('partialName', var.get('partial').get('name').get('original'))
                    var.put('isDynamic', PyJsStrictEq(var.get('partial').get('name').get('type'),Js('SubExpression')))
                    if var.get('isDynamic'):
                        var.get(u"this").callprop('accept', var.get('partial').get('name'))
                    var.get(u"this").callprop('setupFullMustacheParams', var.get('partial'), var.get('program'), var.get('undefined'), Js(True))
                    var.put('indent', (var.get('partial').get('indent') or Js('')))
                    if (var.get(u"this").get('options').get('preventIndent') and var.get('indent')):
                        var.get(u"this").callprop('opcode', Js('appendContent'), var.get('indent'))
                        var.put('indent', Js(''))
                    var.get(u"this").callprop('opcode', Js('invokePartial'), var.get('isDynamic'), var.get('partialName'), var.get('indent'))
                    var.get(u"this").callprop('opcode', Js('append'))
                PyJs_PartialStatement_305_._set_name('PartialStatement')
                @Js
                def PyJs_PartialBlockStatement_306_(partialBlock, this, arguments, var=var):
                    var = Scope({'partialBlock':partialBlock, 'this':this, 'arguments':arguments, 'PartialBlockStatement':PyJs_PartialBlockStatement_306_}, var)
                    var.registers(['partialBlock'])
                    var.get(u"this").callprop('PartialStatement', var.get('partialBlock'))
                PyJs_PartialBlockStatement_306_._set_name('PartialBlockStatement')
                @Js
                def PyJs_MustacheStatement_307_(mustache, this, arguments, var=var):
                    var = Scope({'mustache':mustache, 'this':this, 'arguments':arguments, 'MustacheStatement':PyJs_MustacheStatement_307_}, var)
                    var.registers(['mustache'])
                    var.get(u"this").callprop('SubExpression', var.get('mustache'))
                    if (var.get('mustache').get('escaped') and var.get(u"this").get('options').get('noEscape').neg()):
                        var.get(u"this").callprop('opcode', Js('appendEscaped'))
                    else:
                        var.get(u"this").callprop('opcode', Js('append'))
                PyJs_MustacheStatement_307_._set_name('MustacheStatement')
                @Js
                def PyJs_Decorator_308_(decorator, this, arguments, var=var):
                    var = Scope({'decorator':decorator, 'this':this, 'arguments':arguments, 'Decorator':PyJs_Decorator_308_}, var)
                    var.registers(['decorator'])
                    var.get(u"this").callprop('DecoratorBlock', var.get('decorator'))
                PyJs_Decorator_308_._set_name('Decorator')
                @Js
                def PyJs_ContentStatement_309_(content, this, arguments, var=var):
                    var = Scope({'content':content, 'this':this, 'arguments':arguments, 'ContentStatement':PyJs_ContentStatement_309_}, var)
                    var.registers(['content'])
                    if var.get('content').get('value'):
                        var.get(u"this").callprop('opcode', Js('appendContent'), var.get('content').get('value'))
                PyJs_ContentStatement_309_._set_name('ContentStatement')
                @Js
                def PyJs_CommentStatement_310_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'CommentStatement':PyJs_CommentStatement_310_}, var)
                    var.registers([])
                    pass
                PyJs_CommentStatement_310_._set_name('CommentStatement')
                @Js
                def PyJs_SubExpression_311_(sexpr, this, arguments, var=var):
                    var = Scope({'sexpr':sexpr, 'this':this, 'arguments':arguments, 'SubExpression':PyJs_SubExpression_311_}, var)
                    var.registers(['sexpr', 'type'])
                    var.get('transformLiteralToPath')(var.get('sexpr'))
                    var.put('type', var.get(u"this").callprop('classifySexpr', var.get('sexpr')))
                    if PyJsStrictEq(var.get('type'),Js('simple')):
                        var.get(u"this").callprop('simpleSexpr', var.get('sexpr'))
                    else:
                        if PyJsStrictEq(var.get('type'),Js('helper')):
                            var.get(u"this").callprop('helperSexpr', var.get('sexpr'))
                        else:
                            var.get(u"this").callprop('ambiguousSexpr', var.get('sexpr'))
                PyJs_SubExpression_311_._set_name('SubExpression')
                @Js
                def PyJs_ambiguousSexpr_312_(sexpr, program, inverse, this, arguments, var=var):
                    var = Scope({'sexpr':sexpr, 'program':program, 'inverse':inverse, 'this':this, 'arguments':arguments, 'ambiguousSexpr':PyJs_ambiguousSexpr_312_}, var)
                    var.registers(['program', 'sexpr', 'name', 'inverse', 'isBlock', 'path'])
                    var.put('path', var.get('sexpr').get('path'))
                    var.put('name', var.get('path').get('parts').get('0'))
                    var.put('isBlock', ((var.get('program')!=var.get(u"null")) or (var.get('inverse')!=var.get(u"null"))))
                    var.get(u"this").callprop('opcode', Js('getContext'), var.get('path').get('depth'))
                    var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('program'))
                    var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('inverse'))
                    var.get('path').put('strict', Js(True))
                    var.get(u"this").callprop('accept', var.get('path'))
                    var.get(u"this").callprop('opcode', Js('invokeAmbiguous'), var.get('name'), var.get('isBlock'))
                PyJs_ambiguousSexpr_312_._set_name('ambiguousSexpr')
                @Js
                def PyJs_simpleSexpr_313_(sexpr, this, arguments, var=var):
                    var = Scope({'sexpr':sexpr, 'this':this, 'arguments':arguments, 'simpleSexpr':PyJs_simpleSexpr_313_}, var)
                    var.registers(['sexpr', 'path'])
                    var.put('path', var.get('sexpr').get('path'))
                    var.get('path').put('strict', Js(True))
                    var.get(u"this").callprop('accept', var.get('path'))
                    var.get(u"this").callprop('opcode', Js('resolvePossibleLambda'))
                PyJs_simpleSexpr_313_._set_name('simpleSexpr')
                @Js
                def PyJs_helperSexpr_314_(sexpr, program, inverse, this, arguments, var=var):
                    var = Scope({'sexpr':sexpr, 'program':program, 'inverse':inverse, 'this':this, 'arguments':arguments, 'helperSexpr':PyJs_helperSexpr_314_}, var)
                    var.registers(['program', 'sexpr', 'params', 'name', 'inverse', 'path'])
                    var.put('params', var.get(u"this").callprop('setupFullMustacheParams', var.get('sexpr'), var.get('program'), var.get('inverse')))
                    var.put('path', var.get('sexpr').get('path'))
                    var.put('name', var.get('path').get('parts').get('0'))
                    if var.get(u"this").get('options').get('knownHelpers').get(var.get('name')):
                        var.get(u"this").callprop('opcode', Js('invokeKnownHelper'), var.get('params').get('length'), var.get('name'))
                    else:
                        if var.get(u"this").get('options').get('knownHelpersOnly'):
                            PyJsTempException = JsToPyException(var.get('_exception2').get('default').create((Js('You specified knownHelpersOnly, but used the unknown helper ')+var.get('name')), var.get('sexpr')))
                            raise PyJsTempException
                        else:
                            var.get('path').put('strict', Js(True))
                            var.get('path').put('falsy', Js(True))
                            var.get(u"this").callprop('accept', var.get('path'))
                            var.get(u"this").callprop('opcode', Js('invokeHelper'), var.get('params').get('length'), var.get('path').get('original'), var.get('_ast2').get('default').get('helpers').callprop('simpleId', var.get('path')))
                PyJs_helperSexpr_314_._set_name('helperSexpr')
                @Js
                def PyJs_PathExpression_315_(path, this, arguments, var=var):
                    var = Scope({'path':path, 'this':this, 'arguments':arguments, 'PathExpression':PyJs_PathExpression_315_}, var)
                    var.registers(['blockParamId', 'name', 'scoped', 'path'])
                    var.get(u"this").callprop('addDepth', var.get('path').get('depth'))
                    var.get(u"this").callprop('opcode', Js('getContext'), var.get('path').get('depth'))
                    var.put('name', var.get('path').get('parts').get('0'))
                    var.put('scoped', var.get('_ast2').get('default').get('helpers').callprop('scopedId', var.get('path')))
                    var.put('blockParamId', ((var.get('path').get('depth').neg() and var.get('scoped').neg()) and var.get(u"this").callprop('blockParamIndex', var.get('name'))))
                    if var.get('blockParamId'):
                        var.get(u"this").callprop('opcode', Js('lookupBlockParam'), var.get('blockParamId'), var.get('path').get('parts'))
                    else:
                        if var.get('name').neg():
                            var.get(u"this").callprop('opcode', Js('pushContext'))
                        else:
                            if var.get('path').get('data'):
                                var.get(u"this").get('options').put('data', Js(True))
                                var.get(u"this").callprop('opcode', Js('lookupData'), var.get('path').get('depth'), var.get('path').get('parts'), var.get('path').get('strict'))
                            else:
                                var.get(u"this").callprop('opcode', Js('lookupOnContext'), var.get('path').get('parts'), var.get('path').get('falsy'), var.get('path').get('strict'), var.get('scoped'))
                PyJs_PathExpression_315_._set_name('PathExpression')
                @Js
                def PyJs_StringLiteral_316_(string, this, arguments, var=var):
                    var = Scope({'string':string, 'this':this, 'arguments':arguments, 'StringLiteral':PyJs_StringLiteral_316_}, var)
                    var.registers(['string'])
                    var.get(u"this").callprop('opcode', Js('pushString'), var.get('string').get('value'))
                PyJs_StringLiteral_316_._set_name('StringLiteral')
                @Js
                def PyJs_NumberLiteral_317_(number, this, arguments, var=var):
                    var = Scope({'number':number, 'this':this, 'arguments':arguments, 'NumberLiteral':PyJs_NumberLiteral_317_}, var)
                    var.registers(['number'])
                    var.get(u"this").callprop('opcode', Js('pushLiteral'), var.get('number').get('value'))
                PyJs_NumberLiteral_317_._set_name('NumberLiteral')
                @Js
                def PyJs_BooleanLiteral_318_(bool, this, arguments, var=var):
                    var = Scope({'bool':bool, 'this':this, 'arguments':arguments, 'BooleanLiteral':PyJs_BooleanLiteral_318_}, var)
                    var.registers(['bool'])
                    var.get(u"this").callprop('opcode', Js('pushLiteral'), var.get('bool').get('value'))
                PyJs_BooleanLiteral_318_._set_name('BooleanLiteral')
                @Js
                def PyJs_UndefinedLiteral_319_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'UndefinedLiteral':PyJs_UndefinedLiteral_319_}, var)
                    var.registers([])
                    var.get(u"this").callprop('opcode', Js('pushLiteral'), Js('undefined'))
                PyJs_UndefinedLiteral_319_._set_name('UndefinedLiteral')
                @Js
                def PyJs_NullLiteral_320_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'NullLiteral':PyJs_NullLiteral_320_}, var)
                    var.registers([])
                    var.get(u"this").callprop('opcode', Js('pushLiteral'), Js('null'))
                PyJs_NullLiteral_320_._set_name('NullLiteral')
                @Js
                def PyJs_Hash_321_(hash, this, arguments, var=var):
                    var = Scope({'hash':hash, 'this':this, 'arguments':arguments, 'Hash':PyJs_Hash_321_}, var)
                    var.registers(['hash', 'l', 'i', 'pairs'])
                    var.put('pairs', var.get('hash').get('pairs'))
                    var.put('i', Js(0.0))
                    var.put('l', var.get('pairs').get('length'))
                    var.get(u"this").callprop('opcode', Js('pushHash'))
                    #for JS loop
                    
                    while (var.get('i')<var.get('l')):
                        var.get(u"this").callprop('pushParam', var.get('pairs').get(var.get('i')).get('value'))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    while (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1)):
                        var.get(u"this").callprop('opcode', Js('assignToHash'), var.get('pairs').get(var.get('i')).get('key'))
                    var.get(u"this").callprop('opcode', Js('popHash'))
                PyJs_Hash_321_._set_name('Hash')
                @Js
                def PyJs_opcode_322_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'opcode':PyJs_opcode_322_}, var)
                    var.registers(['name'])
                    var.get(u"this").get('opcodes').callprop('push', Js({'opcode':var.get('name'),'args':var.get('slice').callprop('call', var.get('arguments'), Js(1.0)),'loc':var.get(u"this").get('sourceNode').get('0').get('loc')}))
                PyJs_opcode_322_._set_name('opcode')
                @Js
                def PyJs_addDepth_323_(depth, this, arguments, var=var):
                    var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'addDepth':PyJs_addDepth_323_}, var)
                    var.registers(['depth'])
                    if var.get('depth').neg():
                        return var.get('undefined')
                    var.get(u"this").put('useDepths', Js(True))
                PyJs_addDepth_323_._set_name('addDepth')
                @Js
                def PyJs_classifySexpr_324_(sexpr, this, arguments, var=var):
                    var = Scope({'sexpr':sexpr, 'this':this, 'arguments':arguments, 'classifySexpr':PyJs_classifySexpr_324_}, var)
                    var.registers(['sexpr', 'isBlockParam', 'isHelper', '_name', 'options', 'isSimple', 'isEligible'])
                    var.put('isSimple', var.get('_ast2').get('default').get('helpers').callprop('simpleId', var.get('sexpr').get('path')))
                    var.put('isBlockParam', (var.get('isSimple') and var.get(u"this").callprop('blockParamIndex', var.get('sexpr').get('path').get('parts').get('0')).neg().neg()))
                    var.put('isHelper', (var.get('isBlockParam').neg() and var.get('_ast2').get('default').get('helpers').callprop('helperExpression', var.get('sexpr'))))
                    var.put('isEligible', (var.get('isBlockParam').neg() and (var.get('isHelper') or var.get('isSimple'))))
                    if (var.get('isEligible') and var.get('isHelper').neg()):
                        var.put('_name', var.get('sexpr').get('path').get('parts').get('0'))
                        var.put('options', var.get(u"this").get('options'))
                        if var.get('options').get('knownHelpers').get(var.get('_name')):
                            var.put('isHelper', Js(True))
                        else:
                            if var.get('options').get('knownHelpersOnly'):
                                var.put('isEligible', Js(False))
                    if var.get('isHelper'):
                        return Js('helper')
                    else:
                        if var.get('isEligible'):
                            return Js('ambiguous')
                        else:
                            return Js('simple')
                PyJs_classifySexpr_324_._set_name('classifySexpr')
                @Js
                def PyJs_pushParams_325_(params, this, arguments, var=var):
                    var = Scope({'params':params, 'this':this, 'arguments':arguments, 'pushParams':PyJs_pushParams_325_}, var)
                    var.registers(['l', 'i', 'params'])
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('l', var.get('params').get('length'))
                    while (var.get('i')<var.get('l')):
                        var.get(u"this").callprop('pushParam', var.get('params').get(var.get('i')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_pushParams_325_._set_name('pushParams')
                @Js
                def PyJs_pushParam_326_(val, this, arguments, var=var):
                    var = Scope({'val':val, 'this':this, 'arguments':arguments, 'pushParam':PyJs_pushParam_326_}, var)
                    var.registers(['blockParamIndex', 'blockParamChild', 'val', 'value'])
                    var.put('value', (var.get('val').get('value') if (var.get('val').get('value')!=var.get(u"null")) else (var.get('val').get('original') or Js(''))))
                    if var.get(u"this").get('stringParams'):
                        if var.get('value').get('replace'):
                            var.put('value', var.get('value').callprop('replace', JsRegExp('/^(\\.?\\.\\/)*/g'), Js('')).callprop('replace', JsRegExp('/\\//g'), Js('.')))
                        if var.get('val').get('depth'):
                            var.get(u"this").callprop('addDepth', var.get('val').get('depth'))
                        var.get(u"this").callprop('opcode', Js('getContext'), (var.get('val').get('depth') or Js(0.0)))
                        var.get(u"this").callprop('opcode', Js('pushStringParam'), var.get('value'), var.get('val').get('type'))
                        if PyJsStrictEq(var.get('val').get('type'),Js('SubExpression')):
                            var.get(u"this").callprop('accept', var.get('val'))
                    else:
                        if var.get(u"this").get('trackIds'):
                            var.put('blockParamIndex', var.get('undefined'))
                            if ((var.get('val').get('parts') and var.get('_ast2').get('default').get('helpers').callprop('scopedId', var.get('val')).neg()) and var.get('val').get('depth').neg()):
                                var.put('blockParamIndex', var.get(u"this").callprop('blockParamIndex', var.get('val').get('parts').get('0')))
                            if var.get('blockParamIndex'):
                                var.put('blockParamChild', var.get('val').get('parts').callprop('slice', Js(1.0)).callprop('join', Js('.')))
                                var.get(u"this").callprop('opcode', Js('pushId'), Js('BlockParam'), var.get('blockParamIndex'), var.get('blockParamChild'))
                            else:
                                var.put('value', (var.get('val').get('original') or var.get('value')))
                                if var.get('value').get('replace'):
                                    var.put('value', var.get('value').callprop('replace', JsRegExp('/^this(?:\\.|$)/'), Js('')).callprop('replace', JsRegExp('/^\\.\\//'), Js('')).callprop('replace', JsRegExp('/^\\.$/'), Js('')))
                                var.get(u"this").callprop('opcode', Js('pushId'), var.get('val').get('type'), var.get('value'))
                        var.get(u"this").callprop('accept', var.get('val'))
                PyJs_pushParam_326_._set_name('pushParam')
                @Js
                def PyJs_setupFullMustacheParams_327_(sexpr, program, inverse, omitEmpty, this, arguments, var=var):
                    var = Scope({'sexpr':sexpr, 'program':program, 'inverse':inverse, 'omitEmpty':omitEmpty, 'this':this, 'arguments':arguments, 'setupFullMustacheParams':PyJs_setupFullMustacheParams_327_}, var)
                    var.registers(['program', 'sexpr', 'params', 'inverse', 'omitEmpty'])
                    var.put('params', var.get('sexpr').get('params'))
                    var.get(u"this").callprop('pushParams', var.get('params'))
                    var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('program'))
                    var.get(u"this").callprop('opcode', Js('pushProgram'), var.get('inverse'))
                    if var.get('sexpr').get('hash'):
                        var.get(u"this").callprop('accept', var.get('sexpr').get('hash'))
                    else:
                        var.get(u"this").callprop('opcode', Js('emptyHash'), var.get('omitEmpty'))
                    return var.get('params')
                PyJs_setupFullMustacheParams_327_._set_name('setupFullMustacheParams')
                @Js
                def PyJs_blockParamIndex_328_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'blockParamIndex':PyJs_blockParamIndex_328_}, var)
                    var.registers(['param', 'len', 'name', 'depth', 'blockParams'])
                    #for JS loop
                    var.put('depth', Js(0.0))
                    var.put('len', var.get(u"this").get('options').get('blockParams').get('length'))
                    while (var.get('depth')<var.get('len')):
                        var.put('blockParams', var.get(u"this").get('options').get('blockParams').get(var.get('depth')))
                        var.put('param', (var.get('blockParams') and var.get('_utils').callprop('indexOf', var.get('blockParams'), var.get('name'))))
                        if (var.get('blockParams') and (var.get('param')>=Js(0.0))):
                            return Js([var.get('depth'), var.get('param')])
                        # update
                        (var.put('depth',Js(var.get('depth').to_number())+Js(1))-Js(1))
                PyJs_blockParamIndex_328_._set_name('blockParamIndex')
                return var.get('Compiler').put('prototype', Js({'compiler':var.get('Compiler'),'equals':PyJs_equals_298_,'guid':Js(0.0),'compile':PyJs_compile_299_,'compileProgram':PyJs_compileProgram_300_,'accept':PyJs_accept_301_,'Program':PyJs_Program_302_,'BlockStatement':PyJs_BlockStatement_303_,'DecoratorBlock':PyJs_DecoratorBlock_304_,'PartialStatement':PyJs_PartialStatement_305_,'PartialBlockStatement':PyJs_PartialBlockStatement_306_,'MustacheStatement':PyJs_MustacheStatement_307_,'Decorator':PyJs_Decorator_308_,'ContentStatement':PyJs_ContentStatement_309_,'CommentStatement':PyJs_CommentStatement_310_,'SubExpression':PyJs_SubExpression_311_,'ambiguousSexpr':PyJs_ambiguousSexpr_312_,'simpleSexpr':PyJs_simpleSexpr_313_,'helperSexpr':PyJs_helperSexpr_314_,'PathExpression':PyJs_PathExpression_315_,'StringLiteral':PyJs_StringLiteral_316_,'NumberLiteral':PyJs_NumberLiteral_317_,'BooleanLiteral':PyJs_BooleanLiteral_318_,'UndefinedLiteral':PyJs_UndefinedLiteral_319_,'NullLiteral':PyJs_NullLiteral_320_,'Hash':PyJs_Hash_321_,'opcode':PyJs_opcode_322_,'addDepth':PyJs_addDepth_323_,'classifySexpr':PyJs_classifySexpr_324_,'pushParams':PyJs_pushParams_325_,'pushParam':PyJs_pushParam_326_,'setupFullMustacheParams':PyJs_setupFullMustacheParams_327_,'blockParamIndex':PyJs_blockParamIndex_328_}))
            PyJs_LONG_329_()
            pass
            pass
            pass
            pass
        PyJs_anonymous_297_._set_name('anonymous')
        @Js
        def PyJs_anonymous_332_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['_base', '_interopRequireDefault', '_codeGen', 'exports', '_exception2', 'module', '_exception', '_Object$keys', 'JavaScriptCompiler', '_utils', '__webpack_require__', 'Literal', 'strictLookup', '_codeGen2'])
            @Js
            def PyJsHoisted_Literal_(value, this, arguments, var=var):
                var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
                var.registers(['value'])
                var.get(u"this").put('value', var.get('value'))
            PyJsHoisted_Literal_.func_name = 'Literal'
            var.put('Literal', PyJsHoisted_Literal_)
            @Js
            def PyJsHoisted_JavaScriptCompiler_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                pass
            PyJsHoisted_JavaScriptCompiler_.func_name = 'JavaScriptCompiler'
            var.put('JavaScriptCompiler', PyJsHoisted_JavaScriptCompiler_)
            @Js
            def PyJsHoisted_strictLookup_(requireTerminal, compiler, parts, i, type, this, arguments, var=var):
                var = Scope({'requireTerminal':requireTerminal, 'compiler':compiler, 'parts':parts, 'i':i, 'type':type, 'this':this, 'arguments':arguments}, var)
                var.registers(['stack', 'i', 'len', 'type', 'parts', 'compiler', 'requireTerminal'])
                var.put('stack', var.get('compiler').callprop('popStack'))
                var.put('len', var.get('parts').get('length'))
                if var.get('requireTerminal'):
                    (var.put('len',Js(var.get('len').to_number())-Js(1))+Js(1))
                #for JS loop
                
                while (var.get('i')<var.get('len')):
                    var.put('stack', var.get('compiler').callprop('nameLookup', var.get('stack'), var.get('parts').get(var.get('i')), var.get('type')))
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                if var.get('requireTerminal'):
                    return Js([var.get('compiler').callprop('aliasable', Js('container.strict')), Js('('), var.get('stack'), Js(', '), var.get('compiler').callprop('quotedString', var.get('parts').get(var.get('i'))), Js(', '), var.get('JSON').callprop('stringify', var.get('compiler').get('source').get('currentLocation')), Js(' )')])
                else:
                    return var.get('stack')
            PyJsHoisted_strictLookup_.func_name = 'strictLookup'
            var.put('strictLookup', PyJsHoisted_strictLookup_)
            Js('use strict')
            var.put('_Object$keys', var.get('__webpack_require__')(Js(60.0)).get('default'))
            var.put('_interopRequireDefault', var.get('__webpack_require__')(Js(1.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_base', var.get('__webpack_require__')(Js(4.0)))
            var.put('_exception', var.get('__webpack_require__')(Js(6.0)))
            var.put('_exception2', var.get('_interopRequireDefault')(var.get('_exception')))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('_codeGen', var.get('__webpack_require__')(Js(92.0)))
            var.put('_codeGen2', var.get('_interopRequireDefault')(var.get('_codeGen')))
            pass
            pass
            def PyJs_LONG_397_(var=var):
                @Js
                def PyJs_nameLookup_333_(parent, name, this, arguments, var=var):
                    var = Scope({'parent':parent, 'name':name, 'this':this, 'arguments':arguments, 'nameLookup':PyJs_nameLookup_333_}, var)
                    var.registers(['parent', 'name'])
                    return var.get(u"this").callprop('internalNameLookup', var.get('parent'), var.get('name'))
                PyJs_nameLookup_333_._set_name('nameLookup')
                @Js
                def PyJs_depthedLookup_334_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'depthedLookup':PyJs_depthedLookup_334_}, var)
                    var.registers(['name'])
                    return Js([var.get(u"this").callprop('aliasable', Js('container.lookup')), Js('(depths, '), var.get('JSON').callprop('stringify', var.get('name')), Js(')')])
                PyJs_depthedLookup_334_._set_name('depthedLookup')
                @Js
                def PyJs_compilerInfo_335_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'compilerInfo':PyJs_compilerInfo_335_}, var)
                    var.registers(['revision', 'versions'])
                    var.put('revision', var.get('_base').get('COMPILER_REVISION'))
                    var.put('versions', var.get('_base').get('REVISION_CHANGES').get(var.get('revision')))
                    return Js([var.get('revision'), var.get('versions')])
                PyJs_compilerInfo_335_._set_name('compilerInfo')
                @Js
                def PyJs_appendToBuffer_336_(source, location, explicit, this, arguments, var=var):
                    var = Scope({'source':source, 'location':location, 'explicit':explicit, 'this':this, 'arguments':arguments, 'appendToBuffer':PyJs_appendToBuffer_336_}, var)
                    var.registers(['location', 'explicit', 'source'])
                    if var.get('_utils').callprop('isArray', var.get('source')).neg():
                        var.put('source', Js([var.get('source')]))
                    var.put('source', var.get(u"this").get('source').callprop('wrap', var.get('source'), var.get('location')))
                    if var.get(u"this").get('environment').get('isSimple'):
                        return Js([Js('return '), var.get('source'), Js(';')])
                    else:
                        if var.get('explicit'):
                            return Js([Js('buffer += '), var.get('source'), Js(';')])
                        else:
                            var.get('source').put('appendToBuffer', Js(True))
                            return var.get('source')
                PyJs_appendToBuffer_336_._set_name('appendToBuffer')
                @Js
                def PyJs_initializeBuffer_337_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'initializeBuffer':PyJs_initializeBuffer_337_}, var)
                    var.registers([])
                    return var.get(u"this").callprop('quotedString', Js(''))
                PyJs_initializeBuffer_337_._set_name('initializeBuffer')
                @Js
                def PyJs_internalNameLookup_338_(parent, name, this, arguments, var=var):
                    var = Scope({'parent':parent, 'name':name, 'this':this, 'arguments':arguments, 'internalNameLookup':PyJs_internalNameLookup_338_}, var)
                    var.registers(['parent', 'name'])
                    var.get(u"this").put('lookupPropertyFunctionIsUsed', Js(True))
                    return Js([Js('lookupProperty('), var.get('parent'), Js(','), var.get('JSON').callprop('stringify', var.get('name')), Js(')')])
                PyJs_internalNameLookup_338_._set_name('internalNameLookup')
                @Js
                def PyJs_compile_339_(environment, options, context, asObject, this, arguments, var=var):
                    var = Scope({'environment':environment, 'options':options, 'context':context, 'asObject':asObject, 'this':this, 'arguments':arguments, 'compile':PyJs_compile_339_}, var)
                    var.registers(['opcode', 'context', 'l', 'i', 'opcodes', 'decorators', 'fn', '_context', 'programs', 'environment', 'asObject', 'firstLoc', 'ret', 'options'])
                    var.get(u"this").put('environment', var.get('environment'))
                    var.get(u"this").put('options', var.get('options'))
                    var.get(u"this").put('stringParams', var.get(u"this").get('options').get('stringParams'))
                    var.get(u"this").put('trackIds', var.get(u"this").get('options').get('trackIds'))
                    var.get(u"this").put('precompile', var.get('asObject').neg())
                    var.get(u"this").put('name', var.get(u"this").get('environment').get('name'))
                    var.get(u"this").put('isChild', var.get('context').neg().neg())
                    var.get(u"this").put('context', (var.get('context') or Js({'decorators':Js([]),'programs':Js([]),'environments':Js([])})))
                    var.get(u"this").callprop('preamble')
                    var.get(u"this").put('stackSlot', Js(0.0))
                    var.get(u"this").put('stackVars', Js([]))
                    var.get(u"this").put('aliases', Js({}))
                    var.get(u"this").put('registers', Js({'list':Js([])}))
                    var.get(u"this").put('hashes', Js([]))
                    var.get(u"this").put('compileStack', Js([]))
                    var.get(u"this").put('inlineStack', Js([]))
                    var.get(u"this").put('blockParams', Js([]))
                    var.get(u"this").callprop('compileChildren', var.get('environment'), var.get('options'))
                    var.get(u"this").put('useDepths', (((var.get(u"this").get('useDepths') or var.get('environment').get('useDepths')) or var.get('environment').get('useDecorators')) or var.get(u"this").get('options').get('compat')))
                    var.get(u"this").put('useBlockParams', (var.get(u"this").get('useBlockParams') or var.get('environment').get('useBlockParams')))
                    var.put('opcodes', var.get('environment').get('opcodes'))
                    var.put('opcode', var.get('undefined'))
                    var.put('firstLoc', var.get('undefined'))
                    var.put('i', var.get('undefined'))
                    var.put('l', var.get('undefined'))
                    #for JS loop
                    PyJsComma(var.put('i', Js(0.0)),var.put('l', var.get('opcodes').get('length')))
                    while (var.get('i')<var.get('l')):
                        var.put('opcode', var.get('opcodes').get(var.get('i')))
                        var.get(u"this").get('source').put('currentLocation', var.get('opcode').get('loc'))
                        var.put('firstLoc', (var.get('firstLoc') or var.get('opcode').get('loc')))
                        var.get(u"this").get(var.get('opcode').get('opcode')).callprop('apply', var.get(u"this"), var.get('opcode').get('args'))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    var.get(u"this").get('source').put('currentLocation', var.get('firstLoc'))
                    var.get(u"this").callprop('pushSource', Js(''))
                    if ((var.get(u"this").get('stackSlot') or var.get(u"this").get('inlineStack').get('length')) or var.get(u"this").get('compileStack').get('length')):
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('Compile completed with content left on stack')))
                        raise PyJsTempException
                    if var.get(u"this").get('decorators').callprop('isEmpty').neg():
                        var.get(u"this").put('useDecorators', Js(True))
                        var.get(u"this").get('decorators').callprop('prepend', Js([Js('var decorators = container.decorators, '), var.get(u"this").callprop('lookupPropertyFunctionVarDeclaration'), Js(';\n')]))
                        var.get(u"this").get('decorators').callprop('push', Js('return fn;'))
                        if var.get('asObject'):
                            var.get(u"this").put('decorators', var.get('Function').callprop('apply', var.get(u"this"), Js([Js('fn'), Js('props'), Js('container'), Js('depth0'), Js('data'), Js('blockParams'), Js('depths'), var.get(u"this").get('decorators').callprop('merge')])))
                        else:
                            var.get(u"this").get('decorators').callprop('prepend', Js('function(fn, props, container, depth0, data, blockParams, depths) {\n'))
                            var.get(u"this").get('decorators').callprop('push', Js('}\n'))
                            var.get(u"this").put('decorators', var.get(u"this").get('decorators').callprop('merge'))
                    else:
                        var.get(u"this").put('decorators', var.get('undefined'))
                    var.put('fn', var.get(u"this").callprop('createFunctionContext', var.get('asObject')))
                    if var.get(u"this").get('isChild').neg():
                        var.put('ret', Js({'compiler':var.get(u"this").callprop('compilerInfo'),'main':var.get('fn')}))
                        if var.get(u"this").get('decorators'):
                            var.get('ret').put('main_d', var.get(u"this").get('decorators'))
                            var.get('ret').put('useDecorators', Js(True))
                        var.put('_context', var.get(u"this").get('context'))
                        var.put('programs', var.get('_context').get('programs'))
                        var.put('decorators', var.get('_context').get('decorators'))
                        #for JS loop
                        PyJsComma(var.put('i', Js(0.0)),var.put('l', var.get('programs').get('length')))
                        while (var.get('i')<var.get('l')):
                            if var.get('programs').get(var.get('i')):
                                var.get('ret').put(var.get('i'), var.get('programs').get(var.get('i')))
                                if var.get('decorators').get(var.get('i')):
                                    var.get('ret').put((var.get('i')+Js('_d')), var.get('decorators').get(var.get('i')))
                                    var.get('ret').put('useDecorators', Js(True))
                            # update
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                        if var.get(u"this").get('environment').get('usePartial'):
                            var.get('ret').put('usePartial', Js(True))
                        if var.get(u"this").get('options').get('data'):
                            var.get('ret').put('useData', Js(True))
                        if var.get(u"this").get('useDepths'):
                            var.get('ret').put('useDepths', Js(True))
                        if var.get(u"this").get('useBlockParams'):
                            var.get('ret').put('useBlockParams', Js(True))
                        if var.get(u"this").get('options').get('compat'):
                            var.get('ret').put('compat', Js(True))
                        if var.get('asObject').neg():
                            var.get('ret').put('compiler', var.get('JSON').callprop('stringify', var.get('ret').get('compiler')))
                            var.get(u"this").get('source').put('currentLocation', Js({'start':Js({'line':Js(1.0),'column':Js(0.0)})}))
                            var.put('ret', var.get(u"this").callprop('objectLiteral', var.get('ret')))
                            if var.get('options').get('srcName'):
                                var.put('ret', var.get('ret').callprop('toStringWithSourceMap', Js({'file':var.get('options').get('destName')})))
                                var.get('ret').put('map', (var.get('ret').get('map') and var.get('ret').get('map').callprop('toString')))
                            else:
                                var.put('ret', var.get('ret').callprop('toString'))
                        else:
                            var.get('ret').put('compilerOptions', var.get(u"this").get('options'))
                        return var.get('ret')
                    else:
                        return var.get('fn')
                PyJs_compile_339_._set_name('compile')
                @Js
                def PyJs_preamble_340_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'preamble':PyJs_preamble_340_}, var)
                    var.registers([])
                    var.get(u"this").put('lastContext', Js(0.0))
                    var.get(u"this").put('source', var.get('_codeGen2').get('default').create(var.get(u"this").get('options').get('srcName')))
                    var.get(u"this").put('decorators', var.get('_codeGen2').get('default').create(var.get(u"this").get('options').get('srcName')))
                PyJs_preamble_340_._set_name('preamble')
                @Js
                def PyJs_createFunctionContext_341_(asObject, this, arguments, var=var):
                    var = Scope({'asObject':asObject, 'this':this, 'arguments':arguments, 'createFunctionContext':PyJs_createFunctionContext_341_}, var)
                    var.registers(['params', 'varDeclarations', '_this', 'asObject', 'locals', 'aliasCount', 'source'])
                    var.put('_this', var.get(u"this"))
                    var.put('varDeclarations', Js(''))
                    var.put('locals', var.get(u"this").get('stackVars').callprop('concat', var.get(u"this").get('registers').get('list')))
                    if (var.get('locals').get('length')>Js(0.0)):
                        var.put('varDeclarations', (Js(', ')+var.get('locals').callprop('join', Js(', '))), '+')
                    var.put('aliasCount', Js(0.0))
                    @Js
                    def PyJs_anonymous_342_(alias, this, arguments, var=var):
                        var = Scope({'alias':alias, 'this':this, 'arguments':arguments}, var)
                        var.registers(['node', 'alias'])
                        var.put('node', var.get('_this').get('aliases').get(var.get('alias')))
                        if (var.get('node').get('children') and (var.get('node').get('referenceCount')>Js(1.0))):
                            var.put('varDeclarations', (((Js(', alias')+var.put('aliasCount',Js(var.get('aliasCount').to_number())+Js(1)))+Js('='))+var.get('alias')), '+')
                            var.get('node').get('children').put('0', (Js('alias')+var.get('aliasCount')))
                    PyJs_anonymous_342_._set_name('anonymous')
                    var.get('_Object$keys')(var.get(u"this").get('aliases')).callprop('forEach', PyJs_anonymous_342_)
                    if var.get(u"this").get('lookupPropertyFunctionIsUsed'):
                        var.put('varDeclarations', (Js(', ')+var.get(u"this").callprop('lookupPropertyFunctionVarDeclaration')), '+')
                    var.put('params', Js([Js('container'), Js('depth0'), Js('helpers'), Js('partials'), Js('data')]))
                    if (var.get(u"this").get('useBlockParams') or var.get(u"this").get('useDepths')):
                        var.get('params').callprop('push', Js('blockParams'))
                    if var.get(u"this").get('useDepths'):
                        var.get('params').callprop('push', Js('depths'))
                    var.put('source', var.get(u"this").callprop('mergeSource', var.get('varDeclarations')))
                    if var.get('asObject'):
                        var.get('params').callprop('push', var.get('source'))
                        return var.get('Function').callprop('apply', var.get(u"this"), var.get('params'))
                    else:
                        return var.get(u"this").get('source').callprop('wrap', Js([Js('function('), var.get('params').callprop('join', Js(',')), Js(') {\n  '), var.get('source'), Js('}')]))
                PyJs_createFunctionContext_341_._set_name('createFunctionContext')
                @Js
                def PyJs_mergeSource_343_(varDeclarations, this, arguments, var=var):
                    var = Scope({'varDeclarations':varDeclarations, 'this':this, 'arguments':arguments, 'mergeSource':PyJs_mergeSource_343_}, var)
                    var.registers(['sourceSeen', 'appendFirst', 'bufferEnd', 'varDeclarations', 'bufferStart', 'isSimple', 'appendOnly'])
                    var.put('isSimple', var.get(u"this").get('environment').get('isSimple'))
                    var.put('appendOnly', var.get(u"this").get('forceBuffer').neg())
                    var.put('appendFirst', var.get('undefined'))
                    var.put('sourceSeen', var.get('undefined'))
                    var.put('bufferStart', var.get('undefined'))
                    var.put('bufferEnd', var.get('undefined'))
                    @Js
                    def PyJs_anonymous_344_(line, this, arguments, var=var):
                        var = Scope({'line':line, 'this':this, 'arguments':arguments}, var)
                        var.registers(['line'])
                        if var.get('line').get('appendToBuffer'):
                            if var.get('bufferStart'):
                                var.get('line').callprop('prepend', Js('  + '))
                            else:
                                var.put('bufferStart', var.get('line'))
                            var.put('bufferEnd', var.get('line'))
                        else:
                            if var.get('bufferStart'):
                                if var.get('sourceSeen').neg():
                                    var.put('appendFirst', Js(True))
                                else:
                                    var.get('bufferStart').callprop('prepend', Js('buffer += '))
                                var.get('bufferEnd').callprop('add', Js(';'))
                                var.put('bufferStart', var.put('bufferEnd', var.get('undefined')))
                            var.put('sourceSeen', Js(True))
                            if var.get('isSimple').neg():
                                var.put('appendOnly', Js(False))
                    PyJs_anonymous_344_._set_name('anonymous')
                    var.get(u"this").get('source').callprop('each', PyJs_anonymous_344_)
                    if var.get('appendOnly'):
                        if var.get('bufferStart'):
                            var.get('bufferStart').callprop('prepend', Js('return '))
                            var.get('bufferEnd').callprop('add', Js(';'))
                        else:
                            if var.get('sourceSeen').neg():
                                var.get(u"this").get('source').callprop('push', Js('return "";'))
                    else:
                        var.put('varDeclarations', (Js(', buffer = ')+(Js('') if var.get('appendFirst') else var.get(u"this").callprop('initializeBuffer'))), '+')
                        if var.get('bufferStart'):
                            var.get('bufferStart').callprop('prepend', Js('return buffer + '))
                            var.get('bufferEnd').callprop('add', Js(';'))
                        else:
                            var.get(u"this").get('source').callprop('push', Js('return buffer;'))
                    if var.get('varDeclarations'):
                        var.get(u"this").get('source').callprop('prepend', ((Js('var ')+var.get('varDeclarations').callprop('substring', Js(2.0)))+(Js('') if var.get('appendFirst') else Js(';\n'))))
                    return var.get(u"this").get('source').callprop('merge')
                PyJs_mergeSource_343_._set_name('mergeSource')
                @Js
                def PyJs_lookupPropertyFunctionVarDeclaration_345_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'lookupPropertyFunctionVarDeclaration':PyJs_lookupPropertyFunctionVarDeclaration_345_}, var)
                    var.registers([])
                    return Js('\n      lookupProperty = container.lookupProperty || function(parent, propertyName) {\n        if (Object.prototype.hasOwnProperty.call(parent, propertyName)) {\n          return parent[propertyName];\n        }\n        return undefined\n    }\n    ').callprop('trim')
                PyJs_lookupPropertyFunctionVarDeclaration_345_._set_name('lookupPropertyFunctionVarDeclaration')
                @Js
                def PyJs_blockValue_346_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'blockValue':PyJs_blockValue_346_}, var)
                    var.registers(['blockName', 'blockHelperMissing', 'name', 'params'])
                    var.put('blockHelperMissing', var.get(u"this").callprop('aliasable', Js('container.hooks.blockHelperMissing')))
                    var.put('params', Js([var.get(u"this").callprop('contextName', Js(0.0))]))
                    var.get(u"this").callprop('setupHelperArgs', var.get('name'), Js(0.0), var.get('params'))
                    var.put('blockName', var.get(u"this").callprop('popStack'))
                    var.get('params').callprop('splice', Js(1.0), Js(0.0), var.get('blockName'))
                    var.get(u"this").callprop('push', var.get(u"this").get('source').callprop('functionCall', var.get('blockHelperMissing'), Js('call'), var.get('params')))
                PyJs_blockValue_346_._set_name('blockValue')
                @Js
                def PyJs_ambiguousBlockValue_347_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'ambiguousBlockValue':PyJs_ambiguousBlockValue_347_}, var)
                    var.registers(['blockHelperMissing', 'current', 'params'])
                    var.put('blockHelperMissing', var.get(u"this").callprop('aliasable', Js('container.hooks.blockHelperMissing')))
                    var.put('params', Js([var.get(u"this").callprop('contextName', Js(0.0))]))
                    var.get(u"this").callprop('setupHelperArgs', Js(''), Js(0.0), var.get('params'), Js(True))
                    var.get(u"this").callprop('flushInline')
                    var.put('current', var.get(u"this").callprop('topStack'))
                    var.get('params').callprop('splice', Js(1.0), Js(0.0), var.get('current'))
                    var.get(u"this").callprop('pushSource', Js([Js('if (!'), var.get(u"this").get('lastHelper'), Js(') { '), var.get('current'), Js(' = '), var.get(u"this").get('source').callprop('functionCall', var.get('blockHelperMissing'), Js('call'), var.get('params')), Js('}')]))
                PyJs_ambiguousBlockValue_347_._set_name('ambiguousBlockValue')
                @Js
                def PyJs_appendContent_348_(content, this, arguments, var=var):
                    var = Scope({'content':content, 'this':this, 'arguments':arguments, 'appendContent':PyJs_appendContent_348_}, var)
                    var.registers(['content'])
                    if var.get(u"this").get('pendingContent'):
                        var.put('content', (var.get(u"this").get('pendingContent')+var.get('content')))
                    else:
                        var.get(u"this").put('pendingLocation', var.get(u"this").get('source').get('currentLocation'))
                    var.get(u"this").put('pendingContent', var.get('content'))
                PyJs_appendContent_348_._set_name('appendContent')
                @Js
                def PyJs_append_349_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'append':PyJs_append_349_}, var)
                    var.registers(['local'])
                    if var.get(u"this").callprop('isInline'):
                        @Js
                        def PyJs_anonymous_350_(current, this, arguments, var=var):
                            var = Scope({'current':current, 'this':this, 'arguments':arguments}, var)
                            var.registers(['current'])
                            return Js([Js(' != null ? '), var.get('current'), Js(' : ""')])
                        PyJs_anonymous_350_._set_name('anonymous')
                        var.get(u"this").callprop('replaceStack', PyJs_anonymous_350_)
                        var.get(u"this").callprop('pushSource', var.get(u"this").callprop('appendToBuffer', var.get(u"this").callprop('popStack')))
                    else:
                        var.put('local', var.get(u"this").callprop('popStack'))
                        var.get(u"this").callprop('pushSource', Js([Js('if ('), var.get('local'), Js(' != null) { '), var.get(u"this").callprop('appendToBuffer', var.get('local'), var.get('undefined'), Js(True)), Js(' }')]))
                        if var.get(u"this").get('environment').get('isSimple'):
                            var.get(u"this").callprop('pushSource', Js([Js('else { '), var.get(u"this").callprop('appendToBuffer', Js("''"), var.get('undefined'), Js(True)), Js(' }')]))
                PyJs_append_349_._set_name('append')
                @Js
                def PyJs_appendEscaped_351_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'appendEscaped':PyJs_appendEscaped_351_}, var)
                    var.registers([])
                    var.get(u"this").callprop('pushSource', var.get(u"this").callprop('appendToBuffer', Js([var.get(u"this").callprop('aliasable', Js('container.escapeExpression')), Js('('), var.get(u"this").callprop('popStack'), Js(')')])))
                PyJs_appendEscaped_351_._set_name('appendEscaped')
                @Js
                def PyJs_getContext_352_(depth, this, arguments, var=var):
                    var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'getContext':PyJs_getContext_352_}, var)
                    var.registers(['depth'])
                    var.get(u"this").put('lastContext', var.get('depth'))
                PyJs_getContext_352_._set_name('getContext')
                @Js
                def PyJs_pushContext_353_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'pushContext':PyJs_pushContext_353_}, var)
                    var.registers([])
                    var.get(u"this").callprop('pushStackLiteral', var.get(u"this").callprop('contextName', var.get(u"this").get('lastContext')))
                PyJs_pushContext_353_._set_name('pushContext')
                @Js
                def PyJs_lookupOnContext_354_(parts, falsy, strict, scoped, this, arguments, var=var):
                    var = Scope({'parts':parts, 'falsy':falsy, 'strict':strict, 'scoped':scoped, 'this':this, 'arguments':arguments, 'lookupOnContext':PyJs_lookupOnContext_354_}, var)
                    var.registers(['i', 'strict', 'scoped', 'parts', 'falsy'])
                    var.put('i', Js(0.0))
                    if ((var.get('scoped').neg() and var.get(u"this").get('options').get('compat')) and var.get(u"this").get('lastContext').neg()):
                        var.get(u"this").callprop('push', var.get(u"this").callprop('depthedLookup', var.get('parts').get((var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1)))))
                    else:
                        var.get(u"this").callprop('pushContext')
                    var.get(u"this").callprop('resolvePath', Js('context'), var.get('parts'), var.get('i'), var.get('falsy'), var.get('strict'))
                PyJs_lookupOnContext_354_._set_name('lookupOnContext')
                @Js
                def PyJs_lookupBlockParam_355_(blockParamId, parts, this, arguments, var=var):
                    var = Scope({'blockParamId':blockParamId, 'parts':parts, 'this':this, 'arguments':arguments, 'lookupBlockParam':PyJs_lookupBlockParam_355_}, var)
                    var.registers(['blockParamId', 'parts'])
                    var.get(u"this").put('useBlockParams', Js(True))
                    var.get(u"this").callprop('push', Js([Js('blockParams['), var.get('blockParamId').get('0'), Js(']['), var.get('blockParamId').get('1'), Js(']')]))
                    var.get(u"this").callprop('resolvePath', Js('context'), var.get('parts'), Js(1.0))
                PyJs_lookupBlockParam_355_._set_name('lookupBlockParam')
                @Js
                def PyJs_lookupData_356_(depth, parts, strict, this, arguments, var=var):
                    var = Scope({'depth':depth, 'parts':parts, 'strict':strict, 'this':this, 'arguments':arguments, 'lookupData':PyJs_lookupData_356_}, var)
                    var.registers(['depth', 'strict', 'parts'])
                    if var.get('depth').neg():
                        var.get(u"this").callprop('pushStackLiteral', Js('data'))
                    else:
                        var.get(u"this").callprop('pushStackLiteral', ((Js('container.data(data, ')+var.get('depth'))+Js(')')))
                    var.get(u"this").callprop('resolvePath', Js('data'), var.get('parts'), Js(0.0), Js(True), var.get('strict'))
                PyJs_lookupData_356_._set_name('lookupData')
                @Js
                def PyJs_resolvePath_357_(type, parts, i, falsy, strict, this, arguments, var=var):
                    var = Scope({'type':type, 'parts':parts, 'i':i, 'falsy':falsy, 'strict':strict, 'this':this, 'arguments':arguments, 'resolvePath':PyJs_resolvePath_357_}, var)
                    var.registers(['i', 'len', 'strict', 'type', '_this2', 'parts', 'falsy'])
                    var.put('_this2', var.get(u"this"))
                    if (var.get(u"this").get('options').get('strict') or var.get(u"this").get('options').get('assumeObjects')):
                        var.get(u"this").callprop('push', var.get('strictLookup')((var.get(u"this").get('options').get('strict') and var.get('strict')), var.get(u"this"), var.get('parts'), var.get('i'), var.get('type')))
                        return var.get('undefined')
                    var.put('len', var.get('parts').get('length'))
                    #for JS loop
                    
                    while (var.get('i')<var.get('len')):
                        @Js
                        def PyJs_anonymous_358_(current, this, arguments, var=var):
                            var = Scope({'current':current, 'this':this, 'arguments':arguments}, var)
                            var.registers(['lookup', 'current'])
                            var.put('lookup', var.get('_this2').callprop('nameLookup', var.get('current'), var.get('parts').get(var.get('i')), var.get('type')))
                            if var.get('falsy').neg():
                                return Js([Js(' != null ? '), var.get('lookup'), Js(' : '), var.get('current')])
                            else:
                                return Js([Js(' && '), var.get('lookup')])
                        PyJs_anonymous_358_._set_name('anonymous')
                        var.get(u"this").callprop('replaceStack', PyJs_anonymous_358_)
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_resolvePath_357_._set_name('resolvePath')
                @Js
                def PyJs_resolvePossibleLambda_359_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'resolvePossibleLambda':PyJs_resolvePossibleLambda_359_}, var)
                    var.registers([])
                    var.get(u"this").callprop('push', Js([var.get(u"this").callprop('aliasable', Js('container.lambda')), Js('('), var.get(u"this").callprop('popStack'), Js(', '), var.get(u"this").callprop('contextName', Js(0.0)), Js(')')]))
                PyJs_resolvePossibleLambda_359_._set_name('resolvePossibleLambda')
                @Js
                def PyJs_pushStringParam_360_(string, type, this, arguments, var=var):
                    var = Scope({'string':string, 'type':type, 'this':this, 'arguments':arguments, 'pushStringParam':PyJs_pushStringParam_360_}, var)
                    var.registers(['string', 'type'])
                    var.get(u"this").callprop('pushContext')
                    var.get(u"this").callprop('pushString', var.get('type'))
                    if PyJsStrictNeq(var.get('type'),Js('SubExpression')):
                        if PyJsStrictEq(var.get('string',throw=False).typeof(),Js('string')):
                            var.get(u"this").callprop('pushString', var.get('string'))
                        else:
                            var.get(u"this").callprop('pushStackLiteral', var.get('string'))
                PyJs_pushStringParam_360_._set_name('pushStringParam')
                @Js
                def PyJs_emptyHash_361_(omitEmpty, this, arguments, var=var):
                    var = Scope({'omitEmpty':omitEmpty, 'this':this, 'arguments':arguments, 'emptyHash':PyJs_emptyHash_361_}, var)
                    var.registers(['omitEmpty'])
                    if var.get(u"this").get('trackIds'):
                        var.get(u"this").callprop('push', Js('{}'))
                    if var.get(u"this").get('stringParams'):
                        var.get(u"this").callprop('push', Js('{}'))
                        var.get(u"this").callprop('push', Js('{}'))
                    var.get(u"this").callprop('pushStackLiteral', (Js('undefined') if var.get('omitEmpty') else Js('{}')))
                PyJs_emptyHash_361_._set_name('emptyHash')
                @Js
                def PyJs_pushHash_362_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'pushHash':PyJs_pushHash_362_}, var)
                    var.registers([])
                    if var.get(u"this").get('hash'):
                        var.get(u"this").get('hashes').callprop('push', var.get(u"this").get('hash'))
                    var.get(u"this").put('hash', Js({'values':Js({}),'types':Js([]),'contexts':Js([]),'ids':Js([])}))
                PyJs_pushHash_362_._set_name('pushHash')
                @Js
                def PyJs_popHash_363_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'popHash':PyJs_popHash_363_}, var)
                    var.registers(['hash'])
                    var.put('hash', var.get(u"this").get('hash'))
                    var.get(u"this").put('hash', var.get(u"this").get('hashes').callprop('pop'))
                    if var.get(u"this").get('trackIds'):
                        var.get(u"this").callprop('push', var.get(u"this").callprop('objectLiteral', var.get('hash').get('ids')))
                    if var.get(u"this").get('stringParams'):
                        var.get(u"this").callprop('push', var.get(u"this").callprop('objectLiteral', var.get('hash').get('contexts')))
                        var.get(u"this").callprop('push', var.get(u"this").callprop('objectLiteral', var.get('hash').get('types')))
                    var.get(u"this").callprop('push', var.get(u"this").callprop('objectLiteral', var.get('hash').get('values')))
                PyJs_popHash_363_._set_name('popHash')
                @Js
                def PyJs_pushString_364_(string, this, arguments, var=var):
                    var = Scope({'string':string, 'this':this, 'arguments':arguments, 'pushString':PyJs_pushString_364_}, var)
                    var.registers(['string'])
                    var.get(u"this").callprop('pushStackLiteral', var.get(u"this").callprop('quotedString', var.get('string')))
                PyJs_pushString_364_._set_name('pushString')
                @Js
                def PyJs_pushLiteral_365_(value, this, arguments, var=var):
                    var = Scope({'value':value, 'this':this, 'arguments':arguments, 'pushLiteral':PyJs_pushLiteral_365_}, var)
                    var.registers(['value'])
                    var.get(u"this").callprop('pushStackLiteral', var.get('value'))
                PyJs_pushLiteral_365_._set_name('pushLiteral')
                @Js
                def PyJs_pushProgram_366_(guid, this, arguments, var=var):
                    var = Scope({'guid':guid, 'this':this, 'arguments':arguments, 'pushProgram':PyJs_pushProgram_366_}, var)
                    var.registers(['guid'])
                    if (var.get('guid')!=var.get(u"null")):
                        var.get(u"this").callprop('pushStackLiteral', var.get(u"this").callprop('programExpression', var.get('guid')))
                    else:
                        var.get(u"this").callprop('pushStackLiteral', var.get(u"null"))
                PyJs_pushProgram_366_._set_name('pushProgram')
                @Js
                def PyJs_registerDecorator_367_(paramSize, name, this, arguments, var=var):
                    var = Scope({'paramSize':paramSize, 'name':name, 'this':this, 'arguments':arguments, 'registerDecorator':PyJs_registerDecorator_367_}, var)
                    var.registers(['options', 'paramSize', 'name', 'foundDecorator'])
                    var.put('foundDecorator', var.get(u"this").callprop('nameLookup', Js('decorators'), var.get('name'), Js('decorator')))
                    var.put('options', var.get(u"this").callprop('setupHelperArgs', var.get('name'), var.get('paramSize')))
                    var.get(u"this").get('decorators').callprop('push', Js([Js('fn = '), var.get(u"this").get('decorators').callprop('functionCall', var.get('foundDecorator'), Js(''), Js([Js('fn'), Js('props'), Js('container'), var.get('options')])), Js(' || fn;')]))
                PyJs_registerDecorator_367_._set_name('registerDecorator')
                @Js
                def PyJs_invokeHelper_368_(paramSize, name, isSimple, this, arguments, var=var):
                    var = Scope({'paramSize':paramSize, 'name':name, 'isSimple':isSimple, 'this':this, 'arguments':arguments, 'invokeHelper':PyJs_invokeHelper_368_}, var)
                    var.registers(['paramSize', 'functionCall', 'helper', 'name', 'possibleFunctionCalls', 'functionLookupCode', 'isSimple', 'nonHelper'])
                    var.put('nonHelper', var.get(u"this").callprop('popStack'))
                    var.put('helper', var.get(u"this").callprop('setupHelper', var.get('paramSize'), var.get('name')))
                    var.put('possibleFunctionCalls', Js([]))
                    if var.get('isSimple'):
                        var.get('possibleFunctionCalls').callprop('push', var.get('helper').get('name'))
                    var.get('possibleFunctionCalls').callprop('push', var.get('nonHelper'))
                    if var.get(u"this").get('options').get('strict').neg():
                        var.get('possibleFunctionCalls').callprop('push', var.get(u"this").callprop('aliasable', Js('container.hooks.helperMissing')))
                    var.put('functionLookupCode', Js([Js('('), var.get(u"this").callprop('itemsSeparatedBy', var.get('possibleFunctionCalls'), Js('||')), Js(')')]))
                    var.put('functionCall', var.get(u"this").get('source').callprop('functionCall', var.get('functionLookupCode'), Js('call'), var.get('helper').get('callParams')))
                    var.get(u"this").callprop('push', var.get('functionCall'))
                PyJs_invokeHelper_368_._set_name('invokeHelper')
                @Js
                def PyJs_itemsSeparatedBy_369_(items, separator, this, arguments, var=var):
                    var = Scope({'items':items, 'separator':separator, 'this':this, 'arguments':arguments, 'itemsSeparatedBy':PyJs_itemsSeparatedBy_369_}, var)
                    var.registers(['result', 'items', 'separator', 'i'])
                    var.put('result', Js([]))
                    var.get('result').callprop('push', var.get('items').get('0'))
                    #for JS loop
                    var.put('i', Js(1.0))
                    while (var.get('i')<var.get('items').get('length')):
                        var.get('result').callprop('push', var.get('separator'), var.get('items').get(var.get('i')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    return var.get('result')
                PyJs_itemsSeparatedBy_369_._set_name('itemsSeparatedBy')
                @Js
                def PyJs_invokeKnownHelper_370_(paramSize, name, this, arguments, var=var):
                    var = Scope({'paramSize':paramSize, 'name':name, 'this':this, 'arguments':arguments, 'invokeKnownHelper':PyJs_invokeKnownHelper_370_}, var)
                    var.registers(['helper', 'paramSize', 'name'])
                    var.put('helper', var.get(u"this").callprop('setupHelper', var.get('paramSize'), var.get('name')))
                    var.get(u"this").callprop('push', var.get(u"this").get('source').callprop('functionCall', var.get('helper').get('name'), Js('call'), var.get('helper').get('callParams')))
                PyJs_invokeKnownHelper_370_._set_name('invokeKnownHelper')
                @Js
                def PyJs_invokeAmbiguous_371_(name, helperCall, this, arguments, var=var):
                    var = Scope({'name':name, 'helperCall':helperCall, 'this':this, 'arguments':arguments, 'invokeAmbiguous':PyJs_invokeAmbiguous_371_}, var)
                    var.registers(['helperCall', 'helper', 'name', 'helperName', 'lookup', 'nonHelper'])
                    var.get(u"this").callprop('useRegister', Js('helper'))
                    var.put('nonHelper', var.get(u"this").callprop('popStack'))
                    var.get(u"this").callprop('emptyHash')
                    var.put('helper', var.get(u"this").callprop('setupHelper', Js(0.0), var.get('name'), var.get('helperCall')))
                    var.put('helperName', var.get(u"this").put('lastHelper', var.get(u"this").callprop('nameLookup', Js('helpers'), var.get('name'), Js('helper'))))
                    var.put('lookup', Js([Js('('), Js('(helper = '), var.get('helperName'), Js(' || '), var.get('nonHelper'), Js(')')]))
                    if var.get(u"this").get('options').get('strict').neg():
                        var.get('lookup').put('0', Js('(helper = '))
                        var.get('lookup').callprop('push', Js(' != null ? helper : '), var.get(u"this").callprop('aliasable', Js('container.hooks.helperMissing')))
                    def PyJs_LONG_372_(var=var):
                        return var.get(u"this").callprop('push', Js([Js('('), var.get('lookup'), (Js([Js('),('), var.get('helper').get('paramsInit')]) if var.get('helper').get('paramsInit') else Js([])), Js('),'), Js('(typeof helper === '), var.get(u"this").callprop('aliasable', Js('"function"')), Js(' ? '), var.get(u"this").get('source').callprop('functionCall', Js('helper'), Js('call'), var.get('helper').get('callParams')), Js(' : helper))')]))
                    PyJs_LONG_372_()
                PyJs_invokeAmbiguous_371_._set_name('invokeAmbiguous')
                @Js
                def PyJs_invokePartial_373_(isDynamic, name, indent, this, arguments, var=var):
                    var = Scope({'isDynamic':isDynamic, 'name':name, 'indent':indent, 'this':this, 'arguments':arguments, 'invokePartial':PyJs_invokePartial_373_}, var)
                    var.registers(['indent', 'params', 'isDynamic', 'name', 'options'])
                    var.put('params', Js([]))
                    var.put('options', var.get(u"this").callprop('setupParams', var.get('name'), Js(1.0), var.get('params')))
                    if var.get('isDynamic'):
                        var.put('name', var.get(u"this").callprop('popStack'))
                        var.get('options').delete('name')
                    if var.get('indent'):
                        var.get('options').put('indent', var.get('JSON').callprop('stringify', var.get('indent')))
                    var.get('options').put('helpers', Js('helpers'))
                    var.get('options').put('partials', Js('partials'))
                    var.get('options').put('decorators', Js('container.decorators'))
                    if var.get('isDynamic').neg():
                        var.get('params').callprop('unshift', var.get(u"this").callprop('nameLookup', Js('partials'), var.get('name'), Js('partial')))
                    else:
                        var.get('params').callprop('unshift', var.get('name'))
                    if var.get(u"this").get('options').get('compat'):
                        var.get('options').put('depths', Js('depths'))
                    var.put('options', var.get(u"this").callprop('objectLiteral', var.get('options')))
                    var.get('params').callprop('push', var.get('options'))
                    var.get(u"this").callprop('push', var.get(u"this").get('source').callprop('functionCall', Js('container.invokePartial'), Js(''), var.get('params')))
                PyJs_invokePartial_373_._set_name('invokePartial')
                @Js
                def PyJs_assignToHash_374_(key, this, arguments, var=var):
                    var = Scope({'key':key, 'this':this, 'arguments':arguments, 'assignToHash':PyJs_assignToHash_374_}, var)
                    var.registers(['context', 'key', 'type', 'hash', 'value', 'id'])
                    var.put('value', var.get(u"this").callprop('popStack'))
                    var.put('context', var.get('undefined'))
                    var.put('type', var.get('undefined'))
                    var.put('id', var.get('undefined'))
                    if var.get(u"this").get('trackIds'):
                        var.put('id', var.get(u"this").callprop('popStack'))
                    if var.get(u"this").get('stringParams'):
                        var.put('type', var.get(u"this").callprop('popStack'))
                        var.put('context', var.get(u"this").callprop('popStack'))
                    var.put('hash', var.get(u"this").get('hash'))
                    if var.get('context'):
                        var.get('hash').get('contexts').put(var.get('key'), var.get('context'))
                    if var.get('type'):
                        var.get('hash').get('types').put(var.get('key'), var.get('type'))
                    if var.get('id'):
                        var.get('hash').get('ids').put(var.get('key'), var.get('id'))
                    var.get('hash').get('values').put(var.get('key'), var.get('value'))
                PyJs_assignToHash_374_._set_name('assignToHash')
                @Js
                def PyJs_pushId_375_(type, name, child, this, arguments, var=var):
                    var = Scope({'type':type, 'name':name, 'child':child, 'this':this, 'arguments':arguments, 'pushId':PyJs_pushId_375_}, var)
                    var.registers(['child', 'type', 'name'])
                    if PyJsStrictEq(var.get('type'),Js('BlockParam')):
                        var.get(u"this").callprop('pushStackLiteral', (((((Js('blockParams[')+var.get('name').get('0'))+Js('].path['))+var.get('name').get('1'))+Js(']'))+((Js(' + ')+var.get('JSON').callprop('stringify', (Js('.')+var.get('child')))) if var.get('child') else Js(''))))
                    else:
                        if PyJsStrictEq(var.get('type'),Js('PathExpression')):
                            var.get(u"this").callprop('pushString', var.get('name'))
                        else:
                            if PyJsStrictEq(var.get('type'),Js('SubExpression')):
                                var.get(u"this").callprop('pushStackLiteral', Js('true'))
                            else:
                                var.get(u"this").callprop('pushStackLiteral', Js('null'))
                PyJs_pushId_375_._set_name('pushId')
                @Js
                def PyJs_compileChildren_376_(environment, options, this, arguments, var=var):
                    var = Scope({'environment':environment, 'options':options, 'this':this, 'arguments':arguments, 'compileChildren':PyJs_compileChildren_376_}, var)
                    var.registers(['children', 'l', 'i', 'child', 'existing', 'index', 'environment', 'compiler', 'options'])
                    var.put('children', var.get('environment').get('children'))
                    var.put('child', var.get('undefined'))
                    var.put('compiler', var.get('undefined'))
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('l', var.get('children').get('length'))
                    while (var.get('i')<var.get('l')):
                        var.put('child', var.get('children').get(var.get('i')))
                        var.put('compiler', var.get(u"this").get('compiler').create())
                        var.put('existing', var.get(u"this").callprop('matchExistingProgram', var.get('child')))
                        if (var.get('existing')==var.get(u"null")):
                            var.get(u"this").get('context').get('programs').callprop('push', Js(''))
                            var.put('index', var.get(u"this").get('context').get('programs').get('length'))
                            var.get('child').put('index', var.get('index'))
                            var.get('child').put('name', (Js('program')+var.get('index')))
                            var.get(u"this").get('context').get('programs').put(var.get('index'), var.get('compiler').callprop('compile', var.get('child'), var.get('options'), var.get(u"this").get('context'), var.get(u"this").get('precompile').neg()))
                            var.get(u"this").get('context').get('decorators').put(var.get('index'), var.get('compiler').get('decorators'))
                            var.get(u"this").get('context').get('environments').put(var.get('index'), var.get('child'))
                            var.get(u"this").put('useDepths', (var.get(u"this").get('useDepths') or var.get('compiler').get('useDepths')))
                            var.get(u"this").put('useBlockParams', (var.get(u"this").get('useBlockParams') or var.get('compiler').get('useBlockParams')))
                            var.get('child').put('useDepths', var.get(u"this").get('useDepths'))
                            var.get('child').put('useBlockParams', var.get(u"this").get('useBlockParams'))
                        else:
                            var.get('child').put('index', var.get('existing').get('index'))
                            var.get('child').put('name', (Js('program')+var.get('existing').get('index')))
                            var.get(u"this").put('useDepths', (var.get(u"this").get('useDepths') or var.get('existing').get('useDepths')))
                            var.get(u"this").put('useBlockParams', (var.get(u"this").get('useBlockParams') or var.get('existing').get('useBlockParams')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_compileChildren_376_._set_name('compileChildren')
                @Js
                def PyJs_matchExistingProgram_377_(child, this, arguments, var=var):
                    var = Scope({'child':child, 'this':this, 'arguments':arguments, 'matchExistingProgram':PyJs_matchExistingProgram_377_}, var)
                    var.registers(['len', 'child', 'environment', 'i'])
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('len', var.get(u"this").get('context').get('environments').get('length'))
                    while (var.get('i')<var.get('len')):
                        var.put('environment', var.get(u"this").get('context').get('environments').get(var.get('i')))
                        if (var.get('environment') and var.get('environment').callprop('equals', var.get('child'))):
                            return var.get('environment')
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_matchExistingProgram_377_._set_name('matchExistingProgram')
                @Js
                def PyJs_programExpression_378_(guid, this, arguments, var=var):
                    var = Scope({'guid':guid, 'this':this, 'arguments':arguments, 'programExpression':PyJs_programExpression_378_}, var)
                    var.registers(['child', 'guid', 'programParams'])
                    var.put('child', var.get(u"this").get('environment').get('children').get(var.get('guid')))
                    var.put('programParams', Js([var.get('child').get('index'), Js('data'), var.get('child').get('blockParams')]))
                    if (var.get(u"this").get('useBlockParams') or var.get(u"this").get('useDepths')):
                        var.get('programParams').callprop('push', Js('blockParams'))
                    if var.get(u"this").get('useDepths'):
                        var.get('programParams').callprop('push', Js('depths'))
                    return ((Js('container.program(')+var.get('programParams').callprop('join', Js(', ')))+Js(')'))
                PyJs_programExpression_378_._set_name('programExpression')
                @Js
                def PyJs_useRegister_379_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'useRegister':PyJs_useRegister_379_}, var)
                    var.registers(['name'])
                    if var.get(u"this").get('registers').get(var.get('name')).neg():
                        var.get(u"this").get('registers').put(var.get('name'), Js(True))
                        var.get(u"this").get('registers').get('list').callprop('push', var.get('name'))
                PyJs_useRegister_379_._set_name('useRegister')
                @Js
                def PyJs_push_380_(expr, this, arguments, var=var):
                    var = Scope({'expr':expr, 'this':this, 'arguments':arguments, 'push':PyJs_push_380_}, var)
                    var.registers(['expr'])
                    if var.get('expr').instanceof(var.get('Literal')).neg():
                        var.put('expr', var.get(u"this").get('source').callprop('wrap', var.get('expr')))
                    var.get(u"this").get('inlineStack').callprop('push', var.get('expr'))
                    return var.get('expr')
                PyJs_push_380_._set_name('push')
                @Js
                def PyJs_pushStackLiteral_381_(item, this, arguments, var=var):
                    var = Scope({'item':item, 'this':this, 'arguments':arguments, 'pushStackLiteral':PyJs_pushStackLiteral_381_}, var)
                    var.registers(['item'])
                    var.get(u"this").callprop('push', var.get('Literal').create(var.get('item')))
                PyJs_pushStackLiteral_381_._set_name('pushStackLiteral')
                @Js
                def PyJs_pushSource_382_(source, this, arguments, var=var):
                    var = Scope({'source':source, 'this':this, 'arguments':arguments, 'pushSource':PyJs_pushSource_382_}, var)
                    var.registers(['source'])
                    if var.get(u"this").get('pendingContent'):
                        var.get(u"this").get('source').callprop('push', var.get(u"this").callprop('appendToBuffer', var.get(u"this").get('source').callprop('quotedString', var.get(u"this").get('pendingContent')), var.get(u"this").get('pendingLocation')))
                        var.get(u"this").put('pendingContent', var.get('undefined'))
                    if var.get('source'):
                        var.get(u"this").get('source').callprop('push', var.get('source'))
                PyJs_pushSource_382_._set_name('pushSource')
                @Js
                def PyJs_replaceStack_383_(callback, this, arguments, var=var):
                    var = Scope({'callback':callback, 'this':this, 'arguments':arguments, 'replaceStack':PyJs_replaceStack_383_}, var)
                    var.registers(['stack', 'usedLiteral', 'callback', 'prefix', 'top', '_name', 'item', 'createdStack'])
                    var.put('prefix', Js([Js('(')]))
                    var.put('stack', var.get('undefined'))
                    var.put('createdStack', var.get('undefined'))
                    var.put('usedLiteral', var.get('undefined'))
                    if var.get(u"this").callprop('isInline').neg():
                        PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('replaceStack on non-inline')))
                        raise PyJsTempException
                    var.put('top', var.get(u"this").callprop('popStack', Js(True)))
                    if var.get('top').instanceof(var.get('Literal')):
                        var.put('stack', Js([var.get('top').get('value')]))
                        var.put('prefix', Js([Js('('), var.get('stack')]))
                        var.put('usedLiteral', Js(True))
                    else:
                        var.put('createdStack', Js(True))
                        var.put('_name', var.get(u"this").callprop('incrStack'))
                        var.put('prefix', Js([Js('(('), var.get(u"this").callprop('push', var.get('_name')), Js(' = '), var.get('top'), Js(')')]))
                        var.put('stack', var.get(u"this").callprop('topStack'))
                    var.put('item', var.get('callback').callprop('call', var.get(u"this"), var.get('stack')))
                    if var.get('usedLiteral').neg():
                        var.get(u"this").callprop('popStack')
                    if var.get('createdStack'):
                        (var.get(u"this").put('stackSlot',Js(var.get(u"this").get('stackSlot').to_number())-Js(1))+Js(1))
                    var.get(u"this").callprop('push', var.get('prefix').callprop('concat', var.get('item'), Js(')')))
                PyJs_replaceStack_383_._set_name('replaceStack')
                @Js
                def PyJs_incrStack_384_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'incrStack':PyJs_incrStack_384_}, var)
                    var.registers([])
                    (var.get(u"this").put('stackSlot',Js(var.get(u"this").get('stackSlot').to_number())+Js(1))-Js(1))
                    if (var.get(u"this").get('stackSlot')>var.get(u"this").get('stackVars').get('length')):
                        var.get(u"this").get('stackVars').callprop('push', (Js('stack')+var.get(u"this").get('stackSlot')))
                    return var.get(u"this").callprop('topStackName')
                PyJs_incrStack_384_._set_name('incrStack')
                @Js
                def PyJs_topStackName_385_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'topStackName':PyJs_topStackName_385_}, var)
                    var.registers([])
                    return (Js('stack')+var.get(u"this").get('stackSlot'))
                PyJs_topStackName_385_._set_name('topStackName')
                @Js
                def PyJs_flushInline_386_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'flushInline':PyJs_flushInline_386_}, var)
                    var.registers(['stack', 'i', 'len', 'entry', 'inlineStack'])
                    var.put('inlineStack', var.get(u"this").get('inlineStack'))
                    var.get(u"this").put('inlineStack', Js([]))
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('len', var.get('inlineStack').get('length'))
                    while (var.get('i')<var.get('len')):
                        var.put('entry', var.get('inlineStack').get(var.get('i')))
                        if var.get('entry').instanceof(var.get('Literal')):
                            var.get(u"this").get('compileStack').callprop('push', var.get('entry'))
                        else:
                            var.put('stack', var.get(u"this").callprop('incrStack'))
                            var.get(u"this").callprop('pushSource', Js([var.get('stack'), Js(' = '), var.get('entry'), Js(';')]))
                            var.get(u"this").get('compileStack').callprop('push', var.get('stack'))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_flushInline_386_._set_name('flushInline')
                @Js
                def PyJs_isInline_387_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'isInline':PyJs_isInline_387_}, var)
                    var.registers([])
                    return var.get(u"this").get('inlineStack').get('length')
                PyJs_isInline_387_._set_name('isInline')
                @Js
                def PyJs_popStack_388_(wrapped, this, arguments, var=var):
                    var = Scope({'wrapped':wrapped, 'this':this, 'arguments':arguments, 'popStack':PyJs_popStack_388_}, var)
                    var.registers(['wrapped', 'item', 'inline'])
                    var.put('inline', var.get(u"this").callprop('isInline'))
                    var.put('item', (var.get(u"this").get('inlineStack') if var.get('inline') else var.get(u"this").get('compileStack')).callprop('pop'))
                    if (var.get('wrapped').neg() and var.get('item').instanceof(var.get('Literal'))):
                        return var.get('item').get('value')
                    else:
                        if var.get('inline').neg():
                            if var.get(u"this").get('stackSlot').neg():
                                PyJsTempException = JsToPyException(var.get('_exception2').get('default').create(Js('Invalid stack pop')))
                                raise PyJsTempException
                            (var.get(u"this").put('stackSlot',Js(var.get(u"this").get('stackSlot').to_number())-Js(1))+Js(1))
                        return var.get('item')
                PyJs_popStack_388_._set_name('popStack')
                @Js
                def PyJs_topStack_389_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'topStack':PyJs_topStack_389_}, var)
                    var.registers(['stack', 'item'])
                    var.put('stack', (var.get(u"this").get('inlineStack') if var.get(u"this").callprop('isInline') else var.get(u"this").get('compileStack')))
                    var.put('item', var.get('stack').get((var.get('stack').get('length')-Js(1.0))))
                    if var.get('item').instanceof(var.get('Literal')):
                        return var.get('item').get('value')
                    else:
                        return var.get('item')
                PyJs_topStack_389_._set_name('topStack')
                @Js
                def PyJs_contextName_390_(context, this, arguments, var=var):
                    var = Scope({'context':context, 'this':this, 'arguments':arguments, 'contextName':PyJs_contextName_390_}, var)
                    var.registers(['context'])
                    if (var.get(u"this").get('useDepths') and var.get('context')):
                        return ((Js('depths[')+var.get('context'))+Js(']'))
                    else:
                        return (Js('depth')+var.get('context'))
                PyJs_contextName_390_._set_name('contextName')
                @Js
                def PyJs_quotedString_391_(str, this, arguments, var=var):
                    var = Scope({'str':str, 'this':this, 'arguments':arguments, 'quotedString':PyJs_quotedString_391_}, var)
                    var.registers(['str'])
                    return var.get(u"this").get('source').callprop('quotedString', var.get('str'))
                PyJs_quotedString_391_._set_name('quotedString')
                @Js
                def PyJs_objectLiteral_392_(obj, this, arguments, var=var):
                    var = Scope({'obj':obj, 'this':this, 'arguments':arguments, 'objectLiteral':PyJs_objectLiteral_392_}, var)
                    var.registers(['obj'])
                    return var.get(u"this").get('source').callprop('objectLiteral', var.get('obj'))
                PyJs_objectLiteral_392_._set_name('objectLiteral')
                @Js
                def PyJs_aliasable_393_(name, this, arguments, var=var):
                    var = Scope({'name':name, 'this':this, 'arguments':arguments, 'aliasable':PyJs_aliasable_393_}, var)
                    var.registers(['ret', 'name'])
                    var.put('ret', var.get(u"this").get('aliases').get(var.get('name')))
                    if var.get('ret'):
                        (var.get('ret').put('referenceCount',Js(var.get('ret').get('referenceCount').to_number())+Js(1))-Js(1))
                        return var.get('ret')
                    var.put('ret', var.get(u"this").get('aliases').put(var.get('name'), var.get(u"this").get('source').callprop('wrap', var.get('name'))))
                    var.get('ret').put('aliasable', Js(True))
                    var.get('ret').put('referenceCount', Js(1.0))
                    return var.get('ret')
                PyJs_aliasable_393_._set_name('aliasable')
                @Js
                def PyJs_setupHelper_394_(paramSize, name, blockHelper, this, arguments, var=var):
                    var = Scope({'paramSize':paramSize, 'name':name, 'blockHelper':blockHelper, 'this':this, 'arguments':arguments, 'setupHelper':PyJs_setupHelper_394_}, var)
                    var.registers(['paramSize', 'params', 'name', 'callContext', 'blockHelper', 'paramsInit', 'foundHelper'])
                    var.put('params', Js([]))
                    var.put('paramsInit', var.get(u"this").callprop('setupHelperArgs', var.get('name'), var.get('paramSize'), var.get('params'), var.get('blockHelper')))
                    var.put('foundHelper', var.get(u"this").callprop('nameLookup', Js('helpers'), var.get('name'), Js('helper')))
                    var.put('callContext', var.get(u"this").callprop('aliasable', (((var.get(u"this").callprop('contextName', Js(0.0))+Js(' != null ? '))+var.get(u"this").callprop('contextName', Js(0.0)))+Js(' : (container.nullContext || {})'))))
                    return Js({'params':var.get('params'),'paramsInit':var.get('paramsInit'),'name':var.get('foundHelper'),'callParams':Js([var.get('callContext')]).callprop('concat', var.get('params'))})
                PyJs_setupHelper_394_._set_name('setupHelper')
                @Js
                def PyJs_setupParams_395_(helper, paramSize, params, this, arguments, var=var):
                    var = Scope({'helper':helper, 'paramSize':paramSize, 'params':params, 'this':this, 'arguments':arguments, 'setupParams':PyJs_setupParams_395_}, var)
                    var.registers(['param', 'program', 'paramSize', 'i', 'params', 'ids', 'helper', 'contexts', 'inverse', 'types', 'objectArgs', 'options'])
                    var.put('options', Js({}))
                    var.put('contexts', Js([]))
                    var.put('types', Js([]))
                    var.put('ids', Js([]))
                    var.put('objectArgs', var.get('params').neg())
                    var.put('param', var.get('undefined'))
                    if var.get('objectArgs'):
                        var.put('params', Js([]))
                    var.get('options').put('name', var.get(u"this").callprop('quotedString', var.get('helper')))
                    var.get('options').put('hash', var.get(u"this").callprop('popStack'))
                    if var.get(u"this").get('trackIds'):
                        var.get('options').put('hashIds', var.get(u"this").callprop('popStack'))
                    if var.get(u"this").get('stringParams'):
                        var.get('options').put('hashTypes', var.get(u"this").callprop('popStack'))
                        var.get('options').put('hashContexts', var.get(u"this").callprop('popStack'))
                    var.put('inverse', var.get(u"this").callprop('popStack'))
                    var.put('program', var.get(u"this").callprop('popStack'))
                    if (var.get('program') or var.get('inverse')):
                        var.get('options').put('fn', (var.get('program') or Js('container.noop')))
                        var.get('options').put('inverse', (var.get('inverse') or Js('container.noop')))
                    var.put('i', var.get('paramSize'))
                    while (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1)):
                        var.put('param', var.get(u"this").callprop('popStack'))
                        var.get('params').put(var.get('i'), var.get('param'))
                        if var.get(u"this").get('trackIds'):
                            var.get('ids').put(var.get('i'), var.get(u"this").callprop('popStack'))
                        if var.get(u"this").get('stringParams'):
                            var.get('types').put(var.get('i'), var.get(u"this").callprop('popStack'))
                            var.get('contexts').put(var.get('i'), var.get(u"this").callprop('popStack'))
                    if var.get('objectArgs'):
                        var.get('options').put('args', var.get(u"this").get('source').callprop('generateArray', var.get('params')))
                    if var.get(u"this").get('trackIds'):
                        var.get('options').put('ids', var.get(u"this").get('source').callprop('generateArray', var.get('ids')))
                    if var.get(u"this").get('stringParams'):
                        var.get('options').put('types', var.get(u"this").get('source').callprop('generateArray', var.get('types')))
                        var.get('options').put('contexts', var.get(u"this").get('source').callprop('generateArray', var.get('contexts')))
                    if var.get(u"this").get('options').get('data'):
                        var.get('options').put('data', Js('data'))
                    if var.get(u"this").get('useBlockParams'):
                        var.get('options').put('blockParams', Js('blockParams'))
                    return var.get('options')
                PyJs_setupParams_395_._set_name('setupParams')
                @Js
                def PyJs_setupHelperArgs_396_(helper, paramSize, params, useRegister, this, arguments, var=var):
                    var = Scope({'helper':helper, 'paramSize':paramSize, 'params':params, 'useRegister':useRegister, 'this':this, 'arguments':arguments, 'setupHelperArgs':PyJs_setupHelperArgs_396_}, var)
                    var.registers(['paramSize', 'params', 'helper', 'useRegister', 'options'])
                    var.put('options', var.get(u"this").callprop('setupParams', var.get('helper'), var.get('paramSize'), var.get('params')))
                    var.get('options').put('loc', var.get('JSON').callprop('stringify', var.get(u"this").get('source').get('currentLocation')))
                    var.put('options', var.get(u"this").callprop('objectLiteral', var.get('options')))
                    if var.get('useRegister'):
                        var.get(u"this").callprop('useRegister', Js('options'))
                        var.get('params').callprop('push', Js('options'))
                        return Js([Js('options='), var.get('options')])
                    else:
                        if var.get('params'):
                            var.get('params').callprop('push', var.get('options'))
                            return Js('')
                        else:
                            return var.get('options')
                PyJs_setupHelperArgs_396_._set_name('setupHelperArgs')
                return var.get('JavaScriptCompiler').put('prototype', Js({'nameLookup':PyJs_nameLookup_333_,'depthedLookup':PyJs_depthedLookup_334_,'compilerInfo':PyJs_compilerInfo_335_,'appendToBuffer':PyJs_appendToBuffer_336_,'initializeBuffer':PyJs_initializeBuffer_337_,'internalNameLookup':PyJs_internalNameLookup_338_,'lookupPropertyFunctionIsUsed':Js(False),'compile':PyJs_compile_339_,'preamble':PyJs_preamble_340_,'createFunctionContext':PyJs_createFunctionContext_341_,'mergeSource':PyJs_mergeSource_343_,'lookupPropertyFunctionVarDeclaration':PyJs_lookupPropertyFunctionVarDeclaration_345_,'blockValue':PyJs_blockValue_346_,'ambiguousBlockValue':PyJs_ambiguousBlockValue_347_,'appendContent':PyJs_appendContent_348_,'append':PyJs_append_349_,'appendEscaped':PyJs_appendEscaped_351_,'getContext':PyJs_getContext_352_,'pushContext':PyJs_pushContext_353_,'lookupOnContext':PyJs_lookupOnContext_354_,'lookupBlockParam':PyJs_lookupBlockParam_355_,'lookupData':PyJs_lookupData_356_,'resolvePath':PyJs_resolvePath_357_,'resolvePossibleLambda':PyJs_resolvePossibleLambda_359_,'pushStringParam':PyJs_pushStringParam_360_,'emptyHash':PyJs_emptyHash_361_,'pushHash':PyJs_pushHash_362_,'popHash':PyJs_popHash_363_,'pushString':PyJs_pushString_364_,'pushLiteral':PyJs_pushLiteral_365_,'pushProgram':PyJs_pushProgram_366_,'registerDecorator':PyJs_registerDecorator_367_,'invokeHelper':PyJs_invokeHelper_368_,'itemsSeparatedBy':PyJs_itemsSeparatedBy_369_,'invokeKnownHelper':PyJs_invokeKnownHelper_370_,'invokeAmbiguous':PyJs_invokeAmbiguous_371_,'invokePartial':PyJs_invokePartial_373_,'assignToHash':PyJs_assignToHash_374_,'pushId':PyJs_pushId_375_,'compiler':var.get('JavaScriptCompiler'),'compileChildren':PyJs_compileChildren_376_,'matchExistingProgram':PyJs_matchExistingProgram_377_,'programExpression':PyJs_programExpression_378_,'useRegister':PyJs_useRegister_379_,'push':PyJs_push_380_,'pushStackLiteral':PyJs_pushStackLiteral_381_,'pushSource':PyJs_pushSource_382_,'replaceStack':PyJs_replaceStack_383_,'incrStack':PyJs_incrStack_384_,'topStackName':PyJs_topStackName_385_,'flushInline':PyJs_flushInline_386_,'isInline':PyJs_isInline_387_,'popStack':PyJs_popStack_388_,'topStack':PyJs_topStack_389_,'contextName':PyJs_contextName_390_,'quotedString':PyJs_quotedString_391_,'objectLiteral':PyJs_objectLiteral_392_,'aliasable':PyJs_aliasable_393_,'setupHelper':PyJs_setupHelper_394_,'setupParams':PyJs_setupParams_395_,'setupHelperArgs':PyJs_setupHelperArgs_396_}))
            PyJs_LONG_397_()
            @Js
            def PyJs_anonymous_398_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['reservedWords', 'compilerWords', 'i', 'l'])
                def PyJs_LONG_399_(var=var):
                    return ((((((((((((Js('break else new var')+Js(' case finally return void'))+Js(' catch for switch while'))+Js(' continue function this with'))+Js(' default if throw'))+Js(' delete in try'))+Js(' do instanceof typeof'))+Js(' abstract enum int short'))+Js(' boolean export interface static'))+Js(' byte extends long super'))+Js(' char final native synchronized'))+Js(' class float package throws'))+Js(' const goto private transient'))
                var.put('reservedWords', (((PyJs_LONG_399_()+Js(' debugger implements protected volatile'))+Js(' double import public let yield await'))+Js(' null true false')).callprop('split', Js(' ')))
                var.put('compilerWords', var.get('JavaScriptCompiler').put('RESERVED_WORDS', Js({})))
                #for JS loop
                var.put('i', Js(0.0))
                var.put('l', var.get('reservedWords').get('length'))
                while (var.get('i')<var.get('l')):
                    var.get('compilerWords').put(var.get('reservedWords').get(var.get('i')), Js(True))
                    # update
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            PyJs_anonymous_398_._set_name('anonymous')
            PyJs_anonymous_398_()
            @Js
            def PyJs_anonymous_400_(name, this, arguments, var=var):
                var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
                var.registers(['name'])
                return (var.get('JavaScriptCompiler').get('RESERVED_WORDS').get(var.get('name')).neg() and JsRegExp('/^[a-zA-Z_$][0-9a-zA-Z_$]*$/').callprop('test', var.get('name')))
            PyJs_anonymous_400_._set_name('anonymous')
            var.get('JavaScriptCompiler').put('isValidJavaScriptVariableName', PyJs_anonymous_400_)
            pass
            var.get('exports').put('default', var.get('JavaScriptCompiler'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_332_._set_name('anonymous')
        @Js
        def PyJs_anonymous_401_(module, exports, __webpack_require__, this, arguments, var=var):
            var = Scope({'module':module, 'exports':exports, '__webpack_require__':__webpack_require__, 'this':this, 'arguments':arguments}, var)
            var.registers(['SourceNode', 'CodeGen', 'exports', 'module', 'SourceMap', '_Object$keys', 'castChunk', '_utils', '__webpack_require__'])
            @Js
            def PyJsHoisted_castChunk_(chunk, codeGen, loc, this, arguments, var=var):
                var = Scope({'chunk':chunk, 'codeGen':codeGen, 'loc':loc, 'this':this, 'arguments':arguments}, var)
                var.registers(['i', 'len', 'codeGen', 'chunk', 'loc', 'ret'])
                if var.get('_utils').callprop('isArray', var.get('chunk')):
                    var.put('ret', Js([]))
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('len', var.get('chunk').get('length'))
                    while (var.get('i')<var.get('len')):
                        var.get('ret').callprop('push', var.get('codeGen').callprop('wrap', var.get('chunk').get(var.get('i')), var.get('loc')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    return var.get('ret')
                else:
                    if (PyJsStrictEq(var.get('chunk',throw=False).typeof(),Js('boolean')) or PyJsStrictEq(var.get('chunk',throw=False).typeof(),Js('number'))):
                        return (var.get('chunk')+Js(''))
                return var.get('chunk')
            PyJsHoisted_castChunk_.func_name = 'castChunk'
            var.put('castChunk', PyJsHoisted_castChunk_)
            @Js
            def PyJsHoisted_CodeGen_(srcFile, this, arguments, var=var):
                var = Scope({'srcFile':srcFile, 'this':this, 'arguments':arguments}, var)
                var.registers(['srcFile'])
                var.get(u"this").put('srcFile', var.get('srcFile'))
                var.get(u"this").put('source', Js([]))
            PyJsHoisted_CodeGen_.func_name = 'CodeGen'
            var.put('CodeGen', PyJsHoisted_CodeGen_)
            Js('use strict')
            var.put('_Object$keys', var.get('__webpack_require__')(Js(60.0)).get('default'))
            var.get('exports').put('__esModule', Js(True))
            var.put('_utils', var.get('__webpack_require__')(Js(5.0)))
            var.put('SourceNode', var.get('undefined'))
            try:
                if Js(False):
                    var.put('SourceMap', var.get('require')(Js('source-map')))
                    var.put('SourceNode', var.get('SourceMap').get('SourceNode'))
            except PyJsException as PyJsTempException:
                PyJsHolder_657272_14675839 = var.own.get('err')
                var.force_own_put('err', PyExceptionToJs(PyJsTempException))
                try:
                    pass
                finally:
                    if PyJsHolder_657272_14675839 is not None:
                        var.own['err'] = PyJsHolder_657272_14675839
                    else:
                        del var.own['err']
                    del PyJsHolder_657272_14675839
            if var.get('SourceNode').neg():
                @Js
                def PyJs_anonymous_402_(line, column, srcFile, chunks, this, arguments, var=var):
                    var = Scope({'line':line, 'column':column, 'srcFile':srcFile, 'chunks':chunks, 'this':this, 'arguments':arguments}, var)
                    var.registers(['column', 'line', 'chunks', 'srcFile'])
                    var.get(u"this").put('src', Js(''))
                    if var.get('chunks'):
                        var.get(u"this").callprop('add', var.get('chunks'))
                PyJs_anonymous_402_._set_name('anonymous')
                var.put('SourceNode', PyJs_anonymous_402_)
                @Js
                def PyJs_add_403_(chunks, this, arguments, var=var):
                    var = Scope({'chunks':chunks, 'this':this, 'arguments':arguments, 'add':PyJs_add_403_}, var)
                    var.registers(['chunks'])
                    if var.get('_utils').callprop('isArray', var.get('chunks')):
                        var.put('chunks', var.get('chunks').callprop('join', Js('')))
                    var.get(u"this").put('src', var.get('chunks'), '+')
                PyJs_add_403_._set_name('add')
                @Js
                def PyJs_prepend_404_(chunks, this, arguments, var=var):
                    var = Scope({'chunks':chunks, 'this':this, 'arguments':arguments, 'prepend':PyJs_prepend_404_}, var)
                    var.registers(['chunks'])
                    if var.get('_utils').callprop('isArray', var.get('chunks')):
                        var.put('chunks', var.get('chunks').callprop('join', Js('')))
                    var.get(u"this").put('src', (var.get('chunks')+var.get(u"this").get('src')))
                PyJs_prepend_404_._set_name('prepend')
                @Js
                def PyJs_toStringWithSourceMap_405_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'toStringWithSourceMap':PyJs_toStringWithSourceMap_405_}, var)
                    var.registers([])
                    return Js({'code':var.get(u"this").callprop('toString')})
                PyJs_toStringWithSourceMap_405_._set_name('toStringWithSourceMap')
                @Js
                def PyJs_toString_406_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_406_}, var)
                    var.registers([])
                    return var.get(u"this").get('src')
                PyJs_toString_406_._set_name('toString')
                var.get('SourceNode').put('prototype', Js({'add':PyJs_add_403_,'prepend':PyJs_prepend_404_,'toStringWithSourceMap':PyJs_toStringWithSourceMap_405_,'toString':PyJs_toString_406_}))
            pass
            pass
            def PyJs_LONG_421_(var=var):
                @Js
                def PyJs_isEmpty_407_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'isEmpty':PyJs_isEmpty_407_}, var)
                    var.registers([])
                    return var.get(u"this").get('source').get('length').neg()
                PyJs_isEmpty_407_._set_name('isEmpty')
                @Js
                def PyJs_prepend_408_(source, loc, this, arguments, var=var):
                    var = Scope({'source':source, 'loc':loc, 'this':this, 'arguments':arguments, 'prepend':PyJs_prepend_408_}, var)
                    var.registers(['loc', 'source'])
                    var.get(u"this").get('source').callprop('unshift', var.get(u"this").callprop('wrap', var.get('source'), var.get('loc')))
                PyJs_prepend_408_._set_name('prepend')
                @Js
                def PyJs_push_409_(source, loc, this, arguments, var=var):
                    var = Scope({'source':source, 'loc':loc, 'this':this, 'arguments':arguments, 'push':PyJs_push_409_}, var)
                    var.registers(['loc', 'source'])
                    var.get(u"this").get('source').callprop('push', var.get(u"this").callprop('wrap', var.get('source'), var.get('loc')))
                PyJs_push_409_._set_name('push')
                @Js
                def PyJs_merge_410_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'merge':PyJs_merge_410_}, var)
                    var.registers(['source'])
                    var.put('source', var.get(u"this").callprop('empty'))
                    @Js
                    def PyJs_anonymous_411_(line, this, arguments, var=var):
                        var = Scope({'line':line, 'this':this, 'arguments':arguments}, var)
                        var.registers(['line'])
                        var.get('source').callprop('add', Js([Js('  '), var.get('line'), Js('\n')]))
                    PyJs_anonymous_411_._set_name('anonymous')
                    var.get(u"this").callprop('each', PyJs_anonymous_411_)
                    return var.get('source')
                PyJs_merge_410_._set_name('merge')
                @Js
                def PyJs_each_412_(iter, this, arguments, var=var):
                    var = Scope({'iter':iter, 'this':this, 'arguments':arguments, 'each':PyJs_each_412_}, var)
                    var.registers(['len', 'iter', 'i'])
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('len', var.get(u"this").get('source').get('length'))
                    while (var.get('i')<var.get('len')):
                        var.get('iter')(var.get(u"this").get('source').get(var.get('i')))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                PyJs_each_412_._set_name('each')
                @Js
                def PyJs_empty_413_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments, 'empty':PyJs_empty_413_}, var)
                    var.registers(['loc'])
                    var.put('loc', (var.get(u"this").get('currentLocation') or Js({'start':Js({})})))
                    return var.get('SourceNode').create(var.get('loc').get('start').get('line'), var.get('loc').get('start').get('column'), var.get(u"this").get('srcFile'))
                PyJs_empty_413_._set_name('empty')
                @Js
                def PyJs_wrap_414_(chunk, this, arguments, var=var):
                    var = Scope({'chunk':chunk, 'this':this, 'arguments':arguments, 'wrap':PyJs_wrap_414_}, var)
                    var.registers(['chunk', 'loc'])
                    var.put('loc', ((var.get(u"this").get('currentLocation') or Js({'start':Js({})})) if ((var.get('arguments').get('length')<=Js(1.0)) or PyJsStrictEq(var.get('arguments').get('1'),var.get('undefined'))) else var.get('arguments').get('1')))
                    if var.get('chunk').instanceof(var.get('SourceNode')):
                        return var.get('chunk')
                    var.put('chunk', var.get('castChunk')(var.get('chunk'), var.get(u"this"), var.get('loc')))
                    return var.get('SourceNode').create(var.get('loc').get('start').get('line'), var.get('loc').get('start').get('column'), var.get(u"this").get('srcFile'), var.get('chunk'))
                PyJs_wrap_414_._set_name('wrap')
                @Js
                def PyJs_functionCall_415_(fn, type, params, this, arguments, var=var):
                    var = Scope({'fn':fn, 'type':type, 'params':params, 'this':this, 'arguments':arguments, 'functionCall':PyJs_functionCall_415_}, var)
                    var.registers(['params', 'type', 'fn'])
                    var.put('params', var.get(u"this").callprop('generateList', var.get('params')))
                    return var.get(u"this").callprop('wrap', Js([var.get('fn'), (((Js('.')+var.get('type'))+Js('(')) if var.get('type') else Js('(')), var.get('params'), Js(')')]))
                PyJs_functionCall_415_._set_name('functionCall')
                @Js
                def PyJs_quotedString_416_(str, this, arguments, var=var):
                    var = Scope({'str':str, 'this':this, 'arguments':arguments, 'quotedString':PyJs_quotedString_416_}, var)
                    var.registers(['str'])
                    return ((Js('"')+(var.get('str')+Js('')).callprop('replace', JsRegExp('/\\\\/g'), Js('\\\\')).callprop('replace', JsRegExp('/"/g'), Js('\\"')).callprop('replace', JsRegExp('/\\n/g'), Js('\\n')).callprop('replace', JsRegExp('/\\r/g'), Js('\\r')).callprop('replace', JsRegExp('/\\u2028/g'), Js('\\u2028')).callprop('replace', JsRegExp('/\\u2029/g'), Js('\\u2029')))+Js('"'))
                PyJs_quotedString_416_._set_name('quotedString')
                @Js
                def PyJs_objectLiteral_417_(obj, this, arguments, var=var):
                    var = Scope({'obj':obj, 'this':this, 'arguments':arguments, 'objectLiteral':PyJs_objectLiteral_417_}, var)
                    var.registers(['obj', 'ret', '_this', 'pairs'])
                    var.put('_this', var.get(u"this"))
                    var.put('pairs', Js([]))
                    @Js
                    def PyJs_anonymous_418_(key, this, arguments, var=var):
                        var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
                        var.registers(['key', 'value'])
                        var.put('value', var.get('castChunk')(var.get('obj').get(var.get('key')), var.get('_this')))
                        if PyJsStrictNeq(var.get('value'),Js('undefined')):
                            var.get('pairs').callprop('push', Js([var.get('_this').callprop('quotedString', var.get('key')), Js(':'), var.get('value')]))
                    PyJs_anonymous_418_._set_name('anonymous')
                    var.get('_Object$keys')(var.get('obj')).callprop('forEach', PyJs_anonymous_418_)
                    var.put('ret', var.get(u"this").callprop('generateList', var.get('pairs')))
                    var.get('ret').callprop('prepend', Js('{'))
                    var.get('ret').callprop('add', Js('}'))
                    return var.get('ret')
                PyJs_objectLiteral_417_._set_name('objectLiteral')
                @Js
                def PyJs_generateList_419_(entries, this, arguments, var=var):
                    var = Scope({'entries':entries, 'this':this, 'arguments':arguments, 'generateList':PyJs_generateList_419_}, var)
                    var.registers(['len', 'ret', 'i', 'entries'])
                    var.put('ret', var.get(u"this").callprop('empty'))
                    #for JS loop
                    var.put('i', Js(0.0))
                    var.put('len', var.get('entries').get('length'))
                    while (var.get('i')<var.get('len')):
                        if var.get('i'):
                            var.get('ret').callprop('add', Js(','))
                        var.get('ret').callprop('add', var.get('castChunk')(var.get('entries').get(var.get('i')), var.get(u"this")))
                        # update
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    return var.get('ret')
                PyJs_generateList_419_._set_name('generateList')
                @Js
                def PyJs_generateArray_420_(entries, this, arguments, var=var):
                    var = Scope({'entries':entries, 'this':this, 'arguments':arguments, 'generateArray':PyJs_generateArray_420_}, var)
                    var.registers(['ret', 'entries'])
                    var.put('ret', var.get(u"this").callprop('generateList', var.get('entries')))
                    var.get('ret').callprop('prepend', Js('['))
                    var.get('ret').callprop('add', Js(']'))
                    return var.get('ret')
                PyJs_generateArray_420_._set_name('generateArray')
                return var.get('CodeGen').put('prototype', Js({'isEmpty':PyJs_isEmpty_407_,'prepend':PyJs_prepend_408_,'push':PyJs_push_409_,'merge':PyJs_merge_410_,'each':PyJs_each_412_,'empty':PyJs_empty_413_,'wrap':PyJs_wrap_414_,'functionCall':PyJs_functionCall_415_,'quotedString':PyJs_quotedString_416_,'objectLiteral':PyJs_objectLiteral_417_,'generateList':PyJs_generateList_419_,'generateArray':PyJs_generateArray_420_}))
            PyJs_LONG_421_()
            var.get('exports').put('default', var.get('CodeGen'))
            var.get('module').put('exports', var.get('exports').get('default'))
        PyJs_anonymous_401_._set_name('anonymous')
        @Js
        def PyJs_anonymous_422_(modules, this, arguments, var=var):
            var = Scope({'modules':modules, 'this':this, 'arguments':arguments}, var)
            var.registers(['__webpack_require__', 'installedModules', 'modules'])
            @Js
            def PyJsHoisted___webpack_require___(moduleId, this, arguments, var=var):
                var = Scope({'moduleId':moduleId, 'this':this, 'arguments':arguments}, var)
                var.registers(['module', 'moduleId'])
                if var.get('installedModules').get(var.get('moduleId')):
                    return var.get('installedModules').get(var.get('moduleId')).get('exports')
                var.put('module', var.get('installedModules').put(var.get('moduleId'), Js({'exports':Js({}),'id':var.get('moduleId'),'loaded':Js(False)})))
                var.get('modules').get(var.get('moduleId')).callprop('call', var.get('module').get('exports'), var.get('module'), var.get('module').get('exports'), var.get('__webpack_require__'))
                var.get('module').put('loaded', Js(True))
                return var.get('module').get('exports')
            PyJsHoisted___webpack_require___.func_name = '__webpack_require__'
            var.put('__webpack_require__', PyJsHoisted___webpack_require___)
            var.put('installedModules', Js({}))
            pass
            var.get('__webpack_require__').put('m', var.get('modules'))
            var.get('__webpack_require__').put('c', var.get('installedModules'))
            var.get('__webpack_require__').put('p', Js(''))
            return var.get('__webpack_require__')(Js(0.0))
        PyJs_anonymous_422_._set_name('anonymous')
        return PyJs_anonymous_422_(Js([PyJs_anonymous_1_, PyJs_anonymous_4_, PyJs_anonymous_6_, PyJs_anonymous_8_, PyJs_anonymous_10_, PyJs_anonymous_19_, PyJs_anonymous_23_, PyJs_anonymous_24_, PyJs_anonymous_25_, PyJs_anonymous_27_, PyJs_anonymous_29_, PyJs_anonymous_30_, PyJs_anonymous_33_, PyJs_anonymous_38_, PyJs_anonymous_39_, PyJs_anonymous_40_, PyJs_anonymous_66_, PyJs_anonymous_67_, PyJs_anonymous_69_, PyJs_anonymous_72_, PyJs_anonymous_74_, PyJs_anonymous_79_, PyJs_anonymous_80_, PyJs_anonymous_86_, PyJs_anonymous_88_, PyJs_anonymous_89_, PyJs_anonymous_92_, PyJs_anonymous_94_, PyJs_anonymous_96_, PyJs_anonymous_98_, PyJs_anonymous_100_, PyJs_anonymous_102_, PyJs_anonymous_104_, PyJs_anonymous_106_, PyJs_anonymous_108_, PyJs_anonymous_110_, PyJs_anonymous_112_, PyJs_anonymous_115_, PyJs_anonymous_117_, PyJs_anonymous_119_, PyJs_anonymous_121_, PyJs_anonymous_123_, PyJs_anonymous_124_, PyJs_anonymous_125_, PyJs_anonymous_126_, PyJs_anonymous_127_, PyJs_anonymous_130_, PyJs_anonymous_134_, PyJs_anonymous_136_, PyJs_anonymous_144_, PyJs_anonymous_145_, PyJs_anonymous_148_, PyJs_anonymous_149_, PyJs_anonymous_152_, PyJs_anonymous_154_, PyJs_anonymous_156_, PyJs_anonymous_157_, PyJs_anonymous_158_, PyJs_anonymous_160_, PyJs_anonymous_162_, PyJs_anonymous_166_, PyJs_anonymous_167_, PyJs_anonymous_168_, PyJs_anonymous_171_, PyJs_anonymous_173_, PyJs_anonymous_176_, PyJs_anonymous_179_, PyJs_anonymous_183_, PyJs_anonymous_186_, PyJs_anonymous_189_, PyJs_anonymous_192_, PyJs_anonymous_193_, PyJs_anonymous_197_, PyJs_anonymous_200_, PyJs_anonymous_203_, PyJs_anonymous_204_, PyJs_anonymous_206_, PyJs_anonymous_207_, PyJs_anonymous_209_, PyJs_anonymous_224_, PyJs_anonymous_225_, PyJs_anonymous_226_, PyJs_anonymous_229_, PyJs_anonymous_231_, PyJs_anonymous_236_, PyJs_anonymous_240_, PyJs_anonymous_242_, PyJs_anonymous_273_, PyJs_anonymous_278_, PyJs_anonymous_296_, PyJs_anonymous_297_, PyJs_anonymous_332_, PyJs_anonymous_401_]))
    return PyJs_LONG_423_()
PyJs_anonymous_0_._set_name('anonymous')
@Js
def PyJs_webpackUniversalModuleDefinition_424_(root, factory, this, arguments, var=var):
    var = Scope({'root':root, 'factory':factory, 'this':this, 'arguments':arguments, 'webpackUniversalModuleDefinition':PyJs_webpackUniversalModuleDefinition_424_}, var)
    var.registers(['root', 'factory'])
    if (PyJsStrictEq(var.get('exports',throw=False).typeof(),Js('object')) and PyJsStrictEq(var.get('module',throw=False).typeof(),Js('object'))):
        var.get('module').put('exports', var.get('factory')())
    else:
        if (PyJsStrictEq(var.get('define',throw=False).typeof(),Js('function')) and var.get('define').get('amd')):
            var.get('define')(Js([]), var.get('factory'))
        else:
            if PyJsStrictEq(var.get('exports',throw=False).typeof(),Js('object')):
                var.get('exports').put('Handlebars', var.get('factory')())
            else:
                var.get('root').put('Handlebars', var.get('factory')())
PyJs_webpackUniversalModuleDefinition_424_._set_name('webpackUniversalModuleDefinition')
PyJs_webpackUniversalModuleDefinition_424_(var.get(u"this"), PyJs_anonymous_0_)
pass
pass


# Add lib to the module scope
handlebars_js = var.to_python()