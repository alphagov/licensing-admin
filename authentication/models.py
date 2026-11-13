from dataclasses import dataclass


@dataclass(frozen=True)
class LicensifyUser:
    uid: str
    email: str
    display_name: str
    permissions: tuple[str, ...]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_gds_admin(self) -> bool:
        return "gdsadministrator" in self.permissions

    @property
    def authorities(self) -> frozenset[str]:
        system_roles = {"signin", "gdsadministrator"}
        return frozenset(self.permissions) - system_roles

    def can_access_authority(self, authority_slug: str) -> bool:
        return self.is_gds_admin or authority_slug in self.authorities


@dataclass(frozen=True)
class AnonymousLicensifyUser:
    is_authenticated: bool = False
    is_gds_admin: bool = False
    authorities: frozenset = frozenset()

    def can_access_authority(self, authority_slug: str) -> bool:
        return False
