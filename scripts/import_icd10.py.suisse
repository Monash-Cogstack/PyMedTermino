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


# Get ICD10 from (NB choose "ClaML" format) :
# http://apps.who.int/classifications/apps/icd/ClassificationDownload/DLArea/Download.aspx

ICD10_DIR = "/home/jiba/telechargements/base_med/icd10"

# Get CIM10 French and German translation from (NB choose "XML" format) :
# http://www.icd10.ch/telechargement/Exp_XML.zip

CIM10_DIR = "/home/jiba/telechargements/base_med/cim10"


import sys, os, os.path, stat, sqlite3

if len(sys.argv) >= 3:
  ICD10_DIR = sys.argv[1]
  CIM10_DIR = sys.argv[2]


import xml.sax as sax, xml.sax.handler as handler

if sys.version[0] == "2":
  from StringIO import StringIO
else:
  from io import StringIO

HERE = os.path.dirname(sys.argv[0]) or "."
sys.path.append(os.path.join(HERE, ".."))

from utils.db import *

SQLITE_FILE = os.path.join(HERE, "..", "icd10.sqlite3")

db = create_db(SQLITE_FILE)
db_cursor = db.cursor()

#r = open("/tmp/log.sql", "w")
def do_sql(sql):
  #r.write(sql.encode("utf8"))
  #r.write(";\n")
  db_cursor.execute(sql)
  
def sql_escape(s):
  return s.replace(u'"', u'""').replace(u'\r', u'').replace(u'\x92', u"'")


do_sql(u"PRAGMA synchronous  = OFF")
do_sql(u"PRAGMA journal_mode = OFF")

do_sql(u"""
CREATE TABLE Concept (
  id INTEGER PRIMARY KEY,
  parent_code VARCHAR(7),
  code VARCHAR(7),
  term_en TEXT,
  term_fr TEXT,
  term_de TEXT,
  dagger INTEGER,
  star INTEGER,
  mortality1 TEXT,
  mortality2 TEXT,
  mortality3 TEXT,
  mortality4 TEXT,
  morbidity TEXT
)
""")

do_sql(u"""
CREATE TABLE Text (
  id INTEGER PRIMARY KEY,
  code VARCHAR(7),
  relation VARCHAR(13),
  text_en TEXT,
  text_fr TEXT,
  text_de TEXT,
  dagger INTEGER,
  reference TEXT
)
""")




EN_2_FR    = {}
EN_2_DE    = {}
CODE_2_SID = {}
SID_2_EN   = {}

if CIM10_DIR:

  class Handler(handler.ContentHandler):
    def __init__(self):
      pass

    def startElement(self, name, attrs):
      self.tag = name

    def endElement(self, name):
      pass

    def characters(self, content):
      if   self.tag == "SID":
        self.sid = content.strip()
        
      elif self.tag == "code":
        code = content.strip()
        CODE_2_SID[code] = self.sid

  if sys.version[0] == "2": xml = open(os.path.join(CIM10_DIR, "MASTER.xml")).read()
  else:                     xml = open(os.path.join(CIM10_DIR, "MASTER.xml"), encoding = "latin").read()
  xml = StringIO(xml)
  parser = sax.make_parser()
  parser.setContentHandler(Handler())
  parser.parse(xml)
  
  
  class Handler(handler.ContentHandler):
    def __init__(self):
      pass

    def startElement(self, name, attrs):
      self.tag = name

      if name == "REC":
        self.fr = self.en = self.de = self.sid = self.source = u""
        
    def characters(self, content):
      if   self.tag == "FR_OMS":   self.fr     = content
      elif self.tag == "EN_OMS":   self.en     = content
      elif self.tag == "GE_DIMDI": self.de     = content
      elif self.tag == "SID":      self.sid    = content
      elif self.tag == "source":   self.source = content
      
    def endElement(self, name):
      if name == "REC":
        if self.source == "S":
          if self.en:
            if self.fr:  EN_2_FR [self.en ] = self.fr
            if self.de:  EN_2_DE [self.en ] = self.de
            if self.sid: SID_2_EN[self.sid] = self.en
            
  if sys.version[0] == "2": xml = open(os.path.join(CIM10_DIR, "LIBELLE.xml")).read()
  else:                     xml = open(os.path.join(CIM10_DIR, "LIBELLE.xml"), encoding = "latin").read()
  xml = StringIO(xml)
  parser = sax.make_parser()
  parser.setContentHandler(Handler())
  parser.parse(xml)


LANGUAGE_DICTS = { "fr" : EN_2_FR, "de" : EN_2_DE }
def translate(en, language, code = ""):
  if code:
    sid = CODE_2_SID.get(code)
    if sid:
      en2 = SID_2_EN.get(sid)
      if en2:
        t = translate(en2, language)
        if t: return t
        
  d = LANGUAGE_DICTS[language]
  t = d.get(en)
  if t: return t
  splitted = en.rsplit(None, 1)
  if len(splitted) == 2:
    en, code = splitted
    if code in CONCEPTS:
      t = d.get(en)
      if t: return u"%s %s" % (t, code)
  return u""



