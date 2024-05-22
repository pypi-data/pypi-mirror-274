from typing import List, Tuple, Union, Optional, Callable, Iterable

import numpy as np

from ._base import BaseNotes
from ._utils import get_repr_notes
from .notes import Note
from .envelope import Envelope


class Track(BaseNotes):
    def __init__(
        self,
        sequence: List[Note],
        waveform: Optional[Union[str, Callable]] = None,
        duration: Optional[float] = None,
        unit: Optional[str] = None,
        bpm: Optional[float] = None,
        envelope: Optional[Envelope] = None,
        duty: Optional[float] = None,
        width: Optional[float] = None,
        amp: Optional[float] = None,
        sr: int = 22050,
        A4: float = 440.,
    ):
        """
        Track class. Manage multiple notes as a sequence. If inputed
        specific arguments or set default attributes, these apply to all
        notes in the sequence when rendering. If not, each note will be
        rendered with its own attributes.

        Similar to the Note class, it is possible to generate waveforms
        using render() and sin().

        Args:
            sequence (List[Note]): sequence of notes.
            envelope (Envelope, optional):
                Envelope of the track notes. Defaults to Envelope() with
                attack=0.01, decay=0., sustain=1., release=0.01,
                hold=0..
            amp (float, optional):
                Amplitude of each note in the Track. Note that this
                value is not amplitude of this Track. Defaults to None.

        \Attributes:
            - sequence (List[Note]): sequence of notes.

        Examples:
            >>> import munotes as mn
            >>> track = mn.Track([
            >>>     mn.Note("C4"),
            >>>     mn.Note("D4"),
            >>>     mn.Note("E4"),
            >>>     mn.Chord("C"),
            >>> ])
            >>> track
            Track (notes: Note C4, Note D4, Note E4, Note C4, Note E4, Note G4)

            >>> track.sin()
            array([ 0.        ,  0.07448499,  0.14855616, ..., -0.01429455,
                -0.00726152, -0.        ])
        """
        self.sequence = sequence
        self._notes = sequence
        self._init_attrs(
            waveform=waveform,
            duration=duration,
            unit=unit,
            bpm=bpm,
            envelope= envelope or Envelope(
                attack=0.01,
                decay=0.,
                sustain=1.,
                release=0.01,
                hold=0.,
            ),
            duty=duty,
            width=width,
            amp=amp,
            sr=sr,
            A4=A4,
        )

    def render(
        self,
        waveform: Optional[Union[str, Callable]] = None,
        duration: Optional[float] = None,
        unit: Optional[str] = None,
        bpm: Optional[float] = None,
        envelope: Optional[Envelope] = None,
        duty: Optional[float] = None,
        width: Optional[float] = None,
        amp: Optional[float] = None,
    ) -> np.ndarray:
        """
        Rendering waveform of the track. Notes in the track are
        concatenated and rendered.
        """
        y = np.array([])
        envelope = envelope or self.envelope
        release = envelope.release
        release_samples = int(self.sr * release)
        for note in self:
            y_note = note.render(
                waveform=waveform or self.waveform,
                duration=duration or self.duration,
                unit=unit or self.unit,
                bpm=bpm or self.bpm,
                envelope=envelope or self.envelope,
                duty=duty if duty is not None else self.duty,
                width=width if width is not None else self.width,
                amp = amp if amp is not None else self.amp,
            )
            if len(y):
                y = np.append(y, np.zeros(len(y_note) - release_samples))
                y[-len(y_note):] += y_note
            else:
                y = y_note
        return y

    def append(self, *notes: Note) -> None:
        """
        Append notes to the track.

        Args:
            *notes (Note): notes to append

        Example:
            >>> track = mn.Track([
            >>>     mn.Note("C4", duration=1),
            >>>     mn.Note("D4", duration=1),
            >>> ])
            >>> track.append(mn.Note("E4", duration=1))
            Track (notes: Note C4, Note D4, Note E4)
        """
        self.sequence = [*self.sequence, *notes]
        self._notes = self.sequence

    def __len__(self) -> int:
        return len(self.sequence)

    def __iter__(self) -> Iterable:
        return iter(self.sequence)

    def __getitem__(self, index: int) -> Tuple[Note, float]:
        return self.sequence[index]

    def __repr__(self) -> str:
        return get_repr_notes(self, name="Track")


