var py_c;
var c;
var red = "f70000";
var green = "#82ff05";
var inactive = "#ddd";

var transitions = true;

$(document).ready(function () {
  py_c = new PyClient();
  py_c.onLoadCurriculum = function (nc) {
    if (c) {
      c.remove();
    }
    $("#disp_bar").html("");
    c = new Curriculum(nc);
    $("#disp_bar").append(c);
    c.wire();
    c.compileScore(true);
  };
  py_c.onConnectionChange = setConnDisplay;
  setConnDisplay(false);
  py_c.connect();
});
function setConnDisplay(state) {
  $("#status_field").html(state ? "System Online" : "System not Running");
}

function Curriculum(raw) {
  var that = this;
  Subject.call(this, raw);
  this.addClass("curriculum");
  var that = this;
}

var red = "f70000";
var green = "#82ff05";
var inactive = "#ddd";

function Subject(raw) {
  if (!raw) {
    raw = {};
  }
  var that = this;
  $.extend(this, $(
    '<div class="subject_shell">' +
      '<div class="subject">' +
        '<div class="sbj_title"></div>' +
        '<div class="total s_total"></div>' +
        '<div class="total p_total"></div>' +
        '<div class="sbj_bars">' +
          '<div class="bar_field sw">' +
            '<div class="bar score_bar"></div>' +
          '</div>' +
          '<div class="bar_field">' +
            '<div class="bar penalty_bar"></div>' +
          '</div>' +
        '</div>' +
        '<div class="exp_field">' +
          '<img id="fix_btn" class="img_btn" src="arrow_up_btn.png">' +
          '<img id="rst_btn" class="img_btn" src="arrow_down_btn.png">' +
          '<img id="rsc_btn" class="img_btn" src="rsc_btn.png">' +
          '<img class="img_btn collapse_btn" src="clp_btn.png">' +
          '<img class="img_btn expand_btn" src="exp_btn.png">' +
        '</div>' +
        '<div class="topics"></div>' +
      '</div>' +
    '</div>'
  ));
  this.ctl_disabled = false;
  this.title = raw.title;
  this.tv_toggle = false;
  this.dom_title = this.find(".sbj_title");
  this.score = 0;
  this.dom_sw = this.find(".sw");
  this.dom_score = this.find(".score_bar");
  this.total = 0;
  this.dom_total = this.find(".s_total");
  this.penalties = 0;
  this.dom_penalties = this.find(".penalty_bar");
  this.p_total = 0;
  this.dom_p_total = this.find(".p_total");
  this.topics = [];
  this.dom_topics = this.find(".topics");
  this.dom_exp = this.find(".expand_btn");
  this.dom_clp = this.find(".collapse_btn");
  this.dom_rst = this.find("#rst_btn");
  this.dom_fix = this.find("#fix_btn");
  this.resource = raw.resource;
  this.dom_rsc = this.find("#rsc_btn");
  this.addTopic = function (topic) {
    topic.cparent = that;
    that.topics.push(topic);
    that.dom_topics.append(topic);
  };
  this.getTopic = function (path) {
    if (!Array.isArray(path)) {
      path = path.split("/").slice(1);
    }
    var res;
    var find;
    for (var i=0; i<that.topics.length; i++) {
      var ct = that.topics[i];
      if (ct.title == path[0]) {
        find = ct;
        break;
      }
    }
    if (path.length == 1) {
      res = find;
    } else {
      res = find.getTopic(path.slice(1));
    }
    return res;
  };
  this.compileScore = function (down_prop) {
    that.score = 0;
    that.total = 0;
    that.penalties = 0;
    that.p_total = 0;
    for (var i=0; i<that.topics.length; i++) {
      var ts = that.topics[i];
      if (ts.hasOwnProperty("total")) {
        if (down_prop) {
          ts.compileScore(true);
        }
        that.total += ts.total;
        that.score += ts.score;
        that.p_total += ts.p_total;
        that.penalties += ts.penalties;
      } else {
        if (ts.penalty) {
          that.p_total++;
          that.penalties += ts.score;
        } else {
          that.total++;
          that.score += ts.score;
        }
      }
    }
    that.dom_total.html(that.score + "/" + that.total);
    that.sizeBar();
    that.dom_p_total.html(that.penalties ? ("Penalties: " + that.penalties + "/" + that.p_total) : "");
    that.dom_p_total.css("opacity", that.penalties ? 1 : 0);
    var p_ratio = that.penalties / that.p_total;
    that.dom_penalties.css("width", that.dom_sw.width() * p_ratio);
    if (!down_prop && that.cparent) {
      that.cparent.compileScore();
    }
  };
  this.sizeBar = function () {
    var ratio = that.score / that.total;
    that.dom_score.css("width", that.dom_sw.width() * ratio);
  };
  this.toggleTView = function () {
    if (that.tv_toggle) {
      if (transitions) {
        that.dom_topics.slideUp(400);
      } else {
        that.dom_topics.hide();
      }
      that.dom_clp.hide()
      that.dom_exp.show();
      that.tv_toggle = false;
    } else {
      if (transitions) {
        that.dom_topics.slideDown(400);
      } else {
        that.dom_topics.show();
      }
      that.tv_toggle = true;
      that.dom_exp.hide()
      that.dom_clp.show();
      if (!that.contentsDisplayed) {
        for (var i=0; i<that.topics.length; i++) {
          var ct = that.topics[i];
          if (ct.hasOwnProperty("total")) {
            ct.sizeBar();
          }
        }
        that.contentsDisplayed = true;
      }
    }
  };
  this.setCtl = function (state) {
    that.ctl_disabled = !state;
    that.dom_fix.css("filter", state ? "none" : "grayscale(100%)");
    that.dom_rst.css("filter", state ? "none" : "grayscale(100%)");
    for (var i=0; i<that.topics.length; i++) {
      that.topics[i].setCtl(state);
    }
  };
  CElem.call(this);
  this.wire = function () {
    that.dom_exp.unbind().click(function () {
      that.toggleTView();
    });
    that.dom_clp.unbind().click(function () {
      that.toggleTView();
    });
    that.dom_fix.unbind().click(function () {
      that.fix();
    });
    that.dom_rst.unbind().click(function () {
      that.reset();
    });
    if (!that.resource || that.resource == "None") {
      that.dom_rsc.hide();
    } else {
      that.dom_rsc.unbind().click(function () {
        that.openRsc();
      });
    }
    for (var i=0; i<that.topics.length; i++) {
      that.topics[i].wire();
    }
  };
  this.dom_title.html(this.title);
  if (raw.topics) {
    for (var i=0; i<raw.topics.length; i++) {
      var raw_topic = raw.topics[i];
      if (raw_topic.topics) {
        var s = new Subject(raw_topic);
        this.addTopic(s);
      } else {
        this.addTopic(new Topic(raw_topic));
      }
    }
  }
}

