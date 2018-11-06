#!/usr/bin/python3.6

import asyncio
import websockets
import socket
import os
import sys
import json
from threading import Thread
from time import sleep
from pygame import mixer
from io import StringIO
import subprocess
import sfile

d_root = "./scoring/data"
mixer.init()

class Topic():
  def __init__(self, parent, title, is_penalty, mod, rsc):
    self.parent = parent
    self.title = title
    self.is_penalty = is_penalty
    self.mod = mod
    self.rsc = rsc
    self.score = 0
  def getCondensed(self):
    res = { "title" : self.title, "penalty" : self.is_penalty, "score" : self.score, "resource" : self.rsc }
    return res
  def check(self):
    try:
      res = self.mod.check()
      self.score = 1 if res else 0
    except Exception as e:
      print("Failed vuln check:", e)
    return self.score
  def reset(self):
    try:
      self.mod.reset()
    except Exception as e:
      print("Reset request failed:", e)
  def fix(self):
    try:
      self.mod.fix()
    except Exception as e:
      print("Fix request failed:", e)
  def getTopic(self, path):
    return self

class Subject():
  def __init__(self, parent, title):
    self.parent = parent
    self.title = title
    self.topics = []
  def getCondensed(self):
    # returns JSON-ready object that represents itself
    res = { "title" : self.title }
    o_topics = []
    for i in self.topics:
      o_topics.append(i.getCondensed())
    res["topics"] = o_topics
    return res
  def getTopic(self, path):
    res = None
    if type(path) is not list:
      path = path.split("/")[1:]
    if len(path) > 0:
      for topic in self.topics:
        if topic.title == path[0]:
          res = topic.getTopic(path[1:])
    else:
      res = self
    return res
  def fix(self):
    for t in self.topics:
      t.fix()
  def reset(self):
    for t in self.topics:
      t.reset()
class Curriculum(Subject):
  def __init__(self, root, title="Ubuntu AV18 Training System"):
    self.root = root
    self.topics = []
    self.title = title
    self.used_imports = [];
    self.compileTopics(self.root, self)
    self.title = self.topics[0].title
    self.topics = self.topics[0].topics
  def compileTopics(self, root, subject, rsc=None):
    r_data = {}
    cdir = os.listdir(root)
    if "info" in cdir:
      found_rsc = False
      with open(os.path.join(root, "info")) as f:
        il = f.readlines()
        for iv in il:
          iv_arr = iv.split(": ")
          d = iv_arr[1][:-1]
          #  Reads contents of every resource file. This could become a major memory issue.
          #if iv_arr[0] == "resource":
          #  with open(os.path.join(root, d)) as f:
          #    r_data[iv_arr[0]] = f.read()
          #  found_rsc = True
          #  rsc = r_data["resource"]
          #else:
          #  Creates gettable links for resource files. should be cleaner?
          if iv_arr[0] == "resource":
            if d == "None":
              r_data["resource"] = None;
            else:
              r_data["resource"] = "/".join(os.path.join(root, d).split("/")[2:])
              rsc = r_data["resource"]
          else:
            r_data[iv_arr[0]] = d
      cdir.remove("info")
      if not found_rsc and rsc is not None:
        r_data["resource"] = rsc
    else:
      raise ImportError('Could not find info file in ' + root)
    for cf in cdir:
      if cf[-3:] == ".py":
        r_data["obj_type"] = "Topic"
        imp = cf[:-3]
        if imp in self.used_imports:
          app = 1
          while (imp + str(app)) in self.used_imports:
            app += 1
          imp += str(app)
          os.rename(os.path.join(root, cf), os.path.join(root, imp + ".py"))
        self.used_imports.append(imp)
        sys.path.insert(0, root)
        r_data["mod"] = __import__(imp)
    if "obj_type" not in r_data:
      r_data["obj_type"] = "Subject"
      s = Subject(subject, r_data["title"])
      subject.topics.append(s)
      if len(cdir) > 0:
        for d in cdir:
          fd = os.path.join(root, d)
          if not os.path.isfile(fd):
            self.compileTopics(fd, s, rsc=rsc)
    else:
      subject.topics.append(Topic(subject, r_data["title"], r_data["penalty"] == "True", r_data["mod"], r_data["resource"]))
  async def checkVuln(self, onFind, scope=None, init=False):
    if scope is None:
      scope = self
    for topic in scope.topics:
      if isinstance(topic, Subject):
        await self.checkVuln(onFind, scope=topic, init=init)
      else:
        pre_score = topic.score
        score = topic.check()
        if score != pre_score and not init:
          # send to web clients
          p = self.getPath(topic)
          print("Sending Update:\nPath: {}\nScore: {}".format(p, score))
          await onFind(p, score);
          if ((score == 1 and not topic.is_penalty) or (score == 0 and topic.is_penalty)):
            # play score
            mixer.music.load("score.wav")
            mixer.music.play()
            pass
          else:
            # play alert
            mixer.music.load("alarm.wav")
            mixer.music.play()
            pass
  def getPath(self, item, cpath=""):
    res = cpath
    if not isinstance(item, Curriculum):
      cpath = item.title + (("/" + cpath) if cpath != "" else "")
      res = self.getPath(item.parent, cpath=cpath)
    return res

