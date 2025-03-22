"""Grant, put the workflow and activity implementations
here along with the worker start"""

import asyncio
from datetime import timedelta
from typing import List

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

# Activities that will be called by the workflow


@activity.defn
async def bill_customer(month: int):
    print(f'billing customer for month {month}')


# Basic workflow that logs and invokes different activities based on input
@workflow.defn
class MonthlyCharge:
    @workflow.run
    async def run(self):
        # Order each thing on the list
        ordered: List[str] = []
        for month in range(1, 12+1):
            await asyncio.sleep(4)
            await workflow.execute_activity(
                bill_customer,
                month,
                start_to_close_timeout=timedelta(seconds=5),
            )


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    worker = Worker(
        client,
        task_queue="hello-activity-choice-task-queue",
        workflows=[MonthlyCharge],
        activities=[bill_customer],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
