import json
import logging
import pathlib

import shutil

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass, asdict, field
from tqdm import tqdm
from typing import Dict, List, Optional

from watchtower_pipeline import models, ffprobe


@dataclass
class ProjectListWriter:
    projects: List[models.ProjectListItem]
    destination_path: pathlib.Path

    def to_dict(self):
        return {
            'projects': [asdict(p) for p in self.projects],
        }

    def download_previews(
        self, requests_headers: Optional[Dict] = None, force=False, display_progress=True
    ):
        # Set a variable that semantically matches tqdm API (the inverse of what we want our API to do)
        disable_progress = not display_progress
        for p in tqdm(
            self.projects,
            desc="Downloading Project thumbnails",
            disable=disable_progress,
            ascii=' >=',
        ):
            path = pathlib.Path('projects-list') / 'previews'
            p.download_and_assign_thumbnail(
                self.destination_path,
                path=path,
                requests_headers=requests_headers,
                force=force,
            )

    def write_as_json(self):
        dst = self.destination_path / 'data/projects-list/index.json'
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, 'w') as outfile:
            json.dump(self.to_dict(), outfile, indent=2)


class AbstractProjectListWriter(ABC):
    @abstractmethod
    def get_project_list(self) -> List[models.ProjectListItem]:
        pass

    def _get_project_list_writer(self, destination_path: pathlib.Path) -> ProjectListWriter:
        return ProjectListWriter(
            projects=self.get_project_list(),
            destination_path=destination_path,
        )


@dataclass
class ProjectWriter:
    """Saves a project and all its data as JSON files."""

    project: models.Project
    shots: List[models.Shot]
    assets: List[models.Asset]
    sequences: List[models.Sequence]
    edits: List[models.Edit]
    casting: List[models.ShotCasting]
    destination_path: pathlib.Path
    # task_counts: Optional[List[models.TaskCount]] = None
    task_counts: Optional[List] = None

    def dump_data(self, name, data):
        dst = self.destination_path / f"data/projects/{self.project.id}/{name}.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        logging.debug(f"Saved {name} data for project {self.project.id}")

    @staticmethod
    def count_tasks(entities_list, timestamp):
        """Given a structured entities_list, count tasks.

        An example for the structure can be found in the unit tests.
        """
        task_type_status_dict = defaultdict(lambda: defaultdict(list))

        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        for entity in entities_list:
            episode_id = entity.get('episode_id')
            for task in entity.get('tasks', []):
                task_type_id = task.get('task_type_id')
                task_status_id = task.get('task_status_id')

                if task_type_id and task_status_id:
                    # If we already encountered this task type in this status, increment the count
                    if task_status_id in task_type_status_dict[(task_type_id, episode_id)]:
                        task_type_status_dict[(task_type_id, episode_id)][task_status_id][0][
                            'count'
                        ] += 1
                    # Otherwise, add it for the first time
                    else:
                        task_type_status_dict[(task_type_id, episode_id)][task_status_id].append(
                            {'timestamp': timestamp, 'count': 1}
                        )

        parsed_data = []
        for (task_type_id, episode_id), status_dict in task_type_status_dict.items():
            task_statuses = [
                {
                    'task_status_id': status_id,
                    'data': [{'timestamp': ts['timestamp'], 'count': ts['count']} for ts in tasks],
                }
                for status_id, tasks in status_dict.items()
            ]
            parsed_data.append(
                {
                    'task_type_id': task_type_id,
                    'episode_id': episode_id,
                    'task_statuses': task_statuses,
                }
            )

        return parsed_data

    @staticmethod
    def _merge_task_count_dicts(initial, update) -> list:
        # Convert initial to a dictionary for easier lookup
        initial_dict = {}
        for entry in initial:
            key = (entry['task_type_id'], entry['episode_id'])
            initial_dict[key] = entry

        # Process each update
        for update_entry in update:
            key = (update_entry['task_type_id'], update_entry['episode_id'])

            if key in initial_dict:
                # Entry exists in initial, so update it
                initial_task_statuses = initial_dict[key]['task_statuses']
                update_task_statuses = update_entry['task_statuses']

                # Convert task_counts in initial to a dictionary for easier lookup
                task_status_dict = {
                    task_status['task_status_id']: task_status
                    for task_status in initial_task_statuses
                }

                for update_task_status in update_task_statuses:
                    status_id = update_task_status['task_status_id']
                    if status_id in task_status_dict:
                        # If status_id exists, append the new data
                        task_status_dict[status_id]['data'].extend(update_task_status['data'])
                    else:
                        # If status_id does not exist, add the new task_count
                        task_status_dict[status_id] = update_task_status

                # Convert the task_counts dictionary back to a list
                initial_dict[key]['task_statuses'] = list(task_status_dict.values())
            else:
                # Entry does not exist in initial, so add it
                initial_dict[key] = update_entry

        # Convert initial_dict back to the list format
        return list(initial_dict.values())

    def merge_task_counts(self, new_counts):
        # Create a dictionary for existing task counts based on task_status_id
        existing_counts_src = (
            self.destination_path / f"data/projects/{self.project.id}/task_counts.json"
        )
        if existing_counts_src.is_file():
            existing_counts = json.loads(existing_counts_src.read_text())
        else:
            existing_counts = {}

        self.task_counts = self._merge_task_count_dicts(existing_counts, new_counts)

    def download_previews(self, requests_headers: Optional[Dict] = None, force=False):
        path = pathlib.Path('projects') / self.project.id / 'previews'
        for s in tqdm(self.shots, desc="Downloading Shot thumbnails", ascii=' >='):
            s.download_and_assign_thumbnail(
                self.destination_path,
                path=path,
                requests_headers=requests_headers,
                force=force,
            )
        for a in tqdm(self.assets, desc="Downloading Asset thumbnails", ascii=' >='):
            a.download_and_assign_thumbnail(
                self.destination_path,
                path=path,
                requests_headers=requests_headers,
                force=force,
            )
        for user in tqdm(self.project.team, desc="Downloading User thumbnails", ascii=' >='):
            user.download_and_assign_thumbnail(
                self.destination_path,
                path=path,
                requests_headers=requests_headers,
                force=force,
            )

    def download_edits(self, requests_headers: Optional[Dict] = None, force=False):
        for edit in self.edits:
            in_project_path = f"data/projects/{self.project.id}/edit-{edit.id}.mp4"
            dst = self.destination_path / in_project_path
            models.fetch_and_save_media(
                edit.sourceName,
                requests_headers,
                dst,
                force=force,
                display_progress=True,
            )
            edit.sourceName = str(in_project_path)
            edit.totalFrames = ffprobe.get_frames_count(dst)

    def write_as_json(self):
        self.dump_data('project', asdict(self.project))
        self.dump_data('edits', [e.to_dict() for e in self.edits])
        self.dump_data('assets', [asdict(a) for a in self.assets])
        self.dump_data('shots', [asdict(s) for s in self.shots])
        self.dump_data('sequences', [asdict(s) for s in self.sequences])
        self.dump_data('casting', [c.to_dict() for c in self.casting])
        self.dump_data('task_counts', self.task_counts or [])


