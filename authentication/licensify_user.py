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

    @property
    def is_gds_admin(self) -> bool:
        return "gdsadministrator" in self.permissions

    @property
    def is_authority_admin(self) -> bool:
        return "authorityadministrator" in self.permissions

    @property
    def authorities(self) -> frozenset[str]:
        return frozenset(self.permissions) - SPECIAL_PERMISSIONS

    def can_access_authority(self, authority_slug: str) -> bool:
        return self.is_gds_admin or authority_slug.lower() in self.authorities


@dataclass(frozen=True)
class AnonymousLicensifyUser:
    is_authenticated: bool = False
    is_gds_admin: bool = False
    is_authority_admin: bool = False
    authorities: frozenset[str] = frozenset()

    def can_access_authority(self, authority_slug: str) -> bool:
        return False
