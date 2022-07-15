FROM python:3.9

RUN apt-get update -y && \
    apt-get upgrade -y

WORKDIR /tmp
RUN wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_15.zip && \
    unzip sf_15.zip && \
    cd Stockfish-sf_15/src && \
    make build ARCH=x86-64-modern && \
    cp stockfish /usr/local/bin/stockfish

WORKDIR /stockfish-socket-server
ENV PYTHONPATH=/stockfish-socket-server
COPY . .

# install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Open ports and start server
EXPOSE 5000
ENTRYPOINT ["/bin/bash"]
# CMD ["start_server.sh"]
