# !/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2020 growingio.com, Inc.  All Rights Reserved


class ImportBase:
    """
      Import Base
    """

    def __init__(self, name, path, debug, format, datasourceId, jobName, clear):
        self.name = name
        self.path = path
        self.debug = debug
        self.format = format
        self.datasourceId = datasourceId
        self.jobName = jobName
        self.clear = clear


class SVBase:
    """
      SV Base
    """

    def __init__(self, skipHeader, separator, qualifier='"'):
        self.qualifier = qualifier
        self.separator = separator
        self.skipHeader = skipHeader


class UserVariables(ImportBase):
    """
      用户属性
    """

    def __init__(self, name, path, debug, format, datasourceId, jobName, clear):
        ImportBase.__init__(self, name, path, debug, format, datasourceId, jobName, clear)


class UserVariablesJson(UserVariables):
    """
      用户属性-Josn格式
    """

    def __init__(self, name, path, format, datasourceId, jobName, debug=True, clear=False):
        UserVariables.__init__(self, name, path, debug, format, datasourceId, jobName, clear)


class UserVariablesSv(UserVariables, SVBase):
    """
      用户属性-CSV/TSV格式
    """

    def __init__(self, name, path, debug, format, datasourceId, jobName, attributes, skipHeader, separator, clear,
                 qualifier='"'):
        UserVariables.__init__(self, name, path, debug, format, datasourceId, jobName, clear)
        SVBase.__init__(self, skipHeader, separator, qualifier)
        self.attributes = attributes


class Events(ImportBase):
    """
      用户行为
    """

    def __init__(self, name, path, debug, format, datasourceId, eventStart, eventEnd, jobName, clear):
        ImportBase.__init__(self, name, path, debug, format, datasourceId, jobName, clear)
        self.eventStart = eventStart
        self.eventEnd = eventEnd
        self.jobName = jobName
        self.clear = clear


class EventsJson(Events):
    """
      用户行为-Josn格式
    """

    def __init__(self, name, path, format, datasourceId, eventStart, eventEnd, jobName, debug=True, clear=False):
        Events.__init__(self, name, path, debug, format, datasourceId, eventStart, eventEnd, jobName, clear)


class EventsCv(Events, SVBase):
    """
      用户行为-CSV/TSV格式
    """

    def __init__(self, name, path, debug, format, datasourceId, eventStart, eventEnd, jobName, attributes, skipHeader,
                 separator, clear, qualifier='"'):
        Events.__init__(self, name, path, debug, format, datasourceId, eventStart, eventEnd, jobName, clear)
        SVBase.__init__(self, skipHeader, separator, qualifier)
        self.attributes = attributes


class DataEvent:
    """
      用户行为大数据规定格式
    """

    def __init__(self, userId, event, timestamp, attrs, userKey='', eventId=None, dataSourceId=None):
        self.userId = userId
        self.event = event
        self.userKey = userKey
        self.eventId = eventId
        self.timestamp = timestamp
        self.attrs = attrs
        self.dataSourceId = dataSourceId


class DataUser:
    """
      用户属性大数据规定格式
    """

    def __init__(self, userId, userKey, attrs):
        self.userId = userId
        self.userKey = userKey
        self.attrs = attrs


class DataItem:
    """
      维度表大数据规定格式
    """

    def __init__(self, item_id, attrs):
        self.item_id = item_id
        self.attrs = attrs


class ImportItem:
    """
      Import Item
    """

    def __init__(self, name, path, debug, format, itemKey, jobName, clear):
        self.name = name
        self.path = path
        self.debug = debug
        self.format = format
        self.itemKey = itemKey
        self.jobName = jobName
        self.clear = clear


class ItemVariables(ImportItem):
    """
      维度表
    """

    def __init__(self, name, path, debug, format, itemKey, jobName, clear):
        ImportItem.__init__(self, name, path, debug, format, itemKey, jobName, clear)
        super().__init__(name, path, debug, format, itemKey, jobName, clear)


class ItemVariablesJson(ItemVariables):
    """
      维度表-Json格式
    """

    def __init__(self, name, path, format, itemKey, jobName, debug=True, clear=False):
        ItemVariables.__init__(self, name, path, debug, format, itemKey, jobName, clear)


class ItemVariablesSv(ItemVariables, SVBase):
    """
      维度表-TSV格式
    """

    def __init__(self, name, path, debug, format, itemKey, jobName, attributes, skipHeader, separator, clear,
                 qualifier='"'):
        ItemVariables.__init__(self, name, path, debug, format, itemKey, jobName, clear)
        SVBase.__init__(self, skipHeader, separator, qualifier)
        self.attributes = attributes


class ItemVariablesCsv(ItemVariables):
    """
      维度表-Csv格式
    """

    def __init__(self, name, path, format, itemKey, jobName, debug=True, clear=False):
        ItemVariables.__init__(self, name, path, debug, format, itemKey, jobName, clear)
