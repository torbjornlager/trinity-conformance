FROM local/conformance-input-trealla:20261120 AS trealla
FROM local/conformance-input-gnu:20261120 AS gnu
FROM local/conformance-input-swi:20261120
USER root
COPY --from=trealla /opt/trealla/ /opt/trealla/
COPY --from=trealla /app/*.pl /work/trealla/
COPY --from=gnu /app/isobase/ /work/gnu/isobase/
RUN apt-get update && apt-get install -y --no-upgrade --no-install-recommends procps && rm -rf /var/lib/apt/lists/*
RUN git config --global user.name 'Conformance fixture snapshot' && git config --global user.email 'fixture@localhost' \
 && cd /work/trealla && git init -q && git add . && git commit -q -m 'Exact deployed N5 runtime snapshot' \
 && cd /work/gnu && git init -q && git add . && git commit -q -m 'Exact deployed N6 ISOBASE snapshot'
ENV TPL_LIBRARY_PATH=/opt/trealla/library
ENTRYPOINT []
