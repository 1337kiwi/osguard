sudo apt update
sudo apt install -y cmake
wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
rm -rf go1.22.2.linux-amd64.tar.gz
mkdir /home/$USER/go
cd /home/$USER/go
git clone https://github.com/NousResearch/ollama.git
cd ollama
git checkout grammar
go generate ./...
go build .
export PATH=$PATH:/home/$USER/go/ollama
./ollama serve