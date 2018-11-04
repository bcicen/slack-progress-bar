# -*- coding: utf-8 -*-
import pytest
import responses

from slack_progress import ProgressBar, SlackProgress


@pytest.fixture
def slack_token():
    return 'fake/token'


@pytest.fixture
def slack_channel():
    return 'general'

@pytest.fixture
def postMessage_response():
    return {
        "ok": True,
        "channel": "C1H9RESGL",
        "ts": "1503435956.000247",
        "message": {
            "text": "Here's a message for you",
            "username": "ecto1",
            "bot_id": "B19LU7CSY",
            "attachments": [
                {
                    "text": "This is an attachment",
                    "id": 1,
                    "fallback": "This is an attachment's fallback"
                }
            ],
            "type": "message",
            "subtype": "bot_message",
            "ts": "1503435956.000247"
        }
    }


def test_make_bar(slack_token, slack_channel):
    # default bar character
    f_char = '⬛'
    sp = SlackProgress(slack_token, slack_channel)
    assert  '{} 50%'.format(f_char * 10) == sp._makebar(50)

    # custom bar character
    f_char = 'X'
    sp = SlackProgress(
        slack_token, slack_channel, fill_char='X', empty_char='_',
    )
    assert  '{} 50%'.format(f_char * 10) == sp._makebar(50)


def test_full_width_bar(slack_token, slack_channel):
    # default bar character
    f_char = '⬛'
    e_char='⬜'
    sp = SlackProgress(slack_token, slack_channel, full_width=True)
    assert  '{}{} 50%'.format(
        f_char * 10, e_char * 10
    ) == sp._makebar(50)

    # custom bar character
    f_char = 'X'
    e_char = '_'
    sp = SlackProgress(
        slack_token, slack_channel, full_width=True, fill_char='X',
        empty_char='_',
    )
    assert  '{}{} 50%'.format(
        f_char * 10, e_char * 10
    ) == sp._makebar(50)


@responses.activate
def test_create_bar(slack_token, slack_channel, postMessage_response):
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(
            responses.POST,
            'https://slack.com/api/chat.postMessage',
            status=200, json=postMessage_response,
        )
        sp = SlackProgress(slack_token, slack_channel)
        bar = sp.new()
        assert isinstance(bar, ProgressBar)
