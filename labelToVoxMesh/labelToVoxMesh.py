import vtk

# Read image data

image = vtk.vtkMetaImageReader()
image.SetFileName("test.mha")
image.Update()

start_label = 1
end_label = 2

# # Pad the volume so that we can change the point data into cell
# # data.
extent = image.GetOutput().GetExtent()
pad = vtk.vtkImageWrapPad()
pad.SetInputConnection(image.GetOutputPort())
pad.SetOutputWholeExtent(extent[0], extent[1] + 1, extent[2], extent[3] + 1, extent[4], extent[5] + 1)
pad.Update()

# # Copy the scalar point data of the volume into the scalar cell data
pad.GetOutput().GetCellData().SetScalars(image.GetOutput().GetPointData().GetScalars())

selector = vtk.vtkThreshold()
selector.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject().FIELD_ASSOCIATION_CELLS,
                                vtk.vtkDataSetAttributes().SCALARS)
selector.SetInputConnection(pad.GetOutputPort())
selector.SetLowerThreshold(start_label)
selector.SetUpperThreshold(end_label)
selector.Update()

# Shift the geometry by 1/2
transform = vtk.vtkTransform()
transform.Translate(-0.5, -0.5, -0.5)

transform_model = vtk.vtkTransformFilter()
transform_model.SetTransform(transform)
transform_model.SetInputConnection(selector.GetOutputPort())

scalarsOff = vtk.vtkMaskFields()
scalarsOff.SetInputConnection(transform_model.GetOutputPort())
scalarsOff.CopyAttributeOff(vtk.vtkMaskFields.POINT_DATA, vtk.vtkDataSetAttributes.SCALARS)
scalarsOff.CopyAttributeOff(vtk.vtkMaskFields.CELL_DATA, vtk.vtkDataSetAttributes.SCALARS)
scalarsOff.Update()

# cell = vtk.vtkPointDataToCellData()
# cell.SetInputConnection(transform_model.GetOutputPort())
# cell.Update()

#Write Unstructured Grid as vtk file
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName("test.vtk")
writer.SetInputConnection(transform_model.GetOutputPort())
writer.SetDataModeToAscii()
writer.Write()
