# coding=utf-8

"""
This module contains custom exceptions.
"""


class PropertyError(Exception):
    """Error reading JavaProperty of jpk-force file."""
    def __init__(self, key, message=''):
        self.key = key
        self.message = message

    def __str__(self):
        return 'JavaProperty corrupted:\n"{key}"\n{message}'.format(key=self.key, message=self.message)


class ForceFileError(Exception):
    """Error reading jpk-force file."""
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return 'ForceFile error: {message}'.format(message=self.message)


class ContentError(Exception):
    """Error reading jpk-force file contents."""
    def __init__(self, content, message=''):
        self.message = message
        self.content = content

    def __str__(self):
        return 'Content error: {content} {message}'.format(content=self.content, message=self.message)


class ChannelError(Exception):
    """Error regarding data channels."""
    def __init__(self, channel, message=''):
        self.message = message
        self.channel = channel

    def __str__(self):
        return 'Channel "{channel}" error: {message}'.format(channel=self.channel, message=self.message)
