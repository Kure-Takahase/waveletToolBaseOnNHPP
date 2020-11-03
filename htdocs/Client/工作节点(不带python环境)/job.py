class Job:
    def __init__(self, taskName, taskNum, taskSum, dataTuple, paraTuple, taskFunction, saveFunction, libFiles):
        self.taskName 		= taskName
        self.taskNum 		= taskNum
        self.taskSum 		= taskSum
        self.dataTuple 		= dataTuple
        self.paraTuple 		= paraTuple
        self.taskFunction 	= taskFunction
        self.saveFunction 	= saveFunction
        self.startTime 		= 0
        self.calculateTime 	= 0
        self.message 		= False
        self.libFiles		= libFiles

    def getTaskName(self):
    	return self.taskName

    def getTaskNum(self):
    	return self.taskNum

    def getTaskSum(self):
    	return self.taskSum

    def getDataTuple(self):
    	return self.dataTuple

    def getParaTuple(self):
    	return self.paraTuple

    def setStartTime(self,startTime):
    	self.startTime = startTime

    def getStartTime(self):
    	return self.startTime

    def setCalculateTime(self,calculateTime):
    	self.calculateTime = calculateTime

    def getCalculateTime(self):
    	return self.calculateTime

    def setMessage(self,message):
    	self.message = message

    def getMessage(self):
    	return self.message

    def getLibFiles(self):
    	return self.libFiles

	