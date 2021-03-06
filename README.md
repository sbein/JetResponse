# Jet Response
Welcome to an idiosynchratic code framework. The goal is to extract the detector response to jets from data using tag and probe methods and multivariate density estimation. The code runs on Kevin's ntuples. The first task of the code is to create a tree that will be used for multivariate density regression.

# Regression 
Inputs to the regression:
 1. Tag pT (tag is the well-reconstructed pT in the event)
 2. Probe eta (probe is the leading jet)
 3. Alpha (Measure of the additional jet activity, using the Niedziela Projection)

Regression target:

response = pT(probe)/pT(tag)

#Running the code
To run this code interactively, do
```
python python/BuildResponseTree.py MC_GJets 2016 quickrun
```
MC tells the code the events are from monte carlo. GJets is the physics process and is matched to the data set name in the code. quickrun tells the code to only run over a few files. you can leave this off and all events will be analyzed.
