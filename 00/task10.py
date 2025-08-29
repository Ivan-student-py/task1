def main():
    try:
        input_data = input().split()
        if len(input_data) !=2:
            print("Invalid input")
            return
        N, T = map(int, input_data)
        if N <= 0 or T <= 0:
            print("Invalid input")
            return
        
        devices_by_year = {}

        for _ in range(N):
            device_data = input().split()
            if len(device_data) != 3:
                print("Invalid input")
                return
            year, cost, time = map(int, device_data)
            if year <= 0 or cost <= 0 or time <= 0:
                print("Invalid input")
                return
            if year not in devices_by_year:
                devices_by_year[year] = []
            devices_by_year[year].append((cost, time))
        
        min_cost = float('inf')

        for year, devices in devices_by_year.items():
            n = len(devices)
            for i in range(n):
                for j in range(i + 1, n):
                    cost1, time1 = devices[i]
                    cost2, time2 = devices[j]
                    if time1 + time2 >= T:
                        total_cost = cost1 + cost2
                        min_cost = min(min_cost, total_cost)
        if min_cost != float('inf'):
            print(min_cost)
        else:
            print("Invalid input")

    except Exception:
        print("Invalid input")

if __name__ == "__main__":
    main()