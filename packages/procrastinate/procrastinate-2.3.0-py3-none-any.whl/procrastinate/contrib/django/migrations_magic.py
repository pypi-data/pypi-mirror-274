from __future__ import annotations

import itertools
import pathlib
import sys
import types
from importlib import abc, machinery
from typing import (
    TYPE_CHECKING,
    Iterable,
    Iterator,
)

import attr
from django.db import migrations

if TYPE_CHECKING:
    import importlib_resources
else:
    # https://github.com/pypa/twine/pull/551
    if sys.version_info[:2] < (3, 9):  # coverage: exclude
        import importlib_resources
    else:  # coverage: exclude
        import importlib.resources as importlib_resources

# For a thorough explaination of what this package does, see README.md in the same
# folder

TOP_LEVEL_NAME = "procrastinate.contrib.django.migrations"
VIRTUAL_PATH = "<procrastinate migrations virtual path>"


class ProcrastinateMigrationsImporter(
    abc.PathEntryFinder, abc.MetaPathFinder, abc.Loader
):
    def __init__(self):
        sql_migrations = get_all_migrations()
        self.migrations = {
            mig.name: mig for mig in make_migrations(sql_migrations=sql_migrations)
        }
        from .static_migrations import static_migrations

        for name, migration in static_migrations.items():
            self.migrations[name] = migration

    # Necessary for Pyright
    def find_module(self, fullname, path=None):
        raise NotImplementedError

    def iter_modules(self, prefix):
        return [(mig, False) for mig in self.migrations]

    def exec_module(self, module: types.ModuleType) -> None:
        if module.__name__ == TOP_LEVEL_NAME:
            module.__file__ = "virtual"
            module.__path__.append(VIRTUAL_PATH)  # type: ignore
            return

        migration_cls = self.migrations[module.__name__.split(".")[-1]]
        module.Migration = migration_cls  # type: ignore

    def find_spec(
        self,
        fullname: str,
        *args,
        **kwargs,
    ) -> machinery.ModuleSpec | None:
        if fullname.startswith(TOP_LEVEL_NAME):
            return machinery.ModuleSpec(
                name=fullname, loader=self, is_package=fullname == TOP_LEVEL_NAME
            )
        return None

    def path_hook(self, path: str) -> ProcrastinateMigrationsImporter:
        if path == VIRTUAL_PATH:
            return self
        raise ImportError


def load():
    if any(isinstance(e, ProcrastinateMigrationsImporter) for e in sys.meta_path):
        # Our job is already done
        return
    importer = ProcrastinateMigrationsImporter()
    sys.meta_path.append(importer)
    sys.path_hooks.append(importer.path_hook)


def list_migration_files() -> Iterable[tuple[str, str]]:
    """
    Returns a list of filenames and file contents for all migration files
    """
    return [
        (p.name, p.read_text(encoding="utf-8"))
        for p in importlib_resources.files("procrastinate.sql.migrations").iterdir()
        if p.name.endswith(".sql")
    ]


def version_from_string(version_str) -> tuple:
    return tuple(int(e) for e in version_str.split("."))


@attr.dataclass(frozen=True)
class ProcrastinateMigration:
    filename: str
    name: str
    version: tuple
    index: int
    contents: str

    @classmethod
    def from_file(cls, filename: str, contents: str) -> ProcrastinateMigration:
        path = pathlib.PurePath(filename)
        version_str, index, name = path.stem.split("_", 2)
        return cls(
            filename=path.name,
            name=name,
            version=version_from_string(version_str=version_str),
            index=int(index),
            contents=contents,
        )


def get_all_migrations() -> Iterable[ProcrastinateMigration]:
    all_files = list_migration_files()
    migrations = [
        ProcrastinateMigration.from_file(filename=filename, contents=contents)
        for filename, contents in all_files
    ]

    return sorted(migrations, key=lambda x: (x.version, x.index))


def make_migrations(
    sql_migrations: Iterable[ProcrastinateMigration],
):
    previous_migration = None
    counter = itertools.count(1)

    for sql_migration in sql_migrations:
        migration = make_migration(
            sql_migration=sql_migration,
            previous_migration=previous_migration,
            counter=counter,
        )
        previous_migration = migration
        yield migration


def make_migration(
    sql_migration: ProcrastinateMigration,
    previous_migration: type[migrations.Migration] | None,
    counter: Iterator[int],
) -> type[migrations.Migration]:
    class NewMigration(migrations.Migration):
        initial = previous_migration is None
        operations = [migrations.RunSQL(sql=sql_migration.contents)]
        name = f"{next(counter):04d}_{sql_migration.name}"

        if previous_migration:
            dependencies = [("procrastinate", previous_migration.name)]

    return NewMigration
