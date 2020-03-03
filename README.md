# ODROID N2 Monitor/Control

More info on the N2: https://wiki.odroid.com/odroid-n2/odroid-n2

## General GPIO

Currently I have implemented only digital GPIO on a single pin. See `odroid_n2_gpio.py` for more details.

## Weather Board

I have adapted the libraries provided by HardKernel (https://github.com/hardkernel/WEATHER-BOARD) to work as Prometheus exporters (more on that in the Prometheus section). The two core libraries are copied to this repo for convenience; this will hopefully be rectified eventually.

See `weather_exporter.py` for more details.

## Prometheus

Everything that can be read from the N2 is currently implemented as a Prometheus exporter.

There are three files: `export_cpu_temp.py`, `export_gpio.py`, and `weather_exporter.py`

### Thermal Zone Exporter

The `node_exporter` from Prometheus doesn't work for N2's temperature. So, I've written my own. It is very simple: it simply reads the two "thermal zone" files and converts their contents into floats.

See https://forum.odroid.com/viewtopic.php?t=31295#p226432 for more on how I figured this out.

See `export_cpu_temp.py` for implementation.

### Weather Exporter

Most of the weather data that can be derived from the Weather Board is being exported by `weather_exporter.py`

### Lights State Exporter

Very simple exporter that tracks the commanded state of the plant room lights. See `export_gpio.py` for implementation.

Also see "Control Lights" section for more details.

## Control Lights

The N2 is currently being used to control the plant room lights. This is done via a mechanical relay (electromagnetically-controlled circuit rated for mainline voltage).

See `control_lights.py` for more details.

The mechanical relay can be found here: https://www.amazon.com/gp/product/B07P73PHQY


## Grafana

All exporters are being tracked by Grafana, via three dashboards:

TODO

## System Administration

### Systemd

Everything runs via Systemd:

```sh
thomas@odroid:/etc/prometheus/exporters$ for path in /etc/systemd/system/{nodeexporter,plant_lights*,prometheus,prom_export_*}.service; do echo "$path:" && cat "$path" && echo -e "---\n"; done
/etc/systemd/system/nodeexporter.service:
[Unit]
Description=NodeExporter

[Service]
TimeoutStartSec=0
ExecStart=/usr/local/bin/node_exporter --collector.systemd

[Install]
WantedBy=multi-user.target
---

/etc/systemd/system/plant_lights_off.service:
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root
Type=simple
ExecStart=/home/thomas/off

[Install]
WantedBy=multi-user.target

---

/etc/systemd/system/plant_lights_on.service:
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root
Type=simple
ExecStart=/home/thomas/on

[Install]
WantedBy=multi-user.target

---

/etc/systemd/system/prometheus.service:
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yaml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target

---

/etc/systemd/system/prom_export_thermal.service:
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root
Type=simple
ExecStart=/usr/bin/python3.8 /etc/prometheus/exporters/export_cpu_temp.py

[Install]
WantedBy=multi-user.target

---

/etc/systemd/system/prom_export_weather.service:
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root
Type=simple
ExecStart=/usr/bin/python3.8 /etc/prometheus/exporters/weather_exporter.py

[Install]
WantedBy=multi-user.target

---
```

### Prometheus Configuration

Very simple:

```yaml
# /etc/prometheus/prometheus.yaml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'odroid'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'thermal_zone'
    static_configs:
      - targets: ['localhost:9190']
  - job_name: 'weather'
    static_configs:
      - targets: ['localhost:9191']
  - job_name: 'lights_status'
    static_configs:
      - targets: ['localhost:9192']
```


### Grafana Configuration

TODO
