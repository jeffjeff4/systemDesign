import requests
import uuid

participants = {
    "participant_a": "http://localhost:5001",
    "participant_b": "http://localhost:5002"
}

def coordinator_transaction():
    txn_id = str(uuid.uuid4())
    print(f"Start 2PC Transaction: {txn_id}")

    # Phase 1: Prepare
    print("Phase 1: Sending prepare...")
    prepared = True
    for name, url in participants.items():
        try:
            res = requests.post(f"{url}/prepare", json={"txn_id": txn_id})
            if res.status_code != 200:
                print(f"{name} voted ABORT.")
                prepared = False
                break
            print(f"{name} voted YES.")
        except Exception as e:
            print(f"{name} failed: {e}")
            prepared = False
            break

    # Phase 2: Commit or Rollback
    if prepared:
        print("All participants are ready. Sending COMMIT.")
        for name, url in participants.items():
            requests.post(f"{url}/commit", json={"txn_id": txn_id})
        print("✅ Transaction committed.")
    else:
        print("Something went wrong. Sending ROLLBACK.")
        for name, url in participants.items():
            requests.post(f"{url}/rollback", json={"txn_id": txn_id})
        print("❌ Transaction rolled back.")

if __name__ == '__main__':
    coordinator_transaction()
