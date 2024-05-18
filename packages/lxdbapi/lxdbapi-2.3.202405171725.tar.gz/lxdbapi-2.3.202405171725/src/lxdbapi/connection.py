# Copyright 2015 Lukas Lalinsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import codecs
import logging
import uuid
import weakref
import datetime

from lxdbapi import errorsOld
from lxdbapi.client import OPEN_CONNECTION_PROPERTIES, ONLY_CLIENT_PROPERTIES
from lxdbapi.cursor import Cursor
from lxdbapi.errors import ProgrammingError

__all__ = ['Connection']

logger = logging.getLogger(__name__)


class Connection(object):
    """Database connection.

    You should not construct this object manually, use :func:`~connect` instead.
    """

    def __init__(self, client, conn_id=None, cursor_factory=None, **kwargs):
        self.codeci = None
        self._autocommit = None
        self._readonly = None
        self._transactionisolation = None
        if conn_id:
            self._id = conn_id
        else:
            self._id = str(uuid.uuid4())
        self._client = client
        self._closed = True
        if cursor_factory is not None:
            self.cursor_factory = cursor_factory
        else:
            self.cursor_factory = Cursor
        self._cursors = []
        # Extract properties to pass to OpenConnectionRequest
        self._connection_args = {}
        # The rest of the kwargs
        self._filtered_args = {}
        for k in kwargs:
            if k == 'encoding':
                self.codeci = codecs.lookup(kwargs[k])
            elif k != 'secure':
                if k in OPEN_CONNECTION_PROPERTIES:
                    self._connection_args[k] = kwargs[k]
                elif k not in ONLY_CLIENT_PROPERTIES:
                    self._filtered_args[k] = kwargs[k]
        self._connection_args['is_kryo'] = 'false'
        apptz = self._connection_args.get('appTimeZone', None)
        if apptz is None:
            dt = datetime.datetime.now().astimezone()
            apptz = dt.tzinfo.tzname(None)
            self._connection_args['appTimeZone'] = apptz
        if self.codeci is None:
            self.codeci = codecs.lookup('utf-8')
        self._client.set_avatica_con(self)

    def __del__(self):
        if not self._closed:
            try:
                self.close()
            except BaseException as ex:
                logger.debug("Ignoring exception while closing: {}".format(ex))
            finally:
                self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._closed:
            self.close()

    def open(self):  # call just once
        """Opens the connection."""
        self._client.connect()
        self._client.open_connection(self._id, info=self._connection_args)
        self._closed = False
        self.set_session(**self._filtered_args)

    def close(self):  # updated
        """Closes the connection.
        No further operations are allowed, either on the connection or any
        of its cursors, once the connection is closed.

        If the connection is used in a ``with`` statement, this method will
        be automatically called at the end of the ``with`` block.
        """
        try:
            if self._closed:
                raise ProgrammingError('the connection is already closed')
            for cursor_ref in self._cursors:
                cursor = cursor_ref()
                if cursor is not None and not cursor._closed:
                    cursor.close()
            self._client.close_connection(self._id)
        finally:
            self._client.close()
            self._closed = True

    @property
    def closed(self):
        """Read-only attribute specifying if the connection is closed or not."""
        return self._closed

    def commit(self):
        """Commits pending database changes.

        You need to use :attr:`autocommit` mode.
        """

        self._client.commit(self._id)  # call added commit in avatica
        # TODO can support be added for this?
        if self._closed:
            raise ProgrammingError('the connection is already closed')

    def rollback(self):
        """Rollbacks pending database changes.
        """

        self._client.rollback(self._id)  # call added rollback in avatica
        # TODO can support be added for this?
        if self._closed:
            raise ProgrammingError('the connection is already closed')

    def cursor(self, cursor_factory=None):
        """Creates a new cursor.

        :param cursor_factory:
            This argument can be used to create non-standard cursors.
            The class returned must be a subclass of
            :class:`~phoenixdb.cursor.Cursor` (for example :class:`~phoenixdb.cursor.DictCursor`).
            A default factory for the connection can also be specified using the
            :attr:`cursor_factory` attribute.

        :returns:
            A :class:`~phoenixdb.cursor.Cursor` object.
        """
        if self._closed:
            raise ProgrammingError('the connection is already closed')
        cursor = (cursor_factory or self.cursor_factory)(self)
        self._cursors.append(weakref.ref(cursor, self._cursors.remove))
        return cursor

    def set_session(self, autocommit=None, readonly=None):
        """Sets one or more parameters in the current connection.

        :param autocommit:
            Switch the connection to autocommit mode. With the current
            version, you need to always enable this, because
            :meth:`commit` is not implemented.

        :param readonly:
            Switch the connection to read-only mode.
        """
        props = {}
        if autocommit is not None:
            props['autoCommit'] = bool(autocommit)
        if readonly is not None:
            props['readOnly'] = bool(readonly)

        props = self._client.connection_sync(self._id, props)
        self._autocommit = props.auto_commit
        self._readonly = props.read_only
        self._transactionisolation = props.transaction_isolation

    @property
    def autocommit(self):
        """Read/write attribute for switching the connection's autocommit mode."""
        return self._autocommit

    @autocommit.setter
    def autocommit(self, value):
        if self._closed:
            raise ProgrammingError('the connection is already closed')
        props = self._client.connection_sync(self._id, {'autoCommit': bool(value)})
        self._autocommit = props.auto_commit

    def set_autocommit(self, value):
        if self._closed:
            raise ProgrammingError('the connection is already closed')
        props = self._client.connection_sync(self._id, {'autoCommit': bool(value)})
        self._autocommit = props.auto_commit

    @property
    def readonly(self):
        """Read/write attribute for switching the connection's readonly mode."""
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        if self._closed:
            raise ProgrammingError('the connection is already closed')
        props = self._client.connectionSync(self._id, {'readOnly': bool(value)})
        self._readonly = props.read_only

    @property
    def transactionisolation(self):
        return self._transactionisolation

    @transactionisolation.setter
    def transactionisolation(self, value):
        if self._closed:
            raise ProgrammingError('the connection is already closed')
        props = self._client.connectionSync(self._id, {'transactionIsolation': bool(value)})
        self._transactionisolation = props.transaction_isolation

    @property
    def url(self):
        return self._client.url

    def serve_lx_action(self, action, params=None):
        return self._client.serve_lx_action(action, params)


for name in errorsOld.__all__:
    setattr(Connection, name, getattr(errorsOld, name))
