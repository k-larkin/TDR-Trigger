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
tpgGeV0 = TH1F('tpgGeV_PU0', ';TP Energy [GeV];Events', 100, 0, 20)
tpgGeV140 = TH1F('tpgGeV_PU140', ';TP Energy [GeV];Events', 100, 0, 20)
tpgGeV200 = TH1F('tpgGeV_PU200', ';TP Energy [GeV];Events', 100, 0, 20)

for x in range(0, nevs0):
  rTree0.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs0),'  - TP Energy:', rTree0.tpgGeV

  #Fill histograms
  tpgGeV0.Fill(rTree0.tpgGeV)

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
  leg.AddEntry(tpgGeV0, legs[0], 'l')
  leg.AddEntry(tpgGeV140, legs[1], 'l')
  leg.AddEntry(tpgGeV200, legs[2], 'l')

tpgGeV0.SetLineColor(1)
tpgGeV0.Draw('hist')
norm0 = tpgGeV0.Integral()
tpgGeV0.Scale(1./norm0)
if opt.leg is not None: leg.Draw('same')

#2
rFile1 = TFile(fnames[1])
rTree1 = rFile1.Get("TPGtree")

nevs1 = rTree1.GetEntriesFast()

for x in range(0, nevs1):
  rTree1.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs1),'  - TP Energy:', rTree1.tpgGeV

  #Fill histograms
  tpgGeV140.Fill(rTree1.tpgGeV)

tpgGeV140.SetLineColor(2)
tpgGeV140.Draw('hist same')
norm1 = tpgGeV140.Integral()
tpgGeV140.Scale(1./norm1)

#3
rFile2 = TFile(fnames[2])
rTree2 = rFile2.Get("TPGtree")

nevs2 = rTree2.GetEntriesFast()

for x in range(0, nevs2):
  rTree2.GetEntry(x) #point to entry #x in the tree
  if x%10000 == 0:
    print 'Event #',str(x)+'/'+str(nevs2),'  - TP Energy:', rTree2.tpgGeV

  #Fill histograms
  tpgGeV200.Fill(rTree2.tpgGeV)

tpgGeV200.SetLineColor(4)
tpgGeV200.Draw('hist same')
norm2 = tpgGeV200.Integral()
tpgGeV200.Scale(1./norm2)

#Create output file, if file already exists, will be overwritten
oFile = TFile(opt.outputf, "RECREATE")
oFile.cd()
#Write histograms to file
tpgGeV0.Write()
tpgGeV140.Write()
tpgGeV200.Write()
c.SaveAs(opt.outputf+'.pdf')
#Close file
oFile.Close()
