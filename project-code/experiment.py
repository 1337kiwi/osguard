#!/usr/bin/env python3

from langchain_community.llms import Ollama
import logging
import re
import json

# Set logging level
logging.basicConfig(level=logging.INFO)

# Perm mappings
perm_field = {
  "r": "readfiles",
  "w": "writefiles",
  "x": "binaries"
}

# Dataset folder
data_dir = "../Dataset-Generation"

# langchain.debug = True

def run_experiment(perm: str, dataset: str, modelfile: str):

    # Clear perm results file
    for letter in perm:
        with open(f"results/results_{modelfile}-{letter}-{dataset}.csv", "w") as out:
            out.write("id,perm,required,filename\n")

    #Link model
    llm = Ollama(model=modelfile)

    #Open code dataset
    print("-----Evaluating " + perm + " permission-----")
    cm = open(f"{data_dir}/{dataset}_data.csv", "r")

    # for each in code line in csv
    for code in cm:
        
        # ignore id, get code
        id, code = code.split(",", maxsplit=1)

        logging.info(f"Code: {code}")

        # Get llm response
        resp = llm.invoke(code)

        #Strip newlines
        resp = resp.replace('\n', '')
        #Strip \
        resp = resp.replace('\\', '')

        logging.info(f"Json response: {resp}")
        resp_json = json.loads(resp)

        #For each perm in perm string
        for letter in perm:
            #Set json field
            field = perm_field[letter]

            #Field found and is empty
            if field in resp_json and len(resp_json[field]) == 0:
                with open(f"results/results_{modelfile}-{letter}-{dataset}.csv", "a") as out:
                        out.write(f"{id},{letter},no,\n")
                logging.info(f"Wrote {field} statement for: {json.dumps(resp_json)}")
            #Field found and has files
            elif field in resp_json and len(resp_json[field]) > 0:
                with open(f"results/results_{modelfile}-{letter}-{dataset}.csv", "a") as out:
                        for file in resp_json[field]:
                            out.write(f"{id},{letter},yes,{file}\n")
                logging.info(f"Wrote {field} statement for: {json.dumps(resp_json)}")
            else:
                logging.info("Fail to parse statement for: " + json.dumps(resp_json))
    cm.close()


run_experiment(perm="r", dataset="r", modelfile="OsGuard-r")
run_experiment(perm="r", dataset="w", modelfile="OsGuard-r")
run_experiment(perm="r", dataset="x", modelfile="OsGuard-r")
run_experiment(perm="w", dataset="r", modelfile="OsGuard-w")
run_experiment(perm="w", dataset="w", modelfile="OsGuard-w")
run_experiment(perm="w", dataset="x", modelfile="OsGuard-w")
run_experiment(perm="x", dataset="r", modelfile="OsGuard-x")
run_experiment(perm="x", dataset="w", modelfile="OsGuard-x")
run_experiment(perm="x", dataset="x", modelfile="OsGuard-x")
run_experiment(perm="rwx", dataset="r", modelfile="OsGuard-rwx")
run_experiment(perm="rwx", dataset="w", modelfile="OsGuard-rwx")
run_experiment(perm="rwx", dataset="x", modelfile="OsGuard-rwx")
run_experiment(perm="r", dataset="r", modelfile="OsGuard-r-fs")
run_experiment(perm="r", dataset="w", modelfile="OsGuard-r-fs")
run_experiment(perm="r", dataset="x", modelfile="OsGuard-r-fs")
run_experiment(perm="w", dataset="r", modelfile="OsGuard-w-fs")
run_experiment(perm="w", dataset="w", modelfile="OsGuard-w-fs")
run_experiment(perm="w", dataset="x", modelfile="OsGuard-w-fs")
run_experiment(perm="x", dataset="r", modelfile="OsGuard-x-fs")
run_experiment(perm="x", dataset="w", modelfile="OsGuard-x-fs")
run_experiment(perm="x", dataset="x", modelfile="OsGuard-x-fs")
run_experiment(perm="rwx", dataset="r", modelfile="OsGuard-rwx-fs")
run_experiment(perm="rwx", dataset="w", modelfile="OsGuard-rwx-fs")
run_experiment(perm="rwx", dataset="x", modelfile="OsGuard-rwx-fs")