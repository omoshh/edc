import fastapi
from backend import utils

app = fastapi.FastAPI()

@app.get("/app")
def read_root():
    cp_av = utils.get_cpu()
    mem = utils.get_mem()
    load_av = utils.get_average()
    network = utils.get_bandwidth()
    datetime = utils.get_now()

    return {
        "datetime": datetime,
        "cpu_usage": cp_av,
        "memory_usage": mem,
        "load_average": load_av,
        "network_bandwidth": network,
    }