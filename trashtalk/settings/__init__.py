# pylint: disable=wildcard-import
import sys
from os.path import join

from .utils import PROJECT_PATH

sys.path.append(PROJECT_PATH)
sys.path.append(join(PROJECT_PATH, 'apps'))
