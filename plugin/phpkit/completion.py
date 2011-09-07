# -*- coding: utf-8 -*-

import gobject
import gtksourceview2 as gsv
import os
from gettext import gettext as _

try:
    import json
except ImportError:
    import simplejson as json


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
        self.tags_root = os.path.join(os.path.dirname(__file__), 'tags')

    def do_get_name(self):
        return _('PHP')

    def do_get_activation(self):
        return gsv.COMPLETION_ACTIVATION_USER_REQUESTED

    def do_activate_proposal(self, proposal, textiter):
        return False

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
        textiter = context.get_iter()
        buff = textiter.get_buffer()
        start, word = self.get_word(textiter)
        proposals = self.get_proposals(word)
        self.move_mark(buff, start)
        context.add_proposals(self, proposals, True)

    def move_mark(self, buff, start):
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            buff.create_mark(self.MARK_NAME, start, True)
        else:
            buff.move_mark(mark, start)

    def get_proposals(self, keyword, tag='php_internal'):
        tagpath = os.path.join(self.tags_root, tag)
        proposals = []
        lookups = ['classes', 'interfaces', 'functions']

        for lookup in lookups:
            filepath = os.path.join(tagpath, '%s.json' % lookup)
            candidates = []
            if os.path.isfile(filepath):
                f = open(filepath)
                candidates = json.load(f)
                f.close()

            if candidates:
                for candidate in candidates:
                    if candidate['name'].startswith(keyword) is True:
                        proposals.append(PHPProposal(candidate))
        return proposals

    def get_word(self, textiter):
        if not textiter.ends_word or textiter.get_char() == '_':
            return None, None

        start = textiter.copy()
        while True:
            if start.starts_line():
                break
            start.backward_char()
            ch = start.get_char()
            if not (ch.isalnum() or ch == '_' or ch == ':'):
                start.forward_char()
                break
        if start.equal(textiter):
            return None, None

        while (not start.equal(textiter)) and start.get_char().isdigit():
            start.forward_char()
        if start.equal(textiter):
            return None, None
        return start, start.get_text(textiter)


gobject.type_register(PHPProposal)
gobject.type_register(PHPProvider)
