# CSC591-Project-SecurityinLLMs

## To the run the project

Navigate to /project-code and run

$> sudo apt update

$> sudo apt install -y cmake

$> wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz

$> sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz

$> export PATH=$PATH:/usr/local/go/bin

$> rm -rf go1.22.2.linux-amd64.tar.gz

$> mkdir /home/$USER/go

$> cd /home/$USER/go

$> git clone https://github.com/NousResearch/ollama.git

$> cd ollama

$> git checkout grammar

$> go generate ./...

$> go build .

$> export PATH=$PATH:/home/$USER/go/ollama

$> - ./ollama serve


Then in a new terminal, run

$> pip3 install -r requirements.txt

To run the experiment (This code has been run on a Ubuntu 22 vm with cuda):

$> python3 experiment.py

To check accuracy:

$> python3 accuracy.py

To check metrics:

$> python3 metrics.py

