import hvac
client = hvac.Client(
    url='http://10.233.90.78:8200/',
    token='aiphohTaa0eeHei'
)
client.is_authenticated()

# Пишем секрет
secret_rs= client.secrets.kv.v2.create_or_update_secret(
    path='my_secret',
    secret=dict(netology='My own secret!!!'),
)
print('Secret response of write secret: ',secret_rs)

# Читаем секрет
secret_rs2 = client.secrets.kv.v2.read_secret_version(
    path='my_secret',
)
print('Secret responce of read secret:',secret_rs2)

Скриншот из интерфейса
![screenshot](1.png)