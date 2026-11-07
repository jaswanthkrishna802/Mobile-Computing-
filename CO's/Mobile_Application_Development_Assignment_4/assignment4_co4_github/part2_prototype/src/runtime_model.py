"""Illustrative runtime workload model; not ART benchmark or measured Android logs."""
def runtime_cases():
    return [
      {"case":"cold_start","compile_mode":"verify","startup_ms":780,"steady_ops_per_s":1000,"heap_mb":46,"gc_pause_ms":18},
      {"case":"warm_start","compile_mode":"verify","startup_ms":260,"steady_ops_per_s":1000,"heap_mb":47,"gc_pause_ms":8},
      {"case":"profile_guided","compile_mode":"speed-profile","startup_ms":420,"steady_ops_per_s":1850,"heap_mb":49,"gc_pause_ms":9},
      {"case":"full_aot","compile_mode":"speed","startup_ms":510,"steady_ops_per_s":2100,"heap_mb":52,"gc_pause_ms":9},
    ]
if __name__=="__main__":
    for r in runtime_cases(): print(r)
