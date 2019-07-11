def satisfyPer(tids, maxPer, numTrans):
	tids = list(tids)
	tids.sort()
	if tids[0] > maxPer:
		return 0
	tids.append(numTrans)
	for i in range(1,len(tids)):
		if (tids[i]-tids[i-1]) > maxPer:
			return 0
	return 1
class PFPTree(object):
	def __init__(self):
		self.root = Node(None, 0, {})
		self.summaries = {}

	def __repr__(self):
		return repr(self.root)

	def add(self, basket, tid, count):
		curr = self.root
		curr.count += count
		for i in tid:
			curr.tids.add(i)

		for i in range(0,len(basket)):
			item = basket[i]
			if item in self.summaries.keys():
				summary = self.summaries.get(item)
			else:
				summary = Summary(0,set())
				self.summaries[item] = summary
			summary.count += count

			if item in curr.children.keys():
				child = curr.children.get(item)
			else:
				child = Node(item, 0, {})
				curr.addChild(child)
			summary.nodes.add(child)
			child.count += count
			for j in tid:
				summary.tids.add(j)
				if (i==len(basket)-1):
					child.tids.add(j)
			curr = child
		return self

	def getTransactions(self):
		return [x for x in self.root._getTransactions()]

	def merge(self,tree):
		for t in tree.getTransactions():
			self.add(t[0], t[1], t[2])
		return self

	def project(self,itemId):
		newTree = PFPTree()
		summaryItem = self.summaries.get(itemId)
		if summaryItem:
			for element in summaryItem.nodes:
				t = []
				curr = element.parent
				while curr.parent:
					t.insert(0,curr.item)
					curr = curr.parent
				newTree.add(t, element.tids, element.count)
		return newTree


	def extract(self, minCount, maxPer, numTrans, isResponsible = lambda x:True):
		for item in sorted(self.summaries, reverse = True):
			summary = self.summaries[item]
			if (isResponsible(item)):
				if(summary.count >= minCount and satisfyPer(summary.tids, maxPer, numTrans)):
					yield ([item],summary.count)
					for element in self.project(item).extract(minCount, maxPer, numTrans):
						yield ([item]+element[0],element[1])
			for element in summary.nodes:
				parent = element.parent
				parent.tids |= element.tids
		

class Node(object):

    def __init__(self, item, count, children):
        self.item = item
        self.count = count
        self.children = children #dictionary of children
        self.parent = None
        self.tids = set()

    def __repr__(self):
        return self.toString(0)

    def toString(self, level=0):
        if self.item == None:
            s = "Root("
        else:
            s = "(item="+str(self.item)
            s+= ", count="+str(self.count)
            for i in self.tids:
            	s += " " + str(i)
        tabs = "\t".join(['' for i in range(0,level+2)])
        for v in self.children.values():
            s+= tabs+"\n"
            s+= tabs+v.toString(level=level+1)
        s+=")"
        return s

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self

    def _getTransactions(self):
        count = self.count
        tids = self.tids
        for child in self.children.values():
            for t in child._getTransactions():
                count-=t[2]
                t[0].insert(0,child.item)
                yield t
        if (count>0):
            yield ([],tids,count)



class Summary(object):

        def __init__(self, count, nodes):
            self.count = count
            self.nodes = nodes
            self.tids = set()