class Stream(BaseNotes):
    def __init__(
        self,
        tracks: List[Track],
        waveform: Optional[Union[str, Callable]] = None,
        duration: Optional[float] = None,
        unit: Optional[str] = None,
        bpm: Optional[float] = None,
        envelope: Optional[Envelope] = None,
        duty: Optional[float] = None,
        width: Optional[float] = None,
        amp: Optional[float] = None,
        sr: int = 22050,
        A4: float = 440,
    ):
        """
        Stream class. Manage multiple tracks as a stream.

        Args:
            tracks (List[Track]): tracks
            amp (float, optional):
                Amplitude of each note in the Stream. Note that this
                value is not amplitude of this Stream. Defaults to None.

        \Attributes:
            - tracks (List[Track]): tracks

        Example:
            >>> melody = mn.Track([
            >>>     mn.Note("C4"),
            >>>     mn.Note("D4"),
            >>>     mn.Note("E4"),
            >>> ])
            >>> chords = mn.Track([mn.Chord("C", duration=3)])
            >>> stream = mn.Stream([melody, chords])
            >>> stream
            Stream (notes: Note C4, Note D4, Note E4, Note C4, Note E4, Note G4)

            >>> stream.render('sin')
            array([ 0.        ,  0.35422835,  0.70541282, ..., -0.02489362,
                   -0.01173826,  0.        ])

            >>> stream.render([
            >>>     'square',
            >>>     lambda t: np.sin(t) + np.sin(2*t)
            >>> ])
            array([ 1.        ,  1.83660002,  2.64969075, ..., -0.05431521,
                   -0.02542138,  0.        ])
        """
        self.tracks = tracks
        self._notes = tracks
        self._init_attrs(
            waveform=waveform,
            duration=duration,
            unit=unit,
            bpm=bpm,
            envelope=envelope,
            duty=duty,
            width=width,
            amp=amp,
            sr=sr,
            A4=A4,
        )

    def render(
        self,
        waveform: Optional[Union[str, Callable]] = None,
        duration: Optional[float] = None,
        unit: Optional[str] = None,
        bpm: Optional[float] = None,
        envelope: Optional[Envelope] = None,
        duty: Optional[float] = None,
        width: Optional[float] = None,
        amp: Optional[float] = None,
    ) -> np.ndarray:
        """
        Rendering waveform of the track. Track in the stream are
        rendered simultaneously.
        """
        y = np.array([])
        for track in self:
            y_track = track.render(
                waveform=waveform or self.waveform,
                duration=duration or self.duration,
                unit=unit or self.unit,
                bpm=bpm or self.bpm,
                envelope=envelope or self.envelope,
                duty=duty if duty is not None else self.duty,
                width=width if width is not None else self.width,
                amp = amp if amp is not None else self.amp,
            )
            if len(y_track) > len(y):
                y = np.append(y, np.zeros(len(y_track) - len(y)))
            else:
                y_track = np.append(y_track, np.zeros(len(y) - len(y_track)))
            y += y_track
        return y

    def append(self, *tracks: Track) -> None:
        self.tracks.extend(tracks)
        self._notes = self.tracks

    def __len__(self) -> int:
        return len(self.tracks)

    def __iter__(self) -> Iterable:
        return iter(self.tracks)

    def __getitem__(self, index: int) -> Track:
        return self.tracks[index]

    def __repr__(self) -> str:
        return get_repr_notes(self, name="Stream")
