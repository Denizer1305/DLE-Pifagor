<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationFiltersPanel from "../components/shared/OrganizationFiltersPanel.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import SubjectDetailsPanel from "../components/subjects/SubjectDetailsPanel.vue";
import SubjectForm from "../components/subjects/SubjectForm.vue";
import SubjectListTable from "../components/subjects/SubjectListTable.vue";
import { useOrganizationDictionaries, useSubjects } from "../composables";
import type {
    OrganizationTableActionKey,
    SubjectDto,
    SubjectId,
    SubjectListItemView,
} from "../types";

type FormMode = "create" | "edit";

const {
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
    selectedDetails,
    selectedItem,
    tableConfig,
    viewItems,
    clearSelection,
    createItem,
    deactivateItem,
    fillForm,
    loadDetails,
    loadItems,
    resetForm,
    restoreItem,
    selectItem,
    setActiveFilter,
    setSearch,
    submitSearch,
    updateItem,
} = useSubjects();

const { reloadDictionaries } = useOrganizationDictionaries();
const isFiltersOpen = ref(false);
const isFormModalOpen = ref(false);
const formMode = ref<FormMode>("create");

const activeFilterOptions = [
    {
        label: "Все",
        value: "",
    },
    {
        label: "Активные",
        value: "true",
    },
    {
        label: "Неактивные",
        value: "false",
    },
];

const hasActiveFilters = computed(() => {
    return Boolean(filters.search || filters.isActive !== null);
});

function updateFormModel(value: typeof form): void {
    Object.assign(form, value);
}

function openCreateForm(): void {
    formMode.value = "create";
    resetForm();
    isFormModalOpen.value = true;
}

async function openEditForm(id?: SubjectId): Promise<void> {
    formMode.value = "edit";

    if (id) {
        await selectAndWaitDetails(id);
    } else if (selectedItem.value) {
        fillForm(selectedItem.value);
    }

    isFormModalOpen.value = true;
}

function closeFormModal(): void {
    isFormModalOpen.value = false;
    resetForm();
}

async function submitForm(): Promise<void> {
    if (formMode.value === "create") {
        await createItem();
    } else if (selectedItem.value) {
        await updateItem(selectedItem.value.id);
    }

    if (!Object.keys(fieldErrors.value).length) {
        await reloadDictionaries();
        isFormModalOpen.value = false;
    }
}

async function selectAndWaitDetails(id: SubjectId): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item: SubjectDto) => item.id === id);

    if (selectedItem.value) {
        fillForm(selectedItem.value);
        return;
    }

    if (localItem) {
        fillForm(localItem);
    }
}

function handleTableAction(payload: {
    actionKey: OrganizationTableActionKey;
    item: SubjectListItemView;
}): void {
    if (payload.actionKey === "details") {
        selectItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "edit") {
        void openEditForm(payload.item.id);
        return;
    }

    if (payload.actionKey === "deactivate") {
        void deactivateItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "restore") {
        void restoreItem(payload.item.id);
    }
}

function handleActiveFilterChange(value: string): void {
    setActiveFilter(value === "" ? null : value === "true");
}

onMounted(() => {
    void loadItems();
});
</script>

<template>
    <OrganizationWorkspace
        :search-value="filters.search"
        search-placeholder="Поиск по предмету или коду"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Фильтры"
        refresh-label="Обновить"
        create-label="Создать предмет"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <template #filters>
            <OrganizationFiltersPanel
                title="Фильтры предметов"
                text="Ограничьте список по активности."
                reset-label="Сбросить"
                :is-collapsed="!isFiltersOpen"
                @reset="setActiveFilter(null)"
            >
                <div class="org-filters__field">
                    <span class="org-filters__label">Активность</span>

                    <BaseSelect
                        :model-value="filters.isActive === null ? '' : String(filters.isActive)"
                        :options="activeFilterOptions"
                        placeholder="Все"
                        aria-label="Фильтр активности"
                        @update:model-value="handleActiveFilterChange"
                    />
                </div>
            </OrganizationFiltersPanel>
        </template>

        <SubjectListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка предмета"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные предмета..."
                />

                <SubjectDetailsPanel
                    v-else
                    :details="selectedDetails"
                    @edit="openEditForm()"
                    @close="clearSelection"
                />
            </OrganizationDetailsModal>
        </template>
    </OrganizationWorkspace>

    <OrganizationDetailsModal
        :is-open="isFormModalOpen"
        :title="formMode === 'create' ? 'Создание предмета' : 'Редактирование предмета'"
        @close="closeFormModal"
    >
        <SubjectForm
            :model-value="form"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новый предмет' : 'Данные предмета'"
            text="Заполните название, короткое имя и код учебного предмета."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отмена"
            :is-submitting="isSubmitting"
            @update:model-value="updateFormModel"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>
</template>
