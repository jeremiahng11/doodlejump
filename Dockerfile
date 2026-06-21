# syntax=docker/dockerfile:1

# ---- Build stage: compile the pygame game to WebAssembly with pygbag ----
FROM python:3.12-slim AS build
WORKDIR /src

# pygbag is only needed at build time to package the game into build/web/
RUN pip install --no-cache-dir pygbag

# Copy the whole project (Assets/, Sprites/, Buttons/, *.py).
# pygbag bundles this directory tree into the playable .apk payload.
COPY . .

# Produces /src/build/web/ : index.html + the bundled game + loader.
RUN python -m pygbag --build main.py

# ---- Serve stage: static nginx serving the WASM build ----
FROM nginx:alpine
COPY --from=build /src/build/web /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
