#ifndef USEFULJET_H
#define USEFULJET_H

#include <cmath>
#include <vector>
#include <iostream>
#include <stdlib.h>
#include "TMinuit.h"
#include "TLorentzVector.h"
#include "TF1.h"
#include "TH1F.h"
#include "TGraph.h"

//using namespace std;

struct UsefulJet
{ 
  TLorentzVector tlv;
  double csv;
  double originalPt;
  bool operator < (const UsefulJet& jet) const 
  {
    return (tlv.Pt() > jet.tlv.Pt());
  }
  UsefulJet& operator+=(const UsefulJet& other)
  {
    tlv += other.tlv;
    return *this;
  }
  UsefulJet& operator-=(const UsefulJet& other)
  {
    tlv -= other.tlv;
    return *this;
  }
  UsefulJet& operator*=(const double multiplier)
  {
    tlv *= multiplier;
    return *this;
  }
UsefulJet(TLorentzVector tlv_ = TLorentzVector(), double csv_ = 0, double originalPt_=0) :
  tlv(tlv_), csv(csv_), originalPt(originalPt_) {}
  double Pt() const{return tlv.Pt();}
  double Px() const{return tlv.Px();}
  double Py() const{return tlv.Py();}
  double Pz() const{return tlv.Pz();}
  double Eta()const{return tlv.Eta();}
  double Phi() const{return tlv.Phi();}
  double E() const{return tlv.E();}
  double Csv() const{return csv;}
  double OriginalPt() const{return originalPt;}
  UsefulJet Clone()
  {
    UsefulJet newjet(tlv, csv, originalPt);
    return newjet;
  }
  double DeltaR(const UsefulJet& other)
  {
    return tlv.DeltaR(other.tlv);
  }
  double DeltaR(const TLorentzVector& other)
  {
    return tlv.DeltaR(other);
  }
  double DeltaPhi(const UsefulJet& other)
  {
    return tlv.DeltaPhi(other.tlv);
  }
  double DeltaPhi(const TLorentzVector& other)
  {
    return tlv.DeltaPhi(other);
  }

};

struct TemplateSet
{ 
 
  
  TH1F * hPtTemplate;
  TH1F * hEtaTemplate;
  TH1F * hHtTemplate;

  std::vector<std::vector<std::vector<TH1F*>>> ResponseHistos;
  std::vector<std::vector<std::vector<TGraph*>>> ResponseFunctions;
  std::vector<TGraph*> gGenMhtPtTemplatesB0, gGenMhtPtTemplatesB1, gGenMhtPtTemplatesB2, gGenMhtPtTemplatesB3;
  std::vector<TGraph*> gGenMhtDPhiTemplatesB0, gGenMhtDPhiTemplatesB1, gGenMhtDPhiTemplatesB2, gGenMhtDPhiTemplatesB3;
				    
  double rebThresh;
  double lhdMhtThresh;
  std::vector<UsefulJet> untouchedJets;

  int nparams;
  std::vector<UsefulJet> dynamicJets;

  TemplateSet() {}
};

#endif
