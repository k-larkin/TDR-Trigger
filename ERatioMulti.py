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
e_ratio0 = TH1F('e_ratioPU0', ';Energy Ratio [TP/RecHit];Events', 100, 0, 2)
e_ratio140 = TH1F('e_ratioPU140', ';Energy Ratio [TP/RecHit];Events', 100, 0, 2)
e_ratio200 = TH1F('e_ratioPU200', ';Energy Ratio [TP/RecHit];Events', 100, 0, 2)

for x in range(0, nevs0):
  rTree0.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs0),'  - Energy Ratio:', rTree0.tpgGeV / rTree0.eRec
  
  #Fill histograms
  if rTree0.eRec !=0 #add 'and rTree0.tpgGeV>5:' to cut by energy
    e_ratio0.Fill(rTree0.tpgGeV / rTree0.eRec)

gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)
c = TCanvas('c', 'c', 800, 600)
leg = TLegend(0.7, 0.7, 0.89, 0.89)
leg.SetLineWidth(0)
leg.SetBorderSize(0)
leg.SetFillStyle(0)

if opt.leg is not None:
  legs = opt.leg.split(',')
  leg.AddEntry(e_ratio0, legs[0], 'l')
  leg.AddEntry(e_ratio140, legs[1], 'l')
  leg.AddEntry(e_ratio200, legs[2], 'l')

e_ratio0.SetLineColor(1)
e_ratio0.Draw('hist')
norm0 = e_ratio0.Integral()
e_ratio0.Scale(1./norm0)
if opt.leg is not None: leg.Draw('same')

#2
rFile1 = TFile(fnames[1])
rTree1 = rFile1.Get("TPGtree")

nevs1 = rTree1.GetEntriesFast()

for x in range(0, nevs1):
  rTree1.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs1),'  - Energy Ratio:', rTree1.tpgGeV / rTree1.eRec
  
  #Fill histograms
  if rTree1.eRec !=0 #add 'and rTree1.tpgGeV>5:' to cut by energy
    e_ratio140.Fill(rTree1.tpgGeV / rTree1.eRec)

e_ratio140.SetLineColor(2)
e_ratio140.Draw('hist same')
norm1 = e_ratio140.Integral()
e_ratio140.Scale(1./norm1)

#3
rFile2 = TFile(fnames[2])
rTree2 = rFile2.Get("TPGtree")

nevs2 = rTree2.GetEntriesFast()

for x in range(0, nevs2):
  rTree2.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs2),'  - Energy Ratio:', rTree2.tpgGeV / rTree2.eRec
  
  #Fill histograms
  if rTree2.eRec !=0 #add 'and rTree2.tpgGeV>5:' to cut by energy
    e_ratio200.Fill(rTree2.tpgGeV / rTree2.eRec)

e_ratio200.SetLineColor(4)
e_ratio200.Draw('hist same')
norm2 = e_ratio200.Integral()
e_ratio200.Scale(1./norm2)
title = TPaveLabel(.1, 0.94, .9, .98, "Trigger Primitive Energy / RecHit Energy No Filter")
title.Draw('same')

#Create output file, if file already exists, will be overwritten
oFile = TFile(opt.outputf, "RECREATE")
oFile.cd()
#Write histograms to file
e_ratio0.Write()
e_ratio140.Write()
e_ratio200.Write()
c.SaveAs(opt.outputf+'.pdf')
#Close file
oFile.Close()
