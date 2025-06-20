#!/usr/bin/python3
import pathlib
import requests
from rich.progress import Progress

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
API_KEY_LOCATION = "~/.hevy_api_key"
API_KEY_URL = "https://hevy.com/settings?developer"


class ApiPaginator:
    def paginate(self, endpoint, params, session):
        with Progress() as progress:
            task = progress.add_task(
                f"[bold]Fetching paginated data from {endpoint}[/bold][green] (Page 1) ...[/green]",
                total=None,
            )
            while True:
                response = session.get(endpoint, params=params)
                jsdata = response.json()
                page_count = jsdata["page_count"]

                # Update the total page count in the progress bar when known
                if progress.tasks[task].total is None:
                    progress.update(task, total=page_count)

                yield from jsdata["workouts"]

                progress.update(
                    task,
                    description=f"[bold]Fetching paginated data from {endpoint}[/bold][green] (Page {params['page']} of {page_count}) ... [/green]",
                )
                progress.advance(task)

                ## Stop fetching if we've hit the last page
                if params["page"] >= page_count:
                    break

                ## More to fetch, so go to next page
                params["page"] += 1


class ApiRequest:
    def __init__(self):
        self.session = requests.Session()
        self.api_key = self.load_api_key()
        self.session.headers.update(
            {"accept": "application/json", "api-key": self.api_key}
        )
        self.default_params = {"page": DEFAULT_PAGE, "pageSize": DEFAULT_PAGE_SIZE}
        self.api_URI = "https://api.hevyapp.com/v1"
        self.endpoints = {
            "workouts": "workouts",
            "workouts_count": "workouts/count",
            "workouts_events": "workouts/events",
            "workout_info": "workouts/{workout_id}",
        }

    def get_endpoint(self, key):
        return f"{self.api_URI}/{self.endpoints.get(key)}"

    def load_api_key(self):
        try:
            with open(pathlib.Path(API_KEY_LOCATION).expanduser()) as key:
                return key.read().strip()
        except FileNotFoundError:
            exit(
                f"You must first add your API key to {API_KEY_LOCATION} - Get it here: {API_KEY_URL}"
            )

    def get_workout_count(self):
        response = self.session.get(self.get_endpoint("workouts_count"))
        if response.status_code == 200:
            return response.json().get("workout_count")
        else:
            return None

    def list_workouts(self):
        paginator = ApiPaginator()
        return [
            workout
            for workout in paginator.paginate(
                self.get_endpoint("workouts"), self.default_params, self.session
            )
        ]
