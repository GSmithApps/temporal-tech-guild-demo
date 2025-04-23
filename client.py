"""
You can use this if you want,
or you can use the CLI as written in
the README.
"""

import asyncio
from uuid import uuid4
from temporalio.client import Client

from worker import (
    MonthlyCharge
)

async def main():

    client = await Client.connect("localhost:7233")

    await client.start_workflow(
        MonthlyCharge.run,
        id=f"monthly-charge-workflow-{uuid4()}",
        task_queue="monthly-charge-task-queue",
    )

if __name__ == "__main__":
    asyncio.run(main())
