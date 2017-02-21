############################
# Date created: Feb 20, 2017
############################


import os, sys
from ROOT import *
from utils import *
from array import array
import numpy as np

pwd = '/uscms_data/d3/sbein/Ra2slashB2016/Nov2016/CMSSW_8_0_22/src/JetResponse'
filenametag = ''
try: datasetID = sys.argv[1]
except: datasetID = 'MC_QCD'
physicsProcess = datasetID[datasetID.find('_')+1:]
datamc = datasetID[:datasetID.find('_')]
try: dsId = sys.argv[2]
except: dsId = '700'
try: quickrun = bool(sys.argv[3])
except: quickrun = False

gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')

def findmatch(thing, group, radius=0-.4):
    matched = False
    for groupmember in group:
        if groupmember.DeltaR(thing)<radius: 
            matched = groupmember
            break
    return matched

def calcSumPt(jets, obj, conesize=0.6, thresh=10):
    sumpt_ = 0
    for jet in jets:
        if not jet.Pt()>thresh:
            continue
        if not (obj.DeltaR(jet.tlv)<conesize):
            continue
        sumpt_+=jet.Pt()
    return sumpt_

#book diagnostic histograms.
hHt = TH1F('hHt','hHt',120,0,2500)
hHt.Sumw2()
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',120,0,2500)
hHtWeighted.Sumw2()
hActivity = TH1F('hActivity','hActivity',100,0,3)
histoStyler(hActivity, 2)
hRatioEtaJetPhoton = TH1F('hRatioEtaJetPhoton','hRatioEtaJetPhoton',100,-3,3)
hEtaJetVsEtaPhoton = TH2F('hEtaJetVsEtaPhoton','hEtaJetVsEtaPhoton',20,-4,4, 20,-4,4)
hDeltaPhiJetPhoton = TH1F('hDeltaPhiJetPhoton','hDeltaPhiJetPhoton',100,0,3.2)
histoStyler(hRatioEtaJetPhoton, kBlue)

#define dimensions of the problem and book axes that have the binning built in.
binPt = [0, 30, 100, 500, 1000, 10000]
binPtArr = array('d',binPt)
nBinPt = len(binPtArr)-1
hPtTemplate = TH1F('hPtTemplate','hPtTemplate',nBinPt,binPtArr)
templatePtAxis = hPtTemplate.GetXaxis()
binEta = [0.0,1.0,1.5,2.3,5.0]
binEtaArr = array('d',binEta)
nBinEta = len(binEtaArr)-1
hEtaTemplate = TH1F('hEtaTemplate','hEtaTemplate',nBinEta,binEtaArr)
templateEtaAxis = hEtaTemplate.GetXaxis()
binAct = [0.1, 0.2, 0.3, 0.4, 0.5]
binActArr = array('d',binAct)
nBinAct = len(binActArr)-1
hActTemplate = TH1F('hActTemplate','hActTemplate',nBinAct,binActArr)
templateActAxis = hActTemplate.GetXaxis()

#declare ugly object full of response histograms for cross checks and validation
hResGenTemplates = ['']
hResInfTemplates = ['']
for ieta in range(1,templateEtaAxis.GetNbins()+1):
    hResGenTemplates.append([''])
    hResInfTemplates.append([''])
    etarange = str(templateEtaAxis.GetBinLowEdge(ieta))+'-'+str(templateEtaAxis.GetBinUpEdge(ieta))
    for ipt in range(1,templatePtAxis.GetNbins()+1):
        lowedge = templatePtAxis.GetBinLowEdge(ipt)
        upedge = templatePtAxis.GetBinUpEdge(ipt)
        ptrange = str(lowedge)+'-'+str(upedge)
        if int(lowedge)<30:
            nbins = 730
            rupper = 4.5
        else:
            nbins = 350
            rupper = 3.0
        start = True
        for iact in range(1,templateActAxis.GetNbins()+1):
          act = templateActAxis.GetBinLowEdge(iact)
          hg = TH1F('hRTemplate(gPt'+ptrange+', gEta'+etarange+')'+'_act'+str(act),'pt(gen)',nbins,0,rupper)
          histoStyler(hg, kBlack)
          if start: hResGenTemplates[-1].append([''])
          hResGenTemplates[-1][-1].append(hg)
          hinf = TH1F('hRTemplate(infPt'+ptrange+', infEta'+etarange+')'+'_act'+str(act),'pt(infen)',nbins,0,rupper)
          histoStyler(hinf, kBlack)
          if start: hResInfTemplates[-1].append([''])
          hResInfTemplates[-1][-1].append(hinf)
          start = False    
hResInfInclusive = TH1F('hResInfInclusive','pt(gen)',nbins,0,rupper)

#declare a nice tree on which the anlaysis will be based
jetEta = np.zeros(1,dtype=float)
phoPt = np.zeros(1,dtype=float)
alpha = np.zeros(1,dtype=float)
response = np.zeros(1,dtype=float)#target for regression
tPhotonJetTree = TTree('tPhotonJetTree','tPhotonJetTree')
tPhotonJetTree.Branch('jetEta', jetEta,'jetEta/D')
tPhotonJetTree.Branch('phoPt', phoPt,'phoPt/D')
tPhotonJetTree.Branch('alpha', alpha,'alpha/D')
tPhotonJetTree.Branch('response', response,'response/D')

