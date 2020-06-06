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


# Imports VCM lexicon element priority in ontology.

import sys, os, os.path, re
from pymedtermino.utils.mapping_db import *
from pymedtermino.vcm              import *


HERE              = os.path.dirname(sys.argv[0])
ONTOLOGY_PATH     = os.path.join(HERE, "..", "vcm_onto")
TXT_FILE          = os.path.join(HERE, "..", "vcm_onto", "vcm_lex_priority.txt")
OWL_FILE          = os.path.join(HERE, "..", "vcm_onto", "vcm_lexique.owl")

txt = read_file(TXT_FILE)

groups = txt.split("\n\n\n")

groups = [[line for line in group.split("\n") if line and not line[0] == "#"] for group in groups]

LEX_2_PRIORITY        = {}
LEX_2_SECOND_PRIORITY = {}

n_line_group = 1
for i in reversed(range(len(groups))):
  n_line = 1
  for line in groups[i]:
    words    = line.split()
    lex_code = int(words[0])
    if words[1] == "-1": sign = -1
    else:                sign =  1
    priority = sign * n_line * n_line_group

    if not lex_code in LEX_2_PRIORITY:
      LEX_2_SECOND_PRIORITY[lex_code] = 0
      LEX_2_PRIORITY       [lex_code] = priority
    else:
      LEX_2_SECOND_PRIORITY[lex_code] = LEX_2_PRIORITY[lex_code]
      LEX_2_PRIORITY       [lex_code] = priority
      
    print(VCM_LEXICON[lex_code].term, LEX_2_PRIORITY[lex_code], LEX_2_SECOND_PRIORITY[lex_code])
    
    n_line       += 1
  n_line_group += abs(LEX_2_PRIORITY[lex_code])


owl = read_file(OWL_FILE)

owl = re.sub(r"<priority>-?[0-9]*</priority>", "", owl)
owl = re.sub(r"<second_priority>-?[0-9]*</second_priority>", "", owl)

added_annotations = ""
for lex_code in LEX_2_PRIORITY:
  added_annotations += """
    <owl:Class rdf:about="&vcm_lexique;%s">
        <priority>%s</priority>
    </owl:Class>

""" % (lex_code, LEX_2_PRIORITY[lex_code])
for lex_code in LEX_2_SECOND_PRIORITY:
  added_annotations += """
    <owl:Class rdf:about="&vcm_lexique;%s">
        <second_priority>%s</second_priority>
    </owl:Class>

""" % (lex_code, LEX_2_SECOND_PRIORITY[lex_code])

owl = owl.replace("</rdf:RDF>", added_annotations + "\n</rdf:RDF>")

write_file(OWL_FILE, owl)
