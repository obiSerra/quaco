"strict";

const ip = "__IP__";

const keyboardListener = (commands, onDown, onUp) => {
  document.addEventListener(
    "keydown",
    event => {
      const keyName = event.key;
      if (typeof commands[keyName] !== "undefined") {
        event.preventDefault();
        onDown(keyName);
      }
    },
    false
  );

  document.addEventListener("keyup", event => {
    const keyName = event.key;
    if (typeof commands[keyName] !== "undefined") {
      event.preventDefault();
      onUp(keyName);
    }
  });

  return () => JSON.parse(JSON.strigify(commands));
};

const generateWs = () => {
  const ws = new WebSocket("ws://" + ip + ":5678/");
  const messages = document.createElement("ul");
  let channelOpen = false;
  ws.onmessage = function(event) {
    console.log(event.data);
  };

  const sendMsg = msg => {
    if (!channelOpen) return false;
    try {
      ws.send(JSON.stringify({ data: msg }));
      return true;
    } catch (err) {
      console.log(err.message);
      return false;
    }
  };
  ws.onopen = event => {
    channelOpen = true;
    sendMsg({ msg: "connection started!" });
  };

  document.body.appendChild(messages);
  return {
    sendMsg
  };
};

const init = () => {
  const ws = generateWs();
  const kStrokes = {
    ArrowRight: false,
    ArrowLeft: false,
    ArrowUp: false,
    ArrowDown: false,
    w: false,
    a: false,
    s: false,
    d: false,
    q: false
  };
  const getKeybdStatus = keyboardListener(
    kStrokes,
    key => (kStrokes[key] = true),
    key => (kStrokes[key] = false)
  );

  let lastRun = 0;

  const step = timestamp => {
    const now = +new Date();
    const rate = 250;

    if (now - lastRun > rate) {
      ws.sendMsg(kStrokes);
      lastRun = now;
    }
    requestAnimationFrame(step);
  };

  requestAnimationFrame(step);
};

if (document.readyState != "loading") init();
else if (document.addEventListener)
  document.addEventListener("DOMContentLoaded", init);
else
  document.attachEvent("onreadystatechange", function() {
    if (document.readyState == "complete") init();
  });
