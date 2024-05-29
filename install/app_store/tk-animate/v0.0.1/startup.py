import os
import sys

import sgtk
import sgtk.platform.framework
from sgtk.platform import SoftwareLauncher, SoftwareVersion, LaunchInformation


class EngineConfigurationError(sgtk.TankError):
    pass


class AnimateLauncher(SoftwareLauncher):
    COMPONENT_REGEX_LOOKUP = {
        "version": "[\d.]+",
        "version_back": "[\d.]+",  # backreference to ensure same version
    }
    EXECUTABLE_MATCH_TEMPLATES = {
        "darwin": "/Applications/Adobe Animate {version}/Animate {version_back}.app",
        "win32": "C:/Program Files/Adobe/Adobe Animate {version}/Animate.exe",
    }

    @property
    def minimum_supported_version(self):
        return "2017"

    def prepare_launch(self, exec_path, args, file_to_open=None):

        required_env = self.compute_environment()

        # Add std context and site info to the env
        std_env = self.get_standard_plugin_environment()
        required_env.update(std_env)

        # override with default project file
        # if file_to_open:
        #     required_env["SGTK_FILE_TO_OPEN"] = file_to_open
        args = os.path.join(self.disk_location, "resources", "Untitled.fla")
        return LaunchInformation(exec_path, args, required_env)

    def scan_software(self):
        self.logger.debug("Scanning for Animate executables...")
        icon_path = os.path.join(
            self.disk_location,
            "icon_256.png"
        )
        self.logger.debug("Using icon path: %s" % (icon_path,))

        if sys.platform not in self.EXECUTABLE_MATCH_TEMPLATES:
            self.logger.debug("Animate not supported on this platform.")
            return []

        all_sw_versions = []

        for executable_path, tokens in self._glob_and_match(
                self.EXECUTABLE_MATCH_TEMPLATES[sys.platform],
                self.COMPONENT_REGEX_LOOKUP):
            self.logger.debug(
                "Processing %s with tokens %s",
                executable_path,
                tokens
            )
            executable_version = tokens.get("version")

            sw_version = SoftwareVersion(
                executable_version,
                "Animate CC",
                executable_path,
                icon_path
            )
            supported, reason = self._is_supported(sw_version)
            if supported:
                all_sw_versions.append(sw_version)
            else:
                self.logger.debug(reason)

        return all_sw_versions

    def compute_environment(self):
        env = {}

        framework_location = self.__get_adobe_framework_location()
        if framework_location is None:
            raise EngineConfigurationError(
                ("The tk-framework-adobe "
                 "could not be found in the current environment. "
                 "Please check the log for more information.")
            )

        self.__ensure_framework_is_installed(framework_location)

        # set the interpreter with which to launch the CC integration
        env["SHOTGUN_ADOBE_PYTHON"] = sys.executable
        env["SHOTGUN_ADOBE_FRAMEWORK_LOCATION"] = framework_location
        env["SHOTGUN_ENGINE"] = "tk-animate"

        # We're going to append all of this Python process's sys.path to the
        # PYTHONPATH environment variable. This will ensure that we have access
        # to all libraries available in this process in subprocesses like the
        # Python process that is spawned by the Shotgun CEP extension on launch
        # of an Adobe host application. We're appending instead of setting because
        # we don't want to stomp on any PYTHONPATH that might already exist that
        # we want to persist when the Python subprocess is spawned.
        sgtk.util.append_path_to_env_var(
            "PYTHONPATH",
            os.pathsep.join(sys.path),
        )
        env["PYTHONPATH"] = os.environ["PYTHONPATH"]

        return env

    def __get_adobe_framework_location(self):
        engine = sgtk.platform.current_engine()
        env_name = engine.environment.get("name")

        env = engine.tank.pipeline_configuration.get_environment(env_name)
        engine_desc = env.get_engine_descriptor("tk-animate")

        if env_name is None:
            self.logger.warn(
                ("The current environment {!r} "
                 "is not configured to run the tk-animate "
                 "engine. Please add the engine to your env-file: "
                 "{!r}").format(env, env.disk_location))
            return

        framework_name = None
        for req_framework in engine_desc.get_required_frameworks():
            if req_framework.get("name") == "tk-framework-adobe":
                name_parts = [req_framework["name"]]
                if "version" in req_framework:
                    name_parts.append(req_framework["version"])
                framework_name = "_".join(name_parts)
                break
        else:
            self.logger.warn(
                ("The engine tk-animate must have "
                 "the tk-framework-adobe configured in order to run"))
            return

        desc = env.get_framework_descriptor(framework_name)
        return desc.get_path()

    def __ensure_framework_is_installed(self, framework_location):

        bootstrap_python_path = os.path.join(framework_location, "python")

        sys.path.insert(0, bootstrap_python_path)
        import tk_framework_adobe_utils.startup as startup_utils
        sys.path.remove(bootstrap_python_path)

        # installing the CEP extension.
        startup_utils.ensure_extension_up_to_date(self.logger)
