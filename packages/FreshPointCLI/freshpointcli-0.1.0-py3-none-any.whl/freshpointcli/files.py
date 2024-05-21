import os
import hashlib

from json import JSONDecodeError
from pathlib import Path
from typing import Any, Optional
from platformdirs import PlatformDirs
from pydantic import (
    BaseModel, ConfigDict, ValidationError, ValidationInfo,
    ValidatorFunctionWrapHandler, field_validator, Field
)
from pydantic.alias_generators import to_camel

from freshpointsync import ProductPageData

from .logger import logger


class AppFileData(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        validate_assignment=True,
        )

    file_path: Optional[str] = Field(default=None, exclude=True)
    _last_dump_hash: str = ''

    def model_post_init(self, __context) -> None:
        self._last_dump_hash = self.get_hash()

    @classmethod
    def model_validate_file(
        cls,
        path: str,
        *,
        strict: bool | None = None,
        context: dict[str, Any] | None = None
    ) -> 'AppFileData':
        with open(path, 'r', encoding='utf-8') as file:
            json_data = file.read()
        model = cls.model_validate_json(
            json_data, strict=strict, context=context
            )
        model.file_path = path                    # file_path is assigned after
        model._last_dump_hash = model.get_hash()  # model_post_init is called
        return model

    @field_validator('*', mode='wrap')
    @classmethod
    def _set_field_safe(
        cls,
        value: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo
    ) -> dict[str, Any]:
        try:
            return handler(value)
        except ValidationError:
            logger.warning(
                f'Invalid value "{value}" for settings field '
                f'"{info.field_name}". Setting to default (None).'
                )
            return handler(None)

    def model_dump_file(
        self,
        *,
        indent: int | None = None,
        include: set | dict | None = None,
        exclude: set | dict | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True
    ) -> None:
        if self.file_path is None:
            raise FileNotFoundError('No file path set')
        curr_hash = self.get_hash()
        if curr_hash != self._last_dump_hash:
            self._last_dump_hash = curr_hash
            data = self.model_dump_json(
                indent=indent,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                round_trip=round_trip,
                warnings=warnings
                )
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(data)

    def set_field_and_dump_file(self, field_name: str, value: Any) -> None:
        setattr(self, field_name, value)
        self.model_dump_file()

    def get_hash(self) -> str:
        data = self.model_dump_json().encode()
        return hashlib.sha256(data, usedforsecurity=False).hexdigest()


class AppSettings(AppFileData):
    page_id: Optional[int] = None
    default_query: Optional[str] = None


class AppDirs(PlatformDirs):  # type: ignore

    @property
    def user_pages_cache_dir(self) -> str:
        path = os.path.join(self.user_cache_dir, 'pages')
        if self.ensure_exists and not os.path.exists(path):
            os.makedirs(path)
        return path

    @property
    def user_pages_cache_path(self) -> Path:
        return Path(self.user_pages_cache_dir)


class AppFiles:
    def __init__(self, dirs: AppDirs) -> None:
        self._dirs = dirs

    def get_history_file(self) -> str:
        return os.path.join(self._dirs.user_cache_dir, '.history')

    def get_log_file(self) -> str:
        return os.path.join(self._dirs.user_log_dir, '.log')

    def get_settings_file(self) -> str:
        return os.path.join(self._dirs.user_config_dir, 'settings.json')

    def get_page_cache_file(self, page_id: int) -> str:
        return os.path.join(self._dirs.user_pages_cache_dir, f'{page_id}.json')

    def get_settings(self) -> AppSettings:
        try:
            path = self.get_settings_file()
            return AppSettings.model_validate_file(path)  # type: ignore
        except FileNotFoundError:
            logger.info(
                'Settings file was not found. '
                'Initializing a default settings instance.'
                )
            return AppSettings(file_path=path)
        except (ValidationError, JSONDecodeError) as err:
            logger.warning(
                f'Settings file is invalid ({err}). '
                f'Initializing a default settings instance.'
                )
            return AppSettings(file_path=path)

    def get_page_cache(self, page_id: int) -> ProductPageData:
        try:
            path = self.get_page_cache_file(page_id)
            with open(path, 'r', encoding='utf-8') as file:
                data = file.read()
            page_data = ProductPageData.model_validate_json(data)
            if page_data.location_id != page_id:
                raise ValidationError
            return page_data
        except FileNotFoundError:
            logger.info(
                f'Page cache file for page {page_id} was not found. '
                f'Initializing an empty page data instance.'
                )
            return ProductPageData(location_id=page_id)
        except (ValidationError, JSONDecodeError) as err:
            logger.warning(
                f'Page cache file for page {page_id} is invalid ({err}). '
                f'Initializing an empty page data instance.'
                )
            return ProductPageData(location_id=page_id)
