import "influxdata/influxdb/tasks"

option task = {name: "downsample", every: 1m, offset: 5s}

from(bucket: "generators")
|> range(start: tasks.lastSuccess(orTime: -1h))
|> aggregateWindow(every: 1m, fn: last, createEmpty: false)
|> set(key: "location", value: "USA")
|> to(bucket: "downsampled")