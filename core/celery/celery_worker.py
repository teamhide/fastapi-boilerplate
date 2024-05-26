# core/celery/celery_app.py
import os

from celery import Celery, signals
from kombu import Queue

import app  # noqa
from core.config import config
from core.db.session import reset_session_context, set_session_context


class CeleryConfigurator:
    """
    Configures and manages the Celery application settings, task routing, and logging.

    This class encapsulates the Celery configuration including the setup of task routes,
    logging, and signal connections for task lifecycle events.

    Attributes:
        app (Celery): An instance of the Celery class, configured with backend and broker URLs.
    """

    def __init__(self):
        """
        Initializes the Celery application with specific settings for backend, broker, and signal connections.
        """
        self.app = Celery(
            "worker",
            backend=config.CELERY_BACKEND_URL,
            broker=config.CELERY_BROKER_URL,
        )
        self._connect_signals()
        self.configure_celery()

    def _connect_signals(self):
        """
        Connects custom signal handlers to Celery signals for enhanced session.
        """
        signals.task_prerun.connect(self.start_session)
        signals.task_postrun.connect(self.close_session)

    async def start_session(self, task=None, *args, **kwargs):
        """
        Starts a database session at the beginning of a task's execution, managing the session context.

        This method initializes the session context that will be used throughout the task's lifecycle.
        It does not directly manipulate the session here but sets up the context needed for managing
        the session during the task execution.

        Args:
            task (Celery Task): The current task instance.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.
        """
        session_id = f"session_{task.request.id}"
        token = set_session_context(session_id)
        task.request.session_token = token

    async def close_session(self, task=None, *args, **kwargs):
        """
        Closes the database session after the task's execution is complete.

        This method resets the session context set at the start of the task, ensuring that any session
        specific to the task is properly concluded. The session itself will be automatically closed by
        the async_scoped_session.

        Args:
            task (Celery Task): The current task instance.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.
        """
        token = task.request.session_token
        reset_session_context(token)

    def _setup_queues(self):
        """
        Automatically configures Celery queues based on the application modules.

        This method dynamically sets up queues for each module in the 'app' directory that contains a
        'celery' subdirectory with a 'tasks.py' file. It constructs the queue name from the module name,
        ensuring each task module has its corresponding queue.

        The queues are configured with a naming convention of '<module-name>-queue' and use a routing key
        that matches tasks from the respective module to the appropriate queue based on the module's name.

        How it works:
        - It navigates through the 'app' directory to find subdirectories that match the expected
        structure for Celery tasks (i.e., 'app/<module>/application/celery/tasks.py').
        - For each valid module, it creates a queue named '<module-name>-queue'.
        - The routing key for each queue is set to '<module-name>.#', which means it will match any
        routing keys that start with the module name, allowing for flexible task routing within the module.

        Example:
        - If there is a module 'users' with the path 'app/users/application/celery/tasks.py',
        this method will setup a queue named 'users-queue' with a routing key 'users.#'.

        Note:
        - This method assumes that each part of the system that needs task processing capabilities will
        conform to this directory and naming structure. This convention simplifies the setup and
        scaling of task processing across different parts of the application.
        """
        base_path = os.path.join(os.getcwd(), "app")
        modules = [
            name
            for name in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, name, "application", "celery"))
            and os.path.exists(
                os.path.join(base_path, name, "application", "celery", "tasks.py")
            )
        ]

        self.app.conf.task_queues = [
            Queue(f"{module}-queue", routing_key=f"{module}.#") for module in modules
        ]

    def _setup_task_routes(self):
        """
        Configures task routing rules to ensure tasks are directed to the appropriate queues.

        Detailed Routing Setup:
        - Dynamic routing based on the task's module name allows for a scalable approach
          to handle various tasks.
        - The queue name is inferred dynamically from the module name of the task, promoting
          consistency and maintainability.

        Example:
        - A task located in 'app.catalog_item.tasks' is routed to 'catalog-items-queue'.

        Developers are encouraged to maintain a consistent naming convention in task module
        names to ensure the routing logic functions correctly.

        Note:
        - This method sets up the routing using a lambda function that parses the module name to
          determine the queue. This method assumes that the module name directly corresponds to
          the queue name.
        """

        self.app.conf.task_routes = {
            "app.*.application.celery.*": {
                "queue": lambda args: f"{args[0].split('.')[1]}-queue"
            }
        }

    def configure_celery(self):
        """
        Applies the configurations for task routes and updates default settings for task execution.

        This method centralizes the configuration of task behavior such as concurrency, task expiration,
        and memory limits to optimize worker performance and resource management.
        """

        self._setup_task_routes()
        self._setup_queues()
        self.app.conf.update(
            task_track_started=True,
            worker_concurrency=10,
            worker_prefetch_multiplier=1,
            worker_max_tasks_per_child=100,
            worker_max_memory_per_child=300000,
            result_expires=3600,
            broker_transport_options={"visibility_timeout": 3600},
            broker_connection_retry=True,
        )
        self.app.autodiscover_tasks(["app"])


celery_conf = CeleryConfigurator()
celery_app = celery_conf.app
