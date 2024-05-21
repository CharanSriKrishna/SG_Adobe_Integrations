
class SessionInfo(object):

    def __init__(self, engine):
       self._engine = engine

    def __get_transitions(self, track_items, timebase):
        items = list()
        for i in track_items:
            item = dict(
                name=i.name,
                duration=i.duration.ticks/timebase,
                start=i.start.ticks/timebase,
                end=i.end.ticks/timebase,
                mediaType=i.mediaType,
                speed=i.getSpeed(),
            )
            items.append(item)
        return items

    def __get_track_items(self, track_items, timebase):
        # import sgtk
        # import os
        # engine = sgtk.platform.current_engine()
        items = list()

        for i in track_items:
            clip_name = i.name
            
            getMediaPath_clip = i.projectItem.getMediaPath() if hasattr(i.projectItem, 'getMediaPath') else None
            canChangeMediaPath = i.projectItem.canChangeMediaPath() if hasattr(i.projectItem, 'canChangeMediaPath') else None

            item = dict(
                # shot_exists = shot_exists,
                name=i.name,
                duration=i.duration.ticks/timebase,
                start=i.start.ticks/timebase,
                end=i.end.ticks/timebase,
                inPoint=i.inPoint.ticks/timebase,
                outPoint=i.outPoint.ticks/timebase,
                mediaType=i.mediaType,
                # sym_link_entity=sym_link_entity,
                source_path_clip=getMediaPath_clip,
                # canChangeMediaPath = canChangeMediaPath,
                # videoComponents=videoComponents,
                isSelected = i.isSelected(),
                speed=i.getSpeed(),
                isAdjustmentLayer=i.isAdjustmentLayer()
            )

            items.append(item)

        return items

    def __get_tracks(self, sequence_tracks, timebase):
        tracks = list()
        for t in sequence_tracks:
            track = dict(
                id=t.id,
                name=t.name,
                mediaType=t.mediaType,
                clips=self.__get_track_items(t.clips, timebase),
                transitions=self.__get_transitions(t.transitions, timebase),
                isMuted=t.isMuted()
            )
            tracks.append(track)
        return tracks

    def __get_sequences(self, project_sequences):
        sequences = list()
        prj = self._engine.adobe.app.project
        active_seq = prj.activeSequence
        for s in project_sequences:
            # get info just for active sequence
            if s.name == active_seq.name: 
                timebase = s.timebase
                sequence = dict(
                    sequenceID=s.sequenceID,
                    name=s.name,
                    inPoint=s.getInPointAsTime().ticks/timebase,
                    outPoint=s.getOutPointAsTime().ticks/timebase,
                    timebase=s.timebase,
                    zeroPoint=s.zeroPoint/timebase,
                    end=s.end/timebase,
                    videoTracks=self.__get_tracks(s.videoTracks, timebase),
                    audioTracks=self.__get_tracks(s.audioTracks, timebase)
                )
                sequences.append(sequence)
        return sequences

    def get_info(self):
        session_info = list()
        for p in self._engine.adobe.app.projects:
                project = dict(
                    documentID=p.documentID,
                    name=p.name,
                    path=p.path,
                    sequences=self.__get_sequences(p.sequences),
                    activeSequence=p.activeSequence
                )
                session_info.append(project)
        return session_info
