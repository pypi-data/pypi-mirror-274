import datetime
from TimetableToImage import Timetable


def get_timetable_lesson_from_json(json_lesson: dict) -> Timetable.Lesson:
    """
    Create new Timetable.Lesson object and extract timetable data from json dict.

    :param json_lesson: JSON dict
    :return: Timetable.Lesson object

    JSON dict example:

    {'group': 'ПИбд-21',
       'nameOfLesson': 'Лаб.Операционные '
                       'системы- '
                       '2 п/г',
       'room': '3-418а',
       'teacher': 'Скалкин А '
                  'М'}
    """
    timetable_lesson = Timetable.Lesson()
    timetable_lesson.group = json_lesson["group"].strip()
    timetable_lesson.name = json_lesson["nameOfLesson"].strip()
    timetable_lesson.room = json_lesson["room"].strip()
    timetable_lesson.teacher = json_lesson["teacher"].strip()
    return timetable_lesson


def get_timetable_pair_from_json(json_pair: dict) -> Timetable.Pair:
    """
    Create new Timetable.Pair object and extract timetable data from json dict.

    :param json_pair: JSON pair dict
    :return: Timetable.Pair object

    JSON dict example:

    [{'group': 'ПИбд-21',
       'nameOfLesson': 'пр.Иностранный '
                       'язык',
       'room': '6-502',
       'teacher': 'Зеленова В '
                  'С'},
      {'group': 'ПИбд-21',
       'nameOfLesson': 'пр.Иностранный '
                       'язык',
       'room': '6-503',
       'teacher': 'Макаренко А '
                  'С'}]

		OR

		[{'group': 'ПИбд-21',
           'nameOfLesson': 'Лаб.Операционные '
                           'системы- '
                           '2 п/г',
           'room': '3-418а',
           'teacher': 'Скалкин А '
                      'М'}]
    """
    timetable_pair = Timetable.Pair()
    timetable_pair.lessons = list()
    for json_lesson in json_pair:
        timetable_lesson = get_timetable_lesson_from_json(json_lesson)
        timetable_pair.lessons.append(timetable_lesson)
    return timetable_pair


def get_timetable_day_from_json(json_day: dict) -> Timetable.Day:
    """
    Create new Timetable.Day object and extract timetable data from json dict.

    :param json_day: JSON day dict
    :return: Timetable.Day object

    JSON dict example:
    {'day': 0,
		 'lessons': [[],
					 [],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Физическая '
									   'культура '
									   'и '
									   'спорт',
					   'room': '2-СЗ',
					   'teacher': 'Преподаватели '
								  'кафедры'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Философия',
					   'room': '6-400',
					   'teacher': 'Гильмутдинова '
								  'Н А'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Интернет-программирование- '
									   '2 п/г',
					   'room': '3-431',
					   'teacher': 'Филиппов А '
								  'А'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Интернет-программирование- '
									   '2 п/г',
					   'room': '3-431',
					   'teacher': 'Филиппов А '
								  'А'}],
					 [],
					 []]}
    """
    timetable_day = Timetable.Day()
    timetable_day.pairs = list()
    timetable_day.number = json_day["day"]
    for pair_number, json_pair in enumerate(json_day["lessons"]):
        timetable_pair = get_timetable_pair_from_json(json_pair)
        timetable_pair.number = pair_number
        timetable_day.pairs.append(timetable_pair)
    return timetable_day


