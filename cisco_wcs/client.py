import requests
import pyquery

class LoginFailure(Exception):
    pass

def get_table(html, table_id):
    p = pyquery.PyQuery(html)
    table = p(table_id)[0]
    rows = table.getchildren()
    header = rows[0]
    data = rows[1:]
    col_names = [c.text_content().strip() for c in header.findall("th")]

    ret = []
    for row in data:
        cols = [c.text_content().strip() for c in row.findall("td")]
        ret.append(dict(zip(col_names, cols)))
        
    return ret

class Client:
    def __init__(self, host, username, password):
        self.base = "https://%s/webacs/" % host
        self.username = username
        self.password = password
        self.s = requests.Session(verify=False)
        self.login()

    def login(self):
        data = {'action': 'login', 'username': self.username, 'password': self.password}
        r = self.s.post(self.base + "loginAction.do", data=data)
        r.raise_for_status()
        if 'loginAction.do' in r.text:
            raise LoginFailure()
        return True

    def get_client_detail(self, mac):
        params = {'command': 'detail', 'mobileStationMac': mac}
        r = self.s.get(self.base + "monitorClientDetail.do", params=params)
        return get_table(r.text, "#clientAssoListTable")

    def search_client(self, mac_or_ip_or_name):
        params = {'searchType': 'macOrIpOrName', 'searchText': mac_or_ip_or_name}
        r = self.s.get(self.base + "searchClientAction.do", params=params)
        return get_table(r.text, "#clientFormListTable")
