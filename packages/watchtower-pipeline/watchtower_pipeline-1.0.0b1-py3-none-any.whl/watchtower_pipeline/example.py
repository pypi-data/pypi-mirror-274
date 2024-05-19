#!/usr/bin/env python3
import logging
import random
import sys
from typing import List
from watchtower_pipeline import writers, models, argparser


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class ExampleWriter(writers.AbstractWriter):
    shots: List[models.Shot] = []
    assets: List[models.Asset] = []
    sequences: List[models.Sequence] = []
    frame_out = 0

    @property
    def request_headers(self):
        return

    def get_project_list(self) -> List[models.ProjectListItem]:
        return [
            models.ProjectListItem(
                id='example-project-id',
                name='Example Project',
                thumbnailUrl=None,
            )
        ]

    def get_project(self, project_id) -> models.Project:
        """Generate synthetic project data."""

        # Create Users
        users_list = []
        for i in range(10):
            user = models.User(name=f"User {i}")
            users_list.append(user)

        # Create Asset Types
        asset_types_list = []
        for n in ['Characters', 'Props', 'Environment', 'FX']:
            asset_type = models.AssetType(name=n)
            asset_types_list.append(asset_type)

        # Create Task Types for Assets
        task_types_list = []
        for n, c in [
            ('Concept', '#8D6E63'),
            ('Modeling', '#78909C'),
            ('Shading', '#64B5F6'),
            ('Rigging', '#9CCC65'),
        ]:
            task_type = models.TaskType(
                name=n,
                color=c,
                for_shots=False,
            )
            task_types_list.append(task_type)
        # Create Task Types for Shots
        for n, c in [
            ('Storyboard', '#43A047'),
            ('Layout', '#7CB342'),
            ('Animation', '#F9A825'),
            ('Lighting', '#9CCC65'),
        ]:
            task_type = models.TaskType(
                name=n,
                color=c,
                for_shots=True,
            )
            task_types_list.append(task_type)

        # Create Task Statuses
        task_statuses_list = []
        for n, c in [
            ('Todo', '#f5f5f5'),
            ('Work In Progress', '#3273dc'),
            ('Done', '#22d160'),
        ]:
            task_status = models.TaskStatus(id=None, name=n, color=c)
            task_statuses_list.append(task_status)

        # Create Project Snapshot data
        return models.Project(
            id=project_id,
            name='Example Project',
            ratio="2.35:1",
            resolution='2018x858',
            asset_types=asset_types_list,
            task_types=task_types_list,
            task_statuses=task_statuses_list,
            team=users_list,
            # thumbnailUrl=f"https://picsum.photos/id/{10}/192/108",
            thumbnailUrl=None,
        )

    def get_project_edits(self, project: models.Project) -> models.Edit:
        return models.Edit(
            id='edit-id',
            name='Edit',
            totalFrames=self.frame_out,
            frameOffset=20,
            project_id=project.id,
            sourceName='',
            episode_id=None,
        )

    def get_project_assets(self, project: models.Project) -> List[models.Asset]:
        assets_list = []
        for i in range(10):
            asset_type = random.choice(project.asset_types)
            asset = models.Asset(
                name=f"Asset {i}",
                asset_type_id=asset_type.id,
                # thumbnailUrl=f"https://picsum.photos/id/{i + 1}/192/108",
                thumbnailUrl=None,
            )
            for t in range(3):
                rand_task_status = random.choice(project.task_statuses)
                random_task_type = random.choice(
                    [tt for tt in project.task_types if tt.for_shots is False]
                )
                random_user = random.choice(project.team)
                asset.tasks.append(
                    models.Task(
                        rand_task_status.id,
                        random_task_type.id,
                        [random_user.id],
                    )
                )
            assets_list.append(asset)
        return assets_list

    def get_project_sequences(self, project: models.Project) -> List[models.Sequence]:
        sequence = models.Sequence(name='Seq 1')
        self.sequences = [sequence]
        return self.sequences

    def get_project_shots(self, project: models.Project) -> List[models.Shot]:
        shots_list = []
        frame_in = 0
        frame_out = 50
        for i in range(20):
            shot = models.Shot(
                name=f"SH_{i + 1}",
                sequence_id=self.sequences[0].id,
                data=models.ShotData(frame_in=frame_in, frame_out=frame_out),
                # thumbnailUrl=f"https://picsum.photos/id/{i + 1}/192/108",
                thumbnailUrl=None,
            )
            for t in range(4):
                rand_task_status = random.choice(project.task_statuses)
                random_task_type = random.choice(
                    [tt for tt in project.task_types if tt.for_shots is True]
                )
                random_user = random.choice(project.team)
                shot.tasks.append(
                    models.Task(
                        rand_task_status.id,
                        random_task_type.id,
                        [random_user.id],
                    )
                )
            frame_in = frame_out
            frame_out += random.randint(20, 150)
            self.frame_out = frame_out
            shots_list.append(shot)
        return shots_list

    def get_project_casting(
        self,
        project,
        sequences: List[models.Sequence],
        shots: List[models.Shot],
        assets: List[models.Asset],
    ) -> List[models.ShotCasting]:
        shot_castings: List[models.ShotCasting] = []
        for s in self.shots:
            shot_castings.append(models.ShotCasting(shot=s, assets=random.sample(self.assets, 3)))
        return shot_castings


def main(args):
    parsed_args = argparser.parse_args(args)
    destination_path = parsed_args.destination_path

    ExampleWriter().write_all(destination_path)
    if parsed_args.bundle:
        writers.WatchtowerBundler.bundle(destination_path)


if __name__ == "__main__":
    main(sys.argv[1:])
