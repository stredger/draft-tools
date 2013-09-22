


def quicksort(plist, sortattr):
	# sort in decending order using quicksort
	_quicksort(plist, sortattr, 0, len(plist) - 1)

def _swap(plist, pos, swapspot):
	tmp = plist[pos]
	plist[pos] = plist[swapspot]
	plist[swapspot] = tmp

def _quicksort(plist, sortattr, start, end):
	if end - start < 2: return
	mid = (end + start) / 2 # == ((end - start) / 2) + start
	pivotval = plist[mid].__dict__[sortattr]
	_swap(plist, mid, end) # swap pivot to the end
	i = swappos = start
	while i < end:
		# swap if we are larger than the pivot for descending sort
		if pivotval < plist[i].__dict__[sortattr]:
			_swap(plist, i, swappos)
			swappos += 1
		i += 1
	# put the pivot in its final place	
	_swap(plist, end, swappos) 
	
	_quicksort(plist, sortattr, start, swappos)
	_quicksort(plist, sortattr, swappos+1, end)



