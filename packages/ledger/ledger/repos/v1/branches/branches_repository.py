from .data.branches_datasource import BranchesDataSource
from .models.branch_model import CreateBranch, UpdateBranch, BranchInDb

from ledger.tools import TimeTools, UuidTool


class BranchesRepository:
    _instance: "BranchesRepository|None" = None

    def __init__(self, branches_ds: BranchesDataSource):
        self.branches_ds = branches_ds

    @classmethod
    def get_instance(cls) -> "BranchesRepository":
        if cls._instance is None:
            cls._instance = cls(BranchesDataSource())
        return cls._instance

    async def create_branch(self, create_branch: CreateBranch) -> BranchInDb:
        new_branch_in_db = BranchInDb(
            **create_branch.model_dump(),
            id=UuidTool.generate_uuid(),
            createdAt=TimeTools.get_now_in_milliseconds(),
        )

        await self.branches_ds.create_branch(new_branch_in_db.model_dump())

        return new_branch_in_db

    async def get_all_branches(self) -> list[BranchInDb]:
        results = await self.branches_ds.get_all_branches()
        models = [BranchInDb.model_validate(result) for result in results]
        return models

    async def get_branch_by_id(self, branch_id: str) -> BranchInDb | None:
        result = await self.branches_ds.get_branch_by_id(branch_id)

        if result is None:
            return None

        return BranchInDb.model_validate(result)

    async def update_branch_by_id(
        self, branch_id: str, branch: UpdateBranch
    ) -> BranchInDb | None:

        branch_data = branch.model_dump(exclude_unset=True)

        branch_data["updatedAt"] = TimeTools.get_now_in_milliseconds()

        result = await self.branches_ds.update_branch_by_id(branch_id, branch_data)

        if result is None:
            return None

        return BranchInDb.model_validate(result)

    async def delete_branch_by_id(self, branch_id: str) -> BranchInDb | None:
        result = await self.branches_ds.delete_branch_by_id(branch_id)

        if result is None:
            return None

        return BranchInDb.model_validate(result)
