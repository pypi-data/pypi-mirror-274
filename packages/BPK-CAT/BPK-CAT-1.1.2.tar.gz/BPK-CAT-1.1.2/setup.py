from setuptools import setup


NAME="BPK-CAT"
MAYOR=1 
MINOR=1
PATCH=2
VERSION= '%d.%d.%d' % (MAYOR, MINOR, PATCH)

DESCRIPTION="Orange3 BPK Computer Assisted Audit Technique Tools (CAATT)"
AUTHOR="BPK-RI"
AUTHOR_EMAIL="eppid@bpk.go.id"
URL="https://www.bpk.go.id/"

ENTRY_POINTS = {
    'orange.widgets':(
        'BPK CAT = bpkcat'
    )
}

PACKAGES=['bpkcat']
PACKAGE_DATA = {
    "bpkcat" : ["icons/*.svg"]
}

setup(
    name=NAME,
    description=DESCRIPTION,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    entry_points=ENTRY_POINTS
)