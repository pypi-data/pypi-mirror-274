import asyncio

from ..staircase_env import StaircaseEnvironment


async def assess(
    ci_env: StaircaseEnvironment, *, source_url: str, verbose: bool = False
):
    response = await ci_env.http_client.async_request(
        f"code-assessor/assessments", method="POST", data={"source_url": source_url}
    )
    response_body = await response.json()
    id_ = response_body["assessment_id"]
    if verbose:
        print(f"Assessment id: {id_}")

    while True:
        response = await ci_env.http_client.async_request(
            f"code-assessor/assessments/{id_}"
        )
        response_body = await response.json()
        status = response_body.get("status")
        print(f"Status of assess: {status}")
        if status in ("IN_PROGRESS", "RUNNING"):
            await asyncio.sleep(10)
        elif status == "FAILED":
            if logs := response_body.get("logs"):
                logs = "".join(logs) if isinstance(logs, list) else logs

            raise Exception(response_body)
        else:
            source_url = response_body["source_url"]
            return source_url
