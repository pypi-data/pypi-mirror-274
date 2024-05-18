# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Database Interfaces
    ~~~~~~~~~~~~~~~~~~~

"""

from .account import PrivateKeyDBI, MetaDBI, DocumentDBI
from .account import UserDBI, ContactDBI, GroupDBI, GroupHistoryDBI
from .account import AccountDBI

from .message import ReliableMessageDBI, CipherKeyDBI, GroupKeysDBI
from .message import MessageDBI

from .session import LoginDBI, ProviderDBI, StationDBI
from .session import SessionDBI
from .session import ProviderInfo, StationInfo


__all__ = [

    #
    #   Account
    #
    'PrivateKeyDBI', 'MetaDBI', 'DocumentDBI',
    'UserDBI', 'ContactDBI', 'GroupDBI', 'GroupHistoryDBI',
    'AccountDBI',

    #
    #   Message
    #
    'ReliableMessageDBI', 'CipherKeyDBI', 'GroupKeysDBI',
    'MessageDBI',

    #
    #   Session
    #
    'LoginDBI', 'ProviderDBI', 'StationDBI',
    'SessionDBI',
    'ProviderInfo', 'StationInfo',
]
