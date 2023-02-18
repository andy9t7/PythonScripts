import slicer
import vtk
import json

# Import segmentation from a nrrd + color table file
colorNode = slicer.util.loadColorTable('/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/data/hncma-atlas-lut.ctbl')
segmentation = slicer.util.loadSegmentation("/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/data/hncma-atlas.nrrd", {'colorNodeID': colorNode.GetID()})

atlasStructureJSON = json.load(open('/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/data/atlasStructure.json'))

model = slicer.util.loadModel("/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/data/hncma-atlas-cleaned-single.vtk") #vtkMRMLModelNode
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

def getLabelArray1(mesh, segmentation, atlasStructureJSON):
   sliceViewLabel = "Red"  # any slice view where segmentation node is visible works
   sliceViewWidget = slicer.app.layoutManager().sliceWidget(sliceViewLabel)
   segmentationsDisplayableManager = sliceViewWidget.sliceView().displayableManagerByClassName("vtkMRMLSegmentationsDisplayableManager2D")

   label_array = vtk.vtkIntArray()
   label_array.SetName("atlas-label")

   # for tracking progress
   indexAt25 = round(mesh.GetPoints().GetNumberOfPoints())/4
   indexAt50 = round(mesh.GetPoints().GetNumberOfPoints())/2
   indexAt75 = round(mesh.GetPoints().GetNumberOfPoints())*3/4

   for pointIndex in range(mesh.GetPoints().GetNumberOfPoints()):

      if pointIndex == indexAt25:
         print("25/100")

      if pointIndex == indexAt50:
         print("50/100")

      if pointIndex == indexAt75:
         print("75/100")

      coord = [0, 0, 0]
      mesh.GetPoint(pointIndex, coord)

      segmentIds = vtk.vtkStringArray()
      segmentationsDisplayableManager.GetVisibleSegmentsForPosition(coord, segmentation.GetDisplayNode(), segmentIds)
      
      for idIndex in range(segmentIds.GetNumberOfValues()):
         segment = segmentation.GetSegmentation().GetSegment(segmentIds.GetValue(idIndex))
         for segmentName in atlasStructureJSON:
            if segmentName['@type'] == 'Structure':
               if segmentName['annotation']['name'] == segment.GetName():
                  label_array.InsertNextValue(segmentName['sourceSelector'][0]['dataKey']) 
   return label_array


label_array = getLabelArray1(mesh, segmentation, atlasStructureJSON)

mesh.GetPointData().AddArray(label_array)

writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName("/Users/andy/Documents/PythonScripts/labelVTKPoints/hncma-atlas-cleaned-single-labelled.vtk")
writer.SetInputData(mesh)
writer.SetDataModeToAscii()
writer.Write()
      
exit()