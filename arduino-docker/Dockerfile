FROM alpine:3.19

# System dependencies
# - curl + bash: needed by the arduino-cli install script
# - git: needed by arduino-cli for some library operations
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    bash \
    git

# Install pyserial
RUN pip3 install --break-system-packages pyserial==3.5

# Install arduino-cli into /usr/local/bin
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh \
    | BINDIR=/usr/local/bin sh

# Initialise the arduino-cli config file
RUN arduino-cli config init

# Download the AVR platform (avr-gcc, avrdude, core libraries)
# This is ~150 MB and is cached as a Docker layer after the first build
RUN arduino-cli core update-index && \
    arduino-cli core install arduino:avr

WORKDIR /app
COPY requirements.txt .
COPY server.py .
COPY sketch/ ./sketch/

EXPOSE 9000

# On container start:
#   1. Compile the sketch for the Uno
#   2. Upload it to the board via /dev/ttyACM0
#   3. Start the TCP bridge server
CMD ["bash", "-c", \
    "arduino-cli compile  arduino:avr:mega /app/sketch/blink_serial && \
     arduino-cli upload   arduino:avr:mega --port /dev/ttyACM0 /app/sketch/blink_serial && \
     python3 server.py"]
