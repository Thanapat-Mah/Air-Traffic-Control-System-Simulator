import math
import copy

from numpy import PINF
from configuration import PLNAE_PHASE
### plane collision detector
class CollisionDetector:

    def __init__(self):
        self.__separated_distance = {"horizontal": 9.26,
                                        "vertical": 1000
                                    }

        self.__collision_set = set()
        self.__collision_couple_history_set = set()
        self.__collision_notify_set = set()

    def get_collision_set(self):
        return (self.__collision_set)

    # check all plane collision
    def check_collision(self, plane_list_init, console):
        self.__collision_set = set()
        self.__collision_notify_set = set()
        plane_list = plane_list_init.copy()
        #remove wating plane
        plane_list = [plane for plane in plane_list if plane.get_phase() != PLNAE_PHASE['waiting']]
        #check collision condition
        for i in range(len(plane_list)):
                for j in range(i+1,len(plane_list)):
                    collision_couple = (plane_list[i].get_flight_code(), plane_list[j].get_flight_code())
                    if ((math.dist(plane_list[i].get_degree_position(), plane_list[j].get_degree_position())*111 <= self.__separated_distance["horizontal"])
                        and (abs(plane_list[i].get_altitude()-plane_list[j].get_altitude()) <= self.__separated_distance["vertical"])):
                        self.__collision_set.add(collision_couple[0])
                        self.__collision_set.add(collision_couple[1])
                        if len(self.__collision_couple_history_set) == 0:
                            self.__collision_notify_set.add(collision_couple)
                            self.__collision_couple_history_set.add(collision_couple)
                        else :
                            collision_couple_history_list_tmp = copy.deepcopy(self.__collision_couple_history_set)
                            if collision_couple not in collision_couple_history_list_tmp :
                                self.__collision_notify_set.add(collision_couple)
                                self.__collision_couple_history_set.add(collision_couple)
                    else:
                        if collision_couple in self.__collision_couple_history_set:
                            self.__collision_couple_history_set.remove(collision_couple)
        # send warning for collision to console
        response_message = []
        if len(self.__collision_notify_set) > 0:
            for collision_couple in self.__collision_notify_set:
                response_message.append({"warning": "Potential future collisions detected"})
                response_message.append({"warning_sequence": " - {} and {}".format(collision_couple[0], collision_couple[1])})
        console.handle_response(response_message)
