from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserData:
    name: str
    username: str
    email: str
    password: str
