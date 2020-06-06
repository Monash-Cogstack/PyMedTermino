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

from __future__ import print_function

import pymedtermino
pymedtermino.LANGUAGE = "fr"

from pymedtermino          import *
from pymedtermino.icd10    import *
from pymedtermino.snomedct import *
from pymedtermino.meddra   import *
from pymedtermino.vcm      import *
from pymedtermino.cdf      import *
from pymedtermino.snomedct_2_vcm import *
from pymedtermino.icd10_2_vcm import *
from pymedtermino.snomedct_2_icd10 import *
from pymedtermino.cdf_2_meddra import *
from pymedtermino.umls import *
from pymedtermino.icpc2 import *
from pymedtermino.icpc2_2_vcm import *

pymedtermino.REMOVE_SUPPRESSED_CONCEPTS = 1

connect_to_theriaque_db()

#connect_to_umls_db("10.10.100.12", "jiba", "vicking", "umls")
#UMLS_SNOMEDCT  = UMLS_AUI.extract_terminology("SNOMEDCT", has_int_code = 1)
UMLS_ICD10     = UMLS_AUI.extract_terminology("ICD10")
#UMLS_ICPC2EENG = UMLS_AUI.extract_terminology("ICPC2EENG")
#UMLS_ICPC2P    = UMLS_AUI.extract_terminology("ICPC2P")
UMLS_ATC       = UMLS_AUI.extract_terminology("ATC_2013")

from pymedtermino.umls import db_cursor

if 0:
  import time
  
  t = time.time()
  nb = 0
  for i in ICD10.all_concepts(): nb += 1
  t = time.time() - t
  print(nb, "concepts")
  print(t, "s")
  print(nb / t, "ICD10 concepts / seconds")
  
  t = time.time()
  nb = 0
  for i in SNOMEDCT[123037004].descendants_no_double(): nb += 1
  t = time.time() - t
  print(nb, "concepts")
  print(t, "s")
  print(nb / t, "SNOMED CT concepts / seconds")


print(MEDDRA.first_levels())


print(CDF["01_A1"])
print(CDF.search("RENALE"))
print(CDF["CC_D23"] >> ICD10)
print(ICD10["N18"] >> CDF)