class FE_interface():
  def __init__(self, c):
    Thread.__init__(self)
    self.c = c
    self.init_data = { "curriculum": self.c }
    self.clients = []
    self.start_server = websockets.serve(self.s_cycle, 'localhost', 4298)
    self.tasking = False
  async def s_cycle(self, websocket, path):
    self.clients.append(websocket)
    await websocket.send(json.dumps({ 
      "tag" : "init",
      "data" : self.getInitData()
    }))
    #if True: # Can be swapped out with the try/except block for easy client-driven task debugging
    try:
      while True:
        msg = await websocket.recv()
        msg = json.load(StringIO(msg))
        if "q_id" not in msg:
          print("WARNING: request sent without response queue index.")
        if msg["tag"] == "cat":
          with open(os.path.join("./scoring", msg["data"])) as f:
            await self.send("response", f.read(), q_id=msg["q_id"])
        elif msg["tag"] == "fix":
          if not self.tasking:
            self.tasking = True
            topic = self.c.getTopic(msg["data"])
            topic.fix()
            self.tasking = False
            await self.send("response", "", q_id=msg["q_id"])
        elif msg["tag"] == "reset":
          if not self.tasking:
            self.tasking = True
            topic = self.c.getTopic(msg["data"])
            topic.reset()
            self.tasking = False
            await self.send("response", "", q_id=msg["q_id"])
    except:
      self.clients.remove(websocket)
  async def send(self, tag, msg, q_id=-1):
    res = {}
    res["tag"] = tag
    res["data"] = msg
    res["q_id"] = q_id
    res = json.dumps(res)
    for c in self.clients:
      await c.send(res)
  def getInitData(self):
    res = {}
    for i in self.init_data:
      res[i] = self.init_data[i].getCondensed()
    return res

class VulnCheck():
  def __init__(self, c, s, delay):
    Thread.__init__(self)
    self.c = c
    self.s = s
    self.delay = delay
  async def run(self):
    while True:
      await self.c.checkVuln(self.onFind)
      await self.s.send("pulse", None)
      await asyncio.sleep(self.delay)
  async def onFind(self, path, score):
    await self.s.send("c_update", { "path":path, "score":score })

loop = asyncio.get_event_loop()

async def start():
  c = Curriculum(d_root)
  await c.checkVuln(None, init=True)
  s = FE_interface(c)
  v = VulnCheck(c, s, 1)
  tasks = [s.start_server, loop.create_task(v.run())]
  await asyncio.gather(*tasks)

if __name__ == "__main__":
  user = subprocess.check_output('who', shell=True).decode("utf-8").split()[0]
  os.system("sudo -u " + user + " firefox scoring/score_report.html &")
  loop.run_until_complete(start())
  loop.run_forever()
