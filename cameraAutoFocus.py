'''
DISCLAIMER:
---------------------------------
In any case, all binaries, configuration code, templates and snippets of this solution are of "work in progress" character.
This also applies to GitHub "Release" versions.
Neither Simon Nagel, nor Autodesk represents that these samples are reliable, accurate, complete, or otherwise valid. 
Accordingly, those configuration samples are provided “as is” with no warranty of any kind and you use the applications at your own risk.

Scripted by Simon Nagel, supported by Rutvik Bhatt
'''
  
'''
Activate GPU Raytracing.
Focus will be automatically set to the object in the center of the Screen.
Glass Materials will be ignored

''' 
#set here the transparency Threshold for non-glass-materials to ignore them.          
transThreshold = 0.5
                                 
                                                                                         

import math
timerCameraAutoFocus = vrTimer()
timerCameraAutoFocus.setActive(0)
def cameraDistance():
    global transThreshold
    cam = getActiveCameraNode()
    tape1Pos = cam.getTranslation()
    v = Vec3f(0,0,-1)
    tape1Mat = cam.getWorldTransform()
    rayOrigin = Pnt3f(tape1Pos[0],tape1Pos[1],tape1Pos[2])
    rayDirection = Vec3f(tape1Mat[0] * v.x() + tape1Mat[1] * v.y() + tape1Mat[2] * v.z() , tape1Mat[4] * v.x() + tape1Mat[5] * v.y() + tape1Mat[6] * v.z() ,tape1Mat[8] * v.x() + tape1Mat[9] * v.y() + tape1Mat[10] * v.z())
    intersection = getSceneIntersection(-1, rayOrigin, rayDirection)
    #print intersection
    interPos = intersection[1]
    interObj = intersection[0]
    if interObj.isValid(): 
        mat = interObj.getMaterial()
        matType = interObj.getMaterial().getType()
        
        hasSeeThrough = mat.fields().hasField("seeThrough")
    
        #print(matType)
        #check if glass material is used
        
        if matType == "SwitchMaterial":
            """
            choice = mat.getChoice()
            choicematname = mat.getMaterialByChoice(choice).getType()
            #print(choicematname)
            
            if choicematname == "UGlassMaterial":
                #print("Switch: it is glass material")
                interObj.setActive(0)
                newIntersection = getSceneIntersection(-1, rayOrigin, rayDirection)
                interPos = newIntersection[1]
            """            
            while matType == "SwitchMaterial":
                choice = mat.getChoice()
                choicematname = mat.getMaterialByChoice(choice).getType()
                hasSeeThrough = mat.getMaterialByChoice(choice).fields().hasField("seeThrough")
                #print(choicematname)
    
                if choicematname == "UGlassMaterial":
                    #print("Switch: it is glass material")
                    interObj.setActive(0)
                    newIntersection = getSceneIntersection(-1, rayOrigin, rayDirection)
                    interPos = newIntersection[1]
                
                elif hasSeeThrough == True: 
                    trans = mat.getMaterialByChoice(choice).fields().getVec("seeThrough",3)
                    
                    if trans[0]>transThreshold:
                        interObj.setActive(0)
                        newIntersection = getSceneIntersection(-1, rayOrigin, rayDirection)
                        interPos = newIntersection[1]
                        #print ("Switch:  tranparent")
                        
                
                matType = choicematname
                mat = mat.getMaterialByChoice(choice)
                
    
                                                      
        elif matType == "UGlassMaterial":
            #print "es ist glass"
            interObj.setActive(0)
            newIntersection = getSceneIntersection(-1, rayOrigin, rayDirection)
            interPos = newIntersection[1]
            
        elif hasSeeThrough == True: 
            trans = mat.fields().getVec("seeThrough",3)
            if trans[0]>0.5:
                interObj.setActive(0)
                newIntersection = getSceneIntersection(-1, rayOrigin, rayDirection)
                interPos = newIntersection[1]
                #print ("tranparent")
            else:
                interPos = intersection[1]
                        
        else:
            interPos = intersection[1]
            #print "es ist kein glass"
        x = (tape1Pos[0], tape1Pos[1], tape1Pos[2])
        y = (interPos.x(), interPos.y(), interPos.z())
            
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
        #print distance
        camera= vrCameraService.getActiveCamera()
        camera.setFocusDistance(distance)
        camera.setDepthOfField(1)
        camera.setFStop(2.0)
        interObj.setActive(1)
    

timerCameraAutoFocus.connect(cameraDistance)

timerCameraAutoFocus.setActive(true)
