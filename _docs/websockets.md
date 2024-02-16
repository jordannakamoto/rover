When two WebSocket-connected servers are on the same device, there is typically minimal to no network latency introduced by the network itself. WebSocket communication between two processes on the same device is often referred to as "loopback" or "interprocess communication" (IPC). In this scenario, data travels directly between the two processes within the same device's memory space, without the need to traverse a physical network or a router.

Here's how the communication flow typically works:

One WebSocket server listens on a specific port on the device.
The other WebSocket server connects to that specific port on the same device.
Data is exchanged directly between the two processes using shared memory, without leaving the device or going through a router.
As a result, the latency introduced in such a setup is primarily related to the processing time and the efficiency of the WebSocket implementation in your server applications, rather than network latency.