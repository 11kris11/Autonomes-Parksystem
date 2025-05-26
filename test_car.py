from unittest.mock import MagicMock

from car import Car  # Pfad zu deiner Car-Klasse anpassen

def test_move_forward_velocity_and_move_called():
    car = Car(0, 0, "black", "white")
    car.vel = 10
    car.acceleration = 7
    car.max_vel = 15

    # move() mocken, damit wir prüfen können, ob es aufgerufen wurde
    car.move = MagicMock()

    car.move_forward()

    # vel soll nicht größer als max_vel sein
    assert car.vel == 15  # 10 + 7 = 17, aber max 15

    # move() wurde genau 1x aufgerufen
    car.move.assert_called_once()

def test_move_forward_vel_below_max():
    car = Car(0, 0 ,"black", "white")
    car.vel = 5
    car.acceleration = 3
    car.max_vel = 20

    car.move = MagicMock()
    car.move_forward()

    # vel soll 8 sein (5 + 3)
    assert car.vel == 8
    car.move.assert_called_once()
