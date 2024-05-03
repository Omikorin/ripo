# RiPO

## Installation

```sh
t=ultralytics/ultralytics:latest
```

or for CPU version

```sh
t=ultralytics/ultralytics:latest-cpu
```

```sh
sudo docker pull $t
```

## Running

```sh
sudo docker run -it --ipc=host --gpus all $t
```

or for CPU version

```sh
sudo docker run -it --ipc=host $t
```

By using `-it` we are in the interactive mode, where we can communicate with YOLO.

