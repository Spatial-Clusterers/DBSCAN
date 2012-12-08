import pstats

stats = pstats.Stats("dbscan-9375.profile")
stats.sort_stats('file').print_stats()