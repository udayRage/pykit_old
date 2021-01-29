import node as N
class Tree:
    """
        A class used to represent the fpgrowth tree structure

        ...

        Attributes
        ----------
        child : list
            storing each child of a tree as a subtree
        data : list
            stroing the each itemset as single value of the list

        Methods
        -------
        createHeaderList(items,minSup)
            takes items only which are greater than minSup and sort the items in ascending order
        addTransaction(transaction)
            creating transaction as a branch in fptree
        fixNodeLinks(item,newNode)
            To create the link for nodes with same item
        printTree(Node)
            gives the details of node in fpgrowth tree
        addPrefixPath(prefix,mapSupport,minSup)
           It takes the items in prefix pattern whose support is >=minSup and construct a subtree
    """
    def __init__(self):
        """
        Parameters
        ----------
        headerList : list
            storing the list of items in tree sorted in ascending of their supports
        mapItemNodes : dictionary
            stroing the nodes with same item name
        mapItemLastNodes : dictionary
            representing the map that indicates the last node for each item
        root : Node
            representing the root Node in a tree
        """
        self.headerList=[]
        self.mapItemNodes={}
        self.mapItemLastNodes={}
        self.root=N.Node()

    def addTransaction(self,transaction):
        """adding transaction into tree

        :param transaction: it represents the one transactions in database
        :type(transaction): list
        """

    	# This method taken a transaction as input and returns the tree
        current=self.root
        for i in transaction:
            child=current.getChild(i)
            if(child==None):
                newNode=N.Node()
                newNode.itemid=i
                newNode.parent=current
                current.child.append(newNode)
                self.fixNodeLinks(i,newNode)
                current=newNode
            else:
                child.counter+=1
                current=child
    def fixNodeLinks(self,item,newNode):
        """Fixing node link for the newNode that inserted into fptree

        :param item: it represents the item of newNode
        :type item : int
        :param newNode : it represents the newNode that inserted in fptree
        :type newNode : Node
        
        """
        if item in self.mapItemLastNodes.keys():
            lastNode=self.mapItemLastNodes[item]
            lastNode.nodeLink=newNode
        self.mapItemLastNodes[item]=newNode
        if item not in self.mapItemNodes.keys():
            self.mapItemNodes[item]=newNode
            
    def printTree(self,root):
        """Print the details of Node in fptree
        
        :param root: it represents the Node in fptree
        :type root: Node
        
        This method is to find the details of parent,children,support of Node
        """

    	# this method is used print the details of tree
        if root.child==[]:
            return
        else:
            for i in root.child: 
                print(i.itemid,i.counter,i.parent.itemid)
                self.printTree(i)
    def update(self,header,u1):
        """To update the headerList 

        :param mapsup: it represents the header list
        :type mapsup: list
        :param u1: the list of items
        :type u1 : list
        """

        t1=[]
        for i in header:
            if i in u1:
                t1.append(i)
        return t1
    def createHeaderList(self,mapSupport,min_sup):
        """To create the headerList 

        :param mapSupport : it represents the items with their supports
        :type mapsup : dictionary
        :param min_sup : it represents the minSup
        :param min_sup : float
        """
    	#the fptree always maintains the header table to start the mining from leaf nodes
        t1=[]
        for x,y in mapSupport.items():
            if y>=min_sup:
                t1.append(x)
        mapsup=[k for k,v in sorted(mapSupport.items(),key=lambda x: x[1],reverse=True)]
        self.headerList=[i for i in t1 if i in mapsup]
    def addPrefixPath(self,prefix,mapSupportBeta,min_sup):
        """To construct the conditional tree with prefix paths of a node in fptree 

        :param prefix : it represents the prefix items of a Node
        :type prefix : list
        :param mapSupportBeta : it represents the items with their supports
        :param mapSupportBeta : dictionary
        :param min_sup : to check the item meets with minSup
        :param min_sup : float
        """
    	#this method is used to add prefix paths in conditional trees of fptree
        pathCount=prefix[0].counter
        current=self.root
        prefix.reverse()
        for i  in range(0,len(prefix)-1):
            pathItem=prefix[i]
            #pathCount=mapSupportBeta.get(pathItem.itemid)
            if(mapSupportBeta.get(pathItem.itemid)>=min_sup):
                child=current.getChild(pathItem.itemid)
                if(child==None):
                    newNode=N.Node()
                    newNode.itemid=pathItem.itemid
                    newNode.parent=current
                    newNode.counter=pathCount
                    current.child.append(newNode)
                    current=newNode
                    self.fixNodeLinks(pathItem.itemid,newNode)
                else:
                    child.counter+=pathCount
                    current=child
