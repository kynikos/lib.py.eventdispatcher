# EventDispatcher - An event dispatcher for Python.
# Copyright (C) 2015 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of EventDispatcher.
#
# EventDispatcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EventDispatcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventDispatcher.  If not, see <http://www.gnu.org/licenses/>.


class EventDispatcher:
    # TODO: Use weakref when binding handlers
    def __init__(self):
        self.handlers = {}

    def bind(self, event, handler):
        """
        Bind a handler to an event.
        """
        try:
            self.handlers[event].add(handler)
        except KeyError:
            self.handlers[event] = set((handler, ))

    def bind_one(self, event, handler):
        """
        Bind a handler to an event and unbind all the others.
        """
        self.handlers[event] = set((handler, ))

    def unbind(self, event, handler):
        """
        Unbind a handler from an event.
        """
        self.handlers[event].discard(handler)

    def unbind_all(self, event):
        """
        Unbind all handlers from an event.
        """
        del self.handlers[event]

    def has_handlers(self, event):
        """
        Return True if event has at least one handler, False otherwise.
        """
        try:
            return len(self.handlers[event]) > 0
        except KeyError:
            return False

    def fire(self, event, *args, **kwargs):
        """
        Fire an event.
        """
        try:
            handlerbag = self.handlers[event]
        except KeyError:
            pass
        else:
            # TODO: Test what happens if the handler has been
            #       deleted/garbage-collected, and possibly protect from the
            #       resulting exception
            for handler in handlerbag:
                handler(*args, **kwargs)
