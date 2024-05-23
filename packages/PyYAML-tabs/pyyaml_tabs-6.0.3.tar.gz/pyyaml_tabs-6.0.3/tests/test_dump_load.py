import sys
from pathlib import Path

current_dir = Path(__file__).parent
parent_dir = current_dir.parent

sys.path.append(str(parent_dir))
from lib import yaml

import pytest
#import yaml

def test_dump():
    assert yaml.dump(['foo'])

def test_load_no_loader():
    with pytest.raises(TypeError):
        yaml.load("- foo\n")


def test_load_safeloader():
    assert yaml.load("- foo\n", Loader=yaml.SafeLoader)

def test_tabs():
    o = yaml.safe_load("""
test: |
\tline1:
\t\tline2:
""")
    print(o)

test_tabs()
