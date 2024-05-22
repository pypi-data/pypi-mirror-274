from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.installer_command import InstallerCommand
from poetry.core.packages.project_package import ProjectPackage
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry


class PoetryGroupOverridePlugin(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        """Entry point for the plugin; saves the Cleo IO controller and registers the depedency remover"""
        # application.event_dispatcher.add_listener(COMMAND, self.remove_dependencies)
        # self.io = application._io  # noqa
        self.application = application

        if self.validate_config():
            self.application.event_dispatcher.add_listener(
                COMMAND, self.override_dependencies
            )

    def validate_config(self):
        if not self.overrides:
            return False

        for group in self.overrides:
            if group not in self.application.poetry.package._dependency_groups.keys():
                raise ValueError(f"Group {group} not found in poetry.toml")

        return True

    @property
    def overrides(self):
        if (
            not self.application.poetry.pyproject.data.get("tool", {})
            .get("poetry-overrides", {})
            .get("groups")
        ):
            return []
        return self.application.poetry.pyproject.data["tool"]["poetry-overrides"][
            "groups"
        ]

    def override_dependencies(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ):

        if not isinstance(event.command, InstallerCommand):
            return

        command: InstallerCommand = event.command
        installer = command.installer

        package: ProjectPackage = installer._package
        with_flags = self.application._io.input.option("with") or []
        without_flags = self.application._io.input.option("without") or []
        for group, deps in package._dependency_groups.items():
            if group == "main":
                continue

            if group in with_flags and group in self.overrides:
                for gn, gd in package._dependency_groups.items():
                    if gn == group:
                        continue
                    dep_names = [d.name for d in gd.dependencies]
                    for dep in deps.dependencies:
                        if dep.name in dep_names:
                            package._dependency_groups[gn].remove_dependency(dep.name)
                package.with_dependency_groups(group, only=False)

        installer._package = package