function Topic(raw) {
  if (!raw) {
    raw = {};
  }
  var that = this;
  $.extend(this, $(
    '<div class="topic_shell">' +
      '<div class="topic">' +
        '<div class="score"></div>' +
        '<div class="title">UFW is enabled</div>' +
        '<div class="btn_field">' +
          '<img id="fix_btn" class="img_btn" src="arrow_up_btn.png">' +
          '<img id="rst_btn" class="img_btn" src="arrow_down_btn.png">' +
          '<img id="rsc_btn" class="img_btn" src="rsc_btn.png">' +
        '</div>' +
      '</div>' +
    '</div>'
  ));
  this.ctl_disabled = false;
  this.title = raw.title;
  this.dom_title = this.find(".title");
  this.score = raw.score ? raw.score : 0;
  this.dom_score = this.find(".score");
  this.penalty = raw.penalty;
  this.score_color = raw.penalty ? red : green;
  this.resource = raw.resource;
  this.dom_rsc_btn = this.find("#rsc_btn");
  this.dom_rst_btn = this.find("#rst_btn");
  this.dom_fix_btn = this.find("#fix_btn");
  this.updateDisp = function () {
    that.dom_title.html(that.title);
    that.dom_score.css("background-color", that.score ? that.score_color : inactive);
  };
  this.wire = function () {
    that.dom_rst_btn.unbind().click(function () {
      that.reset();
    });
    that.dom_fix_btn.unbind().click(function () {
      that.fix();
    });
    if (!that.resource || that.resource == "None") {
      that.dom_rsc_btn.hide();
    } else {
      that.dom_rsc_btn.unbind().click(function () {
        that.openRsc();
      });
    }
  };
  this.updateScore = function (score) {
    that.score = score;
    that.dom_score.css("background-color", that.score ? that.score_color : inactive);
    if (that.cparent) {
      that.cparent.compileScore();
    }
  };
  this.setCtl = function (state) {
    that.ctl_disabled = !state;
    that.dom_fix_btn.css("filter", state ? "none" : "grayscale(100%)");
    that.dom_rst_btn.css("filter", state ? "none" : "grayscale(100%)");
  };
  CElem.call(this);
  this.updateDisp();
}
function CElem() {
  var that = this;
  this.getPath = function () {
    if (!that.path) {
      that.path = (that.cparent ? (that.cparent.getPath() + "/") : "") + that.title;
    }
    return that.path;
  };
  this.reset = function () {
    if (!that.ctl_disabled) {
      c.setCtl(false);
      var p = that.getPath()
      py_c.send("reset", p,  function () {
        c.setCtl(true);
      });
    }
  };
  this.fix = function () {
    if (!that.ctl_disabled) {
      c.setCtl(false);
      py_c.send("fix", that.getPath(),  function () {
        c.setCtl(true);
      });
    }
  };
  this.openRsc = function () {
    new Window(that.resource);
  };
}

