"""
Модуль для управління завданнями TMS (Task Management System).
Версія для ПР-8: Типізація, dataclass та документація.
"""
import datetime
import smtplib
from enum import IntEnum
from email.mime.text import MIMEText
from dataclasses import dataclass, field
from typing import List, Optional, Union


class TaskStatus(IntEnum):
    """Статуси виконання завдання."""
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2


class Action(IntEnum):
    """Доступні дії над завданнями."""
    CREATE = 1
    ASSIGN = 2
    COMPLETE = 3


@dataclass
class Task:
    """Модель завдання."""
    id: int
    title: str
    user: str
    priority: int = 3
    status: TaskStatus = TaskStatus.TODO
    created: str = field(default_factory=lambda: str(datetime.datetime.now()))


class TaskRepository:
    """Репозиторій для збереження та доступу до завдань."""

    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add(self, task: Task) -> None:
        """Додає нове завдання у сховище."""
        self.tasks.append(task)

    def get_all(self) -> List[Task]:
        """Повертає список усіх завдань."""
        return self.tasks

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Повертає завдання за його ідентифікатором."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


REPO = TaskRepository()
LOG_FILE = 'log.txt'


def _validate_title(title: str) -> bool:
    """Перевіряє коректність назви завдання."""
    if not title or len(title) == 0:
        return False
    if len(title) > 100:
        return False
    return True


def _log_action(message: str) -> None:
    """Записує дію у лог-файл."""
    with open(LOG_FILE, 'a', encoding='utf-8') as file:
        file.write(f"{datetime.datetime.now()}: {message}\n")


def _send_email(user_email: str, title: str) -> None:
    """Відправляє email сповіщення (імітація)."""
    try:
        msg = MIMEText(f'New task: {title}')
        msg['Subject'] = 'Task created'
        msg['From'] = 'noreply@tms.com'
        msg['To'] = user_email
        # В реальних умовах тут був би SMTP сервер
        pass
    except Exception:
        pass


def create_task(title: str, user_email: str, priority: Optional[int] = None) -> Optional[Task]:
    """Створює та зберігає нове завдання."""
    if not _validate_title(title):
        return None

    final_priority = priority if priority is not None else 3
    task = Task(
        id=len(REPO.get_all()) + 1,
        title=title,
        user=user_email,
        priority=final_priority
    )
    REPO.add(task)
    _log_action(f"created task {title}")
    _send_email(user_email, title)
    return task


def assign_task(task_id: int, user_email: str) -> Optional[Task]:
    """Призначає завдання на конкретного користувача."""
    task = REPO.get_by_id(task_id)
    if task:
        task.user = user_email
        task.status = TaskStatus.IN_PROGRESS
        _log_action("assigned")
        return task
    return None


def complete_task(task_id: int) -> Union[Task, bool, None]:
    """Відмічає завдання як виконане."""
    task = REPO.get_by_id(task_id)
    if not task:
        return None
    if task.status != TaskStatus.IN_PROGRESS:
        return False
    task.status = TaskStatus.DONE
    _log_action("completed")
    return task


def process(
    title_or_id: Union[str, int],
    user_email: str,
    action: int,
    priority: Optional[int] = None
) -> Union[Task, bool, None]:
    """Головний роутер для обробки команд."""
    if action == Action.CREATE and isinstance(title_or_id, str):
        return create_task(title_or_id, user_email, priority)
    if action == Action.ASSIGN and isinstance(title_or_id, int):
        return assign_task(title_or_id, user_email)
    if action == Action.COMPLETE and isinstance(title_or_id, int):
        return complete_task(title_or_id)
    return None
