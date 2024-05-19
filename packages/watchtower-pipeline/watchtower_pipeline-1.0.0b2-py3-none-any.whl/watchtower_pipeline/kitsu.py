#!/usr/bin/env python3
import datetime

import json
import logging
import pathlib
import requests
import sys
from dataclasses import dataclass
from typing import List, Optional, Dict

from watchtower_pipeline import models, writers, ffprobe, argparser

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


@dataclass
class Config:
    """Configuration setup for Kitsu client."""

    dotenv: Optional[str] = '.env.local'
    base_url: Optional[str] = ''
    email: Optional[str] = ''
    password: Optional[str] = ''

    @staticmethod
    def get_env_data_as_dict(path: str) -> dict:
        with open(path, 'r') as f:
            return dict(
                tuple(line.replace('\n', '').split('='))
                for line in f.readlines()
                if not line.startswith('#')
            )

    def __post_init__(self):
        if (self.dotenv and pathlib.Path(self.dotenv).exists()) or pathlib.Path(
            '.env.local'
        ).exists():
            env_vars = self.get_env_data_as_dict(self.dotenv)
            self.base_url = env_vars['KITSU_DATA_SOURCE_URL']
            self.email = env_vars['KITSU_DATA_SOURCE_USER_EMAIL']
            self.password = env_vars['KITSU_DATA_SOURCE_USER_PASSWORD']
        else:
            if not self.base_url or not self.email or not self.password:
                logging.error(
                    "Missing configuration for kitsu Config object."
                    "Please specify base_url, email and password."
                )
                sys.exit(1)


@dataclass
class KitsuClient:
    """Client to query the Kitsu API."""

    config: Config = None
    jwt: str = None

    @property
    def headers(self):
        return {'Authorization': f"Bearer {self.jwt}"}

    @property
    def base_url(self):
        return self.config.base_url

    def get(self, path, params=None):
        return requests.get(
            f"{self.base_url}{path}", params=params, headers=self.headers, allow_redirects=True
        )

    def fetch_jwt(self, email, password) -> str:
        payload = {
            'email': email,
            'password': password,
        }
        r_jwt = requests.post(f"{self.config.base_url}/auth/login", data=payload)
        r_jwt = r_jwt.json()
        if 'error' in r_jwt:
            logging.error(r_jwt['message'])
            exit()
        return r_jwt['access_token']

    def __post_init__(self):
        if not self.config:
            self.config = Config()
        self.jwt = self.fetch_jwt(self.config.email, self.config.password)


