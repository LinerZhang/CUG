from functools import lru_cache

def parse_files(input_file, price_file, promo_file):
    #input.txt
    with open(input_file, 'r') as f:
        lines = f.readlines()
    item_count = int(lines[0].strip())#the first line
    items = []
    for line in lines[1:]:
        id_, qty, price = line.strip().split()
        items.append({"id": int(id_), "qty": int(qty), "price": float(price)})
    #in items[],each element is a dictionary{}

    #price.txt
    with open(price_file, 'r') as f:
        price_lines = f.readlines()
    prices = {int(line.split()[0]): float(line.split()[1]) for line in price_lines}
    #price is a dictionary{}

    #promotions.txt
    with open(promo_file, 'r') as f:
        promo_lines = f.readlines()
    promo_count = int(promo_lines[0].strip())#the first line
    promotions = []
    for line in promo_lines[1:]:
        data = line.strip().split()
        item_types = int(data[0])
        promo_items = []
        for i in range(item_types):
            promo_items.append({"id": int(data[1 + i * 2]), "qty": int(data[2 + i * 2])})
        promo_price = float(data[-1])
        promotions.append({"items": promo_items, "price": promo_price})#items is a list and its elements are dintionaries 
    return items, promotions, prices

def find_min_cost(items, promotions):
    def dp(remaining):
        if all(x == 0 for x in remaining):
            return 0, []
        min_cost = float('inf')
        best_plan = None
        #try to use promotions
        for promo in promotions:#promo is a dictionary{items:{id:qty} ,price:price}
            new_remaining = list(remaining)
            valid = True
            for p_item in promo["items"]:
                idx = next((i for i, item in enumerate(items) if item["id"] == p_item["id"]), None)
                #to find if the items of this promotion exist in items
                if idx is not None and new_remaining[idx] >= p_item["qty"]:
                    #if they exist and they are enough to use this promotion
                    new_remaining[idx] -= p_item["qty"]
                else:
                    valid = False
                    break
            if valid:
                cost, plan = dp(tuple(new_remaining))
                if cost + promo["price"] < min_cost:
                    min_cost = cost + promo["price"]
                    temp_items = promo['items']
                    str1 = ""
                    for temp in temp_items:
                        str1 += f"{temp['id']} {temp['qty']} "
                    best_plan = plan + [f"{str1}{promo['price']}"]

        for i, qty in enumerate(remaining):
            if qty > 0:
                new_remaining = list(remaining)
                new_remaining[i] -= 1
                cost, plan = dp(tuple(new_remaining))
                if cost + items[i]["price"] < min_cost:
                    min_cost = cost + items[i]["price"]
                    best_plan = plan + [f"{items[i]['id']} {items[i]['price']}"]

        return min_cost, best_plan

    initial_state = tuple(item["qty"] for item in items)
    return dp(initial_state)

def process_and_combine_lines(plan,prices):
    from collections import defaultdict
    processed_lines = []
    # 创建一个字典来存储商品代码和价格的映射
    items = defaultdict(int)
    # 读取输入文件并填充字典

    for line in plan:
        parts = line.strip().split()
        if len(parts) == 2:  # 检查是否为两个元素的行
            item_code, price = parts
            items[item_code] += 1  # 增加商品代码的数量
        elif len(parts) > 3:  # 如果行元素超过三个，不做处理
            processed_lines.append(f"{line.strip()}")
        else:
            # 对于三个元素的行，直接输出
            processed_lines.append(f"{line.strip()}")

    # 处理字典，输出结果
    for item_code, count in items.items():
        if count == 1:  # 如果数量为1，输出三行
            price = float(prices[int(item_code)])
            processed_lines.append(f"{item_code} 1 {price}")
        else:  # 如果数量大于1，合并输出
            price = float(prices[int(item_code)])  # 假设价格存储在字典的值中
            processed_lines.append(f"{item_code} {count} {price * count}")
    return processed_lines
def write_output(output_file, min_cost, plan):
    """写入输出文件"""
    #成功写入返回true
    try:
        with open(output_file, 'w') as f:

            for step in plan:
                f.write(f"{step}\n")
            f.write(f"{min_cost}\n")
            return True
    except Exception as e:
        print("Error writing to file:", e)
        return False


def main():
    input_file = "min_price\input.txt"
    price_file = "min_price\price.txt"
    promo_file = "min_price\promotions.txt"
    output_file = "min_price\output.txt"

    items, promotions, prices = parse_files(input_file, price_file, promo_file)
    #update the price according to price.txt
    for item in items:
        item["price"] = prices[item["id"]]

    #
    min_cost, plan = find_min_cost(items, promotions)
    output_plan = process_and_combine_lines(plan,prices)
    # 写入输出
    write_output(output_file, min_cost, output_plan)

if __name__ == "__main__":
    main()
