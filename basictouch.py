from mistyPy.Robot import Robot #libraries
from mistyPy.Events import Events

MISTY_IP = "10.1.14.125"
misty = Robot(MISTY_IP)

def bumped(data):   #functions
    print(data)
    misty.display_image("e_Love.jpg", 1)
    misty.move_head(0, -10, 0, 50)
    misty.move_arms(90, -70, 50, 50)
    misty.change_led(255, 0, 0)

def touched(data):
    print(data)
    misty.display_image("e_Joy.jpg", 1)
    misty.move_head(0, 0, 0, 50)
    misty.move_arms(-40, 90, 50, 50)
    misty.change_led(0, 255, 0)

#events definitions
misty.register_event(event_name='bumped', event_type=Events.BumpSensor, callback_function=bumped, keep_alive=True)
misty.register_event(event_name='touch', event_type=Events.TouchSensor, callback_function=touched, keep_alive=True)

#"run until stopped" of blockly
misty.keep_alive()
