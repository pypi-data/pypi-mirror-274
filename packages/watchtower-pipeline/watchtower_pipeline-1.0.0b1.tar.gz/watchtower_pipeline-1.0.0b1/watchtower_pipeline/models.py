import datetime
import hashlib
import logging
import pathlib
import requests
from urllib.parse import urlparse
from tqdm import tqdm
import sys
import uuid
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, TypedDict, Optional


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def fetch_and_save_media(src_url, headers, dst: pathlib.Path, force=False, display_progress=False):
    if dst.is_file() and not force:
        return
    response = requests.get(src_url, headers=headers, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    # Set a variable that semantically matches tqdm API (the inverse of what we want our API to do)
    disable_progress = not display_progress
    progress_bar = tqdm(
        desc='Downloading edit',
        total=total_size_in_bytes,
        unit='iB',
        unit_scale=True,
        disable=disable_progress,
        ascii=' >=',
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if display_progress and total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        logging.error(f"Error downloading {src_url}")


class StaticPreviewMixin:
    thumbnailUrl = None

    @staticmethod
    def hash_filename(name):
        return hashlib.md5(name.encode()).hexdigest()

    @staticmethod
    def generate_preview_file_path(file_id: str, path: pathlib.Path) -> pathlib.Path:
        """Generate a normalized file path.
        This forces .png extension, which for now is ok since all image
        file use that extension, and we do not need to deal with videos.

        For example:
        - 0a32d425-6723-4f2b-baf7-2a6d457fa669
        becomes:
        - 0a/30a32d425-6723-4f2b-baf7-2a6d457fa669.png
        """
        filename = f'{file_id}.png'
        return pathlib.Path('data') / path / file_id[:2] / filename

    def download_and_assign_thumbnail(
        self,
        base_path: pathlib.Path,
        path: Optional[pathlib.Path] = None,
        requests_headers: Optional[Dict] = None,
        force=False,
    ):
        """Download and assign a thumbnail.

        This function assumes that the download url is a valid (full) url located
        at self.thumbnailUrl, and will replace that value with a path to (absolute
        from the site root) to the local file once it's downloaded.
        """
        src_url = self.thumbnailUrl
        logging.debug(f"Downloading {self.name}, {src_url}")
        if not src_url:
            return
        result = urlparse(src_url)
        if not all([result.scheme, result.netloc]):
            logging.debug("Skipping local url. This file was already processed.")
            return
        if not path:
            path = pathlib.Path('')
        dst_url = self.generate_preview_file_path(self.hash_filename(src_url), path)
        dst = base_path / dst_url
        fetch_and_save_media(src_url, requests_headers, dst, force=force)
        setattr(self, 'thumbnailUrl', str(dst_url))


@dataclass
class IdMixin:
    # id: Optional[str]  # In Kitsu it's a UUID
    # In Python 3.10 it will be possible to use this, and make id actually Optional
    # id: Optional[uuid.UUID] = field(default_factory=get_new_uuid)
    name: str

    @staticmethod
    def get_new_uuid() -> str:
        return str(uuid.uuid4())

    def __post_init__(self):
        self.id = self.id or self.get_new_uuid()


@dataclass
class AssetType(IdMixin):
    """Asset Type such as prop, character, etc."""

    id: Optional[str] = None


@dataclass
class TaskType(IdMixin):
    """Task Type such as layout, animation, lighting etc."""

    color: str  # A hex color
    for_shots: bool = False
    id: Optional[str] = None


@dataclass
class TaskStatus(IdMixin):
    """Task Status such as todo, in_progress, review, etc"""

    color: str  # A hex color
    id: Optional[str] = None


@dataclass
class User(StaticPreviewMixin, IdMixin):
    """Members of a project, associated to tasks."""

    has_avatar: bool = False
    id: Optional[str] = None
    thumbnailUrl: Optional[str] = None

    @property
    def full_name(self):
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'full_name': self.full_name,
            'has_avatar': self.has_avatar,
        }


@dataclass
class JsonMixin:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_list(self, key) -> list:
        """We expect that key is in the dict, and that the value is a list."""
        return self.to_dict()[key]


@dataclass
class Task:
    """A task associated with a Shot or an Asset."""

    task_status_id: str
    task_type_id: str
    assignees: List[str] = field(default_factory=list)  # Maps to User ID
    id: Optional[str] = None

    @staticmethod
    def get_new_uuid() -> str:
        return str(uuid.uuid4())

    def __post_init__(self):
        self.id = self.id or self.get_new_uuid()


@dataclass
class Asset(StaticPreviewMixin, IdMixin):
    """An entity such as a character, set, prop, etc."""

    asset_type_id: str
    tasks: List[Task] = field(default_factory=list)
    id: Optional[str] = None
    thumbnailUrl: Optional[str] = None


class ShotData(TypedDict):
    """Shot metadata (usually custom defined in the production tracker)"""

    frame_in: int
    frame_out: int


@dataclass
class Shot(StaticPreviewMixin, IdMixin):
    """A shot, the reference point for tasks."""

    sequence_id: str
    data: ShotData
    tasks: List[Task] = field(default_factory=list)
    startFrame: int = 0
    durationSeconds: float = 0
    id: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    fps: float = 24

    def __post_init__(self):
        super(Shot, self).__post_init__()
        self.startFrame = int(self.data['frame_in'])
        self.durationSeconds = (int(self.data['frame_out']) - self.startFrame) / self.fps


@dataclass
class ShotCasting:
    """The relationship between assets and shots."""

    shot: Shot
    assets: List[Asset] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        if not self.shot:
            return {}
        return {'shot_id': self.shot.id, 'asset_ids': [a.id for a in self.assets]}


@dataclass
class Sequence(IdMixin):
    id: Optional[str] = None


@dataclass
class Edit(IdMixin):
    """The complete cut of the project."""

    project_id: str
    frameOffset: int
    id: Optional[str] = None
    episode_id: Optional[str] = None
    sourceName: Optional[str] = None
    totalFrames: int = 0
    sourceType: str = 'video/mp4'

    def __post_init__(self):
        if not self.sourceName:
            self.sourceName = f"data/projects/{self.project_id}/edit-{self.id}.mp4"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'totalFrames': self.totalFrames,
            'frameOffset': self.frameOffset,
            'sourceName': self.sourceName,
            'sourceType': self.sourceType,
            'episodeId': self.episode_id,
            'id': self.id,
        }


