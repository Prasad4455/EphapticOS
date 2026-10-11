import pytest

import EphapticOS
from EphapticOS.modules.engine.operations.setup import setup
from EphapticOS.modules.search.types import SearchType
from EphapticOS.modules.users.exceptions import PermissionDeniedError
from EphapticOS.modules.users.methods import create_user, get_user
from EphapticOS.modules.users.permissions.methods import authorized_give_permission_on_datasets
from EphapticOS.modules.users.roles.methods import add_user_to_role, create_role
from EphapticOS.modules.users.tenants.methods import add_user_to_tenant, create_tenant, select_tenant
from EphapticOS.shared.logging_utils import CRITICAL, get_logger, setup_logging

logger = get_logger()


async def main():
    # Create a clean slate for EphapticOS -- reset data and system state
    print("Resetting EphapticOS data...")
    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)
    print("Data reset complete.\n")

    # Set up the necessary databases and tables for user management.
    await setup()

    # Add document for user_1, add it under dataset name AI
    text = """A quantum computer is a computer that takes advantage of quantum mechanical phenomena.
    At small scales, physical matter exhibits properties of both particles and waves, and quantum computing leverages
    this behavior, specifically quantum superposition and entanglement, using specialized hardware that supports the
    preparation and manipulation of quantum state"""

    print("Creating user_1: user_1@example.com")
    user_1 = await create_user("user_1@example.com", "example")
    await EphapticOS.add([text], dataset_name="AI", user=user_1)

    print("\nCreating user_2: user_2@example.com")
    user_2 = await create_user("user_2@example.com", "example")

    # Run Ephaptify for both datasets as the appropriate user/owner
    print("\nCreating different datasets for user_1 (AI dataset) and user_2 (QUANTUM dataset)")
    ai_Ephaptify_result = await EphapticOS.Ephaptify(["AI"], user=user_1)

    # Extract dataset_ids from Ephaptify results
    def extract_dataset_id_from_Ephaptify(Ephaptify_result):
        """Extract dataset_id from Ephaptify output dictionary"""
        for dataset_id in Ephaptify_result:
            return dataset_id  # Return the first dataset_id
        return None

    # Get dataset IDs from Ephaptify results
    # Note: When we want to work with datasets from other users (search, add, Ephaptify and etc.) we must supply dataset
    # information through dataset_id using dataset name only looks for datasets owned by current user
    ai_dataset_id = extract_dataset_id_from_Ephaptify(ai_Ephaptify_result)

    # We can see here that user_1 can read his own dataset (AI dataset)
    search_results = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="What is in the document?",
        user=user_1,
        datasets=[ai_dataset_id],
    )

    # Verify that user_2 cannot access user_1's dataset without permission
    with pytest.raises(PermissionDeniedError):
        search_results = await EphapticOS.search(
            query_type=SearchType.GRAPH_COMPLETION,
            query_text="What is in the document?",
            user=user_2,
            datasets=[ai_dataset_id],
        )

    # Create new tenant and role, add user_2 to tenant and role
    tenant_id = await create_tenant("EphapticOSLab", user_1.id)
    await select_tenant(user_id=user_1.id, tenant_id=tenant_id)
    role_id = await create_role(role_name="Researcher", owner_id=user_1.id)
    await add_user_to_tenant(
        user_id=user_2.id, tenant_id=tenant_id, owner_id=user_1.id, set_as_active_tenant=True
    )
    await add_user_to_role(user_id=user_2.id, role_id=role_id, owner_id=user_1.id)

    # Assert that user_1 cannot give permissions on his dataset to role before switching to the correct tenant
    # AI dataset was made with default tenant and not EphapticOSLab tenant
    with pytest.raises(PermissionDeniedError):
        await authorized_give_permission_on_datasets(
            role_id,
            [ai_dataset_id],
            "read",
            user_1.id,
        )

    # We need to refresh the user object with changes made when switching tenants
    user_1 = await get_user(user_1.id)
    await EphapticOS.add([text], dataset_name="AI_EphapticOS_LAB", user=user_1)
    ai_EphapticOS_lab_Ephaptify_result = await EphapticOS.Ephaptify(["AI_EphapticOS_LAB"], user=user_1)

    ai_EphapticOS_lab_dataset_id = extract_dataset_id_from_Ephaptify(ai_EphapticOS_lab_Ephaptify_result)

    await authorized_give_permission_on_datasets(
        role_id,
        [ai_EphapticOS_lab_dataset_id],
        "read",
        user_1.id,
    )

    search_results = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="What is in the document?",
        user=user_2,
        dataset_ids=[ai_EphapticOS_lab_dataset_id],
    )
    for result in search_results:
        print(f"{result}\n")

    # Let's test changing tenants
    tenant_id = await create_tenant("EphapticOSLab2", user_1.id)
    await select_tenant(user_id=user_1.id, tenant_id=tenant_id)

    user_1 = await get_user(user_1.id)
    await EphapticOS.add([text], dataset_name="AI_EphapticOS_LAB", user=user_1)
    await EphapticOS.Ephaptify(["AI_EphapticOS_LAB"], user=user_1)

    search_results = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="What is in the document?",
        user=user_1,
    )

    # Assert only AI_EphapticOS_LAB dataset from EphapticOSLab2 tenant is visible as the currently selected tenant
    assert len(search_results) == 1, (
        f"Search results must only contain one dataset from current tenant: {search_results}"
    )
    assert search_results[0]["dataset_name"] == "AI_EphapticOS_LAB", (
        f"Dict must contain dataset name 'AI_EphapticOS_LAB': {search_results[0]}"
    )
    assert search_results[0]["dataset_tenant_id"] == user_1.tenant_id, (
        f"Dataset tenant_id must be same as user_1 tenant_id: {search_results[0]}"
    )

    # Switch back to no tenant (default tenant)
    await select_tenant(user_id=user_1.id, tenant_id=None)
    # Refresh user_1 object
    user_1 = await get_user(user_1.id)
    search_results = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="What is in the document?",
        user=user_1,
    )
    assert len(search_results) == 1, (
        f"Search results must only contain one dataset from default tenant: {search_results}"
    )
    assert search_results[0]["dataset_name"] == "AI", (
        f"Dict must contain dataset name 'AI': {search_results[0]}"
    )


if __name__ == "__main__":
    import asyncio

    logger = setup_logging(log_level=CRITICAL)
    asyncio.run(main())
