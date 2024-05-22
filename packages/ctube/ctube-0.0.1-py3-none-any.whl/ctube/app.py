import os
import sys
import shutil
import pydub
import eyed3
from typing import List, Optional, Tuple, Union
from innertube.clients import InnerTube
from innertube.errors import RequestError

from ctube.download import Downloader
from ctube.terminal import Prompt
from ctube.errors import InvalidIndexSyntax, InvalidSyntax
from ctube.containers import MusicItem
from ctube.colors import color, Color
from ctube.download import Data
from ctube.extractors import (
    extract_artist_id, 
    extract_artist_music
)
from ctube.decorators import (
    handle_invalid_index_syntax,
    handle_main_function,
)


class App:
    PREFIXES = {
        "search": "ARTIST_NAME (Search by artist name)",
        "id":     "ARTIST_ID (Search by artist ID)",
        "exit":   "Exit the program",
        "help":   "Print the help message"
    }

    def __init__(
            self, 
            output_path: str,
            skip_existing: bool = True,
    ):
        self.client = InnerTube("WEB_REMIX")
        self.prompt = Prompt()
        self.downloader = Downloader(
            output_path=output_path, 
            skip_existing=skip_existing,
            on_complete_callback=on_complete_callback,
            on_progress_callback=on_progress_callback
        )

        # last search
        self._music_items: Optional[List[MusicItem]] = None
        self._artist_name: Optional[str] = None

    @handle_main_function
    def main_loop(self) -> None:
        print_header()
        while True:
            user_input = self.prompt.get_input()
            if not user_input:
                continue

            res = self.get_filtered_input(user_input)

            if not res:
                continue
            else:
                mode, arg = res

            if mode == "exit":
                exit()
            elif mode == "help":
                print(color("Usage", Color.GREEN))
                print(
                    '\n'.join(
                        [
                            f"{color(prefix, Color.BLUE)}: {desc}" 
                            for prefix, desc in self.PREFIXES.items()
                        ]
                    )
                )
            elif mode == "search" or mode == "id":
                search_res = self.do_search(mode, arg)
                if search_res:
                    self._music_items, self._artist_name = search_res

            elif self._music_items and self._artist_name:
                filtered_items = get_filtered_music_items(self._music_items, user_input)
                if filtered_items:
                    print(color(f"Selected items:", Color.BLUE))
                    for item in filtered_items:
                        print(color(f"\u2022 {item.title}", Color.BOLD))

                    for item in filtered_items:
                        print(color(f":: Downloading: {item.title}", Color.GREEN))
                        self.downloader.download(item=item, artist=self._artist_name)
            else:
                print(color("Invalid syntax", Color.RED))

    def do_search(self, mode: str, arg: str) -> Optional[Tuple[List[MusicItem], str]]:
        if mode == "search":
            data = self.client.search(query=arg)
            artist_id = extract_artist_id(data)
            if not artist_id:
                print(color(f"Artist '{arg}' not found", Color.RED))
                return
        elif mode == "id":
            artist_id = arg
        else:
            raise InvalidSyntax

        try:
            artist_music_data = self.client.browse(browse_id=f"MPAD{artist_id}")
        except RequestError:
            print(color(f"Invalid ID: {artist_id}", Color.RED))
        else:
            res = extract_artist_music(artist_music_data)
            if not res:
                print(color(f"Content not found", Color.RED))
            else:
                music_items, artist_name = res
                print(color(f"Collected music for {artist_name}", Color.GREEN))
                print_music_items(music_items)
                return music_items, artist_name

    def get_filtered_input(self, user_input: str) -> Tuple[str, str]:
        splitted_user_input = user_input.split()
        prefix = splitted_user_input[0]
        arg = ' '.join(splitted_user_input[1:])
        return prefix, arg


