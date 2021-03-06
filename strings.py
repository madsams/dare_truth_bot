from typing import Optional, Union, Callable, List


class StringsTextBtn:
    def __init__(self, text: Union[str, Callable[..., str]], buttons: Optional[dict]):
        self.text = text
        self.buttons = buttons


class Commands:
    def __init__(self, start: StringsTextBtn):
        self.start = start


class Callbacks:
    def __init__(self,
                 bot_link_btn: str,
                 not_recognized: str,
                 not_found_alert: str,
                 before_start: Callable[[any], str],
                 choose_type: StringsTextBtn,
                 question: StringsTextBtn,
                 vote: StringsTextBtn):
        self.bot_link_btn = bot_link_btn
        self.not_recognized = not_recognized
        self.not_found_alert = not_found_alert
        self.before_start = before_start
        self.choose_type = choose_type
        self.question = question
        self.vote = vote


def create_game_inline_query_text(game) -> str:
    inviter = game.inviter.name
    members = game.members
    text = "سلام\n\n" \
           "شما توسط {} به دعوت بازی جرات حقیقت شده‌اید\n\n" \
           "در صورت تمایل به بازی کردن، دکمه 'منم هستم' را بزنید\n\n" \
           "افراد حاضر در بازی:\n\n".format(inviter)
    for i, m in enumerate(members, start=1):
        text += "{}: {} \n".format(i, m.name)
    return text


def create_game_choose_text(game) -> str:
    user = game.turn.name
    text = "نوبت {}:\n\n" \
           "یکی رو انتخاب کن:\n\n".format(user)
    return text


dtc = {
    'dare': 'جرات',
    'truth': 'حقیقت',
}


def create_game_answer_text(game, is_repeated: Optional[bool] = False) -> str:
    user_name: str = game.turn.name
    dtc_type: str = game.question.type
    question: str = game.question.text
    dtc_text = dtc[dtc_type]
    repeat_question = "کاربر '{}'! اعضا با جواب شما قانع نشدن\nلطفا دوباره جواب بدید\n\n".format(user_name)
    new_question = "کاربر '{}' {} رو انتخاب کرد\n\n".format(user_name, dtc_text)
    text = repeat_question if is_repeated else new_question
    text += "متن سوال:\n\n" \
            "{}\n\n" \
            "بعد جواب دادن دکمه جواب دادم رو بزن\n\n".format(question)

    return text


def create_game_vote_text(game) -> str:
    yes: List[str] = [x.name for x in game.yes_list]
    no: List[str] = [x.name for x in game.no_list]
    remained: List[str] = [x.name for x in game.members if x.name not in (yes + no) and x.id != game.turn.id]
    answered_user = game.turn.name

    def get_percent(numerator: List):
        percent = len(numerator) * 100.0 / (len(yes) + len(no) + len(remained))
        return "{:.2f}".format(percent)

    text = "کاربر '{}' دکمه جواب دادم رو زد\n\n" \
           "آیا جواب داده شده قانع‌کننده بود؟\n\n" \
           "بله({}): {}\n\n" \
           "خیر({}): {}\n\n" \
           "افراد باقی مانده: {}\n\n".format(answered_user,
                                             get_percent(yes),
                                             make_csv(yes),
                                             get_percent(no),
                                             make_csv(no),
                                             make_csv(remained))
    return text


def make_csv(yes):
    return ','.join(yes)


class Conversations:
    def __init__(self, send_question_type: StringsTextBtn, enter_question_text: str, send_question_success: str):
        self.send_question_type = send_question_type
        self.enter_question_text = enter_question_text
        self.send_question_success = send_question_success


class Inline:
    def __init__(self, button: str, query_result: StringsTextBtn):
        self.button = button
        self.query_result = query_result


class GameAlerts:
    def __init__(self, ur_not_member: str, start_minimum: str, start_non_inviter: str, already_got_in: str,
                 successfully_got_in: str,
                 not_ur_turn: str, cannot_vote_ur_turn: str, voted_before: str, vote_successful: str):
        self.ur_not_member = ur_not_member
        self.start_minimum = start_minimum
        self.start_non_inviter = start_non_inviter
        self.already_got_in = already_got_in
        self.successfully_got_in = successfully_got_in
        self.not_ur_turn = not_ur_turn
        self.cannot_vote_ur_turn = cannot_vote_ur_turn
        self.voted_before = voted_before
        self.vote_successful = vote_successful


class Game:
    def __init__(self, alert: GameAlerts):
        self.alert = alert


class Strings:
    def __init__(self, commands: Commands, callbacks: Callbacks, conversations: Conversations, inline: Inline,
                 game: Game):
        self.commands = commands
        self.callbacks = callbacks
        self.conversations = conversations
        self.game = game
        self.inline = inline


strings: Strings = Strings(
    Commands(
        StringsTextBtn(
            'سلام\nبه ربات جرات حقیقت خوش اومدین!\nبرای شروع روی یکی از دکمه‌های زیر بزنین:',
            {
                'help': 'راهنما',
                'play': 'بازی',
                'send_question': 'ارسال سوال'
            }
        )
    ),
    Callbacks(
        'بات جرات-حقیقت',
        'عملکرد شناسایی نشد!',
        'ان شا اللّه بزودی آماده می‌شه :))',
        create_game_inline_query_text,
        StringsTextBtn(
            create_game_choose_text,
            dtc
        ),
        StringsTextBtn(
            create_game_answer_text,
            {
                'answered': 'جواب دادم',
            }
        ),
        StringsTextBtn(
            create_game_vote_text,
            {
                'yes': 'بله',
                'no': 'نه',
            }
        )
    ),
    Conversations(
        StringsTextBtn(
            'نوع سوالی که میخواهید بفرستید را انتخاب کنید',
            dtc
        ),
        'متن سوال پیشنهادی را تایپ کنید',
        'ممنون از شما\nسوال شما پس از بررسی اضافه خواد شد'
    ),
    Inline(
        "ارسال",
        StringsTextBtn(
            create_game_inline_query_text,
            {
                'start': 'شروع بازی',
                'get_in': 'منم هستم'
            }
        )
    ),
    Game(
        GameAlerts(
            "شما عضو بازی نیستید!",
            "باید تعداد بیشتری عضو بشن",
            "فقط دعوت‌کننده است که میتونه شروع کنه",
            "شما قبلا عضو شدی",
            "عضو شدی\nصبر کن تا دعوت‌کننده شروع کنه",
            "اکنون نوبت شما نیست",
            "نمیتوانید به خودتان رای دهید",
            "فقط یک بار رای می‌توان رای داد!",
            "رای شما ثبت شد"
        )
    )
)
