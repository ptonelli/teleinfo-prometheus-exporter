from prometheus_client import Gauge, CollectorRegistry, generate_latest
import teleinfo

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

prefix = "electricity_meter_teleinfo"
app = FastAPI()

def get_metric_name(edf_label, unit):
    return '_'.join([prefix, edf_label.lower(), unit])

@app.on_event("startup")
async def start_teleinfo():
    items["teleinfo_serial_port"] = teleinfo.initialize()
    items["prometheus_registry"] = CollectorRegistry()

@app.get("/metrics",response_class=PlainTextResponse)
async def get_metrics():
    registry = items["prometheus_registry"]
    values = get_metrics(items["teleinfo_serial_port"])    
    # we replace initial labels with the ones matching the registry labels
    for edf_key in values.keys():
        value = values.pop(edf_key)
        values[get_metric_name(edf_key, value[-1])] = value

    # we update the existing gauges
    for gauge in registry.collect():
        if gauge.name in values:
            value = values.pop(gauge.name)
            gauge.set(value[0])
        else: #we must remove this gauge
            registry.unregister(registry._names_to_collectors[gauge.name])
    # we then add gauges for the missing values
    for edf_key in values:
        value = values[edf_key]
        Gauge(get_metric_name(edf_key, value[-1]),"",registry=registry)
    return generate_latest(registry)