def get_timetable_week_from_json(json_week: dict, week_begin: datetime.date = None,
                                 week_end: datetime.date = None) -> Timetable.Week:
    """
    Create new Timetable.Week object and extract timetable data from json dict.

    :param json_week: JSON timetable dict
    :param week_begin: Date of first week day (Morning)
    :param week_end: Date of last week day (Sunday)
    :return: Timetable.Week object

    JSON dict example:
    {'days': [{'day': 0,
		 'lessons': [[],
					 [],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Физическая '
									   'культура '
									   'и '
									   'спорт',
					   'room': '2-СЗ',
					   'teacher': 'Преподаватели '
								  'кафедры'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Философия',
					   'room': '6-400',
					   'teacher': 'Гильмутдинова '
								  'Н А'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Интернет-программирование- '
									   '2 п/г',
					   'room': '3-431',
					   'teacher': 'Филиппов А '
								  'А'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Интернет-программирование- '
									   '2 п/г',
					   'room': '3-431',
					   'teacher': 'Филиппов А '
								  'А'}],
					 [],
					 []]},
		{'day': 1,
		 'lessons': [[{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Разработка '
									   'профессиональных '
									   'приложений- '
									   '1 п/г',
					   'room': '3-431',
					   'teacher': 'Эгов Е Н'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Разработка '
									   'профессиональных '
									   'приложений- '
									   '1 п/г',
					   'room': '3-431',
					   'teacher': 'Эгов Е Н'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Организация '
									   'ЭВМ и '
									   'систем- '
									   '2 п/г',
					   'room': '3-429',
					   'teacher': 'Дырночкин А '
								  'А'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Организация '
									   'ЭВМ и '
									   'систем- '
									   '2 п/г',
					   'room': '3-429',
					   'teacher': 'Дырночкин А '
								  'А'}],
					 [],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'лек.Основы '
									   'теории '
									   'систем',
					   'room': '6 -ДОТ',
					   'teacher': 'Тронин В '
								  'Г'}],
					 [],
					 []]},
		{'day': 2,
		 'lessons': [[],
					 [],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Базы '
									   'данных- '
									   '1 п/г',
					   'room': '3-418а',
					   'teacher': 'Строева Ю '
								  'В'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Базы '
									   'данных- '
									   '1 п/г',
					   'room': '3-418а',
					   'teacher': 'Строева Ю '
								  'В'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Операционные '
									   'системы- '
									   '2 п/г',
					   'room': '3-418а',
					   'teacher': 'Скалкин А '
								  'М'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'Лаб.Операционные '
									   'системы- '
									   '2 п/г',
					   'room': '3-418а',
					   'teacher': 'Скалкин А '
								  'М'}],
					 [],
					 []]},
		{'day': 3,
		 'lessons': [[{'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Иностранный '
									   'язык',
					   'room': '6-502',
					   'teacher': 'Зеленова В '
								  'С'},
					  {'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Иностранный '
									   'язык',
					   'room': '6-503',
					   'teacher': 'Макаренко А '
								  'С'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'пр.Физическая '
									   'культура '
									   'и '
									   'спорт',
					   'room': '2-СЗ',
					   'teacher': 'Преподаватели '
								  'кафедры'}],
					 [],
					 [],
					 [],
					 [],
					 [],
					 []]},
		{'day': 4,
		 'lessons': [[{'group': 'ПИбд-21',
					   'nameOfLesson': 'лек.Базы '
									   'данных',
					   'room': '6 -ДОТ',
					   'teacher': 'Скалкин А '
								  'М'}],
					 [],
					 [],
					 [],
					 [],
					 [],
					 [],
					 []]},
		{'day': 5,
		 'lessons': [[{'group': 'ПИбд-21',
					   'nameOfLesson': 'лек.Теория '
									   'вероятностей '
									   'и '
									   'математическая '
									   'статистика',
					   'room': '2-ДОТ',
					   'teacher': 'Кувайскова '
								  'Ю Е'}],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'лек.Интернет-программирование',
					   'room': '6 -ДОТ',
					   'teacher': 'Филиппов А '
								  'А'}],
					 [],
					 [{'group': 'ПИбд-21',
					   'nameOfLesson': 'лек.Философия',
					   'room': '6 -ДОТ',
					   'teacher': 'Гильмутдинова '
								  'Н А'}],
					 [],
					 [],
					 [],
					 []
				    ]
				}
			]
	    }
    """
    timetable_week = Timetable.Week()
    timetable_week.days = list()
    week_have_dates = False
    if week_begin is not None and week_end is not None:
        if week_end < week_begin:
            raise Exception("Week dates wrong!")
        timetable_week.week_begin = week_begin
        timetable_week.week_end = week_end
        week_have_dates = True
    for json_day in json_week["days"]:
        timetable_day = get_timetable_day_from_json(json_day)
        timetable_week.days.append(timetable_day)
    if week_have_dates:
        timetable_week.set_period(week_begin, week_end)
    return timetable_week


def get_timetable_bell_from_json(json_bell: dict) -> Timetable.Bell:
    """
    Create new Timetable.Bell object and extract bell data from json dict.


    :param json_bell: JSON bell dict
    :return: Timetable.Bell object

    JSON dict example:

    {
      "begin": {
        "hour": 8,
        "minute": 30
      },
      "end": {
        "hour": 9,
        "minute": 50
      }
    }
    """
    json_begin_time = json_bell["begin"]
    json_end_time = json_bell["end"]
    begin_time = datetime.time(hour=json_begin_time["hour"], minute=json_begin_time["minute"])
    end_time = datetime.time(hour=json_end_time["hour"], minute=json_end_time["minute"])
    timetable_bell = Timetable.Bell(begin_time, end_time)
    return timetable_bell


def get_timetable_bells_from_json(json_bells: dict) -> Timetable.Bells:
    """
    Create new Timetable.Bells object and extract bells data from json dict.


    :param json_bells: JSON bells dict
    :return: Timetable.Bells object

    JSON dict example:

    {
        "0": {
        "begin": {
        "hour": 8,
        "minute": 30
        },
        "end": {
        "hour": 9,
        "minute": 50
        }
        },
        "1": {
          "begin": {
            "hour": 10,
            "minute": 0
          },
          "end": {
            "hour": 11,
            "minute": 20
          }
        },
        "2": {
          "begin": {
            "hour": 11,
            "minute": 30
          },
          "end": {
            "hour": 12,
            "minute": 50
          }
        },
        "3": {
          "begin": {
            "hour": 13,
            "minute": 30
          },
          "end": {
            "hour": 14,
            "minute": 50
          }
        },
        "4": {
          "begin": {
            "hour": 15,
            "minute": 0
          },
          "end": {
            "hour": 16,
            "minute": 20
          }
        },
        "5": {
          "begin": {
            "hour": 16,
            "minute": 30
          },
          "end": {
            "hour": 17,
            "minute": 50
          }
        },
        "6": {
          "begin": {
            "hour": 18,
            "minute": 0
          },
          "end": {
            "hour": 19,
            "minute": 20
          }
        },
        "7": {
          "begin": {
            "hour": 19,
            "minute": 30
          },
          "end": {
            "hour": 20,
            "minute": 50
          }
        }
    }

    """
    timetable_bells = Timetable.Bells()
    timetable_bells.bells = list()
    for number, json_bell in json_bells.items():
        timetable_bell = get_timetable_bell_from_json(json_bell)
        timetable_bell.number = int(number)
        timetable_bells.bells.append(timetable_bell)
    return timetable_bells
