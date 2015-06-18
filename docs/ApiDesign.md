
# Api Design


## Resource URL

### Biz Model

This is for orders, products, payment... mgmt.

| HTTP 方法   |  行为          |         示例 |
| ---------- |-------------- |---------------|
| GET      |   获取资源的信息 |    http://tecstack.org/biz/api/v1.0/orders |
| GET      |   获取某个特定资源的信息 | http://tecstack.org/biz/api/v1.0/orders/123 |
| POST     |   创建新资源           |  http://tecstack.org/biz/api/v1.0/orders |
| PUT      |   更新资源             |  http://tecstack.org/biz/api/v1.0/orders/123 |
| DELETE   |   删除资源             |  http://tecstack.org/biz/api/v1.0/orders/123 |

### Crm Model

This is for customer, company, ... mgmt.

| HTTP 方法   |  行为          |         示例 |
| ---------- |-------------- |---------------|
| GET      |   获取资源的信息 |    http://tecstack.org/crm/api/v1.0/customers |
| GET      |   获取某个特定资源的信息 | http://tecstack.org/crm/api/v1.0/customers/123 |
| POST     |   创建新资源           |  http://tecstack.org/crm/api/v1.0/customers |
| PUT      |   更新资源             |  http://tecstack.org/crm/api/v1.0/customers/123 |
| DELETE   |   删除资源             |  http://tecstack.org/crm/api/v1.0/customers/123 |

### ... other Models

TBD.


## Authentication

/auth/api/v1.0/oauth/authorize/facebook
/auth/api/v1.0/oauth/callback/facebook

### OAuth

Flow:
* users grant permission to this site on the provider
* visit home of this site
* redirect to oauth provider's authorization URL
* login@provider
* provider redirect back to callback of this site with auth code
* this site uses the auth code to get user information on provider for reg and login.

Ref:

* [Restful auth Example](http://blog.miguelgrinberg.com/post/restful-authentication-with-flask)
* [Chinese Example](http://www.pythondoc.com/flask-restful/third.html)
* [github rauth](http://www.oschina.net/translate/using-flask-and-rauth-for-github-authentication)
