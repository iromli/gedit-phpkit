# -*- coding: utf-8 -*-

import gobject
import gtksourceview2 as gsv


class PHPProposal(gobject.GObject, gsv.CompletionProposal):

    def __init__(self, proposal):
        gobject.GObject.__init__(self)
        self.name = proposal['name']
        self.info = proposal['info']
        self.params = proposal['params']

    def do_get_text(self):
        return self.name

    def do_get_label(self):
        return self.name

    def do_get_info(self):
        if not self.info:
            return _('Info is not available')
        return gobject.markup_escape_text(self.info)


class PHPProvider(gobject.GObject, gsv.CompletionProvider):

    MARK_NAME = 'PHPProviderCompletionMark'

    def __init__(self, plugin):
        gobject.GObject.__init__(self)
        self.mark = None
        self._plugin = plugin

    def do_get_name(self):
        return _('PHP')

    def do_get_activation(self):
        return gsv.COMPLETION_ACTIVATION_USER_REQUESTED

    def do_activate_proposal(self, proposal, textiter):
        return false

    def do_match(self, context):
        lang = context.get_iter().get_buffer().get_language()
        if not lang or lang.get_id() != 'php':
            return False
        return True

    def do_get_start_iter(self, context, proposal):
        buff = context.get_iter().get_buffer()
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            return None
        return buff.get_iter_at_mark(mark)

    def do_populate(self, context):
        pass

    def move_mark(self, buff, start):
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            buff.create_mark(self.MARK_NAME, start, True)
        else:
            buff.move_mark(mark, start)


gobject.type_register(PHPProposal)
gobject.type_register(PHPProvider)
