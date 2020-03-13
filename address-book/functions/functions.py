from ldap3 import Server, Connection, ALL, NTLM


def ad_connect():
    ldap_url = "ldap://10.0.0.1"
    password = "aaa"
    domain = 'xxx.ru'
    username = 'ldapadmin'

    server = Server(ldap_url, get_info=ALL)
    return Connection(server,
                      user='{}\\{}'.format(domain, username),
                      password=password,
                      authentication=NTLM, auto_bind=True)


def ad_disconnect(conn):
    conn.unbind()


