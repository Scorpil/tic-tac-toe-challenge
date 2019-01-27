from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class User:
    name: str
    uid: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.uid
        }

    def __repr__(self):
        return f'[ User | name: {self.name}, id: {self.uid} ]'

    @staticmethod
    def from_dict(data):
        return User(data['name'], data['id'])
