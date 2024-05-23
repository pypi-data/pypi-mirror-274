import os
import copy
import datetime
import textwrap
from typing import Tuple

from TimetableToImage import Timetable
from PIL import Image, ImageDraw, ImageFont


def get_multiline_text_size(
        text_string: str,
        font: ImageFont.FreeTypeFont,
        interval: float = 1.0) -> Tuple[float, float]:
    """
    Calculate size (width, height) of multiline text by text and font

    :param interval:
    :param text_string:
    :param font:
    :return: Tuple of width and height
    """
    text_string = text_string.strip()
    if not text_string:
        return 0, 0
    # https://stackoverflow.com/a/46220683/9263761
    strings = text_string.split('\n')
    text_width = 0
    ascent, descent = font.getmetrics()
    for line in strings:
        text_width = max(font.getmask(line).getbbox()[2], text_width)
    text_height = (ascent + descent) * len(strings)
    return text_width, text_height * interval


def get_shifts_to_place_center(text: str, font: ImageFont.FreeTypeFont,
                               place_width: float = None,
                               place_height: float = None,
                               interval: float = 1.0) -> Tuple[float, float]:
    """
    Returns shift for draw text center of place

    :param interval:
    :param text:
    :param font:
    :param place_width:
    :param place_height:
    :return: tuple of shifts
    """
    text_width, text_height = get_multiline_text_size(text, font, interval=interval)

    shift_x = None
    shift_y = None

    if place_width is not None:
        shift_x = (place_width - text_width) / 2
    if place_height is not None:
        shift_y = (place_height - text_height) / 2

    return shift_x, shift_y


def get_splitted_string(lesson: Timetable.Lesson, limit: int) -> str:
    """
    Return lesson text splitted by symbols limit in string

    :param lesson:
    :param limit:
    :return:
    """
    string = ""
    try:
        room = ""
        for letter in lesson.room:
            if letter != ' ':
                room += letter

        teacher = lesson.teacher
        teacher_words = teacher.split()
        teacher_flag = True
        if len(teacher_words) != 2:
            teacher_flag = False

        name = lesson.name
        if teacher_flag:
            t = ', '.join([name, teacher, room])
        else:
            t = name

        if teacher_flag:
            return textwrap.fill(text=t, width=limit)

        t_lines = textwrap.wrap(text=t, width=limit)

        if t_lines:
            last_line = t_lines[-1]
        else:
            last_line = ""

        t_last_line = last_line + ', ' + teacher
        t_wrap = textwrap.wrap(text=t_last_line, width=limit)
        if len(t_wrap) > 1:
            if len(textwrap.wrap(text=teacher + ',', width=limit)) == 1:
                t_lines[-1] += ','
                t_lines.append(teacher)

        else:
            if t_lines:
                t_lines.pop()
            t_lines += t_wrap

        last_line = t_lines[-1]
        t_last = last_line + ', ' + room
        if len(textwrap.wrap(text=t_last, width=limit)) == 1:
            t_lines[-1] = t_last
        else:
            t_lines[-1] += ',\n' + room

        string = '\n'.join(t_lines)

        string = string.strip()

    except Exception:
        string = ', '.join([lesson.name, lesson.teacher, lesson.room])
        string = textwrap.wrap(text=string, width=limit)

    return string


def get_table_row_letters_count(font: ImageFont.FreeTypeFont, column_width: float) -> int:
    """
    Function calculate letters number in row with font by average symbol
    :param font:
    :param column_width:
    :return: letters count
    """
    text_width = 0
    letters_count = 0
    while text_width < column_width:
        letters_count += 1
        text_width, _ = get_multiline_text_size("д" * letters_count, font)
    return letters_count - 1


def draw_multiline_text(
        text: str,
        draw: ImageDraw.ImageDraw,
        position: Tuple[float, float],
        font: ImageFont.FreeTypeFont,
        color: Tuple[int, int, int],
        centered: bool = False,
        interval: float = 1.0) -> None:
    if not text:
        return
    text_split = text.split("\n")
    x_left, y_top = position
    line_width = 0
    line_height = 0
    for line in text_split:
        tw, th = get_multiline_text_size(line, font, interval)
        line_width = max(tw, line_width)
        line_height = max(th, line_height)
    punc = ",. "
    for i, line in enumerate(text_split):
        if line[0] in punc:
            line = line[1:].strip()
        draw.text(
            xy=(
                x_left + ((line_width - get_multiline_text_size(line, font, interval)[
                    0]) / 2 if centered else 0),
                y_top + line_height * interval * i
            ),
            text=line,
            fill=color,
            font=font
        )


