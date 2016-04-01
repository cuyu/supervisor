# supervisor
codes about server to monitor and control remote clients. (ref to syscon-0.4)

The flowchart is as follows:

```
  +--------+ send request(HTTP) +------------+ send cmds(TCP) +--------+
  |  Web   |------------------->| Supervisor |--------------->| Client |
  |        |<-------------------|   server   |<---------------| server |
  +--------+   send data(HTTP)  +------------+ send data(UDP) +--------+
```
