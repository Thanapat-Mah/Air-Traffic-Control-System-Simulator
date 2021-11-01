import pygame


class CollisionDetector:

    def __init__(self):
        self.__separated_distance = {}
        self.__collision_set = {}
        self.__collision_couple_list = []

    def mock_get_separated_distance(self):
        return ({"horizontal": 9.26,
                "vertical": 1000
        })

    def mock_get_collision_set(self):
        return ({"TG001", "FD002", "FD003"})


    def mock_get_collision_couple_list(self):
        return ([("TG001", "FD002"), ("FD002", "FD003")])

    def mock_check_collision(self):
        return
