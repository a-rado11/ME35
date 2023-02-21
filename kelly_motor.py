

import RPistepper as stp
M1_pins = [18, 17, 27, 22]
M2_pins = [5, 6, 26, 16]

M1 = stp.Motor(M1_pins)
M2 = stp.Motor(M2_pins)
i = 0
steps = 25
while i < steps:
    M2.move(-1)
    M1.move(1)
    i = i + 1
M1.release()
M1.cleanup()
M2.release()
M2.cleanup