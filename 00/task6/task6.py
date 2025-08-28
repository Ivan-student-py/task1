import json

def merge_sorted_lists(list1, list2):
    merged = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i]['year'] <= list2[j]['year']:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    while i < len(list1):
        merged.append(list1[i])
        i += 1
    while j < len(list2):
        merged.append(list2[j])
        j += 1

    return merged

def main():
    try:
        with open("00/task6/input.txt", "r") as file:
            data = json.load(file)
        if 'list1' not in data or 'list2' not in data:
            print("Invalid input")
            return
        list1 = data['list1']
        list2 = data['list2']
        if not isinstance(list1, list) or not isinstance(list2, list):
            print("Invalid input")
            return
        merged_list = merge_sorted_lists(list1, list2)
        result = {"list0": merged_list}
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (json.JSONDecodeError, FileNotFoundError):
        print("Invalid input")

if __name__ == "__main__":
    main()