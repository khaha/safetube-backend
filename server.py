import subprocess

subprocess.run([
    "java",
    "-Xmx2g",
    "-cp", "VnCoreNLP-1.1.1.jar",
    "vn.corenlp.pipeline.StanfordCoreNLPServer",
    "-port", "54053",
    "-annotators", "wseg,pos,ner,parse"
])