class AbstractProjectWriter(ABC):
    @abstractmethod
    def get_project(self, project_id) -> models.Project:
        pass

    @abstractmethod
    def get_project_shots(self, project: models.Project) -> List[models.Shot]:
        pass

    @abstractmethod
    def get_project_assets(self, project: models.Project) -> List[models.Asset]:
        pass

    @abstractmethod
    def get_project_sequences(self, project: models.Project) -> List[models.Sequence]:
        pass

    @abstractmethod
    def get_task_count(self, project_id):
        pass

    @abstractmethod
    def get_project_casting(
        self,
        project,
        sequences: List[models.Sequence],
        shots: List[models.Shot],
        assets: List[models.Asset],
    ) -> List[models.ShotCasting]:
        pass

    @abstractmethod
    def get_project_edits(self, project: models.Project) -> List[models.Edit]:
        pass

    def _get_project_writer(self, project_id, destination_path: pathlib.Path):
        project = self.get_project(project_id)
        sequences = self.get_project_sequences(project)
        shots = self.get_project_shots(project)
        assets = self.get_project_assets(project)
        casting = self.get_project_casting(project, sequences, shots, assets)
        edits = self.get_project_edits(project)

        return ProjectWriter(
            project=project,
            shots=shots,
            assets=assets,
            sequences=sequences,
            edits=edits,
            casting=casting,
            destination_path=destination_path,
        )


class AbstractWriter(AbstractProjectListWriter, AbstractProjectWriter, ABC):
    @property
    @abstractmethod
    def request_headers(self) -> Optional[Dict]:
        pass

    def write_project(self, project_id, destination_path: pathlib.Path):
        project_writer = self._get_project_writer(project_id, destination_path)
        project_writer.download_previews(self.request_headers)
        project_writer.download_edits(self.request_headers)
        current_task_count = self.get_task_count(project_id)
        project_writer.merge_task_counts(current_task_count)
        project_writer.write_as_json()

    def write_all(self, destination_path: pathlib.Path):
        project_list_writer = self._get_project_list_writer(destination_path)
        project_list_writer.download_previews(self.request_headers)
        project_list_writer.write_as_json()
        for p in project_list_writer.projects:
            self.write_project(p.id, destination_path)


@dataclass
class WatchtowerBundler:
    @staticmethod
    def bundle(destination_path: pathlib.Path):
        """Combine the embedded dist_client_web with the static_path content.

        - copy the content dist_client_web into destination_path
        - copy the content of destination_path / 'data'  into destination_path
        - delete destination_path / 'data'
        """
        dist_client_web_src = pathlib.Path(__file__).parent.parent / 'dist_client_web'
        dist_client_web_dst = destination_path / 'watchtower'
        shutil.copytree(dist_client_web_src, dist_client_web_dst, dirs_exist_ok=True)
        shutil.copytree(destination_path / 'data', dist_client_web_dst / 'data', dirs_exist_ok=True)
        shutil.rmtree(destination_path / 'data')
        logging.info(f"Watchtower bundle ready at {dist_client_web_dst}")
        logging.info(f"You can preview it with the following command:")
        logging.info(f"\tpython -m http.server --directory {dist_client_web_dst}")
