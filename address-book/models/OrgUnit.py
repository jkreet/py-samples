import json
from functools import lru_cache

from ldap3 import ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES

from functions import functions


class OrgUnit(object):
    def __init__(self, data):
        self.dn = str(data.distinguishedName)
        self.name = str(data.ou)

        try:
            self.admin_description = json.loads(str(data.adminDescription))
        except:
            self.admin_description = json.loads('{}')

        try:
            self.manager = str(data.managedBy)
        except:
            self.manager = ''

    @property
    @lru_cache(maxsize=None)
    def tags(self):
        try:
            tags =  (self.admin_description["tags"] + ',').split(",")
            while '' in tags:
                tags.remove('')
            return tags
        except:
            return []

    @property
    def json(self):
        return {
            'dn': str(self.dn),
            'name': self.name,
            'tags': self.tags,
            'manager': self.manager,
        }

    @staticmethod
    def find(name=False):
        basedn = "ou=xxxxx,dc=xxx,dc=ru"
        conn = functions.ad_connect()
        if not name:
            filter = "(&(objectClass=OrganizationalUnit)(!(ou=_*))(!(ou=xxxxx)))"

            res = conn.search(basedn, filter,
                              attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

            if not res:
                return False

            org_units = []

            for data in conn.entries:
                org_unit = OrgUnit(data)
                org_units.append(org_unit.json)

            result =  sorted(org_units, key=lambda item: item['name'])

        else:
            filter = "(&(objectClass=OrganizationalUnit)(ou={}))".format(name)

            res = conn.search(basedn, filter,
                              attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

            if not res:
                return False

            data = conn.entries[0]
            result =  OrgUnit(data)

        functions.ad_disconnect(conn)
        return result