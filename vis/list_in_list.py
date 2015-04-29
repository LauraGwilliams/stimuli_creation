def list_in_list(list1,list2,index=False,dataset_to_index=None):
    """
    
    Finds which items of one list are in which items of the other list.
    
    List1             :       can be a list or the column of a dataset
    List2             :       can be a list or the column of a dataset
    Index             :       Set to true if you want to index your ds by removing entries that occur in the other list.
    dataset_to_index  :       If Index is true, need to say what your dataset is that you want to index.
    
    """
    
    items = []
    booln = []
    
    for i in range(0,len(list1)):
        item = list1[i]
        if not any([word in item for word in list2]):
            booln.append(True)
          
        else:
            booln.append(False)
            items.append(item)
    
        if index == False:
            return items
        
        if index == True:
            idx = np.array(booln, dtype=bool)        
            ds_sub = dataset_to_index.sub(idx)
            return ds_sub