class KitsuWriter(writers.AbstractWriter):
    kitsu_client: KitsuClient
    user_context = None

    @property
    def request_headers(self) -> Optional[Dict]:
        return self.kitsu_client.headers

    def get_project_list(self) -> List[models.ProjectListItem]:
        # Project
        projects = []
        for project in self.user_context['projects']:
            episodes = []
            if project['production_type'] == 'tvshow':
                r_episodes = self.kitsu_client.get(f"/data/projects/{project['id']}/episodes")
                for episode in r_episodes.json():
                    episodes.append(
                        models.EpisodeListItem(
                            id=episode['id'],
                            name=episode['name'],
                        )
                    )
            projects.append(
                models.ProjectListItem(
                    id=project['id'],
                    name=project['name'],
                    thumbnailUrl=f"{self.kitsu_client.base_url}/pictures/thumbnails/projects/{project['id']}.png",
                    episodes=episodes,
                )
            )
        return projects

    def get_episodes(self, project):
        # Fetch episodes, if available
        episodes = []
        if project['production_type'] == 'tvshow':
            r_episodes = self.kitsu_client.get(f"/data/projects/{project['id']}/episodes")

            for episode in r_episodes.json():
                sequences = []
                r_sequences = self.kitsu_client.get(
                    f"/data/sequences?project_id={project['id']}&episode_id={episode['id']}"
                )
                for sequence in r_sequences.json():
                    sequences.append(
                        models.Sequence(
                            name=sequence['name'],
                            id=sequence['id'],
                        )
                    )
                episodes.append(
                    models.Episode(
                        sequences=sequences,
                        id=episode['id'],
                        name=episode['name'],
                    )
                )
        return episodes

    def get_project(self, project_id) -> models.Project:
        ctx = self.user_context
        # Get the project from the contex
        project_from_context = next(
            filter(lambda item: item['id'] == project_id, ctx['projects']), None
        )
        # Filter asset_types for project. If the project does not explicitly specify 'asset_types'
        # we use the ones from the context
        if 'asset_types' not in project_from_context:
            filtered_asset_types = ctx['asset_types']
        else:
            filtered_asset_types = [
                item
                for item in ctx['asset_types']
                if item['id'] in project_from_context['asset_types']
            ]

        asset_types = [
            models.AssetType(
                name=item['name'],
                id=item['id'],
            )
            for item in filtered_asset_types
        ]
        # Filter task_types for project. If the project does not explicitly specify 'task_types'
        # we use the ones from the context
        if 'task_types' not in project_from_context:
            filtered_task_types = ctx['task_types']
        else:
            filtered_task_types = [
                item
                for item in ctx['task_types']
                if item['id'] in project_from_context['task_types']
            ]

        task_types = [
            models.TaskType(
                name=item['name'],
                id=item['id'],
                color=item['color'],
                for_shots=item['for_entity'] == 'Shot',
            )
            for item in filtered_task_types
        ]
        # Filter task_statuses for project. If the project does not explicitly specify 'task_statuses'
        # we use the ones from the context
        if 'task_statuses' not in project_from_context:
            filtered_task_statuses = ctx['task_status']  # This is a discrepancy in the Kitsu API
        else:
            filtered_task_statuses = [
                item
                for item in ctx['task_status']
                if item['id'] in project_from_context['task_statuses']
            ]

        task_statuses = [
            models.TaskStatus(
                name=item['name'],
                id=item['id'],
                color=item['color'],
            )
            for item in filtered_task_statuses
        ]
        # Filter users for project
        team = [
            models.User(
                name=item['full_name'],
                id=item['id'],
                thumbnailUrl=f"{self.kitsu_client.base_url}/pictures/thumbnails/persons/{item['id']}.png",
                has_avatar=True,
            )
            for item in ctx['persons']
            if item['id'] in project_from_context['team']
        ]

        # Build the Project
        return models.Project(
            id=project_from_context['id'],
            name=project_from_context['name'],
            asset_types=asset_types,
            task_types=task_types,
            task_statuses=task_statuses,
            resolution=project_from_context['resolution'],
            ratio=project_from_context['ratio'],
            thumbnailUrl=f"{self.kitsu_client.base_url}/pictures/thumbnails/projects/{project_from_context['id']}.png",
            fps=project_from_context['fps'],
            team=team,
            episodes=self.get_episodes(project_from_context),
        )

    def get_project_assets(self, project) -> List[models.Asset]:
        r_assets = self.kitsu_client.get(
            '/data/assets/with-tasks', params={'project_id': project.id}
        )
        assets_list = []

        for a in r_assets.json():
            if a['canceled']:
                continue
            logging.debug(f"Processing asset {a['name']}")

            asset = models.Asset(
                id=a['id'],
                asset_type_id=a['asset_type_id'],
                name=a['name'],
            )

            if a['preview_file_id']:
                asset.thumbnailUrl = f"{self.kitsu_client.base_url}/pictures/thumbnails/preview-files/{a['preview_file_id']}.png"

            # Format data as expected by edit breakdown
            for task in a['tasks']:
                asset.tasks.append(
                    models.Task(
                        task_status_id=task['task_status_id'],
                        task_type_id=task['task_type_id'],
                        assignees=task['assignees'],
                    )
                )
            assets_list.append(asset)
        return assets_list

    def get_project_sequences(self, project) -> List[models.Sequence]:
        r_sequences = self.kitsu_client.get('/data/sequences', params={'project_id': project.id})
        sequences_list = []
        for sequence in r_sequences.json():
            sequences_list.append(models.Sequence(name=sequence['name'], id=sequence['id']))
        return sequences_list

    def get_project_shots(self, project: models.Project) -> List[models.Shot]:
        r_shots = self.kitsu_client.get('/data/shots/with-tasks', params={'project_id': project.id})
        shots = []

        for s in r_shots.json():
            logging.debug(f"Processing shot {s['name']}")
            if 'frame_in' not in s['data'] or not s['data']['frame_in']:
                logging.debug("Skipping shot with no frame_in data")
                continue

            shot = models.Shot(
                id=s['id'],
                name=s['name'],
                sequence_id=s['sequence_id'],
                data=models.ShotData(
                    frame_in=s['data']['frame_in'], frame_out=s['data']['frame_out']
                ),
                fps=float(project.fps),
            )
            if s['preview_file_id']:
                shot.thumbnailUrl = f"{self.kitsu_client.base_url}/pictures/thumbnails/preview-files/{s['preview_file_id']}.png"
            # Format data as expected by edit breakdown
            for task in s['tasks']:
                shot.tasks.append(
                    (
                        models.Task(
                            task_status_id=task['task_status_id'],
                            task_type_id=task['task_type_id'],
                            assignees=task['assignees'],
                        )
                    )
                )
            shots.append(shot)
        return shots

    def get_task_count(self, project_id):
        r_shots = self.kitsu_client.get('/data/shots/with-tasks', params={'project_id': project_id})
        return writers.ProjectWriter.count_tasks(r_shots.json(), datetime.datetime.now())

    def get_project_casting(
        self,
        project,
        sequences: List[models.Sequence],
        shots: List[models.Shot],
        assets: List[models.Asset],
    ) -> List[models.ShotCasting]:
        shot_castings = []
        for sequence in sequences:
            r_casting = self.kitsu_client.get(
                f"/data/projects/{project.id}/sequences/{sequence.id}/casting"
            )
            casting_per_shot = r_casting.json()
            if not casting_per_shot:
                continue
            for shot_id, cast_assets in casting_per_shot.items():
                # Lookup shot in the Shots list
                shot = next((s for s in shots if s.id == shot_id), None)
                shot_casting = models.ShotCasting(shot=shot)
                for ca in cast_assets:
                    # Lookup each cast asset in the Assets list
                    asset = next((a for a in assets if a.id == ca['asset_id']), None)
                    shot_casting.assets.append(asset)
                shot_castings.append(shot_casting)

        return shot_castings

    def get_project_edits(self, project: models.Project):
        logging.info(f"Getting edits for %s" % project.name)
        # Get first edit (if exists)
        r_edits = self.kitsu_client.get('/data/edits/with-tasks', params={'project_id': project.id})
        edits = []
        for e in r_edits.json():
            if e['canceled']:
                continue
            # Get preview-files from the first task found (usually only one)
            r_previews = self.kitsu_client.get(f"/data/edits/{e['id']}/preview-files")
            # Get the Edit task types (so we can identify the task of type "Edit")
            r_task_types = self.kitsu_client.get(f"/data/edits/{e['id']}/task-types")
            edit_task_id = None
            for task_type in r_task_types.json():
                if task_type['name'] != 'Edit':
                    continue
                # Save the edit task id, so we look it up when listing the preview-files
                edit_task_id = task_type['id']
            # Get the first preview (last revision)
            latest_preview = None
            for task_type_id, preview_list in r_previews.json().items():
                if edit_task_id != task_type_id:
                    continue
                latest_preview = preview_list[0]
                break

            source_name = (
                f"{self.kitsu_client.base_url}/movies/low/preview-files/{latest_preview['id']}.mp4"
            )

            # Set frame offset from metadata

            frame_offset = 0
            try:
                frame_offset = int(e['data']['frame_start'])
            except KeyError:
                pass

            edits.append(
                models.Edit(
                    id=e['id'],
                    name=e['name'],
                    project_id=e['project_id'],
                    totalFrames=0,
                    frameOffset=frame_offset,
                    sourceName=source_name,
                    episode_id=None if not 'episode_id' in e else e['episode_id'],
                )
            )
        return edits

    # def write_project(self, project_id, destination_path):
    #     project_writer = self._get_project_writer(project_id, destination_path)
    #     # project_writer.download_previews(self.request_headers)
    #     # project_writer.download_edits(self.request_headers)
    #     current_task_count = self.get_task_count()
    #     project_writer.merge_task_counts(current_task_count)
    #     # project_writer.write_as_json()

    def __init__(self, kitsu_client: Optional[KitsuClient] = None):
        self.kitsu_client = kitsu_client or KitsuClient()
        self.user_context = self.kitsu_client.get('/data/user/context').json()


def main(args):
    parsed_args = argparser.parse_args(args)
    destination_path = parsed_args.destination_path

    kitsu_writer = KitsuWriter()
    if parsed_args.project_ids:
        for project_id in parsed_args.project_ids:
            kitsu_writer.write_project(project_id, destination_path)
    else:
        kitsu_writer.write_all(destination_path)
        if parsed_args.bundle:
            writers.WatchtowerBundler.bundle(destination_path)


if __name__ == "__main__":
    main(sys.argv[1:])
