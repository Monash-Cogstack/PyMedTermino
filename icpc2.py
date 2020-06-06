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

__all__ = ["ICPC2"]

import os, os.path, sqlite3 as sql_module
import pymedtermino

db        = sql_module.connect(os.path.join(pymedtermino.DATA_DIR, "icpc2.sqlite3"), check_same_thread=False)
db_cursor = db.cursor()
db_cursor.execute("PRAGMA query_only = TRUE;")

_SEARCH1 = {}
_SEARCH2 = {}
_TEXT1   = {}
_TEXT2   = {}
_CONCEPT = {}
for lang in ["en", "fr", "de"]:
  _TEXT1  [lang] = "SELECT text_%s FROM Text WHERE id=?"                   % lang
  _TEXT2  [lang] = "SELECT id, text_%s, text_en, dagger, reference FROM Text WHERE code=? AND relation=?" % lang
  _CONCEPT[lang] = "SELECT parent_code, term_%s FROM Concept WHERE code=?" % lang
  
class ICPC2(pymedtermino.Terminology):
  def __init__(self):
    pymedtermino.Terminology.__init__(self, "ICPC2")
    
  def _create_Concept(self): return ICPC2Concept
  
  def first_levels(self):
    return [self[code] for code in ["A", "B", "D", "F", "H", "K", "L", "N", "P", "R", "S", "T", "U", "W", "X", "Y", "Z"]]
  
  def search(self, text):
    db_cursor.execute("SELECT Concept.code FROM Concept, Concept_fts WHERE Concept_fts.term MATCH ? AND Concept.id = Concept_fts.docid", (text,))
    r1 = db_cursor.fetchall()
    return [self[code] for (code,) in set(r1 + r2)]
  
  
class ICPC2Concept(pymedtermino.MultiaxialConcept, pymedtermino._StringCodeConcept):
  def __init__(self, code):
    db_cursor.execute("SELECT term FROM Concept WHERE code=? AND lang=?", (code, pymedtermino.LANGUAGE))
    term = db_cursor.fetchone()[0]
    pymedtermino.MultiaxialConcept.__init__(self, code, term)
    
  def __getattr__(self, attr):
    if   attr == "parents":
      db_cursor.execute("SELECT destination FROM Relation WHERE source=? AND relation='is_a'", (self.code,))
      self.parents = [self.terminology[code] for (code,) in db_cursor.fetchall()]
      return self.parents
    
    elif attr == "children":
      db_cursor.execute("SELECT source FROM Relation WHERE destination=? AND relation='is_a'", (self.code,))
      self.children = [self.terminology[code] for (code,) in db_cursor.fetchall()]
      self.children.sort(key = lambda c: c.code)
      return self.children
    
    elif attr == "relations":
      db_cursor.execute("SELECT DISTINCT relation FROM Relation WHERE source=?", (self.code,))
      self.relations = set(rel for (rel,) in db_cursor.fetchall() if rel != u"is_a")
      db_cursor.execute("SELECT DISTINCT relation FROM Relation WHERE destination=?", (self.code,))
      for (rel,) in db_cursor.fetchall():
        if rel != u"is_a": self.relations.add(u"INVERSE_%s" % rel)
      return self.relations
    
    elif attr.startswith(u"INVERSE_"):
      db_cursor.execute("SELECT DISTINCT source FROM Relation WHERE destination=? AND relation=?", (self.code, attr[8:]))
      l = [self.terminology[code] for (code,) in db_cursor.fetchall()]
      if not l: raise AttributeError(attr)
      setattr(self, attr, l)
      return l
    
    else:
      db_cursor.execute("SELECT DISTINCT destination FROM Relation WHERE source=? AND relation=?", (self.code, attr))
      l = [self.terminology[code] for (code,) in db_cursor.fetchall()]
      if not l: raise AttributeError(attr)
      setattr(self, attr, l)
      return l
    
    raise AttributeError(attr)

  def get_translation(self, lang):
    db_cursor.execute("SELECT term FROM Concept WHERE lang=? AND code=?", (lang, self.code,))
    return db_cursor.fetchone()[0]

  
ICPC2 = ICPC2()
