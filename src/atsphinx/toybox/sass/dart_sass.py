"""dart-sass resolver."""

import platform
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import httpx

OS_NAME = Literal["android", "linux", "macos", "windows"]
ARCH_NAME = Literal[
    "arm",
    "arm-musl",
    "arm64",
    "arm64-musl",
    "ia32",
    "ia32-musl",
    "riscv64",
    "riscv64-musl",
    "x64",
    "x64-musl",
]


@dataclass
class Release:
    """Release base information for GitHub."""

    os: OS_NAME
    arch: ARCH_NAME
    version: str

    @classmethod
    def from_platform(cls, version: str) -> "Release":
        """Create object from runtime information."""
        os_name = resolve_os()
        arch_name = resolve_arch()
        return cls(os=os_name, arch=arch_name, version=version)

    @property
    def archive_url(self) -> str:
        """Retrieve URL for archive of GitHub Releases."""
        return f"https://github.com/sass/dart-sass/releases/download/{self.version}/dart-sass-{self.version}-{self.os}-{self.arch}.{self.file_ext}"

    @property
    def archive_format(self) -> str:
        """String of ``shutil.unpack_archive``."""
        return "zip" if self.os == "windows" else "gztar"

    @property
    def file_ext(self) -> str:
        """File format as extension."""
        return "zip" if self.os == "windows" else "tar.gz"

    @property
    def bin_ext(self) -> str:
        """Extension of executable file."""
        return ".exe" if self.os == "windows" else ""


def resolve_os() -> OS_NAME:
    """Retrieve os name as dart-sass specified."""
    os_name = platform.system()
    if os_name == "Darwin":
        return "macos"
    if os_name in ("Linux", "Windows", "Android"):
        return os_name.lower()  # type: ignore[return-value]
    raise Exception(f"There is not dart-sass binary for {os_name}")


def resolve_arch() -> ARCH_NAME:
    """Retrieve cpu architecture string as dart-sass specified."""
    # NOTE: This logic is not all covered.
    arch_name = platform.machine()
    if arch_name == "x86_64":
        arch_name = "x64"
    if arch_name.startswith("arm") and arch_name != "arm64":
        arch_name = "arm"
    libc = platform.libc_ver()
    arch_suffix = "-musi" if "musl" in libc[0] else ""
    return f"{arch_name}{arch_suffix}"  # type: ignore[return-value]


def setup_dart_sass(version: str, dist: Path) -> Path:
    """If executable is not exists, download archive."""
    release = Release.from_platform(version)
    fullpath = dist / "dart-sass" / f"sass{release.bin_ext}"
    if not fullpath.exists():
        resp = httpx.get(release.archive_url, follow_redirects=True)
        archive_path = Path(tempfile.mktemp())
        archive_path.write_bytes(resp.content)
        shutil.unpack_archive(archive_path, dist, release.archive_format)
    return fullpath
