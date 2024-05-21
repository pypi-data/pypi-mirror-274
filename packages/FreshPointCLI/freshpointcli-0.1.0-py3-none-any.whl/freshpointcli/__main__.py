import argparse
import asyncio
import typing

from rich.console import Console
from rich.padding import Padding

from freshpointsync import ProductPage, ProductPageData

from .files import AppDirs, AppFiles, AppSettings
from .logger import logging, logger, configure_logging
from .promt import PromptProcessor, AppColors, parse_args_init


APP_NAME = 'FreshPoint'


console = Console()


def dump_page_data(page_data: ProductPageData, page_cache_file: str) -> None:
    with open(page_cache_file, 'w', encoding='utf-8') as file:
        file.write(page_data.model_dump_json(indent=4, by_alias=True))


async def dump_page_data_on_update(context) -> None:
    page_data: ProductPageData = context.get('page_data')
    file_path: str = context.get('file_path')
    if not page_data or not file_path:
        logger.error('dump_page_data: page_data or file_path not provided.')
        return
    dump_page_data(page_data, file_path)


class AppSession:
    def __init__(
        self,
        page: ProductPage,
        files: AppFiles,
        update_interval: float = 10.0
    ) -> None:
        self.page = page
        self.files = files
        self.update_interval = update_interval
        self.promp_processor: typing.Optional[PromptProcessor] = None
        self._init_update_task: typing.Optional[asyncio.Task] = None

    async def _init_update_forever_after_delay(self, delay: float) -> None:
        await asyncio.sleep(delay)
        self.page.init_update_forever_task(self.update_interval)

    async def _await_init_update_task(self) -> None:
        if self._init_update_task is None or self._init_update_task.done():
            return
        with console.status(
            'Updating product data...',
            spinner='bouncingBar',
            spinner_style=f'bold {AppColors.FRESHPOINT.value}'
        ):
            await self._init_update_task
            page_cache_file = self.files.get_page_cache_file(
                self.page.data.location_id
                )
            dump_page_data(self.page.data, page_cache_file)

    async def start_session(self) -> None:
        await self.page.start_session()
        self.page.context['page_data'] = self.page.data
        self.page.context['file_path'] = self.files.get_page_cache_file(
            self.page.data.location_id
            )
        self._init_update_task = asyncio.create_task(
            self.page.update_silently()
            )
        asyncio.create_task(
            self._init_update_forever_after_delay(self.update_interval)
            )
        self.page.subscribe_for_update(handler=dump_page_data_on_update)
        if not self.page.data.products:  # first run, no cache
            await self._await_init_update_task()
        if not self.page.data.products:  # invalid page ID
            console.print(
                f'Page {self.page.data.url} is not accessible.',
                style=AppColors.RED.value
                )
            raise SystemExit
        self.promp_processor = PromptProcessor(
            APP_NAME, self.page, self.files.get_history_file()
            )

    async def await_responce(self) -> str:
        assert self.promp_processor is not None
        response = await self.promp_processor.await_responce()
        if not response:
            settings = self.files.get_settings()
            response = settings.default_query or ''
        return response

    async def process_responce(self, response: str) -> None:
        assert self.promp_processor is not None
        args = self.promp_processor.parse_responce(response)
        if args is not None:
            table = self.promp_processor.process_responce_args(args)
            console.print(Padding(table.table, (1, 0)))
            if args.setdefault:
                settings = self.files.get_settings()
                settings.default_query = response
                settings.model_dump_file(indent=4, by_alias=True)

    async def start_prompting(self) -> None:
        response = await self.await_responce()
        await self._await_init_update_task()
        await self.process_responce(response)
        while True:
            response = await self.await_responce()
            await self.process_responce(response)

    async def stop_session(self) -> None:
        await self.page.await_update_handlers()
        await self.page.close_session()


def ensure_location_id_set(
    args: argparse.Namespace, settings: AppSettings
) -> None:
    if args.location_id is None:
        if settings.page_id is None:
            console.print(
                'Page location ID cache not found. '
                'Please provide a location ID.'
                )
            logger.info('Page location ID cache not found.')
            raise SystemExit
        args.location_id = settings.page_id
    elif args.location_id != settings.page_id:
        settings.page_id = args.location_id


def handle_unexpected_error(e: Exception, log_path: str) -> None:
    logger.exception(f'Unexpected error "{type(e).__name__}": {e}')
    console.print(f'Unexpected error. Exiting. See "{log_path}" for details.')
    raise SystemExit


async def app() -> None:
    try:
        args = parse_args_init()
        name = 'FreshPointCLI'
        dirs = AppDirs(appname=name, ensure_exists=True)  # type: ignore
        files = AppFiles(dirs)
    except OSError as e:  # may happen if user has no permissions
        console.print(
            f'Error initializing app files directory ({e}). Exiting.',
            style=AppColors.RED.value
            )
        raise SystemExit
    try:
        configure_logging(
            log_file=files.get_log_file(),
            level=logging.WARNING
            )
    except Exception as e:
        console.print(
            f'WARNING: Failed to configure logging ({e}).',
            style=AppColors.RED.value
            )
    try:
        settings = files.get_settings()
        ensure_location_id_set(args, settings)
        data = files.get_page_cache(args.location_id)
        page = ProductPage(data=data)
        session = AppSession(page, files, update_interval=10.0)
    except Exception as e:
        handle_unexpected_error(e, files.get_log_file())
    try:
        await session.start_session()
        settings.model_dump_file(indent=4, by_alias=True)
        await session.start_prompting()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        handle_unexpected_error(e, files.get_log_file())
    finally:  # still executed if SystemExit is raised
        with console.status(
            'Closing session...',
            spinner='bouncingBar',
            spinner_style=f'bold {AppColors.FRESHPOINT.value}'
        ):
            await session.stop_session()


def main() -> None:
    asyncio.run(app())
