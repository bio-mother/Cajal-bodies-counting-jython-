from ij import WindowManager as WM
from ij import IJ, ImagePlus
from ij.plugin import ZProjector
from ij.process import ImageProcessor
from ij.plugin.filter import ThresholdToSelection
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable
from ij.io import FileSaver
import random

imps = map(WM.getImage, WM.getIDList())
def match(imp):  
  """ Returns true if the image title contains the word 'tile'"""  
  return imp.title.find("tile") > -1 
pic = filter(match, imps)

#Z-project stack summarize (https://wiki.cmci.info/documents/120206pyip_cooking/python_imagej_cookbook)
def sumzp(imp):
	sumzp = ZProjector(imp)
	sumzp.setMethod(ZProjector.SUM_METHOD)
	sumzp.doProjection() 
	sumzpimp = sumzp.getProjection()
	return sumzpimp
#make a program for img random names!!!

nuc = sumzp(pic[10])
cb1 = sumzp(pic[0])
cb2 = sumzp(pic[0])
rm = RoiManager.getInstance()
if (rm==None):
	rm = RoiManager()
rm.runCommand("Reset")
IJ.run(nuc, "Smooth", "")
IJ.run(nuc, "16-bit", "")
IJ.run(nuc, "Auto Threshold", "method=Otsu white")
IJ.run(nuc, "Analyze Particles...", "size=1000-5000 circularity=0.30-1.00 display exclude add composite")
roi_nuc = rm.getRoisAsArray()
IJ.run("Clear Results", "")
rm.runCommand("Set Color", "yellow")
rm.setSelectedIndexes(range(len(roi_nuc)))
rm.runCommand(cb2, "Combine")
rm.runCommand(cb2, "Draw")
rm.setSelectedIndexes(range(len(roi_nuc)))
rm.runCommand(cb1, "Combine")
IJ.run(cb1, "Find Maxima...", "prominence=270 output=[Point Selection]")
cb2.show()
cb1.show()
path = "C:/Users/losti/Documents/Universitetiy/Лаба моя лаба/Тельца Кахаля/results3/" + str(random.choice(range(100000, 999999))) + ".tiff"
FileSaver(cb1).saveAsTiff(path)
path = "C:/Users/losti/Documents/Universitetiy/Лаба моя лаба/Тельца Кахаля/results3/" + str(random.choice(range(100000, 999999))) + ".tiff"
FileSaver(cb2).saveAsTiff(path)

i = 0
#for roi in roi_nuc:
#	cb.setRoi(roi)
#	IJ.run(cb, "Find Maxima...", "prominence=270 output=Count")
#	print ResultsTable.getResultsTable().getValue("Count", i)
#	cb.show()
#	i += 1
#nuc.show()