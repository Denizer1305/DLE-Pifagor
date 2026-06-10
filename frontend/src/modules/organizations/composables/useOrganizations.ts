import { computed, reactive, ref } from "vue";

import { ORGANIZATION_EMPTY_STATES, ORGANIZATION_TABLE_CONFIGS } from "../data";
import { mapOrganizationError } from "../mappers";
import {
    clearOrganizationTeacherRegistrationCode,
    createOrganization,
    disableOrganizationTeacherRegistrationCode,
    loadOrganizationDetails,
    loadOrganizations,
    removeOrganization,
    restoreOrganizationById,
    saveTeacherRegistrationCode,
    updateOrganization,
} from "../services";
import {
    createEmptyCodeForm,
    createEmptyOrganizationForm,
    createOrganizationsQuery,
} from "../utils";
import type {
    CodeFormModel,
    OrganizationDetailsView,
    OrganizationDto,
    OrganizationFiltersState,
    OrganizationFormModel,
    OrganizationId,
    OrganizationListItemView,
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

export function useOrganizations() {
    const items = ref<OrganizationDto[]>([]);
    const viewItems = ref<OrganizationListItemView[]>([]);
    const selectedItem = ref<OrganizationDto | null>(null);
    const selectedDetails = ref<OrganizationDetailsView | null>(null);

    const filters = reactive<OrganizationFiltersState>(createInitialFilters());
    const pagination = reactive<OrganizationPaginationState>(
        createInitialPagination(),
    );

    const form = reactive<OrganizationFormModel>(
        createEmptyOrganizationForm(),
    );
    const codeForm = reactive<CodeFormModel>(
        createEmptyCodeForm(),
    );

    const isLoading = ref(false);
    const isDetailsLoading = ref(false);
    const isSubmitting = ref(false);
    const isActionLoading = ref(false);
    const errorMessage = ref("");
    const fieldErrors = ref<Record<string, string>>({});
    const generatedTeacherCode = ref("");

    const tableConfig = computed(() => {
        return ORGANIZATION_TABLE_CONFIGS.organizations;
    });

    const emptyState = computed(() => {
        return ORGANIZATION_EMPTY_STATES.organizations;
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
            const query = createOrganizationsQuery(filters, pagination);
            const result = await loadOrganizations(query);

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

    async function loadDetails(id: OrganizationId): Promise<void> {
        isDetailsLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await loadOrganizationDetails(id);

            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            replaceLocalItem(result.item, result.viewItem);
        } catch (error) {
            errorMessage.value = mapOrganizationError(error).message;
        } finally {
            isDetailsLoading.value = false;
        }
    }

    async function createItem(): Promise<void> {
        isSubmitting.value = true;
        errorMessage.value = "";
        fieldErrors.value = {};

        try {
            const result = await createOrganization(form);

            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            prependLocalItem(result.item, result.viewItem);
            resetForm();
        } catch (error) {
            const mappedError = mapOrganizationError(error);

            errorMessage.value = mappedError.message;
            fieldErrors.value = mappedError.fields;
        } finally {
            isSubmitting.value = false;
        }
    }

    async function updateItem(id: OrganizationId): Promise<void> {
        isSubmitting.value = true;
        errorMessage.value = "";
        fieldErrors.value = {};

        try {
            const result = await updateOrganization(id, form);

            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            replaceLocalItem(result.item, result.viewItem);
        } catch (error) {
            const mappedError = mapOrganizationError(error);

            errorMessage.value = mappedError.message;
            fieldErrors.value = mappedError.fields;
        } finally {
            isSubmitting.value = false;
        }
    }

    async function deactivateItem(id: OrganizationId): Promise<void> {
        await runItemAction(async () => {
            const result = await removeOrganization(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function restoreItem(id: OrganizationId): Promise<void> {
        await runItemAction(async () => {
            const result = await restoreOrganizationById(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function saveTeacherCode(id: OrganizationId): Promise<void> {
        await runItemAction(async () => {
            const response = await saveTeacherRegistrationCode(id, codeForm);
            const result = await loadOrganizationDetails(response.organization.id);

            generatedTeacherCode.value = response.raw_code;
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            replaceLocalItem(result.item, result.viewItem);
            Object.assign(codeForm, createEmptyCodeForm());
        });
    }

    async function disableTeacherCode(id: OrganizationId): Promise<void> {
        await runItemAction(async () => {
            const result = await disableOrganizationTeacherRegistrationCode(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function clearTeacherCode(id: OrganizationId): Promise<void> {
        await runItemAction(async () => {
            const result = await clearOrganizationTeacherRegistrationCode(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    function setSearch(value: string): void {
        filters.search = value;
    }

    function submitSearch(): void {
        pagination.page = 1;
        void loadItems();
    }

    function setActiveFilter(value: boolean | null): void {
        filters.isActive = value;
        pagination.page = 1;
        void loadItems();
    }

    function setPublicFilter(value: boolean | null): void {
        filters.isPublic = value;
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

    function selectItem(id: OrganizationId): void {
        void loadDetails(id);
    }

    function clearSelection(): void {
        selectedItem.value = null;
        selectedDetails.value = null;
    }

    function fillForm(item: OrganizationDto): void {
        form.name = item.name;
        form.shortName = item.short_name;
        form.slug = item.slug;
        form.code = item.code;
        form.description = item.description;
        form.city = item.city;
        form.address = item.address;
        form.phone = item.phone;
        form.email = item.email;
        form.website = item.website;
        form.isPublic = item.is_public;
        form.isDefaultPublic = item.is_default_public;
    }

    function resetForm(): void {
        Object.assign(form, createEmptyOrganizationForm());
        fieldErrors.value = {};
    }

    function resetCodeForm(): void {
        Object.assign(codeForm, createEmptyCodeForm());
        generatedTeacherCode.value = "";
    }

    async function runItemAction(action: () => Promise<void>): Promise<void> {
        isActionLoading.value = true;
        errorMessage.value = "";

        try {
            await action();
        } catch (error) {
            errorMessage.value = mapOrganizationError(error).message;
        } finally {
            isActionLoading.value = false;
        }
    }

    function prependLocalItem(
        item: OrganizationDto,
        viewItem: OrganizationListItemView,
    ): void {
        items.value = [
            item,
            ...items.value.filter((currentItem) => {
                return currentItem.id !== item.id;
            }),
        ];

        viewItems.value = [
            viewItem,
            ...viewItems.value.filter((currentItem) => {
                return currentItem.id !== viewItem.id;
            }),
        ];

        pagination.totalCount += 1;
    }

    function replaceLocalItem(
        item: OrganizationDto,
        viewItem: OrganizationListItemView,
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
        codeForm,
        emptyState,
        errorMessage,
        fieldErrors,
        filters,
        form,
        generatedTeacherCode,
        hasItems,
        isActionLoading,
        isDetailsLoading,
        isLoading,
        isSubmitting,
        items,
        pagination,
        selectedDetails,
        selectedItem,
        tableConfig,
        viewItems,
        clearSelection,
        clearTeacherCode,
        createItem,
        deactivateItem,
        disableTeacherCode,
        fillForm,
        goNext,
        goPrevious,
        loadDetails,
        loadItems,
        resetCodeForm,
        resetFilters,
        resetForm,
        restoreItem,
        saveTeacherCode,
        selectItem,
        setActiveFilter,
        setPublicFilter,
        setSearch,
        submitSearch,
        updateItem,
    };
}