def draw_pair_on_image(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont,
                       color: Tuple[int, int, int], pair: Timetable.Pair,
                       x_left_cell: float, y_top_cell: float,
                       width_cell: float, height_cell: float,
                       lines_width: float = 0) -> None:
    # If not lessons in pair - return
    if len(pair.lessons) == 0:
        return
    # Interval between lines
    interval = 0.9
    # Calculate truth pair size and position
    width_lesson = width_cell - lines_width
    height_pair = height_cell - lines_width
    x_left_lesson = x_left_cell + lines_width / 2
    y_top_pair = y_top_cell + lines_width / 2

    # Optimizing lessons name (next same lesson name removed)
    i = 0
    optimized_lessons = []
    while i < len(pair.lessons):
        curr_lesson: Timetable.Lesson = copy.copy(pair.lessons[i])
        if i != 0:
            prev_lesson: Timetable.Lesson = pair.lessons[i - 1]
            if prev_lesson.name == curr_lesson.name:
                new_lesson = Timetable.Lesson()
                new_lesson.name = ""
                new_lesson.group = prev_lesson.group
                new_lesson.teacher = prev_lesson.teacher
                new_lesson.room = prev_lesson.room
                optimized_lessons[-1].teacher = ""
                optimized_lessons[-1].room = ""
                optimized_lessons.append(new_lesson)
                curr_lesson.name = ""
        optimized_lessons.append(curr_lesson)
        i += 1

    # Calculate lessons height
    height_lesson = height_pair / len(optimized_lessons)

    # Optimal drawing lessons in cell
    for i, lesson in enumerate(optimized_lessons):
        y_top_lesson = y_top_pair + height_lesson * i
        text_lesson_split_height = 0
        text_lesson_split = ""
        font_lesson = font
        first = True
        while (text_lesson_split_height > height_lesson or first) and font_lesson.size > 9:
            if not first:
                font_lesson = ImageFont.truetype(
                    font_lesson.path,
                    font_lesson.size - 1
                )
            first = False
            letters_count_limit = get_table_row_letters_count(
                font_lesson, width_lesson
            )
            text_lesson_split = get_splitted_string(lesson, letters_count_limit)
            text_lesson_split_width, text_lesson_split_height = get_multiline_text_size(
                text_lesson_split, font, interval
            )

        x_shift_lesson, y_shift_lesson = get_shifts_to_place_center(
            text_lesson_split, font_lesson,
            place_width=width_lesson,
            place_height=height_lesson,
            interval=interval
        )
        draw_multiline_text(
            position=(
                x_left_lesson + x_shift_lesson,
                y_top_lesson + y_shift_lesson
            ),
            text=text_lesson_split,
            font=font_lesson,
            color=color,
            centered=True,
            draw=draw,
            interval=interval
        )


