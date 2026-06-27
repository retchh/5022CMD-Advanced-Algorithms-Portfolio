# =============================================================
# 5022CMD Advanced Algorithms - Q2: Divide and Conquer
# Customer Transaction System using Merge Sort + Binary Search
# =============================================================

import time
import random


# -------------------------------------------------------------
# ENTITY CLASS: Transaction
# -------------------------------------------------------------
class Transaction:
    """Represents a single customer transaction in an online shop."""

    def __init__(self, transaction_id, customer_name, product_name,
                 amount, transaction_date):
        self.transaction_id   = transaction_id    # int   - unique key (sort/search on this)
        self.customer_name    = customer_name     # str   - customer's name
        self.product_name     = product_name      # str   - product purchased
        self.amount           = amount            # float - transaction value (RM)
        self.transaction_date = transaction_date  # str   - date "YYYY-MM-DD"

    def __str__(self):
        return (f"ID: {self.transaction_id:<5} | "
                f"{self.customer_name:<12} | "
                f"{self.product_name:<18} | "
                f"RM{self.amount:>8.2f} | "
                f"{self.transaction_date}")


# -------------------------------------------------------------
# MERGE SORT (Divide and Conquer)
# Global counter tracks recursive calls (optional feature)
# -------------------------------------------------------------
recursive_calls = 0  # counts MERGE_SORT calls for analysis


def merge_sort(arr, key="transaction_id"):
    """
    DIVIDE step:
      - Split the list into two halves at the midpoint.
    CONQUER step:
      - Recursively sort each half.
    COMBINE step:
      - Merge the two sorted halves back together (in merge()).
    Sorts on the chosen attribute (default: transaction_id).
    """
    global recursive_calls
    recursive_calls += 1

    # Base case: a list of 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr

    # ---- DIVIDE ----
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # ---- CONQUER (recursive calls) ----
    left_sorted = merge_sort(left_half, key)
    right_sorted = merge_sort(right_half, key)

    # ---- COMBINE ----
    return merge(left_sorted, right_sorted, key)


def merge(left, right, key):
    """
    COMBINE step of merge sort.
    Merges two already-sorted lists into one sorted list by
    repeatedly taking the smaller front element from each.
    """
    result = []
    i = j = 0

    # Compare front elements and append the smaller one
    while i < len(left) and j < len(right):
        if getattr(left[i], key) <= getattr(right[j], key):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements (one side may be longer)
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# -------------------------------------------------------------
# BINARY SEARCH (Divide and Conquer) - recursive
# Requires the list to be SORTED on transaction_id first
# -------------------------------------------------------------
def binary_search(arr, low, high, target_id):
    """
    Recursive binary search on transaction_id.
    DIVIDE: examine the middle element.
    CONQUER: recurse into the half that may contain the target.
    Returns the index if found, else -1.
    """
    # Base case: search space exhausted
    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid].transaction_id == target_id:
        return mid                                   # found
    elif target_id < arr[mid].transaction_id:
        return binary_search(arr, low, mid - 1, target_id)   # search LEFT
    else:
        return binary_search(arr, mid + 1, high, target_id)  # search RIGHT


# -------------------------------------------------------------
# LINEAR SEARCH (for comparison with Binary Search)
# -------------------------------------------------------------
def linear_search(arr, target_id):
    """Scan every element until the target is found. O(n)."""
    for index in range(len(arr)):
        if arr[index].transaction_id == target_id:
            return index
    return -1


