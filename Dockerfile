FROM python:3.9

RUN apt-get update -y && \
    apt-get upgrade -y

# Build stockfish binary
WORKDIR /tmp
RUN wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_15.zip && \
    unzip sf_15.zip && \
    cd Stockfish-sf_15/src && \
    make build ARCH=x86-64-modern && \
    cp stockfish /usr/local/bin/stockfish && \
    rm -rf *sf_15*

# Copy files for websocket server
WORKDIR /stockfish-socket-server
ENV PYTHONPATH=/stockfish-socket-server
COPY . .

# install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Expose port 5000 and override entrypoint
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "-l", "-c"]
