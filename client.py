"""Grant, this is just the client code"""

import asyncio
from temporalio.client import Client

from worker import (
    MonthlyCharge
)

async def main():

    client = await Client.connect("localhost:7233")

    await client.execute_workflow(
        MonthlyCharge.run,
        id="hello-activity-choice-workflow-id-2",
        task_queue="hello-activity-choice-task-queue",
    )


if __name__ == "__main__":
    asyncio.run(main())
