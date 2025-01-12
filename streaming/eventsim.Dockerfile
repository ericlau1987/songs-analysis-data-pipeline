FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https && \
    echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list && \
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add - && \
    apt-get update && \
    apt-get install -y wget unzip openjdk-8-jdk scala sbt && \
    rm -rf /var/lib/apt/lists/*

// ... rest of the file remains the same ...