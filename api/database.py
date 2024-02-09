from tortoise.models import Model
from tortoise import fields, run_async, Tortoise


class Result(Model):
    job_id = fields.CharField(max_length=50)
    worker_id = fields.CharField(max_length=50)
    key_name = fields.CharField(max_length=50)
    value = fields.CharField(max_length=50)

    class Meta:
        table = 'result'

class Worker(Model):
    id = fields.CharField(pk=True,max_length=50, index =True)
    feed_id = fields.IntField(null=False)
    status = fields.CharField(max_length=20)
    created_by = fields.DatetimeField()
    created_at = fields.DatetimeField()

    class Meta:
        table = 'worker'

class Feed(Model):
    id = fields.IntField(pk=True, index= True)
    name = fields.CharField(max_length=20)
    description = fields.CharField(max_length=100)
    frequency = fields.CharField(max_length=10)
    
    class Meta:
        table = 'feed'

async def run():
    await Tortoise.init(db_url='sqlite://scrapers.db', modules= {'models': ["__main__"]})
    
    from pprint import pprint
    pprint(await Feed.all().values('id', 'name', 'description'))
    pprint(await Worker.all().values('id','feed_id', 'status', 'created_at','created_by'))
    pprint(await Result.all().values('job_id', 'key_name', 'value'))


if __name__ == "__main__":
    run_async(run())