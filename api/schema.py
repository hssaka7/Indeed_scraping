from tortoise.models import Model
from tortoise import fields, run_async, Tortoise 
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

class Feed(Model):
    id = fields.IntField(pk=True, index= True)
    name = fields.CharField(max_length=20)
    description = fields.CharField(max_length=100)
    frequency = fields.CharField(max_length=10)

    workers: fields.ReverseRelation["Worker"]
   

class Worker(Model):
    id = fields.CharField(pk=True,max_length=50, index =True)
    status = fields.CharField(max_length=20)
    # created_by = fields.CharField(max_length=20)
    # created_at = fields.DatetimeField()
    
    feed: fields.ForeignKeyRelation["Feed"]= fields.ForeignKeyField(
        "models.Feed", related_name="workers", description="The feed under which workers are running "
    )
    results: fields.ReverseRelation["Result"]

    # results: fields.ManyToManyRelation["Result"] = fields.ManyToManyField(
    #     "models.Result", related_name="workers", through="worker_result"
    # )


class Result(Model):
    id = fields.IntField(pk=True,index =True)
    job_id = fields.CharField(max_length=50)
    key_name = fields.CharField(max_length=50)
    value = fields.CharField(max_length=200)
    worker: fields.ForeignKeyRelation["Worker"] = fields.ForeignKeyField(
        "models.Worker", related_name="results", description="The results saved by the workers"
    )

Feed_Pydantic = pydantic_model_creator(Feed)
Worker_Pydantic = pydantic_model_creator(Worker)
Result_Pydantic = pydantic_model_creator(Result)

Feed_Pydantic_List= pydantic_queryset_creator(Feed)
Worker_Pydantic_List = pydantic_queryset_creator(Worker)
Result_Pydantic_List = pydantic_queryset_creator(Result)

async def connectToDatabase():
    await Tortoise.init(
        db_url='sqlite://scrapers.db',
        modules={'models': ['__main__']}
    )
    
    # Uncomment this to initialize db. 
    # await Tortoise.generate_schemas()
    

if __name__ == "__main__":
    run_async(connectToDatabase())