import asyncio
from temporalio.client import Client
import sys

from worker import (
    MonthlyCharge
)

async def main():

    customer_name = sys.argv[1]

    client = await Client.connect("localhost:7233")

    await client.start_workflow(
        MonthlyCharge.run,
        customer_name,
        id=f"monthly-charge-{customer_name}",
        task_queue="monthly-charge-task-queue",
    )

if __name__ == "__main__":
    asyncio.run(main())
