import pytest
from v1.api_utils.pagination import Pagination


class TestPagination:
    @pytest.mark.asyncio
    async def test_pagination_execute_success(self):
        # Sample data for testing
        test_data = [i for i in range(1, 21)]  # 20 items

        # Test parameters
        page = 2
        limit = 5

        # Expected results
        expected_items = test_data[(page - 1) * limit : page * limit]
        expected_total_pages = 4
        expected_total_items = 20

        # Execute pagination
        result = await Pagination.execute(test_data, page, limit)

        # Check the results
        assert result.items == expected_items
        assert result.state.page == page
        assert result.state.size == limit
        assert result.state.total_pages == expected_total_pages
        assert result.state.total_items == expected_total_items

    @pytest.mark.asyncio
    async def test_pagination_execute_empty_list(self):
        # Empty data for testing
        test_data = []

        # Test parameters
        page = 1
        limit = 5

        # Execute pagination
        result = await Pagination.execute(test_data, page, limit)

        # Check the results
        assert result.items == []
        assert result.state.page == page
        assert result.state.size == limit
        assert result.state.total_pages == 0
        assert result.state.total_items == 0

    @pytest.mark.asyncio
    async def test_pagination_execute_last_page(self):
        # Sample data for testing
        test_data = [i for i in range(1, 11)]  # 10 items

        # Test parameters
        page = 3
        limit = 4

        # Expected results
        expected_items = test_data[(page - 1) * limit : page * limit]
        expected_total_pages = 3
        expected_total_items = 10

        # Execute pagination
        result = await Pagination.execute(test_data, page, limit)

        # Check the results
        assert result.items == expected_items
        assert result.state.page == page
        assert result.state.size == limit
        assert result.state.total_pages == expected_total_pages
        assert result.state.total_items == expected_total_items

    @pytest.mark.asyncio
    async def test_pagination_execute_invalid_page(self):
        # Sample data for testing
        test_data = [i for i in range(1, 6)]  # 5 items

        # Test parameters
        page = 5
        limit = 2

        # Execute pagination
        result = await Pagination.execute(test_data, page, limit)

        # Check the results
        assert result.items == []
        assert result.state.page == page
        assert result.state.size == limit
        assert result.state.total_pages == 3
        assert result.state.total_items == 5
