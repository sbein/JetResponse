import sys
from ROOT import *
from array import array
import numpy as np

tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 52
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()

def histoStyler(h,color):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    size = 0.065
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size)
    h.GetXaxis().SetLabelSize(size)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(0.9)
    h.Sumw2()

def passesUniversalSelection(t):
    if not (bool(t.JetID) and  t.NVtx>0): return False
    if not (t.eeBadScFilter==1 and t.HBHENoiseFilter and t.HBHEIsoNoiseFilter and t.CSCTightHaloFilter): return False
    if not (t.HBHENoiseFilter==1 and t.HBHEIsoNoiseFilter==1 and t.eeBadScFilter==1 and t.EcalDeadCellTriggerPrimitiveFilter==1 and t.BadChargedCandidateFilter and t.BadPFMuonFilter): return False#
    if not (t.Electrons.size()==0 and t.Muons.size()==0 and t.isoElectronTracks==0 and t.isoMuonTracks==0 and t.isoPionTracks==0): return False
    if not  passQCDHighMETFilter(t): return False
    if not t.PFCaloMETRatio<5: return False
    return True


def passQCDHighMETFilter(t):
    metvec = mkmet(t.MET, t.METPhi)
    for ijet, jet in enumerate(t.Jets):
        if not (jet.Pt() > 200): continue
        if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
        if (abs(jet.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
    return True

def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met
