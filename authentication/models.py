from dataclasses import dataclass

SPECIAL_PERMISSIONS = frozenset(
    {
        "signin",
        "gdsadministrator",
        "authorityadministrator",
    }
)


@dataclass(frozen=True)
class LicensifyUser:
    uid: str
    email: str
    display_name: str
    permissions: tuple[str, ...]

    @property
    def is_authenticated(self) -> bool:
        return "signin" in self.permissions


@dataclass(frozen=True)
class AnonymousLicensifyUser:
    is_authenticated: bool = False
