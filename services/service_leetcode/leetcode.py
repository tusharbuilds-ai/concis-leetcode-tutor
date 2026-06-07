import requests
import os
from dotenv import load_dotenv

load_dotenv()


class LeetcodeService:

    BASE_URL = (
        os.environ["LEETCODE_API_URL"]
    )

    def get_problems(self):

        response = requests.get(
            self.BASE_URL,
            verify=True
        )

        response.raise_for_status()

        return response.json()


leetcode_service = LeetcodeService()