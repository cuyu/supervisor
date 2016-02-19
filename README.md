# supervisor
A remote monitor and control client and server codes. (ref to syscon-0.4)

The design is as follows:

  +--------+ send request(HTTP) +------------+ send cmds(TCP) +--------+
  |  Web   |------------------->| Supervisor |--------------->| Client |
  |        |<-------------------|   server   |<---------------| server |
  +--------+   send data(HTTP)  +------------+ send data(UDP) +--------+



TODO:
1. add logging