class Participant:
    def __init__(self, name, can_commit=True):
        self.name = name
        self.can_commit = can_commit
        self.prepared = False

    def prepare(self):
        print(f"[{self.name}] Received PREPARE request.")
        if self.can_commit:
            self.prepared = True
            print(f"[{self.name}] Prepared to commit.")
            return True
        else:
            print(f"[{self.name}] Cannot commit! Voting NO.")
            return False

    def commit(self):
        if self.prepared:
            print(f"[{self.name}] Committing transaction.")
            self.prepared = False
        else:
            print(f"[{self.name}] Cannot commit, was not prepared.")

    def rollback(self):
        print(f"[{self.name}] Rolling back transaction.")
        self.prepared = False


class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def execute_transaction(self):
        print("=== Phase 1: Prepare ===")
        votes = []
        for p in self.participants:
            vote = p.prepare()
            votes.append(vote)

        if all(votes):
            print("\n=== Phase 2: Commit ===")
            for p in self.participants:
                p.commit()
            print("\n✅ Transaction committed successfully.")
        else:
            print("\n=== Phase 2: Rollback ===")
            for p in self.participants:
                p.rollback()
            print("\n❌ Transaction rolled back due to failure.")


if __name__ == "__main__":
    # 正常情况：两个服务都准备好
    print("----- CASE 1: All commit -----")
    pa = Participant("InventoryService")
    pb = Participant("AccountService")
    coordinator = Coordinator([pa, pb])
    coordinator.execute_transaction()

    print("\n----- CASE 2: One fails -----")
    pa = Participant("InventoryService", can_commit=False)  # 模拟一个失败
    pb = Participant("AccountService")
    coordinator = Coordinator([pa, pb])
    coordinator.execute_transaction()
