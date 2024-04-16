def recur(vis, ans, tiles, se):
	se.setdefault(ans, 1) if ans else None
	[vis.__setitem__(i, True) or recur(vis, ans + tiles[i], tiles, se) or vis.__setitem__(i, False) for i in range(len(tiles)) if not vis[i]]

def count_substrings(tiles):
	se = dict()
	vis = [False] * (len(tiles))
	recur(vis, "", tiles, se)
	return len(se)

if __name__ == '__main__':
	example1 = "AAB"
	example2 = "AAABBC"
	example3 = "V"
	print(count_substrings(example1))
	print(count_substrings(example2))
	print(count_substrings(example3))