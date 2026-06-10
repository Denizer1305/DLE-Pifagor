import { computed, reactive, ref } from "vue";

import { adminUsersPageContent } from "@/modules/admin/data/admin-users.data";
import { getAdminUsersList } from "@/modules/admin/services/admin-users.service";
import type {
    AdminUserRoleGroup,
    AdminUsersFilters,
    AdminUsersListModel,
} from "@/modules/admin/types/admin-users.types";

function createEmptyModel(): AdminUsersListModel {
    return {
        ...adminUsersPageContent.pages.all,
        emptyTitle: adminUsersPageContent.emptyTitle,
        emptyText: adminUsersPageContent.emptyText,
        totalLabel: adminUsersPageContent.totalLabel,
        items: [],
        summary: [],
        total: 0,
        currentPage: 1,
        totalPages: 1,
        hasNext: false,
        hasPrevious: false,
    };
}

export function useAdminUsers(roleGroup: AdminUserRoleGroup = "") {
    const filters = reactive<AdminUsersFilters>({
        roleGroup,
        search: "",
        status: "",
        ordering: "last_name",
        page: 1,
        pageSize: 5,
    });
    const model = ref<AdminUsersListModel>(createEmptyModel());
    const isLoading = ref(false);
    const errorMessage = ref("");

    const canGoPrevious = computed(() => model.value.hasPrevious && filters.page > 1);
    const canGoNext = computed(() => model.value.hasNext);

    async function loadUsers(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            model.value = await getAdminUsersList(filters);
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось загрузить пользователей.";
        } finally {
            isLoading.value = false;
        }
    }

    function setSearch(value: string): void {
        filters.search = value;
    }

    function setFilter(key: "status" | "ordering", value: string): void {
        filters[key] = value;
        filters.page = 1;
        void loadUsers();
    }

    function submitSearch(): void {
        filters.page = 1;
        void loadUsers();
    }

    function resetFilters(): void {
        filters.search = "";
        filters.status = "";
        filters.ordering = "last_name";
        filters.page = 1;
        void loadUsers();
    }

    function goPrevious(): void {
        if (!canGoPrevious.value) {
            return;
        }

        filters.page -= 1;
        void loadUsers();
    }

    function goNext(): void {
        if (!canGoNext.value) {
            return;
        }

        filters.page += 1;
        void loadUsers();
    }

    return {
        content: adminUsersPageContent,
        canGoNext,
        canGoPrevious,
        errorMessage,
        filters,
        isLoading,
        model,
        goNext,
        goPrevious,
        loadUsers,
        resetFilters,
        setFilter,
        setSearch,
        submitSearch,
    };
}
