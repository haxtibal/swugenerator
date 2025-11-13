import io
import os

import pytest

from swugenerator import swu_file


@pytest.fixture
def artifact(tmp_path):
    artifact_path = tmp_path / "artifact.txt"
    with open(artifact_path, "wb") as artifact:
        artifact.write(b"f00d")
    return artifact_path


def test_write_header_64bit_inode(artifact, monkeypatch):
    def _stat(*_args, **_kwargs):
        class StatResult:
            st_dev = 42
            st_gid = 1000
            st_ino = 0xAAAAAAAA12345678
            st_mode = 33204
            st_nlink = 1
            st_rdev = 0
            st_size = 4
            st_uid = 1000

        return StatResult

    virtual_cpio = io.BytesIO()
    virtual_swu_file = swu_file.SWUFile(virtual_cpio)
    monkeypatch.setattr(os, "stat", _stat)
    virtual_swu_file.write_header(artifact)
    assert virtual_cpio.getvalue() == (
        b'070702'
        b'12345678000081B4000003E8000003E80000000100000000'
        b'00000004000000000000002A00000000000000000000000D'
        b'0000012Aartifact.txt\x00'
    )
