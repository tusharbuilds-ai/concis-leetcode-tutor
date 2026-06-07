# import asyncio
# import time
# from core.LogManager import log

# from services.service_in_memory.inmemory import redis_con
# from services.service_agent.agent import root_agent
# from managers.websocket_manager.websocket_manager import websock_manager

# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService

# from google.genai import types


# APP_NAME = "service_agent"

# session_service = InMemorySessionService()

# runner = Runner(
#     agent=root_agent,
#     app_name=APP_NAME,
#     session_service=session_service
# )


# async def ensure_session(session_id: str):

#     try:

#         session = await session_service.get_session(
#             app_name=APP_NAME,
#             user_id=session_id,
#             session_id=session_id
#         )

#         if session:
#             return

#     except Exception:
#         pass

#     # log.debug(
#     #     f"Creating ADK Session -> {session_id}"
#     # )

#     await session_service.create_session(
#         app_name=APP_NAME,
#         user_id=session_id,
#         session_id=session_id
#     )


# async def call_agent(
#     session_id: str,
#     user_message: str
# ):

#     await ensure_session(session_id)

#     content = types.Content(
#         role="user",
#         parts=[
#             types.Part(
#                 text=user_message
#             )
#         ]
#     )

#     final_response = ""

#     async for event in runner.run_async(
#         user_id=session_id,
#         session_id=session_id,
#         new_message=content
#     ):

#         if not event.content:
#             continue

#         if not event.content.parts:
#             continue

#         if event.is_final_response():

#             text = getattr(
#                 event.content.parts[0],
#                 "text",
#                 None
#             )

#             if text:
#                 final_response = text

#     return final_response


# async def process_job(payload):
#     start_time = time.perf_counter()
#     session_id = payload["session_id"]
#     context = f"""
# Problem:
# {payload['question']}

# User Query:
# {payload['query']}
# """
 

#     response = await call_agent(
#         session_id=session_id,
#         user_message=context
#     )

#     llm_time = time.perf_counter() - start_time
#     log.info(f"LLM Processing time -> {llm_time}")



#     # log.debug(
#     #     f"Agent Response -> {response}"
#     # )
    
#     publish_start = time.perf_counter()

#     redis_con.publish_agent_response(
#         session_id,
#         response
#     )

#     publish_time = time.perf_counter() - publish_start

#     log.info(f"Redis publish time -> {publish_time:.4f}s")

#     total_time = time.perf_counter() - start_time

#     log.info(f"Total job time -> {total_time:.2f}s")

# async def worker_loop():

#     while True:

#         try:

#             payload = (
#                 redis_con.pull_for_agent_work_queue()
#             )

#             if not payload:

#                 await asyncio.sleep(1)
#                 continue

#             # log.debug(
#             #     f"Fetched Payload -> {payload}"
#             # )

#             await process_job(payload)

#         except Exception as ex:

#             log.exception(
#                 f"Worker Failed -> {ex}"
#             )

#             await asyncio.sleep(1)


# if __name__ == "__main__":

#     asyncio.run(
#         worker_loop()
#     )




import asyncio
import time

from core.LogManager import log

from services.service_in_memory.inmemory import redis_con
from services.service_agent.agent import root_agent
from managers.websocket_manager.websocket_manager import websock_manager

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.genai import types


APP_NAME = "service_agent"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# ==========================
# Worker Metrics
# ==========================

WORKER_START_TIME = time.perf_counter()
JOBS_PROCESSED = 0
TOTAL_JOB_TIME = 0.0

# ==========================


async def ensure_session(session_id: str):

    try:

        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=session_id,
            session_id=session_id
        )

        if session:
            return

    except Exception:
        pass

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=session_id,
        session_id=session_id
    )


async def call_agent(
    session_id: str,
    user_message: str
):

    await ensure_session(session_id)

    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=user_message
            )
        ]
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=session_id,
        session_id=session_id,
        new_message=content
    ):

        if not event.content:
            continue

        if not event.content.parts:
            continue

        if event.is_final_response():

            text = getattr(
                event.content.parts[0],
                "text",
                None
            )

            if text:
                final_response = text

    return final_response


async def process_job(payload):

    global JOBS_PROCESSED
    global TOTAL_JOB_TIME

    job_start = time.perf_counter()

    session_id = payload["session_id"]

    # ==========================
    # Queue Wait Time
    # ==========================

    if payload.get("created_at"):

        queue_wait = (
            time.time()
            - payload["created_at"]
        )

        log.info(
            f"Queue Wait Time -> "
            f"{queue_wait:.2f}s"
        )

    # ==========================

    context = f"""
Problem:
{payload['question']}

User Query:
{payload['query']}
"""

    llm_start = time.perf_counter()

    response = await call_agent(
        session_id=session_id,
        user_message=context
    )

    llm_time = (
        time.perf_counter()
        - llm_start
    )

    log.info(
        f"LLM Processing Time -> "
        f"{llm_time:.2f}s"
    )

    publish_start = time.perf_counter()

    redis_con.publish_agent_response(
        session_id,
        response
    )

    publish_time = (
        time.perf_counter()
        - publish_start
    )

    log.info(
        f"Redis Publish Time -> "
        f"{publish_time:.4f}s"
    )

    total_job_time = (
        time.perf_counter()
        - job_start
    )

    log.info(
        f"Total Job Time -> "
        f"{total_job_time:.2f}s"
    )

    # ==========================
    # Worker Metrics
    # ==========================

    JOBS_PROCESSED += 1
    TOTAL_JOB_TIME += total_job_time

    worker_uptime = (
        time.perf_counter()
        - WORKER_START_TIME
    )

    avg_job_time = (
        TOTAL_JOB_TIME
        / JOBS_PROCESSED
    )

    log.info(
        f"Worker Stats | "
        f"Jobs={JOBS_PROCESSED} | "
        f"Uptime={worker_uptime:.2f}s | "
        f"AvgJobTime={avg_job_time:.2f}s"
    )

    # ==========================


async def worker_loop():

    log.info(
        "Agent Worker Started"
    )

    while True:

        try:

            payload = (
                redis_con.pull_for_agent_work_queue()
            )

            if not payload:

                await asyncio.sleep(1)
                continue

            await process_job(payload)

        except Exception as ex:

            log.exception(
                f"Worker Failed -> {ex}"
            )

            await asyncio.sleep(1)


if __name__ == "__main__":

    asyncio.run(
        worker_loop()
    )