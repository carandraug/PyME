import time

def doNix(taskQueue): #do nothing
	pass

def popZero(workerN, NWorkers, NTasks): #give worker oldest task irrespective of which worker called
	return 0

class TaskQueue:
	def __init__(self, name, initialTasks=[], onEmpty = doNix, fTaskToPop = popZero):
		#Pyro.core.ObjBase.__init__(self)
		#self.name = name
		self.queueID = name
		self.openTasks = list(initialTasks)
		self.closedTasks = []
		self.tasksInProgress = []
		self.onEmpty = onEmpty #function to call when queue is empty
		self.fTaskToPop = fTaskToPop #function to call to decide which task to give a worker (useful if the workers need to have share information with, e.g., previous tasks as this can improve eficiency of per worker buffering of said info).
                
	def postTask(self,task):
		self.openTasks.append(task)
		#print '[%s] - Recieved new task' % self.queueID

	def postTasks(self,tasks):
		self.openTasks += tasks
		#print '[%s] - Recieved %d new tasks' % (self.queueID, len(tasks))

	def getTask(self, workerN = 0, NWorkers = 1):
		"""get task from front of list, blocks"""
		#print 'Task requested'
		while len(self.openTasks) < 1:
			time.sleep(0.01)

		task = self.openTasks.pop(self.fTaskToPop(workerN, NWorkers, len(self.openTasks)))

		task.queueID = self.queueID
		task.initializeWorkerTimeout(time.clock())
		self.tasksInProgress.append(task)
		#print '[%s] - Task given to worker' % self.queueID
		return task

	def returnCompletedTask(self, taskResult):
		for it in self.tasksInProgress:
			if (it.taskID == taskResult.taskID):
				self.tasksInProgress.remove(it)
		self.fileResult(taskResult)

		if (len(self.openTasks) + len(self.tasksInProgress)) == 0: #no more tasks
			self.onEmpty(self)

	def fileResult(taskResult):
		self.closedTasks.append(taskResult)

	def getCompletedTask(self):
		if len(self.closedTasks) < 1:
			return None
		else:
			return self.closedTasks.pop(0)

	def checkTimeouts(self):
		curTime = time.clock()
		for it in self.tasksInProgress:
			if 'workerTimeout' in dir(it):
				if curTime > workerTimeout:
					self.openTasks.insert(0, it)
					self.tasksInProgress.remove(it)

	def getNumberOpenTasks(self):
		return len(self.openTasks)

	def getNumberTasksInProgress(self):
		return len(self.tasksInProgress)

	def getNumberTasksCompleted(self):
		return len(self.closedTasks)

	def purge(self):
		self.openTasks = []
		self.closedTasks = []
		self.tasksInProgress = []

	def setPopFcn(self, fcn):
		''' sets the function which determines which task to give a worker'''
		self.fTaskToPop = fcn
