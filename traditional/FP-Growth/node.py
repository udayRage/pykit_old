class Node:
    """
    A class used to represent the node of fptree

        ...

        Attributes
        ----------
        itemid : int
            storing item of a node
        count : int
            To maintain the support of node
        Parent : node
            To maintain the parent of every node
        child : list
            To maintain the children of node
        nodeLink : node
            Points to the node with same itemid

        Methods
        -------

        getChild(itemName)
            returns the node with same itemName from fptree
    """
    def __init__(self):
        self.itemid=-1
        self.counter=1
        self.parent=None
        self.child=[]
        self.nodeLink=None
    
    def getChild(self,id1):
        for i in self.child:
            if(i.itemid==id1):
                return i
        return None
