# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-02-28
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from hsutil.misc import nonone

from ..model.completion import CompletionList

class CompletableEdit(object):
    def __init__(self, source=None):
        # `source` must be have a 'document' attr
        self._source = source
        self._attrname = ''
        self._candidates = None
        self._completions = None
        self._complete_completion = ''
        self.completion = ''
        self._text = ''
    
    #--- Private
    def _refresh_candidates(self):
        if self.source is None or not self.attrname:
            return
        doc = self.source.document
        attrname = self.attrname
        if attrname == 'description':
            self._candidates = doc.transactions.descriptions
        elif attrname == 'payee':
            self._candidates = doc.transactions.payees
        elif attrname in ('from', 'to', 'account', 'transfer'):
            result = doc.transactions.account_names
            # `result` doesn't contain empty accounts' name, so we'll add them.
            result += [a.name for a in doc.accounts]
            if attrname == 'transfer' and doc.shown_account is not None:
                result = [name for name in result if name != doc.shown_account.name]
            self._candidates = result
    
    def _set_completion(self, completion):
        completion = nonone(completion, '')
        self._complete_completion = completion
        self.completion = completion[len(self._text):]
    
    #--- Public
    def commit(self):
        """Accepts current completion and updates the text with it.
        
        If the text is a substring of the completion, completion's case will prevail. If, however,
        the completion is the same length as the text, it means that the user completly types the
        string. In this case, we assume that the user wants his own case to prevail.
        """
        if len(self._text) < len(self._complete_completion):
            self._text = self._complete_completion
            self.completion = ''
    
    def down(self):
        if self._completions:
            self._set_completion(self._completions.prev())
    
    def up(self):
        if self._completions:
            self._set_completion(self._completions.next())
    
    #--- Properties
    @property
    def attrname(self):
        return self._attrname
    
    @attrname.setter
    def attrname(self, value):
        self._attrname = value
        self._refresh_candidates()
        self._text = ''
        self._set_completion('')
    
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, value):
        self._source = value
        self._refresh_candidates()
        self._text = ''
        self._set_completion('')
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        if self._candidates:
            self._completions = CompletionList(value, self._candidates)
            self._set_completion(self._completions.current())
        else:
            self._completions = None
    
