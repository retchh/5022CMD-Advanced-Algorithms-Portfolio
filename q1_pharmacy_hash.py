# =============================================================
# 5022CMD Advanced Algorithms - Q1: Hashing
# Pharmacy Inventory System using Hash Table (Linear Probing)
# =============================================================

import time


# -------------------------------------------------------------
# ENTITY CLASS: Medicine
# -------------------------------------------------------------
class Medicine:
    """Represents a pharmacy product (medicine)."""

    def __init__(self, product_id, name, category, price, quantity):
        self.product_id = product_id   # str  - unique key used for hashing
        self.name       = name         # str  - product name
        self.category   = category     # str  - e.g. tablet, syrup, supplement
        self.price      = price        # float - price in RM
        self.quantity   = quantity     # int  - units in stock

    def __str__(self):
        return (f"[{self.product_id}] {self.name:<25} | "
                f"Category: {self.category:<12} | "
                f"Price: RM{self.price:>6.2f} | "
                f"Qty: {self.quantity}")


# -------------------------------------------------------------
# HASH TABLE with LINEAR PROBING (Open Addressing)
# -------------------------------------------------------------
class HashTable:
    """
    Hash Table using Linear Probing for collision resolution.

    Buckets are stored in a fixed-size Python list (array).
    Each bucket holds either None (empty) or a Medicine object.
    A second list (tombstones) tracks deleted slots so that
    searches are not broken by gaps created by deletions.
    """

    def __init__(self, size=20):
        self.size     = size
        self.buckets  = [None] * size   # the main storage array
        self.deleted  = [False] * size  # tombstone markers for deleted slots
        self.count    = 0               # number of active entries

    # ----------------------------------------------------------
    # HASH FUNCTION
    # ----------------------------------------------------------
    def _hash(self, key):
        """
        Convert a string key to a bucket index.
        Uses Python's built-in hash() then takes modulo table size.
        """
        return hash(key) % self.size

    # ----------------------------------------------------------
    # INSERT
    # ----------------------------------------------------------
    def insert(self, medicine):
        """Insert a Medicine object. Returns True on success."""
        if self.count >= self.size:
            print("Hash table is full!")
            return False

        index = self._hash(medicine.product_id)

        # Linear probing: step forward until empty/deleted slot
        for i in range(self.size):
            probe = (index + i) % self.size
            if self.buckets[probe] is None or self.deleted[probe]:
                self.buckets[probe] = medicine
                self.deleted[probe] = False
                self.count += 1
                return True
            # Update existing record if same key
            if self.buckets[probe].product_id == medicine.product_id:
                self.buckets[probe] = medicine
                return True

        return False

    # ----------------------------------------------------------
    # SEARCH
    # ----------------------------------------------------------
    def search(self, product_id):
        """
        Search for a Medicine by product_id.
        Returns the Medicine object or None if not found.
        """
        index = self._hash(product_id)

        for i in range(self.size):
            probe = (index + i) % self.size

            if self.buckets[probe] is None and not self.deleted[probe]:
                return None  # empty slot = key never inserted here

            if (not self.deleted[probe] and
                    self.buckets[probe] is not None and
                    self.buckets[probe].product_id == product_id):
                return self.buckets[probe]

        return None

    # ----------------------------------------------------------
    # DELETE (optional – uses tombstone)
    # ----------------------------------------------------------
    def delete(self, product_id):
        """Mark a slot as deleted (tombstone approach)."""
        index = self._hash(product_id)

        for i in range(self.size):
            probe = (index + i) % self.size

            if self.buckets[probe] is None and not self.deleted[probe]:
                return False

            if (not self.deleted[probe] and
                    self.buckets[probe] is not None and
                    self.buckets[probe].product_id == product_id):
                self.deleted[probe] = True
                self.count -= 1
                return True

        return False

    # ----------------------------------------------------------
    # DISPLAY ALL
    # ----------------------------------------------------------
    def display(self):
        """Print all active records in the hash table."""
        print("\n" + "=" * 75)
        print(f"{'PHARMACY INVENTORY':^75}")
        print("=" * 75)
        print(f"{'ID':<10} {'Name':<25} {'Category':<14} {'Price':>8} {'Qty':>6}")
        print("-" * 75)
        found = False
        for i in range(self.size):
            if self.buckets[i] is not None and not self.deleted[i]:
                m = self.buckets[i]
                print(f"{m.product_id:<10} {m.name:<25} {m.category:<14} "
                      f"RM{m.price:>6.2f} {m.quantity:>6}")
                found = True
        if not found:
            print("  (No records found)")
        print("=" * 75)
        print(f"  Total items: {self.count}")


