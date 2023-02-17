import slicer
import vtk
import json

# Import segmentation from a nrrd + color table file
colorNode = slicer.util.loadColorTable('/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/hncma-atlas-lut.ctbl')
segmentation = slicer.util.loadSegmentation("/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/hncma-atlas.nrrd", {'colorNodeID': colorNode.GetID()})

atlasStructureJSON = json.load(open('/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/atlasStructure.json'))

model = slicer.util.loadModel("/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/hncma-atlas-cleaned-single.vtk") #vtkMRMLModelNode
mesh = model.GetMesh() #vtkUnstructuredGrid

def getLabelArray(mesh, segmentation, atlasStructureJSON):
   sliceViewLabel = "Red"  # any slice view where segmentation node is visible works
   sliceViewWidget = slicer.app.layoutManager().sliceWidget(sliceViewLabel)
   segmentationsDisplayableManager = sliceViewWidget.sliceView().displayableManagerByClassName("vtkMRMLSegmentationsDisplayableManager2D")

   label_array = vtk.vtkIntArray()
   label_array.SetName("atlas-label")
   cellIds = vtk.vtkIdList() # cell ids store to
   for cellIndex in range(mesh.GetNumberOfCells()): # for every cell
      mesh.GetCellPoints(cellIndex, cellIds) # get ids of points of the given cell
      for i in range(0, cellIds.GetNumberOfIds()): # for every points of the given cell
         coord=mesh.GetPoint(cellIds.GetId(i)) # get coordinates of the given point of the given cell, type: class 'tuple'

         segmentIds = vtk.vtkStringArray()
         segmentationsDisplayableManager.GetVisibleSegmentsForPosition(coord, segmentation.GetDisplayNode(), segmentIds)
         print(segmentIds)
         for idIndex in range(segmentIds.GetNumberOfValues()):
            segment = segmentation.GetSegmentation().GetSegment(segmentIds.GetValue(idIndex))
            for segmentName in atlasStructureJSON:
               if segmentName['@type'] == 'Structure':
                  if segmentName['annotation']['name'] == segment.GetName():
                     label_array.InsertNextValue(segmentName['sourceSelector'][0]['dataKey']) 
   return label_array


label_array = getLabelArray(mesh, segmentation, atlasStructureJSON)

mesh.GetPointData().AddArray(label_array)

writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName("/Users/andy/Documents/PythonScripts/labelVTKPoints/hncma-atlas-cleaned-single-labelled.vtk")
writer.SetInputData(mesh)
writer.SetDataModeToAscii()
writer.Write()
      
exit()