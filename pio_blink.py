import machine
import utime
import rp2

# Blink LED at 10Hz with freq = 2000Hz
# 2000Hz / 200 cycles = 10Hz
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1) [19] 	#1 cycle instruction + 19 cycles delay
    nop() [19]			#20 cycles delay
    nop() [19]			#20 cycles delay
    nop() [19]			#20 cycles delay
    nop() [19]    		#20 cycles delay
    set(pins, 0) [19]	#1 cycle instruction + 19 cycles delay
    nop() [19]			#20 cycles delay
    nop() [19]			#20 cycles delay
    nop() [19]			#20 cycles delay
    nop() [19]    		#20 cycles delay
    wrap()

# freq = 2000Hz, control pin#25
sm = rp2.StateMachine(0, blink, freq=2000, set_base=machine.Pin(25))

print("Start state machine...")
sm.active(1)

# CPU is not used for blinking LED
while True:
    print('Idle....')
    utime.sleep(1)    