# -------------------------------------------------------------
# PERFORMANCE COMPARISON: Hash Table vs 1-D Array
# -------------------------------------------------------------
def performance_comparison(hash_table, array, search_keys):
    """
    Compare search performance between the Hash Table and a plain array.
    Performs multiple searches (existing and non-existing keys).
    """
    print("\n" + "=" * 65)
    print(f"{'PERFORMANCE COMPARISON: Hash Table vs Array':^65}")
    print("=" * 65)

    iterations = 1000  # repeat each search many times for measurable time

    for key in search_keys:
        # --- Hash Table Search ---
        start = time.perf_counter_ns()
        for _ in range(iterations):
            result_ht = hash_table.search(key)
        end = time.perf_counter_ns()
        ht_time = (end - start) / iterations

        # --- Array Linear Search ---
        start = time.perf_counter_ns()
        for _ in range(iterations):
            result_arr = None
            for item in array:
                if item.product_id == key:
                    result_arr = item
                    break
        end = time.perf_counter_ns()
        arr_time = (end - start) / iterations

        found_label = "FOUND" if result_ht else "NOT FOUND"
        print(f"\n  Search key : '{key}' -> {found_label}")
        print(f"  Hash Table : {ht_time:>10.2f} ns (avg over {iterations} runs)")
        print(f"  Array      : {arr_time:>10.2f} ns (avg over {iterations} runs)")
        if arr_time > 0:
            ratio = arr_time / ht_time if ht_time > 0 else float('inf')
            print(f"  Speedup    : Hash Table is ~{ratio:.1f}x faster")

    print("\n" + "-" * 65)
    print("  ANALYSIS:")
    print("  Hash Table (Linear Probing) achieves O(1) average-case search")
    print("  because it computes the index directly via the hash function.")
    print("  Array linear search is O(n) — it scans every element until")
    print("  the key is found (or the list is exhausted).")
    print("  As n grows, the performance gap widens significantly.")
    print("=" * 65)


# -------------------------------------------------------------
# SAMPLE DATA
# -------------------------------------------------------------
SAMPLE_MEDICINES = [
    Medicine("MED001", "Paracetamol 500mg",  "Tablet",     2.50,  200),
    Medicine("MED002", "Ibuprofen 200mg",    "Tablet",     4.80,  150),
    Medicine("MED003", "Amoxicillin 250mg",  "Capsule",    8.90,   80),
    Medicine("MED004", "Loratadine 10mg",    "Tablet",     3.20,  120),
    Medicine("MED005", "Omeprazole 20mg",    "Capsule",    6.50,   90),
    Medicine("MED006", "Cough Syrup 100ml",  "Syrup",      7.00,   60),
    Medicine("MED007", "Vitamin C 1000mg",   "Supplement", 12.00, 300),
    Medicine("MED008", "Fish Oil 1000mg",    "Supplement", 18.50, 250),
    Medicine("MED009", "Antacid Syrup",      "Syrup",      5.50,   75),
    Medicine("MED010", "Cetirizine 10mg",    "Tablet",     2.80,  180),
]


# -------------------------------------------------------------
# COMMAND-LINE INVENTORY SYSTEM (Menu)
# -------------------------------------------------------------
def menu():
    """Main menu-driven CLI for the Pharmacy Inventory System."""

    # --- Initialise hash table and load sample data ---
    ht = HashTable(size=20)
    array = []  # mirror array for performance comparison

    for med in SAMPLE_MEDICINES:
        ht.insert(med)
        array.append(med)

    print("\n" + "*" * 55)
    print("*  Welcome to PharmaCare Local Inventory System    *")
    print("*" * 55)

    while True:
        print("\n  MAIN MENU")
        print("  " + "-" * 35)
        print("  1. Display All Inventory")
        print("  2. Insert New Medicine")
        print("  3. Search Medicine")
        print("  4. Delete Medicine")
        print("  5. Performance Comparison (Hash vs Array)")
        print("  6. Exit")
        print("  " + "-" * 35)

        choice = input("  Enter choice (1-6): ").strip()

        # ---- 1. DISPLAY ----
        if choice == "1":
            ht.display()

        # ---- 2. INSERT ----
        elif choice == "2":
            print("\n  --- Add New Medicine ---")
            pid      = input("  Product ID   : ").strip().upper()
            name     = input("  Name         : ").strip()
            category = input("  Category     : ").strip()
            try:
                price    = float(input("  Price (RM)   : ").strip())
                quantity = int(input("  Quantity     : ").strip())
            except ValueError:
                print("  Invalid price/quantity. Please enter numbers.")
                continue
            med = Medicine(pid, name, category, price, quantity)
            if ht.insert(med):
                array.append(med)
                print(f"  '{name}' inserted successfully.")
            else:
                print("  Insertion failed (table may be full).")

        # ---- 3. SEARCH ----
        elif choice == "3":
            print("\n  --- Search Medicine ---")
            pid = input("  Enter Product ID to search: ").strip().upper()
            result = ht.search(pid)
            if result:
                print("\n  Record Found:")
                print("  " + str(result))
            else:
                print(f"  No record found for ID '{pid}'.")

        # ---- 4. DELETE ----
        elif choice == "4":
            print("\n  --- Delete Medicine ---")
            pid = input("  Enter Product ID to delete: ").strip().upper()
            if ht.delete(pid):
                array[:] = [m for m in array if m.product_id != pid]
                print(f"  Record '{pid}' deleted.")
            else:
                print(f"  Record '{pid}' not found.")

        # ---- 5. PERFORMANCE ----
        elif choice == "5":
            keys = ["MED001", "MED005", "MED010",   # existing
                    "MED099", "INVALID"]              # non-existing
            performance_comparison(ht, array, keys)

        # ---- 6. EXIT ----
        elif choice == "6":
            print("\n  Goodbye! Stay healthy.\n")
            break

        else:
            print("  Invalid option. Please enter 1-6.")


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    menu()
