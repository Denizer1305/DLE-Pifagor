import { computed, reactive, ref } from "vue";

import { ORGANIZATION_EMPTY_STATES, ORGANIZATION_TABLE_CONFIGS } from "../data";
import { mapOrganizationError } from "../mappers";
import {
    clearStudyGroupJoinCode,
    createStudyGroup,
    disableStudyGroupJoinCode,
    loadStudyGroupDetails,
    loadStudyGroups,
    removeStudyGroup,
    restoreStudyGroupById,
    saveGroupJoinCode,
    updateStudyGroup,
} from "../services";
import {
    createEmptyCodeForm,
    createEmptyStudyGroupForm,
    createStudyGroupsQuery,
} from "../utils";
import type {
    CodeFormModel,
    OrganizationDetailsView,
    OrganizationFiltersState,
    OrganizationPaginationState,
    StudyGroupDto,
    StudyGroupFormModel,
    StudyGroupId,
    StudyGroupListItemView,
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

export function useStudyGroups() {
    const items = ref<StudyGroupDto[]>([]);
    const viewItems = ref<StudyGroupListItemView[]>([]);
    const selectedItem = ref<StudyGroupDto | null>(null);
    const selectedDetails = ref<OrganizationDetailsView | null>(null);

    const filters = reactive<OrganizationFiltersState>(createInitialFilters());
    const pagination = reactive<OrganizationPaginationState>(
        createInitialPagination(),
    );

    const form = reactive<StudyGroupFormModel>(
        createEmptyStudyGroupForm(),
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

    const tableConfig = computed(() => {
        return ORGANIZATION_TABLE_CONFIGS.studyGroups;
    });

    const emptyState = computed(() => {
        return ORGANIZATION_EMPTY_STATES.studyGroups;
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
            const query = createStudyGroupsQuery(filters, pagination);
            const result = await loadStudyGroups(query);

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

    async function loadDetails(id: StudyGroupId): Promise<void> {
        isDetailsLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await loadStudyGroupDetails(id);

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
            const result = await createStudyGroup(form);

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

    async function updateItem(id: StudyGroupId): Promise<void> {
        isSubmitting.value = true;
        errorMessage.value = "";
        fieldErrors.value = {};

        try {
            const result = await updateStudyGroup(id, form);

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

    async function archiveItem(id: StudyGroupId): Promise<void> {
        await runItemAction(async () => {
            const result = await removeStudyGroup(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function restoreItem(id: StudyGroupId): Promise<void> {
        await runItemAction(async () => {
            const result = await restoreStudyGroupById(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function saveJoinCode(id: StudyGroupId): Promise<void> {
        await runItemAction(async () => {
            await saveGroupJoinCode(id, codeForm);
            await loadDetails(id);
            resetCodeForm();
        });
    }

    async function disableJoinCode(id: StudyGroupId): Promise<void> {
        await runItemAction(async () => {
            const result = await disableStudyGroupJoinCode(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function clearJoinCode(id: StudyGroupId): Promise<void> {
        await runItemAction(async () => {
            const result = await clearStudyGroupJoinCode(id);

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

    function setStatusFilter(value: string): void {
        filters.status = value;
        pagination.page = 1;
        void loadItems();
    }

    function setActiveFilter(value: boolean | null): void {
        filters.isActive = value;
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

    function selectItem(id: StudyGroupId): void {
        void loadDetails(id);
    }

    function clearSelection(): void {
        selectedItem.value = null;
        selectedDetails.value = null;
    }

    function fillForm(item: StudyGroupDto): void {
        form.organizationId = item.organization.id;
        form.departmentId = item.department?.id ?? null;
        form.name = item.name;
        form.code = item.code;
        form.description = item.description ?? "";
        form.admissionYear = item.admission_year;
        form.graduationYear = item.graduation_year;
        form.courseNumber = item.course_number ?? null;
        form.studyForm = item.study_form ?? "full_time";
        form.status = item.status;
    }

    function resetForm(): void {
        Object.assign(form, createEmptyStudyGroupForm());
        fieldErrors.value = {};
    }

    function resetCodeForm(): void {
        Object.assign(codeForm, createEmptyCodeForm());
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
        item: StudyGroupDto,
        viewItem: StudyGroupListItemView,
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
        item: StudyGroupDto,
        viewItem: StudyGroupListItemView,
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
        archiveItem,
        clearJoinCode,
        clearSelection,
        createItem,
        disableJoinCode,
        fillForm,
        goNext,
        goPrevious,
        loadDetails,
        loadItems,
        resetCodeForm,
        resetFilters,
        resetForm,
        restoreItem,
        saveJoinCode,
        selectItem,
        setActiveFilter,
        setDepartmentFilter,
        setOrganizationFilter,
        setSearch,
        setStatusFilter,
        submitSearch,
        updateItem,
    };
}
