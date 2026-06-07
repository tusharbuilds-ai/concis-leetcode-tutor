import asyncio
import uuid
import random
import time

import aiohttp


# ==========================
# CONFIG
# ==========================

API_URL = "http://localhost:8000/api/chat"

TEST_USERS = 1000  # 10, 50, 100, 500, 1000

PROBLEM = """
Given an array nums and a target value,
return indices of the two numbers that add up to target.
"""

QUERIES = [
    "Explain the problem in simple terms.",
    "Give me a hint without solving it.",
    "What is the optimal approach?"
]


# ==========================
# USER SIMULATION
# ==========================

async def simulate_user(session, user_number):
    email = f"user_{user_number}_{random.randint(1,999999)}@test.com"
    session_id = str(uuid.uuid4())

    for query in QUERIES:

        payload = {
            "email": email,
            "session_id": session_id,
            "question": PROBLEM,
            "query": query,
            "context": None
        }

        try:
            start = time.perf_counter()

            async with session.post(
                API_URL,
                json=payload,
                timeout=60
            ) as response:

                latency = time.perf_counter() - start

                print(
                    f"[USER {user_number}] "
                    f"Status={response.status} "
                    f"Latency={latency:.2f}s"
                )

        except Exception as e:
            print(f"[USER {user_number}] ERROR -> {e}")


# ==========================
# MAIN
# ==========================

async def main():

    start = time.perf_counter()

    connector = aiohttp.TCPConnector(limit=0)

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = [
            simulate_user(session, i)
            for i in range(TEST_USERS)
        ]

        await asyncio.gather(*tasks)

    total_time = time.perf_counter() - start

    print("\n====================")
    print("LOAD TEST COMPLETE")
    print("====================")
    print(f"Users: {TEST_USERS}")
    print(f"Messages: {TEST_USERS * 3}")
    print(f"Total Time: {total_time:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())