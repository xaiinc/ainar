import peewee as pw

proxy = pw.Proxy()


class BaseModel(pw.Model):
    class Meta:
        database = proxy
