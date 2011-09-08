# -*- coding: utf-8 -*-

import gobject
import gtksourceview2 as gsv
import os
from gettext import gettext as _
from glob import glob
import re

try:
    import json
except ImportError:
    import simplejson as json


class PHPProposal(gobject.GObject, gsv.CompletionProposal):

    def __init__(self, proposal):
        gobject.GObject.__init__(self)
        self.proposal = proposal

    def do_get_text(self):
        text = self.proposal['name']
        if self.is_constant():
            return text

        required, optional = self.format_params()
        # we only care about required params if any
        return '%s(%s)' % (text, required)

    def do_get_label(self):
        label = self.proposal['name']
        if self.is_constant():
            return label

        params = ''
        required, optional = self.format_params()
        if required:
            params = required
        if optional:
            if required:
                params = '%s %s' % (params, optional)
            else:
                # str is immutable
                option = list(optional)
                # no need for first ', ' characters
                del option[1:3]
                optional = ''.join(option)
                params = optional
        return '%s(%s)' % (label, params)

    def do_get_info(self):
        info = self.proposal['info']
        if info:
            return gobject.markup_escape_text(info)
        return _('Info is not available')

    def format_params(self):
        params = self.proposal.get('params', '')
        required = optional = ''
        if 'required' in params:
            required = ', '.join(params['required'])
        if 'optional' in params:
            optional = ['[, %s]' % option for option in params['optional']]
            optional = ' '.join(optional)
        return required, optional

    def is_constant(self):
        return self.proposal.get('type', '') == 'constant'


class PHPProvider(gobject.GObject, gsv.CompletionProvider):

    MARK_NAME = 'PHPProviderCompletionMark'

    TAGS = {}

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
        # TODO: consider to use placeholder similar to snippet's magic
        buff = textiter.get_buffer()
        buff.begin_user_action()
        text = proposal.do_get_text()

        start, word = self.get_word(textiter)
        text = '%s' % re.sub(r'^%s' % word, '', text)
        buff.insert_at_cursor(text)

        start = buff.get_iter_at_mark(buff.get_insert())
        if '(' in text:
            while not start.get_char() == '(':
                start.backward_char()
            start.forward_char()
        buff.place_cursor(start)
        buff.end_user_action()
        return True

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
        if not word:
            context.add_proposals(self, [], True)
        else:
            self.move_mark(buff, start)
            context.add_proposals(self, self.get_proposals(word), True)

    def move_mark(self, buff, start):
        mark = buff.get_mark(self.MARK_NAME)
        if not mark:
            buff.create_mark(self.MARK_NAME, start, True)
        else:
            buff.move_mark(mark, start)

    def get_proposals(self, keyword, tag='php_internal'):
        tagpath = os.path.join(self.tags_root, tag)

        if not tag in self.TAGS:
            self.TAGS[tag] = {}

        if not self.TAGS[tag]:
            filepaths = glob(os.path.join(tagpath, '*.json'))
            for filepath in filepaths:
                try:
                    f = open(filepath)
                    self.TAGS[tag][os.path.basename(filepath)] = json.load(f)
                    f.close()
                except IOError:
                    pass

        proposals = []
        candidates = self.TAGS[tag].iteritems()

        for key, itemlist in candidates:
            try:
                for item in itemlist:
                    if item['name'].startswith(keyword) is True:
                        proposals.append(PHPProposal(item))
            except KeyError:
                pass
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
