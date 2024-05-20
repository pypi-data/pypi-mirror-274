from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection, register_class, register_method
from orbit_database import SerialiserType
from datetime import datetime
from loguru import logger as log


class UsersTable (BaseTable):

    norm_table_name = 'users'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [{
        'index_name': 'by_group',
        'duplicates': True,
        # 'force': True,
        'func': """def func(doc): return [g.encode() for g in doc.get("groups", []) if g]"""
    }]

    @property
    def last_seen (self):
        return datetime.utcfromtimestamp(self._when).strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def code (self):
        return self._code if self._code else "Activated"


@register_class
class UsersCollection (BaseCollection):

    table_class = UsersTable
    table_strip = ['user_id', 'code']
    table_methods = ['get_ids']
    
    @register_method
    def get_own_details (cls, session, params, transaction=None):
        doc = UsersTable().from_key(params.get('hostid'))
        if doc.isValid:
            ids, data = [], []
            session.append(params, doc.key, ids, data, doc, strip=cls.table_strip)
            session.update(ids, params)
            return {'ok': True, 'ids': ids, 'data': data}
        return {'ok': False, 'error': f'unable to find specified hostid: {params.get("hostid")}'}
    
