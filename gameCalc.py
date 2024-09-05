#TRUST drops when accused
#INDP increases when accused
#TRUST gains each round
#X rounds in total
#INDP increases lying and hiding items and taking breaks
#INDP increases when someone is killed in the same room  DONE
#TRUST drops when witnessing a murder DONE
#INDP drops when a task is done
#SUS goes to random if no one near them or if they think a person is SAFE the exempt
#Gaining a weapon increases INDP
#seeing another with a weapon decreases TRUST
#seeing another with a weapon increases SUS
#utilities installed increases TRUST
#tend to flee when they see a weapon
#tend to conceal weapons

import random
import curses
import unit
import math
import area
import item
import brain
import gameCalc
import time

def runTheHour(units, areas):
    #follow procedural chart
    #isolate alive people
    #Search chance

    for i in range(len(area)):
        for j in range(len(area.units)):
            current_area = areas[i]
            current_unit = areas[i].units[j]
            if current_unit.role == 0: #is not killer
                search_possible = False
                search_chance = 0
                task_chance = 0
                #decide wheter to search
                if len(current_area).items > 0:
                    search_possible = True
                if search_possible:
                    x = random.randint(0,1)
                    current_unit.directive = x
                else:
                    current_unit.directive = 0
                #Check if want to move --> SCARED or not do anything --> TRUST and INDP
                #MOVE
                #they see an unknown body
                move_chance = 0
                for k in range(len(current_area.bodies)):
                    if current_area.bodies[k].knownDead == False:
                        move_chance += 50
                        #add opinion
                        for p in range(len(current_area.units)):
                            if p != j: #not this person
                                current_unit.opinons[p].op -= 20
                                current_unit.trust -= 5
                        if current_unit.trust < 0:
                            current_unit.trust = 0
                        current_unit.independence += 2
                        if current_unit.independence > 20:
                            current_unit.independence = 20

                #they see a weapon
                for k in range(len(current_area.units)):
                    for p in range(len(current_area.units[k].items)):
                        if current_area.units[k].items[p] != None:
                            if current_area.units[k].items[p] != None:
                                move_chance += 10
                                current_unit.opinons[current_area.units[k].id - 1].op -= 10
                
                #there is no tasks left and no items
                if current_area.easy_tasks + current_area.med_tasks + current_area.hard_tasks <= 0 and not search_possible:
                    move_chance += 1000

                #do nothing
                lazy_chance = 0
                x = 0
                if current_unit.trust < 6: #60
                    x = 6 - current_unit.trust
                if current_unit.independence > 15: #50
                    x = 20 - current_unit.independence
                lazy_chance = x * 10

                #attack a unit
                attack_chance = 0
                for k in range(len(current_unit.opinions)):
                    for p in range(len(current_area.units)):
                        if current_unit.opinons[k].op <= 20 and current_unit.opinons[k].id == current_area.units[p].id:
                            #attack chance way up
                            attack_chance += 70
                #check items
                for k in range(len(current_area.units)):
                    for p in range(len(current_area.units[k].items)):
                        if current_area.units[k].items[p].area == current_area.id:
                            #remove item and grant the amount of points HIDDEN STUFF CAN NOT CONTAIN THESE ITEMS IG
                            #check lv and give to stats
                            if current_area.units[k].items[p].lv == 1:
                                current_area.med_tasks -= 1
                                current_area.units[k].items[p] = None
                            if current_area.units[k].items[p].lv == 2:
                                current_area.hard_tasks -= .5
                                current_area.units[k].items[p] = None
                #need to remove opinions on dead people set to 50

                #do attack
                #do nothing
                #do move
                #do search/tasks