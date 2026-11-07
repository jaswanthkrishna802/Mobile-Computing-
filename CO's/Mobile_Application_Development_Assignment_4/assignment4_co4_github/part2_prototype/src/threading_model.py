"""Deterministic synthetic comparison of single-thread and worker-pool overhead.
The values are pedagogical model outputs, not CPU profiler measurements."""
def compare():
    return [
      {"workload":"large_parse","single_ms":180.0,"multi_ms":92.0,"single_threads":1,"multi_threads":4,"interpretation":"Parallel chunks outweigh coordination cost in this model."},
      {"workload":"tiny_task","single_ms":1.2,"multi_ms":3.8,"single_threads":1,"multi_threads":4,"interpretation":"Scheduling and synchronisation overhead dominate."},
      {"workload":"contended_counter","single_ms":42.0,"multi_ms":67.0,"single_threads":1,"multi_threads":4,"interpretation":"Lock contention serialises the critical section."},
    ]
if __name__=="__main__":
    for x in compare(): print(x)