#set up event chain
t = TChain('TreeMaker2/PreSelection')
filefile = open(pwd+'/filelists/filelistKevinV12.txt')
rawfiles = filefile.readlines()
filelist = []
for rawfile in rawfiles:
    if physicsProcess=='QCD':
        if not 'HT'+dsId+'to' in rawfile: continue
    elif 'GJets' in physicsProcess:
        if not '.'+physicsProcess in rawfile: continue
    elif not physicsProcess in rawfile: continue
    #print 'checking out', rawfile.strip()
    filelist.append(rawfile.strip())

if quickrun: 
    print "files=",filelist[:1]
    for f in filelist[:15]: 
        t.Add('root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV12/'+f)
        break
    nEvents = min(100000,t.GetEntries())
    verbosity = 100
else: 
    for flong in filelist: t.Add('root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV12/'+flong)
    nEvents = t.GetEntries()
    verbosity = 10000

t.Show(0)
print "nEvents=", nEvents

newFileName = 'JetPho'+"".join(sys.argv[1:])+'.root'
newFileName = newFileName.replace('.root',filenametag+'.root')
f = TFile(newFileName,'recreate')

#event loop
for ientry in range(nEvents):
    if ientry%verbosity==0: print "processing event", ientry, '/', nEvents
    t.GetEntry(ientry)
    hHt.Fill(t.HT)
    hHtWeighted.Fill(t.HT, t.Weight)
    if not passesUniversalSelection(t): continue
    nphotons = len(t.Photons)
    if not (nphotons>0): continue

    recojets = CreateUsefulJetVector(t.Jetsclean, t.Jetsclean_bDiscriminatorCSV)
    softrecojets = CreateUsefulJetVector(t.SoftJets, t.SoftJets_bDiscriminatorCSV)
    recojets = ConcatenateVectors(recojets, softrecojets)
            
    if not len(recojets)>0: continue
    if not len(t.Photons)>0: continue

    overlapping = False
    for ipho in range(len(t.Photons)):
        photon = t.Photons[ipho]
        matched = findmatch(photon, recojets, 0.4)
        if matched: 
            overlapping = True
            break
    if overlapping: continue

    subLeadingJetBlob = TLorentzVector()
    for jet in recojets[1:]: subLeadingJetBlob+=jet.tlv

    photonBlob = TLorentzVector()
    for photon in t.Photons: 
        if not (photon.Pt()>30): continue
        photonBlob+=photon


    PhotonJetSystem = photonBlob.Clone()
    probevec = recojets[0].tlv.Clone()
    probevec *= photonBlob.Pt()/probevec.Pt()
    PhotonJetSystem += probevec
    
    deltaphi = abs(photonBlob.DeltaPhi(recojets[0].tlv))
    hDeltaPhiJetPhoton.Fill(deltaphi)
    if not (deltaphi>2.8): continue    
        
    hRatioEtaJetPhoton.Fill(photonBlob.Eta()/recojets[0].Eta())
    hEtaJetVsEtaPhoton.Fill(photonBlob.Eta(), recojets[0].Eta())

    jetEta[0] = abs(recojets[0].Eta())
    phoPt[0] = photonBlob.Pt()
    ieta = templateEtaAxis.FindBin(jetEta[0])
    ipt = templatePtAxis.FindBin(phoPt[0])

    # Marek's super awesome activity
    try: alpha[0] = subLeadingJetBlob.Pt()/phoPt[0]*abs(TMath.Sin(subLeadingJetBlob.DeltaPhi(PhotonJetSystem)))
    except: alpha[0] = 5
    hActivity.Fill(alpha[0])
    if not (alpha[0]<0.5): continue
    
    response[0] = recojets[0].Pt()/phoPt[0]

    tPhotonJetTree.Fill()
    hResInfInclusive.Fill(response[0])
    
    for iact in range(1, templateActAxis.GetNbins()+1):
        act_thresh = templateActAxis.GetBinLowEdge(iact)
        if not (alpha[0] < act_thresh): continue

        #resolution w.r.t. pho
        #print 'activity', alpha[0], hResInfTemplates[ieta][ipt][iact].GetName()
        hResInfTemplates[ieta][ipt][iact].Fill(response[0])

        #resolution w.r.t. gen
        matched = False
        for genjet in t.GenJets:
            matched = findmatch(genjet,[recojets[0]], 0.4)
            if matched:
                matched = genjet
                ieta = templateEtaAxis.FindBin(abs(matched.Eta()))
                ipt = templatePtAxis.FindBin(matched.Pt())
                break
        if matched: 
            genresponse = recojets[0].Pt()/matched.Pt()
            #genresponse = photonBlob.Pt()/matched.Pt()
            hResGenTemplates[ieta][ipt][iact].Fill(genresponse)

#write tree to file
tPhotonJetTree.Write()
hResInfInclusive.Write()
#write histograms to file
for etachain in hResInfTemplates[1:]:
    for hrat in etachain[1:]:
        for h in hrat[1:]:
            h.Write()
for etachain in hResGenTemplates[1:]:
    for hrat in etachain[1:]:
        for h in hrat[1:]:
            h.Write()
templatePtAxis.Write('hPtAxis')
templateEtaAxis.Write('hPtAxis')
hHt.Write()
hHtWeighted.Write()
hActivity.Write()
hRatioEtaJetPhoton.Write()
hEtaJetVsEtaPhoton.Write()
hDeltaPhiJetPhoton.Write()
f.Close()
