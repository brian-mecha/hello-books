from flask import Flask

app = Flask('__name__')
app.url_map.strict_slashes = False

app.config['SECRET_KEY'] = '\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
app.config['BCRYPT_LOG_ROUNDS'] = 15
app.config['JWT_SECRET_KEY'] = '\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
