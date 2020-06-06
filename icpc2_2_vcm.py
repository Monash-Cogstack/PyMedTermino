# -*- coding: utf-8 -*-
# PyMedTermino
# Copyright (C) 2012-2013 Jean-Baptiste LAMY
# LIMICS (Laboratoire d'informatique médicale et d'ingénierie des connaissances en santé), UMR_S 1142
# University Paris 13, Sorbonne paris-Cité, Bobigny, France

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ["icpc2_2_vcm", "vcm_2_icpc2"]

import os, os.path
from pymedtermino       import *
from pymedtermino.icpc2 import *
from pymedtermino.vcm   import *
from pymedtermino.vcm   import VCMLexiconIndex

icpc2_2_vcm = SQLMapping(ICPC2, VCM, os.path.join(DATA_DIR, "icpc2_2_vcm.sqlite3"), has_and = 0)
icpc2_2_vcm.register()
vcm_2_icpc2 = icpc2_2_vcm._create_reverse_mapping()
vcm_2_icpc2.register()

ICPC2.vcm_lexicon_index = VCMLexiconIndex(ICPC2, os.path.join(DATA_DIR, "icpc2_vcm_lexicon_index.sqlite3"))