CONCEPTS = {}
class Concept(object):
  def __init__(self, code):
    self.parent_code      = ""
    self.code             = code
    self.term_en          = ""
    self.dagger           = 0
    self.star             = 0
    self.mortality1       = ""
    self.mortality2       = ""
    self.mortality3       = ""
    self.mortality4       = ""
    self.morbidity        = ""
    self.texts            = []
    CONCEPTS[code] = self

  def set_term(self, term_en):
    self.term_en = term_en
    
  def add_text(self, relation, text_en, dagger, reference):
    self.texts.append((relation, text_en, dagger, reference))
    
  def sql(self):
    if self.mortality1 == u"UNDEF": self.mortality1 = u""
    if self.mortality2 == u"UNDEF": self.mortality2 = u""
    if self.mortality3 == u"UNDEF": self.mortality3 = u""
    if self.mortality4 == u"UNDEF": self.mortality4 = u""
    if self.morbidity  == u"UNDEF": self.morbidity  = u""
    return u"""(NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (self.parent_code, self.code, sql_escape(self.term_en), sql_escape(translate(self.term_en, "fr", self.code)), sql_escape(translate(self.term_en, "de", self.code)), self.dagger, self.star, self.mortality1, self.mortality2, self.mortality3, self.mortality4, self.morbidity)

  def sql_text(self):
    return [
      u"""(NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (self.code, relation, sql_escape(text_en), sql_escape(translate(text_en, "fr")), sql_escape(translate(text_en, "de")), dagger, reference)
      for (relation, text_en, dagger, reference) in self.texts
      ]


class Handler(handler.ContentHandler):
  def __init__(self):
    self.concept   = None
    self.inhibited = 0
    self.content   = u""
    self.reference = u""
    
  def startElement(self, name, attrs):
    if self.inhibited: return
    
    if   name == "Fragment":
      self.content = u"%s " % self.content.strip()
      if attrs.get("usage") == "dagger":
        self.dagger = 1
        
    elif name == "Reference":
      self.content = u"%s " % self.content.strip()
      
    elif name == "Label":
      self.content   = u""
      self.reference = u""
      self.dagger    = 0
      
    if   (name == "Modifier") or (name == "ModifierClass"):
      self.inhibited += 1
      
    elif name == "Class":
      self.concept = Concept(attrs["code"])
      if attrs.get("usage") == "dagger": self.concept.dagger = 1
      if attrs.get("usage") == "aster":  self.concept.star   = 1
      
    elif name == "SuperClass":
      self.concept.parent_code = attrs["code"]
      
    elif name == "Meta":
      if   attrs["name"] == "MortL1Code": self.concept.mortality1 = attrs["value"]
      elif attrs["name"] == "MortL2Code": self.concept.mortality2 = attrs["value"]
      elif attrs["name"] == "MortL3Code": self.concept.mortality3 = attrs["value"]
      elif attrs["name"] == "MortL4Code": self.concept.mortality4 = attrs["value"]
      elif attrs["name"] == "MortBCode" : self.concept.morbidity  = attrs["value"]
      
    elif name == "Rubric":
      self.kind = attrs["kind"]
      
    elif name == "Reference":
      self.reference = attrs.get("code", u"")
      
  def endElement(self, name):
    if (name == "Modifier") or (name == "ModifierClass"): self.inhibited -= 1
    if self.inhibited: return

    self.content = self.content.strip()
    if self.content:
      if   name == "Label":
        if   self.kind == "preferred": self.concept.set_term(self.content)
        else:
          self.concept.add_text(self.kind, self.content, self.dagger, self.reference)
          
      elif name == "Reference":
        if not self.reference: self.reference = self.content.strip().split()[-1]
        
      elif name == "Fragment":
        if self.content.endswith(":"): self.content = self.content[:-1]
        
  def characters(self, content):
    if self.inhibited: return
    self.content += content
    
if sys.version[0] == "2": xml = open(os.path.join(ICD10_DIR, "icd102010en.xml")).read()
else:                     xml = open(os.path.join(ICD10_DIR, "icd102010en.xml"), encoding = "latin").read()
xml = xml.replace("""<!DOCTYPE ClaML SYSTEM "ClaML.dtd">""", "")
xml = StringIO(xml)
parser = sax.make_parser()
parser.setContentHandler(Handler())
parser.parse(xml)




for concept in CONCEPTS.values():
  do_sql(u"INSERT INTO Concept VALUES %s" % concept.sql())
  
for concept in CONCEPTS.values():
  for sql in concept.sql_text():
    do_sql(u"INSERT INTO Text VALUES %s" % sql)

do_sql(u"""CREATE UNIQUE INDEX Concept_code_index ON Concept(code)""")
do_sql(u"""CREATE INDEX Concept_parent_code_index ON Concept(parent_code)""")

do_sql(u"""CREATE INDEX Text_code_index          ON Text(code)""")
do_sql(u"""CREATE INDEX Text_code_relation_index ON Text(code, relation)""")


do_sql(u"""CREATE VIRTUAL TABLE Concept_fts USING fts4(content="Concept", term_en, term_fr, term_de);""")
do_sql(u"""INSERT INTO Concept_fts(docid, term_en, term_fr, term_de) SELECT id, term_en, term_fr, term_de FROM Concept;""")
do_sql(u"""INSERT INTO Concept_fts(Concept_fts) VALUES('optimize');""")

do_sql(u"""CREATE VIRTUAL TABLE Text_fts USING fts4(content="Text", text_en, text_fr, text_de);""")
do_sql(u"""INSERT INTO Text_fts(docid, text_en, text_fr, text_de) SELECT id, text_en, text_fr, text_de FROM Text;""")
do_sql(u"""INSERT INTO Text_fts(Text_fts) VALUES('optimize');""")

do_sql(u"""VACUUM;""")

close_db(db, SQLITE_FILE)

