import json
import re
from datetime import datetime
import redis
from ldap3 import ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES

import locale


from functions import functions
from models.OrgUnit import OrgUnit

try:
    r = redis.Redis('10.40.0.11')
except redis.ConnectionError:
    print("no redis - start fail")
    exit(2)

class User(object):
    def __init__(self, userdata, renew=False):
        self.renew = renew
        self.dn = str(userdata.distinguishedName)
        self.login = str(userdata.sAMAccountName)

        try:
            self.firstname = str(userdata.givenName)
        except:
            self.firstname = ''

        try:
            self.lastname = str(userdata.sn)
        except:
            self.lastname = ''

        try:
            self.middlename = str(userdata.patronymic)
        except:
            self.middlename = ''

        try:
            self.mobile = str(userdata.mobile)
        except:
            self.mobile = ''

        try:
            self.description = str(userdata.description)
        except:
            self.description = ''

        try:
            self.mail = str(userdata.mail)
        except:
            self.mail = ''

        try:
            self.phone = str(userdata.telephoneNumber)
        except:
            self.phone = ''

        try:
            self.photo = str(userdata.photo)
        except:
            self.photo = ''

        try:
            self.admin_description = json.loads(str(userdata.adminDescription))
        except:
            self.admin_description = json.loads('{}')

        try:
            locale.setlocale(locale.LC_TIME, "ru_RU")
            birthday = str(self.admin_description["birthday"])
            datetime_object = datetime.strptime(birthday, '%d.%m')
            self.birthday = datetime_object.strftime("%B, %d")
        except (ValueError, KeyError, TypeError):
            self.birthday = ''

    @property
    def tags(self):
        try:
            user_tags = (self.admin_description["tags"] + ',').split(",")
            while '' in user_tags:
                user_tags.remove('')
        except (ValueError, KeyError, TypeError):
            user_tags = []

        org_unit = OrgUnit.find(self.department)

        unit_tags = org_unit.tags

        return sorted([self.department] + unit_tags + user_tags)

    @property
    def department(self):
        result = re.search(r'OU=(?P<department>.*),OU', self.dn)

        if result:
            return str(result.group('department'))

        return 'n/a'

    @property
    def json(self):

        if r.exists(self.login) and not self.renew:
            json_str = r.get(self.login).decode().replace("\'", "\"")
            user_json = json.loads(json_str)
            user_json['cached'] = True
            return user_json
        else:
            user_json = {
                # "cn": str(self.cn),
                "login": self.login,
                "lastname": self.lastname,
                "firstname": self.firstname,
                "middlename": self.middlename,
                "mail": self.mail,
                "description": self.description,
                "birthday": self.birthday,
                "mobile": self.mobile,
                "phone": self.phone,
                # "photo": str(self.photo),
                "tags": self.tags,
                "dn": self.dn,
                "department": self.department
            }
            r.mset({self.login: str(user_json)})
            user_json['cached'] = False
            return user_json

    @staticmethod
    def find(name=False, renew=False):
        basedn = "ou=x,dc=xxx,dc=ru"
        conn = functions.ad_connect()
        if not name:
            filter = "(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(cn=*)(mail=*))"

            res = conn.search(basedn, filter,
                              attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

            if not res:
                return False

            users = []

            for userdata in conn.entries:
                user = User(userdata,renew)
                users.append(user.json)

            result = sorted(users, key=lambda item: item['lastname'])

        else:
            filter = "(&(objectClass=user)(|(sAMAccountName={})(sn={})))".format(name, name)
            res = conn.search(basedn, filter,
                              attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

            if not res:
                return False

            userdata = conn.entries[0]

            result = User(userdata, renew).json

        functions.ad_disconnect(conn)
        return result
