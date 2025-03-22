import asyncio
from datetime import timedelta
import itertools
from dataclasses import dataclass

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class ActivityInput:
    name: str
    month: int

@activity.defn
async def bill_customer(vals: ActivityInput):
    print(f'billing {vals.name} for month {vals.month}')


@workflow.defn
class MonthlyCharge:

    @workflow.run
    async def run(self, customer_name: str):

        for month in itertools.count(1):
            await workflow.execute_activity(
                bill_customer,
                ActivityInput(month=month, name=customer_name),
                start_to_close_timeout=timedelta(seconds=5),
            )
            await asyncio.sleep(4)


async def main():

    client = await Client.connect("localhost:7233")

    await Worker(
        client,
        task_queue="monthly-charge-task-queue",
        workflows=[MonthlyCharge],
        activities=[bill_customer],
    ).run()


if __name__ == "__main__":
    asyncio.run(main())
