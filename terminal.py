
LOG_SOURCE_WIDTH = 7

def log(source, message):
    if len(source) >= LOG_SOURCE_WIDTH:
        print(f'[{source}] {message}')
        return

    padding = LOG_SOURCE_WIDTH - len(source)
    #left_padding = padding // 2
    #right_padding = padding - left_padding
    left_padding = 0
    right_padding = padding

    print(f'[{" "*left_padding}{source}{" "*right_padding}] {message}')

def logger(source):
    return lambda message: log(source, message)

# Just change "logger('whatever')" to "nologger('whatever')" to disable logging
def nologger(source):
    return lambda message: None

