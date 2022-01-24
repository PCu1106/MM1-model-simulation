# MM1-model-simulation
MM1 model is a single-sever model, it has following features...
1. Arriving time is exponentially distributed
2. Service time is exponentially distributed
3. First come first serve
4. Length of the queue is infinite
5. Population is infinite
## Development Environment
VScode

Python

Win10
## Exponential Ramdom Variable
U= Uniform(0,1)

ExpRV= -log(U)/λ
## Simulation Result
Purple part is 95% confident interval

<img src=./sim_10.png width=80% />
<img src=./sim_50.png width=80% />
<img src=./sim_250.png width=80% />

We can see...
1. Confident interval decrease when simulation turns increase
2. When λ> 1/ave_service_time, the average_waiting_time start to increase
   (Because 1/λ= average_arrive_time)
