# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 BarraDev Consulting (<http://www.barradev.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
##############################################################################

from openerp import tools
from openerp import http
from openerp.http import OpenERPSession, Root
from openerp.tools.func import lazy_property
from werkzeug.contrib.sessions import SessionStore

try:
    _redis_import = True
    import redis
except:
    _redis_import = False

try:
    import cPickle as pickle
except:
    import pickle

import logging

_logger = logging.getLogger(__name__)

redis_host = tools.config.get('redis_host', 'localhost')
redis_port = int(tools.config.get('redis_port', 6379))
redis_dbindex = int(tools.config.get('redis_dbindex', 1))
redis_password = tools.config.get('redis_pass', None)


class RedisSessionStore(SessionStore):
    def __init__(self, expire=1800, key_prefix='',
                 session_class=OpenERPSession,
                 redis_conn=None):
        super(SessionStore, self).__init__
        if redis_conn is None:
            self.redis_conn = redis.Redis(redis_host,
                                          redis_port,
                                          redis_dbindex,
                                          password=redis_password)
        self.redis = redis_conn
        self.session_class = session_class
        self.expire = expire
        self.key_prefix = key_prefix

    def save(self, session):
        key = self._get_session_key(session.sid)
        data = pickle.dumps(dict(session))
        _logger.debug("Save: %s", key)
        self.redis.setex(key, data, self.expire)

    def delete(self, session):
        key = self._get_session_key(session.sid)
        self.redis.delete(key)

    def _get_session_key(self, sid):
        key = self.key_prefix + sid
        _logger.debug("SessionKey: %s", key)
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        return key

    def get(self, sid):
        key = self._get_session_key(sid)
        data = self.redis.get(key)
        _logger.debug("Get: %s", key)
        if data:
            self.redis.setex(key, data, self.expire)
            data = pickle.loads(data)
        else:
            data = {}
        return self.session_class(data, sid, False)


def fail_redis(self):
    _logger.info('Redis fail, using FileSystemSessionStore for session')


@lazy_property
def session_store(self):
    _logger.debug('Starting HTTP session store with Redis')
    if not _redis_import:
        fail_redis(self)
        return self.org_session_store
    try:
        redis_conn = redis.Redis(redis_host,
                                 redis_port,
                                 redis_dbindex,
                                 password=redis_password)
        redis_conn.get('anything')
        _logger.info("Redis host: {}, port: {}, dbindex: {}"
                     .format(redis_host, redis_port, redis_dbindex))
    except:
        fail_redis(self)
        return self.org_session_store

    return RedisSessionStore(session_class=OpenERPSession,
                             redis_conn=redis_conn)


def redis_session_gc(session_store):
    pass


Root.org_session_store = Root.session_store
Root.session_store = session_store

http.session_gc_org = http.session_gc
http.session_gc = redis_session_gc