def generate_from_timetable_week(
        timetable_week: Timetable.Week,
        timetable_bells: Timetable.Bells = None,
        inverted: bool = False,
        text_promotion: str = None,
        eng_lang: bool = False,
        font_path: str = None,
        resolution: Tuple[int, int] = (1920, 1080)) -> Image:
    """
    Generate FULL-HD image of timetable

    :param resolution: resolution of result image (default FullHD: 1920x1080)
    :param font_path: path to font
    :param timetable_week: Timetable.Week object
    :param timetable_bells: Timetable.Bells object
    :param inverted: set night theme of image
    :param text_promotion: promotion text on image
    :param eng_lang: set English language of headers and articles
    :return:
    """
    width, height = resolution
    full_hd = True if resolution == (1920, 1080) else False
    #
    have_bells = False
    if timetable_bells is not None:
        have_bells = True
    #
    font_size_article = 28 if not full_hd else 38
    font_size_header = 18 if not full_hd else 30
    font_size_table = 13 if not full_hd else 21
    #
    color_white = (255, 255, 255)
    color_black = (0, 0, 0)
    content_color = color_black
    background_color = color_white
    table_lines_width = 2 if not full_hd else 4
    if inverted:
        content_color = (202, 202, 232)
        background_color = (23, 33, 43)
        table_lines_width = 1 if not full_hd else 2
    #
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font_folder = "Golos-UI"
    #
    font_path_regular = os.path.join(os.path.dirname(__file__), "fonts", font_folder,
                                     "font_regular.ttf")
    font_path_medium = os.path.join(os.path.dirname(__file__), "fonts", font_folder,
                                    "font_medium.ttf")
    font_path_bold = os.path.join(os.path.dirname(__file__), "fonts", font_folder,
                                  "font_bold.ttf")
    #
    font_exist = True
    if not (os.path.exists(font_path_regular) and
            os.path.exists(font_path_medium) and
            os.path.exists(font_path_bold)):
        font_exist = False
        print(font_path_regular, font_path_medium, font_path_bold)
    #
    if font_path is not None or not font_exist:
        if font_path is not None:
            if not os.path.exists(font_path):
                font_path = "calibri.ttf"
        else:
            font_path = "calibri.ttf"
        font_path_regular = font_path
        font_path_medium = font_path
        font_path_bold = font_path
    #
    font_regular_article = ImageFont.truetype(
        font_path_regular, font_size_article)
    font_bold_article = ImageFont.truetype(
        font_path_bold, font_size_article)
    #
    font_regular_header = ImageFont.truetype(
        font_path_regular, font_size_header)
    font_bold_header = ImageFont.truetype(
        font_path_bold, font_size_header)
    #
    font_regular_table = ImageFont.truetype(
        font_path_regular, font_size_table)
    #
    article_height_k = 1.5
    table_header_row_height_k = 1.4
    table_header_rows_count = 2
    table_rows_count = 6
    table_left_header_width = get_multiline_text_size("00.00", font_bold_header)[0] + 20  # 60
    table_cols_count = 8
    x_left_text_article = 5
    y_top_table_header = font_size_article * article_height_k
    # article promotion
    if text_promotion is not None:
        text_width, _ = get_multiline_text_size(text_promotion, font_regular_article)
        shift_x, shift_y = get_shifts_to_place_center(
            text_promotion, font_regular_article,
            place_width=width, place_height=y_top_table_header)
        draw.text((shift_x, shift_y), text_promotion,
                  font=font_regular_article,
                  fill=content_color)

    if timetable_week.group:
        text_timetable_for_group = "Расписание группы: "
        if eng_lang:
            text_timetable_for_group = "Timetable for group: "
        # article "Timetable group: "
        _, shift_y = get_shifts_to_place_center(text_timetable_for_group, font_regular_article,
                                                place_height=y_top_table_header)
        draw.text((x_left_text_article, shift_y), text_timetable_for_group,
                  font=font_regular_article,
                  fill=content_color)
        # article group name
        x_left_text_group_name, _ = get_multiline_text_size(text_timetable_for_group,
                                                            font_regular_article)
        _, shift_y = get_shifts_to_place_center(timetable_week.group, font_bold_article,
                                                place_height=y_top_table_header)
        draw.text((x_left_text_article + x_left_text_group_name + 20, shift_y), timetable_week.group,
                  font=font_bold_article,
                  fill=content_color)
    x_left_text_week = width
    # article week number
    if timetable_week.number is not None:
        text_week = "Неделя:"
        if eng_lang:
            text_week = "Week:"
        _, shift_y = get_shifts_to_place_center(text_week, font_regular_article,
                                                place_height=y_top_table_header)
        t_w, t_h = get_multiline_text_size(text_week, font_regular_article)
        x_left_text_week = width - 10 - 10 - get_multiline_text_size("99", font_bold_article)[
            0] - t_w
        draw.text((x_left_text_week, shift_y), text_week,
                  font=font_regular_article,
                  fill=content_color)
        shift_x, shift_y = get_shifts_to_place_center(
            str(timetable_week.number), font_bold_article,
            place_width=10 + 10 + get_multiline_text_size("99", font_bold_article)[0],
            place_height=y_top_table_header)
        t_w, t_h = get_multiline_text_size(str(timetable_week.number), font_bold_article)
        draw.text((width - t_w - shift_x, shift_y), str(timetable_week.number),
                  font=font_bold_article,
                  fill=content_color)

    # article week dates
    if timetable_week.begin is not None and timetable_week.end is not None:
        week_begin = timetable_week.begin.strftime("%d.%m")
        week_end = timetable_week.end.strftime("%d.%m")
        text_period = f"{week_begin} - {week_end}"
        text_period_width, _ = get_multiline_text_size(text_period, font_bold_article)
        _, shift_y = get_shifts_to_place_center(text_period, font_bold_article,
                                                place_height=y_top_table_header)
        draw.text((x_left_text_week - 20 - text_period_width, shift_y), text_period,
                  font=font_bold_article,
                  fill=content_color)

    # horizontal header
    for i in range(table_header_rows_count):
        draw.line((0, y_top_table_header + font_size_header * table_header_row_height_k * i, width,
                   y_top_table_header + font_size_header * table_header_row_height_k * i),
                  fill=content_color, width=table_lines_width)

    # horizontal table
    y_top_table = y_top_table_header + \
                  font_size_header * table_header_row_height_k * table_header_rows_count
    table_row_height = (height - y_top_table) / table_rows_count
    for i in range(table_rows_count):
        draw.line((0, y_top_table + table_row_height * i, width, y_top_table + table_row_height * i),
                  fill=content_color, width=table_lines_width)

    # vertical header + table
    x_left_table = table_left_header_width
    table_col_width = (width - table_left_header_width) / table_cols_count
    for i in range(table_cols_count):
        draw.line((x_left_table + table_col_width * i, y_top_table_header,
                   x_left_table + table_col_width * i, height), fill=content_color,
                  width=table_lines_width)

    # text pair
    text_pair = "Пара"
    if eng_lang:
        text_pair = "Pair"
    shift_x, shift_y = get_shifts_to_place_center(
        text_pair, font_regular_header,
        place_width=x_left_table,
        place_height=font_size_header * table_header_row_height_k)
    draw.text((shift_x - table_lines_width / 2, y_top_table_header + shift_y), text_pair,
              font=font_regular_header, fill=content_color)

    # text time
    text_time = "Время"
    if eng_lang:
        text_time = "Time"
    shift_x, shift_y = get_shifts_to_place_center(
        text_time, font_regular_header,
        place_width=x_left_table,
        place_height=font_size_header * table_header_row_height_k)
    draw.text((shift_x - table_lines_width / 2,
               y_top_table_header + font_size_header * table_header_row_height_k + shift_y),
              text_time,
              font=font_regular_header, fill=content_color)

    # pair number and time
    for i in range(table_cols_count):
        shift_x, shift_y = get_shifts_to_place_center(
            str(i + 1), font_regular_header,
            place_width=table_col_width,
            place_height=font_size_header * table_header_row_height_k)
        draw.text((x_left_table + table_col_width * i + shift_x, y_top_table_header + shift_y),
                  str(i + 1),
                  font=font_regular_header, fill=content_color)
        if have_bells:
            bell = timetable_bells.bells[i]
            bell: Timetable.Bell
            text_time = f"{bell.begin.strftime('%H:%M')}-{bell.end.strftime('%H:%M')}"
            shift_x, shift_y = get_shifts_to_place_center(
                text_time, font_regular_header,
                place_width=table_col_width,
                place_height=font_size_header * table_header_row_height_k)
            draw.text((x_left_table + table_col_width * i + shift_x,
                       y_top_table_header + font_size_header * table_header_row_height_k + shift_y),
                      text_time,
                      font=font_regular_header, fill=content_color)
    DAYS_NAME = Timetable.Week.DAYS_NAME_RU
    if eng_lang:
        DAYS_NAME = Timetable.Week.DAYS_NAME_EN
    # pairs by days
    for i in range(len(timetable_week.days)):
        timetable_day = timetable_week.days[i]
        timetable_day: Timetable.Day
        text_day = DAYS_NAME[i]
        # if date set - write it
        if timetable_day.date is not None:
            day_date = timetable_day.date
            day_date: datetime.date
            text_date = day_date.strftime("%d.%m")
            text_day += "\n" + text_date
        # write day of week
        x_shift, y_shift = get_shifts_to_place_center(
            text_day,
            font_bold_header,
            place_width=x_left_table,
            place_height=int(table_row_height)
        )
        draw.text((x_shift - table_lines_width, y_top_table + y_shift + table_row_height * i),
                  text_day, font=font_bold_header, fill=content_color, align="center")
        # write timetable
        for j, timetable_pair in enumerate(timetable_day.pairs):
            timetable_pair: Timetable.Pair
            draw_pair_on_image(
                draw,
                font_regular_table,
                content_color,
                timetable_pair,
                x_left_table + table_col_width * j,
                y_top_table + table_row_height * i,
                table_col_width,
                table_row_height,
                table_lines_width
            )
    #
    return image
