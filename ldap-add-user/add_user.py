#!/usr/bin/env python

# import needed modules
import ldap
import ldap.modlist as modlist
import hashlib, os, sys
from base64 import standard_b64encode

baseDN = "dc=xxx,dc=ru"

uid = sys.argv[1]
firstname = sys.argv[2]
lastname = sys.argv[3]
userPassword = sys.argv[4]

class User(object):
    def __init__(self, uid, firstname, lastname, userPassword):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.userPassword = userPassword

    @property
    def uidNumber(self):
        return findMaxUid(conn, baseDN) + 1

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    @property
    def mail(self):
        return f'{self.uid}@xxx.ru'

    @property
    def passwordHash(self):
        salt = os.urandom(4)
        h = hashlib.sha1(self.userPassword.encode('utf-8'))
        # h.update(salt)

        return b"{SHA}" + standard_b64encode(h.digest())


def addUser(user, conn, baseDN):
    # # The dn of our new entry/object
    dn = "uid=" + str(user.uid) + ",ou=users," + baseDN
    #
    # # A dict to help build the "body" of the object
    attrs = {}
    attrs['objectclass'] = [b'top', b'inetOrgPerson', b'posixAccount']
    attrs['cn'] = user.fullname.encode('utf-8')
    attrs['sn'] = user.lastname.encode('utf-8')
    attrs['givenname'] = user.firstname.encode('utf-8')
    attrs['displayname'] = attrs['cn']
    attrs['uid'] = user.uid.encode('utf-8')
    attrs['uidNumber'] = str(user.uidNumber).encode('utf-8')
    attrs['gidNumber'] = b'0'
    attrs['description'] = b''
    attrs['homeDirectory'] = b'none'
    attrs['loginShell'] = b'true'
    attrs['userPassword'] = user.passwordHash

    attrs['mail'] = user.mail.encode('utf-8')

    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
    #
    # # Do the actual synchronous add-operation to the ldapserver


    print(userPassword.encode('utf-16-le'))
    print(ldif)

    try:
        conn.add_s(dn,ldif)
        print("Done")
    except ldap.ALREADY_EXISTS:
        print("Already exist")

def findMaxUid(conn, baseDN):
    # searchScope = conn.SCOPE_SUBTREE
    # retrieveAttributes = None
    retrieveAttributes = {'uidNumber'}
    searchFilter = "uid=*"

    uids = []
    try:
        ldap_result_id = conn.search(baseDN, ldap.SCOPE_SUBTREE, searchFilter, retrieveAttributes, attrsonly=0)
        while 1:
            result_type, result_data = conn.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    uids.append(result_data[0][1]['uidNumber'][0])
    except ldap.LDAPError:
            print("authentication error")

    uids.sort()
    return int(max(uids).decode("utf-8"))

    # Its nice to the server to disconnect and free resources when done

if __name__ == "__main__":
    # Open a connection
    conn = ldap.initialize("ldap://192.168.21.1:389/")

    # Bind/authenticate with a user with apropriate rights to add objects
    conn.simple_bind_s("cn=admin," + baseDN, "3admin")

    uidNumber = findMaxUid(conn, baseDN) + 1

    # print(uidNumber)
    # conn.unbind_s()

    user = User(uid,firstname,lastname,userPassword)
    addUser(user, conn, baseDN)