@dataclass
class Episode(IdMixin):
    sequences: List[Sequence] = field(default_factory=list)
    # edit: Edit = None
    id: Optional[str] = None


@dataclass
class EpisodeListItem(IdMixin):
    """Used only to build the dataset managed via projects.ts"""

    id: Optional[str] = None


@dataclass
class ProjectListItem(StaticPreviewMixin, IdMixin):
    """Used to build the dataset managed via projects.ts"""

    id: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    episodes: List[EpisodeListItem] = field(default_factory=list)


@dataclass
class Project(StaticPreviewMixin, IdMixin):
    """A film, short film, etc."""

    ratio: str
    resolution: str
    asset_types: List[AssetType] = field(default_factory=list)
    task_types: List[TaskType] = field(default_factory=list)
    task_statuses: List[TaskStatus] = field(default_factory=list)
    team: List[User] = field(default_factory=list)
    id: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    fps: float = 24
    episodes: List[Episode] = field(default_factory=list)


@dataclass
class TaskStatusCountSnapshot:
    timestamp: datetime
    count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.timestamp.isoformat(),
            "y": self.count,
        }


@dataclass
class TaskStatusCount:
    task_status_id: uuid.UUID
    data: List[TaskStatusCountSnapshot] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_status_id": self.task_status_id,
            "data": [data.to_dict() for data in self.data],
        }


@dataclass
class TaskCount(IdMixin):
    """A time series of task status counts.

    We group the counts by task type, and then by status. For example:
    - task_type: animation
    - episode: ep01
    - task_statuses:
        - task_status: done
          data:
            - timestamp: 2020-02-01
              count: 10
            - timestamp: 2020-02-02
              count: 15
        - task_status: other
          data:
            - timestamp: 2020-02-01
              count: 16
            - timestamp: 2020-02-02
              count: 11

    """

    task_type_id: uuid.UUID
    episode_id: Optional[str] = None
    task_statuses: List[TaskStatusCount] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_type_id": self.task_type_id,
            "episode_id": self.episode_id,
            "task_statuses": [task_status.to_dict() for task_status in self.task_statuses],
        }
