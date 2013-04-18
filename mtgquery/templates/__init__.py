import markupsafe


def notifier_init(func_name, element_id, max_n, notifications=None):
    init = u"""var {f} = $("#{e}").notifier({m});""".format(f=func_name, e=element_id, m=max_n)
    if notifications is None:
        return init
    notifications = (markupsafe.escape(n) for n in notifications)
    notifications = u"\n  ".join(u'{f}("{n}");'.format(f=func_name, n=n) for n in notifications)
    return init + u"\n  " + notifications
