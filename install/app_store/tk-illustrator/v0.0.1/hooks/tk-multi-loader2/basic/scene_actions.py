# Copyright (c) 2019 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook that loads defines all the available actions, broken down by publish type. 
"""
import os
import re
import glob


import sgtk


HookBaseClass = sgtk.get_hook_baseclass()


# Name of available actions. Corresponds to both the environment config values and the action instance names.
_IMPORT = "import"

class IllustratorActions(HookBaseClass):

    ##############################################################################################################
    # public interface - to be overridden by deriving classes 

    def generate_actions(self, sg_publish_data, actions, ui_area):
        """
        Returns a list of action instances for a particular publish.
        This method is called each time a user clicks a publish somewhere in the UI.
        The data returned from this hook will be used to populate the actions menu for a publish.

        The mapping between Publish types and actions are kept in a different place
        (in the configuration) so at the point when this hook is called, the loader app
        has already established *which* actions are appropriate for this object.

        The hook should return at least one action for each item passed in via the 
        actions parameter.

        This method needs to return detailed data for those actions, in the form of a list
        of dictionaries, each with name, params, caption and description keys.

        Because you are operating on a particular publish, you may tailor the output 
        (caption, tooltip etc) to contain custom information suitable for this publish.

        The ui_area parameter is a string and indicates where the publish is to be shown. 
        - If it will be shown in the main browsing area, "main" is passed. 
        - If it will be shown in the details area, "details" is passed.
        - If it will be shown in the history area, "history" is passed. 

        Please note that it is perfectly possible to create more than one action "instance" for 
        an action! You can for example do scene introspection - if the action passed in 
        is "character_attachment" you may for example scan the scene, figure out all the nodes
        where this object can be attached and return a list of action instances:
        "attach to left hand", "attach to right hand" etc. In this case, when more than 
        one object is returned for an action, use the params key to pass additional 
        data into the run_action hook.

        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        :param actions: List of action strings which have been defined in the app configuration.
        :param ui_area: String denoting the UI Area (see above).
        :returns List of dictionaries, each with keys name, params, caption and description
        """
        app = self.parent
        app.log_debug("Generate actions called for UI element %s. "
                      "Actions: %s. Publish Data: %s" % (ui_area, actions, sg_publish_data))

        action_instances = []
        try:
            # call base class first
            action_instances += HookBaseClass.generate_actions(self, sg_publish_data, actions, ui_area)
        except AttributeError:
            # base class doesn't have the method, so ignore and continue
            pass
        
        action_instances.append({"name": _IMPORT,
                                 "params": None,
                                 "caption": "Add to project",
                                 "description": "Adds the current item to the project root bin."})
        return action_instances

    def execute_multiple_actions(self, actions):
        """
        Executes the specified action on a list of items.

        The default implementation dispatches each item from ``actions`` to
        the ``execute_action`` method.

        The ``actions`` is a list of dictionaries holding all the actions to
        execute.

        Each entry will have the following values:

            name: Name of the action to execute
            sg_publish_data: Publish information coming from Shotgun
            params: Parameters passed down from the generate_actions hook.

        .. note::
            This is the default entry point for the hook. It reuses the
            ``execute_action`` method for backward compatibility with hooks
            written for the previous version of the loader.

        .. note::
            The hook will stop applying the actions on the selection if an error
            is raised midway through.

        :param list actions: Action dictionaries.
        """
        for single_action in actions:
            name = single_action["name"]
            sg_publish_data = single_action["sg_publish_data"]
            params = single_action["params"]
            self.execute_action(name, params, sg_publish_data)
    
    def _get_path_from_sg_publish_data(self, sg_publish_data):
        return self.get_publish_path(sg_publish_data)

    def execute_action(self, name, params, sg_publish_data):
        """
        Execute a given action. The data sent to this be method will
        represent one of the actions enumerated by the generate_actions method.

        :param name: Action name string representing one of the items returned
                     by generate_actions.
        :param params: Params data, as specified by generate_actions.
        :param sg_publish_data: Shotgun data dictionary with all the standard
                                publish fields.
        """
        app = self.parent
        app.log_debug("Execute action called for action %s. "
                      "Parameters: %s. Publish Data: %s" % (name, params, sg_publish_data))

        # resolve path
        # toolkit uses utf-8 encoded strings internally and the Premiere API expects unicode
        # so convert the path to ensure filenames containing complex characters are supported
        path = self._get_path_from_sg_publish_data(sg_publish_data)
        is_sequence = 0

        if self.parent.engine.is_adobe_sequence(path):
            is_sequence = 1
            frame_range = self.parent.engine.find_sequence_range(path)
            if frame_range:
                glob_path = re.sub("[\[]?([#@]+|%0\d+d)[\]]?", "*{}".format(frame_range[0]), path)
                for each_path in sorted(glob.glob(glob_path)):
                    path = each_path
                    break

        if not os.path.exists(path):
            raise IOError("File not found on disk - '%s'" % path)
  
        if name == _IMPORT:
            self._import(path, is_sequence)


    ###########################################################################
    # helper methods

    def _import(self, path, is_sequence):
        """
        Helper method to add the project to the current project
        """
        adobe = self.parent.engine.adobe
        active_doc = adobe.app.activeDocument
        layer = active_doc.layers.add()
        attach_img = layer.placedItems.add()
        attach_img.file = adobe.File(path)
