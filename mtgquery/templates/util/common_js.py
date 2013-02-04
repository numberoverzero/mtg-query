import util


def tablesort_init(table_id):
    return u'''$("#{table_id}").tablesorter({{theme : "bootstrap", widgets : ["uitheme"], widgetOptions : {{ uitheme : "bootstrap" }} }});'''.format(table_id=table_id)


def tablesort_bootstrap_theme():
    return u'''$.extend($.tablesorter.themes.bootstrap, {
table: 'table table-bordered',
header: 'bootstrap-header',
sortNone: 'bootstrap-icon-unsorted',
sortAsc: 'icon-chevron-up',
sortDesc: 'icon-chevron-down'
});'''


def autosize(element):
    return u'''$('{element}').autosize();'''.format(element=element)


def notifier_init(func_name, element_id, max_n, notifications=None):
    init = u"""var {f} = $("#{e}").notifier({m});""".format(f=func_name, e=element_id, m=max_n)
    if notifications is None:
        return init
    notifications = (util.html_escape(n) for n in notifications)
    notifications = u"\n  ".join(u'{f}("{n}");'.format(f=func_name, n=n) for n in notifications)
    return init + u"\n  " + notifications


def hide_element(id):
    return u"""$("#{id}").hide();""".format(id=id)


def add_click_handler(id, string):
    return u"""$('#{id}').click(function(){{{s}return false;}});""".format(id=id, s=string)


def card_tooltips():
    return """var tt = $("a.card-tooltip[rel=tooltip]");
tt.tooltip({
html: true,
trigger: 'click',
placement: 'right',
animation: false,
template: '<div class="tooltip"><div class="tooltip-inner"></div></div>'}).click(function(e) { e.preventDefault(); });
    // [[HACK]] images inside tooltips have weird layout issues the first time they're shown.
    // For now we're just going to show/hide them all.  I have mixed feelings regarding the quality of this 'solution'...
tt.tooltip('show');
tt.tooltip('hide');"""
