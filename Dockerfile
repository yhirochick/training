FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

# Install TeX Live with LuaLaTeX and required packages
RUN apt-get update && apt-get install -y \
    texlive-full \
    texlive-luatex \
    texlive-lang-japanese \
    fonts-noto-cjk \
    python3 \
    python3-pip \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir jinja2 flask

# Set working directory
WORKDIR /workspace

# Expose Flask port
EXPOSE 5000

# Default command (can be overridden)
CMD ["/bin/bash"]
