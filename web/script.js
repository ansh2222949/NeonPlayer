const elMainCard = document.getElementById("mainCard");
const elPlayPauseIcon = document.getElementById("playPauseIcon"),
  elVinylContainer = document.getElementById("vinylContainer");
const elSongTitle = document.getElementById("songTitle"),
  elSongArtist = document.getElementById("songArtist");
const elProgressBar = document.getElementById("progressBar"),
  elMiniProgress = document.getElementById("miniProgress");
const elVinylThumb = document.getElementById("vinylThumb"),
  elVinylDefault = document.getElementById("vinylDefault");
const elBgImageLayer = document.getElementById("bgImageLayer"),
  elAppBody = document.getElementById("appBody"),
  elPinBtn = document.getElementById("pinBtn");

let lastProgressValue = -1,
  lastProgressTs = Date.now();
let lastThumb = "",
  idleTimer = null,
  isDragging = false;
let manualOverride = false,
  overrideTimer = null;
let lastState = { is_playing: null, title: "" };

function handleActivity() {
  if (elMainCard.classList.contains("minimized-mode")) {
    elMainCard.classList.remove("minimized-mode");
    if (window.pywebview?.api) window.pywebview.api.resize_window(310, 220);
  }
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    if (!elMainCard.matches(":hover")) {
      elMainCard.classList.add("minimized-mode");
      if (window.pywebview?.api) window.pywebview.api.resize_window(310, 80);
    }
  }, 5000);
}

function nextTheme() {
  const themes = [
    "theme-neon",
    "theme-night",
    "theme-cyber",
    "theme-emerald",
    "theme-sunset",
    "theme-rose",
  ];
  elAppBody.className =
    themes[(themes.indexOf(elAppBody.className) + 1) % themes.length];
}

function togglePin() {
  window.pywebview.api.toggle_pin().then((p) => {
    p
      ? elPinBtn.classList.add("active-pin")
      : elPinBtn.classList.remove("active-pin");
  });
}

function sendAction(cmd) {
  if (cmd === "play_pause") {
    manualOverride = true;
    clearTimeout(overrideTimer);

    const isPlaying = elPlayPauseIcon.innerText === "⏸";
    elPlayPauseIcon.innerText = isPlaying ? "▶" : "⏸";
    if (!isPlaying) {
      elVinylContainer.classList.add("spin");
      elVinylContainer.classList.remove("paused");
    } else {
      elVinylContainer.classList.remove("spin");
      elVinylContainer.classList.add("paused");
    }

    overrideTimer = setTimeout(() => {
      manualOverride = false;
    }, 2000);
  }
  window.pywebview.api.control(cmd);
}

function onSeek(val) {
  isDragging = true;
  elMiniProgress.style.width = val + "%";
}
function onSeekEnd(val) {
  window.pywebview.api.seek_music(parseInt(val));
  setTimeout(() => {
    isDragging = false;
  }, 400);
}

async function updateUI() {
  if (!window.pywebview?.api) return;

  try {
    const data = await window.pywebview.api.get_music_data();

    if (data && data.title && data.title !== "No Media") {
      const now = Date.now();
      const progressDiff = Math.abs(data.progress - lastProgressValue);

      if (progressDiff > 0.005) {
        lastProgressValue = data.progress;
        lastProgressTs = now;
      }

      const isMoving = now - lastProgressTs < 5000;
      const actuallyPlaying = isMoving;

      if (!manualOverride) {
        if (actuallyPlaying !== lastState.is_playing) {
          elPlayPauseIcon.innerText = actuallyPlaying ? "⏸" : "▶";
          if (actuallyPlaying) {
            elVinylContainer.classList.add("spin");
            elVinylContainer.classList.remove("paused");
          } else {
            elVinylContainer.classList.remove("spin");
            elVinylContainer.classList.add("paused");
          }
          lastState.is_playing = actuallyPlaying;
        }
      }

      if (data.title !== lastState.title) {
        elSongTitle.innerText = data.title;
        elSongArtist.innerText = data.artist;
        lastState.title = data.title;
        lastProgressTs = now;
      }

      if (data.thumbnail && data.thumbnail !== lastThumb) {
        lastThumb = data.thumbnail;
        elVinylThumb.src = data.thumbnail;
        elVinylThumb.classList.remove("hidden");
        elVinylDefault.classList.add("hidden");
        elBgImageLayer.style.backgroundImage = `url(${data.thumbnail})`;
        elBgImageLayer.classList.add("active");
      }

      if (!isDragging) {
        elProgressBar.value = data.progress;
        elProgressBar.style.background = `linear-gradient(to right, var(--accent) ${data.progress}%, rgba(255,255,255,0.1) ${data.progress}%)`;
        elMiniProgress.style.width = data.progress + "%";
      }
    }
  } catch (e) {
    console.error("API sync error");
  }
}

function heartbeat() {
  updateUI();
  setTimeout(heartbeat, 500);
}

window.addEventListener("pywebviewready", () => {
  handleActivity();
  heartbeat();
});

document.addEventListener("mousemove", () => {
  if (!manualOverride) updateUI();
});