# -------------------------------------------------------------
# SAMPLE DATASET (15 unsorted transaction records)
# -------------------------------------------------------------
def build_dataset():
    """Returns a list of unsorted Transaction objects."""
    data = [
        Transaction(105, "Alice",   "Wireless Mouse",    59.90,  "2026-01-05"),
        Transaction(102, "Bob",     "USB-C Cable",       19.50,  "2026-01-07"),
        Transaction(118, "Charlie", "Mechanical Keyboard",189.00, "2026-01-09"),
        Transaction(101, "Diana",   "Laptop Stand",      75.00,  "2026-01-02"),
        Transaction(110, "Ethan",   "Webcam HD",         120.00, "2026-01-11"),
        Transaction(107, "Fiona",   "Headphones",        249.90, "2026-01-03"),
        Transaction(103, "George",  "Phone Case",        29.90,  "2026-01-12"),
        Transaction(115, "Hannah",  "Power Bank",        89.00,  "2026-01-06"),
        Transaction(109, "Ian",     "HDMI Adapter",      35.50,  "2026-01-08"),
        Transaction(112, "Julia",   "Monitor 24in",      450.00, "2026-01-04"),
        Transaction(104, "Kevin",   "Mouse Pad",         15.00,  "2026-01-10"),
        Transaction(120, "Laura",   "External SSD 1TB",  320.00, "2026-01-13"),
        Transaction(106, "Mike",    "Laptop Sleeve",     45.00,  "2026-01-14"),
        Transaction(114, "Nina",    "Bluetooth Speaker", 150.00, "2026-01-15"),
        Transaction(108, "Oscar",   "Desk Lamp",         62.50,  "2026-01-16"),
    ]
    return data


# -------------------------------------------------------------
# DISPLAY HELPERS
# -------------------------------------------------------------
def display_transactions(arr, title="TRANSACTIONS"):
    print("\n" + "=" * 78)
    print(f"{title:^78}")
    print("=" * 78)
    for t in arr:
        print("  " + str(t))
    print("=" * 78)
    print(f"  Total records: {len(arr)}")


