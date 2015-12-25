# -*- coding: utf-8 -*-
import fields
from request import *

class Polling(Request):
    format = (fields.Padding, fields.HostName, '')

class Initialize(Request):
    format = (fields.Count, fields.ID, fields.Data)

class Send(Request):
    format = (fields.Sequence, fields.ID, fields.Data)

class Receive(Request):
    format = (fields.Padding, fields.Sequence, fields.ID, fields.HostName, '')

class Error(Request):
    format = ('0.0', fields.ErrorNo)

class ClientReader(Reader):
    classes = (Receive, Polling)

class ServerReader(Reader):
    classes = (Error, Initialize, Send)
