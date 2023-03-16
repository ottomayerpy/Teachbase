from typing import Dict, List, Optional, Union, Callable

import requests


class TeachbaseException(Exception):
    pass


class TeachbaseClient:
    def __init__(self, client_id: str, client_secret: str, base_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.api_endpoint = "endpoint/v1/"
        self.token_data = None
        self.token = None

    @staticmethod
    def _make_requests(method: str, headers, url, json=None, data=None):
        try:
            if method == "GET":
                response = requests.get(url=url, headers=headers)
            elif method == "POST":
                response = requests.post(url=url, headers=headers, json=json, data=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TeachbaseException(str(e))

    @staticmethod
    def _make_user_create_dict(data: dict) -> dict:
        """
        This func create a necessary dict for outer API
        :param data: {
                                        "email": "email_1_2@factory.tb",
                                        "phone": "79217778866",
                                        "password": "qwerty",
                                        "external_id": "string"
                                }
        """
        final_dict = {
            "users": [
                {
                    "email": data.get("email"),
                    "name": "name",
                    "description": "Corrupti natus quia recusandae.",
                    "last_name": "last_name",
                    "password": data.get("password"),
                    "lang": "ru",
                    "phone": data.get("phone"),
                    "role_id": 1,
                    "auth_type": 0,
                    "external_id": data.get("external_id", "0234er"),
                    "labels": {"23": "25"},
                }
            ],
            "external_labels": True,
            "options": {
                "activate": True,
                "verify_emails": True,
                "skip_notify_new_users": True,
                "skip_notify_active_users": True,
            },
        }
        return final_dict

    def authentication(self) -> None:
        path: str = "oauth/token/"
        url = self.base_url + path
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(url, data=data)
        result = response.json()

        self.token_data = result
        self.token = result.get("access_token")

    def is_token_valid(self) -> bool:
        path: str = "_ping"
        url = self.base_url + self.api_endpoint + path
        response = requests.get(
            url=url,
            headers=self.headers,
        )
        return response.status_code == 200

    @staticmethod
    def refresh_token(func: Callable) -> Callable:
        """
        This decorator make authentication and refresh token if necessary
        """

        def wrapper_refresh(self, *args, **kwargs):
            if not self.is_token_valid():
                self.authentication()
            return func(self, *args, **kwargs)

        return wrapper_refresh

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
        }

    @refresh_token
    def get_courses_list(
        self,
        page: int = None,
        per_page: int = None,
        types: Optional[list] = None,
    ) -> List[dict]:
        path: str = "courses/"
        url = self.base_url + self.api_endpoint + path
        if page is not None:
            url += f"?page={page}"

        if per_page is not None:
            url += f"&per_page={per_page}"

        if types is not None:
            for i in range(len(types)):
                url += f"&types%5B%5D={types[i]}"

        response = self._make_requests(
            method="GET",
            url=url,
            headers=self.headers,
        )
        return response

    @refresh_token
    def get_course_detail(self, pk: int = 55894) -> Dict[str, Union[str, int]]:
        path: str = "courses/"
        url = self.base_url + self.api_endpoint + path + f"{pk}"

        response = self._make_requests(
            method="GET",
            url=url,
            headers=self.headers,
        )
        return response

    @refresh_token
    def create_user(self, json: dict) -> Dict[str, Union[str, int, dict]]:
        """
        :param json: {
                                        "email": "email_1_2@factory.tb",
                                        "phone": "+79217778866",
                                        "password": "string",
                                        "external_id": "string"
                                }
        """
        path: str = "users/create"
        url = self.base_url + self.api_endpoint + path
        headers = {
            "Content-Type": "application/json",
        }
        headers.update(self.headers)

        json = self._make_user_create_dict(json)

        response = self._make_requests(
            method="POST",
            json=json,
            url=url,
            headers=headers,
        )
        return response

    @refresh_token
    def register_user_for_session(self, json: dict, session_pk: int = 495682):
        """
        :param json: {
                                        "email": "email_1_2@factory.tb",
                                        "phone": 792177788666,
                                        "external_id": "string"
                                        "user_id": int
                                }
        """

        path = f"course_sessions/{session_pk}/register"
        url = self.base_url + self.api_endpoint + path
        headers = {
            "Content-Type": "application/json",
        }
        headers.update(self.headers)

        response = self._make_requests(
            method="POST",
            json=json,
            url=url,
            headers=headers,
        )
        return response

    @refresh_token
    def get_courses_sessions_list(
        self,
        course_pk: int = 55894,
        session_status: str = "active",
        page: int = None,
        per_page: int = None,
        participant_ids: List[int] = None,
    ):
        path = f"courses/{course_pk}/course_sessions"
        url = self.base_url + self.api_endpoint + path + f"?filter={session_status}"

        if page is not None:
            url += f"&page={page}"

        if per_page is not None:
            url += f"&per_page={per_page}"

        if participant_ids is not None:
            for i in range(len(participant_ids)):
                url += f"&participant_ids%5B%5D={participant_ids[i]}"

        response = self._make_requests(
            method="GET",
            url=url,
            headers=self.headers,
        )
        return response
