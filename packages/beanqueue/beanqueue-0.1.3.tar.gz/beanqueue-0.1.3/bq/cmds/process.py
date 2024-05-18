import functools
import importlib
import logging
import platform
import sys
import threading
import time
import typing

import click
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from .. import constants
from .. import models
from ..config import Config
from ..container import Container
from ..processors.registry import collect
from ..services.dispatch import DispatchService
from ..services.worker import WorkerService


@inject
def update_workers(
    worker_id: typing.Any,
    config: Config = Provide[Container.config],
    session_factory: typing.Callable = Provide[Container.session_factory],
    make_dispatch_service: typing.Callable = Provide[Container.make_dispatch_service],
    make_worker_service: typing.Callable = Provide[Container.make_worker_service],
):
    db: DBSession = session_factory()
    worker_service: WorkerService = make_worker_service(session=db)
    dispatch_service: DispatchService = make_dispatch_service(session=db)
    current_worker = worker_service.get_worker(worker_id)
    logger = logging.getLogger(__name__)
    logger.info(
        "Updating worker %s with heartbeat_period=%s, heartbeat_timeout=%s",
        current_worker.id,
        config.WORKER_HEARTBEAT_PERIOD,
        config.WORKER_HEARTBEAT_TIMEOUT,
    )
    while True:
        dead_workers = worker_service.fetch_dead_workers(
            timeout=config.WORKER_HEARTBEAT_TIMEOUT
        )
        task_count = worker_service.reschedule_dead_tasks(
            # TODO: a better way to abstract this?
            dead_workers.with_entities(current_worker.__class__.id)
        )
        found_dead_worker = False
        for dead_worker in dead_workers:
            found_dead_worker = True
            logger.info(
                "Found dead worker %s (name=%s), reschedule %s dead tasks in channels %s",
                dead_worker.id,
                dead_worker.name,
                task_count,
                dead_worker.channels,
            )
            dispatch_service.notify(dead_worker.channels)
        if found_dead_worker:
            db.commit()

        if current_worker.state != models.WorkerState.RUNNING:
            # This probably means we are somehow very slow to update the heartbeat in time, or the timeout window
            # is set too short. It could also be the administrator update the worker state to something else than
            # RUNNING. Regardless the reason, let's stop processing.
            logger.warning(
                "Current worker %s state is %s instead of running, quit processing"
            )
            sys.exit(0)

        time.sleep(config.WORKER_HEARTBEAT_PERIOD)
        current_worker.last_heartbeat = func.now()
        db.add(current_worker)
        db.commit()


@inject
def process_tasks(
    channels: tuple[str, ...],
    config: Config = Provide[Container.config],
    db: DBSession = Provide[Container.session],
    dispatch_service: DispatchService = Provide[Container.dispatch_service],
    worker_service: WorkerService = Provide[Container.worker_service],
):
    logger = logging.getLogger(__name__)

    if not channels:
        channels = [constants.DEFAULT_CHANNEL]

    if not config.PROCESSOR_PACKAGES:
        logger.error("No PROCESSOR_PACKAGES provided")
        sys.exit(-1)

    logger.info("Scanning packages %s", config.PROCESSOR_PACKAGES)
    pkgs = list(map(importlib.import_module, config.PROCESSOR_PACKAGES))
    registry = collect(pkgs)
    for channel, module_processors in registry.processors.items():
        logger.info("Collected processors with channel %r", channel)
        for module, func_processors in module_processors.items():
            for processor in func_processors.values():
                logger.info(
                    "  Processor module %r, processor %r", module, processor.name
                )

    worker = worker_service.make_worker(name=platform.node(), channels=channels)
    db.add(worker)
    dispatch_service.listen(channels)
    db.commit()

    logger.info("Created worker %s, name=%s", worker.id, worker.name)
    logger.info("Processing tasks in channels = %s ...", channels)

    worker_update_thread = threading.Thread(
        target=functools.partial(
            update_workers,
            worker_id=worker.id,
        ),
        name="update_workers",
    )
    worker_update_thread.daemon = True
    worker_update_thread.start()

    worker_id = worker.id

    try:
        while True:
            while True:
                tasks = dispatch_service.dispatch(
                    channels,
                    worker_id=worker_id,
                    limit=config.BATCH_SIZE,
                ).all()
                for task in tasks:
                    logger.info(
                        "Processing task %s, channel=%s, module=%s, func=%s",
                        task.id,
                        task.channel,
                        task.module,
                        task.func_name,
                    )
                    # TODO: support processor pool and other approaches to dispatch the workload
                    registry.process(task)
                if not tasks:
                    # we should try to keep dispatching until we cannot find tasks
                    break
                else:
                    db.commit()
            # we will not see notifications in a transaction, need to close the transaction first before entering
            # polling
            db.close()
            try:
                for notification in dispatch_service.poll(timeout=config.POLL_TIMEOUT):
                    logger.debug("Receive notification %s", notification)
            except TimeoutError:
                logger.debug("Poll timeout, try again")
                continue
    except (SystemExit, KeyboardInterrupt):
        db.rollback()
        logger.info("Shutting down ...")
        worker_update_thread.join(5)

    worker.state = models.WorkerState.SHUTDOWN
    db.add(worker)
    task_count = worker_service.reschedule_dead_tasks([worker.id])
    logger.info("Reschedule %s tasks", task_count)
    dispatch_service.notify(channels)
    db.commit()

    logger.info("Shutdown gracefully")


@click.command()
@click.argument("channels", nargs=-1)
def main(
    channels: tuple[str, ...],
):
    process_tasks(channels)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    container = Container()
    container.wire(modules=[__name__])
    main()
