


setup_ollama() {
    curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
    tar -C /usr -xzf ollama-linux-amd64.tgz
}

setup_ollama