### VRay Proxy Maker
### v001
### John Rouse          

from maya import cmds
from maya import mel


import maya.cmds as cmds

# Make a new window
def createVRayProxyMakerUI():

	winName = 'VRayProxyMaker'
	winWidth = 450
	winHeight = 450

	if cmds.window(winName, exists=True):
		cmds.deleteUI(winName, window=True)
		cmds.windowPref( winName, remove=True )

	window = cmds.window(winName, title="VRay Group Proxy Tool",  widthHeight=[winWidth, winHeight], iconName='JR',titleBar=True, minimizeButton=False,maximizeButton=False, s=False )
	columnMain = cmds.columnLayout() 
	headerCentered = cmds.columnLayout()

	#cmds.image(image='c:\\images\\vrayProxyMakerTitle450.jpg')

	cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 70), (2, 350)] )
	cmds.text( label='Group Name' )
	groupName = cmds.textField('groupNameInput')
	cmds.text( label='Face Count' )
	faceCount = cmds.intField('faceCountInput', value=100000)
	cmds.text( label='FolderPath' )
	folderPath = cmds.textField('filepathInput', text="""C:\\temp\\proxy""")


	#    Attach commands to pass focus to the next field if the Enter
	#    key is pressed. Hitting just the Return key will keep focus
	#    in the current field.
	#
	cmds.textField( groupName, edit=True, enterCommand=('cmds.setFocus(\"' + faceCount + '\")') )
	cmds.intField( faceCount, edit=True, enterCommand=('cmds.setFocus(\"' + groupName + '\")') )

	cmds.text(label='')

	def set_textfield(_):
		sel = cmds.ls(selection=True)
		cmds.textField(groupName, edit=True, text=sel[0])

	cmds.text( label='' )
	cmds.text( label='' )
	load_button = cmds.button( label='Select Group to Proxy', c = set_textfield)
	cmds.text(label='')
	cmds.text(label='')
	cmds.text(label='')
	load_button = cmds.button( label='MAKE PROXY BUTTON', c = 'makeProxyRun()')



	cmds.text(label='')
	footer = cmds.rowColumnLayout(numberOfColumns=1, rowSpacing=[1,0], columnSpacing=[1,0], p=columnMain)
	cmds.button(label='Close', command='cmds.deleteUI("'+ winName +'", window=True)',w=winWidth, h=60, p=footer)
	cmds.text(label='')



	cmds.showWindow()



	


createVRayProxyMakerUI()

def makeProxyRun():
	groupNameValue = cmds.textField('groupNameInput', q = True, text = True)
	faceCountValue = cmds.intField('faceCountInput', q = True, value = True)
	filepathValue = cmds.textField('filepathInput', q = True, text = True)

	if not groupNameValue:
		print('Select a Group!')


	else:
		print(groupNameValue)
		print(faceCountValue)
		print(filepathValue)
		childrenToProxy(groupNameValue, faceCountValue, filepathValue)


def childrenToProxy(parentName, inputPreviewFaces, userFilepath):
	
	timestampStr = cmds.date( format='Created_YYYY-MM-DD__hh-mm-ss' )
	timestampGrpName = timestampStr
	#cmds.group(em=True, n=timestampGrp)



	#ref Folder
	ref_folder = "C:\\temp\\proxy"

	#filename for everything?
	proxy_filename = parentName + '_proxy.vrmesh'
	proxy_nodename = parentName + '_proxy'
	sub_groupname = parentName + '_sub'

	#Display Values
	#print(proxy_filename)
	#print(inputPreviewFaces)

	#GO TIME
	if cmds.objExists(parentName):
		cmds.group(n='tmpGRP', p=parentName, em=True)
		cmds.group(n=timestampGrpName, p=parentName, em=True)
		cmds.select(parentName)
		cmds.select(hi=True) #this selects everything without heirarchy needs a different method
		cmds.select([parentName, 'tmpGRP'], d=True)


		#print('Children nodes selected: ' + parentName)
		print('''
			----------------------------------------------------------------------------------------
			----------------------------------------------------------------------------------------

			WARNING! VRAY Processing Started - Don't Do Anything! Dont Mess with the scene! WARNING!
			
			----------------------------------------------------------------------------------------
			----------------------------------------------------------------------------------------
			''')

		cmds.vrayCreateProxy(dir=userFilepath, fname=proxy_filename, overwrite=True, facesPerVoxel=10000, previewFaces=inputPreviewFaces, exportType=1, previewType="combined", createProxyNode=True, node=proxy_nodename)
		print('Finished VRay Function for Creating Proxy. Moving on to organization.')
		cmds.select(proxy_nodename)
		print('Selected')
		cmds.xform(proxy_nodename, p=True, cp=True)
		print('Pivot Centered')
		cmds.delete('tmpGRP')
		print('Deleted the tmpGRP')
		cmds.parent( proxy_nodename, parentName)
		print(proxy_nodename + ' Parented to: ' + parentName)
		print('Done! Move along. Move along.')
				
	else:

		print('Group does not exist: ' + parentName)

