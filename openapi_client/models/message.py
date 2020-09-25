# coding: utf-8

"""
    TamTam Bot API

    # About Bot API allows bots to interact with TamTam. Methods are called by sending HTTPS requests to [botapi.tamtam.chat](https://botapi.tamtam.chat) domain. Bots are third-party applications that use TamTam features. A bot can legitimately take part in a conversation. It can be achieved through HTTP requests to the TamTam Bot API.  ## Features TamTam bots of the current version are able to: - Communicate with users and respond to requests - Recommend users complete actions via programmed buttons - Request personal data from users (name, short reference, phone number) We'll keep working on expanding bot capabilities in the future.  ## Examples Bots can be used for the following purposes: - Providing support, answering frequently asked questions - Sending typical information - Voting - Likes/dislikes - Following external links - Forwarding a user to a chat/channel  ## @PrimeBot [PrimeBot](https://tt.me/primebot) is the main bot in TamTam, all bots creator. Use PrimeBot to create and edit your bots. Feel free to contact us for any questions, [@support](https://tt.me/support) or [team@tamtam.chat](mailto:team@tamtam.chat).  #### [PrimeBot](https://tt.me/primebot) commands: `/start` &mdash; start a dialog with a bot  `/create` &mdash; create a bot, assign the unique short name to it (from 4 to 64 characters)  `/set_name [name]` &mdash; assign a short or full name to the bot (up to 200 characters)  `/set_description [description]` &mdash; enter the description for the bot profile (up to 400 characters)  `/set_picture [URL]` &mdash; enter the URL of bot's picture  `/delete [username]` &mdash; delete the bot  `/list` &mdash; show the list of all bots  `/get_token` &mdash; obtain a token for a bot  `/revoke` &mdash; request a new token  `/help` &mdash; help  ## HTTP verbs `GET` &mdash; getting resources, parameters are transmitted via URL  `POST` &mdash; creation of resources (for example, sending new messages)  `PUT` &mdash; editing resources  `DELETE` &mdash; deleting resources  `PATCH` &mdash; patching resources  ## HTTP response codes `200` &mdash; successful operation  `400` &mdash; invalid request  `401` &mdash; authentication error  `404` &mdash; resource not found  `405` &mdash; method is not allowed  `429` &mdash; the number of requests is exceeded  `503` &mdash; service unavailable  ## Resources format For content requests (PUT and POST) and responses, the API uses the JSON format. All strings are UTF-8 encoded. Date/time fields are represented as the number of milliseconds that have elapsed since 00:00 January 1, 1970 in the long format. To get it, you can simply multiply the UNIX timestamp by 1000. All date/time fields have a UTC timezone. ## Error responses In case of an error, the API returns a response with the corresponding HTTP code and JSON with the following fields:  `code` - the string with the error key  `message` - a string describing the error </br>  For example: ```bash > http https://botapi.tamtam.chat/chats?access_token={EXAMPLE_TOKEN} HTTP / 1.1 403 Forbidden Cache-Control: no-cache Connection: Keep-Alive Content-Length: 57 Content-Type: application / json; charset = utf-8 Set-Cookie: web_ui_lang = ru; Path = /; Domain = .tamtam.chat; Expires = 2019-03-24T11: 45: 36.500Z {    \"code\": \"verify.token\",    \"message\": \"Invalid access_token\" } ``` ## Receiving Notifications TamTam Bot API supports 2 options of receiving notifications on new dialog events for bots: - Push notifications via WebHook. To receive data via WebHook, you'll have to [add subscription](https://dev.tamtam.chat/#operation/subscribe); - Notifications upon request via [long polling](#operation/getUpdates) API. All data can be received via long polling **by default** after creating the bot,  Both methods **cannot** be used simultaneously. Refer to the response schema of [/updates](https://dev.tamtam.chat/#operation/getUpdates) method to check all available types of updates.  ## Message buttons You can program buttons for users answering a bot. TamTam supports the following types of buttons:  `callback` &mdash; sends a notification to a bot (via WebHook or long polling)  `link` &mdash; makes a user to follow a link  `request_contact` &mdash; requests the user permission to access contact information (phone number, short link, email)  You may also send a message with an [InlineKeyboard]() type attachment to start creating buttons. When the user presses a button, the bot receives the answer with filled callback field. It is recommended to edit that message so the user can receive updated buttons.  # Versioning API models and interface may change over time. To make sure your bot will get the right info, we strongly recommend adding API version number to each request. You can add it as `v` parameter to each HTTP-request. For instance, `v=0.1.2`. To specify the data model version you are getting through WebHook subscription, use the `version` property in the request body of the [subscribe](https://dev.tamtam.chat/#operation/subscribe) request.  # Libraries We have created [Java library](https://github.com/tamtam-chat/tamtam-bot-api) to make using API easier.  # Changelog ##### Version 0.1.9 - Added method to [get chat administrators](#operation/getAdmins) - For `type: dialog` chats [added](https://github.com/tamtam-chat/tamtam-bot-api-schema/commit/ff9e2472941d4dd2de540db0d0ea8b9c3d0ed01a#diff-7e9de78f42fb0d2ae80878b90c87300aR1160) `dialog_with_user` - Added `url` for [messages](https://github.com/tamtam-chat/tamtam-bot-api-schema/commit/137dd9dfa4e583d429f017ba69c20caa9deac105) in public chats/channels - [**Removed**](https://github.com/tamtam-chat/tamtam-bot-api-schema/commit/ff9e2472941d4dd2de540db0d0ea8b9c3d0ed01a) `callback_id` of `InlineKeyboardAttachment` - [**Removed**](https://github.com/tamtam-chat/tamtam-bot-api-schema/commit/2ebf36b22758ea3487304f5b0d0d811798e78b61) `user_id` of `CallbackAnswer`. It is no longer required. Just use `callback_id` of `Callback` - Several minor improvements: check [diff](https://github.com/tamtam-chat/tamtam-bot-api-schema/compare/beccbe5f4fbed32182a13e257ca1cfae7f40ea8d...master) for all changes  ##### Version 0.1.8 - Added `code`, `width`, `height` to [StickerAttachment](https://github.com/tamtam-chat/tamtam-bot-api-schema/blob/master/schema.yaml#L1580) - `token` is now only one required property for video/audio/file attachments - `sender` and `chat_id` of [LinkedMessage](https://github.com/tamtam-chat/tamtam-bot-api-schema/blob/master/schema.yaml#L1401) are now optional - Added clarifying `message` to [SimpleQueryResult](https://github.com/tamtam-chat/tamtam-bot-api-schema/blob/master/schema.yaml#L1938)  ##### Version 0.1.7 - It is now **required** to pass `marker` parameter in [/updates](#operation/getUpdates) requests, except initial - Added full `User` object to update types: bot_started, bot_added, bot_removed, user_added, user_removed, chat_title_changed - Added `size` and `filename` to [`FileAttachment`](https://github.com/tamtam-chat/tamtam-bot-api-schema/blob/master/schema.yaml#L1503) - Added [`token`](https://github.com/tamtam-chat/tamtam-bot-api-schema/blob/master/schema.yaml#L1525) property to video/audio/file attachments allows you to reuse attachments uploaded by another user  ##### Version 0.1.6 - Added method to [edit bot info](#operation/editMyInfo) - Added statistics for messages in channel - `Message.sender` and `UserWithPhoto.avatar_url/full_avatar_url` removed from required properties  # noqa: E501

    OpenAPI spec version: 0.1.10
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Message(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'sender': 'User',
        'recipient': 'Recipient',
        'timestamp': 'int',
        'link': 'LinkedMessage',
        'body': 'MessageBody',
        'stat': 'MessageStat',
        'url': 'str'
    }

    attribute_map = {
        'sender': 'sender',
        'recipient': 'recipient',
        'timestamp': 'timestamp',
        'link': 'link',
        'body': 'body',
        'stat': 'stat',
        'url': 'url'
    }

    def __init__(self, sender=None, recipient=None, timestamp=None, link=None, body=None, stat=None, url=None):  # noqa: E501
        """Message - a model defined in OpenAPI"""  # noqa: E501

        self._sender = None
        self._recipient = None
        self._timestamp = None
        self._link = None
        self._body = None
        self._stat = None
        self._url = None
        self.discriminator = None

        if sender is not None:
            self.sender = sender
        self.recipient = recipient
        self.timestamp = timestamp
        self.link = link
        self.body = body
        self.stat = stat
        self.url = url

    @property
    def sender(self):
        """Gets the sender of this Message.  # noqa: E501

        User who sent this message. Can be `null` if message has been posted on behalf of a channel  # noqa: E501

        :return: The sender of this Message.  # noqa: E501
        :rtype: User
        """
        return self._sender

    @sender.setter
    def sender(self, sender):
        """Sets the sender of this Message.

        User who sent this message. Can be `null` if message has been posted on behalf of a channel  # noqa: E501

        :param sender: The sender of this Message.  # noqa: E501
        :type: User
        """

        self._sender = sender

    @property
    def recipient(self):
        """Gets the recipient of this Message.  # noqa: E501

        Message recipient. Could be user or chat  # noqa: E501

        :return: The recipient of this Message.  # noqa: E501
        :rtype: Recipient
        """
        return self._recipient

    @recipient.setter
    def recipient(self, recipient):
        """Sets the recipient of this Message.

        Message recipient. Could be user or chat  # noqa: E501

        :param recipient: The recipient of this Message.  # noqa: E501
        :type: Recipient
        """
        if recipient is None:
            raise ValueError("Invalid value for `recipient`, must not be `None`")  # noqa: E501

        self._recipient = recipient

    @property
    def timestamp(self):
        """Gets the timestamp of this Message.  # noqa: E501

        Unix-time when message was created  # noqa: E501

        :return: The timestamp of this Message.  # noqa: E501
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Message.

        Unix-time when message was created  # noqa: E501

        :param timestamp: The timestamp of this Message.  # noqa: E501
        :type: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def link(self):
        """Gets the link of this Message.  # noqa: E501

        Forwarder or replied message  # noqa: E501

        :return: The link of this Message.  # noqa: E501
        :rtype: LinkedMessage
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this Message.

        Forwarder or replied message  # noqa: E501

        :param link: The link of this Message.  # noqa: E501
        :type: LinkedMessage
        """

        self._link = link

    @property
    def body(self):
        """Gets the body of this Message.  # noqa: E501

        Body of created message. Text + attachments. Could be null if message contains only forwarded message  # noqa: E501

        :return: The body of this Message.  # noqa: E501
        :rtype: MessageBody
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this Message.

        Body of created message. Text + attachments. Could be null if message contains only forwarded message  # noqa: E501

        :param body: The body of this Message.  # noqa: E501
        :type: MessageBody
        """
        if body is None:
            raise ValueError("Invalid value for `body`, must not be `None`")  # noqa: E501

        self._body = body

    @property
    def stat(self):
        """Gets the stat of this Message.  # noqa: E501

        Message statistics. Available only for channels in [GET:/messages](#operation/getMessages) context  # noqa: E501

        :return: The stat of this Message.  # noqa: E501
        :rtype: MessageStat
        """
        return self._stat

    @stat.setter
    def stat(self, stat):
        """Sets the stat of this Message.

        Message statistics. Available only for channels in [GET:/messages](#operation/getMessages) context  # noqa: E501

        :param stat: The stat of this Message.  # noqa: E501
        :type: MessageStat
        """

        self._stat = stat

    @property
    def url(self):
        """Gets the url of this Message.  # noqa: E501

        Message public URL. Can be `null` for dialogs or non-public chats/channels  # noqa: E501

        :return: The url of this Message.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Message.

        Message public URL. Can be `null` for dialogs or non-public chats/channels  # noqa: E501

        :param url: The url of this Message.  # noqa: E501
        :type: str
        """

        self._url = url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Message):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other