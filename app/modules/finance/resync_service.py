from app.modules.finance.repository import FinanceRepository
from app.modules.finance.notion_sync_service import FinanceNotionSyncService


class FinanceResyncService:
    def __init__(self):
        self.repo = FinanceRepository()
        self.notion = FinanceNotionSyncService()

    def resync_all(self):
        transactions = self.repo.list_all()

        total = len(transactions)
        success = 0
        failed = 0

        for tx in transactions:
            try:
                self.notion.sync_transaction(tx)
                success += 1
            except Exception as e:
                print(f"❌ Falha ao sync {tx.get('id')}: {e}")
                failed += 1

        return {
            "total": total,
            "success": success,
            "failed": failed
        }
