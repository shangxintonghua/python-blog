import www.orm,asyncio
from www.models import User,Blog,Comment

def example(loop):
    yield from www.orm.create_pool(loop=loop,user='root',password='',db='awesome')
    u=User(name='test',email='ww.ba',passwd='121212',image='about:blank')
    yield from u.save()

loop=asyncio.get_event_loop()
loop.run_until_complete(example(loop))
loop.close()
