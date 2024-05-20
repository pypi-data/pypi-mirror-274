import logging
import subprocess as sp


logger = logging.getLogger(__name__)


class PackageInfo(object):
    _version = None
    version_cmd = None
    version_file = None

    @classmethod
    def version(klass):

        if klass._version is None:
            if klass.version_cmd is not None:
                try:
                    raw_info = sp.check_output(klass.version_cmd, shell=True).decode(
                        "utf-8"
                    )
                except IOError:
                    return None

            elif klass.version_file is not None:
                try:
                    with open(klass.version_file, "rt") as fobj:
                        raw_info = fobj.read()
                except OSError:
                    return None
            else:
                return None
            klass._version = klass.parse_version(raw_info)
        return klass._version

    @staticmethod
    def parse_version(raw_info):

        raise NotImplementedError
