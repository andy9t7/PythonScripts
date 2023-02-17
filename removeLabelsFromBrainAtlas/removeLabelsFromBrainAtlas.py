# This code removes unnecessary structures from the OA brain atlas.
# Run script by typing "/Applications/Slicer.app/Contents/MacOS/Slicer --no-splash --no-main-window --python-script "removeLabelsFromBrainAtlas.py"" in terminal.
import slicer
import json

# Import segmentation from a nrrd + color table file
colorNode = slicer.util.loadColorTable('/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/hncma-atlas-lut.ctbl')
segmentation = slicer.util.loadSegmentation("/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/hncma-atlas.nrrd", {'colorNodeID': colorNode.GetID()})

# Import Atlas Structure JSON
atlasStructureJSON = json.load(open('atlasStructure.json'))

# Function to get structure IDs of groups
def getStructureIdOfGroups(groupsToRemove, atlasStructureJSON):
    structureIds = []
    for group in groupsToRemove:
        for item in atlasStructureJSON:
            if item['@id'] == group:
                if item['@type'] == "Structure":
                    structureIds.append(item['annotation']['name'])
                if item['@type'] == "Group":
                    groupsToRemove.extend(item['member'])

    return structureIds
    

# Get structure IDs of groups to remove from atlas
#Skin, #Head_and_Neck_Muscles, #right_optic_tract, #left_optic_tract, #right_optic_nerve, #left_optic_nerve, #hypothalamus
segmentIdsToRemove = getStructureIdOfGroups(["#Skin", "#Head_and_Neck_Muscles", "#right_optic_tract", "#left_optic_tract", "#right_optic_nerve", "#left_optic_nerve", "#hypothalamus"], atlasStructureJSON)



# Iterate through segment IDs to remove and remove them
for segmentIdtoRemove in segmentIdsToRemove:
  segmentation.RemoveSegment(segmentIdtoRemove)

# Save cleaned segmentation/labelmap
slicer.util.saveNode(segmentation, "/Users/andy/Documents/PythonScripts/removeLabelsFromBrainAtlas/hncma-atlas-cleaned.nrrd")


exit()