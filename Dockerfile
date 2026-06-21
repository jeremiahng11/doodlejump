# syntax=docker/dockerfile:1

# ---- Build stage: compile the pygame game to WebAssembly with pygbag ----
FROM python:3.12-slim AS build
WORKDIR /src

# pygbag packages the game; ffmpeg transcodes the audio to OGG for the web.
RUN pip install --no-cache-dir pygbag \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the whole project (Assets/, Sprites/, Buttons/, *.py).
# pygbag bundles this directory tree into the playable .apk payload.
COPY . .

# The browser's SDL2_mixer only plays OGG, so transcode every WAV to OGG and
# drop the WAVs from the build tree. sounds.py loads ".ogg" under emscripten,
# so the references line up and pygbag has no WAV files left to choke on.
RUN set -e; \
    for f in Assets/Sounds/*.wav; do \
        ffmpeg -y -i "$f" -c:a libvorbis -q:a 4 "${f%.wav}.ogg" >/dev/null 2>&1; \
        rm -f "$f"; \
    done

# Produces /src/build/web/ : index.html + the bundled game + loader.
RUN python -m pygbag --build main.py

# ---- Serve stage: static nginx serving the WASM build ----
FROM nginx:alpine
COPY --from=build /src/build/web /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
