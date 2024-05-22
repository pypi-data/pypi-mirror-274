#
# rbfly - a library for RabbitMQ Streams using Python asyncio
#
# Copyright (C) 2021-2024 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Basic types for RabbitMQ Streams implementation.
"""

import asyncio
import dataclasses as dtc
import typing as tp

from ..amqp import MessageCtx
from ._mqueue import MessageQueue
from .offset import Offset

class PublishErrorInfo(tp.NamedTuple):
    """
    Error information received from RabbitMQ Streams broker after
    publishing a message.
    """
    publisher_id: int
    errors: tuple[tuple[int, int], ...]

@dtc.dataclass(frozen=True, slots=True)
class PublisherInfo:
    """
    Publisher information.

    The data is used to recreate a stream publisher.

    :var stream: RabbitMQ stream name.
    :var name: Publisher name.
    """
    stream: str
    name: str

class PSubscriber(tp.Protocol):
    """
    Interface for a subscriber class.
    """
    queue: MessageQueue
    next_offset: int

    def reset(self, offset: Offset) -> Offset: ...
    def messages_received(self, protocol: tp.Any) -> None: ...

@dtc.dataclass(slots=True)
class SubscriptionInfo:
    """
    Subscription information.

    The data is used to resubscribe to a stream after connection failure.

    :var stream: RabbitMQ stream name.
    :var offset: RabbitMQ Streams offset specification used to subscribe to
        a stream.
    :var amqp: Messages are in AMQP 1.0 format if true. Otherwise no AMQP
        decoding.
    :var subscriber: Stream subscriber.
    """
    stream: str
    offset: Offset
    amqp: bool
    subscriber: PSubscriber

    @property
    def task(self) -> asyncio.Future[None]:
        return self.subscriber.queue.task

__all__ = ['MessageCtx']

# vim: sw=4:et:ai
