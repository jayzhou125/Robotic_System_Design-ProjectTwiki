# BATCH FILE FORMAT
The batch file shall consist of comma or line separated list of movement instructions, each of which conforms to one of the following formats
## Linear Motion
### Format
```
[up/down] [meters]
```
### Examples
```
up 5
down 3.14
```


## In-Place Rotation
### Format
```
[left/right] [degrees]
```

### Examples
```
right 54.3
left 90
```

## Arc Movement
### Format
```
[up/down] [left/right] [position code]
```

where `position code` is:
```
[meters] r [degrees]
```

### Examples
```
up left 3.1415 r 1
down right 5 r 7
```

## Speed
### Format

all commands have the option to specify a custom speed by appending the following to the end of the command
```
s [speed]
```
where speed is a value between 0 and 1


### Examples
```
right 4 s 0.3
up left 3.14 r 2 s 0.5
```