function Window(src) {
  var that = this;
  $.extend(this, $(
    '<div>' +
      '<div class="dropcloth"></div>' +
      '<div class="window">' +
        '<div class="w_bar">' +
          '<img id="close_btn" class="img_btn" src="x.png" style="float: right;">' +
        '</div>' +
        '<div class="w_contents"></div>' +
      '</div>' +
    '</div>'
  ));
  this.drop = this.find(".dropcloth");
  this.window = this.find(".window");
  this.dom_contents = this.find(".w_contents");
  if (src) {
    //this.dom_contents.append(src);
    py_c.send("cat", src, function (contents) {
      that.dom_contents.append(contents);
      that.reveal();
    });
    /*$.ajax({
      type: "GET",
      url: src,
      dataType: "jsonp",
      success: function (data) {
        that.dom_contents.html(data);
      }
    });*/
    /*$.get(src, function (data) {
      that.dom_contents.html(data);
    });*/
  } else {
    that.reveal();
  }
  this.dom_x_btn = this.find("#close_btn");
  this.reveal = function () {
    that.drop.fadeIn(400);
    that.window.slideDown(400, function () {
      that.dom_contents.css("opacity", 1);
    });
  };
  this.close = function () {
    that.dom_contents.css("opacity", 0);
    setTimeout(function () {
      that.drop.fadeOut(400);
      that.window.slideUp(400, function () {
        that.remove();
      });
    }, 400);
  };
  $("body").append(this);
  that.dom_x_btn.unbind().click(this.close);
}

function hb_pulse() {
  pm = $("#sys_hb_fill");
  pm.show();
  pm.delay(300).fadeOut(400);
}

function PyClient() {
  var that = this;
  this.connected = false;
  this.c;
  this.q = {};
  this.q_max = 0;
  this.connect = function () {
    that.updateState(false);
    try {
      that.c = new WebSocket("ws://localhost:4298");
      that.c.onopen = function () {
        that.updateState(true);
        that.c.onmessage = function (m) {
          m = JSON.parse(m.data);
          switch (m.tag) {
            case "init":
              c_data = m.data.curriculum
              that.onLoadCurriculum(c_data);
              break;
            case "c_update":
              console.log("Score change:", m.data.path, m.data.score);
              var path = m.data.path;
              var score = m.data.score;
              if (c) {
                c.getTopic(path).updateScore(score);
              }
              break;
            case "pulse":
              hb_pulse();
              break;
            case "response":
              if (m.q_id in that.q && m.q_id != -1) {
                var rcb = that.q[m.q_id];
                delete that.q[m.q_id];
                if (Object.keys(that.q).length == 0) {
                  that.q_max = 0;
                }
                rcb(m.data);
              }
              break;
          }
        };
      };
      that.c.onclose = function () {
        that.updateState(false);
        setTimeout(that.connect, 1000);
      };
    } catch (err) {
      that.updateState(false);
      setTimeout(that.connect, 1000);
    }
  };
  this.send = function (tag, data, cb) {
    var packet = {};
    packet.tag = tag;
    packet.data = data;
    if (cb) {
      var q_tag = ++that.q_max;
      that.q[q_tag + ""] = cb;
      packet.q_id = q_tag + "";
    }
    that.c.send(JSON.stringify(packet));
  };
  this.updateState = function (state) {
    var ch = state != that.connected;
    that.connected = state;
    if (ch) {
      this.onConnectionChange(state);
    }
  };
  this.onConnectionChange = function (state) {};
}
