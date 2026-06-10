<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import DepartmentDetailsPanel from "../components/departments/DepartmentDetailsPanel.vue";
import DepartmentForm from "../components/departments/DepartmentForm.vue";
import DepartmentListTable from "../components/departments/DepartmentListTable.vue";
import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationFiltersPanel from "../components/shared/OrganizationFiltersPanel.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import { useDepartments, useOrganizationDictionaries } from "../composables";
import type {
    DepartmentDto,
    DepartmentId,
    DepartmentListItemView,
    OrganizationTableActionKey,
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
    setOrganizationFilter,
    setSearch,
    submitSearch,
    updateItem,
} = useDepartments();

const {
    organizationOptions,
    reloadDictionaries,
} = useOrganizationDictionaries();

const isFiltersOpen = ref(false);
const isFormModalOpen = ref(false);
const formMode = ref<FormMode>("create");

const organizationFilterOptions = computed(() => [
    {
        label: "Все организации",
        value: "",
    },
    ...organizationOptions.value.map((option) => ({
        label: option.label,
        value: String(option.value),
    })),
]);

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
    return Boolean(
        filters.search
        || filters.organizationId
        || filters.isActive !== null,
    );
});

function updateFormModel(value: typeof form): void {
    Object.assign(form, value);
}

function openCreateForm(): void {
    formMode.value = "create";
    resetForm();
    isFormModalOpen.value = true;
}

async function openEditForm(id?: DepartmentId): Promise<void> {
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

async function selectAndWaitDetails(id: DepartmentId): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item: DepartmentDto) => item.id === id);

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
    item: DepartmentListItemView;
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

function handleOrganizationChange(value: string): void {
    setOrganizationFilter(value ? Number(value) : null);
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
        search-placeholder="Поиск по названию или коду отделения"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Фильтры"
        refresh-label="Обновить"
        create-label="Создать отделение"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <template #filters>
            <OrganizationFiltersPanel
                title="Фильтры отделений"
                text="Ограничьте список по организации и активности."
                reset-label="Сбросить"
                :is-collapsed="!isFiltersOpen"
                @reset="() => {
                    setOrganizationFilter(null);
                    setActiveFilter(null);
                }"
            >
                <div class="org-filters__field">
                    <span class="org-filters__label">Организация</span>

                    <BaseSelect
                        :model-value="filters.organizationId ? String(filters.organizationId) : ''"
                        :options="organizationFilterOptions"
                        placeholder="Все организации"
                        aria-label="Фильтр по организации"
                        @update:model-value="handleOrganizationChange"
                    />
                </div>

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

        <DepartmentListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка отделения"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные отделения..."
                />

                <DepartmentDetailsPanel
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
        :title="formMode === 'create' ? 'Создание отделения' : 'Редактирование отделения'"
        @close="closeFormModal"
    >
        <DepartmentForm
            :model-value="form"
            :organization-options="organizationOptions"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новое отделение' : 'Данные отделения'"
            text="Заполните организацию, название и код отделения."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отмена"
            :is-submitting="isSubmitting"
            @update:model-value="updateFormModel"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>
</template>
