import { computed, reactive, ref } from "vue";

import { ORGANIZATION_EMPTY_STATES, ORGANIZATION_TABLE_CONFIGS } from "../data";
import { mapOrganizationError } from "../mappers";
import {
    createTeacherSubject,
    loadTeacherSubjectDetails,
    loadTeacherSubjects,
    makePrimaryTeacherSubject,
    removeTeacherSubject,
    restoreTeacherSubjectById,
    updateTeacherSubject,
} from "../services";
import {
    createEmptyTeacherSubjectForm,
    createTeacherSubjectsQuery,
} from "../utils";
import type {
    OrganizationDetailsView,
    OrganizationFiltersState,
    OrganizationPaginationState,
    TeacherSubjectDto,
    TeacherSubjectFormModel,
    TeacherSubjectId,
    TeacherSubjectListItemView,
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

export function useTeacherSubjects() {
    const items = ref<TeacherSubjectDto[]>([]);
    const viewItems = ref<TeacherSubjectListItemView[]>([]);
    const selectedItem = ref<TeacherSubjectDto | null>(null);
    const selectedDetails = ref<OrganizationDetailsView | null>(null);

    const filters = reactive<OrganizationFiltersState>(createInitialFilters());
    const pagination = reactive<OrganizationPaginationState>(
        createInitialPagination(),
    );

    const form = reactive<TeacherSubjectFormModel>(
        createEmptyTeacherSubjectForm(),
    );

    const isLoading = ref(false);
    const isDetailsLoading = ref(false);
    const isSubmitting = ref(false);
    const isActionLoading = ref(false);
    const errorMessage = ref("");
    const fieldErrors = ref<Record<string, string>>({});

    const tableConfig = computed(() => {
        return ORGANIZATION_TABLE_CONFIGS.teacherSubjects;
    });

    const emptyState = computed(() => {
        return ORGANIZATION_EMPTY_STATES.teacherSubjects;
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
            const query = createTeacherSubjectsQuery(filters, pagination);
            const result = await loadTeacherSubjects(query);

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

    async function loadDetails(id: TeacherSubjectId): Promise<void> {
        isDetailsLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await loadTeacherSubjectDetails(id);

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
            const result = await createTeacherSubject(form);

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

    async function updateItem(id: TeacherSubjectId): Promise<void> {
        isSubmitting.value = true;
        errorMessage.value = "";
        fieldErrors.value = {};

        try {
            const result = await updateTeacherSubject(id, form);

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

    async function deactivateItem(id: TeacherSubjectId): Promise<void> {
        await runItemAction(async () => {
            const result = await removeTeacherSubject(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function restoreItem(id: TeacherSubjectId): Promise<void> {
        await runItemAction(async () => {
            const result = await restoreTeacherSubjectById(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
        });
    }

    async function setPrimaryItem(id: TeacherSubjectId): Promise<void> {
        await runItemAction(async () => {
            const result = await makePrimaryTeacherSubject(id);

            replaceLocalItem(result.item, result.viewItem);
            selectedItem.value = result.item;
            selectedDetails.value = result.details;
            await loadItems();
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

    function setTeacherFilter(value: number | null): void {
        filters.teacherId = value;
        pagination.page = 1;
        void loadItems();
    }

    function setSubjectFilter(value: number | null): void {
        filters.subjectId = value;
        pagination.page = 1;
        void loadItems();
    }

    function setActiveFilter(value: boolean | null): void {
        filters.isActive = value;
        pagination.page = 1;
        void loadItems();
    }

    function setPrimaryFilter(value: boolean | null): void {
        filters.isPrimary = value;
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

    function selectItem(id: TeacherSubjectId): void {
        void loadDetails(id);
    }

    function clearSelection(): void {
        selectedItem.value = null;
        selectedDetails.value = null;
    }

    function fillForm(item: TeacherSubjectDto): void {
        form.teacherId = item.teacher;
        form.subjectId = item.subject.id;
        form.isPrimary = item.is_primary;
        form.isActive = item.is_active;
        form.notes = item.notes;
    }

    function resetForm(): void {
        Object.assign(form, createEmptyTeacherSubjectForm());
        fieldErrors.value = {};
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
        item: TeacherSubjectDto,
        viewItem: TeacherSubjectListItemView,
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
        item: TeacherSubjectDto,
        viewItem: TeacherSubjectListItemView,
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
        clearSelection,
        createItem,
        deactivateItem,
        fillForm,
        goNext,
        goPrevious,
        loadDetails,
        loadItems,
        resetFilters,
        resetForm,
        restoreItem,
        selectItem,
        setActiveFilter,
        setOrganizationFilter,
        setPrimaryFilter,
        setPrimaryItem,
        setSearch,
        setSubjectFilter,
        setTeacherFilter,
        submitSearch,
        updateItem,
    };
}