# -------------------------------------------------------------
# PERFORMANCE COMPARISON: Merge Sort vs Binary Search
# -------------------------------------------------------------
def performance_comparison(data):
    """Measure execution time of Merge Sort and Binary Search."""
    global recursive_calls
    print("\n" + "=" * 65)
    print(f"{'PERFORMANCE COMPARISON: Merge Sort vs Binary Search':^65}")
    print("=" * 65)

    # --- Merge Sort timing ---
    recursive_calls = 0
    start = time.perf_counter_ns()
    sorted_data = merge_sort(list(data))
    end = time.perf_counter_ns()
    merge_time = end - start

    # --- Binary Search timing (search an existing key) ---
    target = sorted_data[len(sorted_data) // 2].transaction_id
    start = time.perf_counter_ns()
    binary_search(sorted_data, 0, len(sorted_data) - 1, target)
    end = time.perf_counter_ns()
    bsearch_time = end - start

    print(f"\n  Dataset size            : {len(data)} records")
    print(f"  Merge Sort time         : {merge_time:>10} ns")
    print(f"  Merge Sort recursive calls: {recursive_calls}")
    print(f"  Binary Search time      : {bsearch_time:>10} ns")
    print("\n  " + "-" * 60)
    print("  ANALYSIS:")
    print("  Merge Sort     -> O(n log n): it divides the list and merges,")
    print("                    doing more work as it must order ALL elements.")
    print("  Binary Search  -> O(log n) : it halves the search space each")
    print("                    step, so it finishes far faster than sorting.")
    print("  Sorting is inherently more expensive than a single search,")
    print("  which is why Merge Sort takes longer than Binary Search.")
    print("=" * 65)


# -------------------------------------------------------------
# COMPLEXITY TABLE (optional advanced feature)
# -------------------------------------------------------------
def complexity_table():
    print("\n" + "=" * 60)
    print(f"{'TIME COMPLEXITY ANALYSIS':^60}")
    print("=" * 60)
    print(f"  {'Algorithm':<18}{'Best':<12}{'Average':<14}{'Worst':<12}")
    print("  " + "-" * 54)
    print(f"  {'Merge Sort':<18}{'O(n log n)':<12}{'O(n log n)':<14}{'O(n log n)':<12}")
    print(f"  {'Binary Search':<18}{'O(1)':<12}{'O(log n)':<14}{'O(log n)':<12}")
    print(f"  {'Linear Search':<18}{'O(1)':<12}{'O(n)':<14}{'O(n)':<12}")
    print("=" * 60)


# -------------------------------------------------------------
# MENU-DRIVEN PROGRAM
# -------------------------------------------------------------
def menu():
    data = build_dataset()          # unsorted working list
    is_sorted = False               # track whether data is sorted

    print("\n" + "*" * 58)
    print("*   Customer Transaction Management System (D&C)        *")
    print("*" * 58)

    while True:
        print("\n  MAIN MENU")
        print("  " + "-" * 45)
        print("  1. Display all transactions")
        print("  2. Sort transactions (Merge Sort)")
        print("  3. Search transaction (Binary Search)")
        print("  4. Search transaction (Linear Search)")
        print("  5. Insert new transaction")
        print("  6. Sort by amount (Merge Sort)")
        print("  7. Performance comparison")
        print("  8. Show complexity table")
        print("  9. Exit")
        print("  " + "-" * 45)

        choice = input("  Enter choice (1-9): ").strip()

        # ---- 1. DISPLAY ----
        if choice == "1":
            display_transactions(data,
                "ALL TRANSACTIONS (sorted)" if is_sorted
                else "ALL TRANSACTIONS (unsorted)")

        # ---- 2. MERGE SORT by ID ----
        elif choice == "2":
            global recursive_calls
            print("\n  --- BEFORE SORTING ---")
            display_transactions(data, "BEFORE MERGE SORT")
            recursive_calls = 0
            data = merge_sort(data, "transaction_id")
            is_sorted = True
            print("\n  --- AFTER SORTING (by transaction_id) ---")
            display_transactions(data, "AFTER MERGE SORT")
            print(f"  Recursive calls made: {recursive_calls}")

        # ---- 3. BINARY SEARCH ----
        elif choice == "3":
            if not is_sorted:
                print("\n  Data must be sorted first! Sorting now...")
                data = merge_sort(data, "transaction_id")
                is_sorted = True
            try:
                tid = int(input("  Enter transaction ID to search: ").strip())
            except ValueError:
                print("  Invalid ID. Please enter a number.")
                continue
            idx = binary_search(data, 0, len(data) - 1, tid)
            if idx != -1:
                print(f"\n  [Binary Search] FOUND at index {idx}:")
                print("  " + str(data[idx]))
            else:
                print(f"\n  [Binary Search] Transaction ID {tid} NOT FOUND.")

        # ---- 4. LINEAR SEARCH ----
        elif choice == "4":
            try:
                tid = int(input("  Enter transaction ID to search: ").strip())
            except ValueError:
                print("  Invalid ID. Please enter a number.")
                continue
            idx = linear_search(data, tid)
            if idx != -1:
                print(f"\n  [Linear Search] FOUND at index {idx}:")
                print("  " + str(data[idx]))
            else:
                print(f"\n  [Linear Search] Transaction ID {tid} NOT FOUND.")

        # ---- 5. INSERT ----
        elif choice == "5":
            print("\n  --- Insert New Transaction ---")
            try:
                tid    = int(input("  Transaction ID : ").strip())
                name   = input("  Customer Name  : ").strip()
                product= input("  Product Name   : ").strip()
                amount = float(input("  Amount (RM)    : ").strip())
                date   = input("  Date (YYYY-MM-DD): ").strip()
            except ValueError:
                print("  Invalid input. Transaction not added.")
                continue
            data.append(Transaction(tid, name, product, amount, date))
            is_sorted = False
            print(f"  Transaction {tid} added. (List is now unsorted)")

        # ---- 6. SORT BY AMOUNT ----
        elif choice == "6":
            data = merge_sort(data, "amount")
            is_sorted = False  # sorted by amount, not ID
            display_transactions(data, "SORTED BY AMOUNT (ascending)")
            print("  Note: list is sorted by AMOUNT, not ID.")
            print("  Re-sort by ID before using Binary Search.")

        # ---- 7. PERFORMANCE ----
        elif choice == "7":
            performance_comparison(data)

        # ---- 8. COMPLEXITY TABLE ----
        elif choice == "8":
            complexity_table()

        # ---- 9. EXIT ----
        elif choice == "9":
            print("\n  Goodbye!\n")
            break

        else:
            print("  Invalid option. Please enter 1-9.")


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    menu()
