# -*- coding: utf-8 -*-

import time

from slacker import Slacker


class SlackProgress(object):
    def __init__(
            self, token, channel, suffix='%', full_width=False,
            fill_char='⬛', empty_char='⬜',
    ):
        self.suffix = suffix
        self.channel = channel
        self.slack = Slacker(token)
        self.full_width = full_width
        self.fill_char = fill_char
        self.empty_char = empty_char

    def new(self, total=100):
        """
        Instantiate and return a new ProgressBar object
        params:
         - total(int): total number of items
        """
        res = self.slack.chat.post_message(self.channel, self._makebar(0), 
                                           as_user=True)
        bar = ProgressBar(self, total)
        bar.msg_ts = res.body['ts']
        bar.channel_id = res.body['channel']
        return bar

    def iter(self, iterable):
        """
        Wraps an iterable object, automatically creating
        and updating a progress bar
        """
        bar = self.new(total=len(iterable)-1)
        for idx, item in enumerate(iterable):
            yield(item)
            bar.done = idx

    def _update(self, chan, msg_ts, pos, msg_log):
        content = [self._makebar(pos)] + msg_log
        content = '\n'.join(content)
        self.slack.chat.update(chan, msg_ts, content)

    def _makebar(self, pos):
        filled = int(round(pos / 5))
        bar = filled * self.fill_char
        empty = ''
        if self.full_width:
            empty  = (int(100 / 5) - filled) * self.empty_char
        return '{}{} {}{}'.format(bar, empty, pos, self.suffix)


class ProgressBar(object):

    msg_ts = None
    channel_id = None

    def __init__(self, sp, total):
        self._sp = sp
        self._pos = 0
        self._done = 0
        self.total = total
        self._msg_log = []

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, val):
        self._done = val
        self.pos = round((val/self.total) * 100)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if val != self._pos:
            self._pos = val
            self._update()

    def log(self, msg):
        timestamp = time.strftime('%X')  # returns HH:MM:SS time
        self._msg_log.append('*{}* - [{}]'.format(timestamp, msg))
        self._update()

    def _update(self):
        self._sp._update(self.channel_id, self.msg_ts, self._pos, self._msg_log)
