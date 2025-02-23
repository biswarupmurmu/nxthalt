import heapq

def time_str_to_minutes(t1:str):
    t1 = t1.split(":")
    a=0
    a += int(t1[0].strip())
    a *= 60
    a += int(t1[1].strip())

    return a

def minutes_to_time(t):
    h = t//60
    m = t%60
    return f"{h}:{m}"

def minutes_to_words(t):
    h = t//60
    m = t%60
    return f"{h} hrs {m} minutes"

def view_bus(bus):
    print(bus['name'])
    schedule = dict(bus['schedule'])
    for stop in bus['stops']:
        print(stop['name'], schedule[stop['id']])

    # sys.exit()


def create_graph(mongo):
    print("Creating the graph")
    buses = mongo.db['busroutes'].find({})
    graph = dict()
    buses = list(buses)
    c = 0
    b = 0
    for i in range(len(buses)):
        bus=buses[i]
        # print(bus)
        # sys.exit()
        stops=bus['stops']
        schedule = dict(bus['schedule'])

        if bus['name'].strip() == 'Mitra':
            #view_bus(bus)
            pass

        for i in range(len(stops)):
            origin = stops[i]['name']
            origin_id = stops[i]['id']
            origin = origin.lower()
            for j in range(i+1, len(stops)):
                destination = stops[j]['name']
                destination_id = stops[j]['id']
                destination = destination.lower()
                src_departure_time = time_str_to_minutes(schedule[origin_id])
                des_arrival_time = time_str_to_minutes(schedule[destination_id])
                journey_time = des_arrival_time - src_departure_time

                if origin not in graph:
                    graph[origin] = []

                if journey_time < 0:
                    des_arrival_time += 720
                    journey_time = des_arrival_time - src_departure_time
                    c += 1
                if journey_time < 0:
                    if des_arrival_time >= 720:
                        des_arrival_time -= 720
                        journey_time = time_str_to_minutes('24:00') - time_str_to_minutes(schedule[origin_id]) + time_str_to_minutes(schedule[destination_id])
                        # print(bus['name'], origin, destination, schedule[origin_id], schedule[destination_id], journey_time)
                        b += 1

                graph[origin].append([destination, src_departure_time, journey_time, bus['operatingDays'], bus['name']])

    print(f"Length of graph {len(graph)} and time problem {c}, left problem {b}")
    return graph


def dijkstra(graph, start, end, arrival_time, mode='time'):
    print('trying to find route between ', start, end, arrival_time)
    queue = []
    shortest_paths = {start: [0,  None, None, arrival_time]}  # (cost(journey), source bus stand, bus name, departure_time)
    shortest_paths = {start: {'cost':0, 'source':None, 'bus':None, 'departure': arrival_time}}  # (cost(journey), source bus stand, bus name, departure_time)
    visited = set()
    
    heapq.heappush(queue, (0, start, arrival_time))  # (cost, busstand, arrival_time)

    while queue:
        current_cost, current_busstand, arrival_time = heapq.heappop(queue)

        if current_busstand == end:
            break

        # If the bus stand has already been visited, skip it
        if current_busstand in visited:
            continue
        visited.add(current_busstand)

        for neighbor in graph.get(current_busstand, []):
            neighbor_name, departure_time, journey_time, operating_daya, bus_name = neighbor
            
            # Check if we can take this bus (we need to arrive before departure)
            if arrival_time <= departure_time:
                # Calculate the new cost based on the mode
                if mode == 'time':
                    new_cost = current_cost + journey_time
                    new_cost = new_cost + departure_time - arrival_time
                else:
                    raise ValueError("Mode must be 'time'")

                # If this path to the neighbor is shorter, update the shortest path
                if neighbor_name not in shortest_paths or new_cost < shortest_paths[neighbor_name]['cost']:
                    #shortest_paths[neighbor_name] = [journey_time, current_busstand, bus_name, departure_time]
                    shortest_paths[neighbor_name] = {
                        'cost': journey_time,
                        'source' : current_busstand,
                        'bus' : bus_name,
                        'departure' : departure_time
                    }
                    # Push the neighbor into the queue with the new cost and arrival time
                    heapq.heappush(queue, (new_cost, neighbor_name, departure_time + journey_time))
            # else:
            #     print(f"Cannot take bus '{route.bus.name}' from {current_busstand} to {neighbor_name} - Arrival time: {arrival_time}, Departure time: {departure_time}")
            #

    current = end
    path = []
    while current is not None:
        p = shortest_paths.get(current, {'cost':0, 'source':None, 'bus':None, 'departure': arrival_time})
        p['destination'] = current
        p['cost'] = minutes_to_words(p['cost'])
        p['departure'] = minutes_to_time(p['departure'])

        if p['source']:
            path.append(p)
        current = p['source']

    path.reverse()

    return path


if __name__ == "__main__":
    pass
