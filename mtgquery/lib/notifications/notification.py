class GenericNotification(object):
    notification_name = 'GenericNotification'

    def __init__(self, message):
        self.message = message

    @property
    def msg(self):
        return unicode(self.message, encoding="UTF-8")

    def to_flash_string(self):
        return "{}:{}".format(self.notification_name, self.message)

    @classmethod
    def load_from(cls, string):
        try:
            pieces = string.split(':', 1)
            name = pieces[0]
            if name != cls.notification_name:
                return None

            message = pieces[1]
            return cls(message)
        except:
            return None


class InvalidLine(object):
    notification_name = 'InvalidLine'
    
    def __init__(self, line):
        self.line = line

    @property
    def msg(self):
        return u'Could not parse the following "{}"'.format(self.line)

    def to_flash_string(self):
        return u'{}:{}'.format(self.notification_name, self.line)

    @classmethod
    def load_from(cls, string):
        try:
            pieces = string.split(':', 1)
            name = pieces[0]
            if name != cls.notification_name:
                return None

            line = pieces[1]
            return cls(line)
        except:
            return None


class UnknownCardName(object):
    notification_name = 'UnknownCardName'

    def __init__(self, card_name):
        self.card_name = card_name

    @property
    def msg(self):
        return u'Unrecognized card "{}"'.format(self.card_name)

    def to_flash_string(self):
        return u'{}:{}'.format(self.notification_name, self.card_name)

    @classmethod
    def load_from(cls, string):
        try:
            pieces = string.split(':', 1)
            name = pieces[0]
            if name != cls.notification_name:
                return None

            card_name = pieces[1]
            return cls(card_name)
        except:
            return None


class UnknownSetName(object):
    notification_name = 'UnknownSetName'

    def __init__(self, set_name):
        self.set_name = set_name

    @property
    def msg(self):
        return u'Unrecognized set "{}"'.format(self.set_name)

    def to_flash_string(self):
        return u'{}:{}'.format(self.notification_name, self.set_name)

    @classmethod
    def load_from(cls, string):
        try:
            pieces = string.split(':', 1)
            name = pieces[0]
            if name != cls.notification_name:
                return None

            set_name = pieces[1]
            return cls(set_name)
        except:
            return None


class InvalidSet(object):
    notification_name = 'InvalidSet'

    def __init__(self, set_name, card_name):
        self.set_name = set_name
        self.card_name = card_name

    @property
    def msg(self):
        return u'{c} was not printed in {s}'.format(
            c=self.card_name, s=self.set_name)

    def to_flash_string(self):
        return u'{}:{}:{}'.format(self.notification_name, self.set_name, self.card_name)

    @classmethod
    def load_from(cls, string):
        try:
            pieces = string.split(':', 2)
            name = pieces[0]
            if name != cls.notification_name:
                return None

            set_name = pieces[1]
            card_name = pieces[2]
            return cls(set_name, card_name)
        except:
            return None
