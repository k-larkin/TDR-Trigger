from ROOT import *
import argparse
parser =  argparse.ArgumentParser(description='ECAL TPG Flat Tree Reader')
parser.add_argument('-i', '--inputFile', dest='inputf', required=True, type=str, default=None)
parser.add_argument('-o', '--outputFile', dest='outputf', required=False, type=str, default="output.root")
parser.add_argument('-l', '--legend', dest='leg', type=str, default=None)

opt = parser.parse_args()

fnames = opt.inputf.split(',')
files = []
for f in fnames:
  files.append(TFile(f))

#repeat here on to create output
rFile0 = TFile(fnames[0])
rTree0 = rFile0.Get("TPGtree")

nevs0 = rTree0.GetEntriesFast()

'''
Tree variables:
tpIphi - TP iPhi (phi coordinate in #crystal units)
tpIeta - TP iEta (eta coordinate in #crystal units)
rhIphi - RecHit iPhi
rhIeta - RecHit iEta
eRec - RecHit Energy (in GeV)
tpgADC - TP Energy in ADC counts
tpgGeV - TP Energy in GeV
'''

#Create Histogram
eRec0 = TH1F('eRec_PU0', ';RecHit Energy [GeV];Events', 100, 0, 20)
eRec140 = TH1F('eRec_PU140', ';RecHit Energy [GeV];Events', 100, 0, 20)
eRec200 = TH1F('eRec_PU200', ';RecHit Energy [GeV];Events', 100, 0, 20)

for x in range(0, nevs0):
  rTree0.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs0),'  - RecHit Energy:', rTree0.eRec

  #Fill histograms
  eRec0.Fill(rTree0.eRec)

gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)
c = TCanvas('c', 'c', 800, 600)
c.SetLogy()
leg = TLegend(0.7, 0.7, 0.89, 0.89)
leg.SetLineWidth(0)
leg.SetBorderSize(0)
leg.SetFillStyle(0)

if opt.leg is not None:
  legs = opt.leg.split(',')
  leg.AddEntry(eRec0, legs[0], 'l')
  leg.AddEntry(eRec140, legs[1], 'l')
  leg.AddEntry(eRec200, legs[2], 'l')

eRec0.SetLineColor(1)
eRec0.Draw('hist')
norm0 = eRec0.Integral()
eRec0.Scale(1./norm0)
if opt.leg is not None: leg.Draw('same')

#2
rFile1 = TFile(fnames[1])
rTree1 = rFile1.Get("TPGtree")

nevs1 = rTree1.GetEntriesFast()

for x in range(0, nevs1):
  rTree1.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs1),'  - RecHit Energy:', rTree1.eRec

  #Fill histograms
  eRec140.Fill(rTree1.eRec)

eRec140.SetLineColor(2)
eRec140.Draw('hist same')
norm1 = eRec140.Integral()
eRec140.Scale(1./norm1)

#3
rFile2 = TFile(fnames[2])
rTree2 = rFile2.Get("TPGtree")

nevs2 = rTree2.GetEntriesFast()

for x in range(0, nevs2):
  rTree2.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs2),'  - RecHit Energy:', rTree2.eRec
  #Fill histograms
  eRec200.Fill(rTree2.eRec)

eRec200.SetLineColor(4)
eRec200.Draw('hist same')
norm2 = eRec200.Integral()
eRec200.Scale(1./norm2)
title = TPaveLabel(.1, 0.94, .9, .98, "RecHit Energy No Filter")
title.Draw('same')

#Create output file, if file already exists, will be overwritten
oFile = TFile(opt.outputf, "RECREATE")
oFile.cd()
#Write histograms to file
eRec0.Write()
eRec140.Write()
eRec200.Write()
c.SaveAs(opt.outputf+'.pdf')
#Close file
oFile.Close()
