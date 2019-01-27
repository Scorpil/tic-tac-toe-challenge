from dataclasses import dataclass, field
from uuid import uuid4

from tictactoe.models import User
from tictactoe.storage import Storage


@dataclass
class FakeGame:
    uid: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self):
        return {'uid': self.uid}


@dataclass
class FakeRequest:
    body: str = field(default='')


@dataclass
class FakeHandler:
    current_user: User = field(default=None)
    request: FakeRequest = field(default_factory=lambda: FakeRequest())
    storage: Storage = field(default_factory=lambda: Storage())
    game: FakeGame = field(default=None)
    output: str = field(default=None)

    def write(self, output):
        self.output = output


def fake_method(self, *args, **kwargs):
    return {
        'self': self,
        'args': args,
        'kwargs': kwargs
    }


def assert_decorates(decorator, self_,
                     in_args=None,
                     in_kwargs=None,
                     out_args=None,
                     out_kwargs=None):
    in_args = in_args or (1, 2, 3)
    in_kwargs = in_kwargs or {'kwarg1': 1, 'kwarg2': 2}

    out_args = out_args if out_args is not None else in_args
    out_kwargs = out_kwargs if out_kwargs is not None else in_kwargs

    decorated = decorator(fake_method)
    result = decorated(self_, *in_args, **in_kwargs)
    assert result['args'] == out_args
    assert result['kwargs'] == out_kwargs