def print_header() -> None:
    print(color("Clitube", Color.GREEN))
    print(f"Source: {color("https://github.com/g3nsy/clitube", Color.BLUE)}")
    print("Version: 1.0.0")
    print("Type 'help' for a list of available commands")


def print_music_items(music_items: List[MusicItem]) -> None:
    terminal_columns = shutil.get_terminal_size().columns
    max_index_len = len(str(len(music_items)))
    space_for_title = terminal_columns - max_index_len - 3  # [, ], ' '
    for i, music_item in enumerate(music_items):
        if len(music_item.title) > space_for_title:
            title = f"{music_item.title[:space_for_title - 3]}..."
        else:
            title = music_item.title
        lb = color("[", Color.BLUE)
        rb = color("]", Color.BLUE)
        ci = color(str(i), Color.GREEN)
        print(f"{lb}{ci}{rb}{' ' * (1 + max_index_len - len(str(i)))}{title}")


@handle_invalid_index_syntax
def get_filtered_music_items(music_items: List[MusicItem], user_input: str) -> Optional[List[MusicItem]]:
    selected_indexes = get_selected_indexes(user_input)
    if not selected_indexes:
        return music_items

    elif isinstance(selected_indexes, slice):
        selected_music_items = music_items[selected_indexes]
        if not selected_music_items:
            if selected_indexes.start == selected_indexes.stop + 1:
                print(color("Invalid index", Color.RED))
            else:
                print(color("Invalid slice", Color.RED))
        else:
            return selected_music_items
    else:
        incorrect_indexes: List[int] = []
        for index in selected_indexes:
            if index >= len(music_items):
                incorrect_indexes.append(index)
        if incorrect_indexes:
            print(f"Invalid indexes: {', '.join(map(str, incorrect_indexes))}")
        else:
            return [music_items[index] for index in selected_indexes]


def get_selected_indexes(string: str) -> Optional[Union[slice, List[int]]]:
    if not string:
        return None

    else:
        # x
        if string.isdigit():
            return slice(int(string), int(string) + 1)

        # x: y
        double_points_splitted_string = string.split(":")
        if len(double_points_splitted_string) > 1:
            if len(double_points_splitted_string) != 2:
                raise InvalidIndexSyntax

            first, second = double_points_splitted_string
            
            if not first.isdigit() or not second.isdigit():
                raise InvalidIndexSyntax

            first, second = int(first), int(second)

            if first < 0 or second < 0 or second <= first:
                raise InvalidIndexSyntax

            return slice(first, second)

        # x, y, ..., z
        comma_splitted_string = string.split(",")
        if len(comma_splitted_string) > 1:
            try:
                indexes = list(map(int, comma_splitted_string))
            except ValueError:
                raise InvalidIndexSyntax

            filtered_indexes: List[int] = []
            for index in indexes:
                if index < 0:
                    raise InvalidIndexSyntax
                if index not in filtered_indexes:
                    filtered_indexes.append(index)

            return filtered_indexes

        raise InvalidIndexSyntax


def on_progress_callback(
        data: Data,
        filesize: int, 
        bytes_received: int, 
) -> None:
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * 0.40)
    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = "#" * filled + "-" * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)

    distance_from_bar = columns - (max_width + 9)  # len bar + percentage len
    title = f":: {data.title} "

    if len(title) > distance_from_bar:
        title = f"{title[:distance_from_bar - 4]}... "
    else:
        title = f"{title}{' ' * (distance_from_bar - len(title))}"

    text = f"{title}[{progress_bar}] {percent}%\r"

    sys.stdout.write(text)
    sys.stdout.flush()


def on_complete_callback(data: Data) -> None:
    output = f"{os.path.splitext(data.filepath)[0]}.mp3"

    mp4 = pydub.AudioSegment.from_file(data.filepath, "mp4")
    mp4.export(output, format="mp3")

    audio = eyed3.load(output)
    if audio and audio.tag:
        audio.tag.title = data.title
        audio.tag.artist = data.artist
        audio.tag.album = data.album
        audio.tag.release_year = data.release_year
        audio.tag.tracks_num = data.tracks_num
        audio.tag.images.set(3, data.image_data, "image/jpeg", u"cover")
        audio.tag.save()
        
    os.remove(data.filepath)
    print()


def exit():
    sys.stdout.write('\033[?25h')
    sys.exit(0)
