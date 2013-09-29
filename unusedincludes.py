def getIncludes(lines):
	ifdefStack = 0
	includes = []
	for line in lines:
		if '#if' in line:
			ifdefStack = ifdefStack + 1
		elif '#endif' in line:
			ifdefStack = ifdefStack - 1
		if '#include' in line and ifdefStack == 0:
			includes.append(line)
	return includes

def getClassName(include):
	return include.split('/')[-1].split('.')[0].replace('<','').replace('>','').replace('"', '').split(' ')[-1]

def unusedIncludes(path):
	unused = []
	f = open(path).read()
	lines = f.split('\n')
	includes = getIncludes(lines)
	lines = [a for a in lines if a not in includes]
	for include in includes:
		name = getClassName(include)
		if len([a for a in lines if name in a]) == 0:
			unused.append(include)
	return unused

def findFiles(base):
	import os
	files = []
	for root, dirnames, filenames in os.walk(base):
		for f in filenames:
			files.append(os.path.join(root, f))
	return files

def appSpecificFilter(includeName):
	import re
	excludeFilters = [r'ui_']
	for pattern in excludeFilters:
		if len(re.findall(pattern, includeName)) > 0:
			return False
	return True

def removeIncludes(filename, unused):
	import envoy
	import codecs
	import shutil
	if len(unused) > 0:
		oldlines = codecs.open(filename, 'r', 'utf-8').read().split('\n')
		shutil.copyfile(filename, 'test.tmp')
		newfile = codecs.open(filename, 'w', 'utf-8')
		newlines = [a+'\n' for a in oldlines if a not in unused]
		if newlines[-1] == '\n':
			newlines = newlines[:-1]
		newfile.writelines(newlines)
		newfile.close()
		ret = envoy.run('make')
		if ret.status_code == 0:
			print 'got rid of some includes! ' + filename
		else:
			print 'failed, backing it out! ' + filename
			print 'tried includes: ' + ', '.join(unused)
			print 'error: ' + ret.std_err
			shutil.copyfile('test.tmp', filename)
			return False
	else:
		print 'no changes needed! ' + filename
	return True

def removeSubsets(filename, l):
	import itertools
	for numtoremove in range(len(l), 0, -1):
		for test in itertools.combinations(l, numtoremove):
			print 'testing: ', filename, test
			if removeIncludes(filename, test):
				return

def testRemovingIncludes(filename):
	unused = unusedIncludes(filename)
	unused = filter(appSpecificFilter, unused)
	removeSubsets(filename, unused)			


def removeUnusedIncludesRecursive(dirName):
	files = findFiles(dirName)
	files = [a for a in files if '.svn' not in a and '.cpp' in a]
	for f in files:
		testRemovingIncludes(f)
