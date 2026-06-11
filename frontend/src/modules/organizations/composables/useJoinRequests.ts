import { computed, reactive, ref } from "vue";

import { ORGANIZATION_EMPTY_STATES, ORGANIZATION_TABLE_CONFIGS } from "../data";
import { mapOrganizationError } from "../mappers";
import {
    approveJoinRequest,
    loadJoinRequestDetails,
    loadJoinRequests,
    rejectJoinRequest,
} from "../services";
import {
    createEmptyJoinRequestReviewForm,
    createJoinRequestsQuery,
} from "../utils";
import type {
    JoinRequestDto,
    JoinRequestId,
    JoinRequestListItemView,
    JoinRequestReviewFormModel,
    OrganizationDetailsView,
    OrganizationFiltersState,
    OrganizationPaginationState,
} from "../types";

const DEFAULT_PAGE_SIZE = 10;

function createInitialFilters(): OrganizationFiltersState {
    return {
        search: "",
        organizationId: null,
        departmentId: null,
        groupId: null,
        subjectId: null,
        teacherId: null,
        status: "",
        isActive: null,
        isPrimary: null,
        isPublic: null,
    };
}

function createInitialPagination(): OrganizationPaginationState {
    return {
        page: 1,
        pageSize: DEFAULT_PAGE_SIZE,
        totalCount: 0,
        hasNext: false,
        hasPrevious: false,
    };
}

export function useJoinRequests() {
    const items = ref<JoinRequestDto[]>([]);
    const viewItems = ref<JoinRequestListItemView[]>([]);
    const selectedItem = ref<JoinRequestDto | null>(null);
    const selectedDetails = ref<OrganizationDetailsView | null>(null);

    const filters = reactive<OrganizationFiltersState>(createInitialFilters());
    const pagination = reactive<OrganizationPaginationState>(
        createInitialPagination(),
    );

    const reviewForm = reactive<JoinRequestReviewFormModel>(
        createEmptyJoinRequestReviewForm(),
    );

    const isLoading = ref(false);
    const isDetailsLoading = ref(false);
    const isReviewSubmitting = ref(false);
    const errorMessage = ref("");
    const fieldErrors = ref<Record<string, string>>({});

    const tableConfig = computed(() => {
        return ORGANIZATION_TABLE_CONFIGS.joinRequests;
    });

    const emptyState = computed(() => {
        return ORGANIZATION_EMPTY_STATES.joinRequests;
    });

    const hasItems = computed(() => {
        return viewItems.value.length > 0;
    });

    const canGoPrevious = computed(() => {
        return pagination.hasPrevious && pagination.page > 1;
    });

    const canGoNext = computed(() => {
        return pagination.hasNext;
    });

    async function loadItems(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const query = createJoinRequestsQuery(filters, pagination);
            const result = await loadJoinRequests(query);

            items.value = result.items;
            viewItems.value = result.viewItems;
            pagination.totalCount = result.totalCount;
            pagination.hasNext = result.hasNext;
            pagination.hasPrevious = result.hasPrevious;
        } catch (error) {
            errorMessage.value = mapOrganizationError(error).message;
        } finally {
            isLoading.value = false;
        }
    }

    async function loadDetails(id: JoinRequestId): Promise<void> {
        isDetailsLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await loadJoinRequestDetails(id);

            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            replaceLocalItem(result.item, result.viewItem);
        } catch (error) {
            errorMessage.value = mapOrganizationError(error).message;
        } finally {
            isDetailsLoading.value = false;
        }
    }

    async function approveItem(id: JoinRequestId): Promise<void> {
        await runReviewAction(async () => {
            const result = await approveJoinRequest(id, reviewForm);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            resetReviewForm();
        });
    }

    async function rejectItem(id: JoinRequestId): Promise<void> {
        await runReviewAction(async () => {
            const result = await rejectJoinRequest(id, reviewForm);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            resetReviewForm();
        });
    }

    function setSearch(value: string): void {
        filters.search = value;
    }

    function submitSearch(): void {
        pagination.page = 1;
        void loadItems();
    }

    function setOrganizationFilter(value: number | null): void {
        filters.organizationId = value;
        pagination.page = 1;
        void loadItems();
    }

    function setDepartmentFilter(value: number | null): void {
        filters.departmentId = value;
        pagination.page = 1;
        void loadItems();
    }

    function setGroupFilter(value: number | null): void {
        filters.groupId = value;
        pagination.page = 1;
        void loadItems();
    }

    function setStatusFilter(value: string): void {
        filters.status = value;
        pagination.page = 1;
        void loadItems();
    }

    function resetFilters(): void {
        Object.assign(filters, createInitialFilters());
        pagination.page = 1;
        void loadItems();
    }

    function goPrevious(): void {
        if (!canGoPrevious.value) {
            return;
        }

        pagination.page -= 1;
        void loadItems();
    }

    function goNext(): void {
        if (!canGoNext.value) {
            return;
        }

        pagination.page += 1;
        void loadItems();
    }

    function selectItem(id: JoinRequestId): void {
        void loadDetails(id);
    }

    function clearSelection(): void {
        selectedItem.value = null;
        selectedDetails.value = null;
    }

    function setReviewComment(value: string): void {
        reviewForm.comment = value;
    }

    function resetReviewForm(): void {
        Object.assign(reviewForm, createEmptyJoinRequestReviewForm());
        fieldErrors.value = {};
    }

    async function runReviewAction(action: () => Promise<void>): Promise<void> {
        isReviewSubmitting.value = true;
        errorMessage.value = "";
        fieldErrors.value = {};

        try {
            await action();
        } catch (error) {
            const mappedError = mapOrganizationError(error);

            errorMessage.value = mappedError.message;
            fieldErrors.value = mappedError.fields;
        } finally {
            isReviewSubmitting.value = false;
        }
    }

    function replaceLocalItem(
        item: JoinRequestDto,
        viewItem: JoinRequestListItemView,
    ): void {
        const itemIndex = items.value.findIndex((currentItem) => {
            return currentItem.id === item.id;
        });

        const viewItemIndex = viewItems.value.findIndex((currentItem) => {
            return currentItem.id === viewItem.id;
        });

        if (itemIndex === -1) {
            items.value = [item, ...items.value];
        } else {
            items.value.splice(itemIndex, 1, item);
        }

        if (viewItemIndex === -1) {
            viewItems.value = [viewItem, ...viewItems.value];
        } else {
            viewItems.value.splice(viewItemIndex, 1, viewItem);
        }
    }

    return {
        canGoNext,
        canGoPrevious,
        emptyState,
        errorMessage,
        fieldErrors,
        filters,
        hasItems,
        isDetailsLoading,
        isLoading,
        isReviewSubmitting,
        items,
        pagination,
        reviewForm,
        selectedDetails,
        selectedItem,
        tableConfig,
        viewItems,
        approveItem,
        clearSelection,
        goNext,
        goPrevious,
        loadDetails,
        loadItems,
        rejectItem,
        resetFilters,
        resetReviewForm,
        selectItem,
        setDepartmentFilter,
        setGroupFilter,
        setOrganizationFilter,
        setReviewComment,
        setSearch,
        setStatusFilter,
        submitSearch,
    };
}
