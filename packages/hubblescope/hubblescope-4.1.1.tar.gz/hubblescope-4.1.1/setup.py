from hubblescope import NAME, VERSION, DESCRIPTION
from blueness.pypi import setup

setup(
    filename=__file__,
    repo_name="hubblescope",
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[NAME],
)
