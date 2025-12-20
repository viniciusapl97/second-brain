from app.infra.supabase.client import get_supabase_client


class MemoryRepository:
    TABLE_NAME = "memory_notes"

    def create(self, data: dict) -> dict:
        supabase = get_supabase_client()

        response = (
            supabase
            .table(self.TABLE_NAME)
            .insert(data)
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to insert memory")

        return response.data[0]

    def get_by_id(self, memory_id: str) -> dict | None:
        supabase = get_supabase_client()

        response = (
            supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("id", memory_id)
            .single()
            .execute()
        )

        return response.data
