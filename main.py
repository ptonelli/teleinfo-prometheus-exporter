from prometheus_client import Gauge, CollectorRegistry, generate_latest
import teleinfo

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


prefix = "electricity_meter_teleinfo"
app = FastAPI()
items = {}

def get_metric_name(edf_label, unit,):
#    return '_'.join([prefix] + edf_label.lower().replace(',','').split(' ') + [unit])
    return '_'.join(edf_label.lower().replace(',','').split(' ') + [unit])

@app.on_event("startup")
def start_teleinfo():
    items["prometheus_registry"] = CollectorRegistry()
    items["gauge_list"] = {} #used to store gauges as the registry does not contain everything

@app.get("/metrics",response_class=PlainTextResponse)
def get_metrics():
    values = teleinfo.get_metrics()
    registry = items["prometheus_registry"]
    gauge_list = items["gauge_list"]
    # we replace initial labels with the ones matching the registry labels
    for edf_key in list(values.keys()):
        value = values.pop(edf_key)
        values[get_metric_name(value[-1], value[-2])] = value

    # we update the existing gauges
    for gauge in registry.collect():
        if gauge.name in values:
            value = values.pop(gauge.name)
            gauge = gauge_list[gauge.name]
            gauge.set(value[0])
        else: #we must remove this gauge
            registry.unregister(registry._names_to_collectors[gauge.name])
            gauge_list.pop(gauge.name)
    # we then add gauges for the missing values
    for edf_key in values:
        value = values[edf_key]
        gauge = Gauge(edf_key,"",registry=registry)
        gauge_list[edf_key] = gauge
        gauge.set(value[0])
    return generate_latest(registry)
