# JetResponse
 Welcome to my idiosynchratic code framework that runs on Kevin's ntuples. I wrote
 this mostly yesterday. The code creates a tree that will be used in attempt to
 extract the jet response using density regression and tag and probe methods.

# Regression inputs: 
 1. Tag pT (tag is the well-reconstructed pT in the event)
 2. Probe eta (probe is the leading jet)
 3. Alpha (Measure of the additional jet activity, using the Niedziela Projection)
 Regression target:
 response = pT(probe)/pT(tag)

#Running the code
 To run this code interactively, do
 python python/BuildResponseTree.py MC_GJets 2016 quickrun

 quickrun tells the code to only run over a few files. you can leave this off and
the code will analyze all events
